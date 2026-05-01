from datetime import date, datetime, timezone
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

_FRANCE_BBOX = {"west": -5.15, "east": 9.57, "south": 41.32, "north": 51.10}
_LICENSE_LABELS = {
    "odc-odbl": "Open Database License (ODbL)",
    "fr-lo": "Licence Ouverte / Open Licence",
    "cc-by": "Creative Commons Attribution",
    "cc-by-sa": "Creative Commons Attribution-ShareAlike",
    "cc-zero": "Creative Commons Zero (CC0)",
    "notspecified": "Non spécifiée",
}


def _parse_date(value: str | None) -> str:
    if not value:
        return date.today().isoformat()
    try:
        return datetime.fromisoformat(value).date().isoformat()
    except ValueError:
        return date.today().isoformat()


def dataset_to_xml(dataset: dict, file_identifier: str | None = None) -> str:
    spatial = dataset.get("spatial") or {}
    geom = spatial.get("geom")
    if geom and geom.get("type") == "Polygon":
        coords = geom["coordinates"][0]
        lons = [c[0] for c in coords]
        lats = [c[1] for c in coords]
        bbox = {"west": min(lons), "east": max(lons), "south": min(lats), "north": max(lats)}
    else:
        bbox = _FRANCE_BBOX

    org = dataset.get("organization") or {}
    license_slug = dataset.get("license") or "notspecified"

    context = {
        "file_identifier": file_identifier or dataset["id"],
        "title": dataset["title"],
        "abstract": dataset.get("description") or dataset.get("description_short") or dataset["title"],
        "organisation_name": org.get("name") or "Inconnu",
        "date_stamp": _parse_date(dataset.get("last_modified")),
        "created_date": _parse_date(dataset.get("created_at")),
        "keywords": dataset.get("tags") or [],
        "license": _LICENSE_LABELS.get(license_slug, license_slug),
        "bbox": bbox,
    }

    env = Environment(loader=FileSystemLoader(Path(__file__).parent), autoescape=False)
    tmpl = env.get_template("template.xml.j2")
    return tmpl.render(**context)
