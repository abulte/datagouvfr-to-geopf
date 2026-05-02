source: https://geoplateforme.github.io/tutoriels/production/raster/mise-a-jour/composition/

[Chaînage](../../../tags/#tag:chaînage) [Donnée raster](../../../tags/#tag:donnée-raster) [Intégration](../../../tags/#tag:intégration)

# Par composition a posteriori

L'avantage de ce mode de fonctionnement est que les générations des pyramides indépendantes peuvent se faire en parallèle. Il n'y a pas de modifications de données et celles ci ne sont pas dupliquées. En revanche, une dépendance est ajoutée entre les données, ce qui va empêcher la suppression des données référencées (les pyramides utilisées dans la composition).
    
    
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
    
        LIV2: Calcul de la pyramide contenant le deuxième jeu
        note left of LIV2
            Livraison (upload)
            Vérification (check)
            Traitement (processing)
            Exécution de traitement (processing execution)
            Données stockée (stored data)
        end note
    
        FUS: Calcul de la pyramide fusionnée
        note left of FUS
            Traitement (processing)
            Exécution de traitement (processing execution)
            Données stockée (stored data)
        end note
    
        PUB_TILED: Publication en WMTS/TMS pour validation
        note right of PUB_TILED
            Configuration (configuration)
            Point d'accès (endpoint)
            Offre (offering)
        end note
    
        state fork_state_deb <<fork>>
        state fork_state_fin <<fork>>
    
        [*] --> fork_state_deb
        fork_state_deb --> LIV1
        fork_state_deb --> LIV2
        LIV1 --> fork_state_fin
        LIV2 --> fork_state_fin
        fork_state_fin --> FUS
        FUS --> PUB_TILED
    
        classDef concepts fill:#eee,stroke:#8d1d75,stroke-width:3px;
    
        class LIV1,LIV2,PUB_TILED,FUS concepts

## Gestion du premier jeu de données

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



Attention

Il est important de préciser que l'on veut générer et stocker les masques. Ces derniers vont être indispensables pour que la fusion évite la perte de données.

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
            "interpolation": "bicubic",
            "mask": true
        }
    }
    

  * Lancement de l'exécution : ID de la données stockée `{stored data Corse Nord}`



Il n'est pas nécessaire d'attendre la fin de ce traitement pour lancer celui sur le deuxième jeu.

## Gestion du deuxième jeu de données

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
  * Création de l'exécution de traitement



Attention

Il est important de préciser que l'on veut générer et stocker les masques. Ces derniers vont être indispensables pour que la fusion évite la perte de données.

/datastores/{datastore}/processings/executions

Corps de requête JSON
    
    
    {
        "processing": "2ae50661-986c-4f47-a3f0-e380417b522c",
        "inputs": {
            "upload": [
                "{upload Corse Sud}"
            ]
        },
        "output": {
            "stored_data": {
                "name": "SCAN 1000 Sud Corse",
                "storage_tags": ["PYRAMIDE"]
            }
        },
        "parameters": {
            "tms": "PM",
            "compression": "jpg",
            "interpolation": "bicubic",
            "mask": true
        }
    }
    

  * Lancement de l'exécution : ID de la données stockée `{stored data Corse Sud}`



## Génération de la pyramide fusionnée

Lorsque les deux pyramides indépendantes sont générées :

  * Récupération du traitement qui nous intéresse : ID `7cdca031-9e86-4804-8764-9b1d783b087d`

/datastores/{datastore}/processings/7cdca031-9e86-4804-8764-9b1d783b087d

Corps de réponse JSON
    
    
    {
        "name": "Fusion de pyramides raster",
        "description": "Ce traitement permet de générer une pyramide raster par composition de plusieurs pyramides indépendantes. Seules les dalles présentes dans plusieurs entrées seront recalculées. Celles présentes dans une seule entrée seront référencées. La pyramide en sortie a donc des dépendances avec celles en entrée.",
        "input_types": {
            "upload": [],
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
                "name": "parallelization",
                "description": "Le niveau de parallélisation du calcul (nombre de scripts parallèles, nombre de threads)",
                "mandatory": false,
                "default_value": 1
            },
            {
                "name": "top",
                "description": "Niveau du haut de la pyramide en sortie : ce sera par défaut le plus haut de toutes les pyramides en entrée",
                "mandatory": false
            },
            {
                "name": "bottom",
                "description": "Niveau du bas de la pyramide en sortie : ce sera par défaut le plus bas de toutes les pyramides en entrée",
                "mandatory": false
            },
            {
                "name": "bbox",
                "description": "Étendue géographique sur laquelle sera générée la pyramide : ce sera par défaut l'union des étendues de toutes les pyramides en entrée",
                "mandatory": false
            }
        ],
        "_id": "7cdca031-9e86-4804-8764-9b1d783b087d",
        "required_checks": []
    }
    

  * Création de l'exécution de traitement (on s'appuie sur les valeurs par défaut des paramètres)

/datastores/{datastore}/processings/executions

Corps de requête JSON
    
    
    {
        "processing": "7cdca031-9e86-4804-8764-9b1d783b087d",
        "inputs": {
            "stored_data": [
                "{stored data Corse Nord}",
                "{stored data Corse Sud}"
            ]
        },
        "output": {
            "stored_data": {
                "name": "SCAN 1000 Corse",
                "storage_tags": ["PYRAMIDE"]
            }
        },
        "parameters": {}
    }
    

  * Lancement de l'exécution
  * À la fin, on peut voir que notre nouvelle pyramide a deux dépendances : elle utilise nos deux pyramides indépendantes, qu'on ne pourra plus supprimer.

/datastores/{datastore}/stored_data/{stored data Corse}/dependencies

Corps de réponse JSON
    
    
    {
        "used_by": [],
        "use": [
            {
                "name": "SCAN 1000 Nord Corse",
                "_id": "{stored data Corse Nord}"
            },
            {
                "name": "SCAN 1000 Sud Corse",
                "_id": "{stored data Corse Sud}"
            }
        ]
    }
    

En publiant notre pyramide fusionnée, on retrouve bien la Corse en entier.
