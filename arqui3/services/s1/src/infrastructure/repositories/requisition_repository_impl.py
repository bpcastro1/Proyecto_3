from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...domain.entities.requisition import Requisition
from ...domain.interfaces.requisition_repository import RequisitionRepository
from ..database.models import RequisitionModel

class SQLAlchemyRequisitionRepository(RequisitionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, requisition: Requisition) -> Requisition:
        db_requisition = RequisitionModel(
            position_name=requisition.position_name,
            functions=requisition.functions,
            salary_category=requisition.salary_category,
            profile=requisition.profile,
            status=requisition.status
        )
        self.session.add(db_requisition)
        await self.session.commit()
        await self.session.refresh(db_requisition)
        return self._to_domain(db_requisition)

    async def get_by_id(self, requisition_id: int) -> Optional[Requisition]:
        result = await self.session.execute(
            select(RequisitionModel).where(RequisitionModel.id == requisition_id)
        )
        db_requisition = result.scalar_one_or_none()
        return self._to_domain(db_requisition) if db_requisition else None

    async def list_by_status(self, status: Optional[str] = None) -> List[Requisition]:
        query = select(RequisitionModel)
        if status:
            query = query.where(RequisitionModel.status == status)
        result = await self.session.execute(query)
        return [self._to_domain(r) for r in result.scalars().all()]

    async def update_status(self, requisition_id: int, status: str) -> Optional[Requisition]:
        result = await self.session.execute(
            select(RequisitionModel).where(RequisitionModel.id == requisition_id)
        )
        db_requisition = result.scalar_one_or_none()
        if db_requisition:
            db_requisition.status = status
            await self.session.commit()
            return self._to_domain(db_requisition)
        return None

    def _to_domain(self, model: RequisitionModel) -> Requisition:
        if not model:
            return None
        return Requisition(
            id=model.id,
            position_name=model.position_name,
            functions=model.functions,
            salary_category=model.salary_category,
            profile=model.profile,
            status=model.status,
            created_at=model.created_at
        ) 