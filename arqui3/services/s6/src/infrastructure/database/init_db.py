import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from src.infrastructure.database.config import DATABASE_URL
from src.infrastructure.database.models import Base

def init_db():
    # Crear el engine sin asyncpg para la inicialización
    sync_db_url = DATABASE_URL.replace('+asyncpg', '')
    
    # Crear la base de datos si no existe
    if not database_exists(sync_db_url):
        create_database(sync_db_url)
        print("Base de datos creada.")
    
    # Crear el engine y las tablas
    engine = create_engine(sync_db_url)
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas correctamente.")

if __name__ == "__main__":
    init_db()
    print("Base de datos inicializada correctamente.") 