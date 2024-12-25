import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM")
