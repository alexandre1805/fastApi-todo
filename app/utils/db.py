# db.py
import os
from sqlmodel import Session, create_engine, SQLModel
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer l'URL de la base de données depuis les variables d'environnement
DATABASE_URL = os.getenv("DATABASE_URL")

# Créer un moteur de base de données
engine = create_engine(DATABASE_URL, echo=True)

# Fonction pour créer les tables dans la base de données
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Fonction pour obtenir la session de base de données
def get_session():
    with Session(engine) as session:
        yield session
