from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager
from .infrastructure.database.config import get_session
from .infrastructure.events.kafka_producer import KafkaProducer
from .infrastructure.graphql.schema import schema

# Inicializar el productor de Kafka
kafka_producer = KafkaProducer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Iniciar el productor de Kafka
    await kafka_producer.start()
    yield
    # Detener el productor de Kafka al cerrar
    await kafka_producer.stop()

app = FastAPI(
    title="Selection Service",
    description="Servicio para gestionar la selección de candidatos",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar el contexto de GraphQL
async def get_context():
    async for session in get_session():
        yield {
            "session": session,
            "kafka_producer": kafka_producer
        }

# Configurar la ruta de GraphQL
graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
    graphiql=True
)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {
        "message": "Bienvenido al servicio de selección",
        "docs": "/docs",
        "graphql": "/graphql"
    } 