from fastapi import APIRouter, HTTPException, Depends, Response
from pydantic import BaseModel
from typing import List, Optional
from ..controllers.recruitment_controller import RecruitmentController

router = APIRouter(prefix="/evaluations", tags=["Evaluaciones"])

# Modelos de datos
class TestInput(BaseModel):
    name: str
    type: str  # TECHNICAL, LANGUAGE, PSYCHOMETRIC
    duration_minutes: int
    min_score_required: float

class EvaluationInput(BaseModel):
    candidate_id: int
    vacancy_id: int
    tests: List[TestInput]

class TestResultInput(BaseModel):
    evaluation_id: int
    test_name: str
    score: float
    comments: Optional[str] = ""

# Dependencia para obtener el controlador
def get_controller():
    return RecruitmentController()

@router.post("/", status_code=201)
async def assign_evaluation(
    evaluation: EvaluationInput,
    controller: RecruitmentController = Depends(get_controller)
):
    """Asigna pruebas de evaluación a un candidato"""
    result = await controller.assign_candidate_evaluation(
        evaluation.candidate_id,
        evaluation.vacancy_id,
        [test.dict() for test in evaluation.tests]
    )
    
    if not result:
        raise HTTPException(
            status_code=400, 
            detail="No se pudo asignar la evaluación. Verifica que el candidato exista."
        )
        
    return result

@router.post("/results", status_code=200)
async def submit_test_result(
    result_data: TestResultInput,
    controller: RecruitmentController = Depends(get_controller)
):
    """Registra el resultado de una prueba"""
    result = await controller.register_test_result(
        result_data.evaluation_id,
        result_data.test_name,
        result_data.score,
        result_data.comments
    )
    
    if not result:
        raise HTTPException(
            status_code=400, 
            detail="No se pudo registrar el resultado. Verifica que la evaluación exista."
        )
        
    return result

@router.get("/{evaluation_id}")
async def get_evaluation(
    evaluation_id: int,
    controller: RecruitmentController = Depends(get_controller)
):
    """Obtiene una evaluación por su ID"""
    result = controller.evaluation_service.get_evaluation(evaluation_id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Evaluación {evaluation_id} no encontrada")
        
    return result

@router.get("/candidate/{candidate_id}")
async def get_evaluations_by_candidate(
    candidate_id: int,
    controller: RecruitmentController = Depends(get_controller)
):
    """Obtiene todas las evaluaciones de un candidato"""
    result = controller.evaluation_service.get_evaluations_by_candidate(candidate_id)
    return result

@router.get("/reports/{candidate_id}/excel")
async def download_excel_report(
    candidate_id: int,
    controller: RecruitmentController = Depends(get_controller)
):
    """Descarga un reporte en Excel para un candidato"""
    try:
        file_path = controller.evaluation_service.download_excel_report(candidate_id)
        
        with open(file_path, "rb") as file:
            content = file.read()
            
        headers = {
            "Content-Disposition": f"attachment; filename=evaluation_report_{candidate_id}.xlsx"
        }
        
        return Response(
            content=content,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers=headers
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar el reporte: {str(e)}")

@router.get("/reports/{candidate_id}/pdf")
async def download_pdf_report(
    candidate_id: int,
    controller: RecruitmentController = Depends(get_controller)
):
    """Descarga un reporte en PDF para un candidato"""
    try:
        file_path = controller.evaluation_service.download_pdf_report(candidate_id)
        
        with open(file_path, "rb") as file:
            content = file.read()
            
        headers = {
            "Content-Disposition": f"attachment; filename=evaluation_report_{candidate_id}.pdf"
        }
        
        return Response(
            content=content,
            media_type="application/pdf",
            headers=headers
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar el reporte: {str(e)}") 