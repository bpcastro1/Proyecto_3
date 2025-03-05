from datetime import datetime
from typing import Optional, List
from ...domain.entities.selection import Selection, SelectionStatus, SelectionDecision
from ...domain.interfaces.selection_repository import SelectionRepository
from ...infrastructure.events.kafka_producer import KafkaProducer

class CreateSelectionUseCase:
    def __init__(self, repository: SelectionRepository):
        self.repository = repository

    async def execute(self, vacancy_id: int, candidate_id: int) -> Selection:
        selection = Selection(
            vacancy_id=vacancy_id,
            candidate_id=candidate_id,
            status=SelectionStatus.PENDING
        )
        
        if not selection.is_valid():
            raise ValueError("La selección no contiene toda la información requerida")

        return await self.repository.create(selection)

class GetSelectionUseCase:
    def __init__(self, repository: SelectionRepository):
        self.repository = repository

    async def execute(self, selection_id: int) -> Optional[Selection]:
        selection = await self.repository.get_by_id(selection_id)
        if not selection:
            raise ValueError("La selección no existe")
        return selection

class ListSelectionsUseCase:
    def __init__(self, repository: SelectionRepository):
        self.repository = repository

    async def execute(
        self,
        vacancy_id: Optional[int] = None,
        candidate_id: Optional[int] = None
    ) -> List[Selection]:
        if vacancy_id:
            return await self.repository.list_by_vacancy(vacancy_id)
        elif candidate_id:
            return await self.repository.list_by_candidate(candidate_id)
        else:
            raise ValueError("Debe especificar al menos un criterio de búsqueda")

class UpdateSelectionReportUseCase:
    def __init__(self, repository: SelectionRepository):
        self.repository = repository

    async def execute(self, id: int, report: dict) -> Selection:
        selection = await self.repository.get_by_id(id)
        if not selection:
            raise ValueError("La selección no existe")

        if not selection.can_generate_report():
            raise ValueError("No se puede generar el reporte en este momento")

        updated_selection = await self.repository.update_report(id, report)
        if updated_selection.status == SelectionStatus.PENDING:
            updated_selection = await self.repository.update_decision(
                id,
                None,
                SelectionStatus.IN_REVIEW
            )

        return updated_selection

class UpdateSelectionDecisionUseCase:
    def __init__(self, repository: SelectionRepository):
        self.repository = repository

    async def execute(self, id: int, decision: str) -> Selection:
        selection = await self.repository.get_by_id(id)
        if not selection:
            raise ValueError("La selección no existe")

        if not selection.can_make_decision():
            raise ValueError("No se puede tomar una decisión en este momento")

        if decision not in [
            SelectionDecision.HIRE,
            SelectionDecision.NO_HIRE,
            SelectionDecision.ON_HOLD
        ]:
            raise ValueError("Decisión no válida")

        status = (
            SelectionStatus.SELECTED if decision == SelectionDecision.HIRE
            else SelectionStatus.REJECTED if decision == SelectionDecision.NO_HIRE
            else SelectionStatus.IN_REVIEW
        )

        return await self.repository.update_decision(id, decision, status)

class GenerateFinalReportUseCase:
    def __init__(self, repository: SelectionRepository, event_producer: KafkaProducer):
        self.repository = repository
        self.event_producer = event_producer

    async def execute(self, selection_id: int, report_data: dict) -> Optional[Selection]:
        selection = await self.repository.get_by_id(selection_id)
        if not selection:
            raise ValueError("La selección no existe")

        if not selection.can_generate_report():
            raise ValueError("No se puede generar el reporte en este momento")

        # Actualizar reporte y estado
        updated_selection = await self.repository.update_report(selection_id, report_data)
        if updated_selection.status == SelectionStatus.PENDING:
            updated_selection = await self.repository.update_decision(
                selection_id,
                None,
                SelectionStatus.IN_REVIEW
            )

        # Publicar evento
        await self.event_producer.send_message(
            "selection_report_generated",
            {
                "selection_id": updated_selection.id,
                "vacancy_id": updated_selection.vacancy_id,
                "candidate_id": updated_selection.candidate_id,
                "report_summary": report_data,
                "generation_date": datetime.utcnow().isoformat()
            }
        )

        return updated_selection

class SelectCandidateUseCase:
    def __init__(self, repository: SelectionRepository, event_producer: KafkaProducer):
        self.repository = repository
        self.event_producer = event_producer

    async def execute(
        self,
        selection_id: int,
        decision: str
    ) -> Optional[Selection]:
        selection = await self.repository.get_by_id(selection_id)
        if not selection:
            raise ValueError("La selección no existe")

        if not selection.can_make_decision():
            raise ValueError("No se puede tomar una decisión en este momento")

        if decision not in [
            SelectionDecision.HIRE,
            SelectionDecision.NO_HIRE,
            SelectionDecision.ON_HOLD
        ]:
            raise ValueError("Decisión no válida")

        # Determinar el estado basado en la decisión
        status = (
            SelectionStatus.SELECTED if decision == SelectionDecision.HIRE
            else SelectionStatus.REJECTED if decision == SelectionDecision.NO_HIRE
            else SelectionStatus.IN_REVIEW
        )

        # Actualizar decisión y estado
        updated_selection = await self.repository.update_decision(
            selection_id,
            decision,
            status
        )

        # Publicar evento
        await self.event_producer.send_message(
            "candidate_selection_decision",
            {
                "selection_id": updated_selection.id,
                "vacancy_id": updated_selection.vacancy_id,
                "candidate_id": updated_selection.candidate_id,
                "decision": decision,
                "status": status,
                "decision_date": datetime.utcnow().isoformat()
            }
        )

        return updated_selection

class GetFinalReportUseCase:
    def __init__(self, repository: SelectionRepository):
        self.repository = repository

    async def execute(self, selection_id: int) -> Optional[Selection]:
        selection = await self.repository.get_by_id(selection_id)
        if not selection:
            raise ValueError("La selección no existe")
        
        if not selection.report:
            raise ValueError("El reporte aún no ha sido generado")
        
        return selection 