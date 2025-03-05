from typing import List, Optional
import strawberry
from datetime import datetime
from src.domain.models import TestType, EvaluationStatus

@strawberry.type
class PsychometricResultType:
    id: int
    evaluation_id: int
    personality_traits: Optional[str] = None
    cognitive_score: Optional[float] = None
    emotional_intelligence: Optional[float] = None
    created_at: str

@strawberry.type
class TechnicalResultType:
    id: int
    evaluation_id: int
    programming_score: Optional[float] = None
    problem_solving_score: Optional[float] = None
    technical_knowledge: Optional[str] = None
    created_at: str

@strawberry.type
class EvaluationType:
    id: int
    candidate_id: int
    test_type: TestType
    status: EvaluationStatus
    score: Optional[float] = None
    feedback: Optional[str] = None
    created_at: str
    updated_at: str

@strawberry.input
class EvaluationInput:
    candidate_id: int
    test_type: TestType

@strawberry.input
class PsychometricResultInput:
    evaluation_id: int
    personality_traits: Optional[str] = None
    cognitive_score: Optional[float] = None
    emotional_intelligence: Optional[float] = None

@strawberry.input
class TechnicalResultInput:
    evaluation_id: int
    programming_score: Optional[float] = None
    problem_solving_score: Optional[float] = None
    technical_knowledge: Optional[str] = None 