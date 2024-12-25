from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from utils.db import create_db_and_tables

app = FastAPI(
    title="Todo API", version="1.0.0", swagger_ui_init_oauth={"clientId": "todo-front"}
)

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_db_and_tables()

app.include_router(router)
