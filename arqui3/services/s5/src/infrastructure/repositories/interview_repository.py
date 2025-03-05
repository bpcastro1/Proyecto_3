from datetime import datetime
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ...domain.entities.interview import Interview, InterviewStatus, InterviewFeedback
from ...domain.interfaces.interview_repository import InterviewRepository
from ..database.models import InterviewModel

class SQLAlchemyInterviewRepository(InterviewRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, interview: Interview) -> Interview:
        db_interview = InterviewModel(
            candidate_id=interview.candidate_id,
            interviewer_id=interview.interviewer_id,
            vacancy_id=interview.vacancy_id,
            interview_type=interview.interview_type,
            scheduled_time=interview.scheduled_time,
            duration_minutes=interview.duration_minutes,
            location=interview.location,
            status=interview.status
        )
        self.session.add(db_interview)
        await self.session.commit()
        await self.session.refresh(db_interview)
        return self._to_entity(db_interview)

    async def get_by_id(self, interview_id: int) -> Optional[Interview]:
        result = await self.session.execute(
            select(InterviewModel).where(InterviewModel.id == interview_id)
        )
        db_interview = result.scalar_one_or_none()
        return self._to_entity(db_interview) if db_interview else None

    async def list_by_vacancy(self, vacancy_id: int) -> List[Interview]:
        result = await self.session.execute(
            select(InterviewModel).where(InterviewModel.vacancy_id == vacancy_id)
        )
        return [self._to_entity(i) for i in result.scalars().all()]

    async def list_by_candidate(self, candidate_id: int) -> List[Interview]:
        result = await self.session.execute(
            select(InterviewModel).where(InterviewModel.candidate_id == candidate_id)
        )
        return [self._to_entity(i) for i in result.scalars().all()]

    async def list_by_interviewer(
        self,
        interviewer_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Interview]:
        query = select(InterviewModel).where(InterviewModel.interviewer_id == interviewer_id)
        
        if start_date:
            query = query.where(InterviewModel.scheduled_time >= start_date)
        if end_date:
            query = query.where(InterviewModel.scheduled_time <= end_date)

        result = await self.session.execute(query)
        return [self._to_entity(i) for i in result.scalars().all()]

    async def list_by_status(
        self,
        status: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Interview]:
        query = select(InterviewModel).where(InterviewModel.status == status)
        
        if start_date:
            query = query.where(InterviewModel.scheduled_time >= start_date)
        if end_date:
            query = query.where(InterviewModel.scheduled_time <= end_date)

        result = await self.session.execute(query)
        return [self._to_entity(i) for i in result.scalars().all()]

    async def update_status(self, interview_id: int, status: InterviewStatus) -> Optional[Interview]:
        db_interview = await self._get_db_interview(interview_id)
        if not db_interview:
            return None

        db_interview.status = status
        await self.session.commit()
        await self.session.refresh(db_interview)
        return self._to_entity(db_interview)

    async def submit_feedback(self, interview_id: int, feedback: InterviewFeedback) -> Optional[Interview]:
        db_interview = await self._get_db_interview(interview_id)
        if not db_interview:
            return None

        db_interview.feedback = feedback.dict()
        await self.session.commit()
        await self.session.refresh(db_interview)
        return self._to_entity(db_interview)

    async def reschedule(
        self,
        interview_id: int,
        new_time: datetime,
        new_duration: Optional[int] = None
    ) -> Optional[Interview]:
        db_interview = await self._get_db_interview(interview_id)
        if not db_interview:
            return None

        db_interview.scheduled_time = new_time
        if new_duration:
            db_interview.duration_minutes = new_duration

        await self.session.commit()
        await self.session.refresh(db_interview)
        return self._to_entity(db_interview)

    async def _get_db_interview(self, interview_id: int) -> Optional[InterviewModel]:
        result = await self.session.execute(
            select(InterviewModel).where(InterviewModel.id == interview_id)
        )
        return result.scalar_one_or_none()

    def _to_entity(self, model: InterviewModel) -> Interview:
        return Interview(
            id=model.id,
            candidate_id=model.candidate_id,
            interviewer_id=model.interviewer_id,
            vacancy_id=model.vacancy_id,
            interview_type=model.interview_type,
            scheduled_time=model.scheduled_time,
            duration_minutes=model.duration_minutes,
            location=model.location,
            feedback=InterviewFeedback(**model.feedback) if model.feedback else None,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at
        ) 