import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv
from minicli import cli, run

from auth import auth_headers
from mapper import dataset_to_xml
from pipeline import ingest_dataset

load_dotenv()

API_ROOT = "https://data.geopf.fr/api"
CSW_ENDPOINT_ID = "ae062611-13eb-4a18-8d04-9b7604a031cc"

SERVICE_URLS = {
    "WFS": "https://data.geopf.fr/wfs",
    "WMS-VECTOR": "https://data.geopf.fr/wms-v",
    "WMS-RASTER": "https://data.geopf.fr/wms-r",
    "WMTS-TMS": "https://data.geopf.fr/wmts",
    "TMS": "https://data.geopf.fr/tms",
    "DOWNLOAD": "https://data.geopf.fr/telechargement",
}


def get_datastore_id() -> str:
    datastore_id = os.getenv("GEOPF_DATASTORE_ID")
    if datastore_id:
        return datastore_id
    resp = requests.get(f"{API_ROOT}/users/me", headers=auth_headers())
    resp.raise_for_status()
    communities = resp.json().get("communities_member", [])
    if not communities:
        print("No communities found. Set GEOPF_DATASTORE_ID manually.")
        sys.exit(1)
    datastore_id = communities[0]["community"]["datastore"]
    print(f"Using datastore: {datastore_id}")
    return datastore_id


def upload_metadata(datastore_id: str, xml_content: str, file_identifier: str, datasheet_name: str) -> None:
    resp = requests.post(
        f"{API_ROOT}/datastores/{datastore_id}/metadata",
        headers=auth_headers(),
        files={"file": (f"{file_identifier}.xml", xml_content.encode(), "application/xml")},
        data={"type": "ISOAP", "open_data": "true"},
    )
    if not resp.ok:
        raise RuntimeError(f"metadata upload failed {resp.status_code}: {resp.text}")
    metadata_id = resp.json()["_id"]
    print(f"  Metadata uploaded: {metadata_id}")

    tag = requests.post(
        f"{API_ROOT}/datastores/{datastore_id}/metadata/{metadata_id}/tags",
        headers={**auth_headers(), "content-type": "application/json"},
        json={"datasheet_name": datasheet_name},
    )
    if not tag.ok:
        raise RuntimeError(f"metadata tag failed {tag.status_code}: {tag.text}")

    pub = requests.post(
        f"{API_ROOT}/datastores/{datastore_id}/metadata/publication",
        headers={**auth_headers(), "content-type": "application/json"},
        json={"file_identifiers": [file_identifier], "endpoint": CSW_ENDPOINT_ID},
    )
    if not pub.ok:
        raise RuntimeError(f"metadata publication failed {pub.status_code}: {pub.text}")
    print("  Metadata published to CSW.")


@cli
def upload_file(name: str, *, file: Path | None = None, srs: str = "EPSG:4326", skip_data: bool = False) -> None:
    """Publish a data.gouv.fr dataset to Geoplateforme."""
    if not skip_data and file is None:
        print("Error: --file is required unless --skip-data is set")
        sys.exit(1)

    dataset = json.loads(Path("dataset.json").read_text())
    datastore_id = get_datastore_id()
    file_identifier = f"{dataset['id']}-{name}"

    if not skip_data and file:
        ingest_dataset(datastore_id, name=name, file=file, srs=srs)

    print("\n[metadata] Uploading and publishing metadata...")
    xml = dataset_to_xml(dataset, file_identifier=file_identifier)
    upload_metadata(datastore_id, xml, file_identifier, datasheet_name=name)

    print(f"\nAll done. Fiche visible at:")
    print(f"  https://cartes.gouv.fr/tableau-de-bord/entrepots/{datastore_id}/donnees")
    print(f"\nCSW record:")
    print(f"  https://data.geopf.fr/csw?SERVICE=CSW&REQUEST=GetRecordById&VERSION=2.0.2&ID={file_identifier}&ElementSetName=full")


@cli
def get_services(name: str) -> None:
    """List published services (offerings) for a datasheet by name."""
    datastore_id = get_datastore_id()

    # Configurations are tagged with datasheet_name when created via cartes.gouv.fr
    resp = requests.get(
        f"{API_ROOT}/datastores/{datastore_id}/configurations",
        headers=auth_headers(),
        params={"tags[datasheet_name]": name},
    )
    resp.raise_for_status()
    configs = resp.json()

    if not configs:
        print(f"No configurations found for datasheet '{name}'.")
        return

    total = 0
    for config in configs:
        config_id = config["_id"]
        resp = requests.get(
            f"{API_ROOT}/datastores/{datastore_id}/configurations/{config_id}/offerings",
            headers=auth_headers(),
        )
        resp.raise_for_status()
        offerings = resp.json()
        for offering in offerings:
            total += 1
            otype = offering.get("type", "?")
            status = offering.get("status", "?")
            layer = offering.get("layer_name", "?")
            base_url = SERVICE_URLS.get(otype, "")
            url_hint = f"\n    {base_url}?SERVICE={otype}&REQUEST=GetCapabilities&LAYER={layer}" if base_url else ""
            print(f"  [{otype}] {layer}  status={status}{url_hint}")

    if total == 0:
        print(f"No offerings published yet for datasheet '{name}'.")
    else:
        print(f"\n{total} offering(s) found.")


if __name__ == "__main__":
    run()
