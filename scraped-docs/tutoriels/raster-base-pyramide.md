source: https://geoplateforme.github.io/tutoriels/production/raster/base/calcul_pyramide/

[Donnée raster](../../../tags/#tag:donnée-raster) [Intégration](../../../tags/#tag:intégration)

# Calcul de la pyramide

## Calcul de la pyramide raster

Les données déposées sur la plateforme sont systématiquement transformées et stockées sur des espaces dédiés pour pouvoir être diffusées. Dans le cas des données raster, ce stockage est une pyramide d'images (la donnée est calculée dans plusieurs résolutions) sur du stockage S3. L'entité qui correspond à cette donnée pérenne est une donnée stockée.

Pour transformer la donnée livrée en donnée stockée, des traitements sont mis à disposition de l'entrepôt.
    
    
    flowchart LR
        ds[(Donnée stockée)]
    
        subgraph liv[Livraison raster]
            direction TB
            fic1[/Fichier raster 1/]
            fic2[/Fichier raster 2/]
            fic3[/Fichier raster 3/]
        end
    
        subgraph tra[Traitement de calcul de pyramide]
            exe[Exécution du traitement]
        end
    
        liv ==> exe ==> ds
    
        classDef indiv fill:#eee,stroke:#ff8000,stroke-width:3px;
        classDef global fill:#fff,stroke:#3465a4,stroke-width:3px;
    
        class liv,exe,ds indiv
        class tra global

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

Le détail sur un traitement permet de voir les types de données (livrées ou stockées) attendus en entrée, le type de donnée en sortie, les paramètres et les vérifications requises pour les livraisons en entrée.

/datastores/{datastore}/processings/2ae50661-986c-4f47-a3f0-e380417b522c

Corps de réponse JSON
    
    
    {
        "name": "Calcul de pyramide raster",
        "description": "Génération ou mise à jour d'une pyramide de tuiles raster à partir d'une livraison d'images géo-référencées",
        "input_types": {
            "upload": [
                "RASTER"
            ],
            "stored_data": [
                "ROK4-PYRAMID-RASTER"
            ]
        },
        "output_type": {
            "stored_data": "ROK4-PYRAMID-RASTER",
            "storage": [
                "S3"
            ]
        },
        "parameters": [
            {
                "name": "bottom",
                "description": "Niveau du bas de la pyramide. Attention à ne pas sur-échantillonner les données utilisées. En ne précisant pas de niveau, le traitement prendra le niveau de la grille dont lé résolution est la plus proche des images livrées",
                "mandatory": false
            },
            {
                "name": "tms",
                "description": "Tile Matrix Set, grille de définition des tuiles. Dans le cas d'une génération initiale, il est obligatoire",
                "mandatory": false,
                "constraints": {
                    "type": "string",
                    "enum": [
                        "PM"
                    ]
                }
            },
            {
                "name": "width",
                "description": "Nombre de tuiles dans une dalle, dans le sens de la largeur",
                "mandatory": false,
                "default_value": 16
            },
            {
                "name": "compression",
                "description": "Compression des données dans les tuiles",
                "mandatory": false,
                "constraints": {
                    "type": "string",
                    "enum": [
                        "jpg",
                        "png"
                    ]
                }
            },
            {
                "name": "interpolation",
                "description": "Interpolation",
                "mandatory": false,
                "constraints": {
                    "type": "string",
                    "enum": [
                        "nn",
                        "linear",
                        "bicubic"
                    ]
                }
            },
            {
                "name": "parallelization",
                "description": "Nombre de scripts d'écriture des dalles en parallèle",
                "mandatory": false,
                "default_value": 1
            },
            {
                "name": "top",
                "description": "Niveau du haut de la pyramide. Par défaut, on remonte jusqu'au niveau le plus haut de la grille",
                "mandatory": false
            },
            {
                "name": "mask",
                "description": "Écriture des masques de données dans la pyramide en sortie",
                "mandatory": false,
                "default_value": "false"
            },
            {
                "name": "height",
                "description": "Nombre de tuiles dans une dalle, dans le sens de la haureur",
                "mandatory": false,
                "default_value": 16
            }
        ]
        "_id": "2ae50661-986c-4f47-a3f0-e380417b522c",
        "required_checks": [
            {
                "name": "Vérification raster",
                "description": "La vérification raster contrôle que les fichiers sont bien lisibles et en extraie le géoréférencement",
                "_id": "66ed8a1b-93d9-4fe9-a413-ab93d31b2964"
            },
            {
                "name": "Vérification standard",
                "description": "La vérification standard contrôle les signatures MD5 fournies",
                "_id": "ecb00ba0-eb42-427e-8418-f5d8a30e84ec"
            }
        ]
    }
    

### Configuration d'une exécution de ce traitement

On distingue le traitement, ressource de la plateforme mise à disposition de l'entrepôt, et son exécution. Une exécution appartient à un entrepôt et a en entrée et en sortie des données spécifiques.

/datastores/{datastore}/processings/executions

Corps de requête JSONCorps de réponse JSON
    
    
    {
        "processing": "2ae50661-986c-4f47-a3f0-e380417b522c",
        "inputs": {
            "upload": [
            "{upload}"
            ]
        },
        "output": {
            "stored_data": {
                "name": "SCAN1000 de la Corse",
                "storage_tags": ["PYRAMIDE"]
            }
        },
        "parameters": {
            "tms": "PM",
            "compression": "jpg",
            "interpolation": "bicubic"
        }
    }
    
    
    
    {
        "processing": {
            "name": "Calcul de pyramide raster",
            "_id": "2ae50661-986c-4f47-a3f0-e380417b522c"
        },
        "status": "CREATED",
        "creation": "2023-05-22T09:15:50.353341276Z",
        "inputs": {
            "upload": [
                {
                    "type": "RASTER",
                    "name": "SCAN1000 - Corse",
                    "status": "CLOSED",
                    "srs": "EPSG:2154",
                    "_id": "{upload}"
                }
            ],
            "stored_data": []
        },
        "output": {
            "stored_data": {
                "name": "SCAN1000 de la Corse",
                "type": "ROK4-PYRAMID-RASTER",
                "status": "CREATED",
                "_id": "{stored data}"
            }
        },
        "parameters": {
            "tms": "PM",
            "compression": "jpg",
            "interpolation": "bicubic",
            "parallelization": 1,
            "mask": "false",
            "width": 16,
            "height": 16
        },
        "_id": "{execution}"
    }
    

Points d'attentions

Si votre pyramide est destinée à être mise à jour (voir [l'alimentation raster par mise à jour](../../mise-a-jour/)), il peut être important de préciser que l'on souhaite calculer les masques de données (paramètre `"mask": true`).

### Déclenchement de cette exécution

/datastores/{datastore}/processings/executions/{execution}/launch

### Consultation de l'état de l'exécution

Une exécution va avoir les statuts dans l'ordre suivant :

  * CREATED : créée mais non lancée
  * WAITING : lancée mais pas encore pris en charge par le cluster de calcul
  * PROGRESS : en cours d'exécution sur le cluster de calcul
  * SUCCESS ou FAILURE : terminé

/datastores/{datastore}/processings/executions/{execution}

Corps de réponse JSON
    
    
    {
        "processing": {
            "name": "Calcul de pyramide raster",
            "_id": "2ae50661-986c-4f47-a3f0-e380417b522c"
        },
        "status": "PROGRESS",
        "creation": "2023-05-22T09:15:50.353341276Z",
        "launch": "2023-05-22T11:30:32.650969Z",
        "inputs": {
            "upload": [
                {
                    "type": "RASTER",
                    "name": "SCAN1000 - Corse",
                    "status": "CLOSED",
                    "srs": "EPSG:2154",
                    "_id": "{upload}"
                }
            ],
            "stored_data": []
        },
        "output": {
            "stored_data": {
                "name": "SCAN1000 de la Corse",
                "type": "ROK4-PYRAMID-RASTER",
                "status": "CREATED",
                "_id": "{stored data}"
            }
        },
        "parameters": {
            "tms": "PM",
            "compression": "jpg",
            "interpolation": "bicubic",
            "parallelization": 1,
            "mask": "false",
            "width": 16,
            "height": 16
        },
        "_id": "{execution}"
    }
    

## Consultation de la donnée stockée en sortie

À la fin du traitement, des informations concernant la donnée finale sont remontées afin d'apparaître au niveau de l'API (taille, étendue, système de coordonnées et niveaux).

/datastores/{datastore}/stored_data/{stored data}

Corps de réponse JSON
    
    
    {
        "name": "SCAN1000 de la Corse",
        "type": "ROK4-PYRAMID-RASTER",
        "srs": "EPSG:3857",
        "contact": "contact@ign.fr",
        "extent": {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        43.0475237,
                        8.35476935
                    ],
                    [
                        43.0475237,
                        9.75281343
                    ],
                    [
                        41.23486116,
                        9.75281343
                    ],
                    [
                        41.23486116,
                        8.35476935
                    ],
                    [
                        43.0475237,
                        8.35476935
                    ]
                ]
            ]
        },
        "last_event": {
            "title": "Génération",
            "date": "2023-05-22T11:30:32.630725",
            "initiator": {
                "_id": "{user}"
            }
        },
        "tags": {},
        "storage": {
            "type": "S3",
            "labels": []
        },
        "size": 5104340,
        "status": "GENERATED",
        "_id": "{stored data}"
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
                "9",
                "10"
            ],
            "channels_format": "UINT8",
            "channels_number": 3,
            "compression": "JPG",
            "nodata_value": "255,255,255"
        }
    }
    

## Nettoyage de la livraison

Maintenant que la donnée a été stockée de manière pérenne, on peut supprimer la livraison et son contenu :

/datastores/{datastore}/uploads/{upload}
