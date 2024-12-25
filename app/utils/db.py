# db.py
from settings import DATABASE_URL
from sqlmodel import Session, SQLModel, create_engine

# Créer un moteur de base de données
engine = create_engine(DATABASE_URL)


# Fonction pour créer les tables dans la base de données
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Fonction pour obtenir la session de base de données
def get_session():
    with Session(engine) as session:
        yield session
