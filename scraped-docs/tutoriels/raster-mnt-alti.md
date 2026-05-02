source: https://geoplateforme.github.io/tutoriels/production/raster/mnt/publication_alti/

[Diffusion](../../../tags/#tag:diffusion) [Donnée raster](../../../tags/#tag:donnée-raster) [MNT](../../../tags/#tag:mnt) [Service d'altimétrie](../../../tags/#tag:service-daltimétrie)

# Publication sur le service d'altimétrie

La pyramide générée va être également utilisable par le service d'altimétrie. Ce dernier permet de récupérer les altitudes en un point, ainsi que demander un profil altimétrique. Nous allons ici utiliser la donnée MNT ainsi que le MNS.

## Configuration de la diffusion

/datastores/{datastore}/configurations

Corps de requête JSON pour lidarhd
    
    
    {
        "type": "ALTIMETRY",
        "name": "LidarHD : MNT et MNS",
        "layer_name": "lidarhd_test",
        "type_infos": {
            "title": "LidarHD : MNT et MNS",
            "abstract": "LidarHD : MNT et MNS, à 50 cm",
            "keywords": [
                "LidarHD",
                "MNT",
                "MNS"
            ],
            "used_data": [
                {
                    "title": "MNT à 50cm, issu du Lidar HD",
                    "stored_data": "{stored data MNT}",
                    "source": {
                        "value": "Lidar HD"
                    },
                    "accuracy": {
                        "value": "Moins de 1m"
                    }
                },
                {
                    "title": "MNS à 50cm, issu du Lidar HD",
                    "stored_data": "{stored data MNS}",
                    "source": {
                        "value": "Lidar HD"
                    },
                    "accuracy": {
                        "value": "Moins de 1m"
                    }
                }
            ]
        }
    }
    

Les informations pour la source et la précision de la donnée peuvent être définies de manière statiques, comme ici, ou bien s'appuyer sur des pyramides raster (1 canal entier). On précisera alors la correspondance entre la valeur entière du pixel et l'intitulé de l'information.

## Envoi sur les services de diffusion

### Consultation des points de diffusion disponibles

Ce sont les points d'accès de type `ALTIMETRY` qui nous intéressent ici.

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

/datastores/{datastore}/configurations/{configuration altimétrie}/offerings

Corps de requête JSON
    
    
    {
        "endpoint": "0ac92a1e-aa86-4843-8528-e303f12296e5",
        "open": true
    }
    

On peut vérifier la présence de notre ressource couche `lidarhd_test` dans le [getCapabilities du service](https://data.geopf.fr/altimetrie/resources). Voici un exemple de demande d'altitude en deux points :

https://data.geopf.fr/altimetrie/calcul/alti/rest/elevation.json

Paramètres de requêteCorps de réponse JSON

  * resource = `lidarhd_test`
  * lon = `5.96|5.961`
  * lat = `45.13|45.131`
  * measures = `true`


    
    
    {
        "elevations": [
            {
                "lon": 5.96,
                "lat": 45.13,
                "z": 1995.53,
                "acc": "Moins de 1m",
                "measures": [
                    {
                        "z": 1995.53,
                        "source_name": "Lidar HD",
                        "source_measure": "Fixed value",
                        "acc": "Moins de 1m",
                        "title": "MNS \u00e0 50cm, issu du Lidar HD"
                    },
                    {
                        "z": 1989.14,
                        "source_name": "Lidar HD",
                        "source_measure": "Fixed value",
                        "acc": "Moins de 1m",
                        "title": "MNT \u00e0 50cm, issu du Lidar HD"
                    }
                ]
            },
            {
                "lon": 5.961,
                "lat": 45.131,
                "z": 2098.24,
                "acc": "Moins de 1m",
                "measures": [
                    {
                        "z": 2098.24,
                        "source_name": "Lidar HD",
                        "source_measure": "Fixed value",
                        "acc": "Moins de 1m",
                        "title": "MNT \u00e0 50cm, issu du Lidar HD"
                    },
                    {
                        "z": 2098.24,
                        "source_name": "Lidar HD",
                        "source_measure": "Fixed value",
                        "acc": "Moins de 1m",
                        "title": "MNS \u00e0 50cm, issu du Lidar HD"
                    }
                ]
            }
        ]
    }
    
