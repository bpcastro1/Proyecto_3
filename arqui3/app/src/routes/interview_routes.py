from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from ..controllers.recruitment_controller import RecruitmentController

router = APIRouter(prefix="/interviews", tags=["Entrevistas"])

# Modelos de datos
class InterviewInput(BaseModel):
    candidate_id: int
    interviewer_id: int
    vacancy_id: int
    interview_type: str  # TECHNICAL, HR, CULTURAL
    scheduled_time: str  # ISO format
    duration_minutes: int
    location: str

class FeedbackInput(BaseModel):
    interview_id: int
    strengths: List[str]
    weaknesses: List[str]
    technical_score: int
    communication_score: int
    culture_fit_score: int
    recommendation: str  # HIRE, REJECT, CONSIDER
    notes: Optional[str] = ""

# Dependencia para obtener el controlador
def get_controller():
    return RecruitmentController()

@router.post("/", status_code=201)
async def schedule_interview(
    interview: InterviewInput,
    controller: RecruitmentController = Depends(get_controller)
):
    """Programa una entrevista para un candidato"""
    result = await controller.schedule_candidate_interview(
        interview.candidate_id,
        interview.interviewer_id,
        interview.vacancy_id,
        interview.interview_type,
        interview.scheduled_time,
        interview.duration_minutes,
        interview.location
    )
    
    if not result:
        raise HTTPException(
            status_code=400, 
            detail="No se pudo programar la entrevista. Verifica que el candidato exista."
        )
        
    return result

@router.post("/feedback", status_code=200)
async def submit_feedback(
    feedback: FeedbackInput,
    controller: RecruitmentController = Depends(get_controller)
):
    """Registra el feedback de una entrevista"""
    result = await controller.register_interview_feedback(
        feedback.interview_id,
        feedback.strengths,
        feedback.weaknesses,
        feedback.technical_score,
        feedback.communication_score,
        feedback.culture_fit_score,
        feedback.recommendation,
        feedback.notes
    )
    
    if not result:
        raise HTTPException(
            status_code=400, 
            detail="No se pudo registrar el feedback. Verifica que la entrevista exista."
        )
        
    return result

@router.get("/{interview_id}")
async def get_interview(
    interview_id: int,
    controller: RecruitmentController = Depends(get_controller)
):
    """Obtiene una entrevista por su ID"""
    result = controller.interview_service.get_interview(interview_id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Entrevista {interview_id} no encontrada")
        
    return result

@router.get("/candidate/{candidate_id}")
async def list_interviews_by_candidate(
    candidate_id: int,
    controller: RecruitmentController = Depends(get_controller)
):
    """Lista todas las entrevistas de un candidato"""
    result = controller.interview_service.list_interviews_by_candidate(candidate_id)
    return result 