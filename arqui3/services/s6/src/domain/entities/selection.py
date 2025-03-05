from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class SelectionStatus:
    PENDING = "PENDING"
    IN_REVIEW = "IN_REVIEW"
    SELECTED = "SELECTED"
    REJECTED = "REJECTED"

class SelectionDecision:
    HIRE = "HIRE"
    NO_HIRE = "NO_HIRE"
    ON_HOLD = "ON_HOLD"

class Selection(BaseModel):
    id: Optional[int] = None
    vacancy_id: int = Field(..., gt=0)
    candidate_id: int = Field(..., gt=0)
    report: Optional[dict] = Field(default_factory=dict)
    decision: Optional[str] = None
    status: str = Field(default=SelectionStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def is_valid(self) -> bool:
        """Verifica si la selección contiene toda la información requerida."""
        return all([
            self.vacancy_id > 0,
            self.candidate_id > 0,
            self.status in [
                SelectionStatus.PENDING,
                SelectionStatus.IN_REVIEW,
                SelectionStatus.SELECTED,
                SelectionStatus.REJECTED
            ],
            not self.decision or self.decision in [
                SelectionDecision.HIRE,
                SelectionDecision.NO_HIRE,
                SelectionDecision.ON_HOLD
            ]
        ])

    def can_generate_report(self) -> bool:
        """Verifica si se puede generar el reporte final."""
        return self.status in [SelectionStatus.IN_REVIEW, SelectionStatus.PENDING]

    def can_make_decision(self) -> bool:
        """Verifica si se puede tomar una decisión."""
        return self.status == SelectionStatus.IN_REVIEW and bool(self.report)

    class Config:
        json_schema_extra = {
            "example": {
                "vacancy_id": 1,
                "candidate_id": 1,
                "report": {
                    "technical_evaluation": {
                        "score": 85,
                        "feedback": "Excelente conocimiento técnico"
                    },
                    "hr_evaluation": {
                        "score": 90,
                        "feedback": "Buena comunicación y actitud"
                    }
                },
                "status": "IN_REVIEW"
            }
        } 