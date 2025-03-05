import asyncio
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine
from .config import DEFAULT_DATABASE_URL, DATABASE_URL
from .models import Base

async def create_database():
    try:
        conn = await asyncpg.connect(DEFAULT_DATABASE_URL)
        await conn.execute(
            "CREATE DATABASE evaluations_db"
        )
        print("Base de datos evaluations_db creada exitosamente")
    except asyncpg.exceptions.DuplicateDatabaseError:
        print("La base de datos evaluations_db ya existe")
    except Exception as e:
        print(f"Error al crear la base de datos: {str(e)}")
    finally:
        await conn.close()

async def create_tables():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas creadas exitosamente")
    await engine.dispose()

async def init_db():
    print("Iniciando creación de base de datos...")
    await create_database()
    print("Iniciando creación de tablas...")
    await create_tables()
    print("Inicialización completada")

if __name__ == "__main__":
    asyncio.run(init_db()) 