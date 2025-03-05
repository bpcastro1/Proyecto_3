from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from .infrastructure.graphql.schema import schema
from .infrastructure.database.config import get_session
from .infrastructure.events.kafka_producer import KafkaProducer

app = FastAPI(title="Vacancy Service")

# Crear instancia del productor de Kafka
kafka_producer = KafkaProducer()

@app.on_event("startup")
async def startup_event():
    await kafka_producer.start()

@app.on_event("shutdown")
async def shutdown_event():
    await kafka_producer.stop()

graphql_app = GraphQLRouter(
    schema,
    context_getter=lambda: {
        "session": get_session(),
        "kafka_producer": kafka_producer
    }
)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {"message": "Bienvenido al Servicio de Vacantes"} 