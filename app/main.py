from fastapi import FastAPI
from utils.db import create_db_and_tables
from routes import router

app = FastAPI(title="Todo API", version="1.0.0")

create_db_and_tables()

app.include_router(router)
