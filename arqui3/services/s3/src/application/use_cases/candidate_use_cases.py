from typing import List, Optional
from ...domain.entities.candidate import Candidate, CandidateStatus
from ...domain.interfaces.candidate_repository import CandidateRepository
from ...infrastructure.events.kafka_producer import KafkaProducer

class SubmitApplicationUseCase:
    def __init__(self, repository: CandidateRepository, event_producer: KafkaProducer):
        self.repository = repository
        self.event_producer = event_producer

    async def execute(self, candidate_data: dict) -> Candidate:
        candidate = Candidate(**candidate_data)
        
        if not candidate.is_valid():
            raise ValueError("La aplicación no contiene toda la información requerida")

        created_candidate = await self.repository.create(candidate)

        # Publicar evento de nueva aplicación
        await self.event_producer.send_message(
            "application_submitted",
            {
                "candidate_id": created_candidate.id,
                "vacancy_id": created_candidate.vacancy_id,
                "candidate_name": created_candidate.name,
                "candidate_email": created_candidate.email,
                "application_date": created_candidate.application_date.isoformat()
            }
        )

        return created_candidate

class FilterCandidatesUseCase:
    def __init__(self, repository: CandidateRepository):
        self.repository = repository

    async def execute(
        self,
        vacancy_id: Optional[int] = None,
        required_skills: Optional[List[str]] = None,
        min_experience: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[Candidate]:
        candidates = await self.repository.list_by_filters(
            vacancy_id=vacancy_id,
            skills=required_skills,
            min_experience=min_experience,
            status=status
        )
        
        # Aplicar filtros adicionales en memoria si es necesario
        if required_skills or min_experience:
            candidates = [
                c for c in candidates
                if c.matches_requirements(required_skills or [], min_experience or 0)
            ]
        
        return candidates

class ListCandidatesUseCase:
    def __init__(self, repository: CandidateRepository):
        self.repository = repository

    async def execute(self, vacancy_id: int) -> List[Candidate]:
        return await self.repository.list_by_vacancy(vacancy_id)

class UpdateCandidateStatusUseCase:
    def __init__(self, repository: CandidateRepository, event_producer: KafkaProducer):
        self.repository = repository
        self.event_producer = event_producer

    async def execute(self, candidate_id: int, status: str) -> Optional[Candidate]:
        if status not in [s for s in dir(CandidateStatus) if not s.startswith("_")]:
            raise ValueError("Estado no válido")

        updated_candidate = await self.repository.update_status(candidate_id, status)
        
        if updated_candidate:
            # Publicar evento de cambio de estado
            await self.event_producer.send_message(
                "candidate_status_updated",
                {
                    "candidate_id": updated_candidate.id,
                    "vacancy_id": updated_candidate.vacancy_id,
                    "new_status": status,
                    "candidate_name": updated_candidate.name
                }
            )

        return updated_candidate 