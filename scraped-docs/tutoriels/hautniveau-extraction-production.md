source: https://geoplateforme.github.io/tutoriels/production/hautniveau/extraction/production/

[Gestion](../../../tags/#tag:gestion) [Service avancé](../../../tags/#tag:service-avancé)

# Rendre ses données vecteur extractibles

En tant que personne responsable de la diffusion de données, on peut souhaiter que ses données stockées vecteur soient disponibles sur le service d'extraction. Il y a alors deux possibilités :

  * Que la donnée soit extractible par tout le monde
  * Que la donnée ne soit extractible que par les membres de certaines communautés



## Mise à disposition pour tout le monde

Il suffit simplement de définir l'attribut `open` de la donnée stockée à `true`.

/datastores/{datastore}/stored_data/{stored data}

Corps de requête JSON
    
    
    {
        "open": true
    }
    

De cette manière, les personnes voulant en extraire une partie verront les détails de cette donnée et l'entrepôt d'extraction y aura accès en lecture pour réaliser l'extraction.

## Mise à disposition restreinte

Cette mise à disposition limitée nécessite deux étapes. Tout d'abord, il faut donner de la visibilité sur la donnée aux communautés voulues.

/datastores/{datastore}/stored_data/{stored data}/visibility

Corps de requête JSONCorps de réponse JSON
    
    
    [
        "{community 1}", "{community 2}"
    ]
    
    
    
    [
        {
            "name": "Communauté 1",
            "_id": "{community 1}"
        },
        {
            "name": "Communauté 2",
            "_id": "{community 2}"
        }
    ]
    

Il est possible de lister les visibilités actuelles de la donnée :

/datastores/{datastore}/stored_data/{stored data}/visibility

Corps de réponse JSON
    
    
    [
        {
            "name": "Communauté 1",
            "_id": "{community 1}"
        },
        {
            "name": "Communauté 2",
            "_id": "{community 2}"
        }
    ]
    

On peut également supprimer des visibilités avec des communautés :

/datastores/{datastore}/stored_data/{stored data}/visibility

Corps de requête JSONCorps de réponse JSON
    
    
    [
        "{community 1}"
    ]
    
    
    
    [
        {
            "name": "Communauté 2",
            "_id": "{community 2}"
        }
    ]
    

À ce moment, les personnes membres des communautés ciblées verront les détails sur la donnée et la verront au niveau de l'API d'extraction. En revanche, il faut que le datastore de l'extracteur puisse y avoir accès en lecture. On va donc partager notre donnée avec ce datastore (`579526dc-a3bb-437f-8163-d7e48d79d385`). Cette action ne doit être faite qu'une fois. Si on ajoute une nouvelle communauté pour la visibilité, il n'y a pas besoin de refaire ce partage.

/datastores/{datastore}/stored_data/{stored data}/sharings

Corps de requête JSON
    
    
    [
        "579526dc-a3bb-437f-8163-d7e48d79d385"
    ]
    

Attention

On donne des visibilités sur la donnée à des **communautés** via leurs identifiants, on partage une donnée avec des **entrepôts** via leurs identifiants
