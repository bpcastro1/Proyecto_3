from typing import List, Optional
import strawberry
from sqlalchemy.ext.asyncio import AsyncSession
from .types import Requisition, RequisitionInput
from ...application.use_cases.requisition_use_cases import (
    CreateRequisitionUseCase,
    ReviewRequisitionUseCase,
    ListRequisitionsUseCase
)
from ..repositories.requisition_repository_impl import SQLAlchemyRequisitionRepository

@strawberry.type
class Query:
    @strawberry.field
    async def requisition(self, info, requisition_id: int) -> Optional[Requisition]:
        async for session in info.context["session"]:
            repository = SQLAlchemyRequisitionRepository(session)
            result = await repository.get_by_id(requisition_id)
            return result

    @strawberry.field
    async def requisitions(self, info, status: Optional[str] = None) -> List[Requisition]:
        async for session in info.context["session"]:
            repository = SQLAlchemyRequisitionRepository(session)
            use_case = ListRequisitionsUseCase(repository)
            return await use_case.execute(status)

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_requisition(self, info, input: RequisitionInput) -> Requisition:
        async for session in info.context["session"]:
            repository = SQLAlchemyRequisitionRepository(session)
            use_case = CreateRequisitionUseCase(repository)
            return await use_case.execute(input.__dict__)

    @strawberry.mutation
    async def review_requisition(
        self, info, requisition_id: int, approve: bool
    ) -> Optional[Requisition]:
        async for session in info.context["session"]:
            repository = SQLAlchemyRequisitionRepository(session)
            use_case = ReviewRequisitionUseCase(repository)
            return await use_case.execute(requisition_id, approve)

schema = strawberry.Schema(query=Query, mutation=Mutation) 