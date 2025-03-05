from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class CandidateStatus:
    PENDING = "PENDING"
    REVIEWING = "REVIEWING"
    INTERVIEWED = "INTERVIEWED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

class Candidate(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr = Field(...)
    resume_url: str = Field(..., min_length=5)
    vacancy_id: int = Field(..., gt=0)
    application_date: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default=CandidateStatus.PENDING)
    skills: list[str] = Field(default_factory=list)
    experience_years: Optional[int] = Field(default=None, ge=0)
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def is_valid(self) -> bool:
        """Verifica si el candidato contiene toda la información requerida."""
        return all([
            len(self.name.strip()) >= 2,
            "@" in self.email,  # Validación básica de email
            len(self.resume_url) >= 5,
            self.vacancy_id > 0,
            self.status in [
                CandidateStatus.PENDING,
                CandidateStatus.REVIEWING,
                CandidateStatus.INTERVIEWED,
                CandidateStatus.ACCEPTED,
                CandidateStatus.REJECTED
            ]
        ])

    def matches_requirements(self, required_skills: list[str], min_experience: int) -> bool:
        """Verifica si el candidato cumple con los requisitos mínimos."""
        if min_experience and (not self.experience_years or self.experience_years < min_experience):
            return False
        
        if required_skills:
            candidate_skills = set(skill.lower() for skill in self.skills)
            required_skills_set = set(skill.lower() for skill in required_skills)
            return required_skills_set.issubset(candidate_skills)
        
        return True

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Juan Pérez",
                "email": "juan.perez@email.com",
                "resume_url": "https://storage.com/resumes/juan-perez-cv.pdf",
                "vacancy_id": 1,
                "skills": ["Python", "FastAPI", "PostgreSQL"],
                "experience_years": 5
            }
        } 