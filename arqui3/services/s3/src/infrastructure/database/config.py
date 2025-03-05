from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# URL para la base de datos principal
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5434/candidates_db")

# URL para la base de datos por defecto (postgres)
DEFAULT_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5434/postgres"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Ya no necesitamos el get_session ya que usaremos async_session directamente 