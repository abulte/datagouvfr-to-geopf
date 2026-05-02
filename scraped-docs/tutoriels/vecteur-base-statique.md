source: https://geoplateforme.github.io/tutoriels/production/vecteur/base/gestion_statique/

[Diffusion](../../../tags/#tag:diffusion) [Donnée vecteur](../../../tags/#tag:donnée-vecteur) [Fichier de style](../../../tags/#tag:fichier-de-style) [WMS](../../../tags/#tag:wms)

# Dépôt de fichiers statiques

## Gestion des styles

Pour certains types de diffusion, le serveur de diffusion peut avoir besoin de fichiers de configuration. Dans le cas de la diffusion WMS à partir de données vecteur, assurée par Geoserver, ce sont des styles au format SLD et des FTL qui sont utilisés. Afin de les déposer au sein de l'entrepôt, le concept de fichier statique (static) est exploité.

### Génération d'un SLD

Après l'export des styles depuis QGis dans son format, il est nécessaire d'utiliser l'outil geostyler en ligne de commande pour les convertir :
    
    
    $  geostyler-cli -o ecoregions.sld -t sld -s qgis ecoregions.qml 
    ✔ File "ecoregions.qml" translated successfully. Output written to ecoregions.sld
    $  geostyler-cli -o pays.sld -t sld -s qgis pays.qml 
    ✔ File "pays.qml" translated successfully. Output written to pays.sld
    

Attention

Chaque outil d'export peut entraîner des comportements différents. Au final, le SLD sera interprété par Geoserver sur la Géoplateforme. Le plugin [GeoCat Bridge](https://plugins.qgis.org/plugins/geocatbridge/) peut également être utilisé.

Télécharger [ecoregions.sld](../../../assets/data/ecoregions.sld)

Télécharger [pays.sld](../../../assets/data/pays.sld)

### Écriture de FTL

Ces [fichiers FTL](https://docs.geoserver.org/stable/en/user/tutorials/freemarker.html) permettent de mettre en forme la réponse HTML lors des appels au GetFeatureInfo

Télécharger [ecoregions.ftl](../../../assets/data/ecoregions.ftl)

Contenu
    
    
    <#list features as feature>
    
        <h2>${feature.eco_name.value}</h2>
        <p>${feature.biome_name.value}</p>
    
    </#list>
    

Télécharger [pays.ftl](../../../assets/data/pays.ftl)

Contenu
    
    
    <#list features as feature>
    
        <h1>${feature.name.value}</h1>
    
    </#list>
    

### Téléversement dans l'entrepôt

On dépose les 4 fichiers de configuration (2 SLD et 2 FTL).

`ecoregions.sld`

/datastores/{datastore}/statics

Corps de requête MultipartCorps de réponse JSON

  * file = `<ecoregions.sld>`
  * type = "GEOSERVER-STYLE"
  * name = "Style pour les écorégions"


    
    
    {
        "name": "Style pour les écorégions",
        "type": "GEOSERVER-STYLE",
        "_id": "{sld ecoregions}",
        "type_infos": {
            "used_attributes": [
                "biome_name"
            ]
        }
    }
    

`pays.sld`

/datastores/{datastore}/statics

Corps de requête MultipartCorps de réponse JSON

  * file = `<pays.sld>`
  * type = "GEOSERVER-STYLE"
  * name = "Style pour les pays"


    
    
    {
        "name": "Style pour les pays",
        "type": "GEOSERVER-STYLE",
        "_id": "{sld pays}",
        "type_infos": {}
    }
    

`ecoregions.ftl`

/datastores/{datastore}/statics

Corps de requête MultipartCorps de réponse JSON

  * file = `<ecoregions.ftl>`
  * type = "GEOSERVER-FTL"
  * name = "FTL pour les écorégions"


    
    
    {
        "name": "FTL pour les écorégions",
        "type": "GEOSERVER-FTL",
        "_id": "{ftl ecoregions}",
        "type_infos": {
            "used_attributes": [
                "biome_name",
                "eco_name"
            ]
        }
    }
    

`pays.ftl`

/datastores/{datastore}/statics

Corps de requête MultipartCorps de réponse JSON

  * file = `<pays.ftl>`
  * type = "GEOSERVER-FTL"
  * name = "FTL pour les pays"


    
    
    {
        "name": "FTL pour les pays",
        "type": "GEOSERVER-FTL",
        "_id": "{ftl pays}",
        "type_infos": {
            "used_attributes": [
                "name"
            ]
        }
    }
    
