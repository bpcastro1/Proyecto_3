from typing import List, Optional
import strawberry
from sqlalchemy.ext.asyncio import AsyncSession
from ...domain.entities.selection import SelectionStatus, SelectionDecision
from ...application.use_cases.selection_use_cases import (
    GenerateFinalReportUseCase,
    SelectCandidateUseCase,
    GetFinalReportUseCase,
    CreateSelectionUseCase,
    GetSelectionUseCase,
    UpdateSelectionReportUseCase,
    UpdateSelectionDecisionUseCase,
    ListSelectionsUseCase
)
from ..repositories.selection_repository_impl import SQLAlchemySelectionRepository
from ..events.kafka_producer import KafkaProducer
from .types import Selection, SelectionInput, ReportInput

@strawberry.type
class Query:
    @strawberry.field
    async def selection(self, info, selection_id: int) -> Optional[Selection]:
        session: AsyncSession = info.context["session"]
        repository = SQLAlchemySelectionRepository(session)
        use_case = GetSelectionUseCase(repository)
        return await use_case.execute(selection_id)

    @strawberry.field
    async def selections(
        self,
        info,
        vacancy_id: Optional[int] = None,
        candidate_id: Optional[int] = None
    ) -> List[Selection]:
        session: AsyncSession = info.context["session"]
        repository = SQLAlchemySelectionRepository(session)
        use_case = ListSelectionsUseCase(repository)
        return await use_case.execute(vacancy_id, candidate_id)

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_selection(
        self,
        info,
        input: SelectionInput
    ) -> Selection:
        session: AsyncSession = info.context["session"]
        repository = SQLAlchemySelectionRepository(session)
        use_case = CreateSelectionUseCase(repository)
        return await use_case.execute(
            vacancy_id=input.vacancy_id,
            candidate_id=input.candidate_id
        )

    @strawberry.mutation
    async def generate_final_report(
        self,
        info,
        selection_id: int,
        report: ReportInput
    ) -> Selection:
        session: AsyncSession = info.context["session"]
        producer: KafkaProducer = info.context["kafka_producer"]
        repository = SQLAlchemySelectionRepository(session)
        use_case = GenerateFinalReportUseCase(repository, producer)
        return await use_case.execute(selection_id, report.__dict__)

    @strawberry.mutation
    async def select_candidate(
        self,
        info,
        selection_id: int,
        decision: str
    ) -> Optional[Selection]:
        session: AsyncSession = info.context["session"]
        producer: KafkaProducer = info.context["kafka_producer"]
        repository = SQLAlchemySelectionRepository(session)
        use_case = SelectCandidateUseCase(repository, producer)
        return await use_case.execute(selection_id, decision)

    @strawberry.mutation
    async def update_selection_report(
        self,
        info,
        id: int,
        report: ReportInput
    ) -> Selection:
        session: AsyncSession = info.context["session"]
        repository = SQLAlchemySelectionRepository(session)
        use_case = UpdateSelectionReportUseCase(repository)
        result = await use_case.execute(
            id=id,
            report={
                "technical_evaluation": {
                    "score": report.technical_evaluation.score,
                    "feedback": report.technical_evaluation.feedback
                } if report.technical_evaluation else None,
                "hr_evaluation": {
                    "score": report.hr_evaluation.score,
                    "feedback": report.hr_evaluation.feedback
                } if report.hr_evaluation else None,
                "additional_notes": report.additional_notes
            }
        )
        return result

    @strawberry.mutation
    async def update_selection_decision(
        self,
        info,
        id: int,
        decision: str
    ) -> Selection:
        session: AsyncSession = info.context["session"]
        repository = SQLAlchemySelectionRepository(session)
        use_case = UpdateSelectionDecisionUseCase(repository)
        return await use_case.execute(id=id, decision=decision)

schema = strawberry.Schema(query=Query, mutation=Mutation) 