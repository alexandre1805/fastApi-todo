import urllib.parse

from fastapi import HTTPException, Security, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID
from pydantic import Json
from settings import KEYCLOAK_CLIENT_ID, KEYCLOAK_REALM, KEYCLOAK_URL

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=urllib.parse.urljoin(
        KEYCLOAK_URL, f"/realms/${KEYCLOAK_REALM}/protocol/openid-connect/auth"
    ),
    tokenUrl=urllib.parse.urljoin(
        KEYCLOAK_URL, f"/realms/${KEYCLOAK_REALM}/protocol/openid-connect/token"
    ),
    refreshUrl=urllib.parse.urljoin(
        KEYCLOAK_URL, f"/realms/${KEYCLOAK_REALM}/protocol/openid-connect/token"
    ),
)

keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_URL,
    client_id=KEYCLOAK_CLIENT_ID,
    realm_name=KEYCLOAK_REALM,
)


async def get_auth(token: str = Security(oauth2_scheme)) -> Json:
    try:
        return keycloak_openid.decode_token(token, validate=True)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),  # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
