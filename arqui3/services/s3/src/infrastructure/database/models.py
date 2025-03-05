from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ARRAY, Text
from .config import Base

class CandidateModel(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, index=True)
    resume_url = Column(String(500), nullable=False)
    vacancy_id = Column(Integer, nullable=False, index=True)
    application_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String(20), nullable=False, default="PENDING")
    skills = Column(ARRAY(String), nullable=False, default=list)
    experience_years = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow) 