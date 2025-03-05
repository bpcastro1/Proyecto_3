from datetime import datetime
from sqlalchemy import Column, Integer, String, ARRAY, DateTime
from .config import Base

class RequisitionModel(Base):
    __tablename__ = "requisitions"

    id = Column(Integer, primary_key=True, index=True)
    position_name = Column(String(100), nullable=False)
    functions = Column(ARRAY(String), nullable=False)
    salary_category = Column(String(50), nullable=False)
    profile = Column(String(500), nullable=False)
    status = Column(String(20), nullable=False, default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow) 