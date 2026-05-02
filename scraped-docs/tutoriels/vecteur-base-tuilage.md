source: https://geoplateforme.github.io/tutoriels/production/vecteur/base/tuilage/

[Donnée vecteur](../../../tags/#tag:donnée-vecteur) [Dérivation](../../../tags/#tag:dérivation) [Fichier de style](../../../tags/#tag:fichier-de-style) [TMS](../../../tags/#tag:tms)

# Diffusion en tuiles vectorielles précalculée

Cette étape supplémentaire permet une diffusion à plus grande échelle de données vecteurs. Seules les parties nouvelles sont détaillées.

## Calcul de la pyramide de tuiles vectorielle

### Consultation des traitements disponibles

/datastores/{datastore}/processings

Corps de réponse JSON
    
    
    [
        {
            "name": "Intégration de données vecteur livrées en base",
            "description": "Ce traitement permet de stocker dans les bases de données PostgreSQL de la plateforme des données vecteurs livrées. Les formats pris en charge sont le CSV, le Shapefile, le Geopackage et le GeoJSON. Il est également possible de préciser un autre système afin de réaliser une reprojection à l'intégration",
            "_id": "0de8c60b-9938-4be9-aa36-9026b77c3c96"
        },
        {
            "name": "Recopie d'une archive livrée",
            "description": "Génération ou mise à jour d'une donnée stockée ARCHIVE à partir d'une archive livrées. Si un fichier livré existait déjà dans la donnée en sortie, celui ci va écraser l'ancienne version",
            "_id": "12cdc646-3976-4f18-b273-f34fca37e2a6"
        },
        {
            "name": "Calcul de pyramide raster",
            "description": "Génération ou mise à jour d'une pyramide de tuiles raster à partir d'une livraison d'images géo-référencées",
            "_id": "2ae50661-986c-4f47-a3f0-e380417b522c"
        },
        {
            "name": "Calcul ou mise à jour de pyramide raster par moissonnage WMS",
            "description": "Il n'y a pas besoin de donnée en entrée. Sont fournis en paramètres toutes les informations sur le service WMS et le jeu de données à moissonner, ainsi que la zone sur laquelle faire le moissonnage",
            "_id": "6a54dc92-fc93-4c8e-9f02-046bf889550e"
        },
        {
            "name": "Fusion de pyramides raster",
            "description": "Ce traitement permet de générer une pyramide raster par composition de plusieurs pyramides indépendantes. Seules les dalles présentes dans plusieurs entrées seront recalculées. Celles présentes dans une seule entrée seront référencées. La pyramide en sortie a donc des dépendances avec celles en entrée.",
            "_id": "7cdca031-9e86-4804-8764-9b1d783b087d"
        },
        {
            "name": "Calcul de pyramide vecteur",
            "description": "Génération ou mise à jour d'une pyramide de tuiles vectorielles à partir d'une donnée vecteur en base",
            "_id": "aa5f9391-0bdb-4b97-9209-fcde351b82f6"
        }
    ]
    

### Consultation du traitement qui nous intéresse

/datastores/{datastore}/processings/aa5f9391-0bdb-4b97-9209-fcde351b82f6

Corps de réponse JSON
    
    
    {
        "name": "Calcul de pyramide vecteur",
        "description": "Génération ou mise à jour d'une pyramide de tuiles vectorielles à partir d'une donnée vecteur en base",
        "input_types": {
            "upload": [],
            "stored_data": [
                "VECTOR-DB",
                "ROK4-PYRAMID-VECTOR"
            ]
        },
        "output_type": {
            "stored_data": "ROK4-PYRAMID-VECTOR",
            "storage": [
                "S3"
            ]
        },
        "parameters": [
            {
                "name": "composition",
                "description": "Tables à exporter et niveaux limites d'utilisation",
                "mandatory": false,
                "constraints": {
                    "$schema": "https://json-schema.org/draft/2020-12/schema",
                    "required": [
                        "table",
                        "bottom_level",
                        "top_level"
                    ],
                    "properties": {
                        "layer": {
                            "type": "string"
                        },
                        "table": {
                            "type": "string"
                        },
                        "filter": {
                            "type": "string"
                        },
                        "top_level": {
                            "type": "string"
                        },
                        "attributes": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "bottom_level": {
                            "type": "string"
                        }
                    }
                }
            },
            {
                "name": "bottom_level",
                "description": "Niveau du bas de la pyramide (obligatoire si pas de composition fournie)",
                "mandatory": false
            },
            {
                "name": "width",
                "description": "Nombre de tuiles dans une dalle, dans le sens de la largeur",
                "mandatory": false,
                "default_value": 16
            },
            {
                "name": "top_level",
                "description": "Niveau du haut de la pyramide (obligatoire si pas de composition fournie)",
                "mandatory": false
            },
            {
                "name": "tippecanoe_options",
                "description": "Options de l'outil tippecanoe pour la généralisation des données vecteur",
                "mandatory": false
            },
            {
                "name": "area",
                "description": "WKT de la zone sur laquelle le moissonnage doit se faire, en EPSG:4326 (obligatoire si la base vecteur en entrée n'a pas d'étendue)",
                "mandatory": false
            },
            {
                "name": "height",
                "description": "Nombre de tuiles dans une dalle, dans le sens de la haureur",
                "mandatory": false,
                "default_value": 16
            },
            {
                "name": "parallelization",
                "description": "Nombre de scripts d'écriture des dalles en parallèle",
                "mandatory": false,
                "default_value": 1
            }
        ],
        "_id": "aa5f9391-0bdb-4b97-9209-fcde351b82f6"
        "required_checks": []
    }
    

### Configuration d'une exécution de ce traitement

Points d'attentions

Les niveaux sur lesquels on transforme les données vecteurs en tuiles vectorielles sont importants : en calculant un niveau trop résolu (trop bas), le temps de génération et le volume occupé par la pyramide en sortie sera inutilement grand. En utilisant une table volumineuse dans des niveaux trop hauts, les tuiles seront très lourdes car contenant trop de données (ou vidées de la majoraité des objets). Il faut donc prêter une attention particulière aux niveaux d'utilisation des tables.

Dans notre exemple ici, on choisit un cas simple : les pays sont présents dans tous les niveaux, et les écorégions ne seront présents que jusqu'au niveau 5. On ne filtre pas les données et on ne change pas les noms des tables dans les tuiles. On veut tous les attributs.

/datastores/{datastore}/processings/executions

Corps de requête JSON
    
    
    {
        "processing": "aa5f9391-0bdb-4b97-9209-fcde351b82f6",
        "inputs": {
        "stored_data": [
            "{stored data}"
        ]
        },
        "output": {
            "stored_data": {
                "name": "Pays et éco-régions",
                "storage_tags": ["VECTEUR"]
            }
        },
        "parameters": {
            "composition": [
                {
                    "table": "ecoregions",
                    "bottom_level": "9",
                    "top_level": "5",
                    "attributes": ["*"]
                },
                {
                    "table": "pays",
                    "bottom_level": "9",
                    "top_level": "0",
                    "attributes": ["*"]
                }
            ]
        }
    }
    

### Consultation de la donnée stockée en sortie

À la fin du traitement, des informations concernant la donnée finale sont remontées afin d'apparaître au niveau de l'API (taille, étendue, système de coordonnées, grille et niveaux).

/datastores/{datastore}/stored_data/{stored data pyramide}

Corps de réponse JSON
    
    
    {
        "name": "Pays et éco-régions",
        "type": "ROK4-PYRAMID-VECTOR",
        "srs": "EPSG:3857",
        "contact": "contact@ign.fr",
        "extent": {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        175,
                        -85
                    ],
                    [
                        175,
                        83.623596
                    ],
                    [
                        -175,
                        83.623596
                    ],
                    [
                        -175,
                        -85
                    ],
                    [
                        175,
                        -85
                    ]
                ]
            ]
        },
        "last_event": {
            "title": "Génération",
            "date": "2023-07-12T09:04:07.271074",
            "initiator": {
                "_id": "{user}"
            }
        },
        "tags": {},
        "storage": {
            "type": "S3",
            "labels": []
        },
        "size": 79570364,
        "status": "GENERATED",
        "_id": "{stored data pyramide}",
        "type_infos": {
            "tms": "PM",
            "levels": [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9"
            ]
        }
    }
    

## Diffusion des tuiles vectorielles

Les données de la pyramide de tuiles vectorielles sont diffusable selon l'API Tile Map Service. Cette API est disponible sur un point d'accès de type WMTS-TMS.

### Création de la configuration

/datastores/{datastore}/configurations

Corps de requête JSON
    
    
    {
        "type": "WMTS-TMS",
        "name": "Pays et écorégions",
        "layer_name": "pays_ecoregions",
        "type_infos": {
            "title": "Mes écorégions",
            "abstract": "Grandes régions naturelles mondiales",
            "used_data": [
                {
                    "bottom_level": "9",
                    "top_level": "0",
                    "stored_data": "{stored data}"
                }
            ]
        }
    }
    

La donnée n'est pas représentée côté serveur, il n'y a donc pas de fichier de style à préciser au niveau de la configuration.

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

$/datastores/{datastore}/configurations/{configuration wmts-tms}/offerings

Corps de requête JSON
    
    
    {
        "endpoint": "ae032611-13eb-4a18-8d04-9b7604a031cc",
        "open": true
    }
    

On peut vérifier la présence de notre couche `pays_ecoregions` dans le [getCapabilities du service TMS](https://data.geopf.fr/tms/1.0.0). On peut également avoir des [détails sur cette couche](https://data.geopf.fr/tms/1.0.0/pays_ecoregions).

On peut également récupérer nos données dans QGis. Il faut ajouter une source de donnée "Tuile vectorielle" et précisé comme URL `https://data.geopf.fr/tms/1.0.0/pays_ecoregions/{z}/{x}/{y}.pbf`

### Hébergement du style sous forme d'annexe

L'affichage des tuiles vectorielles implique l'application d'un style côté client. Il suffit donc de fournir un style accessible pour faciliter la consommation de telles données. On va exploiter la fonctionnalité des annexes pour mettre à disposition une URL publique pour un tel style. 

Ce [style d'exemple](../../../assets/data/pays_ecoregions.json) est format mapbox.

/datastores/{datastore}/annexes

Corps de requête MultipartCorps de réponse JSON

  * file = `<pays_ecoregions.json>`
  * paths = `styles/mapbox/pays_ecoregions.json`
  * published = `true`


    
    
    {
        "paths": [
            "/styles/mapbox/pays_ecoregions.json"
        ],
        "size": 10768,
        "mime_type": "application/json",
        "published": true,
        "_id": "{annexe}"
    }
    

Nous avons demandé à ce que cette annexe soit directement publiée. Nous pouvons donc maintenant y accéder publiquement. On va pouvoir définir une couche "Tuile vectorielle" dans QGis, en précisant la source des tuiles et l'URL du style :

  * URL = `https://data.geopf.fr/tms/1.0.0/pays_ecoregions/{z}/{x}/{y}.pbf`
  * URL du style = `https://data.geopf.fr/annexes/{technical_name}/styles/mapbox/pays_ecoregions.json`



En zoomant en dessous du niveau 5, on voit bien nos regions écologiques et les limites des payes, avec le style mis en ligne.
