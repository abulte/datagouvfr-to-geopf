source: https://geoplateforme.github.io/tutoriels/production/controle-des-acces/diffusion/cle/

[Contrôle des accès](../../../tags/#tag:contrôle-des-accès) [Diffusion](../../../tags/#tag:diffusion)

# Gestion des clés

En tant que consommateur de données, c'est également via l'API que l'on va pouvoir configuer ses clés d'accès. Cela n'implique pas d'avoir accès à une entrepôt, ni même d'être le membre d'une communauté.

## Consultation des permissions

L'ensemble des permissions qui m'ont été personnellement donnée ou qui ont été données à une communauté à laquelle l'utilisateur appartient constitue une sorte de catalogue de données qu'il va être possible de consommer.

### Récupérer ses permissions personnelles

/users/me/permissions

Paramètres de requêteCorps de réponse JSON

  * personal = `true`
  * community = `false`


    
    
    [
        {
            "licence": "Accès restreint",
            "end_date": "2023-06-23T14:00:00Z",
            "offerings": [
                {
                    "type": "WFS",
                    "status": "PUBLISHED",
                    "layer_name": "pays_ecoregions",
                    "open": false,
                    "available": true,
                    "_id": "{offering}"
                }
            ],
            "only_oauth": false,
            "_id": "{permission utilisateur}"
        }
    ]
    

En tant que bénéficiaire de cette permission personnelle, je peux la supprimer si elle ne m'intéresse pas.

### Récupérer ses permissions communautaires

/users/me/permissions

Paramètres de requêteCorps de réponse JSON

  * personal = `false`
  * community = `true`


    
    
    [
        {
            "licence": "Accès restreint",
            "end_date": "2023-06-23T14:00:00Z",
            "offerings": [
                {
                    "type": "WFS",
                    "status": "PUBLISHED",
                    "layer_name": "pays_ecoregions",
                    "open": false,
                    "available": true,
                    "_id": "{offering}"
                }
            ],
            "only_oauth": false,
            "_id": "{permission communauté}"
        }
    ]
    

Les deux permissions donnent accès à la même offre. Lors de la configuration de la clé, il sera important de préciser quelle permission exploiter, en gardant à l'esprit qu'il est possible de perdre le droit de consommer des données si la permission est modifiée par le diffuseur de la donnée.

### Consulter une permission

Dans la suite, nous allons exploiter la permission personnelle. Il est possible d'avoir plus d'informations sur celle ci.

/users/me/permissions/{permission utilisateur}

Corps de réponse JSON
    
    
    [
        {
            "licence": "Accès restreint",
            "end_date": "2023-06-23T14:00:00Z",
            "offerings": [
                {
                    "type": "WFS",
                    "status": "PUBLISHED",
                    "layer_name": "pays_ecoregions",
                    "open": false,
                    "available": true,
                    "_id": "{offering}"
                }
            ],
            "only_oauth": false,
            "_id": "{permission communauté}"
        }
    ]
    

## Gérer une clé d'accès

Sans clé d'accès, il n'est pas possible de consulter le service de diffusion, même pour une [requête de capacité du service](https://data.geopf.fr/private/wfs?REQUEST=GetCapabilities&SERVICE=WFS&VERSION=2.0.0).

https://data.geopf.fr/private/wfs

Paramètres de requêteCorps de réponse XML

  * REQUEST = `GetCapabilities`
  * SERVICE = `WFS`
  * VERSION = `2.0.0`


    
    
    <html>
        <head><title>401 Authorization Required</title></head>
        <body>
            <center><h1>401 Authorization Required</h1></center>
        </body>
    </html>
    

La clé d'accès est un moyen de s'identifier lors de l'utilisation des services de diffusion. Il existe trois type d'identification :

  * Le hash en paramètre de requête `api_key` ou en header `X-Key`
  * Une authentification `Basic`
  * Une authentification `Bearer` (jeton généré par le gestionnaire d'identité). C'est l'authentification forte, qui peut être nécessaire pour exploiter les permissions dont le champ `only_oauth` est à vrai.



### Créer une clé d'accès simple

Nous allons ici voir un exemple de mise en place d'une clé de type HASH.

/users/me/keys

Corps de requête JSONCorps de réponse JSON
    
    
    {
        "name": "Ma clé HASH",
        "type": "HASH",
        "type_infos": {
            "hash": "masupercle"
        }
    }
    
    
    
    {
        "name": "Ma clé HASH",
        "type": "HASH",
        "whitelist": [],
        "blacklist": [],
        "type_infos": {
            "hash": "masupercle"
        },
        "_id": "{key HASH}"
    }
    

Quelque soit le type de clé, il est possible de préciser des conditions d'utilisation de la clé :

  * Limiter les IP pouvant l'utiliser (whitelist)
  * Bloquer des IP (blacklist)
  * Forcer le referer
  * Forcer le user agent



Il est maintenant possible [d'interroger le service](https://data.geopf.fr/private/wfs?REQUEST=GetCapabilities&SERVICE=WFS&VERSION=2.0.0&apikey=masupercle). Cependant, aucune couche ne semble disponible, car nous n'avons pas encore donné de droit à cette clé.

### Gérer les accès à la clé

Les permissions ouvrent des droits a priori sur des offres, mais c'est à la charge du propriétaire de la clé de définir les accès aux offres. Un accès est un lien entre une clé et une offre, en exploitant une permission. On peut ajouter plusieurs accès à des offres en un appel, tant que c'est la même permission qui permet les accès.

/users/me/keys/{key HASH}/accesses

Corps de requête JSON
    
    
    {
        "permission": "{permission utilisateur}",
        "offerings": [
            "{offering}"
        ]
    }
    

On peut connaître toutes les offres que la clé peut consommer avec l'appel suivant.

/users/me/keys/{key HASH}/accesses

Corps de réponse JSON
    
    
    [
        {
            "permission": {
                "licence": "Accès restreint",
                "end_date": "2023-06-23T14:00:00Z",
                "only_oauth": false,
                "_id": "{permission utilisateur}"
            },
            "offering": {
                "open": false,
                "available": true,
                "layer_name": "pays_ecoregions",
                "type": "WFS",
                "status": "PUBLISHED",
                "_id": "{offering}"
            },
            "_id": "{access}"
        }
    ]
    

On peut maintenant voir les couches correspondantes à l'offre dans les [capacités du serveur](https://data.geopf.fr/private/wfs?REQUEST=GetCapabilities&SERVICE=WFS&VERSION=2.0.0&apikey=masupercle).

https://data.geopf.fr/private/wfs

Paramètres de requêteCorps de réponse XML

  * REQUEST = `GetCapabilities`
  * SERVICE = `WFS`
  * VERSION = `2.0.0`
  * apikey = `masupercle`


    
    
    <FeatureTypeList>
        <FeatureType
            xmlns:pays_ecoregions="http://pays_ecoregions">
            <ows:Keywords>
                <ows:Keyword>Tutoriel</ows:Keyword>
                <ows:Keyword>Données mondiales</ows:Keyword>
            </ows:Keywords>
            <Name>pays_ecoregions:pays</Name>
            <ows:WGS84BoundingBox>
                <ows:UpperCorner>175.0 85.0</ows:UpperCorner>
                <ows:LowerCorner>-175.0 -75.0</ows:LowerCorner>
            </ows:WGS84BoundingBox>
            <Title>Pays du monde</Title>
            <Abstract>Pays du monde</Abstract>
            <DefaultCRS>urn:ogc:def:crs:EPSG::3857</DefaultCRS>
        </FeatureType>
        <FeatureType
            xmlns:pays_ecoregions="http://pays_ecoregions">
            <ows:Keywords>
                <ows:Keyword>Tutoriel</ows:Keyword>
                <ows:Keyword>Données mondiales</ows:Keyword>
            </ows:Keywords>
            <Name>pays_ecoregions:regions_ecologiques</Name>
            <ows:WGS84BoundingBox>
                <ows:UpperCorner>175.0 85.0</ows:UpperCorner>
                <ows:LowerCorner>-175.0 -75.0</ows:LowerCorner>
            </ows:WGS84BoundingBox>
            <Title>Régions écologiques</Title>
            <Abstract>Grandes régions naturelles mondiales</Abstract>
            <DefaultCRS>urn:ogc:def:crs:EPSG::3857</DefaultCRS>
        </FeatureType>
    </FeatureTypeList>
    

Il est aussi possible de mettre la clé dans le header `apikey` plutôt qu'en paramètre de requête.

Clé HASH dans QGis

### Créer une clé de type BASIC

Nous allons ajouter à cette clé des limites d'utilisation, un user agent particulier qui limite l'usage de la clé au client QGis. À noter que l'ajout d'un filtrage par referer ne peut être considéré comme une méthode de sécurisation forte.

/users/me/keys

Corps de requête JSONCorps de réponse JSON
    
    
    {
        "name": "Ma clé BASIC",
        "type": "BASIC",
        "user_agent": ".*QGIS.*",
        "type_infos": {
            "login": "cestmoi",
            "password": "cestmaclesecrète"
        }
    }
    
    
    
    {
        "name": "Ma clé BASIC",
        "type": "BASIC",
        "whitelist": [],
        "blacklist": [],
        "user_agent": ".*QGIS.*",
        "type_infos": {
            "login": "cestmoi",
            "password": "ff4728a2a0058c14b6c0297408c8825a1fa15132"
        },
        "_id": "{key BASIC}"
    }
    

L'affectation d'accès sur cette clé se fait exactement comme pour la première clé.

Afin que les requêtes passent, il est maintenant nécessaire que le header "Referer" contienne une valeur avec QGIS (cela permet par exemple d'accepter toutes les requêtes venant de QGis, quelque soit la version et le système d'exploitation).

Clé BASIC dans QGis

### Créer une clé de type OAUTH2

Cette clé est un moyen de préciser que l'on va consommer les services de diffusion en utilisant son compte. Ce mode d'identification de la consommation est considéré comme la seule sécurisation forte. C'est pourquoi certaines permissions peuvent n'autoriser leur usage qu'avec de telles clés. Comme chaque utilisateur n'a qu'un compte, il ne peut se créer qu'une seule clé de ce type.

/users/me/keys

Corps de requête JSONCorps de réponse JSON
    
    
    {
        "name": "Ma clé OAUTH2",
        "type": "OAUTH2",
        "type_infos": {}
    }
    
    
    
    {
        "name": "Ma clé OAUTH2",
        "type": "OAUTH2",
        "whitelist": [],
        "blacklist": [],
        "type_infos": {},
        "_id": "{key OAUTH}"
    }
    

L'affectation d'accès sur cette clé se fait exactement comme pour la première clé.

Clé OAUTH2 dans QGis

  * URL de requête : `https://sso.geopf.fr/realms/geoplateforme/protocol/openid-connect/auth`
  * URL du jeton : `https://sso.geopf.fr/realms/geoplateforme/protocol/openid-connect/token`
  * Client ID : `qgis`
  * Secret client : `F77z01QHTaJClBJ1p2OZYkFGL24XYLti`


