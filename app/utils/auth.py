import urllib.parse

import settings
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID
from pydantic import BaseModel, Json
from settings import KEYCLOAK_CLIENT_ID, KEYCLOAK_REALM, KEYCLOAK_URL


class User(BaseModel):
    id: str
    username: str
    email: str
    first_name: str
    last_name: str
    client_roles: list


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=urllib.parse.urljoin(
        KEYCLOAK_URL, f"/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth"
    ),
    tokenUrl=urllib.parse.urljoin(
        KEYCLOAK_URL, f"/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
    ),
    refreshUrl=urllib.parse.urljoin(
        KEYCLOAK_URL, f"/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
    ),
)

keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_URL,
    client_id=KEYCLOAK_CLIENT_ID,
    realm_name=KEYCLOAK_REALM,
)


async def get_auth(token: str = Security(oauth2_scheme)) -> Json:
    try:
        return keycloak_openid.decode_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="L'authentification a echoué.",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_user(payload: dict = Depends(get_auth)) -> User:
    try:
        return User(
            id=payload.get("sub"),
            username=payload.get("preferred_username"),
            email=payload.get("email"),
            first_name=payload.get("given_name"),
            last_name=payload.get("family_name"),
            client_roles=payload.get("resource_access", {})
            .get(settings.KEYCLOAK_CLIENT_ID, {})
            .get("roles", []),
        )
    except Exception as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exception),
            headers={"WWW-Authenticate": "Bearer"},
        )
