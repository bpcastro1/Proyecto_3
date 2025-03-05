from datetime import datetime
from typing import List, Optional
from ...domain.entities.vacancy import Vacancy, VacancyStatus
from ...domain.interfaces.vacancy_repository import VacancyRepository
from ...infrastructure.events.kafka_producer import KafkaProducer

class PublishVacancyUseCase:
    def __init__(self, repository: VacancyRepository, event_producer: KafkaProducer):
        self.repository = repository
        self.event_producer = event_producer

    async def execute(self, vacancy_data: dict) -> Vacancy:
        # Crear o recuperar la vacante
        vacancy = Vacancy(**vacancy_data)
        
        if not vacancy.id:
            # Si es nueva vacante, crearla primero
            vacancy = await self.repository.create(vacancy)
        else:
            # Verificar que existe
            existing = await self.repository.get_by_id(vacancy.id)
            if not existing:
                raise ValueError("La vacante no existe")
            vacancy = existing

        if not vacancy.can_publish():
            raise ValueError("La vacante no puede ser publicada")

        # Actualizar estado y fecha de publicación
        updated_vacancy = await self.repository.update_status(
            vacancy.id,
            VacancyStatus.PUBLISHED,
            datetime.utcnow()
        )

        # Publicar evento
        await self.event_producer.send_message(
            "vacancy_published",
            {
                "vacancy_id": updated_vacancy.id,
                "requisition_id": updated_vacancy.requisition_id,
                "platforms": updated_vacancy.platforms,
                "publication_date": updated_vacancy.publication_date.isoformat()
            }
        )

        return updated_vacancy

class CloseVacancyUseCase:
    def __init__(self, repository: VacancyRepository, event_producer: KafkaProducer):
        self.repository = repository
        self.event_producer = event_producer

    async def execute(self, vacancy_id: int) -> Optional[Vacancy]:
        vacancy = await self.repository.get_by_id(vacancy_id)
        if not vacancy:
            raise ValueError("La vacante no existe")

        if not vacancy.can_close():
            raise ValueError("La vacante no puede ser cerrada")

        updated_vacancy = await self.repository.update_status(
            vacancy_id,
            VacancyStatus.CLOSED,
            datetime.utcnow()
        )

        # Publicar evento
        await self.event_producer.send_message(
            "vacancy_closed",
            {
                "vacancy_id": updated_vacancy.id,
                "requisition_id": updated_vacancy.requisition_id,
                "closing_date": updated_vacancy.closing_date.isoformat()
            }
        )

        return updated_vacancy

class ListVacanciesUseCase:
    def __init__(self, repository: VacancyRepository):
        self.repository = repository

    async def execute(self, status: Optional[str] = None) -> List[Vacancy]:
        return await self.repository.list_by_status(status) 