from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/evaluations_db"

# Crear el engine asíncrono
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

# Crear el sessionmaker asíncrono
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Crear la base declarativa
Base = declarative_base()

# Función para obtener una sesión asíncrona
@asynccontextmanager
async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close() 