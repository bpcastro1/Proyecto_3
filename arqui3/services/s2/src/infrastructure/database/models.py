from datetime import datetime
from sqlalchemy import Column, Integer, String, ARRAY, DateTime
from .config import Base

class VacancyModel(Base):
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True, index=True)
    requisition_id = Column(Integer, nullable=False)
    platforms = Column(ARRAY(String), nullable=False)
    status = Column(String(20), nullable=False, default="DRAFT")
    publication_date = Column(DateTime, nullable=True)
    closing_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow) 