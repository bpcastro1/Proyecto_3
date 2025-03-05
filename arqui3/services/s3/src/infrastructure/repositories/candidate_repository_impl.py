from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from ...domain.entities.candidate import Candidate
from ...domain.interfaces.candidate_repository import CandidateRepository
from ..database.models import CandidateModel

class SQLAlchemyCandidateRepository(CandidateRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, candidate: Candidate) -> Candidate:
        db_candidate = CandidateModel(
            name=candidate.name,
            email=candidate.email,
            resume_url=candidate.resume_url,
            vacancy_id=candidate.vacancy_id,
            application_date=candidate.application_date,
            status=candidate.status,
            skills=candidate.skills,
            experience_years=candidate.experience_years,
            notes=candidate.notes
        )
        self.session.add(db_candidate)
        await self.session.commit()
        await self.session.refresh(db_candidate)
        return self._to_domain(db_candidate)

    async def get_by_id(self, candidate_id: int) -> Optional[Candidate]:
        result = await self.session.execute(
            select(CandidateModel).where(CandidateModel.id == candidate_id)
        )
        db_candidate = result.scalar_one_or_none()
        return self._to_domain(db_candidate) if db_candidate else None

    async def list_by_vacancy(self, vacancy_id: int) -> List[Candidate]:
        result = await self.session.execute(
            select(CandidateModel).where(CandidateModel.vacancy_id == vacancy_id)
        )
        return [self._to_domain(r) for r in result.scalars().all()]

    async def list_by_filters(
        self,
        vacancy_id: Optional[int] = None,
        status: Optional[str] = None,
        skills: Optional[List[str]] = None,
        min_experience: Optional[int] = None
    ) -> List[Candidate]:
        query = select(CandidateModel)
        conditions = []

        if vacancy_id:
            conditions.append(CandidateModel.vacancy_id == vacancy_id)
        if status:
            conditions.append(CandidateModel.status == status)
        if min_experience:
            conditions.append(CandidateModel.experience_years >= min_experience)
        if skills:
            # PostgreSQL specific: array overlap operator &&
            conditions.append(CandidateModel.skills.overlap(skills))

        if conditions:
            query = query.where(and_(*conditions))

        result = await self.session.execute(query)
        return [self._to_domain(r) for r in result.scalars().all()]

    async def update_status(self, candidate_id: int, status: str) -> Optional[Candidate]:
        result = await self.session.execute(
            select(CandidateModel).where(CandidateModel.id == candidate_id)
        )
        db_candidate = result.scalar_one_or_none()
        if db_candidate:
            db_candidate.status = status
            await self.session.commit()
            return self._to_domain(db_candidate)
        return None

    async def add_notes(self, candidate_id: int, notes: str) -> Optional[Candidate]:
        result = await self.session.execute(
            select(CandidateModel).where(CandidateModel.id == candidate_id)
        )
        db_candidate = result.scalar_one_or_none()
        if db_candidate:
            db_candidate.notes = notes
            await self.session.commit()
            return self._to_domain(db_candidate)
        return None

    def _to_domain(self, model: CandidateModel) -> Candidate:
        return Candidate(
            id=model.id,
            name=model.name,
            email=model.email,
            resume_url=model.resume_url,
            vacancy_id=model.vacancy_id,
            application_date=model.application_date,
            status=model.status,
            skills=model.skills,
            experience_years=model.experience_years,
            notes=model.notes,
            created_at=model.created_at
        ) 