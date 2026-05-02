source: https://geoplateforme.github.io/tutoriels/production/hautniveau/extraction/utilisation/

[Donnée vecteur](../../../tags/#tag:donnée-vecteur) [Service avancé](../../../tags/#tag:service-avancé) [Téléchargement](../../../tags/#tag:téléchargement)

# Télécharger un sous ensemble d'une donnée vecteur

Lorsque l'on veut télécharger une donnée vecteur, il y a plusieurs possibilités :

  * La donnée entière est disponible sur le service de téléchargement et la récupérer en entier est acceptable
  * La donnée est disponible sur le service de téléchargement selon certains découpages et s'appuyer sur cette offre est acceptable (téléchargement de la BDTopo sur un département)
  * La sous partie qui nous intéresse est suffisamment petite pour pouvoir exploiter le standard WFS de manière viable (filtrage assez simple, résultat assez léger)



Lorsqu'aucun de ces cas n'est acceptable, il est alors possible d'utiliser le service d'extraction. Cela implique d'avoir accès à la donnée voulue sur ce service.

Le service d'extraction nécessite d'être authentifié avec son compte Géoplateforme.

## Outil de requête

Une [collection Bruno](https://github.com/Geoplateforme/clients-configurations/tree/master/bruno/diffusion/extraction) est préconfigurée avec les requêtes de ce tutoriel. Vous pouvez lire [cette documentation](https://github.com/Geoplateforme/clients-configurations?tab=readme-ov-file#collections-bruno) pour voir comment l'utiliser.

## Lister son catalogue de données extractibles

Les données sont rendues extractibles par les personnes responsables de leur diffusion. Elles peuvent choisir de les rendre ouvertes, donc extractibles par tout le monde, ou ne les partager qu'avec certaines communautés. Dans ce dernier cas, il faut alors être membre d'une de ces communautés pour les voir sur le service d'extraction.

https://data.geopf.fr/extraction/processes

Corps de réponse JSON
    
    
    {
        "processes": [
            ...
            {
                "id": "{process}",
                "title": "Extraction Vecteur depuis Pays et écorégions",
                "description": "Script d'extraction d'une donnée stockée ARCHIVE depuis une donnée stockée VECTOR-DB. Description de cette donnée stockée :  Pays et écorégions",
                "links": [
                    {
                    "rel": "self",
                    "type": "application/json",
                    "title": "Extraction Vecteur depuis Pays et écorégions",
                    "href": "/processes/{process}"
                    },
                    {
                    "rel": "describedby",
                    "type": "application/json",
                    "title": "Extraction Vecteur depuis Pays et écorégions",
                    "href": "/users/me/stored_data/{stored data}"
                    }
                ],
                "outputTransmission": [
                    "reference"
                ],
                "jobControlOptions": [
                    "async-execute"
                ]
            },
            ...
        ],
        "links": [
            {
            "rel": "self",
            "type": "application/json",
            "title": "Liste des processus disponibles",
            "href": "/processes"
            }
        ]
    }
    

On peut également voir les données partagées avec nous via un appel à l'API Entrepôt dans notre espace personnel. On voit ici toutes les données publiques et celles partagées avec nos communautés. Cependant, seules les données vecteur sont extractibles pour le moment, mais cette route permet un filtrage plus fin :

/users/me/stored_data

Paramètres de requêteCorps de réponse JSON

  * type = `VECTOR-DB`
  * name = `%25régions%25`


    
    
    [
        {
            "name": "Pays et écorégions",
            "type": "VECTOR-DB",
            "open": true,
            "srs": "EPSG:4326",
            "_id": "{stored data}"
        }
    ]
    

## Avoir les informations détaillées sur la donnée extractible

Afin de connaître les paramètres possibles pour définir la sous partie de la donnée qui nous intéresse, il est possible d'avoir plus de détails sur la donnée et son extraction

  * via l'API Extraction : on a tous les paramètres possibles pour configurer son extraction, mais pas sur la donnée extraite elle même

https://data.geopf.fr/extraction/processes/{process}

Corps de réponse JSON
    
    
    {
        "id": "{process}",
        "title": "Extraction Vecteur depuis Pays et écorégions",
        "description": "Script d'extraction d'une donnée stockée ARCHIVE depuis une donnée stockée VECTOR-DB. Description de cette donnée stockée :  Pays et écorégions",
        "links": [
            {
            "rel": "self",
            "type": "application/json",
            "title": "Extraction Vecteur depuis Pays et écorégions",
            "href": "/processes/{process}"
            },
            {
            "rel": "describedby",
            "type": "application/json",
            "title": "Extraction Vecteur depuis Pays et écorégions",
            "href": "/users/me/stored_data/{stored data}"
            }
        ],
        "outputTransmission": [
            "reference"
        ],
        "jobControlOptions": [
            "async-execute"
        ],
        "version": "1.0.0",
        "inputs": [
            {
                "maxOccurs": "1",
                "description": "La compression de sortie",
                "schema": {
                    "enum": [
                        "7zip"
                    ],
                    "type": "string"
                },
                "minOccurs": "0",
                "title": "compression"
            },
            {
                "maxOccurs": "1",
                "description": "Détails des tables à extraire et filtres à appliquer sous la forme {\"nom_table\" :{\"attributes\" :[\"champ1\",\"champ2\"],\"filters\" :\"champ1 ='valeur_a_respecter'..\"}, \"nom_table2\" :{\"attributes\" :[\"champ1\",\"champ2\"],\"filters\" :\"champ1='valeur_a_respecter'..\"}...}. La syntaxe du filtre est une clause WHERE POSTGRESQL/POSTGIS qui peut inclure une ou plusieurs fonctions spatiales",
                "schema": {},
                "minOccurs": "1",
                "title": "relations"
            },
            {
                "maxOccurs": "1",
                "description": "La projection de sortie des données géométrie sous la forme EPSG:xxxx où xxxx est le code EPSG de la projection souhaitée.",
                "schema": {},
                "minOccurs": "0",
                "title": "srs"
            },
            {
                "maxOccurs": "1",
                "description": "Le format de sortie",
                "schema": {
                    "enum": [
                    "PGDUMP",
                    "ESRI SHAPEFILE",
                    "GEOJSON",
                    "GPKG",
                    "GML",
                    "PARQUET"
                    ]
                },
                "minOccurs": "1",
                "title": "format"
            },
            {
                "maxOccurs": "1",
                "description": "Indique pour les formats possible si un seul fichiers doit être produit en sortie pour l'ensemble des relations",
                "schema": {
                    "type": "boolean"
                },
                "minOccurs": "0",
                "title": "append"
            },
            {
                "maxOccurs": "1",
                "description": "Durée (en heures) du temps de conservation des données extraites à partir de leur mise à disposition via l'API de résultats (par défaut : {DEFAULT_LIFETIME) heures)",
                "schema": {
                    "type": "integer"
                },
                "minOccurs": "0",
                "title": "Durée de rétention"
            }
        ],
        "outputs": {
            "logs": {
                "title": "Logs du processus d'extraction",
                "schema": {
                    "type": "string"
                }
            },
            "summary": {
                "title": "Informations sur le processus d'extraction",
                "schema": {
                    "$ref": "/annexes/extraction/schema.json"
                }
            },
            "extractedData": {
                "title": "Résultats du processus d'extraction",
                "schema": {
                    "contentMediaType": "application/atom+xml",
                    "type": "string",
                    "contentEncoding": "UTF-8"
                }
            }
        }
    }
    

  * via l'API Entrepôt : on retrouve cette URL directement dans les réponses de l'API extraction, au niveau de la liste des processes. Cet appel permet d'avoir des informations sur la donnée mais pas sur les paramètres d'extraction

/users/me/stored_data/{stored data}

Corps de réponse JSON
    
    
        {
        "creation": "2024-11-06T14:27:12.139552Z",
        "name": "Pays et écorégions",
        "type": "VECTOR-DB",
        "open": true,
        "srs": "EPSG:4326",
        "contact": "contact@ign.fr",
        "extent": {
            "geometry": {
            "type": "MultiPolygon",
                "coordinates": [
                    ....
                ]
            },
            "type": "Feature"
        },
        "size": 13139968,
        "status": "GENERATED",
        "_id": "{stored data}",
        "type_infos": {
            "relations": [
                {
                    "name": "ecoregions",
                    "type": "TABLE",
                    "attributes": {
                        "id": "integer",
                        "fid": "integer",
                        "nnh": "integer",
                        "geom": "geometry(Polygon,4326)",
                        "color": "character varying",
                        "realm": "character varying",
                        "eco_name": "character varying",
                        "nnh_name": "character varying",
                        "color_bio": "character varying",
                        "color_nnh": "character varying",
                        "biome_name": "character varying",
                        "test_add_column": "integer"
                    },
                    "primary_key": [
                        "fid"
                    ]
                },
                {
                    "name": "pays",
                    "type": "TABLE",
                    "attributes": {
                        "id": "integer",
                        "un": "integer",
                        "fid": "integer",
                        "lat": "double precision",
                        "lon": "double precision",
                        "area": "integer",
                        "fips": "character varying(2)",
                        "geom": "geometry(Polygon,4326)",
                        "iso2": "character varying(2)",
                        "iso3": "character varying(3)",
                        "name": "character varying(50)",
                        "region": "integer",
                        "pop2005": "bigint",
                        "subregion": "integer"
                    },
                    "primary_key": [
                        "fid"
                    ]
                }
            ]
        }
    }
    

## Demander une extraction

On va maintenant demander une extraction sur ma donnée :

  * Je ne veux que la table pays
  * Les pays dont la population est inférieure à 50 millions
  * Je ne veux que les attributs `id`, `area`, `pop2005`, `name` et `region`
  * Je veux les données en EPSG:3857
  * Je veux les données en Géoparquet non compressé.



Les inputs sont les paramètres d'extraction décrits dans l'appel précédent à l'API Extraction : ceux avec `minOccurs` à 1 sont obligatoires. Les outputs permettent de dire si on veut les logs et le résumé

https://data.geopf.fr/extraction/processes/{process}/execution

Corps de requête JSONCorps de réponse JSON
    
    
    {
        "inputs": {
            "format": "PARQUET",
            "relations": {
                "pays": {
                    "attributes": ["id", "area", "pop2005", "name", "region"],
                    "filters": "pop2005 < 50000000"
                }
            },
            "srs": "EPSG:3857"
        },
        "outputs": {
            "logs": {},
            "summary": {},
            "extractedData": {}
        }
    }
    
    
    
    {
        "jobID": "{job}",
        "status": "running",
        "message": "Extraction des données demandées en cours",
        "created": "2025-09-03T08:53:11.580143115Z",
        "updated": "2025-09-03T08:53:11.580143115Z",
        "links": [
            {
            "rel": "describedBy",
            "type": "application/json",
            "title": "Job {job}",
            "href": "/jobs/{job}"
            }
        ],
        "started": "2025-09-03T08:53:11.580143115Z",
        "processID": "{process}",
        "type": "process"
    }
    

## Suivre son extraction

Selon la taille de la donnée et la taille / complexité de la sous partie demandée, une extraction peut prendre du temps. Pour suivre son avancement et connaître l'URL de téléchargement à la fin, on fait l'appel suivant :

https://data.geopf.fr/extraction/jobs/{job}

Corps de réponse JSON
    
    
    {
        "jobID": "{job}",
        "status": "running",
        "message": "Données extraites, mise à disposition des résultats en cours",
        "created": "2025-09-03T08:53:11.580143Z",
        "updated": "2025-09-03T08:55:24.681932Z",
        "links": [
            {
            "rel": "self",
            "type": "application/json",
            "title": "Job {job}",
            "href": "/jobs/{job}"
            },
            {
            "rel": "describedBy",
            "type": "application/json",
            "title": "Résultats du job {job},
            "href": "/jobs/{job}/results"
            }
        ],
        "started": "2025-09-03T08:53:11.580143Z",
        "processID": "ef202bf4-faf9-4d71-95bb-080ce599ada5_5e8c9b27-4610-436d-a24c-7aa2fe5a9feb",
        "type": "process"
    }
    

Si vous avez perdu l'identifiant de votre extraction (job), vous pouvez récupérer la liste de vos extraction (il est possible de filtrer par statut, process, durée d'exécution...). Cela permet aussi de retrouver un historique de ses extractions.

https://data.geopf.fr/extraction/jobs

Paramètres de requêteCorps de réponse JSON

  * statuses = `RUNNING`


    
    
    {
        "jobs": [
            {
            "jobID": "{job}",
            "status": "running",
            "message": "Données extraites, mise à disposition des résultats en cours",
            "created": "2025-09-03T08:53:11.580143Z",
            "updated": "2025-09-03T08:55:24.681932Z",
            "links": [
                {
                "rel": "describedBy",
                "type": "application/json",
                "title": "Résultats du job {job}",
                "href": "/jobs/{job}"
                }
            ],
            "started": "2025-09-03T08:53:11.580143Z",
            "processID": "{process}",
            "type": "process"
            }
        ],
        "links": [
            {
            "rel": "self",
            "type": "application/json",
            "title": "Liste des jobs",
            "href": "/jobs"
            }
        ]
    }
    

## Télécharger le résultat

Lorsque le statut du job passe à `successful`, l'API suivante devient disponible, pour connaître notamment l'URL de téléchargement du résultat

https://data.geopf.fr/extraction/jobs/{job}/results

Corps de réponse JSON
    
    
    {
        "logs": "[\"2025-09-03 14:37:03,049INFO||gpf-extraction-vector-db||8||Ouverture du fichier de configuration\",\"2025-09-03 14:37:03,095INFO||cli||224||Extraction de données vecteurs\",\"2025-09-03 14:37:03,293INFO||cli||224||Création de l'utilisateur temporaire\",\"2025-09-03 14:37:03,349INFO||cli||224||Début des traitements : 2025-09-03T14:37:03Z\",\"2025-09-03 14:37:04,347INFO||cli||224||Fin des traitements : 2025-09-03T14:37:04Z\",\"2025-09-03 14:37:04,347INFO||cli||224||Génération et upload du fichier de métadonnées\",\"2025-09-03 14:37:04,364INFO||cli||224||Copie des données vers le S3\",\"2025-09-03 14:37:04,692INFO||core||550||Calcul et upload du fichier __descriptor.json\",\"2025-09-03 14:37:04,897INFO||core||550||Mise à jour des informations de la données stockée\",\"2025-09-03 14:37:04,897INFO||cli||224||Suppression de l'utilisateur temporaire\"]",
        "summary": {
            "rel": "describedBy",
            "type": "application/json",
            "title": "Informations sur le processus d'extraction",
            "href": "https://data.geopf.fr/extraction/telechargement/download/{{ layer }}/data/extraction.json"
        },
        "extractData": {
            "rel": "describedBy",
            "type": "application/atom+xml",
            "title": "Résultats du processus d'extraction",
            "href": "https://data.geopf.fr/extraction/telechargement/resource/{{ layer }}/data"
        }
    }
    

Si cet appel est fait alors que l'extraction est encore en cours (statut `running`), une erreur 404 est retournée.

L'appel à `https://data.geopf.fr/extraction/telechargement/resource/{{ layer }}/data` donne la liste des fichiers téléchargeables. Le fichier `https://data.geopf.fr/extraction/telechargement/download/{{ layer }}/data/extraction.json` est un compte rendu de l'extraction :
    
    
    {
        "begin_timestamp": "2025-09-03T14:37:03Z",
        "end_timestamp": "2025-09-03T14:37:04Z",
        "format": "PARQUET",
        "data_output_name": "export",
        "metadata_output_name": "extraction.json",
        "relations": [
            {
                "{schema}.pays": "SUCCESS"
            }
        ]
    }
    

Dans notre cas, nous n'avons qu'un fichier de données à télécharger (une seule table) avec `https://data.geopf.fr/extraction/telechargement/resource/{{ layer }}/data/data/export/{schema}.pays.parquet`

Une fois les données chargées dans QGis, on retrouve bien nos données, limitées à ce que l'on avait demandé.
