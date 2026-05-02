source: https://geoplateforme.github.io/tutoriels/production/vecteur/derivation/

[Donnée vecteur](../../tags/#tag:donnée-vecteur) [Dérivation](../../tags/#tag:dérivation) [Injection](../../tags/#tag:injection)

# Dérivation d'une donnée vecteur en base

Il est possible de modifier une donnée vecteur en lui ajoutant des index, des champs ou en recalculant des champs. Toutes ces actions peuvent donner une nouvelle donnée ou être jouée sur une donnée existante.

Impacts sur la diffusion

Lors de la modifications d'une donnée stockée existante et diffusée, pour que ce soit pris en compte, il peut-être nécessaire de mettre à jour les offres de diffusion.

Dans certains cas, la modification peut aller jusqu'à "casser" la diffusion, comme la suppression de colonne ou le changement de type. En effet, les services de diffusion ont en mémoire une structure qui n'est plus valide et la lecture des données ne sera plus fonctionnelle tant que la synchronisation de l'offre n'est pas faite.

Les instructions SQL suivantes sont autorisées :

  * CREATE TABLE
  * INSERT
  * UDPATE
  * SELECT
  * CREATE INDEX
  * ALTER TABLE
  * CREATE FUNCTION
  * DROP TABLE
  * DELETE
  * CREATE SEQUENCE
  * CREATE VIEW
  * ALTER SEQUENCE
  * CREATE TRIGGER



Pour que le SQL de dérivation soit paramétrable via les paramètres de l'exécution de traitement, il faut utiliser la syntaxe `{{ params.<x> }}` et passer comme valeur du paramètre `params` de l'exécution un objet avec l'attribut `<x>`. La valeur sera injectée dans le SQL lors de l'exécution.

Les entités (tables, vues, fonctions...) écrites le sont dans la donnée de sortie. Il est possible d'avoir une ou plusieurs données stockées de type VECTOR-DB en entrée de l'exécution. Elles seront uniquement lisibles et leur désignations dans le SQL de dérivation se fait avec la syntaxe `{{ inputs.<n> }}` : `{{ inputs.1 }}` pour la première donnée stockée en entrée, `{{ inputs.2 }}` pour la deuxième...

Un exemple d'utilisation est disponible [ici](exemple1/).
