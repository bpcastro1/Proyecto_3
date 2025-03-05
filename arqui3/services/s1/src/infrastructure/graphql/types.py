from datetime import datetime
from typing import List, Optional
import strawberry
from ...domain.entities.requisition import RequisitionStatus

@strawberry.type
class Requisition:
    id: Optional[int]
    position_name: str
    functions: List[str]
    salary_category: str
    profile: str
    status: str
    created_at: datetime

@strawberry.input
class RequisitionInput:
    position_name: str
    functions: List[str]
    salary_category: str
    profile: str 