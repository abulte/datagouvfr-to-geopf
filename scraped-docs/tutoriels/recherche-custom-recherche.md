source: https://geoplateforme.github.io/tutoriels/production/recherche/custom/recherche/

[Diffusion](../../../tags/#tag:diffusion) [Donnée indexée](../../../tags/#tag:donnée-indexée) [Service de recherche](../../../tags/#tag:service-de-recherche)

# Recherche dans un index personnalisé

Pour effectuer une recherche sur un index custom, il faudra se connecter au préalable avec [un compte Géoplateforme ou une clé défini précédemment](../../../controle-des-acces/diffusion/cle/).

Il est possible de lister les différents index custom qui nous sont disponibles avec cette route (toutes les index custom à _open=true_ et les _open=false_ où vous avez la permission) :

https://data.geopf.fr/private/recherche/api/indexes

Le champ _index_ obtenu pour chaque index est à utiliser par la suite pour rechercher dans celui-ci. Il est défini selon le _layer_name_ de la configuration dans l'entrepôt

Ensuite, la recherche dans les index custom fonctionnent différemment selon la définition du is_layer_search de l'index custom.

## Index custom Search_Layer (ressemblant à l'index standard)

La recherche fonctionne exactement comme [l'index standard](../../standard/), la seule différence est l'URL de base qui est différente : _https://data.geopf.fr/private/recherche/api/indexes/{index}_ avec le nom de l'index à la place de {index}.

## Index custom classique

Plusieurs routes ne sont plus accessibles avec ce type d'index custom :

  * Suggestion par champ : _/api/indexes/{index}/suggest_
  * Consultation par l'id d'un document
  * Consultation par offres



Donc les routes possibles sont la recherche POST et l'autocomplétion de titre. Ces deux routes fonctionnent comme pour l'index standard.

Pour la requête POST, les champs recherchables correspondent à ceux définis dans le Get Capabilities de l'index;

Pour l'autocomplétion de titre, les champs recherchables sont seulement ceux de type _string_.

## Utiliser l'autocomplétion dans les index custom

Si vous souhaitez utiliser l'autocomplétion sur vos index custom (_/api/indexes/{index}/suggest_), nous vous conseillons de créer deux index :

  * Un index custom classique avec vos informations enregistrées dans le format souhaité.
  * Un index custom Search_Layer (ressemblant à l'index standard) pour pouvoir utiliser l'autocomplétion. Il faudra respecter le format de données nécessaire à la création de ce [type d'index](../creation/), mais les seuls champs qui nous intéressent sont les champs sur lesquels l'autocomplétion est possible : _title_ , _description_ , _layer_name_ , _theme_ et _keywords_ (les autres champs peuvent être remplis avec des informations génériques). Ce sont dans ces champs que devront se trouver vos champs de l'index custom classique sur lequel vous souhaitez faire l'autocomplétion.



A partir de ces deux index custom vous pourrez utiliser l'index custom Search_Layer pour utiliser la requête _/api/indexes/{index}/suggest_ et faire de l'autocomplétion et l'index custom classique pour faire la recherche final (la recherche POST par exemple) et obtenir toutes les informations nécessaires du document ressorti par l'autcomplétion.

#### Exemple

J'ai un index custom sur lequel je veux faire de l'autocomplétion sur un champ _Titre_

Je crée un index custom Search_Layer dans lequel j'intègre le champ _Titre_ en le rennomant _title_ et remplis tous les autres champs par des informations génériques

Je fais les requêtes d'autocomplétion sur l'index custom Search_Layer en filtrant uniquement sur _title_ (_/api/indexes/{index}/suggest?fields=title_)

Je fais une requête final POST sur l'index custom classique pour obtenir les informations de toutes les autres champs du document choisis à partir de l'autocomplétion
