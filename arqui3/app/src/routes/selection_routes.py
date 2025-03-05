from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict
from ..controllers.recruitment_controller import RecruitmentController

router = APIRouter(prefix="/selection", tags=["Selección"])

# Modelos de datos
class EvaluationDetail(BaseModel):
    score: float
    feedback: str

class ReportInput(BaseModel):
    selection_id: int
    technical_evaluation: EvaluationDetail
    hr_evaluation: EvaluationDetail
    additional_notes: Optional[str] = ""

class DecisionInput(BaseModel):
    selection_id: int
    decision: str  # HIRE, REJECT
    reason: Optional[str] = ""

# Dependencia para obtener el controlador
def get_controller():
    return RecruitmentController()

@router.post("/reports", status_code=201)
async def generate_final_report(
    report: ReportInput,
    controller: RecruitmentController = Depends(get_controller)
):
    """Genera el reporte final para un proceso de selección"""
    result = await controller.generate_selection_report(
        report.selection_id,
        report.technical_evaluation.dict(),
        report.hr_evaluation.dict(),
        report.additional_notes
    )
    
    if not result:
        raise HTTPException(
            status_code=400, 
            detail="No se pudo generar el reporte. Verifica que el proceso de selección exista."
        )
        
    return result

@router.post("/decision", status_code=200)
async def make_hiring_decision(
    decision: DecisionInput,
    controller: RecruitmentController = Depends(get_controller)
):
    """Registra la decisión final de contratación"""
    result = await controller.make_final_decision(
        decision.selection_id,
        decision.decision,
        decision.reason
    )
    
    if not result:
        raise HTTPException(
            status_code=400, 
            detail="No se pudo registrar la decisión. Verifica que el proceso de selección exista."
        )
        
    return result

@router.get("/vacancy/{vacancy_id}")
async def get_selection_process(
    vacancy_id: int,
    controller: RecruitmentController = Depends(get_controller)
):
    """Obtiene la información de un proceso de selección por ID de vacante"""
    result = controller.selection_service.get_selection_process(vacancy_id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Proceso de selección para la vacante {vacancy_id} no encontrado")
        
    return result

@router.get("/")
async def list_selection_processes(
    status: Optional[str] = None,
    controller: RecruitmentController = Depends(get_controller)
):
    """Lista todos los procesos de selección, opcionalmente filtrados por estado"""
    result = controller.selection_service.list_selection_processes(status)
    return result 