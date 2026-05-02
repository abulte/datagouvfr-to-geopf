source: https://geoplateforme.github.io/tutoriels/production/vecteur/mise-a-jour/delete_update/

[Donnée vecteur](../../../tags/#tag:donnée-vecteur) [Injection](../../../tags/#tag:injection) [Intégration](../../../tags/#tag:intégration)

# Suppression et modification de données

On peut également réaliser des suppressions et des modifications dans les tables de la donnée cible. Suppressions et modifications se font via des fichiers eu format CSV :

  * Des suppressions dans une table se fait via la livraison d'un fichier CSV `<nom de la table>.delete`. Chaque ligne de ce fichier donnera une instruction d'un DELETE dont le filtre est défini par les champs précisés.
  * Des modifications dans un table se fait via la livraison d'un fichier CSV `<nom de la table>.update`. La table cible doit avoir une clé primaire de définie et le fichier CSV doit préciser les valeurs des attributs de cette clé primaire. Chaque ligne de ce fichier donnera une instruction d'un UPDATE dont le filtre est défini par les champs de la clé primaire et les champs modifiés par les autres champs présent.



Les suppressions sont jouées en premier, puis les modifications et enfin les insertions via des fichiers vecteurs comme vu précédemment.

## Livraison des modifications

Exemple :

[installation.delete](../../../assets/data/installation.delete)

Contenu
    
    
    commune
    VILLERS SEMEUSE
    CHARLEVILLE MEZIERES
    

[installation.update](../../../assets/data/installation.update)

Contenu
    
    
    id,commune
    10060,BESANÇON
    10062,BESANÇON
    10063,BESANÇON
    10064,BESANÇON
    10066,BESANÇON
    10068,BESANÇON
    10070,BESANÇON
    10077,BESANÇON
    10082,BESANÇON
    10087,BESANÇON
    10095,BESANÇON
    

### Déclarer la livraison

/datastores/{datastore}/uploads

Corps de requête JSONCorps de réponse JSON
    
    
    {
        "description": "Suppression des données",
        "name": "Modification et suppression de données",
        "type": "VECTOR",
        "srs": "EPSG:4326"
    }
    
    
    
    {
        "name": "Modification et suppression de données",
        "description": "Suppression des données",
        "type": "VECTOR",
        "status": "OPEN",
        "srs": "EPSG:4326",
        "contact": "contact@ign.fr",
        "size": 0,
        "last_event": {
            "title": "Création",
            "date": "2023-10-20T10:17:58.178975406",
            "initiator": {
                "last_name": "Lopper",
                "first_name": "Dave",
                "_id": "{user}"
            }
        },
        "_id": "{upload suppression modification}"
    }
    

### Téléverser les fichiers CSV

`<installation.update>`

/datastores/{datastore}/uploads/{upload suppression modification}/data?path=data/installation.update

Corps de requête Multipart

  * file = `<installation.update>`



`<installation.delete`

/datastores/{datastore}/uploads/{upload suppression modification}/data?path=data/installation.delete

Corps de requête Multipart

  * file = `<installation.delete>`



### Contrôler le contenu

Afin de vérifier que tous les fichiers ont bien été déposés, et l'éventuelle arborescence :

/datastores/{datastore}/uploads/{upload suppression modification}/tree

Corps de réponse JSON
    
    
    [
        {
            "type": "DIRECTORY",
            "name": "data",
            "size": 232,
            "children": [
                {
                    "type": "FILE",
                    "name": "installation.delete",
                    "size": 45
                },
                {
                    "type": "FILE",
                    "name": "installation.update",
                    "size": 187
                }
            ]
        }
    ]
    

## Terminer la livraison

### Fermeture

/datastores/{datastore}/uploads/{upload suppression modification}/close

### Consultation des vérifications sur ma livraison

/datastores/{datastore}/uploads/{upload suppression modification}/checks

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
    

## Modification des données

### Configuration de l'exécution de traitement

On utilise à nouveau le traitement d'intégration de données vecteur.

Points d'attentions

Pour la donnée en sortie, on ne précise pas un nom, mais l'identifiant de notre donnée stockée initialisée juste avant. On va donc modifier une donnée plutôt qu'en créer une nouvelle. Par défaut, le traitement d'intégration ne prend pas en compte les fichiers de suppressions et modifications, pour limiter les mauvaises manipulations. On va donc préciser en paramètre que nous voulons faire ce genre d'action.

/datastores/{datastore}/processings/executions

Corps de requête JSONCorps de réponse JSON
    
    
    {
        "processing": "0de8c60b-9938-4be9-aa36-9026b77c3c96",
        "inputs": {
            "upload": [
                "{upload suppression modification}}"
            ]
        },
        "output": {
            "stored_data": {
                "id": "{stored data}"
            }
        },
        "parameters": {
            "update": true,
            "delete": true
        }
    }
    
    
    
    {
        "processing": {
            "name": "Intégration de données vecteur livrées en base",
            "_id": "0de8c60b-9938-4be9-aa36-9026b77c3c96"
        },
        "status": "CREATED",
        "creation": "2023-10-20T12:44:07.451183707Z",
        "inputs": {
            "upload": [
                {
                    "type": "VECTOR",
                    "name": "Installations classées pour la protection de l'environnement",
                    "status": "CLOSED",
                    "srs": "EPSG:4326",
                    "_id": "{upload suppression modification}"
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
        "parameters": {
            "update": true,
            "delete": true
        },
        "_id": "{execution suppression modification}}"
    }
    

### Déclenchement de cette exécution

/datastores/{datastore}/processings/executions/{execution suppression modification}}/launch

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
                        7.11555778,
                        46.26953767
                    ],
                    [
                        7.11555778,
                        50.15761815
                    ],
                    [
                        4.0492738,
                        50.15761815
                    ],
                    [
                        4.0492738,
                        46.26953767
                    ],
                    [
                        7.11555778,
                        46.26953767
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
        "size": 1073152,
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
    

## Nettoyage de la livraison

Maintenant que la donnée a été stockée de manière pérenne, on peut supprimer la livraison et son contenu :

/datastores/{datastore}/uploads/{upload suppression modification}

## Consultation du flux WMS

Notre flux WMS retourne désormais la donnée modifiée sur les Ardennes et le Doubs.

https://data.geopf.fr/wms-v?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetFeatureInfo&BBOX=47.15389042500531502,5.95024509374819122,47.37809636403335389,6.16439800318477449&CRS=EPSG:4326&WIDTH=916&HEIGHT=959&LAYERS=installations_classees&STYLES=&FORMAT=image/png&QUERY_LAYERS=installations_classees&INFO_FORMAT=application/json&I=437&J=478&FEATURE_COUNT=10

AvantAprès
    
    
    {
        "type": "FeatureCollection",
        "features":
        [
            {
                "type": "Feature",
                "id": "installation_autorisation_ad93fd1b-d2be-4dc2-8860-63f86e469ca2.fid-4a7acf16_18ad0a2e739_-43de",
                "geometry":
                {
                    "type": "Point",
                    "coordinates":
                    [
                        6.051,
                        47.267
                    ]
                },
                "geometry_name": "geom",
                "properties":
                {
                    "id": 10060,
                    "nom_ets": "CURTIL PLASTIQUE",
                    "adresse": "12 chemin de l'Ermitage",
                    "commune": "BESANCON",
                    "lib_regime": "Autorisation",
                    "url_fiche": "https://www.georisques.gouv.fr/risques/installations/donnees/details/0005902181",
                    "lib_seveso": "Non Seveso"
                },
                "bbox":
                [
                    6.051,
                    47.267,
                    6.051,
                    47.267
                ]
            }
        ],
        "totalFeatures": "unknown",
        "numberReturned": 1,
        "timeStamp": "2023-10-20T13:43:19.684Z",
        "crs":
        {
            "type": "name",
            "properties":
            {
                "name": "urn:ogc:def:crs:EPSG::4326"
            }
        },
        "bbox":
        [
            6.051,
            47.267,
            6.051,
            47.267
        ]
    }
    
    
    
    {
        "type": "FeatureCollection",
        "features":
        [
            {
                "type": "Feature",
                "id": "installation_autorisation_ad93fd1b-d2be-4dc2-8860-63f86e469ca2.fid-4a7acf16_18ad0a2e739_-43de",
                "geometry":
                {
                    "type": "Point",
                    "coordinates":
                    [
                        6.051,
                        47.267
                    ]
                },
                "geometry_name": "geom",
                "properties":
                {
                    "id": 10060,
                    "nom_ets": "CURTIL PLASTIQUE",
                    "adresse": "12 chemin de l'Ermitage",
                    "commune": "BESANÇON",
                    "lib_regime": "Autorisation",
                    "url_fiche": "https://www.georisques.gouv.fr/risques/installations/donnees/details/0005902181",
                    "lib_seveso": "Non Seveso"
                },
                "bbox":
                [
                    6.051,
                    47.267,
                    6.051,
                    47.267
                ]
            }
        ],
        "totalFeatures": "unknown",
        "numberReturned": 1,
        "timeStamp": "2023-10-20T13:43:19.684Z",
        "crs":
        {
            "type": "name",
            "properties":
            {
                "name": "urn:ogc:def:crs:EPSG::4326"
            }
        },
        "bbox":
        [
            6.051,
            47.267,
            6.051,
            47.267
        ]
    }
    
