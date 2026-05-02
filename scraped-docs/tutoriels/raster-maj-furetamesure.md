source: https://geoplateforme.github.io/tutoriels/production/raster/mise-a-jour/furetamesure/

[Chaînage](../../../tags/#tag:chaînage) [Donnée raster](../../../tags/#tag:donnée-raster) [Intégration](../../../tags/#tag:intégration)

# Au fur et à mesure

Une mise à jour par chaînage va créer une nouvelle donnée stockée. Le nouveau contenu sera ajouté et les anciennes données seront référencées.

L'avantage est qu'il n'y a pas de modifications des anciennes données et que celles ci ne sont pas dupliquées. En revanche, une dépendance est ajoutée entre les données, ce qui va empêcher la suppression des données référencées (les anciennes données).
    
    
    ---
    title: Étapes du tutoriel
    ---
    stateDiagram
    
    
        LIV1: Calcul de la pyramide contenant le premier jeu
        note left of LIV1
            Livraison (upload)
            Vérification (check)
            Traitement (processing)
            Exécution de traitement (processing execution)
            Données stockée (stored data)
        end note
    
        PUB_TILED1: Publication en WMTS/TMS pour validation
        note right of PUB_TILED1
            Configuration (configuration)
            Point d'accès (endpoint)
            Offre (offering)
        end note
    
        LIV2: Calcul de la pyramide de mise à jour ajoutant le deuxième jeu
        note left of LIV2
            Livraison (upload)
            Vérification (check)
            Traitement (processing)
            Exécution de traitement (processing execution)
            Données stockée (stored data)
        end note
    
        PUB_TILED2: Republication en WMTS/TMS pour validation
        note right of PUB_TILED2
            Configuration (configuration)
            Point d'accès (endpoint)
            Offre (offering)
        end note
    
        [*] --> LIV1
        LIV1 --> PUB_TILED1
        PUB_TILED1 --> LIV2
        LIV2 --> PUB_TILED2
    
        classDef concepts fill:#eee,stroke:#8d1d75,stroke-width:3px;
    
        class LIV1,LIV2,PUB_TILED1,PUB_TILED2 concepts

## Gestion du premier jeu de données

### Calcul de la pyramide

On a notre permier jeu de donnée, la pyramide calculée se fera dans les même conditions que dans le [tutoriel de diffusion de données raster](../../base/).

  * Création de la livraison

/datastores/{datastore}/uploads

Corps de requête JSON
    
    
    {
        "description": "SCAN 1000 Nord Corse",
        "name": "SCAN 1000 Nord Corse",
        "type": "RASTER",
        "srs": "EPSG:2154"
    }
    

  * Livraison des fichiers : [scan1000_corse_nord.tif](../../../assets/data/scan1000_corse_nord.tif)
  * Fermeture de la livraison
  * Création de l'exécution de traitement

/datastores/{datastore}/processings/executions

Corps de requête JSON
    
    
    {
        "processing": "2ae50661-986c-4f47-a3f0-e380417b522c",
        "inputs": {
            "upload": [
                "{upload Corse Nord}"
            ]
        },
        "output": {
            "stored_data": {
                "name": "SCAN 1000 Nord Corse",
                "storage_tags": ["PYRAMIDE"]
            }
        },
        "parameters": {
            "tms": "PM",
            "compression": "jpg",
            "interpolation": "bicubic"
        }
    }
    

  * Lancement de l'exécution : ID de la données stockée `{stored data Corse Nord}`



### Diffusion

  * Création de la configuration WMTS-TMS : ID `{configuration}`

/datastores/{datastore}/configurations

Corps de requête JSON
    
    
    {
        "type": "WMTS-TMS",
        "name": "SCAN 1000 Nord Corse",
        "layer_name": "scan1000_corse",
        "metadata": [
            {
                "format": "application/xml",
                "url": "https://geoservices.ign.fr/sites/default/files/2021-07/IGNF_SCAN1000r_2-1.xml",
                "type": "ISO19115:2003"
            }
        ],
        "type_infos": {
            "title": "SCAN 1000 Nord Corse",
            "abstract": "Données SCAN 1000 sur le Nord de la Corse",
            "keywords": [
                "Tutoriel", "Raster", "Mise à jour"
            ],
            "used_data": [
                {
                    "bottom_level": "10",
                    "top_level": "0",
                    "stored_data": "{stored data Corse Nord}"
                }
            ]
        },
        "getfeatureinfo": {
            "stored_data": true
        }
    }
    

  * Création de l'offre : ID `{offering}`



On met tout de suite comme `layer_name` le nom cible : lorsque l'on mettra à jour la diffusion, on ne pourra plus le changer.

## Gestion du deuxième jeu de données

### Calcul de la pyramide

  * Création de la livraison

/datastores/{datastore}/uploads

Corps de requête JSON
    
    
    {
        "description": "SCAN 1000 Sud Corse",
        "name": "SCAN 1000 Sud Corse",
        "type": "RASTER",
        "srs": "EPSG:2154"
    }
    

  * Livraison des fichiers : [scan1000_corse_sud.tif](../../../assets/data/scan1000_corse_sud.tif)
  * Fermeture de la livraison
  * Création de l'exécution de traitement : on a ici deux données en entrée, la nouvelle zone livrée, ainsi que la pyramide ne contenant que le Nord de la Corse

/datastores/{datastore}/processings/executions

Corps de requête JSON
    
    
    {
        "processing": "2ae50661-986c-4f47-a3f0-e380417b522c",
        "inputs": {
            "upload": [
                "{upload Corse Sud}"
            ],
            "stored_data": [
                "{stored data Corse Nord}"
            ]
        },
        "output": {
            "stored_data": {
                "name": "SCAN 1000 Corse complète",
                "storage_tags": ["PYRAMIDE"]
            }
        },
        "parameters": {}
    }
    

  * Lancement de l'exécution : ID de la données stockée `{stored data Corse}`
  * À la fin, on peut voir que notre nouvelle pyramide a une dépendance : elle utilise notre première pyramide, qu'on ne pourra plus supprimer

/datastores/{datastore}/stored_data/{stored data Corse}/dependencies

Corps de réponse JSON
    
    
    {
        "used_by": [],
        "use": [
            {
                "name": "SCAN 1000 Nord Corse",
                "_id": "{stored data Corse Nord}"
            }
        ]
    }
    

### Diffusion

  * Mise à jour de la configuration WMTS-TMS : on change le titre, le résumé et surtout la donnée stockée utilisée. À ce stade, la diffusion n'a pas encore été mise à jour

/datastores/{datastore}/configurations/{configuration}

Corps de requête JSON
    
    
    {
        "type": "WMTS-TMS",
        "name": "SCAN 1000 Corse complète",
        "layer_name": "scan1000_corse",
        "metadata": [
            {
                "format": "application/xml",
                "url": "https://geoservices.ign.fr/sites/default/files/2021-07/IGNF_SCAN1000r_2-1.xml",
                "type": "ISO19115:2003"
            }
        ],
        "type_infos": {
            "title": "SCAN 1000 Corse complète",
            "abstract": "Données SCAN 1000 sur toute la Corse",
            "keywords": [
                "Tutoriel", "Raster", "Mise à jour"
            ],
            "used_data": [
                {
                    "bottom_level": "10",
                    "top_level": "0",
                    "stored_data": "{stored data Corse}"
                }
            ]
        },
        "getfeatureinfo": {
            "stored_data": true
        }
    }
    

  * Synchronisation de l'offre : cette action va renvoyer les informations auprès des serveurs de diffusion pour prendre en compte les modifications. Cela permet de conserver l'offre et son identifiant, ce qui est intéressant lorsque des restrictions d'accès ont été définies 

/datastores/{datastore}/offerings/{offering}
