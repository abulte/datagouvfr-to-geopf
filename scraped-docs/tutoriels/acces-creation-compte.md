source: https://geoplateforme.github.io/tutoriels/production/controle-des-acces/entrepot/creation_compte/

[API Entrepôt](../../../tags/#tag:api-entrepôt) [Contrôle des accès](../../../tags/#tag:contrôle-des-accès)

# Création d'un compte Géoplateforme

Toutes les applications de la Géoplateforme s'appuient, pour l'authentification, sur un gestionnaire d'identité unique (solution Keycloak). La première étape consiste donc à [s'enregistrer](https://sso.geopf.fr/realms/geoplateforme/account/) si ce n'est pas déjà le cas.

Par convention, le nom d'utilisateur doit être de la forme {prenom}.{nom}, en minuscule.

Lors de l'enregistrement, vous aurez à utiliser une application de génération de code à usage unique (FreeOTP sur votre téléphone par exemple). Vous en aurez besoin à chaque authentification.
