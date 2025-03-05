from datetime import datetime
from typing import List, Optional, Dict, Any
import strawberry
from src.domain.entities.evaluation import TestType, EvaluationStatus

@strawberry.type
class TestScore:
    test_name: str
    score: float
    comments: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TestScore":
        return cls(
            test_name=data["test_name"],
            score=data["score"],
            comments=data.get("comments")
        )

@strawberry.type
class Test:
    name: str
    type: str
    duration_minutes: int
    min_score_required: float

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Test":
        return cls(
            name=data["name"],
            type=data["type"],
            duration_minutes=data["duration_minutes"],
            min_score_required=data["min_score_required"]
        )

@strawberry.input
class TestInput:
    name: str
    type: str
    duration_minutes: int
    min_score_required: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type,
            "duration_minutes": self.duration_minutes,
            "min_score_required": self.min_score_required
        }

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

    @classmethod
    def from_domain(cls, evaluation_dict: Dict[str, Any]) -> "Evaluation":
        return cls(
            id=evaluation_dict.get("id"),
            candidate_id=evaluation_dict["candidate_id"],
            vacancy_id=evaluation_dict["vacancy_id"],
            tests=[Test.from_dict(test) for test in evaluation_dict.get("tests", [])],
            scores=[TestScore.from_dict(score) for score in evaluation_dict.get("scores", [])],
            status=evaluation_dict.get("status", EvaluationStatus.PENDING),
            assigned_date=evaluation_dict.get("assigned_date", datetime.utcnow()),
            completion_date=evaluation_dict.get("completion_date"),
            created_at=evaluation_dict.get("created_at", datetime.utcnow())
        )

@strawberry.input
class EvaluationInput:
    candidate_id: int
    vacancy_id: int
    tests: List[TestInput]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "vacancy_id": self.vacancy_id,
            "tests": [test.to_dict() for test in self.tests]
        }

@strawberry.input
class TestResultInput:
    evaluation_id: int
    test_name: str
    score: float
    comments: Optional[str] = None 