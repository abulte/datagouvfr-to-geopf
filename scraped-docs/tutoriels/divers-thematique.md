source: https://geoplateforme.github.io/tutoriels/production/divers/thematique/

[Diffusion](../../tags/#tag:diffusion) [Divers](../../tags/#tag:divers)

# Mise en place d'un groupe thématique de couches

Sur un point d'accès ouvert, toutes les données sont accessibles. Toutes les couches apparaissent dans la requête de capacité du service. Aucune clé d'accès ne va permettre de filtrer cela pour ne montrer qu'une sous partie de ce que les serveurs de diffusion contiennent. Pour remédier à cela, il est possible de mettre en place des capacités de service statique.

Dans la suite, nous allons travailler avec le service WFS public.

## Récupération et filtrage manuel des capacités complètes

On commence par télécharger les [capacités complètes](https://data.geopf.fr/wfs?REQUEST=GetCapabilities&SERVICE=WFS&VERSION=2.0.0) du service de diffusion ciblé.
    
    
    curl -o getcap.xml "https://data.geopf.fr/wfs?REQUEST=GetCapabilities&SERVICE=WFS&VERSION=2.0.0"
    

Le nettoyage doit se faire au sein des noeuds XML `wfs:WFS_Capabilities/FeatureTypeList/FeatureType`. Il est également possible de nettoyer les namespaces définis au niveau du noeud racine du document. Il est nécessaire de ne pas toucher aux autres éléments du document XML, afin que celui ci reste une réponse interprétable par les clients applicatifs consommant du WFS.

Les informations particulièrement importantes sont les URL à utiliser pour les requêtes de consultation (noeuds `wfs:WFS_Capabilities/ows:OperationsMetadata/ows:Operation`) : elles doivent bien correspondre au point d'accès cible.

Il n'est pas nécessaire d'être le propriétaire des couches laissées dans la liste.

## Hébergement sous forme d'annexe

Afin de rendre ce fichier accessible, nous allons le déposer au sein de l'entrepôt sous forme d'annexe. Il est bien sur possible de l'héberger de n'importe quelle manière, par un simple serveur de fichier.

/datastores/{datastore}/annexes

Corps de requête MultipartCorps de réponse JSON

  * file = `<getcap.xml>`
  * paths = `capabilities/mes_couches_wfs`
  * published = `true`


    
    
    {
        "paths": [
            "/capabilities/mes_couches_wfs"
        ],
        "size": 206798,
        "mime_type": "application/xml",
        "published": true,
        "_id": "{annexe}"
    }
    

Nous avons demandé à ce que cette annexe soit directement publiée. Nous pouvons donc maintenant y accéder publiquement à cette URL : 

  * https://data.geopf.fr/annexes/{technical_name}/capabilities/mes_couches_wfs



En mettant cette URL dans QGis pour définir un nouveau serveur WFS, on va pouvoir ne récupérer, en s'y connectant, que les couches sélectionnées.
