from datetime import datetime
from sqlalchemy import Column, Integer, String, JSON, DateTime
from .config import Base
from ...domain.entities.selection import SelectionStatus, SelectionDecision

class SelectionModel(Base):
    __tablename__ = "selections"

    id = Column(Integer, primary_key=True, index=True)
    vacancy_id = Column(Integer, nullable=False)
    candidate_id = Column(Integer, nullable=False)
    report = Column(JSON, nullable=True)
    decision = Column(String(20), nullable=True)
    status = Column(String(20), nullable=False, default=SelectionStatus.PENDING)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow) 