import argparse
import json
import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

from auth import auth_headers
from mapper import dataset_to_xml
from pipeline import ingest_dataset

load_dotenv()

API_ROOT = "https://data.geopf.fr/api"
CSW_ENDPOINT_ID = "ae062611-13eb-4a18-8d04-9b7604a031cc"


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
    print(f"  Metadata published to CSW.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish a data.gouv.fr dataset to Geoplateforme.")
    parser.add_argument("name", help="Unique test name (used for upload name and fileIdentifier)")
    parser.add_argument("--file", type=Path, default=None, help="Vector file to upload (required unless --skip-data)")
    parser.add_argument("--srs", default="EPSG:4326", help="SRS of the source data (default: EPSG:4326)")
    parser.add_argument("--skip-data", action="store_true", help="Skip data ingestion, only upload metadata")
    args = parser.parse_args()

    if not args.skip_data and args.file is None:
        parser.error("--file is required unless --skip-data is set")

    dataset = json.loads(Path("dataset.json").read_text())
    datastore_id = get_datastore_id()
    file_identifier = f"{dataset['id']}-{args.name}"

    if not args.skip_data:
        ingest_dataset(datastore_id, dataset, name=args.name, file=args.file, srs=args.srs)

    print("\n[metadata] Uploading and publishing metadata...")
    xml = dataset_to_xml(dataset, file_identifier=file_identifier)
    upload_metadata(datastore_id, xml, file_identifier, datasheet_name=args.name)

    print(f"\nAll done. Fiche visible at:")
    print(f"  https://cartes.gouv.fr/tableau-de-bord/entrepots/{datastore_id}/donnees")
    print(f"\nCSW record:")
    print(f"  https://data.geopf.fr/csw?SERVICE=CSW&REQUEST=GetRecordById&VERSION=2.0.2&ID={file_identifier}&ElementSetName=full")


if __name__ == "__main__":
    main()
