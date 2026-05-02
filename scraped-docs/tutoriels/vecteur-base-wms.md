source: https://geoplateforme.github.io/tutoriels/production/vecteur/base/publication_wms/

[Diffusion](../../../tags/#tag:diffusion) [Donnée vecteur](../../../tags/#tag:donnée-vecteur) [WMS](../../../tags/#tag:wms)

# Publication en WMS

## Configuration de la diffusion WMS

Contrairement au WFS, une configuration WMS va définir une couche seule couche finale. Il est possible d'utiliser plusieurs tables, mais seul l'agrégat sera consultable, avec les styles définis.

La création de la configuration WMS va permettre de vérifier de nombreuses informations :

  * nom de couche déjà pris (il doit y avoir unicité sur toutes les configurations WMS Vecteur de la plateforme)
  * table absente de la donnée stockée
  * style ou FTL exploitant des attributs absent de la table utilisée

/datastores/{datastore}/configurations

Corps de requête JSON
    
    
    {
        "type": "WMS-VECTOR",
        "name": "Écorégions et frontières des pays",
        "layer_name": "ecoregions_tutoriel",
        "type_infos": {
            "title": "Mes écorégions",
            "abstract": "Grandes régions naturelles mondiales",
            "keywords": [
                "Tutoriel", "Données mondiales"
            ],
            "bbox": {
                "west": -175,
                "south": -75,
                "east": 175,
                "north": 85
            },
            "used_data": [
                {
                    "relations": [
                        {
                            "name": "pays",
                            "style": "{sld pays}",
                            "ftl": "{ftl pays}"
                        },
                        {
                            "name": "ecoregions",
                            "style": "{sld ecoregions}",
                            "ftl": "{ftl ecoregions}"
                        }
                    ],
                    "stored_data": "{stored data}"
                }
            ]
        }
    }
    

Attention

Une configuration WMS-VECTOR donnera une unique couche. Même si elle utilise plusieurs tables, ces dernières ne seront pas consultables individuellement en WMS. Si c'est votre besoin, faites une configuration (et donc une couche) par table.

## Envoi sur les services de diffusion

Comme pour le WFS, seule la création d'une offre sur un point d'accès (publication) permet d'envoyer les informations de configuration au serveurs de diffusion.

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

/datastores/{datastore}/configurations/{configuration wms}/offerings

Corps de requête JSON
    
    
    {
        "endpoint": "ae022611-13eb-4a18-8d04-9b7604a031cc",
        "open": true
    }
    

On peut vérifier la présence de notre couche `ecoregions_tutoriel` dans le [getCapabilities du service](https://data.geopf.fr/wms-v?REQUEST=GetCapabilities&SERVICE=WMS&VERSION=1.3.0)
