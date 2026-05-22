# datagouvfr-to-geopf

POC exploring automated publication of [data.gouv.fr](https://www.data.gouv.fr) datasets to [Geoplateforme](https://geoplateforme.fr), including metadata registration and data ingestion.

---

## Goal

Given a dataset on data.gouv.fr, trigger the creation of a *fiche de données* on cartes.gouv.fr so that the dataset owner can configure WFS/WMS services from it.

The minimal flow is:
1. Map dataset.json metadata → ISO 19115 XML
2. Upload the XML to the entrepôt → publish it to the CSW catalog
3. Download a vector resource from the dataset and ingest it through the livraison pipeline
4. The resulting `stored_data` appears as a fiche in the cartes.gouv.fr entrepôt

---

## Auth

### What the platform uses

Geoplateforme uses Keycloak (`sso.geopf.fr`, realm `geoplateforme`) for authentication. The API uses Bearer tokens.

### Grant types tried

| Flow | Result |
|------|--------|
| `password` grant (login/password) | Works if you have a native Geoplateforme account. The SDK (`sdk-entrepot-gpf`) uses this by default with `client_id=gpf-warehouse`. Not usable if you authenticate via a third-party IdP. |
| Device authorization flow | Supported by the realm but **disabled for `gpf-warehouse`**: `"Client is not allowed to initiate OAuth 2.0 Device Authorization Grant."` |
| Authorization code + localhost redirect | The `gpf-warehouse` client returns `"Paramètre invalide : redirect_uri"` — no localhost URI is registered for it. The QGIS plugin uses this flow with a private `client_id` (injected via CI secret, not public). |
| Manual token from Swagger UI | **Works for POC.** Log in via Swagger UI (`https://data.geopf.fr/api/swagger-ui/index.html`), execute any endpoint, copy the `Authorization: Bearer ...` header from devtools → Network. |

### Current auth setup

For this POC, authentication is manual:

```bash
# After logging in via Swagger UI, copy the Bearer token from devtools
export GEOPF_TOKEN='eyJ...'
```

Token TTL is ~12h (observed). The `GEOPF_TOKEN` env var (or `.env` file) is read by `auth.py`.

### Known client credentials (from sdk-entrepot-gpf defaults)

```
token_url:     https://sso.geopf.fr/realms/geoplateforme/protocol/openid-connect/token
client_id:     gpf-warehouse
client_secret: BK2G7Vvkn7UDc8cV7edbCnHdYminWVw2
```

These are public (shipped in the SDK). The `gpf-warehouse` client only supports `password` and `authorization_code` flows, with no public redirect URIs registered.

### Path forward

A proper integration would need either:
- A dedicated OAuth2 client registered by IGN with `http://localhost:PORT/callback` as redirect URI, enabling the authorization code + local server flow (as in `IGNF/oidc-python`)
- Or a service account using `client_credentials` grant

---

## Metadata (ISO 19115 / CSW)

### Minimal mapping from dataset.json

The entrepôt metadata API accepts ISO 19115 XML. The only **strictly required** field is `fileIdentifier` (must be unique on the platform). In practice, a useful record also needs:

| data.gouv.fr field | XML path | Notes |
|---|---|---|
| `id` | `gmd:fileIdentifier` | Used as-is; append a test suffix to avoid collisions |
| `title` | `MD_DataIdentification/citation/title` | |
| `description` | `abstract` | Falls back to `title` if null |
| `organization.name` | `contact/organisationName` | |
| `created_at` | `citation/date` | |
| `last_modified` | `dateStamp` | |
| `tags[]` | `descriptiveKeywords` | |
| `license` (slug) | `resourceConstraints/otherConstraints` | Slug mapped to human label |
| `spatial` (null) | `EX_GeographicBoundingBox` | Defaults to France metro bbox when null |

`hierarchyLevel` is set to `dataset` (not `series`). Language is hardcoded to `fre`.

### Upload + publication (two separate steps)

Uploading metadata to the entrepôt does **not** make it public. There are two steps:

```
POST /datastores/{id}/metadata          → creates the record in the entrepôt (type=ISOAP, open_data=true)
POST /datastores/{id}/metadata/publication → pushes it to the CSW catalog
```

The publication body requires a `file_identifiers` array and an `endpoint` UUID. The CSW endpoint (`gpf-geonetwork`) is platform-wide:

```
endpoint: ae062611-13eb-4a18-8d04-9b7604a031cc
URL:      https://data.geopf.fr/csw
```

This endpoint UUID is **not** discoverable via the regular API (requires superadmin). It was found in the tutorial documentation examples.

### Verify a published record

```
https://data.geopf.fr/csw?SERVICE=CSW&REQUEST=GetRecordById&VERSION=2.0.2&ID={fileIdentifier}&ElementSetName=full
```

### What metadata does NOT do

Publishing metadata to the CSW creates a catalog record but does **not** create an entry in the cartes.gouv.fr entrepôt données tab (`/donnees`). That tab requires the full data ingestion pipeline AND the `datasheet_name` tag (see below).

---

## Data ingestion pipeline (livraison → stored_data)

To create a fiche in the entrepôt données tab, actual data files must go through the full pipeline:

```
download resource → livraison (upload) → checks → processing execution → stored_data
```

### Step by step

**1. Create a livraison**
```
POST /datastores/{id}/uploads
{ "name": "...", "type": "VECTOR", "srs": "EPSG:4326" }
```

**2. Push the data file**
```
POST /datastores/{id}/uploads/{upload}/data?path=/{filename}
body: multipart file
```

**3. Push MD5 checksum**
```
POST /datastores/{id}/uploads/{upload}/md5
body: multipart file with content "{md5}  {filename}\n"
```

**4. Close the livraison** (triggers automatic checks)
```
POST /datastores/{id}/uploads/{upload}/close
```

Poll `GET /uploads/{upload}` until `status == "CLOSED"` (checks passed) or `"UNSTABLE"` (failed).

Two checks run automatically on vector uploads:
- `ecb00ba0` — standard (MD5 verification)
- `66ed8a1b` — vector (file readability + extent extraction)

**5. Create + launch processing execution**
```
POST /datastores/{id}/processings/executions
{
  "processing": "0de8c60b-9938-4be9-aa36-9026b77c3c96",
  "inputs": { "upload": ["{upload_id}"] },
  "output": { "stored_data": { "name": "..." } },
  "parameters": { "srs": "EPSG:4326" }
}

POST /datastores/{id}/processings/executions/{exec_id}/launch
```

The processing `0de8c60b` is **"Intégration de données vecteur livrées en base"**. It accepts VECTOR uploads and produces `VECTOR-DB` stored_data (PostgreSQL). Supported input formats: CSV, Shapefile, GeoPackage, GeoJSON.

Poll `GET /processings/executions/{exec_id}` until `status == "SUCCESS"`. The response then contains `output.stored_data._id`.

**6. Delete the livraison** (cleanup)
```
DELETE /datastores/{id}/uploads/{upload_id}
```

Once the data is stored permanently, the upload is no longer needed. Without this step, it remains visible in the cartes.gouv.fr UI as a "livraison non terminée".

### Required field: `description` on upload creation

The `description` field is mandatory when creating a livraison, even though it is not mentioned in the API documentation. Omitting it returns `400 {"error_description": ["Le champ description ne doit pas être vide"]}`. We set it to the same value as `name`.

### The `datasheet_name` tag — undocumented, critical

The cartes.gouv.fr `/donnees` tab does **not** list `stored_data` directly. It calls a cartes.gouv.fr Symfony backend endpoint (`/api/datastores/{id}/datasheet`) which builds a virtual list by collecting all uploads, stored_data, and metadata that share the same `datasheet_name` tag. Without this tag, data exists in the entrepôt API but is invisible in the UI.

**Not documented anywhere in the official tutorials.** Found by reading the [cartes.gouv.fr source code](https://github.com/IGNF/cartes.gouv.fr) (`DatasheetController.php`).

The tag must be set on each entity after creation:

```
POST /datastores/{id}/uploads/{upload_id}/tags
POST /datastores/{id}/stored_data/{stored_data_id}/tags
POST /datastores/{id}/metadata/{metadata_id}/tags
body (JSON): { "datasheet_name": "<name>" }
```

The value must be identical across all three. The cartes.gouv.fr UI then groups them into a single fiche entry under that name.

---

## Running the POC

```bash
cp .env.example .env
# Fill in GEOPF_TOKEN and GEOPF_DATASTORE_ID

uv run python main.py --help
```

`main.py` exposes two commands via [minicli](https://github.com/jamesturk/minicli).

### `upload-file` — ingest data and publish metadata

```bash
# Full pipeline: ingest data + upload metadata
uv run python main.py upload-file my-test-01 --file example.gpkg --srs EPSG:4326

# Metadata only (skip data ingestion)
uv run python main.py upload-file my-test-01 --skip-data
```

The `name` argument is used as the `datasheet_name` tag value and is appended to the dataset ID to form a unique `fileIdentifier` (e.g. `69f44162620029ea7beff6ea-my-test-01`).

After a successful run, the fiche is visible at:
```
https://cartes.gouv.fr/tableau-de-bord/entrepots/{GEOPF_DATASTORE_ID}/donnees
```

### `get-services` — list published offerings for a fiche

Once a fiche has been created, a user can configure WFS/WMS/WMTS services on it from the cartes.gouv.fr UI. This command retrieves all published offerings for a given datasheet name:

```bash
uv run python main.py get-services my-test-01
```

**How it works:**
1. Fetches all configurations in the datastore tagged `datasheet_name=<name>` — cartes.gouv.fr tags configurations with `datasheet_name` when a service is created through its UI
2. For each configuration, fetches its offerings (`GET /configurations/{id}/offerings`)
3. Prints type, layer name, status, and a GetCapabilities URL for each offering

**Offering payload:** offerings carry only operational fields — `type`, `status`, `layer_name`, `open`, `available`, `urls` (ready-made service URLs), plus back-references to the configuration and endpoint. Title/description live in the ISO 19115 metadata record in the CSW, linked from the configuration's `metadata` array.

**Entity chain:** `stored_data → configuration → offering → endpoint`

A configuration describes how a stored_data is served (layer name, bbox, relations). An offering links a configuration to a diffusion endpoint (WFS/WMS/WMTS server); creating one triggers publication to the server. The `available` boolean toggles access without touching permissions.

---

## Documentation scraping

The geoplateforme public docs span three sub-sites (~76 pages total, all in French, no public source repo):

- `https://geoplateforme.github.io/entrepot/production/` — concepts, components, OpenAPI
- `https://geoplateforme.github.io/sdk-entrepot/` — Python SDK
- `https://geoplateforme.github.io/tutoriels/production/` — step-by-step workflows

### Scraping

`scrape.py` fetches all 67 substantive pages, extracts the `<article>` content, converts it to markdown via `html2text`, and saves it under `scraped-docs/{entrepot,sdk,tutoriels}/`. Raw source material is preserved for re-summarization without re-scraping.

```bash
uv run --with html2text scrape.py
```

`html2text` is intentionally kept out of `pyproject.toml` (scraping is a one-off tool, not a project dependency).

### Summary

`geopf-docs-summary.md` is a condensed English developer reference generated from the scraped pages. It covers all sections with intro paragraphs, workflow flow lines, API endpoints inline, and a constants/UUIDs lookup table at the end. French platform terms (entrepôt, livraison, offre, etc.) are kept as-is. Every section links back to its source page.

---

## Architecture

The platform is built in three independent layers with no enforced consistency between them.

**Layer 1 — Entrepôt API** (`data.geopf.fr/api`): a generic data warehouse. It stores independent entities — uploads, stored_data, metadata records, processings, configurations, offerings. There is no "fiche" entity. Each object has a UUID and optional free-form tags.

**Layer 2 — CSW catalog** (`data.geopf.fr/csw`, GeoNetwork): a separate OGC-standard catalog service. It only knows about ISO 19115 records explicitly published to it. It has no knowledge of stored_data or uploads.

**Layer 3 — cartes.gouv.fr** (Symfony app): a view layer that calls the entrepôt API. The `DatasheetController` builds "fiches de données" at query time by collecting all entities that share the same `datasheet_name` tag value. There is no fiche entity in the database — it is synthesized on every request.

### Why data can exist without appearing in the UI

An entity exists in the entrepôt as soon as it is created. It appears in the cartes.gouv.fr UI only if it carries the correct `datasheet_name` tag. These are two separate states. This is how data ends up in the API (`GET /stored_data` returns it) while remaining completely invisible in the `/donnees` tab — which is exactly what happened during this POC before the tag was discovered.

### Tag-based grouping has no referential integrity

The `datasheet_name` tag is a plain string. Nothing enforces consistency:

- Delete a tag → entity silently disappears from the fiche
- Re-run the pipeline without setting the tag → new stored_data is orphaned
- Typo in the tag value → silent split into two partial fiches
- An entity can belong to zero fiches or two with no error

### Why it is designed this way

The entrepôt is a reusable warehouse meant to serve multiple clients: the QGIS plugin, the API directly, cartes.gouv.fr. The tag is the integration contract between the generic warehouse and the specific UI. The tradeoff is flexibility (any client can build its own view) at the cost of consistency (no client is required to maintain the grouping).

In practice this means the responsibility for keeping data and UI in sync falls entirely on the caller. A production integration would need either an atomic creation workflow that always sets the tag, or a periodic audit that flags entities without a `datasheet_name`.

---

## Findings

End-to-end publication from data.gouv.fr to cartes.gouv.fr is feasible via the entrepôt API. The full pipeline was validated on 2026-05-01.

### What works

- **ISO 19115 XML generation** from a data.gouv.fr dataset JSON is straightforward with a minimal field set. Only `fileIdentifier` is strictly required by the API; a handful of additional fields (`title`, `abstract`, `contact`, `bbox`, `language`) make the record useful.
- **Metadata upload + CSW publication** works in two API calls. The record is immediately queryable via the public CSW at `https://data.geopf.fr/csw`.
- **Vector data ingestion** (GeoPackage, GeoJSON, Shapefile, CSV) works through the livraison → checks → processing pipeline. The integration processing `0de8c60b` ("Intégration de données vecteur livrées en base") accepts all common vector formats and produces a PostgreSQL-backed `VECTOR-DB` stored_data.
- **Fiche de données creation** on cartes.gouv.fr is achieved by tagging the upload, stored_data, and metadata with `{"datasheet_name": "<name>"}`. Once tagged, the fiche appears in the cartes.gouv.fr entrepôt UI and the user can configure WFS/WMS services from it.

### What is undocumented but required

- **`datasheet_name` tag**: The single most important finding. The cartes.gouv.fr `/donnees` tab does not read `stored_data` directly — it calls an internal Symfony endpoint that groups entities by this tag. Without it, data is fully ingested and accessible via API but completely invisible in the UI. Not mentioned anywhere in the official tutorials; discovered by reading `DatasheetController.php` in the [cartes.gouv.fr source](https://github.com/IGNF/cartes.gouv.fr).
- **`description` field on upload**: Required by the API despite not being documented. Returns `400` if omitted.
- **CSW endpoint UUID**: `ae062611-13eb-4a18-8d04-9b7604a031cc` is the platform-wide GeoNetwork endpoint needed for metadata publication. Not discoverable via the standard API (superadmin only). Found in a tutorial documentation example.
- **Two-step metadata publication**: Uploading metadata and publishing it to the CSW are separate API calls. The upload creates the record in the entrepôt; the publication call is what makes it appear in the catalog.

### Authentication situation

The platform uses Keycloak with the `gpf-warehouse` public client. For users authenticating via a third-party IdP (agent using ProConnect, etc.), none of the standard programmatic flows work: device flow is disabled for this client, and authorization code flow has no localhost redirect URI registered. The only working approach for this POC is a manually copied Bearer token from the Swagger UI. A proper integration requires IGN to either register a redirect URI for a dedicated client or provide a service account with `client_credentials` grant.

-> Swagger is at https://data.geopf.fr/api/swagger-ui/index.html#/, click "Authorize"

### Open questions / next steps

- Can the `datasheet_name` tag be set at upload creation time (in the body), or must it always be a separate POST to `/tags`? The API accepts it as a separate call; we haven't tested whether the creation body accepts a `tags` field.
- The metadata `fileIdentifier` is currently scoped as `{dataset_id}-{name}` to avoid collisions during testing. In production it should probably just be the dataset ID.
- Spatial coverage defaults to France metro bbox when `spatial` is null on the data.gouv.fr dataset. Datasets with actual geographic coverage should resolve this from the data itself (e.g. from the GeoPackage extent returned by the vector check).
- The pipeline does not yet link the metadata record to the stored_data via a configuration/offering. This link may be needed for the fiche detail page to show the metadata alongside the data.
- Querying published services is now supported via `get-services`. The next step would be automating service creation (POST a configuration + offering) rather than requiring manual setup through the cartes.gouv.fr UI.
