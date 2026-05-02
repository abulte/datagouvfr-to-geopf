source: https://geoplateforme.github.io/tutoriels/production/raster/base/livraison/

[Alimentation](../../../tags/#tag:alimentation) [Donnée raster](../../../tags/#tag:donnée-raster)

# Téléversement des données

## Livraison des données

La livraison est une entité qui permet de déposer un ensemble de fichiers de données au sein de l'entrepôt. Une livraison et son contenu sera toujours utilisée comme un tout.

La livraison n'a qu'un rôle temporaire, le temps que les données soient transformées et stockées dans leur format pérenne sur la plateforme. Les fichiers déposés ne sont pas ceux utilisés par les services de diffusion.

### Déclarer la livraison

/datastores/{datastore}/uploads

Corps de requête JSONCorps de réponse JSON
    
    
    {
    "description": "Données SCAN1000 sur la Corse",
    "name": "SCAN1000 - Corse",
    "type": "RASTER",
    "srs": "EPSG:2154"
    }
    
    
    
    {
        "name": "SCAN1000 - Corse",
        "description": "Données SCAN1000 sur la Corse",
        "type": "RASTER",
        "status": "OPEN",
        "srs": "EPSG:2154",
        "contact": "contact@ign.fr",
        "size": 0,
        "last_event": {
            "title": "Création",
            "date": "2023-05-22T08:07:13.812601878",
            "initiator": {
                "_id": "{user}"
            }
        },
        "_id": "{upload}",
        "type_infos": {}
    }
    

### Téléverser un fichier

Les formats de fichier raster gérés sont :

  * GeoTIFF
  * TIFF + TFW
  * JPEG2000



`<scan1000_corse.tif>`

/datastores/{datastore}/uploads/{upload}/data?path=data/scan1000_corse.tif

Corps de requête Multipart

  * file = `<scan1000_corse.tif>`



`<scan1000_corse.tfw>`

/datastores/{datastore}/uploads/{upload}/data?path=data/scan1000_corse.tfw

Corps de requête Multipart

  * file = `<scan1000_corse.tfw>`



### Contrôler le contenu

Afin de vérifier que tous les fichiers ont bien été déposés, et l'éventuelle arborescence :

/datastores/{datastore}/uploads/{upload}/tree

Corps de réponse JSON
    
    
    [
        {
            "type": "DIRECTORY",
            "name": "data",
            "size": 6308587,
            "children": [
                {
                    "type": "FILE",
                    "name": "scan1000_corse.tfw",
                    "size": 47
                },
                {
                    "type": "FILE",
                    "name": "scan1000_corse.tif",
                    "size": 6308540
                }
            ]
        }
    ]
    

## Terminer la livraison

Terminer la livraison va consister à retirer les droits en écriture sur les données déposées afin que l'on puisse le traiter sans conflit. Des vérifications vont s'exécuter, lire les données livrées et détecter d'éventuels problème qui aurait mis en échec les traitements à suivre.

### Fermeture

/datastores/{datastore}/uploads/{upload}/close

### Consultation des vérifications sur ma livraison

Plusieurs vérifications peuvent tourner sur une mếme livraison, celles ci ne faisant que lire les données déposées.

/datastores/{datastore}/uploads/{upload}/checks

Corps de réponse JSON
    
    
    {
        "asked": [
            {
                "check": {
                    "name": "Vérification raster",
                    "_id": "a4060831-9c6f-42e2-9435-e07a4e8ef535"
                },
                "_id": "{execution}"
            },
            {
                "check": {
                    "name": "Vérification standard",
                    "_id": "ecb00ba0-eb42-427e-8418-f5d8a30e84ec"
                },
                "_id": "{execution}"
            }
        ],
        "in_progress": [],
        "passed": [],
        "failed": []
    }
    

Lorsque toutes les vérifications seront passées, la livraison passera en statut `CLOSED` et la réponse à l'appel précédent sera :

/datastores/{datastore}/uploads/{upload}/checks

Corps de réponse JSON
    
    
    {
        "asked": [],
        "in_progress": [],
        "passed": [
            {
                "check": {
                    "name": "Vérification raster",
                    "_id": "a4060831-9c6f-42e2-9435-e07a4e8ef535"
                },
                "_id": "{execution}"
            },
            {
                "check": {
                    "name": "Vérification standard",
                    "_id": "ecb00ba0-eb42-427e-8418-f5d8a30e84ec"
                },
                "_id": "{execution}"
            }
        ],
        "failed": []
    }
    
