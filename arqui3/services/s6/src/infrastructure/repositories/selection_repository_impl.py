from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from ...domain.entities.selection import Selection
from ...domain.interfaces.selection_repository import SelectionRepository
from ..database.models import SelectionModel

class SQLAlchemySelectionRepository(SelectionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, selection: Selection) -> Selection:
        db_selection = SelectionModel(
            vacancy_id=selection.vacancy_id,
            candidate_id=selection.candidate_id,
            report=selection.report,
            decision=selection.decision,
            status=selection.status
        )
        self.session.add(db_selection)
        await self.session.commit()
        await self.session.refresh(db_selection)
        return self._to_domain(db_selection)

    async def get_by_id(self, selection_id: int) -> Optional[Selection]:
        result = await self.session.execute(
            select(SelectionModel).where(SelectionModel.id == selection_id)
        )
        db_selection = result.scalar_one_or_none()
        return self._to_domain(db_selection) if db_selection else None

    async def get_by_vacancy_and_candidate(
        self,
        vacancy_id: int,
        candidate_id: int
    ) -> Optional[Selection]:
        result = await self.session.execute(
            select(SelectionModel).where(
                and_(
                    SelectionModel.vacancy_id == vacancy_id,
                    SelectionModel.candidate_id == candidate_id
                )
            )
        )
        db_selection = result.scalar_one_or_none()
        return self._to_domain(db_selection) if db_selection else None

    async def list_by_vacancy(self, vacancy_id: int) -> List[Selection]:
        result = await self.session.execute(
            select(SelectionModel).where(SelectionModel.vacancy_id == vacancy_id)
        )
        return [self._to_domain(r) for r in result.scalars().all()]

    async def list_by_candidate(self, candidate_id: int) -> List[Selection]:
        result = await self.session.execute(
            select(SelectionModel).where(SelectionModel.candidate_id == candidate_id)
        )
        return [self._to_domain(r) for r in result.scalars().all()]

    async def update_report(
        self,
        selection_id: int,
        report: dict
    ) -> Optional[Selection]:
        result = await self.session.execute(
            select(SelectionModel).where(SelectionModel.id == selection_id)
        )
        db_selection = result.scalar_one_or_none()
        if db_selection:
            db_selection.report = report
            await self.session.commit()
            await self.session.refresh(db_selection)
            return self._to_domain(db_selection)
        return None

    async def update_decision(
        self,
        selection_id: int,
        decision: str,
        status: str
    ) -> Optional[Selection]:
        result = await self.session.execute(
            select(SelectionModel).where(SelectionModel.id == selection_id)
        )
        db_selection = result.scalar_one_or_none()
        if db_selection:
            db_selection.decision = decision
            db_selection.status = status
            await self.session.commit()
            await self.session.refresh(db_selection)
            return self._to_domain(db_selection)
        return None

    def _to_domain(self, model: SelectionModel) -> Selection:
        return Selection(
            id=model.id,
            vacancy_id=model.vacancy_id,
            candidate_id=model.candidate_id,
            report=model.report,
            decision=model.decision,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at
        ) 