from typing import List, Optional
from ...domain.entities.requisition import Requisition, RequisitionStatus
from ...domain.interfaces.requisition_repository import RequisitionRepository

class CreateRequisitionUseCase:
    def __init__(self, repository: RequisitionRepository):
        self.repository = repository

    async def execute(self, requisition_data: dict) -> Requisition:
        requisition = Requisition(**requisition_data)
        if not requisition.is_valid():
            raise ValueError("La requisición no contiene toda la información requerida")
        return await self.repository.create(requisition)

class ReviewRequisitionUseCase:
    def __init__(self, repository: RequisitionRepository):
        self.repository = repository

    async def execute(self, requisition_id: int, approve: bool) -> Optional[Requisition]:
        status = RequisitionStatus.APPROVED if approve else RequisitionStatus.REJECTED
        return await self.repository.update_status(requisition_id, status)

class ListRequisitionsUseCase:
    def __init__(self, repository: RequisitionRepository):
        self.repository = repository

    async def execute(self, status: Optional[str] = None) -> List[Requisition]:
        return await self.repository.list_by_status(status) 