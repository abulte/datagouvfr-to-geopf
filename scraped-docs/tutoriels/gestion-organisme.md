source: https://geoplateforme.github.io/tutoriels/production/gestion/organisme/

[Gestion](../../tags/#tag:gestion) [Organisme](../../tags/#tag:organisme)

# Consultation d'un organisme

Lorsque l'on appartient à un organisme, on a la possibilité d'en gérer les membres et de lire le contenu de ses communautés.

## Gestion des membres

Pour connaître les membres de l'organisme (pagination disponible) :

/organizations/{organization}/users

Corps de réponse JSON
    
    
    [
        {
            "last_name": "Lopper",
            "first_name": "Dave",
            "email": "dave.lopper@organization.org",
            "_id": "{user}"
        },
        {
            "last_name": "Oriale",
            "first_name": "Edith",
            "email": "edith.orial@organization.org",
            "_id": "{user}"
        }
    ]
    

Pour ajouter un membre à l'organisme (pas de droits plus fins, être attaché à un organisme donne tous les droits de lecture et de gestion de ses membres) :

/organizations/{organization}/users/{user}

Pour supprimer un membre de l'organisme :

/organizations/{organization}/users/{user}

## Lecture du contenu

Avoir la liste des communautés rattachées à l'organisme peut se faire via l'appel suivant :

/organizations/{organization}/communities

Corps de réponse JSON
    
    
    [
        {
            "name": "Communauté 1",
            "technical_name": "community_1",
            "organization": {
                "name": "Organisme",
                "_id": "{organization}"
            },
            "_id": "{community 1}",
            "public": false
        },
        {
            "name": "Communauté 2",
            "technical_name": "community_2",
            "organization": {
                "name": "Organisme",
                "_id": "{organization}"
            },
            "_id": "{community 2}",
            "public": false
        }
    ]
    

La liste des entités suivantes sont consultables au niveau de l'organisme. Dans les réponses, l'identifiant de la communauté et de l'entrepôt sont disponible pour pouvoir en consulter le détail. Les filtres présents sur les routes de consultation de l'entrepôt sont également disponibles dans ces routes (consulter les spécifications OpenAPI pour avoir le détail). Il est possible en plus de filtrer par communauté ou entrepôt.

  * les annexes : `GET /organizations/{organization}/annexes`
  * les configurations : `GET /organizations/{organization}/configurations`
  * les points d'accès disponibles, avec les quotas : `GET /organizations/{organization}/endpoints`
  * Les offres : `GET /organizations/{organization}/offerings`
  * les permissions : `GET /organizations/{organization}/permissions`
  * les exécutions de traitement : `GET /organizations/{organization}/processings/executions`
  * les fichiers statiques : `GET /organizations/{organization}/statics`
  * les données stockées : `GET /organizations/{organization}/stored_data`
  * les livraisons : `GET /organizations/{organization}/uploads`


