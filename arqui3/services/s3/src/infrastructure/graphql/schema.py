from typing import List, Optional
import strawberry
from sqlalchemy.ext.asyncio import AsyncSession
from .types import Candidate, CandidateInput, CandidateFilterInput
from ...application.use_cases.candidate_use_cases import (
    SubmitApplicationUseCase,
    FilterCandidatesUseCase,
    ListCandidatesUseCase,
    UpdateCandidateStatusUseCase
)
from ..repositories.candidate_repository_impl import SQLAlchemyCandidateRepository
from ..events.kafka_producer import KafkaProducer
from ..database.config import async_session

@strawberry.type
class Query:
    @strawberry.field
    async def candidate(self, info, candidate_id: int) -> Optional[Candidate]:
        async with async_session() as session:
            repository = SQLAlchemyCandidateRepository(session)
            result = await repository.get_by_id(candidate_id)
            return result

    @strawberry.field
    async def candidates(self, info, vacancy_id: int) -> List[Candidate]:
        async with async_session() as session:
            repository = SQLAlchemyCandidateRepository(session)
            use_case = ListCandidatesUseCase(repository)
            return await use_case.execute(vacancy_id)

    @strawberry.field
    async def filter_candidates(
        self, info, filters: CandidateFilterInput
    ) -> List[Candidate]:
        async with async_session() as session:
            repository = SQLAlchemyCandidateRepository(session)
            use_case = FilterCandidatesUseCase(repository)
            return await use_case.execute(
                vacancy_id=filters.vacancy_id,
                required_skills=filters.required_skills,
                min_experience=filters.min_experience,
                status=filters.status
            )

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def submit_application(self, info, input: CandidateInput) -> Candidate:
        async with async_session() as session:
            producer: KafkaProducer = info.context["kafka_producer"]
            repository = SQLAlchemyCandidateRepository(session)
            use_case = SubmitApplicationUseCase(repository, producer)
            return await use_case.execute(input.__dict__)

    @strawberry.mutation
    async def update_candidate_status(
        self, info, candidate_id: int, status: str
    ) -> Optional[Candidate]:
        async with async_session() as session:
            producer: KafkaProducer = info.context["kafka_producer"]
            repository = SQLAlchemyCandidateRepository(session)
            use_case = UpdateCandidateStatusUseCase(repository, producer)
            return await use_case.execute(candidate_id, status)

    @strawberry.mutation
    async def create_candidate(self, name: str, email: str) -> Candidate:
        return Candidate(id="1", name=name, email=email, status="ACTIVE")

schema = strawberry.Schema(query=Query, mutation=Mutation) 