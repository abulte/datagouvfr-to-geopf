source: https://geoplateforme.github.io/tutoriels/production/archive/base/publication/

[Diffusion](../../../tags/#tag:diffusion) [Donnée archive](../../../tags/#tag:donnée-archive) [Nomenclature](../../../tags/#tag:nomenclature) [Téléchargement](../../../tags/#tag:téléchargement)

# Publication en téléchargement

## Configuration de la diffusion

La configuration centralise toutes les informations nécessaires à la diffusion de données sur les services. A ce moment, on va contrôler les paramètres et détecter les erreurs ou conflits potentiels :

  * nom de couche déjà pris (il doit y avoir unicité sur toutes les configurations DOWNLOAD de la plateforme)
  * doublon dans le nom des sous-couches (si on veut diffuser plusieurs données ARCHIVE au sein d'une même configuration)

/datastores/{datastore}/configurations

Corps de requête JSON
    
    
    {
        "type": "DOWNLOAD",
        "name": "Limites administratives",
        "layer_name": "limites_administratives",
        "type_infos": {
            "title": {
                "fr": "Limites administratives",
                "en": "Administrative units"
            },
            "abstract": {
                "fr": "Limites administratives, au format Shapefile, sur la France métropolitaine"
            },
            "keywords": ["Tutoriel", "Limites administratives"],
            "product_identifier": "Admin Express",
            "used_data": [
                {
                    "sub_name": "departements",
                    "title": {
                        "fr": "Données départementales"
                    },
                    "abstract": {
                        "fr": "Départements et limites départementales, au format Shapefile, sur la France métropolitaine"
                    },
                    "keywords": ["Limites départementales"],
                    "format": "SHP",
                    "zone": "FXX",
                    "stored_data": "{stored data}"
                }
            ]
        }
    }
    

Si on ne précise pas de titre ou de résumé pour la donnée stockée diffusée, ce sera son nom qui sera utilisé. Les codes des langues sont ceux [ISO-639-1](https://fr.wikipedia.org/wiki/Liste_des_codes_ISO_639-1).

Dans les sous-ressources, `format`, `zone` et `resolution` (non utilisé ici) s'appuieront sur les nomenclatures pour afficher au niveau du service de téléchargement des noms plus humains. On fournit ici les `term` et les `label` seront ajoutés. Si la valeur dans la configuration ne correspond à aucun term pour le type correspondant, le label prendra la même valeur. Le SRS de la donnée stockée sera également enrichie en utilisant la nomenclature. Dans le service de téléchargement, le `term` sera convertit en URL pour respecter les specifications Atom.

Voici un exemple pour voir la nomenclature des zones :

/statics/nomenclatures

Paramètres de requêteCorps de réponse JSON

  * type = `ZONE`


    
    
        [
            {
                "type": "ZONE",
                "label": "Paris",
                "term": "D075"
            },
            {
                "type": "ZONE",
                "label": "Ain",
                "term": "D001"
            },
            {
                "type": "ZONE",
                "label": "France métropolitaine",
                "term": "FXX"
            }
        ]
    

## Publication

À ce stade, aucune information n'a été envoyée aux serveurs de téléchargement assurant la diffusion. Cette synchronisation de la configuration sur les serveurs de diffusion, représentés par le point d'accès, se fait via la création d'une offre : la publication. Elle matérialise la présence d'une configuration sur un point d'accès.

### Consultation des points de diffusion disponibles

/datastores/{datastore}

Corps de réponse JSON
    
    
    [
        {
            "name": "Service de diffusion WFS principal",
            "technical_name": "gpf-geoserver-wfs",
            "type": "WFS",
            "urls": [
                {
                    "type": "WFS",
                    "url": "https://data.geopf.fr/wfs/geoserver/ows"
                }
            ],
            "_id": "ae012611-13eb-4a18-8d04-9b7604a031cc",
            "open": true,
            "metadata_fi": "gpf-geoserver-wfs"
        },
        {
            "name": "Service de diffusion WMTS/TMS principal",
            "technical_name": "gpf-rok4-server-wmts-tms",
            "type": "WMTS-TMS",
            "urls": [
                {
                    "type": "WMTS",
                    "url": "https://data.geopf.fr/wmts"
                },
                {
                    "type": "TMS",
                    "url": "https://data.geopf.fr/tms/"
                }
            ],
            "_id": "ae032611-13eb-4a18-8d04-9b7604a031cc",
            "open": true,
            "metadata_fi": "gpf-rok4-server-wmts-tms"
        },
        {
            "name": "Service de diffusion WMS Raster principal",
            "technical_name": "gpf-rok4-server-wms-r",
            "type": "WMS-RASTER",
            "urls": [
                {
                    "type": "WMS",
                    "url": "https://data.geopf.fr/wms-r/wms"
                }
            ],
            "_id": "ae042611-13eb-4a18-8d04-9b7604a031cc",
            "open": true,
            "metadata_fi": "gpf-rok4-server-wms-r"
        },
        {
            "name": "Service de diffusion WMS Vecteur principal",
            "technical_name": "gpf-geoserver-wms-v",
            "type": "WMS-VECTOR",
            "urls": [
                {
                    "type": "WMS",
                    "url": "https://data.geopf.fr/wms-v/geoserver/ows"
                }
            ],
            "_id": "ae022611-13eb-4a18-8d04-9b7604a031cc",
            "open": true,
            "metadata_fi": "gpf-geoserver-wms-v"
        },
        {
            "name": "Service de Téléchargement principal",
            "technical_name": "gpf-download",
            "type": "DOWNLOAD",
            "urls": [
                {
                    "type": "DOWNLOAD",
                    "url": "https://data.geopf.fr/telechargement/"
                }
            ],
            "_id": "ae052611-13eb-4a18-8d04-9b7604a031cc",
            "open": true,
            "metadata_fi": "gpf-download"
        },
        {
            "name": "Service de diffusion CSW",
            "technical_name": "gpf-geonetwork",
            "type": "METADATA",
            "urls": [
                {
                    "type": "METADATA",
                    "url": "https://data.geopf.fr/csw"
                }
            ],
            "_id": "ae062611-13eb-4a18-8d04-9b7604a031cc",
            "open": true,
            "metadata_fi": "gpf-geonetwork"
        },
        {
            "name": "Service de téléchargement private",
            "technical_name": "gpf-download-private",
            "type": "DOWNLOAD",
            "urls": [
                {
                    "type": "DOWNLOAD",
                    "url": "https://data.geopf.fr/private/telechargement/"
                }
            ],
            "_id": "b5bf7ab2-8998-4829-8c80-cd2ec02e6e58",
            "open": false,
            "metadata_fi": "gpf-download-private"
        },
        {
            "name": "Service de diffusion WFS privé",
            "technical_name": "gpf-geoserver-wfs-private",
            "type": "WFS",
            "urls": [
                {
                    "type": "WFS",
                    "url": "https://data.geopf.fr/private/wfs/"
                }
            ],
            "_id": "d02feec9-1169-403f-bfc3-7ba6d6015ed4",
            "open": false,
            "metadata_fi": "gpf-geoserver-wfs-private"
        },
        {
            "name": "Service de diffusion WMS Vecteur privé",
            "technical_name": "gpf-geoserver-wms-v-private",
            "type": "WMS-VECTOR",
            "urls": [
                {
                    "type": "WMS",
                    "url": "https://data.geopf.fr/private/wms-v/"
                }
            ],
            "_id": "519c8bb1-9b7f-414a-9850-1a73dfd467ed",
            "open": false,
            "metadata_fi": "gpf-geoserver-wms-v-private"
        },
        {
            "name": "Service de diffusion WMS Raster privé",
            "technical_name": "gpf-rok4-server-wms-r-private",
            "type": "WMS-RASTER",
            "urls": [
                {
                    "type": "WMS",
                    "url": "https://data.geopf.fr/private/wms-r/"
                }
            ],
            "_id": "66866100-48eb-4340-bbc9-f5c7d9707928",
            "open": false,
            "metadata_fi": "gpf-rok4-server-wms-r-private"
        },
        {
            "name": "Service de diffusion WMTS/TMS privé",
            "technical_name": "gpf-rok4-server-wmts-tms-private",
            "type": "WMTS-TMS",
            "urls": [
                {
                    "type": "TMS",
                    "url": "https://data.geopf.fr/private/tms/"
                },
                {
                    "type": "WMTS",
                    "url": "https://data.geopf.fr/private/wmts/"
                }
            ],
            "_id": "7e0a92d1-8213-4ce0-8903-eb4c305a1849",
            "open": false,
            "metadata_fi": "gpf-rok4-server-wmts-tms-private"
        }
    ]
    

C'est le point d'accès de type DOWNLOAD qui va nous intéresser.

Formats Cloud optimized

Pour publier des données dans des formats "cloud optimized" (COG, GeoParquet, PMTiles, FlatGeoBuf, COPC...), un point d'accès de téléchargement est d'avantage adapté, celui "chunk". Il est dimensionné pour gérer plus de requête de lecture de plus petite taille. N'hésitez pas demander son affectation à votre entrepôt si vous travaillez avec ces formats.

### Création de l'offre

/datastores/{datastore}/configurations/{configuration}/offerings

Corps de requête JSONCorps de réponse JSON
    
    
    {
        "endpoint": "ae052611-13eb-4a18-8d04-9b7604a031cc",
        "open": true
    }
    
    
    
    {
        "open": true,
        "available": true,
        "layer_name": "limites_administratives",
        "type": "DOWNLOAD",
        "status": "PUBLISHED",
        "configuration": {
            "name": "Limites administratives",
            "status": "PUBLISHED",
            "_id": "{configuration}"
        },
        "endpoint": {
            "name": "gpf-download",
            "_id": "ae052611-13eb-4a18-8d04-9b7604a031cc"
        },
        "urls": [],
        "_id": "{offering}"
    }
    

## Consultation du service de téléchargement

En consultant les [capacités du service de téléchargement](https://data.geopf.fr/telechargement/capabilities), on retrouve notre couche (on demande ici la réponse en JSON, c'est le format XML Atom par défaut). On va également filtrer sur nos valeurs spécifiques pour n'avoir que notre résultat.

https://data.geopf.fr/telechargement/capabilities

Paramètres de requêteEn-tête de requêteCorps de réponse JSON

  * crs = `https://www.opengis.net/def/crs/EPSG/0/2154`
  * zone = `FXX`
  * format = `SHP`
  * editionDateTo = `2024-09-16`



  * Accept = `application/json`


    
    
    {
        "georssNs": "http://www.georss.org/georss",
        "gpfDlNs": "https://data.geopf.fr/annexes/ressources/xsd/gpf_dl.xsd",
        "xmlns": "http://www.w3.org/2005/Atom",
        "inspireDlsNs": "http://inspire.ec.europa.eu/schemas/inspire_dls/1.0",
        "lang": "en",
        "page": 1,
        "pagesize": 20,
        "pagecount": 1,
        "totalentries": 1,
        "title": "Public Download Service of Géoplateforme",
        "subtitle": "This Download Service allows you to download public datasources",
        "id": "https://data.geopf.fr/telechargement/capabilities",
        "rights": "Conditions Générales d'Utilisation disponibles ici : https://cartes.gouv.fr/cgu-licences",
        "updated": "2024-09-17",
        "author":
        {
            "name": "Institut National de l'Information Géographique et Forestière",
            "email": "geoplateforme@ign.fr"
        },
        "link":
        [
            {
                "href": "https://data.geopf.fr/telechargement/capabilities",
                "rel": "self",
                "type": "application/atom+xml",
                "title": "This document",
                "bbox": null
            },
            {
                "href": "https://data.geopf.fr/telechargement/capabilities?lang=en",
                "hreflang": "en",
                "rel": "alternate",
                "type": "application/atom+xml",
                "title": "Public Download Service of Géoplateforme",
                "bbox": null
            },
            {
                "href": "https://data.geopf.fr/telechargement/capabilities?lang=fr",
                "hreflang": "fr",
                "rel": "alternate",
                "type": "application/atom+xml",
                "title": "Service de téléchargement public de la Géoplateforme",
                "bbox": null
            },
            {
                "href": "https://data.geopf.fr/telechargement/capabilities",
                "rel": "up",
                "type": "application/atom+xml",
                "bbox": null
            }
        ],
        "entry":
        [
            {
                "title": "Administrative units",
                "spatialDatasetIdentifierCode": "Admin Express",
                "link":
                [
                    {
                        "href": "https://data.geopf.fr/telechargement/resource/limites_administratives",
                        "rel": "alternate",
                        "type": "application/atom+xml",
                        "bbox": null
                    }
                ],
                "id": "https://data.geopf.fr/telechargement/resource/limites_administratives",
                "updated": "2024-09-16",
                "content": "Limites administratives, au format Shapefile, sur la France métropolitaine",
                "polygon": "-5.33254008 41.20611066 9.85432008 41.20611066 9.85432008 51.20324649 -5.33254008 51.20324649 -5.33254008 41.20611066",
                "editionDateStart": "2022-09-30",
                "editionDateEnd": "2022-09-30",
                "category":
                [
                    {
                        "term": "https://www.opengis.net/def/crs/EPSG/0/2154",
                        "label": "RGF93 v1 / Lambert-93 -- France"
                    }
                ],
                "zone":
                [
                    {
                        "term": "FXX",
                        "label": "France métropolitaine"
                    }
                ],
                "format":
                [
                    {
                        "term": "SHP",
                        "label": "Shapefile"
                    }
                ],
                "resolution":
                [
                    {
                        "term": "1m",
                        "label": "Précision à 1 mètres"
                    }
                ]
            }
        ]
    }
    

Si on veut avoir le contenu de notre ressource de téléchargement `limites_administratives`, on suit [le lien dans l'entrée](https://data.geopf.fr/telechargement/resource/limites_administratives), c'est à dire les sous-ressources. Dans notre cas, on a une seule sous ressource, `departements`.

https://data.geopf.fr/telechargement/resource/limites_administratives

En-tête de requêteCorps de réponse JSON

  * Accept = `application/json`


    
    
    {
        "georssNs": "http://www.georss.org/georss",
        "gpfDlNs": "https://data.geopf.fr/annexes/ressources/xsd/gpf_dl.xsd",
        "xmlns": "http://www.w3.org/2005/Atom",
        "inspireDlsNs": "http://inspire.ec.europa.eu/schemas/inspire_dls/1.0",
        "lang": "en",
        "page": 1,
        "pagesize": 10,
        "pagecount": 1,
        "totalentries": 1,
        "title": "Administrative units",
        "subtitle": "Limites administratives, au format Shapefile, sur la France métropolitaine",
        "id": "https://data.geopf.fr/telechargement/resource/limites_administratives",
        "updated": "2024-09-16",
        "spatialDatasetIdentifierCode": "Admin Express",
        "link":
        [
            {
                "href": "https://data.geopf.fr/telechargement/resource/limites_administratives?lang=en",
                "hreflang": "en",
                "rel": "alternate",
                "type": "application/atom+xml",
                "title": "Administrative units",
                "bbox": null
            },
            {
                "href": "https://data.geopf.fr/telechargement/resource/limites_administratives?lang=fr",
                "hreflang": "fr",
                "rel": "alternate",
                "type": "application/atom+xml",
                "title": "Limites administratives",
                "bbox": null
            },
            {
                "href": "https://data.geopf.fr/telechargement/resource/limites_administratives",
                "rel": "self",
                "type": "application/atom+xml",
                "title": "This document",
                "bbox": null
            },
            {
                "href": "https://data.geopf.fr/telechargement/capabilities",
                "rel": "up",
                "type": "application/atom+xml",
                "bbox": null
            }
        ],
        "entry":
        [
            {
                "title": "Données départementales",
                "link":
                [
                    {
                        "href": "https://data.geopf.fr/telechargement/resource/limites_administratives/departements",
                        "rel": "alternate",
                        "type": "application/atom+xml",
                        "title": "Données départementales",
                        "bbox": "-5.33254008 41.20611066 9.85432008 51.20324649"
                    }
                ],
                "id": "https://data.geopf.fr/telechargement/resource/limites_administratives/departements",
                "updated": "2024-09-16",
                "content": "Départements et limites départementales, au format Shapefile, sur la France métropolitaine",
                "polygon": "9.09172851 42.89115936 9.12915131 43.2450106 9.61454396 43.37599636 9.85432008 42.28024058 9.59263351 41.27883529 9.17895507 41.20611066 8.57606386 41.52172702 8.37515061 42.18155293 8.60679353 42.88081313 9.09172851 42.89115936 -5.11714547 48.69143916 -5.11904295 48.7036136 -3.53090169 49.07144036 -2.05981435 48.92176625 -2.39266145 49.61836715 -1.44304026 49.97518135 -0.28790953 49.71802866 1.16554867 50.22539848 1.2106405 51.10547173 2.68327037 51.20324649 4.36996119 50.39029281 5.12108028 50.52630512 5.36566614 50.02071857 7.44864671 49.52189837 8.75795607 49.11102171 8.46599244 48.64627595 7.99941283 47.83257925 7.55725079 47.1390034 6.89685602 46.70928797 7.3839402 46.33582437 7.64872697 45.69932199 7.59199086 44.80571585 8.1070412 44.4026185 8.14445803 43.87311823 7.46554269 43.21632897 6.55534602 42.85813836 5.32652298 42.92854218 4.0485537 43.1811621 3.59296671 42.79301466 3.90045719 42.26485025 3.25766156 42.10938675 0.45381917 42.38499265 -2.10506004 43.12661715 -1.60510675 43.99536685 -1.49342246 45.59517123 -2.88176427 46.80885968 -4.86703502 47.65004168 -5.33254008 48.29493047 -5.11714547 48.69143916",
                "editionDate": "2022-09-30",
                "category":
                [
                    {
                        "term": "https://www.opengis.net/def/crs/EPSG/0/2154",
                        "label": "RGF93 v1 / Lambert-93 -- France"
                    }
                ],
                "zone":
                [
                    {
                        "term": "FXX",
                        "label": "France métropolitaine"
                    }
                ],
                "format":
                [
                    {
                        "term": "SHP",
                        "label": "Shapefile"
                    }
                ],
                "resolution":
                [
                    {
                        "term": "1m",
                        "label": "Précision à 1 mètres"
                    }
                ]
            }
        ]
    }
    

Pour connaître les fichiers téléchargeables, on va pouvoir demander le contenu de la sous ressource en suivant le [lien de l'entrée](https://data.geopf.fr/telechargement/resource/limites_administratives/departements).

https://data.geopf.fr/telechargement/resource/limites_administratives/departements

En-tête de requêteCorps de réponse JSON

  * Accept = `application/json`


    
    
    {
        "georssNs": "http://www.georss.org/georss",
        "gpfDlNs": "https://data.geopf.fr/annexes/ressources/xsd/gpf_dl.xsd",
        "xmlns": "http://www.w3.org/2005/Atom",
        "inspireDlsNs": "http://inspire.ec.europa.eu/schemas/inspire_dls/1.0",
        "lang": "en",
        "page": 1,
        "pagesize": 10,
        "pagecount": 1,
        "totalentries": 10,
        "title": "Données départementales",
        "subtitle": "Départements et limites départementales, au format Shapefile, sur la France métropolitaine",
        "id": "https://data.geopf.fr/telechargement/resource/limites_administratives/departements",
        "updated": "2024-09-16",
        "zone":
        {
            "term": "FXX",
            "label": "France métropolitaine"
        },
        "format":
        {
            "term": "SHP",
            "label": "Shapefile"
        },
        "resolution":
        {
            "term": "1m",
            "label": "Précision à 1 mètres"
        },
        "editionDate": "2022-09-30",
        "link":
        [
            {
                "href": "https://data.geopf.fr/telechargement/resource/limites_administratives/departements?lang=fr",
                "hreflang": "fr",
                "rel": "alternate",
                "type": "application/atom+xml",
                "title": "Données départementales",
                "bbox": null
            },
            {
                "href": "https://data.geopf.fr/telechargement/resource/limites_administratives/departements",
                "rel": "self",
                "type": "application/atom+xml",
                "title": "This document",
                "bbox": null
            },
            {
                "href": "https://data.geopf.fr/telechargement/resource/limites_administratives",
                "rel": "up",
                "type": "application/atom+xml",
                "bbox": null
            }
        ],
        "entry":
        [
            {
                "link":
                [
                    {
                        "href": "https://data.geopf.fr/telechargement/download/limites_administratives/departements/DEPARTEMENT.cpg",
                        "rel": "alternate",
                        "type": "image/x-cpg",
                        "length": 6,
                        "bbox": null
                    }
                ],
                "id": "https://data.geopf.fr/telechargement/download/limites_administratives/departements/DEPARTEMENT.cpg",
                "content": "ed16c6bc54359dade2e7fafa83607f16",
                "category":
                [
                    {
                        "term": "https://www.opengis.net/def/crs/EPSG/0/2154",
                        "label": "RGF93 v1 / Lambert-93 -- France"
                    }
                ],
                "mime_type":
                [
                    "image/x-cpg"
                ]
            },
            {
                "link":
                [
                    {
                        "href": "https://data.geopf.fr/telechargement/download/limites_administratives/departements/DEPARTEMENT.dbf",
                        "rel": "alternate",
                        "type": "application/octet-stream",
                        "length": 17186,
                        "bbox": null
                    }
                ],
                "id": "https://data.geopf.fr/telechargement/download/limites_administratives/departements/DEPARTEMENT.dbf",
                "content": "d9c1ff8f8980daa8f9b969a429987673",
                "category":
                [
                    {
                        "term": "https://www.opengis.net/def/crs/EPSG/0/2154",
                        "label": "RGF93 v1 / Lambert-93 -- France"
                    }
                ],
                "mime_type":
                [
                    "application/octet-stream"
                ]
            },
            {
                "link":
                [
                    {
                        "href": "https://data.geopf.fr/telechargement/download/limites_administratives/departements/DEPARTEMENT.prj",
                        "rel": "alternate",
                        "type": "image/x-prj",
                        "length": 449,
                        "bbox": null
                    }
                ],
                "id": "https://data.geopf.fr/telechargement/download/limites_administratives/departements/DEPARTEMENT.prj",
                "content": "a125df3368127b8203a6c823c4e2b881",
                "category":
                [
                    {
                        "term": "https://www.opengis.net/def/crs/EPSG/0/2154",
                        "label": "RGF93 v1 / Lambert-93 -- France"
                    }
                ],
                "mime_type":
                [
                    "image/x-prj"
                ]
            },
            {
                "link":
                [
                    {
                        "href": "https://data.geopf.fr/telechargement/download/limites_administratives/departements/DEPARTEMENT.shp",
                        "rel": "alternate",
                        "type": "application/x-shapefile",
                        "length": 3125208,
                        "bbox": null
                    }
                ],
                "id": "https://data.geopf.fr/telechargement/download/limites_administratives/departements/DEPARTEMENT.shp",
                "content": "ab9b820b4c50936862f45f21eb434d82",
                "category":
                [
                    {
                        "term": "https://www.opengis.net/def/crs/EPSG/0/2154",
                        "label": "RGF93 v1 / Lambert-93 -- France"
                    }
                ],
                "mime_type":
                [
                    "application/x-shapefile"
                ]
            },
            {
                "link":
                [
                    {
                        "href": "https://data.geopf.fr/telechargement/download/limites_administratives/departements/DEPARTEMENT.shx",
                        "rel": "alternate",
                        "type": "application/octet-stream",
                        "length": 868,
                        "bbox": null
                    }
                ],
                "id": "https://data.geopf.fr/telechargement/download/limites_administratives/departements/DEPARTEMENT.shx",
                "content": "1b4b27aa51e8c981c80fc009c5612f36",
                "category":
                [
                    {
                        "term": "https://www.opengis.net/def/crs/EPSG/0/2154",
                        "label": "RGF93 v1 / Lambert-93 -- France"
                    }
                ],
                "mime_type":
                [
                    "application/octet-stream"
                ]
            },
            {
                "link":
                [
                    {
                        "href": "https://data.geopf.fr/telechargement/download/limites_administratives/departements/LIMITE_DEPARTEMENT.cpg",
                        "rel": "alternate",
                        "type": "image/x-cpg",
                        "length": 6,
                        "bbox": null
                    }
                ],
                "id": "https://data.geopf.fr/telechargement/download/limites_administratives/departements/LIMITE_DEPARTEMENT.cpg",
                "content": "ed16c6bc54359dade2e7fafa83607f16",
                "category":
                [
                    {
                        "term": "https://www.opengis.net/def/crs/EPSG/0/2154",
                        "label": "RGF93 v1 / Lambert-93 -- France"
                    }
                ],
                "mime_type":
                [
                    "image/x-cpg"
                ]
            },
            {
                "link":
                [
                    {
                        "href": "https://data.geopf.fr/telechargement/download/limites_administratives/departements/LIMITE_DEPARTEMENT.dbf",
                        "rel": "alternate",
                        "type": "application/octet-stream",
                        "length": 2039048,
                        "bbox": null
                    }
                ],
                "id": "https://data.geopf.fr/telechargement/download/limites_administratives/departements/LIMITE_DEPARTEMENT.dbf",
                "content": "d5b48ce0035f521dba949d29cf6c7770",
                "category":
                [
                    {
                        "term": "https://www.opengis.net/def/crs/EPSG/0/2154",
                        "label": "RGF93 v1 / Lambert-93 -- France"
                    }
                ],
                "mime_type":
                [
                    "application/octet-stream"
                ]
            },
            {
                "link":
                [
                    {
                        "href": "https://data.geopf.fr/telechargement/download/limites_administratives/departements/LIMITE_DEPARTEMENT.prj",
                        "rel": "alternate",
                        "type": "image/x-prj",
                        "length": 449,
                        "bbox": null
                    }
                ],
                "id": "https://data.geopf.fr/telechargement/download/limites_administratives/departements/LIMITE_DEPARTEMENT.prj",
                "content": "a125df3368127b8203a6c823c4e2b881",
                "category":
                [
                    {
                        "term": "https://www.opengis.net/def/crs/EPSG/0/2154",
                        "label": "RGF93 v1 / Lambert-93 -- France"
                    }
                ],
                "mime_type":
                [
                    "image/x-prj"
                ]
            },
            {
                "link":
                [
                    {
                        "href": "https://data.geopf.fr/telechargement/download/limites_administratives/departements/LIMITE_DEPARTEMENT.shp",
                        "rel": "alternate",
                        "type": "application/x-shapefile",
                        "length": 2527748,
                        "bbox": null
                    }
                ],
                "id": "https://data.geopf.fr/telechargement/download/limites_administratives/departements/LIMITE_DEPARTEMENT.shp",
                "content": "afd8b8f3d13da008b5305fe49e8ccab3",
                "category":
                [
                    {
                        "term": "https://www.opengis.net/def/crs/EPSG/0/2154",
                        "label": "RGF93 v1 / Lambert-93 -- France"
                    }
                ],
                "mime_type":
                [
                    "application/x-shapefile"
                ]
            },
            {
                "link":
                [
                    {
                        "href": "https://data.geopf.fr/telechargement/download/limites_administratives/departements/LIMITE_DEPARTEMENT.shx",
                        "rel": "alternate",
                        "type": "application/octet-stream",
                        "length": 72596,
                        "bbox": null
                    }
                ],
                "id": "https://data.geopf.fr/telechargement/download/limites_administratives/departements/LIMITE_DEPARTEMENT.shx",
                "content": "bcef9e262f77e5b1dcfe1eed5e14f935",
                "category":
                [
                    {
                        "term": "https://www.opengis.net/def/crs/EPSG/0/2154",
                        "label": "RGF93 v1 / Lambert-93 -- France"
                    }
                ],
                "mime_type":
                [
                    "application/octet-stream"
                ]
            }
        ]
    }
    

On retrouve nos 10 fichiers, avec leur taille et leur signature MD5, téléchargeables :

  * [LIMITE_DEPARTEMENT.dbf](https://data.geopf.fr/telechargement/download/limites_administratives/departements/LIMITE_DEPARTEMENT.dbf)
  * [LIMITE_DEPARTEMENT.prj](https://data.geopf.fr/telechargement/download/limites_administratives/departements/LIMITE_DEPARTEMENT.prj)
  * [LIMITE_DEPARTEMENT.cpg](https://data.geopf.fr/telechargement/download/limites_administratives/departements/LIMITE_DEPARTEMENT.cpg)
  * [LIMITE_DEPARTEMENT.shp](https://data.geopf.fr/telechargement/download/limites_administratives/departements/LIMITE_DEPARTEMENT.shp)
  * [LIMITE_DEPARTEMENT.shx](https://data.geopf.fr/telechargement/download/limites_administratives/departements/LIMITE_DEPARTEMENT.shx)
  * [DEPARTEMENT.dbf](https://data.geopf.fr/telechargement/download/limites_administratives/departements/DEPARTEMENT.dbf)
  * [DEPARTEMENT.prj](https://data.geopf.fr/telechargement/download/limites_administratives/departements/DEPARTEMENT.prj)
  * [DEPARTEMENT.cpg](https://data.geopf.fr/telechargement/download/limites_administratives/departements/DEPARTEMENT.cpg)
  * [DEPARTEMENT.shp](https://data.geopf.fr/telechargement/download/limites_administratives/departements/DEPARTEMENT.shp)
  * [DEPARTEMENT.shx](https://data.geopf.fr/telechargement/download/limites_administratives/departements/DEPARTEMENT.shx)


