from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class VacancyStatus:
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    CLOSED = "CLOSED"

class Platform:
    LINKEDIN = "LINKEDIN"
    INDEED = "INDEED"
    GLASSDOOR = "GLASSDOOR"
    COMPANY_WEBSITE = "COMPANY_WEBSITE"

class Vacancy(BaseModel):
    id: Optional[int] = None
    requisition_id: int = Field(..., gt=0)
    platforms: List[str] = Field(..., min_items=1)
    status: str = Field(default=VacancyStatus.DRAFT)
    publication_date: Optional[datetime] = None
    closing_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def is_valid(self) -> bool:
        """Verifica si la vacante contiene toda la información requerida."""
        return all([
            self.requisition_id > 0,
            len(self.platforms) > 0,
            all(platform in [Platform.LINKEDIN, Platform.INDEED, Platform.GLASSDOOR, Platform.COMPANY_WEBSITE] 
                for platform in self.platforms),
            self.status in [VacancyStatus.DRAFT, VacancyStatus.PUBLISHED, VacancyStatus.CLOSED]
        ])

    def can_publish(self) -> bool:
        """Verifica si la vacante puede ser publicada."""
        return self.status == VacancyStatus.DRAFT and self.is_valid()

    def can_close(self) -> bool:
        """Verifica si la vacante puede ser cerrada."""
        return self.status == VacancyStatus.PUBLISHED

    class Config:
        json_schema_extra = {
            "example": {
                "requisition_id": 1,
                "platforms": ["LINKEDIN", "INDEED"],
                "status": "DRAFT"
            }
        } 