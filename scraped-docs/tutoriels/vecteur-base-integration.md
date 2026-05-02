source: https://geoplateforme.github.io/tutoriels/production/vecteur/base/integration/

[Donnée vecteur](../../../tags/#tag:donnée-vecteur) [Intégration](../../../tags/#tag:intégration)

# Intégration des données

## Intégration en base

Les données déposées sur la plateforme sont systématiquement transformées et stockées sur des espaces dédiés pour pouvoir être diffusées. Dans le cas des données vecteur, ce stockage est un schéma sur des serveurs PostgreSQL. L'entité qui correspond à cette donnée pérenne est une donnée stockée.

Pour transformer la donnée livrée en donnée stockée, des traitements sont mis à disposition de l'entrepôt.
    
    
    flowchart LR
        ds[(Donnée stockée)]
    
        subgraph liv[Livraison vecteur]
            direction TB
            fic1[/Fichier vecteur 1/]
            fic2[/Fichier vecteur 2/]
            fic3[/Fichier vecteur 3/]
        end
    
        subgraph tra[Traitement d'intégration]
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

/datastores/{datastore}/processings/0de8c60b-9938-4be9-aa36-9026b77c3c96

Corps de réponse JSON
    
    
    {
        "name": "Intégration de données vecteur livrées en base",
        "description": "Ce traitement permet de stocker dans les bases de données PostgreSQL de la plateforme des données vecteurs livrées. Les formats pris en charge sont le CSV, le Shapefile, le Geopackage et le GeoJSON. Il est également possible de préciser un autre système afin de réaliser une reprojection à l'intégration",
        "input_types": {
            "upload": [
                "VECTOR"
            ],
            "stored_data": []
        },
        "output_type": {
            "stored_data": "VECTOR-DB",
            "storage": [
                "POSTGRESQL"
            ]
        },
        "parameters": [
            {
                "name": "srs",
                "description": "Système de coordonnées cible",
                "mandatory": false
            }
        ],
        "_id": "0de8c60b-9938-4be9-aa36-9026b77c3c96",
        "required_checks": [
            {
                "name": "Vérification vecteur",
                "description": "La vérification vecteur contrôle que les fichiers sont bien lisibles et en extraie l'étendue",
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
        "processing": "0de8c60b-9938-4be9-aa36-9026b77c3c96",
        "inputs": {
            "upload": [
                "{upload}"
            ]
        },
        "output": {
            "stored_data": {
                "name": "Pays et éco-régions",
                "storage_tags": ["VECTEUR"]
            }
        },
        "parameters": {
            "srs": "EPSG:3857"
        }
    }
    
    
    
    {
        "processing": {
            "name": "Intégration de données vecteur livrées en base",
            "_id": "0de8c60b-9938-4be9-aa36-9026b77c3c96"
        },
        "status": "CREATED",
        "creation": "2023-05-10T14:57:08.832176082Z",
        "inputs": {
            "upload": [
                {
                    "type": "VECTOR",
                    "name": "Données mondiales",
                    "status": "CLOSED",
                    "srs": "EPSG:4326",
                    "_id": "{upload}"
                }
            ],
            "stored_data": []
        },
        "output": {
            "stored_data": {
                "name": "Pays et éco-régions",
                "type": "VECTOR-DB",
                "status": "CREATED",
                "_id": "{stored data}"
            }
        },
        "parameters": [
            {
                "name": "srs",
                "value": "EPSG:3857"
            }
        ],
        "_id": "{execution}"
    }
    

Attention

Pour intégrer des couches avec des multi-géométries (ex: multipolygon), il faut lister ces couches dans l'exécution avec le paramètre `"multigeom_layers": ["couche_1","couche_2"]`.

### Déclenchement de cette exécution

/datastores/{datastore}/processings/executions/{execution}/launch

Attention

Les noms des tables et des champs sont "standardisés" lors de l'intégration en base pour éviter tout souci d'utilisation par les applications : pas de majuscules, pas d'accent, pas de tirets.

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
            "name": "Intégration de données vecteur livrées en base",
            "_id": "0de8c60b-9938-4be9-aa36-9026b77c3c96"
        },
        "status": "PROGRESS",
        "creation": "2023-05-10T14:57:08.832176Z",
        "launch": "2023-05-10T14:59:23.787740Z",
        "inputs": {
            "upload": [
                {
                    "type": "VECTOR",
                    "name": "Données mondiales",
                    "status": "CLOSED",
                    "srs": "EPSG:4326",
                    "_id": "{upload}"
                }
            ],
            "stored_data": []
        },
        "output": {
            "stored_data": {
                "name": "Pays et éco-régions",
                "type": "VECTOR-DB",
                "status": "GENERATING",
                "_id": "{stored data}"
            }
        },
        "parameters": [
            {
                "name": "srs",
                "value": "EPSG:3857"
            }
        ],
        "_id": "{execution}"
    }
    

## Consultation de la donnée stockée en sortie

À la fin du traitement, des informations concernant la donnée finale sont remontées afin d'apparaître au niveau de l'API (taille, étendue, système de coordonnées, tables et attributs).

/datastores/{datastore}/stored_data/{stored data}

Corps de réponse JSON
    
    
    {
        "name": "Pays et éco-régions",
        "type": "VECTOR-DB",
        "srs": "EPSG:3857",
        "contact": "email",
        "extent": {
            "type": "Polygon",
            "coordinates": [
    
            ]
        },
        "last_event": {
            "title": "Génération",
            "date": "2023-05-10T17:23:26.795112",
            "initiator": {
                "last_name": "Lopper",
                "first_name": "Dave",
                "_id": "{user}"
            }
        },
        "tags": {},
        "storage": {
            "type": "POSTGRESQL",
            "labels": []
        },
        "size": 5906432,
        "status": "GENERATED",
        "_id": "{stored data}",
        "type_infos": {
            "relations": [
                {
                    "name": "ecoregions",
                    "type": "TABLE",
                    "attributes": [
                        "ogc_fid",
                        "id",
                        "eco_name",
                        "biome_name",
                        "realm",
                        "nnh",
                        "nnh_name",
                        "color",
                        "color_bio",
                        "color_nnh",
                        "geom"
                    ],
                    "primary_key": [
                        "ogc_fid"
                    ]
                },
                {
                    "name": "pays",
                    "type": "TABLE",
                    "attributes": [
                        "ogc_fid",
                        "id",
                        "fips",
                        "iso2",
                        "iso3",
                        "un",
                        "name",
                        "area",
                        "pop2005",
                        "region",
                        "subregion",
                        "lon",
                        "lat",
                        "geom"
                    ],
                    "primary_key": [
                        "ogc_fid"
                    ]
                }
            ]
        }
    }
    

## Nettoyage de la livraison

Maintenant que la donnée a été stockée de manière pérenne, on peut supprimer la livraison et son contenu :

/datastores/{datastore}/uploads/{upload}
