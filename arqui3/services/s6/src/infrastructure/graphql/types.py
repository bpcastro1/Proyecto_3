from datetime import datetime
from typing import Optional, Dict, Any, List
import strawberry
from ...domain.entities.selection import SelectionStatus, SelectionDecision

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