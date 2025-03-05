# Este archivo marca el directorio como un paquete Python 
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = "evaluation_service"  # Nombre fijo de la base de datos
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# Primero nos conectamos a la base de datos por defecto 'postgres' para crear nuestra base de datos
default_connection_string = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/postgres"

def create_database():
    try:
        # Conectar a la base de datos postgres
        conn = psycopg2.connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Verificar si la base de datos existe
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{POSTGRES_DB}'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f'CREATE DATABASE {POSTGRES_DB}')
            print(f"Base de datos {POSTGRES_DB} creada exitosamente")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error al crear la base de datos: {e}")
        raise e

# Crear la base de datos si no existe
create_database()

# Ahora nos conectamos a nuestra base de datos
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 