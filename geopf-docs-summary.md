# Géoplateforme (GPF) — Developer Summary

API base: `https://data.geopf.fr/api`  
Swagger: `https://data.geopf.fr/api/swagger-ui/index.html`

---

## [Platform concepts](https://geoplateforme.github.io/entrepot/production/concepts/)

The platform is built around a strict entity hierarchy that governs how data moves from raw files to publicly accessible services. Understanding the chain — from the entrepôt down to the offering — is essential before calling any API endpoint, because every object exists in relation to its parent entities. Several concepts (livraison quotas, layer_name uniqueness, permission/access separation) are easy to get wrong and hard to debug without this mental model.

- Core entity chain: user → organization → community → datastore (entrepôt) → upload (livraison) → processing execution → stored_data → configuration → offering → endpoint
- A **community** is the organizational unit; every community that produces data is backed by a **datastore** (entrepôt), which has allocated quotas for storage, processings, checks, and endpoints
- **livraison** is a temporary landing zone; files are uploaded then the livraison is closed, triggering automatic checks; it must be deleted after processing to reclaim upload-quota
- **stored_data** types: `VECTOR-DB` (PostgreSQL/PostGIS), `ROK4-PYRAMID-RASTER` (S3), `ROK4-PYRAMID-VECTOR` (S3), `ARCHIVE` (S3), `INDEX` (OpenSearch)
- **configuration** describes how a stored_data is served (layer name, style references, bbox, relations); its `layer_name` must be **globally unique across the entire platform** for a given configuration type
- **offering** (offre) links a configuration to an endpoint; creating an offering triggers publication to the diffusion servers; the `available` boolean toggles access without touching permissions
- **static files** are server-side assets (SLD styles, FreeMarker templates, ROK4 styles, SQL derivation scripts) uploaded to the entrepôt; **annexes** are client-facing hosted files (thumbnails, legends, capabilities) served publicly at `https://data.geopf.fr/annexes/{technical_name}/{path}`
- **permissions** and **accesses** form the access-control layer for non-open offerings: a permission grants a user/community rights on one or more offerings; an access links a key to an offering via a permission

---

## [Platform components](https://geoplateforme.github.io/entrepot/production/composants/)

This section maps the logical concepts to the concrete infrastructure: which server handles which protocol, which storage backend holds which stored_data type, and where each service is reachable. Knowing the component layout helps when debugging publishing failures or configuring clients that need direct endpoint URLs.

- Open diffusion endpoints: WFS `https://data.geopf.fr/wfs`, WMS-Vector `https://data.geopf.fr/wms-v`, WMS-Raster `https://data.geopf.fr/wms-r`, WMTS `https://data.geopf.fr/wmts`, TMS `https://data.geopf.fr/tms`, vector-TMS catalog `https://data.geopf.fr/vector-tms/1.0.0/index.json`, download `https://data.geopf.fr/telechargement`, CSW `https://data.geopf.fr/csw`
- Private (access-controlled) variants of all the above live under `https://data.geopf.fr/private/`
- Internal storage stack: S3 (OpenIO) for raster pyramids, archives, and annexes; PostgreSQL+PostGIS for vector stored_data; OpenSearch for search indexes; GitLab is used as workflow orchestrator for processing executions
- Diffusion servers: Geoserver (WFS, WMS-Vector), ROK4 (WMS-Raster, WMTS/TMS), pg_tileserv (VECTOR-TMS on-the-fly)
- Additional services: altimetry at `https://data.geopf.fr/altimetrie/`, extraction (OGC API Processes) at `https://data.geopf.fr/extraction/`, validation at `https://data.geopf.fr/validation/api/`, search at `https://data.geopf.fr/recherche/`

---

## [Auth & access control](https://geoplateforme.github.io/tutoriels/production/controle-des-acces/)

Authentication on the Géoplateforme is Keycloak-based with TOTP at every login, and the access-control model (keys → accesses → permissions → offerings) is separate from community membership rights. Both layers must be configured correctly for a private service to be consumable, and several details (TOTP seed extraction, key types, `only_oauth` flag) are not obvious from the API alone.

- Self-registration: `https://sso.geopf.fr/realms/geoplateforme/account/`; username convention is `{prenom}.{nom}` lowercase; a TOTP app is required during registration (FreeOTP on mobile)
- SSO: Keycloak at `https://sso.geopf.fr/realms/geoplateforme/`; TOTP required at every login; SDK note: FreeOTP does not expose the raw TOTP key — use Aegis instead to extract `totp_key` for the SDK config
- `GET /users/me` returns user info, community memberships, and per-community rights (`ANNEX`, `UPLOAD`, `BROADCAST`, `PROCESSING`, `COMMUNITY`); all datastore IDs appear in this response
- Three key (clé) types for service consumption: `HASH` (pass as `api_key` query param or `X-Key` / `apikey` header), `BASIC` (HTTP Basic), `OAUTH2` (one per account; strong auth); keys are scoped per user, not per datastore
- Key → access → permission chain: `POST /users/me/keys` → `POST /users/me/keys/{key}/accesses` with a `{permission, offerings[]}` body
- `only_oauth: true` on a permission forces consumers to use their OAUTH2 key; HASH/BASIC keys cannot consume that offering
- QGIS OAUTH2 config: auth URL `https://sso.geopf.fr/realms/geoplateforme/protocol/openid-connect/auth`, token URL `…/token`, client ID `qgis`, secret `F77z01QHTaJClBJ1p2OZYkFGL24XYLti`
- Community rights are coarse-grained (route-level, not entity-level); even a member with no rights can read most entities; `COMMUNITY` right is required to list members

---

## [Vector data — livraison](https://geoplateforme.github.io/tutoriels/production/vecteur/base/livraison/)

Livraison → VECTOR-DB → configuration → offering

The livraison is the entry point for all vector data: files are uploaded in an open upload, then the upload is closed to trigger automatic format and integrity checks before any processing can start. Getting the format, SRS declaration, and file layout right at this stage avoids failures later in the pipeline that are harder to diagnose.

- Accepted formats: GeoPackage, GeoJSON, Shapefile, CSV (geometry in `WKT` column, CRS in `crs` column), SQL (DDL only; no schema qualifiers in CREATE TABLE)
- Flow: `POST /datastores/{datastore}/uploads` (type=VECTOR, srs=EPSG:xxxx) → `PUT .../data?path=` (multipart per file) → `GET .../tree` (verify) → `POST .../close` → poll `GET .../checks`
- Upload status goes OPEN → CLOSED after `/close`; checks run automatically; delete the upload after successful integration to free quota
- CSV requires exact column names for geometry (`WKT`) and CRS (`crs`); SQL files must not reference schema names (the platform has its own schema layout)

---

## [Vector data — integration](https://geoplateforme.github.io/tutoriels/production/vecteur/base/integration/)

Integration is the processing step that converts a closed livraison into a VECTOR-DB stored_data in PostgreSQL/PostGIS, making the data queryable and publishable. Table and column names are normalized during this step, and multi-geometry tables require explicit declaration — both details matter for correctly referencing fields downstream in styles, configurations, and update operations.

- Processing UUID (vector integration): `0de8c60b-9938-4be9-aa36-9026b77c3c96`
- Output type: `VECTOR-DB` on `POSTGRESQL` storage
- Table/column names are normalized at integration time: lowercased, accents stripped, hyphens removed; the normalized names are what appear in WFS/WMS services
- Multi-geometry tables require explicit `"multigeom_layers": ["table_name"]` parameter in the execution body; otherwise the integration will fail or silently drop geometries
- Launch execution: `POST /datastores/{datastore}/processings/executions` then `POST .../executions/{execution}/launch`; poll status (CREATED → WAITING → PROGRESS → SUCCESS/FAILURE) via `GET .../executions/{execution}`

---

## [Vector data — WFS](https://geoplateforme.github.io/tutoriels/production/vecteur/base/wfs/)

The WFS configuration exposes a VECTOR-DB as an OGC Web Feature Service, with each table in the stored_data becoming a distinct feature type. The `layer_name` doubles as an XML namespace prefix, which affects how clients reference feature types and why its platform-wide uniqueness is important.

- Endpoint UUID (open WFS): `ae012611-13eb-4a18-8d04-9b7604a031cc`; URL: `https://data.geopf.fr/wfs`
- The `layer_name` of the WFS configuration becomes an XML namespace prefix; each table in the stored_data is exposed as `{layer_name}:{table_name}`
- Default feature limit per request: 1000; clients must paginate with `startIndex` for larger datasets
- Configuration body requires `type_infos.used_data[].relations` array with `native_name`, `title`, `abstract`, and optional `keywords` per table

---

## [Vector data — WMS-VECTOR](https://geoplateforme.github.io/tutoriels/production/vecteur/base/wms/)

WMS-VECTOR serves a VECTOR-DB as a rendered map via Geoserver, requiring SLD styles and FreeMarker GetFeatureInfo templates uploaded as static files beforehand. Unlike WFS, WMS-VECTOR collapses all tables in the stored_data into a single output layer, so styling must account for all feature types in a single SLD.

- Endpoint UUID (open WMS-Vector): `ae022611-13eb-4a18-8d04-9b7604a031cc`; URL: `https://data.geopf.fr/wms-v`
- WMS-VECTOR configuration produces a single output layer even if the stored_data has multiple tables; each table requires a `GEOSERVER-STYLE` (SLD) static and a `GEOSERVER-FTL` (FreeMarker) static for GetFeatureInfo
- Statics are uploaded via `POST /datastores/{datastore}/statics` multipart; response includes `used_attributes` listing which attribute names the style references (useful for validating field mapping)

---

## [Vector data — VECTOR-TMS on-the-fly](https://geoplateforme.github.io/tutoriels/production/vecteur/base/tmsv/)

VECTOR-TMS serves a VECTOR-DB as Mapbox Vector Tiles on-the-fly via pg_tileserv, without a pre-tiling step — tiles are generated at request time directly from PostGIS. This makes it fast to publish but unsuitable for very large datasets where pre-calculated tiles (see next section) are preferable.

- Served by pg_tileserv; configuration type `VECTOR-TMS`; tiles at `https://data.geopf.fr/vector-tms/1.0.0/{layer_name}.{table}/{z}/{x}/{y}.pbf`
- Supports server-side filtering via query params: `?filter=<PostGIS WHERE clause>` and `?properties=col1,col2` for attribute projection
- The endpoint UUID for the VECTOR-TMS (pg_tileserv) service is **not documented** in the tutorials (the template rendering failed in the source: `{{ no such element: ... }}`); it must be retrieved from `GET /datastores/{datastore}` or requested from the platform

---

## [Vector data — pre-calculated TMS tiles](https://geoplateforme.github.io/tutoriels/production/vecteur/base/tuilage/)

Pre-calculated TMS tiles are generated from a VECTOR-DB using the tippecanoe-backed pyramid processing, producing a `ROK4-PYRAMID-VECTOR` on S3. This approach trades publish-time cost for runtime performance and is appropriate for large datasets or when client-side style control (Mapbox GL JSON) is needed.

- Processing UUID (vector pyramid): `aa5f9391-0bdb-4b97-9209-fcde351b82f6`; output type: `ROK4-PYRAMID-VECTOR` on S3
- `composition` parameter controls per-table tile generation: array of `{table, bottom_level, top_level, filter}` objects; uses tippecanoe internally
- Published via the WMTS-TMS endpoint; client-side style (Mapbox GL JSON) hosted as an annexe and referenced in the configuration
- Published tile URL pattern: `https://data.geopf.fr/tms/1.0.0/{layer_name}/{z}/{x}/{y}.pbf`

---

## [Vector data — static files](https://geoplateforme.github.io/tutoriels/production/vecteur/base/statique/)

Static files are server-side assets — SLD styles and FreeMarker templates — that must be uploaded to the entrepôt before a WMS-VECTOR configuration can reference them. The upload response's `used_attributes` field is the main tool for verifying that a style correctly maps to the normalized column names produced at integration time.

- Static types for vector: `GEOSERVER-STYLE` (SLD XML), `GEOSERVER-FTL` (FreeMarker HTML template for GetFeatureInfo)
- Upload: `POST /datastores/{datastore}/statics` multipart with fields `file`, `name`, `type`, `description`
- Response includes `used_attributes` — the list of data attributes the style or template references; verify these match the normalized column names from integration

---

## [Vector data — updates: delete/update](https://geoplateforme.github.io/tutoriels/production/vecteur/maj/delete-update/)

Partial updates (deletes and in-place updates of existing rows) are driven by special companion files delivered inside the same livraison as new data. The processing is the same vector integration UUID, but the execution parameters must explicitly opt in to delete/update mode — without those flags, the companion files are ignored.

- Partial update uses special CSV files delivered in the same upload as new data:
  - `{tablename}.delete` — each row specifies WHERE-clause column values; generates a DELETE per row
  - `{tablename}.update` — must include primary key column(s); generates UPDATE WHERE pk per row
- Processing execution parameters must include `"delete": true` and/or `"update": true` for these files to be processed
- Operations order within a single integration run: deletes → updates → inserts; ensures no conflicts from overlapping rows
- Primary key columns in `.update` files must exactly match the normalized (lowercased) column names

---

## [Vector data — updates: batch injection](https://geoplateforme.github.io/tutoriels/production/vecteur/maj/injection/)

Batch injection is the append-only update pattern: new files are delivered as a fresh livraison and integrated into an existing VECTOR-DB by targeting its UUID in the output block. The key distinction from a normal integration is using `output.stored_data.id` instead of `output.stored_data.name` — the API silently creates a new stored_data if you pass `name`, with no error.

- For append-only updates: deliver new files as a new upload, then run the same vector integration processing (`0de8c60b-9938-4be9-aa36-9026b77c3c96`) but with `"output": {"stored_data": {"id": "{existing_uuid}"}}` instead of a `"name"` key — this targets the existing VECTOR-DB and appends new rows; there is **no `mode` parameter**
- The stored_data extent is automatically updated to encompass all data across all injected batches after each run; no configuration or offering update is needed — WFS/WMS serve the new rows immediately
- Multiple sequential batches (e.g., CSV batch 1, CSV batch 2…) all target the same `stored_data.id`; files can be in any supported vector format
- Gotcha: if you pass `"name"` instead of `"id"` in the output block, the platform creates a brand-new VECTOR-DB instead of appending — there is no error; it silently produces a separate stored_data

---

## [Vector data — SQL derivation](https://geoplateforme.github.io/tutoriels/production/vecteur/derivation/)

SQL derivation lets you transform or enrich an existing VECTOR-DB using a Jinja2-templated SQL script uploaded as a `DERIVATION-SQL` static, without going through a new livraison cycle. It can operate in-place on the same stored_data or produce a new one, making it useful for computed columns, joins, or geometry transformations that aren't practical at upload time.

- Processing UUID (derivation): `2c18eda8-d30c-42ab-8760-ec16d8929de5`; uses a `DERIVATION-SQL` static file
- SQL file supports Jinja2-like templating: `{{ params.x }}` for free parameters, `{{ inputs.1 }}` / `{{ inputs.N }}` for referencing input stored_data tables by index
- Can modify the target stored_data **in-place** (same UUID) or produce a new one; the derivation can add/drop columns, join tables, compute new geometries
- After any structural schema change (add/drop column), all offerings pointing at that stored_data must be re-synced: `PUT /datastores/{datastore}/offerings/{offering}` to push the schema update to Geoserver

---

## [Raster data — livraison + pyramid](https://geoplateforme.github.io/tutoriels/production/raster/base/pyramide/)

Upload → ROK4-PYRAMID-RASTER → configuration → offering

Publishing raster data requires first delivering source imagery as a RASTER livraison, then running the raster pyramid processing to produce a `ROK4-PYRAMID-RASTER` stored_data tiled into the platform's S3 storage. Choices made here — compression, interpolation, and whether to enable masks — directly affect both visual quality and the ability to do incremental updates later.

- Upload type: `RASTER`; accepted formats: GeoTIFF (with optional .tfw world file), PNG, JPEG, JPEG2000; MNT/DEM formats: GeoTIFF only (no JPEG2000)
- Checks triggered on raster livraison close: "Vérification raster" (`a4060831-9c6f-42e2-9435-e07a4e8ef535`) and "Vérification standard" (`ecb00ba0-eb42-427e-8418-f5d8a30e84ec`)
- Processing UUID (raster pyramid): `2ae50661-986c-4f47-a3f0-e380417b522c`; output type: `ROK4-PYRAMID-RASTER` on S3
- Only TMS grid supported for standard imagery: `PM` (pseudo-Mercator / WebMercator EPSG:3857)
- Compression options: `jpg` (lossy, smaller), `png` (lossless); interpolation: `nn` (nearest-neighbor), `linear`, `bicubic`
- If the pyramid will later be fused or updated, set `"mask": true` in parameters — masks track nodata pixels and prevent bleeding when pyramids are composed

---

## [Raster data — WMTS/TMS](https://geoplateforme.github.io/tutoriels/production/raster/base/wmts-tms/)

The WMTS/TMS configuration publishes a `ROK4-PYRAMID-RASTER` through the ROK4 server, making it accessible to standard tile clients. Style references (ROK4 JSON palette files, not SLD) and zoom-level bounds must be declared in the configuration body; verifying layer_name uniqueness in GetCapabilities before publication avoids conflicts that are difficult to clean up.

- Endpoint UUID (open WMTS/TMS): `ae032611-13eb-4a18-8d04-9b7604a031cc`; URLs: `https://data.geopf.fr/wmts`, `https://data.geopf.fr/tms`
- Configuration body requires `bottom_level` / `top_level` (integer zoom levels) and `used_data[].stored_data`
- ROK4-style files (JSON palette definitions, not SLD) are used for raster coloring; referenced by UUID in configuration `styles` array; first in list is default
- GetCapabilities verify layer_name uniqueness before attempting publication: `https://data.geopf.fr/wmts?SERVICE=WMTS&REQUEST=GetCapabilities`

---

## [Raster data — WMS-RASTER](https://geoplateforme.github.io/tutoriels/production/raster/base/wms/)

WMS-RASTER publishes a `ROK4-PYRAMID-RASTER` through ROK4 as a WMS layer, with optional ROK4-STYLE JSON palettes for colorization. The style referenced in the WMS `STYLES=` parameter corresponds to a static uploaded to the entrepôt — the first style in the configuration list is served as the default.

- Endpoint UUID (open WMS-Raster): `ae042611-13eb-4a18-8d04-9b7604a031cc`; URL: `https://data.geopf.fr/wms-r`
- ROK4-STYLE static type (JSON palette) used for raster styles; upload via `POST /datastores/{datastore}/statics` with `type=ROK4-STYLE`
- Style identifier is referenced in WMS `STYLES=` parameter; the first style in the configuration list is served as default when no STYLES param is given

---

## [Raster data — WMS harvesting](https://geoplateforme.github.io/tutoriels/production/raster/base/pyramide-wms/)

WMS harvesting creates a `ROK4-PYRAMID-RASTER` by fetching tiles from an existing WMS source rather than from a livraison, which is useful for ingesting data from third-party or internal services without a separate file delivery step. Network access from the platform is restricted by default, and incremental updates can be done efficiently by chaining to an existing pyramid.

- Processing UUID (WMS harvest): `6a54dc92-fc93-4c8e-9f02-046bf889550e`; no livraison needed — the platform fetches tiles from an existing WMS
- Harvest area specified as WKT polygon in EPSG:4326 (longitude first); parameters include source WMS URL, layer name, target zoom levels, and SRS
- Outbound network from the platform is restricted by default to `data.geopf.fr`; use `harvest_extras` to pass an `apikey` parameter for private GPF sources
- If an existing stored_data UUID is provided as input, the new pyramid is created with chaining (references old tiles for unchanged areas) — efficient incremental updates

---

## [Raster data — updates](https://geoplateforme.github.io/tutoriels/production/raster/maj/)

Raster pyramid updates offer four strategies with different trade-offs between destructiveness, storage cost, and the ability to roll back. The right choice depends on whether the old pyramid needs to remain accessible and whether the input pyramids were built with `mask: true`.

Four strategies:

- **By injection** (`raster-maj-parinjection`): pass existing stored_data UUID in `output.id` instead of a new name; overwrites pyramid in-place; **irreversible**
- **By chaining** (`pyramide-wms` with stored_data input): new pyramid references old tiles; keeps both generations accessible if needed
- **By fusion/composition** (`raster-maj-composition`): processing UUID `7cdca031-9e86-4804-8764-9b1d783b087d`; merges multiple independent pyramids into a new one; all input pyramids must have `mask: true`; creates a `use`/`used_by` dependency — input pyramids cannot be deleted until the fusion pyramid is deleted first
- **Au fur et à mesure** (incremental chaining): deliver the second dataset as a new upload and run the raster pyramid processing with **both** `inputs.upload=[{new_upload}]` and `inputs.stored_data=[{old_pyramid}]`; the processing produces a new stored_data that tiles the new data fresh and references unchanged old tiles; the old pyramid gains a `used_by` dependency and cannot be deleted; update the existing configuration to point at the new stored_data, then synchronize the offering (`PUT /datastores/{datastore}/offerings/{offering}`) to push the change to servers without losing the offering UUID (important if access permissions are already attached); set the final `layer_name` on the first configuration — it cannot be changed after the offering is created

---

## [Raster data — DEM/MNT](https://geoplateforme.github.io/tutoriels/production/raster/mnt/)

MNT (digital elevation model) publishing uses the ALTIMETRY configuration type and has stricter constraints than standard imagery: FLOAT32 output, lossless compression, and nearest-neighbor interpolation to preserve exact elevation values. The available TMS grids differ from standard raster, and a single configuration can expose both ground surface (MNT) and above-ground surface (MNS).

- MNT-specific TMS grids (not available for standard imagery): `LAMB93_50cm`, `LAMB93_10cm`, `4326`
- Output is FLOAT32 single-channel; compression must be `zip` (lossless); interpolation must be `nn` to preserve exact elevation values
- ALTIMETRY configuration type; endpoint UUID: `0ac92a1e-aa86-4843-8528-e303f12296e5`
- A single ALTIMETRY configuration can combine MNT (ground surface) + MNS (above-ground surface); `source` and `accuracy` metadata fields can be either static values or read from a raster band via a mapping dict
- Service URL: `https://data.geopf.fr/altimetrie/`

---

## [Archives](https://geoplateforme.github.io/tutoriels/production/archive/)

Upload (type=ARCHIVE) → stored_data (ARCHIVE) → DOWNLOAD configuration → offering

Archives allow publishing arbitrary files (COG, GeoParquet, PMTiles, or any other format) through the platform's download service via an Atom feed. The archive processing stores files flat by name regardless of directory structure in the upload, which constrains how batches can be organized and updated.

- Processing UUID (archive copy): `12cdc646-3976-4f18-b273-f34fca37e2a6`; output type: `ARCHIVE` on S3; no processing parameters needed
- Re-running the archive copy processing against an existing stored_data UUID (via `output.stored_data.id`) overwrites files that already exist by the same name; new files are added; no files are deleted — safe incremental update pattern
- Required checks before the copy processing will run: "Vérification standard" (`ecb00ba0-eb42-427e-8418-f5d8a30e84ec`) and "Vérification archive" (`f4f79b5e-7056-4b56-981d-34043b4925ab`; validates no filename collisions within the upload tree, since files are stored flat by name)
- Gotcha: two files with the same filename in different subdirectories of the same upload will fail the archive check — files are stored flat by name, not by path
- ARCHIVE integration does **not** extract an extent; after processing, manually set extent (GeoJSON MultiPolygon, ≤5000 vertices) and edition dates via `PATCH /datastores/{datastore}/stored_data/{stored_data}`
- DOWNLOAD configuration uses an Atom feed structure; `sub_name`, `format`, `zone`, `resolution` reference nomenclature terms from `/statics/nomenclatures?type=FORMAT` and `?type=ZONE`
- Cloud-optimized formats (COG, GeoParquet, PMTiles) should be published on a "chunk" endpoint variant that supports range requests
- Endpoint UUID (open download): `ae052611-13eb-4a18-8d04-9b7604a031cc`; URL: `https://data.geopf.fr/telechargement`
- Archives are stored as-is; the platform provides an Atom feed of available files; clients can discover and download individual files by appending filename to the download URL

---

## [Search (recherche)](https://geoplateforme.github.io/tutoriels/production/recherche/)

The platform exposes two search mechanisms: a standard index (`geoplateforme`) that is automatically maintained as offerings are published and unpublished, and custom indexes for domain-specific search needs. The subsections below cover how to enrich standard search results with tags and custom facets, and how to build, populate, and query a custom index.

### Standard index

- The standard index `geoplateforme` is **automatically populated and purged** when offerings are published or unpublished — no manual indexing step required
- Search tags on **configuration** (set via `POST /datastores/{datastore}/configurations/{configuration}/tags`): `theme`, `licence`, `thumbnail`
- Search tags on **stored_data** (set via `POST /datastores/{datastore}/stored_data/{stored_data}/tags`): `production_year`, `producer`
- The `extra._search` sub-object in a configuration body is passed through to search results as-is; use it for custom facets
- Endpoints: `POST /recherche/api/indexes/geoplateforme` (full-text search), `GET .../suggest?text=` (suggest by field), `GET .../suggest_autocomplete?text=` (autocomplete titles)

### Custom indexes

- INDEX upload type with `"is_search_layer": true` flag for search-layer indexes; CSV separator must be `;`; each CSV requires a companion `.csvt` file declaring column types; JSON documents require a `schema.json`
- Create index: livraison (type=INDEX) → `index2index` processing → INDEX stored_data → SEARCH configuration → offering
- Custom index URL: `https://data.geopf.fr/private/recherche/api/indexes/{index}` (requires key or auth)
- Two custom index variants: **search_layer** (same API as standard index, including `/suggest`) and **classic** (only POST search + autocomplete on string fields; no per-field suggest, no lookup by ID)
- For autocomplete on a classic index: create a parallel search_layer index mapping your fields to the standard `title`/`description`/`keywords` schema; query the search_layer for autocomplete, then query the classic index for full result data
- Updating a custom index: append documents by re-running `index2index` against the existing stored_data; deletes or field changes require full re-delivery (no partial delete API)

---

## [Metadata & complements](https://geoplateforme.github.io/tutoriels/production/complement/)

This section covers the supporting assets that complete a publication: ISO 19115 metadata for catalogue discovery, annexes for client-facing hosted files, personal documents for user-scoped sharing, and thematic GetCapabilities for exposing filtered service subsets. These are independent of the core data pipeline but required for a fully integrated presence in the platform ecosystem.

### Metadata

- Upload ISO 19115 XML: `POST /datastores/{datastore}/metadata` multipart; `type` is `ISOAP` or `INSPIRE`
- `open_data=true` flag on the metadata upload enables automatic harvesting by data.gouv.fr
- The `file_identifier` (from `gmd:MD_Metadata/gmd:fileIdentifier/gco:CharacterString`) must be **platform-globally unique**; collisions cause upload failure
- Publish metadata on a CSW endpoint: `POST /datastores/{datastore}/metadata/publication` with `{"file_identifiers": [...], "endpoint": "{csw_endpoint_uuid}"}` — publishes multiple metadata in one call by `file_identifier` string, not by metadata UUID; unpublish with `POST .../metadata/unpublication` (same body); delete a metadata only after unpublishing it; CSW endpoint UUID: `ae062611-13eb-4a18-8d04-9b7604a031cc`, URL: `https://data.geopf.fr/csw`

### Annexes

- Upload: `POST /datastores/{datastore}/annexes` multipart with `file`, `paths` (list of URL suffixes), `published`, `labels`
- Publish/unpublish: `PATCH /datastores/{datastore}/annexes/{annexe}` with `{"published": true/false}`; can also publish by label via `POST /datastores/{datastore}/annexes/publication`
- Final public URL: `https://data.geopf.fr/annexes/{technical_name}/{path}` — the `technical_name` comes from `GET /datastores/{datastore}`
- Labels enable bulk operations and are used by cartes.gouv.fr conventions (e.g., `type=thumbnail`, `datasheet_name=...`)

### Personal documents

- Documents are user-scoped (no datastore needed): `POST /users/me/documents` multipart
- Sharing: nominative via `POST /users/me/documents/{document}/sharings` (recipients need an account); public URL via `PATCH /users/me/documents/{document}` with `{"public_url": true}` — generates a random opaque URL; setting `false` revokes it

### Thematic GetCapabilities

- To expose a filtered subset of a WFS/WMS to clients (e.g., only specific layers): download the full GetCapabilities XML, trim the `FeatureTypeList` / `Layer` elements, upload as an annexe, and point QGIS or other clients at the annexe URL — no server-side filtering key is needed

---

## [High-level services](https://geoplateforme.github.io/tutoriels/production/hautniveau/)

The platform exposes two high-level services that operate on already-published data: an extraction service for downloading filtered subsets of vector stored_data, and a standalone validation service for checking files before delivery. Both have non-obvious configuration requirements that are easy to miss.

### Extraction service

- API: OGC API Processes at `https://data.geopf.fr/extraction/`; asynchronous job model
- Output formats: `PGDUMP`, `ESRI SHAPEFILE`, `GEOJSON`, `GPKG`, `GML`, `PARQUET`
- Filter syntax: standard PostgreSQL/PostGIS WHERE clause passed as a parameter
- To make a stored_data extractable: either set `open: true` on the stored_data OR add community visibility; **also** share the stored_data with the extraction service datastore `579526dc-a3bb-437f-8163-d7e48d79d385` — this sharing step is separate from visibility and easy to overlook

### Validation service

- Standalone validation at `https://data.geopf.fr/validation/api/validations`; upload a ZIP, POST to launch with a `model` URL pointing at a validation schema
- Status `"success"` means the validation **ran** successfully, not that data **passed**; inspect result `level` fields for `ERROR` / `WARNING` entries in the detailed report
- Can download a normalized version of the dataset after validation; useful for pre-processing before livraison

---

## [Workspace management](https://geoplateforme.github.io/tutoriels/production/gestion/)

Workspace management covers how community membership rights are assigned, how organization-level read routes aggregate data across datastores, and the admin-only flow for provisioning new communities and datastores. This section also collects all processing UUIDs in one place for quick reference.

- Community rights (ANNEX, UPLOAD, BROADCAST, PROCESSING, COMMUNITY) are set per-member via `PUT /communities/{community}/users/{user}` (upsert semantics); supervisor cannot be removed and always holds all rights
- Organization-level read routes: `GET /organizations/{organization}/{annexes|configurations|endpoints|offerings|permissions|processings/executions|statics|stored_data|uploads}` — all support the same filters as their per-datastore equivalents plus a `community` or `datastore` filter
- Admin-only workspace provisioning flow: `POST /administrator/communities` → `POST /administrator/datastores` → `PATCH /administrator/datastores/{datastore}` with `{"active": true}` → assign processings, checks, storages, endpoints via admin routes
- Key UUIDs for processings (prod environment):
  - Vector integration: `0de8c60b-9938-4be9-aa36-9026b77c3c96`
  - Raster pyramid: `2ae50661-986c-4f47-a3f0-e380417b522c`
  - Vector pyramid: `aa5f9391-0bdb-4b97-9209-fcde351b82f6`
  - Fusion (joincache): `7cdca031-9e86-4804-8764-9b1d783b087d`
  - WMS harvest: `6a54dc92-fc93-4c8e-9f02-046bf889550e`
  - SQL derivation: `2c18eda8-d30c-42ab-8760-ec16d8929de5`
  - Extraction datastore: `579526dc-a3bb-437f-8163-d7e48d79d385`

---

## [cartes.gouv.fr compatibility](https://geoplateforme.github.io/tutoriels/production/compatibilites/cartes-gouv/)

This section covers the conventions required for a dataset to be correctly represented in the cartes.gouv.fr interface: the `datasheet_name` tag that groups entities into a fiche de données, the labeling conventions for thumbnails and editorial documents, and the generation history tags that power the lineage report. Most of these are additive tags and annexes on top of a standard publication, but they must be applied consistently across all entities in the chain.

- The `datasheet_name` tag (human-readable, accents and spaces allowed) must be added to the livraison, stored_data, and all configurations to group them into a **fiche de données** visible in cartes.gouv.fr at `https://cartes.gouv.fr/entrepot/{datastore}/donnees/{datasheet_name}`
- Thumbnail: upload an annexe with labels `type=thumbnail,datasheet_name=...`; the thumbnail also needs to be referenced in the metadata to appear in the public catalogue (adding the label alone is not sufficient)
- Client-side WFS style: store the style JSON (SLD or QML annexe URL references) in `configuration.extra.styles` array; format is `[{name, current, layers: [{name: "<layer_name>:<table>", annexe_id, url}]}]`
- Editorial documents: label annexes with `type=document,datasheet_name=...`, then update the auto-generated `type=document-list` annexe JSON to register them; same caveat — they only appear in the public catalogue after being referenced in the metadata
- Generation history: tag livraison with `proc_int_id` and `vectordb_id`; tag stored_data with `upload_id` and `proc_int_id` — enables the generation report tab in cartes.gouv.fr
- Metadata is the entity that makes a fiche visible in the catalogue; it can be built through the cartes.gouv.fr UI form or programmatically; the resulting ISO 19115 XML is uploaded to the entrepôt and published on the CSW

---

## [SDK python](https://geoplateforme.github.io/sdk-entrepot/)

Package: `sdk_entrepot_gpf`; entry points: `python -m sdk_entrepot_gpf` or `egpf`

The SDK wraps the platform API in a Python CLI and library, providing higher-level abstractions for delivery (livraison) and multi-step workflows. The subsections below cover INI-format configuration, the delivery descriptor format, and the workflow/resolver system that underpins automated pipelines.

### Configuration

- INI-format config file (`config.ini`); minimum required: `[store_authentification]` with `login`/`password` (or `grant_type=client_credentials` + `client_id`/`client_secret` for service accounts), and `[store_api]` with `datastore`
- Default API root: `https://data.geopf.fr/api`; override with `root_url` for qualification (`https://data-qua.priv.geopf.fr/api`)
- TOTP: add `totp_key=<raw OTP seed>` — this is the seed, not the 6-digit code; FreeOTP does not expose the seed, use Aegis
- Config file location: either named `config.ini` in the working directory, or pointed to via `--ini` CLI flag or `SDK_ENTREPOT_CONFIG_FILE` environment variable

### Delivery (livraison)

- Upload descriptor JSON: `{"datasets": [{data_dirs, upload_infos: {name, description, srs, type}, comments, tags}]}`
- Upload types: `VECTOR` (SHP, CSV, GeoJSON), `RASTER` (PNG, TIFF, JPEG, JPEG2000), `ARCHIVE` (any)
- CLI: `python -m sdk_entrepot_gpf delivery descriptor.json [-b CONTINUE|DELETE]`
- The `delivery` command also handles annexes, statics, metadata, and key creation via the same descriptor format with top-level `annexe`, `static`, `metadata`, `key` arrays

### Workflows

- Workflow JSON defines named `steps`, each with `actions` list and `parents` list; steps can be launched individually
- Action types: `processing-execution`, `configuration`, `offering`, `permission`, `access`, `delete-entity`, `edit-entity`, `used_data-configuration`, `copy-configuration`, `synchronize-offering`
- CLI: `python -m sdk_entrepot_gpf workflow -f workflow.json -s step_name [-p param_name value ...]`
- Built-in example workflows (retrieve with `python -m sdk_entrepot_gpf example workflow <name>`): `generic_archive.jsonc`, `generic_vecteur.jsonc`, `generic_raster.jsonc`, `generic_joincache.jsonc`, `generic_maj_bdd.jsonc`, `generic_moissonnage.jsonc`, `PCRS.jsonc`

### Resolvers

Four resolvers are auto-registered in CLI mode: `store_entity` (StoreEntityResolver), `user` (UserResolver), `datetime` (DateResolver), `params` (DictResolver for `-p` CLI args)

- `store_entity` pattern: `{store_entity.{entity_type}.{infos|tags}.{field} [INFOS(k=v,...), TAGS(k=v,...)]}`; entity types: `upload`, `stored_data`, `processing_execution`, `offering`, `processing`, `configuration`, `endpoint`, `static`, `datastore`
- Example: `{store_entity.stored_data.infos._id [INFOS(name=MY_DATA_{params.edition})]}` resolves to the UUID of the stored_data named `MY_DATA_2024-01` when called with `-p edition 2024-01`
- Custom resolvers: subclass `AbstractResolver`, implement `resolve(string_to_solve)`; register with `GlobalResolver().add_resolver(...)`

### PCRS workflow (notable real-world use case)

- PCRS (Plan Corps de Rue Simplifié) raster tiles: deliver as RASTER upload; the `PCRS.jsonc` workflow handles pyramid generation (step `pyramide`) and publication (step `publication`) using `--param producteur $name`
- Incremental update: deliver new tiles with a `version` tag, then run `pyramide_maj` step with `--param old_version X --param new_version Y`; the joincache processing creates a new pyramid referencing both old and new tiles
- layer_name uniqueness warning is especially critical for PCRS: check WMTS and WMS-R GetCapabilities before delivery since the project name becomes the layer_name

---

## Key constants & UUIDs

| Resource | UUID |
|---|---|
| Processing: vector integration | `0de8c60b-9938-4be9-aa36-9026b77c3c96` |
| Processing: raster pyramid | `2ae50661-986c-4f47-a3f0-e380417b522c` |
| Processing: vector pyramid (tippecanoe) | `aa5f9391-0bdb-4b97-9209-fcde351b82f6` |
| Processing: raster fusion (joincache) | `7cdca031-9e86-4804-8764-9b1d783b087d` |
| Processing: WMS harvest | `6a54dc92-fc93-4c8e-9f02-046bf889550e` |
| Processing: archive copy | `12cdc646-3976-4f18-b273-f34fca37e2a6` |
| Processing: SQL derivation | `2c18eda8-d30c-42ab-8760-ec16d8929de5` |
| Endpoint: WFS (open) | `ae012611-13eb-4a18-8d04-9b7604a031cc` |
| Endpoint: WMS-Vector (open) | `ae022611-13eb-4a18-8d04-9b7604a031cc` |
| Endpoint: WMS-Raster (open) | `ae042611-13eb-4a18-8d04-9b7604a031cc` |
| Endpoint: WMTS/TMS (open) | `ae032611-13eb-4a18-8d04-9b7604a031cc` |
| Endpoint: Download (open) | `ae052611-13eb-4a18-8d04-9b7604a031cc` |
| Endpoint: CSW / METADATA (open) | `ae062611-13eb-4a18-8d04-9b7604a031cc` |
| Endpoint: WFS (private) | `d02feec9-1169-403f-bfc3-7ba6d6015ed4` |
| Endpoint: WMS-Vector (private) | `519c8bb1-9b7f-414a-9850-1a73dfd467ed` |
| Endpoint: WMS-Raster (private) | `66866100-48eb-4340-bbc9-f5c7d9707928` |
| Endpoint: WMTS/TMS (private) | `7e0a92d1-8213-4ce0-8903-eb4c305a1849` |
| Endpoint: Download (private) | `b5bf7ab2-8998-4829-8c80-cd2ec02e6e58` |
| Endpoint: ALTIMETRY | `0ac92a1e-aa86-4843-8528-e303f12296e5` |
| Datastore: extraction service | `579526dc-a3bb-437f-8163-d7e48d79d385` |
| Check: standard (MD5) | `ecb00ba0-eb42-427e-8418-f5d8a30e84ec` |
| Check: raster | `a4060831-9c6f-42e2-9435-e07a4e8ef535` |
| Check: archive (no filename collisions) | `f4f79b5e-7056-4b56-981d-34043b4925ab` |
| SSO realm (token URL suffix) | `realms/geoplateforme/protocol/openid-connect/token` |
| QGIS OAuth2 client ID | `qgis` |
| QGIS OAuth2 client secret | `F77z01QHTaJClBJ1p2OZYkFGL24XYLti` |
| SDK default client_id | `gpf-warehouse` |
| SDK default client_secret | `BK2G7Vvkn7UDc8cV7edbCnHdYminWVw2` |
