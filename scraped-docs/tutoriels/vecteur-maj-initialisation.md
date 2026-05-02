source: https://geoplateforme.github.io/tutoriels/production/vecteur/mise-a-jour/initialisation/

[Donnée vecteur](../../../tags/#tag:donnée-vecteur) [Injection](../../../tags/#tag:injection) [Intégration](../../../tags/#tag:intégration)

# Initialisation des données

## Livraison des informations d'initialisation

### Déclarer la livraison

/datastores/{datastore}/uploads

Corps de requête JSONCorps de réponse JSON
    
    
    {
        "description": "Seule la structure est définie : une table et une vue",
        "name": "Installations classées pour la protection de l'environnement",
        "type": "VECTOR",
        "srs": "EPSG:4326"
    }
    
    
    
    {
        "name": "Installations classées pour la protection de l'environnement",
        "description": "Seule la structure est définie : une table et une vue",
        "type": "VECTOR",
        "status": "OPEN",
        "srs": "EPSG:4326",
        "contact": "contact@ign.fr",
        "size": 0,
        "last_event": {
            "title": "Création",
            "date": "2023-05-10T14:42:29.004734134",
            "initiator": {
                "last_name": "Lopper",
                "first_name": "Dave",
                "_id": "{user}"
            }
        },
        "_id": "{upload initialisation}"
    }
    

### Téléverser le fichier SQL

Contenu du SQL
    
    
    CREATE TABLE installation (
        id SERIAL PRIMARY KEY,
        nom_ets character varying(254),
        adresse character varying(207),
        commune character varying(50),
        lib_regime character varying(50),
        url_fiche character varying(80),
        lib_seveso character varying(20),
        geom geometry(Point,4326)
    );
    
    CREATE VIEW installation_autorisation AS SELECT * FROM installation WHERE lib_regime = 'Autorisation';
    
    CREATE INDEX ON installation (lib_regime);
    

`<installation-init.sql>`

/datastores/{datastore}/uploads/{upload initialisation}/data?path=data/installation-init.sql

Corps de requête Multipart

  * file = `<installation-init.sql>`



### Contrôler le contenu

Afin de vérifier que tous les fichiers ont bien été déposés, et l'éventuelle arborescence :

/datastores/{datastore}/uploads/{upload initialisation}/tree

Corps de réponse JSON
    
    
    [
        {
            "type": "DIRECTORY",
            "name": "data",
            "size": 411,
            "children": [
                {
                    "type": "FILE",
                    "name": "installation-init.sql",
                    "size": 411
                }
            ]
        }
    ]
    

## Finalisation de la livraison

### Fermeture

/datastores/{datastore}/uploads/{upload initialisation}/close

### Consultation des vérifications sur ma livraison

/datastores/{datastore}/uploads/{upload initialisation}/checks

Corps de réponse JSON
    
    
    {
        "asked": [
            {
                "check": {
                    "name": "Vérification vecteur",
                    "_id": "66ed8a1b-93d9-4fe9-a413-ab93d31b2964"
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
    

## Création de la donnée vide

### Configuration de l'exécution de traitement

On utilise le traitement d'intégration de données vecteur.

/datastores/{datastore}/processings/executions

Corps de requête JSONCorps de réponse JSON
    
    
    {
        "processing": "0de8c60b-9938-4be9-aa36-9026b77c3c96",
        "inputs": {
            "upload": [
                "{upload initialisation}"
            ]
        },
        "output": {
            "stored_data": {
                "name": "Installations classées pour la protection de l'environnement",
                "storage_tags": ["VECTEUR"]
            }
        }
    }
    
    
    
    {
        "processing": {
            "name": "Intégration de données vecteur livrées en base",
            "_id": "0de8c60b-9938-4be9-aa36-9026b77c3c96"
        },
        "status": "CREATED",
        "creation": "2023-05-24T15:21:21.279291196Z",
        "inputs": {
            "upload": [
                {
                    "type": "VECTOR",
                    "name": "Installations classées pour la protection de l'environnement",
                    "status": "CLOSED",
                    "srs": "EPSG:4326",
                    "_id": "{upload initialisation}"
                }
            ],
            "stored_data": []
        },
        "output": {
            "stored_data": {
                "name": "Installations classées pour la protection de l'environnement",
                "type": "VECTOR-DB",
                "status": "CREATED",
                "_id": "{stored data}"
            }
        },
        "parameters": [],
        "_id": "{execution initialisation}"
    }
    

### Déclenchement de cette exécution

/datastores/{datastore}/processings/executions/{execution initialisation}/launch

## Consultation de la donnée

/datastores/{datastore}/stored_data/{stored data}

Corps de réponse JSON
    
    
    {
        "name": "Installations classées pour la protection de l'environnement",
        "type": "VECTOR-DB",
        "srs": "EPSG:4326",
        "contact": "contact@ign.fr",
        "last_event": {
            "title": "Génération",
            "date": "2023-05-24T15:23:04.928879",
            "initiator": {
                "_id": "{user}"
            }
        },
        "tags": {},
        "storage": {
            "type": "POSTGRESQL",
            "labels": []
        },
        "size": 16384,
        "status": "GENERATED",
        "_id": "{stored data}",
        "type_infos": {
            "relations": [
                {
                    "name": "installation",
                    "type": "TABLE",
                    "attributes": [
                        "id",
                        "nom_ets",
                        "adresse",
                        "commune",
                        "lib_regime",
                        "url_fiche",
                        "lib_seveso",
                        "geom"
                    ],
                    "primary_key": [
                        "id"
                    ]
                },
                {
                    "name": "installation_autorisation",
                    "type": "VIEW",
                    "attributes": [
                        "id",
                        "nom_ets",
                        "adresse",
                        "commune",
                        "lib_regime",
                        "url_fiche",
                        "lib_seveso",
                        "geom"
                    ],
                    "primary_key": []
                }
            ]
        }
    }
    

On retrouve bien notre table et notre vue, qu'on distingue grâce au champ `type`.

## Nettoyage de la livraison

Maintenant que la donnée a été stockée de manière pérenne, on peut supprimer la livraison et son contenu :

/datastores/{datastore}/uploads/{upload initialisation}

## Publication du flux

### Téléversement du style

Télécharger [installation.sld](../../../assets/data/installation.sld)

`<installation.sld>`

/datastores/{datastore}/statics

Corps de requête MultipartCorps de réponse JSON

  * file = `<installation.sld>`
  * type = "GEOSERVER-STYLE"
  * name = "Style pour les installations"


    
    
    {
        "name": "Style pour les installations",
        "type": "GEOSERVER-STYLE",
        "_id": "{sld}",
        "type_infos": {
            "used_attributes": [
                "lib_seveso"
            ]
        }
    }
    

### Téléversement du template d'info-bulle

Télécharger [installation.ftl](../../../assets/data/installation.ftl)

`<installation.ftl>`

/datastores/{datastore}/statics

Corps de requête MultipartCorps de réponse JSON

  * file = `<installation.ftl>`
  * type = "GEOSERVER-FTL"
  * name = "FTL pour les installations"


    
    
    {
        "name": "FTL pour les installations",
        "type": "GEOSERVER-FTL",
        "_id": "{sld}",
        "type_infos": {
            "used_attributes": [
                "nom_ets",
                "url_fiche",
                "commune",
                "adresse",
                "lib_regime"
            ]
        }
    }
    

### Création de la configuration WMS

/datastores/{datastore}/configurations

Corps de requête JSON
    
    
    {
        "type": "WMS-VECTOR",
        "name": "Installations classées pour la protection de l'environnement",
        "layer_name": "installations_classees",
        "type_infos": {
            "title": "Installations classées pour la protection de l'environnement",
            "abstract": "Ce jeu de données correspond aux Installations classées pour la protection de l'environnement (ICPE) soumises à autorisation ou à enregistrement (en fonctionnement ou en cessation d'activité).",
            "keywords": [
                "Tutoriel", "Géorisques", "Installation classées"
            ],
            "bbox": {
                "west": -175,
                "south": -75,
                "east": 175,
                "north": 85
            },
            "used_data": [
            {
                "relations": [
                    {
                        "name": "installation_autorisation",
                        "style": "{sld}",
                        "ftl": "{ftl}"
                    }
                ],
                "stored_data": "{stored data}"
            }
            ]
        }
    }
    

Points d'attentions

  * Comme les tables sont vides, il est indispensable de surcharger le rectangle englobant, en mettant la couverture cible des données (ici une bbox mondiale)
  * On publie bien la vue et non la table



### Publication

/datastores/{datastore}/configurations/{configuration}/offerings

Corps de requête JSON
    
    
    {
        "endpoint": "ae022611-13eb-4a18-8d04-9b7604a031cc",
        "open": true
    }
    

On peut vérifier la présence de notre couche `installations_classees` dans le [getCapabilities du service](https://data.geopf.fr/wms-v?REQUEST=GetCapabilities&SERVICE=WMS&VERSION=1.3.0)

Si on consulte la donnée sur QGis, on ne verra pour le moment aucune donnée.
