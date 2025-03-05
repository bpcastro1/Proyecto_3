from datetime import datetime
from typing import List, Optional
import strawberry
from ...domain.entities.vacancy import VacancyStatus, Platform

@strawberry.type
class Vacancy:
    id: Optional[int]
    requisition_id: int
    platforms: List[str]
    status: str
    publication_date: Optional[datetime]
    closing_date: Optional[datetime]
    created_at: datetime

@strawberry.input
class VacancyInput:
    requisition_id: int
    platforms: List[str]
    id: Optional[int] = None 