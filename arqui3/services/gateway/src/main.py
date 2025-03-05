from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from .schema import schema

app = FastAPI(
    title="HR Selection Process Gateway",
    description="API Gateway para el proceso de selección de personal",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar la ruta de GraphQL
graphql_app = GraphQLRouter(
    schema,
    graphiql=True  # Habilitar la interfaz GraphiQL
)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {
        "message": "Bienvenido al Gateway del Proceso de Selección",
        "services": {
            "requisitions": "http://localhost:8001",
            "vacancies": "http://localhost:8002",
            "candidates": "http://localhost:8003",
            "evaluations": "http://localhost:8004",
            "interviews": "http://localhost:8005",
            "selections": "http://localhost:8006"
        },
        "documentation": "/docs",
        "graphql": "/graphql"
    } 