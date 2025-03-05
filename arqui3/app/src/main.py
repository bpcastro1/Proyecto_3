import logging
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from .config import Config
from .routes import requisition_routes, vacancy_routes, candidate_routes
from .routes import evaluation_routes, interview_routes, selection_routes
from .kafka_client import KafkaClient

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Crear la aplicación FastAPI
app = FastAPI(
    title="Sistema de Gestión de Selección de Personal",
    description="Aplicación para gestionar el proceso de selección de personal",
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

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar plantillas
templates = Jinja2Templates(directory="templates")

# Incluir rutas
app.include_router(requisition_routes.router)
app.include_router(vacancy_routes.router)
app.include_router(candidate_routes.router)
app.include_router(evaluation_routes.router)
app.include_router(interview_routes.router)
app.include_router(selection_routes.router)

# Cliente Kafka
kafka_client = KafkaClient()

@app.on_event("startup")
async def startup_event():
    """Evento de inicio de la aplicación"""
    logger.info("Iniciando la aplicación...")
    
    # Iniciar el productor de Kafka
    await kafka_client.start_producer()
    
    # Iniciar los consumidores solo si Kafka está habilitado
    if kafka_client.kafka_enabled:
        try:
            # Registrar los consumidores para los eventos relevantes
            await kafka_client.start_consumer("requisition.created", handle_requisition_created)
            await kafka_client.start_consumer("vacancy.published", handle_vacancy_published)
            await kafka_client.start_consumer("candidate.registered", handle_candidate_registered)
        except Exception as e:
            logger.error(f"Error al iniciar consumidores: {e}")
            logger.info("La aplicación continuará funcionando sin procesamiento de eventos")
    else:
        logger.warning("Kafka no está disponible - Las funciones de eventos asíncronos están deshabilitadas")
        logger.info("La aplicación funcionará en modo manual sin procesamiento de eventos")

@app.on_event("shutdown")
async def shutdown_event():
    """Evento de cierre de la aplicación"""
    logger.info("Deteniendo la aplicación...")
    
    # Detener los consumidores y el productor de Kafka
    if kafka_client.kafka_enabled:
        await kafka_client.stop_all_consumers()
    await kafka_client.stop_producer()
    
    logger.info("Aplicación detenida correctamente")

# Manejadores de eventos Kafka
async def handle_requisition_created(message):
    """Manejar evento de requisición creada"""
    logger.info(f"Requisición creada: {message}")

async def handle_vacancy_published(message):
    """Manejar evento de vacante publicada"""
    logger.info(f"Vacante publicada: {message}")

async def handle_candidate_registered(message):
    """Manejar evento de candidato registrado"""
    logger.info(f"Candidato registrado: {message}")

@app.get("/")
async def root(request: Request):
    """Página principal"""
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "title": "Sistema de Gestión de Selección de Personal"}
    )

@app.get("/health")
async def health_check():
    """Endpoint para verificar el estado de salud de la aplicación"""
    return {"status": "ok"}

@app.get("/metrics")
async def metrics():
    """Endpoint para obtener métricas de la aplicación"""
    return {
        "services": {
            "requisition": "ok",
            "vacancy": "ok",
            "candidate": "ok",
            "evaluation": "ok",
            "interview": "ok",
            "selection": "ok"
        }
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Manejador global de excepciones"""
    logger.error(f"Error no manejado: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=Config.APP_HOST,
        port=Config.APP_PORT,
        reload=True
    ) 