from typing import List, Optional
import strawberry
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.repositories.evaluation_repository_impl import EvaluationRepositoryImpl
from src.infrastructure.events.kafka_producer import KafkaProducer
from src.infrastructure.database.config import get_session
from src.infrastructure.graphql.types import Evaluation, EvaluationInput, TestResultInput, Test
from src.application import (
    AssignTestsUseCase,
    SubmitTestResultUseCase,
    ListEvaluationsUseCase,
    GetCandidateEvaluationsUseCase
)

@strawberry.type
class Query:
    @strawberry.field
    async def evaluation(self, info, evaluation_id: int) -> Optional[Evaluation]:
        async with get_session() as session:
            repository = EvaluationRepositoryImpl(session)
            result = await repository.get_by_id(evaluation_id)
            return Evaluation.from_domain(result) if result else None

    @strawberry.field
    async def evaluations(self, info, vacancy_id: int) -> List[Evaluation]:
        async with get_session() as session:
            repository = EvaluationRepositoryImpl(session)
            use_case = ListEvaluationsUseCase(repository)
            results = await use_case.execute(vacancy_id)
            return [Evaluation.from_domain(result) for result in results]

    @strawberry.field
    async def candidate_evaluations(
        self, info, candidate_id: int
    ) -> List[Evaluation]:
        async with get_session() as session:
            repository = EvaluationRepositoryImpl(session)
            use_case = GetCandidateEvaluationsUseCase(repository)
            results = await use_case.execute(candidate_id)
            return [Evaluation.from_domain(result) for result in results]

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def assign_tests(self, info, input: EvaluationInput) -> Evaluation:
        async with get_session() as session:
            producer: KafkaProducer = info.context["kafka_producer"]
            repository = EvaluationRepositoryImpl(session)
            use_case = AssignTestsUseCase(repository, producer)
            result = await use_case.execute(input.to_dict())
            return Evaluation.from_domain(result)

    @strawberry.mutation
    async def submit_test_result(
        self, info, input: TestResultInput
    ) -> Optional[Evaluation]:
        async with get_session() as session:
            producer: KafkaProducer = info.context["kafka_producer"]
            repository = EvaluationRepositoryImpl(session)
            use_case = SubmitTestResultUseCase(repository, producer)
            result = await use_case.execute(
                input.evaluation_id,
                input.test_name,
                input.score,
                input.comments
            )
            return Evaluation.from_domain(result) if result else None

schema = strawberry.Schema(query=Query, mutation=Mutation) 