source: https://geoplateforme.github.io/tutoriels/production/vecteur/mise-a-jour/injection1/

[Donnée vecteur](../../../tags/#tag:donnée-vecteur) [Injection](../../../tags/#tag:injection) [Intégration](../../../tags/#tag:intégration)

# Injection d'un premier lot de données

## Ajout du premier lot de données

### Déclarer la livraison

/datastores/{datastore}/uploads

Corps de requête JSONCorps de réponse JSON
    
    
    {
        "description": "Données sur les Ardennes",
        "name": "Installations classées pour la protection de l'environnement",
        "type": "VECTOR",
        "srs": "EPSG:4326"
    }
    
    
    
    {
        "description": "Données sur les Ardennes",
        "name": "Installations classées pour la protection de l'environnement",
        "type": "VECTOR",
        "status": "OPEN",
        "srs": "EPSG:4326",
        "contact": "contact@ign.fr",
        "size": 0,
        "last_event": {
            "title": "Création",
            "date": "2023-05-10T14:52:29.004734134",
            "initiator": {
                "last_name": "Lopper",
                "first_name": "Dave",
                "_id": "{user}"
            }
        },
        "_id": "{upload injection 1}"
    }
    

### Téléverser le fichier Geopackage

`<installation.gpkg>`

/datastores/{datastore}/uploads/{upload injection 1}/data?path=data/installation.gpkg

Corps de requête Multipart

  * file = `<installation.gpkg>`



### Contrôler le contenu

Afin de vérifier que tous les fichiers ont bien été déposés, et l'éventuelle arborescence :

/datastores/{datastore}/uploads/{upload injection 1}/tree

Corps de réponse JSON
    
    
    [
        {
            "type": "DIRECTORY",
            "name": "data",
            "size": 368640,
            "children": [
                {
                    "type": "FILE",
                    "name": "installation.gpkg",
                    "size": 368640
                }
            ]
        }
    ]
    

## Finalisation de la livraison

### Fermeture

/datastores/{datastore}/uploads/{upload injection 1}/close

### Consultation des vérifications sur ma livraison

/datastores/{datastore}/uploads/{upload injection 1}/checks

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
    

## Injection des données

### Configuration de l'exécution de traitement

On utilise à nouveau le traitement d'intégration de données vecteur.

Points d'attentions

Pour la donnée en sortie, on ne précise pas un nom, mais l'identifiant de notre donnée stockée initialisée juste avant. On va donc modifier une donnée plutôt qu'en créer une nouvelle.

/datastores/{datastore}/processings/executions

Corps de requête JSONCorps de réponse JSON
    
    
    {
        "processing": "0de8c60b-9938-4be9-aa36-9026b77c3c96",
        "inputs": {
            "upload": [
                "{upload injection 1}"
            ]
        },
        "output": {
            "stored_data": {
                "id": "{stored data}"
            }
        }
    }
    
    
    
    {
        "processing": {
            "name": "Intégration de données vecteur livrées en base",
            "_id": "0de8c60b-9938-4be9-aa36-9026b77c3c96"
        },
        "status": "CREATED",
        "creation": "2023-05-24T16:29:24.113049487Z",
        "inputs": {
            "upload": [
                {
                    "type": "VECTOR",
                    "name": "Installations classées pour la protection de l'environnement",
                    "status": "CLOSED",
                    "srs": "EPSG:4326",
                    "_id": "{upload injection 1}"
                }
            ],
            "stored_data": []
        },
        "output": {
            "stored_data": {
                "name": "Installations classées pour la protection de l'environnement",
                "type": "VECTOR-DB",
                "status": "GENERATED",
                "srs": "EPSG:4326",
                "_id": "{stored data}"
            }
        },
        "parameters": [],
        "_id": "{execution injection 1}"
    }
    

### Déclenchement de cette exécution

/datastores/{datastore}/processings/executions/{execution injection 1}/launch

## Consultation de la donnée

/datastores/{datastore}/stored_data/{stored data}

Corps de réponse JSON
    
    
    {
        "name": "Installations classées pour la protection de l'environnement",
        "type": "VECTOR-DB",
        "srs": "EPSG:4326",
        "contact": "contact@ign.fr",
        "extent": {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        5.35581878,
                        49.2396879
                    ],
                    [
                        5.35581878,
                        50.15761815
                    ],
                    [
                        4.0492738,
                        50.15761815
                    ],
                    [
                        4.0492738,
                        49.2396879
                    ],
                    [
                        5.35581878,
                        49.2396879
                    ]
                ]
            ]
        },
        "last_event": {
            "title": "Modification",
            "date": "2023-05-24T16:32:50.838863",
            "initiator": {
                "_id": "{user}"
            }
        },
        "tags": {},
        "storage": {
            "type": "POSTGRESQL",
            "labels": []
        },
        "size": 270336,
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
    

On note qu'une étendue a pu être calculée, et que la taille est passée de 16 384 octets à 270 336. Le dernier événement est une modification et plus une génération.

## Nettoyage de la livraison

Maintenant que la donnée a été stockée de manière pérenne, on peut supprimer la livraison et son contenu :

/datastores/{datastore}/uploads/{upload injection 1}

## Consultation du flux WMS

Sans avoir à modifier la configuration de la diffusion, notre flux WMS retourne désormais de la donnée sur les Ardennes

On peut voir les cercles en dessous qui sont les données livrées. Les données accessibles en WMS (diamant rose, bleu ou vert) sont bien un sous-ensemble seulement.
