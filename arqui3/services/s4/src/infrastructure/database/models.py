from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, Float, ForeignKey
from sqlalchemy.orm import relationship
from .config import Base

class EvaluationModel(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, nullable=False, index=True)
    vacancy_id = Column(Integer, nullable=False, index=True)
    tests = Column(JSON, nullable=False)  # Lista de pruebas asignadas
    scores = Column(JSON, nullable=True)  # {test_name: score}
    comments = Column(String, nullable=True)
    status = Column(String(20), nullable=False, default="PENDING")
    assigned_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    completion_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow) 