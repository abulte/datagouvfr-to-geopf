source: https://geoplateforme.github.io/tutoriels/production/raster/mnt/publication_wms/

[Diffusion](../../../tags/#tag:diffusion) [Donnée raster](../../../tags/#tag:donnée-raster) [Fichier de style](../../../tags/#tag:fichier-de-style) [MNT](../../../tags/#tag:mnt) [WMS](../../../tags/#tag:wms)

# Publication en WMS

## Mise en place d'un style

Les données MNT ont un format particulier : les images ont un unique canal, avec des valeurs flottantes. Les flux WMS et WMTS vont permettre de récupérer la donnée brute (pour d'éventuels calculs), mais l'affichage peut être compliqué.

En WMS, on va permettre la demande de donnée symbolisée, en appliquant des teintes hypsométriques. Afin que le consommateur des flux puisse connaître les caractéristiques de ces teintes, nous allons mettre en ligne la légende, qui sera référencée dans le style via son URL.

Nous allons partir sur une représentation qui, sur la donnée en exemple, donne le résultat suivant.

Avec la légende :

### Hébergement de la légende sous forme d'annexe

Pour obtenir une URL publique pointant sur notre légende, nous allons la téléverser dans l'entrepôt sous forme d'annexe, en en demandant la publication immédiate.

`<hypso_legende.png>`

/datastores/{datastore}/annexes

Corps de requête Multipart

  * file = `<hypso_legende.png>`
  * paths = "legendes/teintes_hypsometriques.png"
  * published = `true`
  * labels = "legende"



Le renseignement d'un label va permettre de plus facilement retrouver et publier / dépublier les annexes.

La légende est maintenant accessible à l'URL `https://data.geopf.fr/annexes/{technical_name}/legendes/teintes_hypsometriques.png`.

### Téléversement du style à destination du serveur WMS

Le style permettant au serveur WMS d'appliquer ces teintes sur de la donnée MNT est le suivant :

Contenu de hypso.json
    
    
    {
        "identifier": "hypsometrique",
        "title": "Teintes hypsométriques",
        "abstract": "Teintes hypsométriques",
        "keywords": ["MNT"],
        "legend": {
            "format": "image/png",
            "url": "https://data.geopf.fr/annexes/{technical_name}/legendes/teintes_hypsometriques.png",
            "height": 118,
            "width": 87,
            "min_scale_denominator": 0,
            "max_scale_denominator": 10000000
        },
        "palette": {
            "max_value": 3.40282e+38,
            "rgb_continuous": true,
            "alpha_continuous": true,
            "colours": [
                { "value": -100000, "red": 0, "green": 0, "blue": 0, "alpha": 0 },
                { "value": -98000, "red": 0, "green": 0, "blue": 0, "alpha": 0 },
                { "value": 0, "red": 161, "green": 225, "blue": 143, "alpha": 255 },
                { "value": 500, "red": 48, "green": 164, "blue": 16, "alpha": 255 },
                { "value": 1500, "red": 237, "green": 239, "blue": 0, "alpha": 255 },
                { "value": 2000, "red": 225, "green": 0, "blue": 0, "alpha": 255 },
                { "value": 2500, "red": 0, "green": 0, "blue": 0, "alpha": 255 },
                { "value": 4000, "red": 255, "green": 255, "blue": 255, "alpha": 255 }
            ]
        }
    }
    

On y précise bien les informations sur la légende associée. Le champ `identifier` sera l'identifiant public que les consommateurs du WMS pourront préciser dans les requêtes pour demander l'utilisation de ce style.

`hypso.json`

/datastores/{datastore}/statics

Corps de requête MultipartCorps de réponse JSON

  * file = `<hypso.json>`
  * type = "ROK4-STYLE"
  * name = "Teintes hypsométriques"


    
    
    {
        "name": "Teintes hypsométriques",
        "type": "ROK4-STYLE",
        "_id": "{style hypso}",
        "type_infos": {
            "identifier": "hypsometrique",
            "legend_url": "https://data.geopf.fr/annexes/{technical_name}/legendes/teintes_hypsometriques.png"
        }
    }
    

Pour que la même couche puisse être aussi interrogée au format brut, nous allons déposer un style qui ne modifie pas la donnée

Contenu de normal.json
    
    
    {
        "identifier": "normal",
        "title": "Données brutes",
        "abstract": "Données brutes, sans transformation",
        "keywords": ["MNT"],
        "legend": {
            "format": "image/jpeg",
            "url": "https://data.geopf.fr/annexes/ressources/legendes/LEGEND.jpg",
            "height": 69,
            "width": 280,
            "min_scale_denominator": 0,
            "max_scale_denominator": 10000000
        }
    }
    

On y précise bien les informations sur la légende associée. Le champ `identifier` sera l'identifiant public que les consommateurs du WMS pourront préciser dans les requêtes pour demander l'utilisation de ce style. Une même couche ne peut pas avoir deux styles qui ont le même `identifier`.

`normal.json`

/datastores/{datastore}/statics

Corps de requête MultipartCorps de réponse JSON

  * file = `<normal.json>`
  * type = "ROK4-STYLE"
  * name = "Données brutes"


    
    
    {
        "name": "Données brutes",
        "type": "ROK4-STYLE",
        "_id": "{style normal}",
        "type_infos": {
            "identifier": "normal",
            "legend_url": "https://data.geopf.fr/annexes/ressources/legendes/LEGEND.jpg"
        }
    }
    

## Configuration de la diffusion

Nous allons publier la donnée selon une couche, avec les deux styles. Le style mis en premier sera celui appliqué par défaut si aucun style n'est précisé dans la requête GetMap.

/datastores/{datastore}/configurations

Corps de requête JSON
    
    
    {
        "type": "WMS-RASTER",
        "name": "MNT LidarHD données brutes",
        "layer_name": "lidarhd",
        "type_infos": {
            "title": "MNT LidarHD",
            "abstract": "MNT LidarHD brut",
            "keywords": [
                "MNT", "LidarHD"
            ],
            "styles": [
                "{style normal}",
                "{style hypso}"
            ],
            "interpolation": "NEAREST-NEIGHBOUR",
            "used_data": [
                {
                    "bottom_level": "18",
                    "top_level": "0",
                    "stored_data": "{stored data MNT}"
                }
            ]
        },
        "getfeatureinfo": {
            "stored_data": true
        }
    }
    

## Envoi sur les services de diffusion

Seule la création d'une offre sur un point d'accès (publication) permet d'envoyer les informations de configuration au serveurs de diffusion.

### Consultation des points de diffusion disponibles

/datastores/{datastore}

Corps de réponse JSON (champ `endpoints`)
    
    
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
    

### Publication

/datastores/{datastore}/configurations/{configuration wms lidarhd}/offerings

Corps de requête JSON
    
    
    {
        "endpoint": "ae042611-13eb-4a18-8d04-9b7604a031cc",
        "open": true
    }
    

On peut vérifier la présence de notre couche `lidarhd` dans le [getCapabilities du service](https://data.geopf.fr/wms-r?REQUEST=GetCapabilities&SERVICE=WMS&VERSION=1.3.0), avec la présence des deux styles.

Dans QGis, on retrouve la légende déposée sous forme d'annexe.
