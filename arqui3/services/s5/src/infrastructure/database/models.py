from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON
from .config import Base
from ...domain.entities.interview import InterviewStatus, InterviewType

class InterviewModel(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, nullable=False)
    interviewer_id = Column(Integer, nullable=False)
    vacancy_id = Column(Integer, nullable=False)
    interview_type = Column(String(20), nullable=False)
    scheduled_time = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    location = Column(String(500), nullable=True)
    feedback = Column(JSON, nullable=True)
    status = Column(String(20), nullable=False, default=InterviewStatus.SCHEDULED)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow) 