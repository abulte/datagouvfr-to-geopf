import hashlib
import time
from pathlib import Path

import requests

from auth import auth_headers

API_ROOT = "https://data.geopf.fr/api"
VECTOR_INTEGRATION_ID = "0de8c60b-9938-4be9-aa36-9026b77c3c96"
POLL_INTERVAL = 10


def _ds(datastore_id: str) -> str:
    return f"{API_ROOT}/datastores/{datastore_id}"


# --- livraison ---

def add_tags(datastore_id: str, entity: str, entity_id: str, tags: dict) -> None:
    resp = requests.post(
        f"{_ds(datastore_id)}/{entity}/{entity_id}/tags",
        headers={**auth_headers(), "content-type": "application/json"},
        json=tags,
    )
    if not resp.ok:
        raise RuntimeError(f"add tags failed {resp.status_code}: {resp.text}")


def create_upload(datastore_id: str, name: str, srs: str) -> str:
    resp = requests.post(
        f"{_ds(datastore_id)}/uploads",
        headers={**auth_headers(), "content-type": "application/json"},
        json={"name": name, "description": name, "type": "VECTOR", "srs": srs},
    )
    if not resp.ok:
        raise RuntimeError(f"create upload failed {resp.status_code}: {resp.text}")
    upload_id = resp.json()["_id"]
    print(f"  Created upload: {upload_id}")
    return upload_id


def push_file(datastore_id: str, upload_id: str, filename: str, content: bytes) -> None:
    resp = requests.post(
        f"{_ds(datastore_id)}/uploads/{upload_id}/data",
        headers=auth_headers(),
        files={"file": (filename, content)},
        params={"path": f"/{filename}"},
    )
    if not resp.ok:
        raise RuntimeError(f"push file failed {resp.status_code}: {resp.text}")
    print(f"  Pushed file: {filename}")


def push_md5(datastore_id: str, upload_id: str, filename: str, content: bytes) -> None:
    md5 = hashlib.md5(content).hexdigest()
    md5_content = f"{md5}  {filename}\n".encode()
    resp = requests.post(
        f"{_ds(datastore_id)}/uploads/{upload_id}/md5",
        headers=auth_headers(),
        files={"file": ("checksums.md5", md5_content)},
    )
    if not resp.ok:
        raise RuntimeError(f"push md5 failed {resp.status_code}: {resp.text}")
    print(f"  Pushed MD5: {md5}")


def close_upload(datastore_id: str, upload_id: str) -> None:
    resp = requests.post(
        f"{_ds(datastore_id)}/uploads/{upload_id}/close",
        headers=auth_headers(),
    )
    if not resp.ok:
        raise RuntimeError(f"close upload failed {resp.status_code}: {resp.text}")
    print("  Upload closed — checks running...")


def wait_for_checks(datastore_id: str, upload_id: str, timeout: int = 600) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        resp = requests.get(
            f"{_ds(datastore_id)}/uploads/{upload_id}",
            headers=auth_headers(),
        )
        resp.raise_for_status()
        status = resp.json().get("status")
        if status == "CLOSED":
            print("  Checks passed.")
            return
        if status == "UNSTABLE":
            checks = requests.get(
                f"{_ds(datastore_id)}/uploads/{upload_id}/checks",
                headers=auth_headers(),
            ).json()
            raise RuntimeError(f"Upload checks failed: {checks}")
        print(f"  Upload status: {status} — waiting...")
        time.sleep(POLL_INTERVAL)
    raise TimeoutError("Timed out waiting for upload checks.")


# --- processing ---

def create_and_launch_processing(datastore_id: str, upload_id: str, name: str, srs: str) -> str:
    resp = requests.post(
        f"{_ds(datastore_id)}/processings/executions",
        headers={**auth_headers(), "content-type": "application/json"},
        json={
            "processing": VECTOR_INTEGRATION_ID,
            "inputs": {"upload": [upload_id]},
            "output": {"stored_data": {"name": name}},
            "parameters": {"srs": srs},
        },
    )
    if not resp.ok:
        raise RuntimeError(f"create processing execution failed {resp.status_code}: {resp.text}")
    exec_id = resp.json()["_id"]
    print(f"  Created processing execution: {exec_id}")

    launch = requests.post(
        f"{_ds(datastore_id)}/processings/executions/{exec_id}/launch",
        headers=auth_headers(),
    )
    if not launch.ok:
        raise RuntimeError(f"launch processing execution failed {launch.status_code}: {launch.text}")
    print("  Processing launched...")
    return exec_id


def delete_upload(datastore_id: str, upload_id: str) -> None:
    resp = requests.delete(
        f"{_ds(datastore_id)}/uploads/{upload_id}",
        headers=auth_headers(),
    )
    if not resp.ok:
        raise RuntimeError(f"delete upload failed {resp.status_code}: {resp.text}")
    print(f"  Livraison deleted: {upload_id}")


def wait_for_stored_data(datastore_id: str, exec_id: str, timeout: int = 900) -> str:
    deadline = time.time() + timeout
    while time.time() < deadline:
        resp = requests.get(
            f"{_ds(datastore_id)}/processings/executions/{exec_id}",
            headers=auth_headers(),
        )
        resp.raise_for_status()
        data = resp.json()
        status = data.get("status")
        if status == "SUCCESS":
            stored_data_id = data["output"]["stored_data"]["_id"]
            print(f"  Stored data created: {stored_data_id}")
            return stored_data_id
        if status in ("FAILURE", "ABORTED"):
            raise RuntimeError(f"Processing {status}: check logs at {exec_id}")
        print(f"  Processing status: {status} — waiting...")
        time.sleep(POLL_INTERVAL)
    raise TimeoutError("Timed out waiting for processing execution.")


# --- main entry point ---

def ingest_dataset(datastore_id: str, name: str, file: Path, srs: str = "EPSG:4326") -> str:
    """Full pipeline: file → livraison → integration → stored_data. Returns stored_data ID."""
    print(f"\n[1/4] Using file: {file}")
    filename, content = file.name, file.read_bytes()

    print("\n[2/4] Creating livraison...")
    upload_id = create_upload(datastore_id, name, srs)
    add_tags(datastore_id, "uploads", upload_id, {"datasheet_name": name})
    push_file(datastore_id, upload_id, filename, content)
    push_md5(datastore_id, upload_id, filename, content)
    close_upload(datastore_id, upload_id)
    wait_for_checks(datastore_id, upload_id)

    print("\n[3/4] Running vector integration...")
    exec_id = create_and_launch_processing(datastore_id, upload_id, name, srs)
    stored_data_id = wait_for_stored_data(datastore_id, exec_id)
    add_tags(datastore_id, "stored_data", stored_data_id, {"datasheet_name": name})
    delete_upload(datastore_id, upload_id)

    print(f"\n[4/4] Done — fiche created: {stored_data_id}")
    return stored_data_id
