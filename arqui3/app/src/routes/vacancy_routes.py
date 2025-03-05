from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from ..controllers.recruitment_controller import RecruitmentController

router = APIRouter(prefix="/vacancies", tags=["Vacantes"])

# Modelos de datos
class VacancyInput(BaseModel):
    requisition_id: int
    platforms: List[str]

class VacancyCloseInput(BaseModel):
    reason: str = "FILLED"  # FILLED o CANCELLED

# Dependencia para obtener el controlador
def get_controller():
    return RecruitmentController()

@router.post("/", status_code=201)
async def publish_vacancy(
    vacancy: VacancyInput,
    controller: RecruitmentController = Depends(get_controller)
):
    """Publica una vacante para una requisición aprobada"""
    result = await controller.publish_vacancy(
        vacancy.requisition_id,
        vacancy.platforms
    )
    
    if not result:
        raise HTTPException(
            status_code=400, 
            detail="No se pudo publicar la vacante. Verifica que la requisición exista y esté aprobada."
        )
        
    return result

@router.get("/{vacancy_id}")
async def get_vacancy(
    vacancy_id: int,
    controller: RecruitmentController = Depends(get_controller)
):
    """Obtiene una vacante por su ID"""
    result = controller.vacancy_service.get_vacancy(vacancy_id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Vacante {vacancy_id} no encontrada")
        
    return result

@router.get("/")
async def list_vacancies(
    status: Optional[str] = None,
    controller: RecruitmentController = Depends(get_controller)
):
    """Lista todas las vacantes, opcionalmente filtradas por estado"""
    result = controller.vacancy_service.list_vacancies(status)
    return result

@router.post("/{vacancy_id}/close")
async def close_vacancy(
    vacancy_id: int,
    close_data: VacancyCloseInput,
    controller: RecruitmentController = Depends(get_controller)
):
    """Cierra una vacante sin contratar a ningún candidato"""
    result = await controller.close_vacancy_without_hiring(
        vacancy_id,
        close_data.reason
    )
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Vacante {vacancy_id} no encontrada o no se pudo cerrar")
        
    return result 