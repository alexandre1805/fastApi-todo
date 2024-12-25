import settings
from fastapi import FastAPI
from routes import router
from utils.db import create_db_and_tables

app = FastAPI(
    title="Todo API",
    version="1.0.0",
    swagger_ui_init_oauth={"clientId": settings.KEYCLOAK_CLIENT_ID},
)

create_db_and_tables()

app.include_router(router)
