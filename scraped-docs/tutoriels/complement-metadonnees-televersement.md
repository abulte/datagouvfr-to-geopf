source: https://geoplateforme.github.io/tutoriels/production/complement/metadonnees/televersement/

[Alimentation](../../../tags/#tag:alimentation) [Métadonnée](../../../tags/#tag:métadonnée)

# Téléversement des métadonnées

Les métadonnées permettent de décrire les données diffusées sur la plateforme : la source, la date et la méthode d'acquisition... Ces fichiers au format XML peuvent se référencer les uns les autres à l'aide d'un identifiant unique au sein de la plateforme : le file identifier. Deux "niveaux" de métadonnées sont gérées par l'utilisateur de l'entrepôt : la métadonnée de lot (`dataset`) et la métadonnée de produit (`serie`). Les métadonnées de services sont assumées par le gestionnaire de la plateforme.

## Téléversement d'une nouvelle métadonnée

Le fichier de métadonnée :

  * doit être un fichier XML valide
  * doit avoir son file identifier défini au xpath : `gmd:MD_Metadata / gmd:fileIdentifier / gco:CharacterString` : si celui ci est déjà pris sur la plateforme, une erreur sera remontée
  * peut avoir son niveau défini au xpath : `md:MD_Metadata / gmd:hierarchyLevel / gmd:MD_ScopeCode` (valeur `dataset` ou `series`). S'il n'est pas défini, la métadonnée sera considérée comme étant de lot.



Exemple :

  * [métadonnée de lot](../../../assets/data/metadonnee_lot.xml)
  * [métadonnée de produit](../../../assets/data/metadonnee_produit.xml)



`<metadonnee_lot.xml>`

/datastores/{datastore}/metadata

Corps de requête MultipartCorps de réponse JSON

  * file = `<metadonnee_lot.xml>`
  * type = `ISOAP` (non obligatoire, `ISOAP` par défaut, valeurs possibles : `ISOAP`, `INSPIRE`)
  * open_data = `false` (non obligatoire, `false` par défaut, valeurs possibles : `true`, `false`)


    
    
    {
        "type": "ISOAP",
        "open_data": false,
        "level": "DATASET",
        "file_identifier": "IGNF_RGEALTIr_2-0_ASC_5M_LAMB93_IGN69_D074.xml",
        "tags": {},
        "endpoints": [],
        "_id": "{metadata}"
    }
    

Notez que : 

  * Pour que la métadonnée soit intégrée dans le [catalogue INSPIRE](https://data.geopf.fr/csw/INSPIRE), il suffit de l’indiquer dans l’attribut type (type = `INSPIRE`). Elle sera alors moissonnée par le [Géocatalogue](https://www.geocatalogue.fr/fr). 
  * Pour que la métadonnée soit moissonnée par le site [data.gouv.fr](https://www.data.gouv.fr), il suffit de l’indiquer dans l’attribut open_data (open_data = `true`). 



À ce stade, elle n'est accessible que par l'API Entrepôt, aux membres de la communauté, via son identifiant. L’étape suivante est [la publication](../publication/). 

## Modification d'une métadonnée

Il est possible de modifier le fichier XML correspondant à une métadonnée. Le file identifier ne doit pas changer, et si la métadonnée est déjà publiée, la modification est reportée au niveau des catalogues.

`<metadonnee_lot.xml>`

/datastores/{datastore}/metadata/{metadata}

Corps de requête MultipartCorps de réponse JSON

  * file = `<metadonnee_lot.xml>`


    
    
    {
        "type": "ISOAP",
        "level": "DATASET",
        "file_identifier": "IGNF_RGEALTIr_2-0_ASC_5M_LAMB93_IGN69_D074.xml",
        "endpoints": [],
        "_id": "{metadata}"
    }
    

## Modification des attributs d'une métadonnée

Il est possible de modifier les attributs (type et open_data) d’une métadonnée déjà existante. 

/datastores/{datastore}/metadata/{metadata}

Corps de requête JSONCorps de réponse JSON
    
    
    {        
      "type": "INSPIRE",
      "open_data": true
    }
    
    
    
    {
        "type": "INSPIRE",
        "open_data": true,
        "level": "DATASET",
        "file_identifier": "IGNF_RGEALTIr_2-0_ASC_5M_LAMB93_IGN69_D074.xml",
        "tags": {},
        "endpoints": [],
        "_id": "{metadata}"
    }
    

La métadonnée doit être republiée par la suite afin de répercuter les modifications au niveau des services de catalogage.
