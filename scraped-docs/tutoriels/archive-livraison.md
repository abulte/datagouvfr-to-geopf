source: https://geoplateforme.github.io/tutoriels/production/archive/base/livraison/

[Alimentation](../../../tags/#tag:alimentation) [Donnée archive](../../../tags/#tag:donnée-archive)

# Téléversement des données

## Livraison des données

La livraison est une entité qui permet de déposer un ensemble de fichiers de données au sein de l'entrepôt. Une livraison et son contenu seront toujours utilisés comme un tout.

La livraison n'a qu'un rôle temporaire, le temps que les données soient transformées et stockées dans leur format pérenne sur la plateforme. Les fichiers déposés ne sont pas ceux utilisés par les services de diffusion.

### Déclarer la livraison

Le système de coordonnées ne sera jamais utilisée dans des calculs. Il sera simplement une information 

/datastores/{datastore}/uploads

Corps de requête JSONCorps de réponse JSON
    
    
    {
        "description": "Départements et limites départementales",
        "name": "Données départementales",
        "type": "ARCHIVE",
        "srs": "EPSG:2154"
    }
    
    
    
    {
        "name": "Données départementales",
        "description": "Départements et limites départementales",
        "type": "ARCHIVE",
        "status": "OPEN",
        "srs": "EPSG:2154",
        "contact": "contact@ign.fr",
        "size": 0,
        "last_event": {
            "title": "Création",
            "date": "2023-07-03T14:01:15.108781764",
            "initiator": {
                "last_name": "Lopper",
                "first_name": "Dave",
                "_id": "{user}"
            }
        },
        "_id": "{upload}",
        "type_infos": {}
    }
    

### Téléverser un fichier

Il n'y a aucune limitation aux formats de fichiers qui seront pris en charge. La seule contrainte est sur le nommage : on ne peut pas avoir deux fichiers qui ont le même nom à des endroits différents de l'oarborescence de la livraison. La vérification sortirait en erreur. Les fichiers étant stockés de manière pérenne à plat, on ne veut pas de conflit sur le nommage.

`<DEPARTEMENT.cpg>`

/datastores/{datastore}/uploads/{upload}/data?path=data/DEPARTEMENT.cpg

Corps de requête Multipart

  * file = `<DEPARTEMENT.cpg>`



`<DEPARTEMENT.dbf>`

/datastores/{datastore}/uploads/{upload}/data?path=data/DEPARTEMENT.dbf

Corps de requête Multipart

  * file = `<DEPARTEMENT.dbf>`



`<DEPARTEMENT.prj>`

/datastores/{datastore}/uploads/{upload}/data?path=data/DEPARTEMENT.prj

Corps de requête Multipart

  * file = `<DEPARTEMENT.prj>`



`<DEPARTEMENT.shp>`

/datastores/{datastore}/uploads/{upload}/data?path=data/DEPARTEMENT.shp

Corps de requête Multipart

  * file = `<DEPARTEMENT.shp>`



`<DEPARTEMENT.shx>`

/datastores/{datastore}/uploads/{upload}/data?path=data/DEPARTEMENT.shx

Corps de requête Multipart

  * file = `<DEPARTEMENT.shx>`



`<LIMITE_DEPARTEMENT.cpg>`

/datastores/{datastore}/uploads/{upload}/data?path=data/LIMITE_DEPARTEMENT.cpg

Corps de requête Multipart

  * file = `<LIMITE_DEPARTEMENT.cpg>`



`<LIMITE_DEPARTEMENT.dbf>`

/datastores/{datastore}/uploads/{upload}/data?path=data/LIMITE_DEPARTEMENT.dbf

Corps de requête Multipart

  * file = `<LIMITE_DEPARTEMENT.dbf>`



`<LIMITE_DEPARTEMENT.prj>`

/datastores/{datastore}/uploads/{upload}/data?path=data/LIMITE_DEPARTEMENT.prj

Corps de requête Multipart

  * file = `<LIMITE_DEPARTEMENT.prj>`



`<LIMITE_DEPARTEMENT.shp>`

/datastores/{datastore}/uploads/{upload}/data?path=data/LIMITE_DEPARTEMENT.shp

Corps de requête Multipart

  * file = `<LIMITE_DEPARTEMENT.shp>`



`<LIMITE_DEPARTEMENT.shx>`

/datastores/{datastore}/uploads/{upload}/data?path=data/LIMITE_DEPARTEMENT.shx

Corps de requête Multipart

  * file = `<LIMITE_DEPARTEMENT.shx>`



### Contrôler le contenu

Afin de vérifier que tous les fichiers ont bien été déposés et leur éventuelle arborescence :

/datastores/{datastore}/uploads/{upload}/tree

Corps de réponse JSON
    
    
    [
        {
            "type": "DIRECTORY",
            "name": "data",
            "size": 7783564,
            "children": [
                {
                    "type": "FILE",
                    "name": "DEPARTEMENT.cpg",
                    "size": 6
                },
                {
                    "type": "FILE",
                    "name": "DEPARTEMENT.dbf",
                    "size": 17186
                },
                {
                    "type": "FILE",
                    "name": "DEPARTEMENT.prj",
                    "size": 449
                },
                {
                    "type": "FILE",
                    "name": "DEPARTEMENT.shp",
                    "size": 3125208
                },
                {
                    "type": "FILE",
                    "name": "DEPARTEMENT.shx",
                    "size": 868
                },
                {
                    "type": "FILE",
                    "name": "LIMITE_DEPARTEMENT.cpg",
                    "size": 6
                },
                {
                    "type": "FILE",
                    "name": "LIMITE_DEPARTEMENT.dbf",
                    "size": 2039048
                },
                {
                    "type": "FILE",
                    "name": "LIMITE_DEPARTEMENT.prj",
                    "size": 449
                },
                {
                    "type": "FILE",
                    "name": "LIMITE_DEPARTEMENT.shp",
                    "size": 2527748
                },
                {
                    "type": "FILE",
                    "name": "LIMITE_DEPARTEMENT.shx",
                    "size": 72596
                }
            ]
        }
    ]
    

## Terminer la livraison

Terminer la livraison va consister à retirer les droits en écriture sur les données déposées afin qu'elles puissent être traitées sans conflit. Des vérifications vont s'exécuter, lire les données livrées et détecter d'éventuels problème qui auraient mis en échec les traitements à suivre.

### Fermeture

/datastores/{datastore}/uploads/{upload}/close

### Consultation des vérifications sur ma livraison

Plusieurs vérifications peuvent tourner sur une mếme livraison, celles ci ne faisant que lire les données déposées.

/datastores/{datastore}/uploads/{upload}/checks

Corps de réponse JSON
    
    
    {
        "asked": [],
        "in_progress": [
            {
                "check": {
                    "name": "Vérification standard",
                    "_id": "ecb00ba0-eb42-427e-8418-f5d8a30e84ec"
                },
                "_id": "{execution}"
            },
            {
                "check": {
                    "name": "Vérification archive",
                    "_id": "f4f79b5e-7056-4b56-981d-34043b4925ab"
                },
                "_id": "{execution}"
            }
        ],
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
                    "name": "Vérification standard",
                    "_id": "ecb00ba0-eb42-427e-8418-f5d8a30e84ec"
                },
                "_id": "{execution}"
            },
            {
                "check": {
                    "name": "Vérification archive",
                    "_id": "f4f79b5e-7056-4b56-981d-34043b4925ab"
                },
                "_id": "{execution}"
            }
        ],
        "failed": []
    }
    
