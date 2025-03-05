from datetime import datetime
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...domain.entities.vacancy import Vacancy
from ...domain.interfaces.vacancy_repository import VacancyRepository
from ..database.models import VacancyModel

class SQLAlchemyVacancyRepository(VacancyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, vacancy: Vacancy) -> Vacancy:
        db_vacancy = VacancyModel(
            requisition_id=vacancy.requisition_id,
            platforms=vacancy.platforms,
            status=vacancy.status
        )
        self.session.add(db_vacancy)
        await self.session.commit()
        await self.session.refresh(db_vacancy)
        return self._to_domain(db_vacancy)

    async def get_by_id(self, vacancy_id: int) -> Optional[Vacancy]:
        result = await self.session.execute(
            select(VacancyModel).where(VacancyModel.id == vacancy_id)
        )
        db_vacancy = result.scalar_one_or_none()
        return self._to_domain(db_vacancy) if db_vacancy else None

    async def list_by_status(self, status: Optional[str] = None) -> List[Vacancy]:
        query = select(VacancyModel)
        if status:
            query = query.where(VacancyModel.status == status)
        result = await self.session.execute(query)
        return [self._to_domain(r) for r in result.scalars().all()]

    async def update_status(self, vacancy_id: int, status: str, date: datetime) -> Optional[Vacancy]:
        result = await self.session.execute(
            select(VacancyModel).where(VacancyModel.id == vacancy_id)
        )
        db_vacancy = result.scalar_one_or_none()
        if db_vacancy:
            db_vacancy.status = status
            if status == "PUBLISHED":
                db_vacancy.publication_date = date
            elif status == "CLOSED":
                db_vacancy.closing_date = date
            await self.session.commit()
            return self._to_domain(db_vacancy)
        return None

    async def get_by_requisition_id(self, requisition_id: int) -> Optional[Vacancy]:
        result = await self.session.execute(
            select(VacancyModel).where(VacancyModel.requisition_id == requisition_id)
        )
        db_vacancy = result.scalar_one_or_none()
        return self._to_domain(db_vacancy) if db_vacancy else None

    def _to_domain(self, model: VacancyModel) -> Vacancy:
        return Vacancy(
            id=model.id,
            requisition_id=model.requisition_id,
            platforms=model.platforms,
            status=model.status,
            publication_date=model.publication_date,
            closing_date=model.closing_date,
            created_at=model.created_at
        ) 