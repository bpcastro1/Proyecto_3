from datetime import datetime
from typing import List, Optional
from ...domain.entities.interview import Interview, InterviewStatus, InterviewFeedback
from ...domain.interfaces.interview_repository import InterviewRepository
from ...infrastructure.events.kafka_producer import KafkaProducer

class ScheduleInterviewUseCase:
    def __init__(self, repository: InterviewRepository, event_producer: KafkaProducer):
        self.repository = repository
        self.event_producer = event_producer

    async def execute(self, interview_data: dict) -> Interview:
        interview = Interview(**interview_data)
        
        if not interview.is_valid():
            raise ValueError("La entrevista no contiene toda la información requerida")

        created_interview = await self.repository.create(interview)

        # Publicar evento de entrevista programada
        await self.event_producer.send_message(
            "interview_scheduled",
            {
                "interview_id": created_interview.id,
                "candidate_id": created_interview.candidate_id,
                "interviewer_id": created_interview.interviewer_id,
                "vacancy_id": created_interview.vacancy_id,
                "interview_type": created_interview.interview_type,
                "scheduled_time": created_interview.scheduled_time.isoformat(),
                "duration_minutes": created_interview.duration_minutes,
                "location": created_interview.location
            }
        )

        return created_interview

class SubmitInterviewResultUseCase:
    def __init__(self, repository: InterviewRepository, event_producer: KafkaProducer):
        self.repository = repository
        self.event_producer = event_producer

    async def execute(
        self,
        interview_id: int,
        feedback_data: dict
    ) -> Optional[Interview]:
        # Obtener entrevista actual
        interview = await self.repository.get_by_id(interview_id)
        if not interview:
            raise ValueError("La entrevista no existe")

        if not interview.can_submit_feedback():
            raise ValueError("No se puede enviar feedback para esta entrevista")

        feedback = InterviewFeedback(**feedback_data)
        updated_interview = await self.repository.submit_feedback(interview_id, feedback)

        # Actualizar estado a completado
        if updated_interview.status != InterviewStatus.COMPLETED:
            updated_interview = await self.repository.update_status(
                interview_id,
                InterviewStatus.COMPLETED
            )

        # Publicar evento de feedback enviado
        await self.event_producer.send_message(
            "interview_feedback_submitted",
            {
                "interview_id": updated_interview.id,
                "candidate_id": updated_interview.candidate_id,
                "interviewer_id": updated_interview.interviewer_id,
                "vacancy_id": updated_interview.vacancy_id,
                "feedback": feedback_data,
                "submission_time": datetime.utcnow().isoformat()
            }
        )

        return updated_interview

class ListInterviewsUseCase:
    def __init__(self, repository: InterviewRepository):
        self.repository = repository

    async def execute(
        self,
        status: Optional[str] = None,
        vacancy_id: Optional[int] = None,
        candidate_id: Optional[int] = None,
        interviewer_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Interview]:
        if status:
            return await self.repository.list_by_status(status, start_date, end_date)
        elif vacancy_id:
            return await self.repository.list_by_vacancy(vacancy_id)
        elif candidate_id:
            return await self.repository.list_by_candidate(candidate_id)
        elif interviewer_id:
            return await self.repository.list_by_interviewer(interviewer_id, start_date, end_date)
        else:
            raise ValueError("Debe especificar al menos un criterio de búsqueda")

class RescheduleInterviewUseCase:
    def __init__(self, repository: InterviewRepository, event_producer: KafkaProducer):
        self.repository = repository
        self.event_producer = event_producer

    async def execute(
        self,
        interview_id: int,
        new_time: datetime,
        new_duration: Optional[int] = None
    ) -> Optional[Interview]:
        interview = await self.repository.get_by_id(interview_id)
        if not interview:
            raise ValueError("La entrevista no existe")

        if interview.status not in [InterviewStatus.SCHEDULED, InterviewStatus.CANCELLED]:
            raise ValueError("No se puede reprogramar esta entrevista")

        updated_interview = await self.repository.reschedule(
            interview_id,
            new_time,
            new_duration
        )

        # Publicar evento de entrevista reprogramada
        await self.event_producer.send_message(
            "interview_rescheduled",
            {
                "interview_id": updated_interview.id,
                "candidate_id": updated_interview.candidate_id,
                "interviewer_id": updated_interview.interviewer_id,
                "vacancy_id": updated_interview.vacancy_id,
                "new_time": new_time.isoformat(),
                "new_duration": new_duration or updated_interview.duration_minutes,
                "rescheduled_at": datetime.utcnow().isoformat()
            }
        )

        return updated_interview 