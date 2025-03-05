from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class RequisitionStatus:
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class Requisition(BaseModel):
    id: Optional[int] = None
    position_name: str = Field(..., min_length=1, max_length=100)
    functions: list[str] = Field(..., min_items=1)
    salary_category: str = Field(..., min_length=1)
    profile: str = Field(..., min_length=10)
    status: str = Field(default=RequisitionStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def is_valid(self) -> bool:
        """Verifica si la solicitud contiene toda la información requerida."""
        return all([
            self.position_name,
            len(self.functions) > 0,
            self.salary_category,
            len(self.profile) >= 10,
            self.status in [RequisitionStatus.PENDING, RequisitionStatus.APPROVED, RequisitionStatus.REJECTED]
        ])

    class Config:
        json_schema_extra = {
            "example": {
                "position_name": "Senior Python Developer",
                "functions": ["Desarrollo backend", "Diseño de arquitectura", "Mentoring"],
                "salary_category": "Senior",
                "profile": "Desarrollador con 5+ años de experiencia en Python",
                "status": "PENDING"
            }
        } 