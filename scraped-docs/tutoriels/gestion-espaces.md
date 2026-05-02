source: https://geoplateforme.github.io/tutoriels/production/gestion/administrateur/espaces/

[Administration](../../../tags/#tag:administration) [Gestion](../../../tags/#tag:gestion)

# Créer et gérer un espace de travail

Le but de ce tutoriel est de permettre à des utilisateurs **ayant le rôle ADMINISTRATOR** de créer et modifier des espaces de travail pour permettre à des producteurs de données d'utiliser l'Entrepôt Géoplateforme.

## Lister les entités globales

Définir un espace de travail implique de connaître les ressources partagées pour les affecter avec quota. Il y 4 types de ressources partagées :

  * Les espaces de stockages : **GET** `/administrator/storages`
  * Les points d'accès pour la diffusion des données : **GET** `/administrator/endpoints`
  * Les vérifications pour les livraisons : **GET** `/administrator/checks`
  * Les traitements : **GET** `/administrator/processings`



## Créer la communauté

La communauté permet de définir les utilisateurs qui y ont accès et leurs droits. Le nom technique doit être URL-compliant et être unique. Il se retrouvera entre autres dans les URL publiques de téléchargement des annexes.

/administrator/communities

Corps de requête JSONCorps de réponse JSON
    
    
    {
        "name": "Communauté des tutoriels",
        "technical_name": "tutoriels",
        "contact": "email",
        "public": true,
        "supervisor": "{user}"
    }
    
    
    
    {
        "name": "Communauté des tutoriels",
        "technical_name": "tutoriels",
        "contact": "contact@ign.fr",
        "supervisor": {
            "email": "dave.lopper@ign.fr",
            "_id": "{user}",
            "last_name": "Lopper",
            "first_name": "Dave"
        },
        "public": true,
        "_id": "{community}"
    }
    

Le superviseur est un utilisateur qui a forcément tous les droits sur la communauté et ne peut pas être enlevé. Cela assure la présence d'au moins une personne qui pourra en faire entrer d'autres.

## Créer l'entrepôt

Comme nous souhaitons mettre en place un espace de travail pour de producteur de données, nous allons associer à cette communauté d'utilisateurs un entrepôt. Une communauté sans entrepôt sera utile pour regrouper des consommateurs des flux et centraliser les permissions sur les offres de données (flux de diffusion).

C'est au niveau de l'entrepôt que l'on va affecter tout ou partie des ressources partagées, potentiellement avec quota. On crée dans l'exemple un entrepôt pour la gestion de base de la donnée vecteur (sans tuiles vectorielles). On liste après l'exemple les ressources à attribuer pour chaque usage et par type.

/administrator/datastores

Corps de requête JSONCorps de réponse JSON
    
    
    {
        "processings": [
            "0de8c60b-9938-4be9-aa36-9026b77c3c96"
        ],
        "storages": {
            "data": [
                {
                    "quota": 10000000000,
                    "storage": "e53852da-e713-4115-8af4-36ce0490f93b"
                }
            ],
            "uploads": {
                "quota": 10000000000,
                "storage": "40d3ae5e-f46b-4cb7-b08b-9a2f207f4dc6"
            },
            "annexes": {
                "quota": 10000000000,
                "storage": "1b0371a1-aad9-4f0f-b687-367d485a665b"
            }
        },
        "endpoints": [
            {
                "quota": 10,
                "endpoint": "ae022611-13eb-4a18-8d04-9b7604a031cc"
            },
            {
                "quota": 10,
                "endpoint": "ae012611-13eb-4a18-8d04-9b7604a031cc"
            }
        ],
        "community": "{community}",
        "check": [
            "ecb00ba0-eb42-427e-8418-f5d8a30e84ec",
            "66ed8a1b-93d9-4fe9-a413-ab93d31b2964"
        ]
    }
    
    
    
    {
        "community": {
            "contact": "contact@ign.fr",
            "public": true,
            "_id": "{community}"
        },
        "processings": [
            "0de8c60b-9938-4be9-aa36-9026b77c3c96"
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
            }
        ],
        "storages": {
            "data": [
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
        "active": false,
        "_id": "{datastore}",
        "checks": [
            "ecb00ba0-eb42-427e-8418-f5d8a30e84ec",
            "66ed8a1b-93d9-4fe9-a413-ab93d31b2964"
        ]
    }
    

Les quotas de stockage sont à définir en octets. Ceux sur les points d'accès sont en nombre d'offres.

Ressources par usage

Usage communUsage vecteurUsage vecteur avancéUsage rasterUsage archive

  * Stockage :
    * Stockage OpenIO pour les annexes : `40d3ae5e-f46b-4cb7-b08b-9a2f207f4dc6` (S3)
    * Stockage OpenIO pour les livraisons : `1b0371a1-aad9-4f0f-b687-367d485a665b` (S3)
  * Vérification :
    * Vérification standard : `ecb00ba0-eb42-427e-8418-f5d8a30e84ec`
  * Point d'accès :
    * Catalogue des métadonnées : `ae062611-13eb-4a18-8d04-9b7604a031cc` (CSW)



  * Stockage :
    * Stockage en base pour les données vecteur des partenaires : `e53852da-e713-4115-8af4-36ce0490f93b` (POSTGRESQL)
  * Vérification :
    * Vérification vecteur : `66ed8a1b-93d9-4fe9-a413-ab93d31b2964`
  * Traitement :
    * Intégration en base : `0de8c60b-9938-4be9-aa36-9026b77c3c96`
  * Point d'accès :
    * Service de diffusion WMS Vecteur principal : `ae022611-13eb-4a18-8d04-9b7604a031cc` (WMS-VECTOR)
    * Service de diffusion WFS principal : `ae012611-13eb-4a18-8d04-9b7604a031cc` (WFS)



  * Traitement :
    * Calcul de pyramide vecteur : `aa5f9391-0bdb-4b97-9209-fcde351b82f6`
  * Point d'accès :
    * Service de diffusion WMTS/TMS principal : `ae032611-13eb-4a18-8d04-9b7604a031cc` (WMTS-TMS)



  * Stockage :
    * Stockage OpenIO performant pour les données pyramides des partenaires : `7a7ccc8b-e0d1-47ed-848d-5a5cdb529539` (S3)
  * Vérification :
    * Vérification raster : `a4060831-9c6f-42e2-9435-e07a4e8ef535`
  * Traitements :
    * Calcul de pyramide raster : `2ae50661-986c-4f47-a3f0-e380417b522c`
    * Calcul ou mise à jour de pyramide raster par moissonnage WMS : `6a54dc92-fc93-4c8e-9f02-046bf889550e`
    * Fusion de pyramides raster : `7cdca031-9e86-4804-8764-9b1d783b087d`
  * Points d'accès :
    * Service de diffusion WMS Raster principal : `ae042611-13eb-4a18-8d04-9b7604a031cc` (WMS-RASTER)
    * Service de diffusion WMTS/TMS principal : `ae032611-13eb-4a18-8d04-9b7604a031cc` (WMTS-TMS)



  * Stockage :
    * Stockage OpenIO performant pour les données archives des partenaires : `4c2d24e6-870d-4194-8bc8-3ac8b7f76d08` (S3)
  * Vérification :
    * Vérification archive : `f4f79b5e-7056-4b56-981d-34043b4925ab`
  * Traitement :
    * Recopie d'une archive livrée : `12cdc646-3976-4f18-b273-f34fca37e2a6`
  * Point d'accès :
    * Service de Téléchargement principal : `ae052611-13eb-4a18-8d04-9b7604a031cc` (DOWNLOAD)



Toutes les ressources par type

VérificationsTraitementsStockagesPoints d'accès

  * Vérification standard : `ecb00ba0-eb42-427e-8418-f5d8a30e84ec`
  * Vérification raster : `a4060831-9c6f-42e2-9435-e07a4e8ef535`
  * Vérification vecteur : `66ed8a1b-93d9-4fe9-a413-ab93d31b2964`
  * Vérification archive : `f4f79b5e-7056-4b56-981d-34043b4925ab`
  * Vérification pyramide ROK4 : `f879e8c6-0838-48a6-a8d3-41d47b208a6c`



  * Intégration de données vecteur livrées en base : `0de8c60b-9938-4be9-aa36-9026b77c3c96`
  * Recopie d'une archive livrée : `12cdc646-3976-4f18-b273-f34fca37e2a6`
  * Calcul de pyramide raster : `2ae50661-986c-4f47-a3f0-e380417b522c`
  * Calcul ou mise à jour de pyramide raster par moissonnage WMS : `6a54dc92-fc93-4c8e-9f02-046bf889550e`
  * Fusion de pyramides raster : `7cdca031-9e86-4804-8764-9b1d783b087d`
  * Calcul de pyramide vecteur : `aa5f9391-0bdb-4b97-9209-fcde351b82f6`



  * S3 :
    * Stockage OpenIO pour les livraisons : `40d3ae5e-f46b-4cb7-b08b-9a2f207f4dc6`
    * Stockage OpenIO pour les annexes : `1b0371a1-aad9-4f0f-b687-367d485a665b`
    * Stockage OpenIO performant pour les données pyramides : `7a7ccc8b-e0d1-47ed-848d-5a5cdb529539`
    * Stockage OpenIO performant pour les données archives : `4c2d24e6-870d-4194-8bc8-3ac8b7f76d08`
  * POSTGRESQL

    * Stockage PostgreSQL standard : `e53852da-e713-4115-8af4-36ce0490f93b`
  * OPENSEARCH

    * Stockage OpenSearch standard : `d5134033-c9c1-4342-a348-fbc4182f34bc`



  *     * Service de diffusion WFS principal : `ae012611-13eb-4a18-8d04-9b7604a031cc` (WFS)
    * Service de diffusion WMTS/TMS principal : `ae032611-13eb-4a18-8d04-9b7604a031cc` (WMTS-TMS)
    * Service de diffusion WMS Raster principal : `ae042611-13eb-4a18-8d04-9b7604a031cc` (WMS-RASTER)
    * Service de diffusion WMS Vecteur principal : `ae022611-13eb-4a18-8d04-9b7604a031cc` (WMS-VECTOR)
    * Service de Téléchargement principal : `ae052611-13eb-4a18-8d04-9b7604a031cc` (DOWNLOAD)
    * Service de diffusion CSW : `ae062611-13eb-4a18-8d04-9b7604a031cc` (METADATA)

Services "open"

    * Service d'altimétrie : `0ac92a1e-aa86-4843-8528-e303f12296e5` (ALTI)

    * Service de recherche : `043dd5e1-4136-49d3-b7a6-26de70d4a195` (SEARCH)

  * Services "restreint"

    * Service de téléchargement privé : `b5bf7ab2-8998-4829-8c80-cd2ec02e6e58` (DOWNLOAD)
    * Service de diffusion WFS privé : `d02feec9-1169-403f-bfc3-7ba6d6015ed4` (WFS)
    * Service de diffusion WMS Vecteur privé : `519c8bb1-9b7f-414a-9850-1a73dfd467ed` (WMS-VECTOR)
    * Service de diffusion WMS Raster privé : `66866100-48eb-4340-bbc9-f5c7d9707928` (WMS-RASTER)
    * Service de diffusion WMTS/TMS privé : `7e0a92d1-8213-4ce0-8903-eb4c305a1849` (WMTS-TMS)

    * Service de recherche : `5c8f3cd0-405f-4c3e-8240-959683fc2a93` (SEARCH)




## Activer l'entrepôt

À ce stade, l'entrepôt n'est pas utilisable car non activé. Pour l'activer, il suffit de modifier son champ `active`:

/administrator/datastores/{datastore}

Corps de requête JSON
    
    
    {
        "active": true
    }
    

Par la suite, il sera possible de désactiver un entrepôt pour bloquer instantanément tous les nouveaux appels sur celui ci. Rien n'est supprimé, mais cela permet de mettre en sécurité un entrepôt pour lequel une utilisation frauduleuse ou dangereurse est détectée.

## Modifier un espace de travail

Il est possible de changer le superviseur d'une communauté après coup :

/administrator/communities/{community}

Corps de requête JSON
    
    
    {
        "supervisor": "id nouveau superviseur"
    }
    

On peut également modifier les quotas après coup, ou donner accès à de nouveaux traitements. Il n'est pas nécessaire de tout fournie, mais seulement les parties à changer. Un exemple ici pour augmenter le quota de l'espace de livraison à 100 Go :

/administrator/datastores/{datastore}

Corps de requête JSON
    
    
    {
        "storages": {
                "uploads": {
                "quota": 100000000000,
                "storage": "40d3ae5e-f46b-4cb7-b08b-9a2f207f4dc6"
            }
        }
    }
    
