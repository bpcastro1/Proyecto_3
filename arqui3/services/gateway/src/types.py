from typing import List, Optional
from datetime import datetime
import strawberry

# Tipos para Requisiciones (s1)
@strawberry.type
class Requisition:
    id: Optional[int]
    position_name: str
    functions: List[str]
    salary_category: str
    profile: str
    status: str
    created_at: datetime

@strawberry.input
class RequisitionInput:
    position_name: str
    functions: List[str]
    salary_category: str
    profile: str

# Tipos para Vacantes (s2)
@strawberry.type
class Vacancy:
    id: Optional[int]
    requisition_id: int
    platforms: List[str]
    status: str
    publication_date: Optional[datetime]
    closing_date: Optional[datetime]
    created_at: datetime

@strawberry.input
class VacancyInput:
    requisition_id: int
    platforms: List[str]

# Tipos para Candidatos (s3)
@strawberry.type
class Candidate:
    id: Optional[int]
    name: str
    email: str
    resume_url: str
    vacancy_id: int
    status: str
    skills: List[str]
    experience_years: Optional[int]
    application_date: datetime
    created_at: datetime

@strawberry.input
class CandidateInput:
    name: str
    email: str
    resume_url: str
    vacancy_id: int
    skills: List[str]
    experience_years: Optional[int]

# Tipos para Evaluaciones (s4)
@strawberry.type
class Test:
    name: str
    type: str
    duration_minutes: int
    min_score_required: float

@strawberry.type
class TestScore:
    test_name: str
    score: float

@strawberry.type
class Evaluation:
    id: Optional[int]
    candidate_id: int
    vacancy_id: int
    tests: List[Test]
    scores: List[TestScore]
    status: str
    assigned_date: datetime
    completion_date: Optional[datetime]
    created_at: datetime

@strawberry.input
class TestInput:
    name: str
    type: str
    duration_minutes: int
    min_score_required: float

@strawberry.input
class EvaluationInput:
    candidate_id: int
    vacancy_id: int
    tests: List[TestInput]

# Tipos para Entrevistas (s5)
@strawberry.type
class InterviewFeedback:
    strengths: List[str]
    weaknesses: List[str]
    technical_score: Optional[float]
    communication_score: Optional[float]
    cultural_fit_score: Optional[float]
    recommendation: Optional[str]
    notes: Optional[str]

@strawberry.type
class Interview:
    id: Optional[int]
    candidate_id: int
    interviewer_id: int
    vacancy_id: int
    interview_type: str
    scheduled_time: datetime
    duration_minutes: int
    location: Optional[str]
    feedback: Optional[InterviewFeedback]
    status: str
    created_at: datetime

@strawberry.input
class InterviewInput:
    candidate_id: int
    interviewer_id: int
    vacancy_id: int
    interview_type: str
    scheduled_time: datetime
    duration_minutes: int
    location: Optional[str]

# Tipos para Selección (s6)
@strawberry.type
class EvaluationScore:
    score: float
    feedback: str

@strawberry.type
class SelectionReport:
    technical_evaluation: Optional[EvaluationScore]
    hr_evaluation: Optional[EvaluationScore]
    additional_notes: Optional[str]

@strawberry.type
class Selection:
    id: Optional[int]
    vacancy_id: int
    candidate_id: int
    report: Optional[SelectionReport]
    decision: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

@strawberry.input
class EvaluationScoreInput:
    score: float
    feedback: str

@strawberry.input
class ReportInput:
    technical_evaluation: Optional[EvaluationScoreInput]
    hr_evaluation: Optional[EvaluationScoreInput]
    additional_notes: Optional[str]

@strawberry.input
class SelectionInput:
    vacancy_id: int
    candidate_id: int 