source: https://geoplateforme.github.io/tutoriels/production/hautniveau/validation/api/

[Contrôle des données](../../../tags/#tag:contrôle-des-données) [Donnée vecteur](../../../tags/#tag:donnée-vecteur) [Service avancé](../../../tags/#tag:service-avancé)

# API validation

Cette API permet de faire passer une validation (et une éventuelle normalisation des données) sur un jeu de donnée téléversé en dehors de tout espace de travail.

## Outil de requête

Une [collection Bruno](https://github.com/Geoplateforme/clients-configurations/tree/master/bruno/diffusion/validation) est préconfigurée avec les requêtes de ce tutoriel. Vous pouvez lire [cette documentation](https://github.com/Geoplateforme/clients-configurations?tab=readme-ov-file#collections-bruno) pour voir comment l'utiliser.

## Créer une nouvelle validation

La création d'une validation passe par le téléversement des données à valider sous forme d'un fichier ZIP. Ce tutoriel utilise le jeu de données [BrestMetropole_20220216-2154.zip](../../../assets/data/BrestMetropole_20220216-2154.zip). Cette archive contient un fichier GML. On va pouvoir dès le téléversement préciser le temps de rétention de la donnée à valider avant de la supprimer du serice (nombre à préciser en jours, 15 jours par défaut)

https://data.geopf.fr/validation/api/validations

Paramètres de requêteCorps de requête MultipartCorps de réponse JSON

  * retention = `1`



  * file = `<BrestMetropole_20220216-2154.zip>`


    
    
    {
        "validationID": "{validation}",
        "status": "created",
        "dataset_name": "BrestMetropole_20220216-2154.zip",
        "arguments": {},
        "created": "2025-10-20T08:09:14.477480241Z",
        "message": "Validation créée"
    }
    

Je peux maintenant retrouver ma validation via l'appel suivant. Cette API permet également de voir toutes les validations passées, est paginée et est filtrable selon le nom du jeu de donnée et du statut de la validation (**à mettre en majuscule dans le paramètre de requête, contrairement à la valeur dans les réponses**).

https://data.geopf.fr/validation/api/validations

Corps de réponse JSON
    
    
    {
        "validations": [
            {
                "validationID": "{validation}",
                "status": "created",
                "dataset_name": "BrestMetropole_20220216-2154.zip",
                "created": "2025-10-20T08:09:14.477480Z"
            }
        ],
        "links": [
            {
                "rel": "self",
                "type": "application/json",
                "title": "Liste des validations",
                "href": "/validations"
            }
        ]
    }
    

Il est également possible d'avoir le détail d'une validation via l'appel suivant :

https://data.geopf.fr/validation/api/validations/{validation}

Corps de réponse JSON
    
    
    {
        "validationID": "{validation}",
        "status": "created",
        "dataset_name": "BrestMetropole_20220216-2154.zip",
        "arguments": {},
        "created": "2025-10-20T08:09:14.477480Z",
        "message": "Validation créée"
    }
    

## Lancer une validation

À ce stade, seul le téléversement des données a été fait, aucune validation n'est en cours. Pour déclencher cette validation, il est nécessaire d'en préciser les paramètre. Le paramètre `normalize` permet de demander une modification du jeu de donnée pour le mettre en conformité (on pourra télécharger le résultat de cette normalisation). Le champ `model` permet de préciser le modèle de conformité à appliquer et doit être une URL accessible depuis la Géoplateforme.

https://data.geopf.fr/validation/api/validations/{validation}

Corps de requête JSONCorps de réponse JSON
    
    
    {
        "model": "https://ignf.github.io/validator/validator-core/src/test/resources/config-json/CNIG_PCRS_v2.0/document.json",
        "srs": "EPSG:2154",
        "max-errors": 30,
        "normalize": true,
        "encoding": "UTF-8"
    }
    
    
    
    {
        "validationID": "{validation}",
        "status": "progress",
        "dataset_name": "BrestMetropole_20220216-2154.zip",
        "arguments": {
            "model": "https://ignf.github.io/validator/validator-core/src/test/resources/config-json/CNIG_PCRS_v2.0/document.json",
            "srs": "EPSG:2154",
            "max-errors": 30,
            "normalize": true,
            "encoding": "UTF-8"
        },
        "created": "2025-10-20T08:09:14.477480Z",
        "message": "Validation lancée",
        "started": "2025-10-20T08:22:35.034392Z"
    }
    

## Consulter le résultat d'une validation

Lorsque la validation est terminée, nous pouvons voir d'avantage de détails dessus :

https://data.geopf.fr/validation/api/validations/{validation}

Corps de réponse JSON
    
    
    {
        "validationID": "b90028d6-1d1e-4c10-a6a3-3ad9f5818032",
        "status": "success",
        "dataset_name": "BrestMetropole_20220216-2154.zip",
        "arguments": {
            "model": "https://ignf.github.io/validator/validator-core/src/test/resources/config-json/CNIG_PCRS_v2.0/document.json",
            "srs": "EPSG:2154",
            "max-errors": 30,
            "normalize": true,
            "encoding": "UTF-8"
        },
        "created": "2025-10-20T08:09:14.477480Z",
        "message": "Validation terminée",
        "started": "2025-10-20T08:22:35.034392Z",
        "finished": "2025-10-20T08:25:29.868189Z",
        "results": [
            {
                "id": "",
                "code": "VALIDATOR_INFO",
                "file": "",
                "level": "INFO",
                "scope": "DIRECTORY",
                "message": "Validation avec le modèle : CNIG_PCRS_v2.0",
                "attribute": "",
                "featureId": "",
                "fileModel": "",
                "featureBbox": null,
                "documentModel": "",
                "errorGeometry": null
            },
            {
                "id": "",
                "code": "VALIDATOR_INFO",
                "file": "",
                "level": "INFO",
                "scope": "DIRECTORY",
                "message": "Version du validateur : 4.4.8-SNAPSHOT",
                "attribute": "",
                "featureId": "",
                "fileModel": "",
                "featureBbox": null,
                "documentModel": "",
                "errorGeometry": null
            },
            {
                "id": "",
                "code": "VALIDATOR_INFO",
                "file": "",
                "level": "INFO",
                "scope": "DIRECTORY",
                "message": "Version GDAL utilisée : GDAL 3.8.4, released 2024/02/08",
                "attribute": "",
                "featureId": "",
                "fileModel": "",
                "featureBbox": null,
                "documentModel": "",
                "errorGeometry": null
            },
            {
                "id": "",
                "code": "VALIDATOR_PROJECTION_INFO",
                "file": "BrestMetropole_20220216-2154/",
                "level": "INFO",
                "scope": "DIRECTORY",
                "message": "La projection EPSG:2154 (http://www.opengis.net/def/crs/EPSG/0/2154) est utilisée pour la validation",
                "attribute": "",
                "featureId": "",
                "fileModel": "",
                "featureBbox": null,
                "documentModel": "CNIG_PCRS_v2.0",
                "errorGeometry": null
            },
            {
                "id": "",
                "code": "MULTITABLE_UNEXPECTED",
                "file": "999-48-00164-01454-19-B-18.gml",
                "level": "WARNING",
                "scope": "DIRECTORY",
                "message": "La table 'plancorpsruesimplifie' n'est pas prévue dans le modèle de validation.",
                "attribute": "",
                "featureId": "",
                "fileModel": "DONNEES",
                "featureBbox": null,
                "documentModel": "CNIG_PCRS_v2.0",
                "errorGeometry": null
            },
            {
                "id": "",
                "code": "MULTITABLE_UNEXPECTED",
                "file": "999-48-00164-01454-19-B-18.gml",
                "level": "WARNING",
                "scope": "DIRECTORY",
                "message": "La table 'plancorpsruesimplifie_featuremember' n'est pas prévue dans le modèle de validation.",
                "attribute": "",
                "featureId": "",
                "fileModel": "DONNEES",
                "featureBbox": null,
                "documentModel": "CNIG_PCRS_v2.0",
                "errorGeometry": null
            }
        ]
    }
    

Le statut de la validation signifie seulement que celle ci a pu se dérouler, et non qu'elle n'a pas détecté d'erreur. Pour avoir ces informations "métier", le champ `result` est présent : le niveau de log de l'élément va nous dire si des non-respects ont été rencontrés. Nous avons ici deux warnings, concernant des tables non prévues.

Ces résultats "métier" peuvent être télécharger au format CSV via la route :

https://data.geopf.fr/validation/api/validations/{validation}/results.csv

Corps de réponse CSV
    
    
        id,code,file,level,scope,message,attribute,featureId,fileModel,featureBbox,documentModel,errorGeometry
        ,VALIDATOR_INFO,,INFO,DIRECTORY,"Validation avec le modèle : CNIG_PCRS_v2.0",,,,,,
        ,VALIDATOR_INFO,,INFO,DIRECTORY,"Version du validateur : 4.4.8-SNAPSHOT",,,,,,
        ,VALIDATOR_INFO,,INFO,DIRECTORY,"Version GDAL utilisée : GDAL 3.8.4, released 2024/02/08",,,,,,
        ,"VALIDATOR_PROJECTION_INFO","BrestMetropole_20220216-2154/",INFO,DIRECTORY,"La projection EPSG:2154 (http://www.opengis.net/def/crs/EPSG/0/2154) est utilisée pour la validation",,,,,CNIG_PCRS_v2.0,
        ,MULTITABLE_UNEXPECTED,"999-48-00164-01454-19-B-18.gml",WARNING,DIRECTORY,"La table 'plancorpsruesimplifie' n'est pas prévue dans le modèle de validation.",,,DONNEES,,CNIG_PCRS_v2.0,
        ,MULTITABLE_UNEXPECTED,"999-48-00164-01454-19-B-18.gml",WARNING,DIRECTORY,"La table 'plancorpsruesimplifie_featuremember' n'est pas prévue dans le modèle de validation.",,,DONNEES,,CNIG_PCRS_v2.0,
    

Il est aussi possible de voir les logs "système" de la validation (utile notamment si la validation a un statut en échec). La réponse est paginée, avec les paramètres `page` et `limit` :

https://data.geopf.fr/validation/api/validations/{validation}/logs

Corps de réponse JSON
    
    
    [
        "2025-10-20 08:23:13,535INFO||gpf-validator-script||7||Ouverture du fichier de configuration",
        "2025-10-20 08:23:13,538INFO||gpf-validator-script||7||Récupération des fichiers de la livraison",
        "2025-10-20 08:23:14,274INFO||cli||242||Vérification des paramètres",
        "2025-10-20 08:23:14,282INFO||cli||242||Vérification des fichiers",
        "2025-10-20 08:23:14,287INFO||core||450||Détection de l'extension de l'archive",
        "2025-10-20 08:23:14,287INFO||core||450||Extension de l'archive : zip",
        "2025-10-20 08:23:14,287INFO||core||450||Extraction de l'archive",
        "2025-10-20 08:23:28,676INFO||cli||242||Compression de l'archive",
        "2025-10-20 08:23:29,148INFO||cli||242||Ajout des informations calculées"
    ]
    

## Télécharger les jeux de données

Tant que le temps de rétention n'est pas passé, il est possible de télécharger le jeu de données initial et le jeu de données normalisé si demandé :

https://data.geopf.fr/validation/api/validations/{validation}/files/source https://data.geopf.fr/validation/api/validations/{validation}/files/normalize

Dans notre exemple, les données ont été converties en CSV dans la version normalisée.

## Supprimer une validation

Il est possible de ne pas attendre le délai de rétention et supprimer manuellement une validation. Les données seront supprimées mais la validation et ses logs métiers resteront consultables.

https://data.geopf.fr/validation/api/validations/{validation}
