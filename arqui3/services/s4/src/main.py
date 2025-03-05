import os
import sys
from pathlib import Path

# Añadir el directorio src al PYTHONPATH
current_dir = Path(__file__).resolve().parent.parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.responses import FileResponse
import strawberry
from strawberry.fastapi import GraphQLRouter
from src.infrastructure.resolvers import Query, Mutation
from src.infrastructure.database import engine, get_db
from src.domain.models import Base
from src.application.report_service import ReportService
from tempfile import NamedTemporaryFile
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Servicio de Evaluación")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    try:
        # Crear las tablas en la base de datos
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas creadas exitosamente en la base de datos")
    except Exception as e:
        logger.error(f"Error al crear las tablas: {e}")
        raise

# Crear y configurar el schema GraphQL
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)

# Crear y configurar el router de GraphQL
graphql_app = GraphQLRouter(
    schema,
    graphiql=True  # Habilitar la interfaz GraphiQL
)

# Añadir las rutas
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {"message": "Servicio de Evaluación API"}

@app.post("/reports/{candidate_id}/excel")
async def generate_excel_report(candidate_id: int, db: Session = Depends(get_db)):
    try:
        report_service = ReportService(db)
        temp_file = NamedTemporaryFile(delete=False, suffix=".xlsx")
        report_service.generate_excel_report(candidate_id, temp_file.name)
        
        return FileResponse(
            temp_file.name,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=f"evaluation_report_{candidate_id}.xlsx"
        )
    except Exception as e:
        logger.error(f"Error generando reporte Excel: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if 'temp_file' in locals():
            os.unlink(temp_file.name)

@app.post("/reports/{candidate_id}/pdf")
async def generate_pdf_report(candidate_id: int, db: Session = Depends(get_db)):
    try:
        report_service = ReportService(db)
        temp_file = NamedTemporaryFile(delete=False, suffix=".pdf")
        report_service.generate_pdf_report(candidate_id, temp_file.name)
        
        return FileResponse(
            temp_file.name,
            media_type="application/pdf",
            filename=f"evaluation_report_{candidate_id}.pdf"
        )
    except Exception as e:
        logger.error(f"Error generando reporte PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if 'temp_file' in locals():
            os.unlink(temp_file.name)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004) 