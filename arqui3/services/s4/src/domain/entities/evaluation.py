from datetime import datetime
from typing import Optional, List, Dict, Any

class TestType:
    PSYCHOMETRIC = "PSYCHOMETRIC"
    TECHNICAL = "TECHNICAL"
    LANGUAGE = "LANGUAGE"
    PERSONALITY = "PERSONALITY"

class EvaluationStatus:
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Evaluation:
    def __init__(
        self,
        candidate_id: int,
        vacancy_id: int,
        tests: List[Dict[str, Any]],
        id: Optional[int] = None,
        scores: Optional[List[Dict[str, Any]]] = None,
        comments: Optional[str] = None,
        status: str = EvaluationStatus.PENDING,
        assigned_date: Optional[datetime] = None,
        completion_date: Optional[datetime] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.candidate_id = candidate_id
        self.vacancy_id = vacancy_id
        self.tests = tests
        self.scores = scores or []
        self.comments = comments
        self.status = status
        self.assigned_date = assigned_date or datetime.utcnow()
        self.completion_date = completion_date
        self.created_at = created_at or datetime.utcnow()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Evaluation':
        return cls(
            id=data.get("id"),
            candidate_id=data["candidate_id"],
            vacancy_id=data["vacancy_id"],
            tests=data.get("tests", []),
            scores=data.get("scores", []),
            status=data.get("status", EvaluationStatus.PENDING),
            assigned_date=data.get("assigned_date"),
            completion_date=data.get("completion_date"),
            created_at=data.get("created_at")
        )

    def is_completed(self) -> bool:
        completed_tests = {score["test_name"] for score in self.scores}
        return len(completed_tests) == len(self.tests)

    def has_passed(self) -> bool:
        if not self.is_completed():
            return False
        
        scores_dict = {score["test_name"]: score["score"] for score in self.scores}
        return all(
            scores_dict.get(test["name"], 0) >= test["min_score_required"]
            for test in self.tests
        )

    def is_valid(self) -> bool:
        """Verifica si la evaluación contiene toda la información requerida."""
        return all([
            self.candidate_id > 0,
            self.vacancy_id > 0,
            len(self.tests) > 0,
            self.status in [
                EvaluationStatus.PENDING,
                EvaluationStatus.IN_PROGRESS,
                EvaluationStatus.COMPLETED,
                EvaluationStatus.FAILED
            ]
        ])

    def can_submit_result(self, test_name: str, score: float) -> bool:
        """Verifica si se puede enviar el resultado de una prueba."""
        if self.status not in [EvaluationStatus.PENDING, EvaluationStatus.IN_PROGRESS]:
            return False
        
        test = next((t for t in self.tests if t["name"] == test_name), None)
        if not test:
            return False

        return 0 <= score <= 100

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "candidate_id": 1,
                "vacancy_id": 1,
                "tests": [
                    {
                        "name": "Razonamiento Lógico",
                        "type": "PSYCHOMETRIC",
                        "duration_minutes": 60,
                        "min_score_required": 70
                    },
                    {
                        "name": "Python Skills",
                        "type": "TECHNICAL",
                        "duration_minutes": 120,
                        "min_score_required": 80
                    }
                ]
            }
        } 