source: https://geoplateforme.github.io/tutoriels/production/controle-des-acces/entrepot/connexion_api/

[API Entrepôt](../../../tags/#tag:api-entrepôt) [Contrôle des accès](../../../tags/#tag:contrôle-des-accès)

# Connexion à l'API Entrepôt

Une fois le compte existant, on va pouvoir manipuler l'API Entrepôt.

## Qui suis-je ?

Un premier appel va permettre de récupérer nos informations personnelles et principalement les communautés dont nous sommes membres.

/users/me

Corps de réponse JSON
    
    
    {
        "email": "dave.lopper@ign.fr",
        "creation": "2023-02-01T09:45:10.725069Z",
        "last_call": "2023-03-24T17:02:32.676055Z",
        "communities_member": [
            {
                "rights": [
                    "ANNEX",
                    "UPLOAD",
                    "BROADCAST",
                    "PROCESSING",
                    "COMMUNITY"
                ],
                "community": {
                    "name": "Communauté des tutoriels",
                    "technical_name": "tutoriels",
                    "datastore": "{datastore}",
                    "supervisor": "{user}",
                    "public": true,
                    "_id": "{community}"
                }
            }
        ],
        "technical": false,
        "administrator": false,
        "_id": "{user}",
        "last_name": "Lopper",
        "first_name": "Dave"
    }
    

L'identifiant de votre utilisateur est une information :

  * à fournir à un gestionnaire de communauté si vous voulez la rejoindre
  * à l'adresse `geoplateforme@ign.fr` si vous souhaitez qu'un espace de travail soit créé pour vous (en tant que producteur ou gestionnaire de consommateur de données).



Lorsque la communauté est associée à un entrepôt, on a également dans cette réponse son identifiant. Cet identifiant d'entrepôt sera systèmatiquement présent dans les routes d'appels à l'API pour l'alimentation précisant au sein de quel entrepôt on souhaite travailler.

On voit également les droits que l'on a dans chaque communauté, limitant les actions autorisées.

La vidéo suivante montre comment avoir ces informations en utilisant l'[interface Swagger](https://data.geopf.fr/api/swagger-ui/index.html).

## Quelles possibilités a mon entrepôt ?

La plateforme dispose de ressources globales pour permettre l'alimentation et la diffusion de données :

  * Des vérifications
  * Des traitements
  * Des espaces de stockage
  * Des grappes de serveur de diffusion, les points d'accès 



Ces ressources sont individuellement mises à disposition des entrepôts, avec quotas.

Pour voir celles accessibles par mon entrepôt (la réponse dépend des ressources qui vous ont été allouées) :

/datastores/{datastore}

Corps de réponse JSON
    
    
    {
        "community": {
            "contact": "contact@ign.fr",
            "public": true,
            "_id": "{community}"
        },
        "processings": [
            "0de8c60b-9938-4be9-aa36-9026b77c3c96"
            "12cdc646-3976-4f18-b273-f34fca37e2a6",
            "aa5f9391-0bdb-4b97-9209-fcde351b82f6",
            "2ae50661-986c-4f47-a3f0-e380417b522c",
            "7cdca031-9e86-4804-8764-9b1d783b087d"
        ],
        "name": "Communauté des tutoriels",
        "technical_name": "tutoriels",
        "endpoints": [
            {
                "use": 0,
                "quota": 10,
                "endpoint": {
                    "name": "Service de diffusion WMS Vecteur principal",
                    "technical_name": "gpf-geoserver-wms-v",
                    "type": "WMS-VECTOR",
                    "urls": [
                        {
                            "type": "WMS",
                            "url": "https://data.geopf.fr/wms-v"
                        }
                    ],
                    "_id": "ae022611-13eb-4a18-8d04-9b7604a031cc",
                    "open": true,
                    "metadata_fi": "gpf-geoserver-wms-v"
                }
            },
            {
                "use": 0,
                "quota": 10,
                "endpoint": {
                    "name": "Service de diffusion WFS principal",
                    "technical_name": "gpf-geoserver-wfs",
                    "type": "WFS",
                    "urls": [
                        {
                            "type": "WFS",
                            "url": "https://data.geopf.fr/wfs"
                        }
                    ],
                    "_id": "ae012611-13eb-4a18-8d04-9b7604a031cc",
                    "open": true,
                    "metadata_fi": "gpf-geoserver-wfs"
                }
            },
            {
                "use": 0,
                "quota": 10,
                "endpoint": {
                    "name": "Service de diffusion WMS Raster principal",
                    "technical_name": "gpf-rok4-server-wms-r",
                    "type": "WMS-RASTER",
                    "urls": [
                        {
                            "type": "WMS",
                            "url": "https://data.geopf.fr/wms-r"
                        }
                    ],
                    "_id": "ae042611-13eb-4a18-8d04-9b7604a031cc",
                    "open": true,
                    "metadata_fi": "gpf-rok4-server-wms-r"
                }
            },{
                "use": 0,
                "quota": 10,
                "endpoint": {
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
                            "url": "https://data.geopf.fr/tms"
                        }
                    ],
                    "_id": "ae032611-13eb-4a18-8d04-9b7604a031cc",
                    "open": true,
                    "metadata_fi": "gpf-rok4-server-wmts-tms"
                }
            },{
                "use": 0,
                "quota": 10,
                "endpoint": {
                    "name": "Service de téléchargement principal",
                    "technical_name": "gpf-download",
                    "type": "DOWNLOAD",
                    "urls": [
                        {
                            "type": "DOWNLOAD",
                            "url": "https://data.geopf.fr/telechargement"
                        }
                    ],
                    "_id": "ae052611-13eb-4a18-8d04-9b7604a031cc",
                    "open": true,
                    "metadata_fi": "gpf-download"
                }
            },{
                "use": 0,
                "quota": 100,
                "endpoint": {
                    "name": "Service de diffusion de métadonnées principal",
                    "technical_name": "gpf-geonetwork",
                    "type": "CSW",
                    "urls": [
                        {
                            "type": "CSW",
                            "url": "https://data.geopf.fr/csw"
                        }
                    ],
                    "_id": "ae062611-13eb-4a18-8d04-9b7604a031cc",
                    "open": true,
                    "metadata_fi": "gpf-geonetwork"
                }
            }
        ],
        "storages": {
            "data": [
                {
                    "use": 0,
                    "quota": 10000000000,
                    "storage": {
                        "name": "Stockage OpenIO performant pour les données pyramides des partenaires",
                        "type": "S3",
                        "labels": [
                            "PARTENAIRE",
                            "PYRAMIDE",
                            "PERF"
                        ],
                        "_id": "7a7ccc8b-e0d1-47ed-848d-5a5cdb529539"
                    }
                },
                {
                    "use": 0,
                    "quota": 10000000000,
                    "storage": {
                        "name": "Stockage OpenIO performant pour les données archives des partenaires",
                        "type": "S3",
                        "labels": [
                            "PARTENAIRE",
                            "ARCHIVE",
                            "PERF"
                        ],
                        "_id": "4c2d24e6-870d-4194-8bc8-3ac8b7f76d08"
                    }
                },
                {
                    "use": 0,
                    "quota": 10000000000,
                    "storage": {
                        "name": "Stockage PostgreSQL standard Partenaires",
                        "type": "POSTGRESQL",
                        "labels": [
                            "PARTENAIRE",
                            "VECTEUR"
                        ],
                        "_id": "e53852da-e713-4115-8af4-36ce0490f93b"
                    }
                }
            ],
            "upload": {
                "use": 0,
                "quota": 10000000000,
                "storage": {
                    "name": "Stockage OpenIO pour les livraisons",
                    "type": "S3",
                    "labels": [
                        "LIVRAISON",
                        "PERF"
                    ],
                    "_id": "40d3ae5e-f46b-4cb7-b08b-9a2f207f4dc6"
                }
            },
            "annexe": {
                "use": 0,
                "quota": 10000000000,
                "storage": {
                    "name": "Stockage OpenIO pour les annexes",
                    "type": "S3",
                    "labels": [
                        "ANNEXE",
                        "PERF"
                    ],
                    "_id": "1b0371a1-aad9-4f0f-b687-367d485a665b"
                }
            }
        },
        "active": true,
        "_id": "{datastore}",
        "checks": [
            "ecb00ba0-eb42-427e-8418-f5d8a30e84ec",
            "66ed8a1b-93d9-4fe9-a413-ab93d31b2964",
            "a4060831-9c6f-42e2-9435-e07a4e8ef535",
            "f4f79b5e-7056-4b56-981d-34043b4925ab",
            "f879e8c6-0838-48a6-a8d3-41d47b208a6c"
        ]
    }
    
