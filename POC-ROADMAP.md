# datagouv ↔ geopf — Integration Roadmap

## Scope

Users who authenticate on data.gouv.fr can push a compatible geo-file (GeoPackage for POC) to Geoplateforme at the end of the contribution funnel. This creates a *fiche de données* in the entrepôt and enables WFS/WMS... service configuration via cartes.gouv.fr. Published service URLs are periodically synced back to data.gouv.fr as resources on the originating dataset.

## 1. Authentication

**Target:** OAuth2 authorization code flow initiated from the data.gouv.fr frontend.

TBD in meeting. See also token sharing with backend below (push flow).

**Alternative (interim):** 
- service account with `client_credentials` grant scoped to a shared entrepôt, for testing only
- env var with Bearer token (cf current test script)

## 2. Entrepôt (datastore) Linking

Map data.gouv.fr organizations (and users) to a Geoplateforme datastore ID. One needs a target datastore ID to send the uploaded file too.

For POC: use the DINUM test datastore as a constant.

Later: 
- either define a relation organization -> datastore(s) in data.gouv.fr ;
- or use the oauth connection to fetch the user's writable datastores (to be tested)

## 3. Push Flow (datagouv → geopf)

Triggered at the end of the contribution funnel when a geo-compatible resource is uploaded.

```
user uploads geo-file on data.gouv.fr
  → detect compatible format (gpkg)
  → resolve datastore_id from org/user link
  → run pipeline (livraison → integration → stored_data)
  → generate ISO 19115 XML from dataset metadata
  → upload metadata + publish to CSW
  → tag all entities with datasheet_name
  → store stored_data_id on the resource or dataset
```

Structure:
- `datasheet_name` = stable slug derived from dataset ID + resource ID
- `fileIdentifier` = dataset ID
- -> this means we could have multiple datasheet (resources) per dataset, thus mapping data.gouv.fr structure to geopf. Needs to be tested/challenged.

SRS:
- mandatory input
- default to a given value for POC, could be either asked for from the user or detected from gpkg

Implementation:
- Full JS/front: CORS are open, so possible ; but beware of long polling (several minutes) that could leave the object in a transient state on geopf ;
- Drive a backend sync with loader/resume feature on front: probably best for future-proofing? And faster prototyping. But beware of auth sharing: send the oauth token for processing on the backend? Could be acceptable if token are medium-lived: long enough for the process to succeed, short enough for it to not be a security concern. It looks like it's twelve hours, kind of perfect.

Metadata sync, currently missing mandatory metadata for service creation (can be filled by user on geopf):
- Catégorie thématique: extract from the tags list against know Inspire vocabulary?
- Adresse électronique de contact sur les métadonnées: extract from contact points?
- Adresse électronique (données): extract from contact points?

## 4. Services Sync (geopf → datagouv)

Periodic job that pulls published offerings back to data.gouv.fr as resources.

```
for each dataset with a known stored_data_id:
  → GET /configurations?tags[datasheet_name]=<name>
  → for each configuration, GET /configurations/{id}/offerings
  → for each PUBLISHED offering, upsert a resource on the datagouv dataset:
      title:  offering layer_name + type (e.g. "my-layer WFS")
      url:    offering.urls[0].url
      format: WFS / WMS / WMTS
      extras: { geopf_offering_id, last_synced_at }
  → depublish resources whose offering is no longer PUBLISHED
```

- Sync cadence: TBD (daily?)
- Idempotent: keyed on `geopf_offering_id` (offering technical id on geopf) to avoid duplicates
- Offerings carry no description — title/abstract come from the ISO 19115 CSW record if needed

This will be unauthenticated, so will only consider PUBLISHED services. Unpublished services will be removed from data.gouv.fr.