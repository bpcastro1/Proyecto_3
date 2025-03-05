from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from ..controllers.recruitment_controller import RecruitmentController

router = APIRouter(prefix="/candidates", tags=["Candidatos"])

# Modelos de datos
class CandidateInput(BaseModel):
    name: str
    email: str
    resume_url: str
    vacancy_id: int
    skills: List[str]
    experience_years: int

class CandidateFilterInput(BaseModel):
    vacancy_id: int
    status: Optional[str] = None
    required_skills: Optional[List[str]] = None
    min_experience: Optional[int] = None

# Dependencia para obtener el controlador
def get_controller():
    return RecruitmentController()

@router.post("/", status_code=201)
async def register_candidate(
    candidate: CandidateInput,
    controller: RecruitmentController = Depends(get_controller)
):
    """Registra un nuevo candidato para una vacante"""
    result = await controller.register_candidate(
        candidate.name,
        candidate.email,
        candidate.resume_url,
        candidate.vacancy_id,
        candidate.skills,
        candidate.experience_years
    )
    
    if not result:
        raise HTTPException(
            status_code=400, 
            detail="No se pudo registrar el candidato. Verifica que la vacante exista y esté publicada."
        )
        
    return result

@router.get("/{candidate_id}")
async def get_candidate(
    candidate_id: int,
    controller: RecruitmentController = Depends(get_controller)
):
    """Obtiene un candidato por su ID"""
    result = controller.candidate_service.get_candidate(candidate_id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Candidato {candidate_id} no encontrado")
        
    return result

@router.get("/vacancy/{vacancy_id}")
async def list_candidates_by_vacancy(
    vacancy_id: int,
    controller: RecruitmentController = Depends(get_controller)
):
    """Lista todos los candidatos para una vacante"""
    result = controller.candidate_service.list_candidates_by_vacancy(vacancy_id)
    return result

@router.post("/filter")
async def filter_candidates(
    filters: CandidateFilterInput,
    controller: RecruitmentController = Depends(get_controller)
):
    """Filtra candidatos según criterios"""
    result = controller.candidate_service.filter_candidates(
        filters.vacancy_id,
        filters.status,
        filters.required_skills,
        filters.min_experience
    )
    return result 