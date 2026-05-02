source: https://geoplateforme.github.io/entrepot/production/composants/

# Applicatifs de la Géoplateforme

## Les briques générales

[Gestionnaire d'identitéGestion des comptes utilisateurs   
Keycloak ](https://sso.geopf.fr/realms/geoplateforme/account)

[API EntrepôtGestion des données et de leurs diffusions](https://data.geopf.fr/api/swagger-ui/index.html)

## Les services de diffusion de données

### À accès libre

[Service WMS VecteurDiffusion des données vecteur selon le standard OGC Web Map Service   
Geoserver ](https://data.geopf.fr/wms-v?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0)

[Service WMS RasterDiffusion des données raster selon le standard OGC Web Map Service   
Rok4 ](https://data.geopf.fr/wms-r?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0)

[Service WMTSDiffusion des données raster selon le standard OGC Web Map Tile Service   
Rok4 ](https://data.geopf.fr/wmts?SERVICE=WMTS&REQUEST=GetCapabilities&VERSION=1.0.0)

[Service TMSDiffusion des données raster et vecteur selon l'API Tile Map Service   
Rok4 ](https://data.geopf.fr/tms/1.0.0)

[Service TMS VecteurDiffusion des données vecteur en base selon l'API Tile Map Service   
Pg_tileserv ](https://data.geopf.fr/vector-tms/1.0.0/index.json)

[Service WFSDiffusion des données vecteur selon le standard OGC Web Feature Service   
Geoserver ](https://data.geopf.fr/wfs?SERVICE=WFS&REQUEST=GetCapabilities&VERSION=2.0.0)

[Service de téléchargementDiffusion de données sous forme de fichiers téléchargeables ](https://data.geopf.fr/telechargement/capabilities)

[Service d'altimétrieInterrogation des données raster MNT pour obtenir des altitudes ou des profils altimétriques ](https://data.geopf.fr/altimetrie/resources)

[Service d'itinéraire et d'isochroneInterrogation des graphes navigables pour obtenir des itinéraires ou des isochrones ](https://data.geopf.fr/navigation/getcapabilities)

[Service de rechercheInterrogation d'un index de recherche pour obtenir des documents ](https://data.geopf.fr/recherche/api/indexes)

### À accès restreint

Attention

Il est nécessaire de préciser un moyen d'identification (une "clé") lors des appels aux services qui suivent, même pour récupérer les capacités. Les liens suivant, sans ajouter de clé, seront en erreur 401

[Service WMS VecteurDiffusion des données vecteur selon le standard OGC Web Map Service   
Geoserver ](https://data.geopf.fr/private/wms-v?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0)

[Service WMS RasterDiffusion des données raster selon le standard OGC Web Map Service   
Rok4 ](https://data.geopf.fr/private/wms-r?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0)

[Service WMTSDiffusion des données raster selon le standard OGC Web Map Tile Service   
Rok4 ](https://data.geopf.fr/private/wmts?SERVICE=WMTS&REQUEST=GetCapabilities&VERSION=1.0.0)

[Service TMSDiffusion des données raster et vecteur selon l'API Tile Map Service   
Rok4 ](https://data.geopf.fr/private/tms/1.0.0)

[Service WFSDiffusion des données vecteur selon le standard OGC Web Feature Service   
Geoserver ](https://data.geopf.fr/private/wfs?SERVICE=WFS&REQUEST=GetCapabilities&VERSION=2.0.0)

[Service de téléchargementDiffusion de données sous forme de fichiers téléchargeables ](https://data.geopf.fr/private/telechargement/capabilities)

[Service d'altimétrieInterrogation des données raster MNT pour obtenir des altitudes ou des profils altimétriques ](https://data.geopf.fr/private/altimetrie/resources)

[Service d'itinéraire et d'isochroneInterrogation des graphes navigables pour obtenir des itinéraires ou des isochrones ](https://data.geopf.fr/private/navigation/getcapabilities)

[Service de rechercheInterrogation d'un index de recherche pour obtenir des documents ](https://data.geopf.fr/private/recherche/api/indexes)

## Les services de diffusion complémentaires

[Catalogue de métadonnéesConsultation des métadonnées publiées dans l'entrepôt Géoplateforme   
Geonetwork ](https://data.geopf.fr/csw?SERVICE=CSW&REQUEST=GetCapabilities&VERSION=2.0.2)

[Catalogue des annexesConsultation des fichiers publiées dans l'entrepôt Géoplateforme sous forme d'annexes   
racine du service non consultable ](https://data.geopf.fr/annexes)

## Les applicatifs internes

Précisions

Les stockages ne sont pas accessibles directement. L'écriture des données sur ces derniers se fait exclusivement via les traitements de l'Entrepôt, et leur consultation via les services de diffusion. L'orchestrateur de calcul est également pilotable exclusivement via l'API Entrepôt.

S3

Stockage des archives, des pyramides, des données livrées, des annexes 

PostgreSQL + PostGIS

Stockage des bases vecteur 

OpenSearch

Stockage des index de recherche 

PostgreSQL + PostGIS + PGRouting

Stockage des graphes navigables vecteur 

GitLab

Orchestrateur de traitements 

## Consommation des services

Afin de faciliter l'usage des services, des configurations sont disponible sur [ce dépôt GitHub](https://github.com/Geoplateforme/clients-configurations/) pour QGis et Insomnia.
