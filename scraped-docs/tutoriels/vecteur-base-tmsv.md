source: https://geoplateforme.github.io/tutoriels/production/vecteur/base/publication_tmsv/

[Diffusion](../../../tags/#tag:diffusion) [Donnée vecteur](../../../tags/#tag:donnée-vecteur) [TMS](../../../tags/#tag:tms)

# Diffusion en tuiles vectorielles à la volée

## Configuration de la diffusion

La configuration centralise toutes les informations nécessaires à la diffusion de données sur les services. A ce moment, on va contrôler les paramètres et détecter les erreurs ou conflits potentiels :

  * nom de couche déjà pris (il doit y avoir unicité sur toutes les configurations TMS vecteur de la plateforme)
  * table absente de la donnée stockée



Dans le cas du TMS vecteur, une configuration va donner plusieurs couches finales, le layername défini va servir de préfixe au nom des tables. On aura dans notre exemple les couches WFS :

  * `pays_ecoregions.regions_ecologiques`
  * `pays_ecoregions.pays`

/datastores/{datastore}/configurations

Corps de requête JSON
    
    
    {
        "type": "VECTOR-TMS",
        "name": "Pays et écorégions",
        "layer_name": "pays_ecoregions",
        "type_infos": {
            "used_data": [
                {
                    "relations": [
                        {
                            "native_name": "ecoregions",
                            "public_name": "regions_ecologiques",
                            "abstract": "Grandes régions naturelles mondiales"
                        },
                        {
                            "native_name": "pays",
                            "abstract": "Pays du monde"
                        }
                    ],
                    "stored_data": "{stored data}"
                }
            ]
        }
    }
    

Si on ne précise pas de public_name, c'est le nom natif de stockage qui est utilisé.

## Envoi sur les services de diffusion

À ce stade, aucune information n'a été envoyée aux serveurs pg_tileserv assurant la diffusion. Cette synchronisation de la configuration sur les serveurs de diffusion, représentés par le point d'accès, se fait via la création d'une offre: la publication. Elle matérialise la présence d'une configuration sur un point d'accès.

### Consultation des points de diffusion disponibles

/datastores/{datastore}

Corps de réponse JSON (champ `endpoints`)
    
    
    [
        {
            "name": "Service de diffusion WFS principal",
            "technical_name": "gpf-geoserver-wfs",
            "type": "WFS",
            "urls": [
                {
                    "type": "WFS",
                    "url": "https://data.geopf.fr/wfs/geoserver/ows"
                }
            ],
            "_id": "ae012611-13eb-4a18-8d04-9b7604a031cc",
            "open": true,
            "metadata_fi": "gpf-geoserver-wfs"
        },
        {
            "name": "Service de diffusion WMTS/TMS principal",
            "technical_name": "gpf-rok4-server-wmts-tms",
            "type": "WMTS-TMS",
            "urls": [
                {
                    "type": "WMTS",
                    "url": "https://data.geopf.fr/wmts"
                },
                {
                    "type": "TMS",
                    "url": "https://data.geopf.fr/tms/"
                }
            ],
            "_id": "ae032611-13eb-4a18-8d04-9b7604a031cc",
            "open": true,
            "metadata_fi": "gpf-rok4-server-wmts-tms"
        },
        {
            "name": "Service de diffusion WMS Raster principal",
            "technical_name": "gpf-rok4-server-wms-r",
            "type": "WMS-RASTER",
            "urls": [
                {
                    "type": "WMS",
                    "url": "https://data.geopf.fr/wms-r/wms"
                }
            ],
            "_id": "ae042611-13eb-4a18-8d04-9b7604a031cc",
            "open": true,
            "metadata_fi": "gpf-rok4-server-wms-r"
        },
        {
            "name": "Service de diffusion WMS Vecteur principal",
            "technical_name": "gpf-geoserver-wms-v",
            "type": "WMS-VECTOR",
            "urls": [
                {
                    "type": "WMS",
                    "url": "https://data.geopf.fr/wms-v/geoserver/ows"
                }
            ],
            "_id": "ae022611-13eb-4a18-8d04-9b7604a031cc",
            "open": true,
            "metadata_fi": "gpf-geoserver-wms-v"
        },
        {
            "name": "Service de Téléchargement principal",
            "technical_name": "gpf-download",
            "type": "DOWNLOAD",
            "urls": [
                {
                    "type": "DOWNLOAD",
                    "url": "https://data.geopf.fr/telechargement/"
                }
            ],
            "_id": "ae052611-13eb-4a18-8d04-9b7604a031cc",
            "open": true,
            "metadata_fi": "gpf-download"
        },
        {
            "name": "Service de diffusion CSW",
            "technical_name": "gpf-geonetwork",
            "type": "METADATA",
            "urls": [
                {
                    "type": "METADATA",
                    "url": "https://data.geopf.fr/csw"
                }
            ],
            "_id": "ae062611-13eb-4a18-8d04-9b7604a031cc",
            "open": true,
            "metadata_fi": "gpf-geonetwork"
        },
        {
            "name": "Service de téléchargement private",
            "technical_name": "gpf-download-private",
            "type": "DOWNLOAD",
            "urls": [
                {
                    "type": "DOWNLOAD",
                    "url": "https://data.geopf.fr/private/telechargement/"
                }
            ],
            "_id": "b5bf7ab2-8998-4829-8c80-cd2ec02e6e58",
            "open": false,
            "metadata_fi": "gpf-download-private"
        },
        {
            "name": "Service de diffusion WFS privé",
            "technical_name": "gpf-geoserver-wfs-private",
            "type": "WFS",
            "urls": [
                {
                    "type": "WFS",
                    "url": "https://data.geopf.fr/private/wfs/"
                }
            ],
            "_id": "d02feec9-1169-403f-bfc3-7ba6d6015ed4",
            "open": false,
            "metadata_fi": "gpf-geoserver-wfs-private"
        },
        {
            "name": "Service de diffusion WMS Vecteur privé",
            "technical_name": "gpf-geoserver-wms-v-private",
            "type": "WMS-VECTOR",
            "urls": [
                {
                    "type": "WMS",
                    "url": "https://data.geopf.fr/private/wms-v/"
                }
            ],
            "_id": "519c8bb1-9b7f-414a-9850-1a73dfd467ed",
            "open": false,
            "metadata_fi": "gpf-geoserver-wms-v-private"
        },
        {
            "name": "Service de diffusion WMS Raster privé",
            "technical_name": "gpf-rok4-server-wms-r-private",
            "type": "WMS-RASTER",
            "urls": [
                {
                    "type": "WMS",
                    "url": "https://data.geopf.fr/private/wms-r/"
                }
            ],
            "_id": "66866100-48eb-4340-bbc9-f5c7d9707928",
            "open": false,
            "metadata_fi": "gpf-rok4-server-wms-r-private"
        },
        {
            "name": "Service de diffusion WMTS/TMS privé",
            "technical_name": "gpf-rok4-server-wmts-tms-private",
            "type": "WMTS-TMS",
            "urls": [
                {
                    "type": "TMS",
                    "url": "https://data.geopf.fr/private/tms/"
                },
                {
                    "type": "WMTS",
                    "url": "https://data.geopf.fr/private/wmts/"
                }
            ],
            "_id": "7e0a92d1-8213-4ce0-8903-eb4c305a1849",
            "open": false,
            "metadata_fi": "gpf-rok4-server-wmts-tms-private"
        }
    ]
    

### Publication

/datastores/{datastore}/configurations/{configuration tms vecteur}/offerings

Corps de requête JSON
    
    
    {
        "endpoint": "{{ no such element: super_collections.SuperDict object['tmsv'] }}",
        "open": true
    }
    

On peut vérifier la présence de nos couches `pays_ecoregions.regions_ecologiques` et `pays_ecoregions.pays` dans le [getCapabilities du service TMS Vecteur](https://data.geopf.fr/vector-tms/1.0.0/index.json). On peut également avoir des [détails sur la couche pays_ecoregions.regions_ecologiques](https://data.geopf.fr/vector-tms/1.0.0/pays_ecoregions.regions_ecologiques.json) et des [détails sur la couche pays_ecoregions.pays](https://data.geopf.fr/vector-tms/1.0.0/pays_ecoregions.pays.json).

L'avantage de ce service est de pouvoir faire du filtrage côté serveur, en précisant un paramètre `filter`, ainsi que limiter les champs retournés avec le paramètre `properties`. Voici un exemple en définissant une source `Tuiles vectorielles` dans QGIs avec l'URL suivante : `https://data.geopf.fr/vector-tms/1.0.0/pays_ecoregions.regions_ecologiques/{z}/{x}/{y}.pbf?filter=realm='Palearctic'&properties=id,eco_name`
