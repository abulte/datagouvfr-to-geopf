source: https://geoplateforme.github.io/tutoriels/production/complement/documents/partage/

[Document personnel](../../../tags/#tag:document-personnel) [Partage](../../../tags/#tag:partage)

# Partage des documents

Il existe deux possibilités de partage de documents personnels : 

  * le partage nominatif : la personne pourra alors voir le document dans sa liste et le télécharger
  * le partage public : une URL aléatoire permet alors à n'importe qui de télécharger le fichier



## Le partage nominatif

Il est nécessaire d'avoir les identifiants des personnes avec lesquelles on souhaite partager notre document.

L'ajout au chemin du nom technique de l'entrepôt permet de gérer l'unicité d'un chemin de publication d'une annexe seulement au sein d'un entrepôt. Ce nom est récupérable avec l'appel **GET** `/datastores/{identifiant de l'entrepôt de travail}`. Dans l'exemple qui suit, la racine d'accès public aux annexes de mon entrepôt est https://data.geopf.fr/annexes/{technical_name}.

Publier une annexe revient à modifier son statut de publication.

/users/me/documents/{document}/sharings

Corps de requête JSONCorps de réponse JSON
    
    
    [
        "{compte 1}",
        "{compte 2}"
    ]
    
    
    
    {
        "name": "Mon super croquis",
        "description": "Un petit coucou géoréférencé à l'IGN",
        "size": 5435,
        "mime_type": "application/octet-stream",
        "labels": [
            "tutoriels",
            "croquis"
        ],
        "_id": "{document}"
    }
    

Désormais, les comptes ciblés pourront voir le document dans leur liste avec l'appel :

/users/me/documents

Paramètres de requête

  * shared = `true`



Et ces comptes pourront télécharger le fichier via l'API Entrepôt (/users/me/documents/{document}/file, la même URL qu'avec' le compte propriétaire). Ce partage implique d'être authentifié pour le destinataire (donc d'avoir un compte) et de partager explicitement avec tous les destinataires.

## Le partage public

Ce mode de partage est plus simple mais moins sécurisé. Il consiste à associer au fichier une URL publique qui pourra être consultée anonymement.

/users/me/documents/{document}

Corps de requête JSONCorps de réponse JSON
    
    
    {
        "public_url": true
    }
    
    
    
    {
        "name": "Mon super croquis",
        "description": "Un petit coucou géoréférencé à l'IGN",
        "size": 5435,
        "mime_type": "application/octet-stream",
        "labels": [
            "tutoriels",
            "croquis"
        ],
        "public_url": "https://data.geopf.fr/documents/89476dA1gBOOJWU9yXp8QcpZwnTt4ICxlhWtIIQHPbMGLo.bin",
        "_id": "{document}"
    }
    

Une URL publique a été générée aléatoirement, une extension en accord avec le type de fichier a été mise. Il est possible de supprimer cet accès public en précisant `"public_url": false`. À chaque partage public, l'URL sera différente.
