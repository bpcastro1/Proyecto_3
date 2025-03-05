from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from zoneinfo import ZoneInfo

class InterviewStatus:
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"

class InterviewType:
    TECHNICAL = "TECHNICAL"
    HR = "HR"
    CULTURAL_FIT = "CULTURAL_FIT"
    FINAL = "FINAL"

class InterviewFeedback(BaseModel):
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    technical_score: Optional[float] = Field(None, ge=0, le=100)
    communication_score: Optional[float] = Field(None, ge=0, le=100)
    cultural_fit_score: Optional[float] = Field(None, ge=0, le=100)
    recommendation: Optional[str] = None
    notes: Optional[str] = None

class Interview(BaseModel):
    id: Optional[int] = None
    candidate_id: int = Field(..., gt=0)
    interviewer_id: int = Field(..., gt=0)
    vacancy_id: int = Field(..., gt=0)
    interview_type: str = Field(...)
    scheduled_time: datetime
    duration_minutes: int = Field(..., ge=30, le=180)
    location: Optional[str] = None  # Puede ser presencial o un link de videollamada
    feedback: Optional[InterviewFeedback] = None
    status: str = Field(default=InterviewStatus.SCHEDULED)
    created_at: datetime = Field(default_factory=lambda: datetime.now(ZoneInfo("UTC")))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(ZoneInfo("UTC")))

    @validator("scheduled_time")
    def validate_scheduled_time(cls, scheduled_time: datetime) -> datetime:
        # Asegurar que la fecha tenga zona horaria UTC
        if scheduled_time.tzinfo is None:
            scheduled_time = scheduled_time.replace(tzinfo=ZoneInfo("UTC"))
        elif scheduled_time.tzinfo != ZoneInfo("UTC"):
            scheduled_time = scheduled_time.astimezone(ZoneInfo("UTC"))
        return scheduled_time

    @validator("interview_type")
    def validate_type(cls, v):
        if v not in [
            InterviewType.TECHNICAL,
            InterviewType.HR,
            InterviewType.CULTURAL_FIT,
            InterviewType.FINAL
        ]:
            raise ValueError("Tipo de entrevista no válido")
        return v

    @validator("status")
    def validate_status(cls, v):
        if v not in [
            InterviewStatus.SCHEDULED,
            InterviewStatus.IN_PROGRESS,
            InterviewStatus.COMPLETED,
            InterviewStatus.CANCELLED,
            InterviewStatus.NO_SHOW
        ]:
            raise ValueError("Estado de entrevista no válido")
        return v

    def is_valid(self) -> bool:
        """Verifica si la entrevista contiene toda la información requerida."""
        return all([
            self.candidate_id > 0,
            self.interviewer_id > 0,
            self.vacancy_id > 0,
            self.interview_type in [
                InterviewType.TECHNICAL,
                InterviewType.HR,
                InterviewType.CULTURAL_FIT,
                InterviewType.FINAL
            ],
            self.duration_minutes >= 30,
            self.duration_minutes <= 180,
            self.status in [
                InterviewStatus.SCHEDULED,
                InterviewStatus.IN_PROGRESS,
                InterviewStatus.COMPLETED,
                InterviewStatus.CANCELLED,
                InterviewStatus.NO_SHOW
            ]
        ])

    def can_start(self) -> bool:
        """Verifica si la entrevista puede comenzar."""
        now = datetime.now(ZoneInfo("UTC"))
        scheduled = self.scheduled_time if self.scheduled_time.tzinfo else self.scheduled_time.replace(tzinfo=ZoneInfo("UTC"))
        
        return (
            self.status == InterviewStatus.SCHEDULED and
            abs((scheduled - now).total_seconds()) <= 300  # 5 minutos antes/después
        )

    def can_submit_feedback(self) -> bool:
        """Verifica si se puede enviar feedback para la entrevista."""
        return self.status == InterviewStatus.IN_PROGRESS

    class Config:
        json_schema_extra = {
            "example": {
                "candidate_id": 1,
                "interviewer_id": 2,
                "vacancy_id": 3,
                "interview_type": "TECHNICAL",
                "scheduled_time": "2024-03-01T14:00:00Z",
                "duration_minutes": 60,
                "location": "Google Meet"
            }
        } 