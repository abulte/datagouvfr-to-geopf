# Authentication: data.gouv.fr → Géoplateforme

## Problem

A user logged into data.gouv.fr uploads a geo-compatible resource and clicks "Push to Géoplateforme." data.gouv.fr needs to call the geopf API **on behalf of that user** — without asking them to manage tokens, paste credentials, or maintain a separate geopf session.

## Solution: OAuth 2.0 authorization_code, data.gouv.fr as a confidential client of geopf

data.gouv.fr is registered as an OIDC client in geopf's Keycloak (`sso.geopf.fr`, realm `geoplateforme`). The user consents once; data.gouv.fr stores a refresh_token and calls the geopf API as the user from then on.

This is **delegated authorization**, not identity federation. ProConnect is orthogonal — it just makes the consent step silent for public-sector users who already have a ProConnect session.

## User flow

1. User logged into data.gouv.fr uploads a geo-compatible resource.
2. UI offers "Push to Géoplateforme."
3. First time: browser bounces through geopf's auth (silent if the user has a live ProConnect session shared between data.gouv.fr and geopf) + consent screen, then back to data.gouv.fr. Subsequent times, within the active window (any use in the past 12h): silent refresh, no bounce. After >12h of inactivity: the user re-consents.
4. data.gouv.fr's backend calls the geopf API with a fresh access_token and pushes the resource.

## Architecture

- **cdata (Nuxt frontend)** renders the "Push to Géoplateforme" button and links to the OAuth start endpoint. It does not handle tokens or secrets.
- **udata (Python backend)** holds the `client_secret`, runs the OAuth dance, stores per-user tokens, and uses them to call the geopf API. Mirrors the existing ProConnect client integration (`udata/auth/proconnect.py`) using Authlib.
- **Session continuity** between cdata and udata already exists.

```
[cdata UI] ──(click)──▶ udata /api/1/geopf/login
                            │
                            ▼
                  sso.geopf.fr authorize endpoint
                            │
                  (user authenticates / silent SSO via ProConnect)
                            │
                            ▼
                  udata /api/1/geopf/auth
                            │
                  (exchange code + persist refresh_token)
                            │
                            ▼
                  302 back to the originating cdata page
```

The route names mirror the existing ProConnect integration in udata (`/api/1/proconnect/login` to initiate, `/api/1/proconnect/auth` as the callback). We reuse the same `<api>/<provider>/login` + `<api>/<provider>/auth` shape under a new `geopf` API namespace.

## What we need from geopf

- A **confidential OIDC client** registered in the `geoplateforme` realm (e.g. `datagouvfr-publisher`) with `client_id` + `client_secret`.
- Grants: `authorization_code` + `refresh_token`.
- Callback URLs (route mirrors the existing `/api/1/proconnect/auth` convention in udata):
  - Prod: `https://www.data.gouv.fr/api/1/geopf/auth`
  - Demo: `https://demo.data.gouv.fr/api/1/geopf/auth`
  - Dev: `https://dev.data.gouv.fr/api/1/geopf/auth`
  - Local dev: `http://dev.local:7000/api/1/geopf/auth`
- Scopes: "default" — confirmed by geopf, the user's own rights on geopf apply.

## Token lifecycle

- **Access token TTL:** 12h.
- **Refresh token:** sliding 12h. As long as data.gouv.fr refreshes (or the user acts) within any 12h window, the link stays alive indefinitely. After 12h of inactivity, the user re-consents (to be confirmed).
- **Storage:** server-side in udata, encrypted, scoped per data.gouv.fr user. Tokens never reach the browser.
- **Revocation:** a "Disconnect from Géoplateforme" action wipes the stored tokens; the user can re-link any time.

### Note on token storage

RFC 6819: OAuth 2.0 Threat Model and Security Considerations https://www.rfc-editor.org/info/rfc6819/

https://www.rfc-editor.org/info/rfc6819/#section-5.1.4.1.4

    5.1.4.1.4.  Encryption of Credentials

    For client applications, insecurely persisted client credentials are
    easy targets for attackers to obtain.  Store client credentials using
    an encrypted persistence mechanism such as a keystore or database.
    Note that compiling client credentials directly into client code
    makes client applications vulnerable to scanning as well as difficult
    to administer should client credentials change over time.


Testing for OAuth Client Weaknesses https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/05.2-Testing_for_OAuth_Client_Weaknesses

    Confidential clients should store tokens in volatile memory to prevent access through other attacks such as local file inclusion, attackers who are able to access the environment, or SQL Injection attacks.

Volatile memory storage seems impratical re udata architecture, we probably can go with oauth2 recommendation and encrypt in db.

## Non-goals (for v1)

- **Backend async beyond 12h inactivity.** The sliding refresh covers normal usage; long-idle background republish needs `offline_access` and is deferred.
- **Identity stitching with proconnect infos.** The refresh_token itself binds the data.gouv.fr user to their geopf identity. Display niceties ("connected as xxx@…") can be done with a `userinfo` call.
- **ProConnect-level federation.** Not applicable — ProConnect is authentication-only and doesn't broker SP-to-SP API access.

## Open items for follow-up with geopf

- NOW: Provide the test client + register our dev/preprod/prod callback URLs.
- NOW: Confirm the refresh_token policy is sliding (not absolute) 12h.
- LATER: Confirm whether `offline_access` scope is available if we later need long-idle backend async.
