"""Scrape geoplateforme.github.io docs pages to scraped-docs/."""
import re
import time
from pathlib import Path

import html2text
import requests

BASE = "https://geoplateforme.github.io"

PAGES = [
    # entrepôt
    ("entrepot", "composants",    f"{BASE}/entrepot/production/composants/"),
    ("entrepot", "concepts",      f"{BASE}/entrepot/production/concepts/"),
    # sdk
    ("sdk", "configuration",             f"{BASE}/sdk-entrepot/configuration/"),
    ("sdk", "configuration_details",     f"{BASE}/sdk-entrepot/configuration_details/"),
    ("sdk", "comme-executable",          f"{BASE}/sdk-entrepot/comme-executable/"),
    ("sdk", "comme-module",              f"{BASE}/sdk-entrepot/comme-module/"),
    ("sdk", "upload_descriptor",         f"{BASE}/sdk-entrepot/upload_descriptor/"),
    ("sdk", "workflow",                  f"{BASE}/sdk-entrepot/workflow/"),
    ("sdk", "resolveurs",                f"{BASE}/sdk-entrepot/resolveurs/"),
    ("sdk", "tutoriel_1_archive",        f"{BASE}/sdk-entrepot/tutoriel_1_archive/"),
    ("sdk", "tutoriel_2_flux_vecteur",   f"{BASE}/sdk-entrepot/tutoriel_2_flux_vecteur/"),
    ("sdk", "tutoriel_3_flux_raster",    f"{BASE}/sdk-entrepot/tutoriel_3_flux_raster/"),
    ("sdk", "tutoriel_pcrs",             f"{BASE}/sdk-entrepot/tutoriel_pcrs/"),
    # tutoriels — vecteur base
    ("tutoriels", "vecteur-base-livraison",        f"{BASE}/tutoriels/production/vecteur/base/livraison/"),
    ("tutoriels", "vecteur-base-integration",      f"{BASE}/tutoriels/production/vecteur/base/integration/"),
    ("tutoriels", "vecteur-base-wfs",              f"{BASE}/tutoriels/production/vecteur/base/publication_wfs/"),
    ("tutoriels", "vecteur-base-statique",         f"{BASE}/tutoriels/production/vecteur/base/gestion_statique/"),
    ("tutoriels", "vecteur-base-wms",              f"{BASE}/tutoriels/production/vecteur/base/publication_wms/"),
    ("tutoriels", "vecteur-base-tmsv",             f"{BASE}/tutoriels/production/vecteur/base/publication_tmsv/"),
    ("tutoriels", "vecteur-base-tuilage",          f"{BASE}/tutoriels/production/vecteur/base/tuilage/"),
    ("tutoriels", "vecteur-base-fme",              f"{BASE}/tutoriels/production/vecteur/base/alimentation_fme/"),
    # tutoriels — vecteur mise à jour
    ("tutoriels", "vecteur-maj-initialisation",   f"{BASE}/tutoriels/production/vecteur/mise-a-jour/initialisation/"),
    ("tutoriels", "vecteur-maj-injection1",        f"{BASE}/tutoriels/production/vecteur/mise-a-jour/injection1/"),
    ("tutoriels", "vecteur-maj-injection2",        f"{BASE}/tutoriels/production/vecteur/mise-a-jour/injection2/"),
    ("tutoriels", "vecteur-maj-delete-update",     f"{BASE}/tutoriels/production/vecteur/mise-a-jour/delete_update/"),
    # tutoriels — vecteur dérivation
    ("tutoriels", "vecteur-derivation",            f"{BASE}/tutoriels/production/vecteur/derivation/"),
    ("tutoriels", "vecteur-derivation-exemple1",   f"{BASE}/tutoriels/production/vecteur/derivation/exemple1/"),
    # tutoriels — raster base
    ("tutoriels", "raster-base-livraison",         f"{BASE}/tutoriels/production/raster/base/livraison/"),
    ("tutoriels", "raster-base-pyramide",          f"{BASE}/tutoriels/production/raster/base/calcul_pyramide/"),
    ("tutoriels", "raster-base-wmts-tms",          f"{BASE}/tutoriels/production/raster/base/publication_tuile/"),
    ("tutoriels", "raster-base-wms",               f"{BASE}/tutoriels/production/raster/base/publication_wms/"),
    ("tutoriels", "raster-base-pyramide-wms",      f"{BASE}/tutoriels/production/raster/base/calcul_pyramide_wms/"),
    # tutoriels — raster mise à jour
    ("tutoriels", "raster-maj-furetamesure",       f"{BASE}/tutoriels/production/raster/mise-a-jour/furetamesure/"),
    ("tutoriels", "raster-maj-parinjection",       f"{BASE}/tutoriels/production/raster/mise-a-jour/parinjection/"),
    ("tutoriels", "raster-maj-composition",        f"{BASE}/tutoriels/production/raster/mise-a-jour/composition/"),
    # tutoriels — raster MNT
    ("tutoriels", "raster-mnt-livraison",          f"{BASE}/tutoriels/production/raster/mnt/livraison/"),
    ("tutoriels", "raster-mnt-calcul",             f"{BASE}/tutoriels/production/raster/mnt/calcul/"),
    ("tutoriels", "raster-mnt-wms",                f"{BASE}/tutoriels/production/raster/mnt/publication_wms/"),
    ("tutoriels", "raster-mnt-alti",               f"{BASE}/tutoriels/production/raster/mnt/publication_alti/"),
    # tutoriels — archive
    ("tutoriels", "archive-livraison",             f"{BASE}/tutoriels/production/archive/base/livraison/"),
    ("tutoriels", "archive-integration",           f"{BASE}/tutoriels/production/archive/base/integration/"),
    ("tutoriels", "archive-publication",           f"{BASE}/tutoriels/production/archive/base/publication/"),
    # tutoriels — recherche
    ("tutoriels", "recherche-standard",            f"{BASE}/tutoriels/production/recherche/standard/"),
    ("tutoriels", "recherche-custom-creation",     f"{BASE}/tutoriels/production/recherche/custom/creation/"),
    ("tutoriels", "recherche-custom-recherche",    f"{BASE}/tutoriels/production/recherche/custom/recherche/"),
    # tutoriels — compléments
    ("tutoriels", "complement-annexes-televersement",  f"{BASE}/tutoriels/production/complement/annexes/televersement/"),
    ("tutoriels", "complement-annexes-publication",    f"{BASE}/tutoriels/production/complement/annexes/publication/"),
    ("tutoriels", "complement-metadonnees-televersement", f"{BASE}/tutoriels/production/complement/metadonnees/televersement/"),
    ("tutoriels", "complement-metadonnees-publication",   f"{BASE}/tutoriels/production/complement/metadonnees/publication/"),
    ("tutoriels", "complement-documents-televersement",   f"{BASE}/tutoriels/production/complement/documents/televersement/"),
    ("tutoriels", "complement-documents-partage",         f"{BASE}/tutoriels/production/complement/documents/partage/"),
    # tutoriels — services haut-niveau
    ("tutoriels", "hautniveau-extraction-production",  f"{BASE}/tutoriels/production/hautniveau/extraction/production/"),
    ("tutoriels", "hautniveau-extraction-utilisation", f"{BASE}/tutoriels/production/hautniveau/extraction/utilisation/"),
    ("tutoriels", "hautniveau-validation-api",         f"{BASE}/tutoriels/production/hautniveau/validation/api/"),
    ("tutoriels", "hautniveau-validation-integree",    f"{BASE}/tutoriels/production/hautniveau/validation/integree/"),
    # tutoriels — contrôle des accès
    ("tutoriels", "acces-creation-compte",     f"{BASE}/tutoriels/production/controle-des-acces/entrepot/creation_compte/"),
    ("tutoriels", "acces-connexion-api",       f"{BASE}/tutoriels/production/controle-des-acces/entrepot/connexion_api/"),
    ("tutoriels", "acces-connexion-fme",       f"{BASE}/tutoriels/production/controle-des-acces/entrepot/connexion_fme/"),
    ("tutoriels", "acces-permission",          f"{BASE}/tutoriels/production/controle-des-acces/diffusion/permission/"),
    ("tutoriels", "acces-cle",                 f"{BASE}/tutoriels/production/controle-des-acces/diffusion/cle/"),
    # tutoriels — gestion
    ("tutoriels", "gestion-organisme",         f"{BASE}/tutoriels/production/gestion/organisme/"),
    ("tutoriels", "gestion-membres",           f"{BASE}/tutoriels/production/gestion/communaute/gestion_membres/"),
    ("tutoriels", "gestion-espaces",           f"{BASE}/tutoriels/production/gestion/administrateur/espaces/"),
    # tutoriels — divers
    ("tutoriels", "divers-thematique",         f"{BASE}/tutoriels/production/divers/thematique/"),
    # tutoriels — compatibilités cartes.gouv
    ("tutoriels", "cartesgouv-alimentation",   f"{BASE}/tutoriels/production/compatibilites/cartes-gouv/alimentation/"),
    ("tutoriels", "cartesgouv-entree-carto",   f"{BASE}/tutoriels/production/compatibilites/cartes-gouv/entree-carto/"),
    ("tutoriels", "cartesgouv-catalogue",      f"{BASE}/tutoriels/production/compatibilites/cartes-gouv/catalogue/"),
]

h2md = html2text.HTML2Text()
h2md.ignore_links = False
h2md.ignore_images = True
h2md.body_width = 0


def fetch_page(section: str, slug: str, url: str) -> None:
    out_dir = Path("scraped-docs") / section
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slug}.md"

    resp = requests.get(url, timeout=15)
    resp.raise_for_status()

    m = re.search(r'<article[^>]*>(.*?)</article>', resp.text, re.DOTALL)
    if not m:
        print(f"  WARNING: no <article> found for {url}")
        content = resp.text
    else:
        content = m.group(1)

    md = h2md.handle(content)
    out_path.write_text(f"source: {url}\n\n{md}", encoding="utf-8")
    print(f"  saved {out_path} ({len(md)} chars)")


def main() -> None:
    for section, slug, url in PAGES:
        print(f"fetching {slug}...")
        try:
            fetch_page(section, slug, url)
        except Exception as e:
            print(f"  ERROR {url}: {e}")
        time.sleep(0.3)

    print(f"\nDone. {len(PAGES)} pages scraped.")


if __name__ == "__main__":
    main()
