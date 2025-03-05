import asyncio
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine
from .config import DATABASE_URL, DEFAULT_DATABASE_URL, Base
from ..database.models import CandidateModel

async def create_database():
    try:
        # Intentar conectar a la base de datos postgres
        conn = await asyncpg.connect(
            user="postgres",
            password="postgres",
            host="localhost",
            port="5434",
            database="postgres"
        )
        
        # Verificar si la base de datos ya existe
        result = await conn.fetch(
            "SELECT 1 FROM pg_database WHERE datname = $1",
            "candidates_db"
        )
        
        if not result:
            # Crear la base de datos si no existe
            await conn.execute("CREATE DATABASE candidates_db")
            print("Base de datos 'candidates_db' creada exitosamente")
        else:
            print("La base de datos 'candidates_db' ya existe")
            
    except Exception as e:
        print(f"Error al crear la base de datos: {str(e)}")
        raise
    finally:
        await conn.close()

async def create_tables():
    try:
        # Crear el engine con la nueva base de datos
        engine = create_async_engine(DATABASE_URL, echo=True)
        
        async with engine.begin() as conn:
            # Crear todas las tablas
            await conn.run_sync(Base.metadata.create_all)
            print("Tablas creadas exitosamente")
            
    except Exception as e:
        print(f"Error al crear las tablas: {str(e)}")
        raise

async def init_db():
    print("Iniciando la creación de la base de datos...")
    await create_database()
    print("Iniciando la creación de las tablas...")
    await create_tables()
    print("Inicialización completada")

def main():
    try:
        asyncio.run(init_db())
        print("Proceso completado exitosamente")
    except Exception as e:
        print(f"Error durante la inicialización: {str(e)}")
        raise

if __name__ == "__main__":
    main() 