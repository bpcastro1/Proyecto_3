from datetime import datetime
from typing import Optional, Dict, Any, List
import strawberry
from zoneinfo import ZoneInfo
from ...domain.entities.interview import InterviewStatus, InterviewType

@strawberry.type
class InterviewFeedback:
    strengths: List[str]
    weaknesses: List[str]
    technical_score: Optional[float]
    communication_score: Optional[float]
    cultural_fit_score: Optional[float]
    recommendation: Optional[str]
    notes: Optional[str]

@strawberry.input
class InterviewFeedbackInput:
    strengths: List[str]
    weaknesses: List[str]
    technical_score: float
    communication_score: float
    cultural_fit_score: float
    recommendation: str
    notes: Optional[str] = None

@strawberry.type
class Interview:
    id: int
    candidate_id: int
    interviewer_id: int
    vacancy_id: int
    interview_type: str
    scheduled_time: datetime
    duration_minutes: int
    location: str
    feedback: Optional[InterviewFeedback]
    status: str
    created_at: datetime
    updated_at: datetime

@strawberry.input
class InterviewInput:
    candidate_id: int
    interviewer_id: int
    vacancy_id: int
    interview_type: str
    scheduled_time: datetime
    duration_minutes: int
    location: str

    def to_dict(self) -> Dict[str, Any]:
        # Asegurarse de que la fecha tenga zona horaria UTC
        scheduled_time = self.scheduled_time

        if scheduled_time.tzinfo is None:
            scheduled_time = scheduled_time.replace(tzinfo=ZoneInfo("UTC"))
        elif scheduled_time.tzinfo != ZoneInfo("UTC"):
            scheduled_time = scheduled_time.astimezone(ZoneInfo("UTC"))

        return {
            "candidate_id": self.candidate_id,
            "interviewer_id": self.interviewer_id,
            "vacancy_id": self.vacancy_id,
            "interview_type": self.interview_type,
            "scheduled_time": scheduled_time,
            "duration_minutes": self.duration_minutes,
            "location": self.location
        }

@strawberry.input
class RescheduleInput:
    interview_id: int
    new_time: datetime
    new_duration: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "interview_id": self.interview_id,
            "new_time": self.new_time.replace(tzinfo=ZoneInfo("UTC"))
        }
        if self.new_duration is not None:
            data["new_duration"] = self.new_duration
        return data 