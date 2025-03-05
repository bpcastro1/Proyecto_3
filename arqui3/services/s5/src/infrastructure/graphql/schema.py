from datetime import datetime
from typing import List, Optional
import strawberry
from sqlalchemy.ext.asyncio import AsyncSession
from ...domain.entities.interview import InterviewStatus
from ...application.use_cases.interview_use_cases import (
    ScheduleInterviewUseCase,
    SubmitInterviewResultUseCase,
    ListInterviewsUseCase,
    RescheduleInterviewUseCase
)
from ...infrastructure.repositories.interview_repository import SQLAlchemyInterviewRepository
from ...infrastructure.events.kafka_producer import KafkaProducer
from .types import Interview, InterviewInput, InterviewFeedbackInput, RescheduleInput

@strawberry.type
class Query:
    @strawberry.field
    async def interview(self, info, interview_id: int) -> Optional[Interview]:
        session: AsyncSession = info.context["session"]
        repository = SQLAlchemyInterviewRepository(session)
        interview = await repository.get_by_id(interview_id)
        return interview

    @strawberry.field
    async def interviews_by_vacancy(self, info, vacancy_id: int) -> List[Interview]:
        session: AsyncSession = info.context["session"]
        repository = SQLAlchemyInterviewRepository(session)
        use_case = ListInterviewsUseCase(repository)
        return await use_case.execute(vacancy_id=vacancy_id)

    @strawberry.field
    async def interviews_by_candidate(self, info, candidate_id: int) -> List[Interview]:
        session: AsyncSession = info.context["session"]
        repository = SQLAlchemyInterviewRepository(session)
        use_case = ListInterviewsUseCase(repository)
        return await use_case.execute(candidate_id=candidate_id)

    @strawberry.field
    async def interviews_by_interviewer(
        self,
        info,
        interviewer_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Interview]:
        session: AsyncSession = info.context["session"]
        repository = SQLAlchemyInterviewRepository(session)
        use_case = ListInterviewsUseCase(repository)
        return await use_case.execute(
            interviewer_id=interviewer_id,
            start_date=start_date,
            end_date=end_date
        )

    @strawberry.field
    async def interviews_by_status(
        self,
        info,
        status: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Interview]:
        session: AsyncSession = info.context["session"]
        repository = SQLAlchemyInterviewRepository(session)
        use_case = ListInterviewsUseCase(repository)
        return await use_case.execute(
            status=status,
            start_date=start_date,
            end_date=end_date
        )

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def schedule_interview(self, info, input: InterviewInput) -> Interview:
        session: AsyncSession = info.context["session"]
        producer: KafkaProducer = info.context["kafka_producer"]
        repository = SQLAlchemyInterviewRepository(session)
        use_case = ScheduleInterviewUseCase(repository, producer)
        return await use_case.execute(input.__dict__)

    @strawberry.mutation
    async def submit_feedback(
        self,
        info,
        interview_id: int,
        feedback: InterviewFeedbackInput
    ) -> Optional[Interview]:
        session: AsyncSession = info.context["session"]
        producer: KafkaProducer = info.context["kafka_producer"]
        repository = SQLAlchemyInterviewRepository(session)
        use_case = SubmitInterviewResultUseCase(repository, producer)
        return await use_case.execute(interview_id, feedback.__dict__)

    @strawberry.mutation
    async def reschedule_interview(
        self,
        info,
        input: RescheduleInput
    ) -> Optional[Interview]:
        session: AsyncSession = info.context["session"]
        producer: KafkaProducer = info.context["kafka_producer"]
        repository = SQLAlchemyInterviewRepository(session)
        use_case = RescheduleInterviewUseCase(repository, producer)
        return await use_case.execute(
            input.interview_id,
            input.new_time,
            input.new_duration
        )

    @strawberry.mutation
    async def update_interview_status(
        self,
        info,
        interview_id: int,
        status: str
    ) -> Optional[Interview]:
        session: AsyncSession = info.context["session"]
        repository = SQLAlchemyInterviewRepository(session)
        interview = await repository.update_status(
            interview_id,
            InterviewStatus[status]
        )
        return interview

schema = strawberry.Schema(query=Query, mutation=Mutation) 