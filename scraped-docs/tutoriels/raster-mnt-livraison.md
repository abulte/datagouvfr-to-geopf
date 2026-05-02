source: https://geoplateforme.github.io/tutoriels/production/raster/mnt/livraison/

[Alimentation](../../../tags/#tag:alimentation) [Donnée raster](../../../tags/#tag:donnée-raster) [MNT](../../../tags/#tag:mnt)

# Téléversement des données

## Livraison des données

La livraison est une entité qui permet de déposer un ensemble de fichiers de données au sein de l'entrepôt. Une livraison et son contenu sera toujours utilisée comme un tout.

La livraison n'a qu'un rôle temporaire, le temps que les données soient transformées et stockées dans leur format pérenne sur la plateforme. Les fichiers déposés ne sont pas ceux utilisés par les services de diffusion.

### Déclarer la livraison

/datastores/{datastore}/uploads

Corps de requête JSONCorps de réponse JSON
    
    
    {
        "description": "Dalle kilométrique de MNT 50 cm issue du LidarHD",
        "name": "Dalle MNT LidarHD",
        "type": "RASTER",
        "srs": "EPSG:2154"
    }
    
    
    
    {
        "name": "Dalle MNT LidarHD",
        "description": "Dalle kilométrique de MNT 50 cm issue du LidarHD",
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
        "_id": "{upload MNT}",
        "type_infos": {}
    }
    

### Téléverser un fichier

Les formats de fichier raster gérés pour du MNT sont :

  * GeoTIFF
  * TIFF + TFW



`<LHD_FXX_0932_6453_MNT_0M50_LAMB93_IGN69.tif>`

/datastores/{datastore}/uploads/{upload MNT}/data?path=data/LHD_FXX_0932_6453_MNT_0M50_LAMB93_IGN69.tif

Corps de requête Multipart

  * file = `<LHD_FXX_0932_6453_MNT_0M50_LAMB93_IGN69.tif>`



### Contrôler le contenu

Afin de vérifier que tous les fichiers ont bien été déposés, et l'éventuelle arborescence :

/datastores/{datastore}/uploads/{upload}/tree

Corps de réponse JSON
    
    
    [
        {
            "type": "DIRECTORY",
            "name": "data",
            "size": 16012500,
            "children": [
                {
                    "type": "FILE",
                    "name": "LHD_FXX_0932_6453_MNT_0M50_LAMB93_IGN69.tif",
                    "size": 16012500
                }
            ]
        }
    ]
    

## Terminer la livraison

Terminer la livraison va consister à retirer les droits en écriture sur les données déposées afin que l'on puisse le traiter sans conflit. Des vérifications vont s'exécuter, lire les données livrées et détecter d'éventuels problème qui aurait mis en échec les traitements à suivre.

### Fermeture

/datastores/{datastore}/uploads/{upload MNT}/close

### Consultation des vérifications sur ma livraison

Plusieurs vérifications peuvent tourner sur une mếme livraison, celles ci ne faisant que lire les données déposées.

/datastores/{datastore}/uploads/{upload MNT}/checks

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

/datastores/{datastore}/uploads/{upload MNT}/checks

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
    
