from datetime import datetime
from typing import List, Optional
import strawberry
from ...domain.entities.candidate import CandidateStatus

@strawberry.type
class Candidate:
    id: Optional[int]
    name: str
    email: str
    resume_url: str
    vacancy_id: int
    application_date: datetime
    status: str
    skills: List[str]
    experience_years: Optional[int]
    notes: Optional[str]
    created_at: datetime

@strawberry.input
class CandidateInput:
    name: str
    email: str
    resume_url: str
    vacancy_id: int
    skills: List[str]
    experience_years: Optional[int] = None

@strawberry.input
class CandidateFilterInput:
    vacancy_id: Optional[int] = None
    status: Optional[str] = None
    required_skills: Optional[List[str]] = None
    min_experience: Optional[int] = None 