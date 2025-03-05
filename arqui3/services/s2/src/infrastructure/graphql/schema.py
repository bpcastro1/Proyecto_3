from typing import List, Optional
import strawberry
from sqlalchemy.ext.asyncio import AsyncSession
from .types import Vacancy, VacancyInput
from ...application.use_cases.vacancy_use_cases import (
    PublishVacancyUseCase,
    CloseVacancyUseCase,
    ListVacanciesUseCase
)
from ..repositories.vacancy_repository_impl import SQLAlchemyVacancyRepository
from ..events.kafka_producer import KafkaProducer

@strawberry.type
class Query:
    @strawberry.field
    async def vacancy(self, info, vacancy_id: int) -> Optional[Vacancy]:
        async for session in info.context["session"]:
            repository = SQLAlchemyVacancyRepository(session)
            result = await repository.get_by_id(vacancy_id)
            return result

    @strawberry.field
    async def vacancies(self, info, status: Optional[str] = None) -> List[Vacancy]:
        async for session in info.context["session"]:
            repository = SQLAlchemyVacancyRepository(session)
            use_case = ListVacanciesUseCase(repository)
            return await use_case.execute(status)

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def publish_vacancy(self, info, input: VacancyInput) -> Vacancy:
        async for session in info.context["session"]:
            producer: KafkaProducer = info.context["kafka_producer"]
            repository = SQLAlchemyVacancyRepository(session)
            use_case = PublishVacancyUseCase(repository, producer)
            return await use_case.execute(input.__dict__)

    @strawberry.mutation
    async def close_vacancy(self, info, vacancy_id: int) -> Optional[Vacancy]:
        async for session in info.context["session"]:
            producer: KafkaProducer = info.context["kafka_producer"]
            repository = SQLAlchemyVacancyRepository(session)
            use_case = CloseVacancyUseCase(repository, producer)
            return await use_case.execute(vacancy_id)

schema = strawberry.Schema(query=Query, mutation=Mutation) 