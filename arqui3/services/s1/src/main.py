from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from .infrastructure.graphql.schema import schema
from .infrastructure.database.config import get_session

app = FastAPI(title="Requisition Service")

graphql_app = GraphQLRouter(
    schema,
    context_getter=lambda: {"session": get_session()}
)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {"message": "Bienvenido al Servicio de Requisiciones"} 