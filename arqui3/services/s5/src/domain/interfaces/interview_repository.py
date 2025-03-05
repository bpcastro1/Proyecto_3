from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from ..entities.interview import Interview, InterviewFeedback

class InterviewRepository(ABC):
    @abstractmethod
    async def create(self, interview: Interview) -> Interview:
        """Crea una nueva entrevista"""
        pass

    @abstractmethod
    async def get_by_id(self, interview_id: int) -> Optional[Interview]:
        """Obtiene una entrevista por su ID"""
        pass

    @abstractmethod
    async def list_by_vacancy(self, vacancy_id: int) -> List[Interview]:
        """Lista las entrevistas de una vacante específica"""
        pass

    @abstractmethod
    async def list_by_candidate(self, candidate_id: int) -> List[Interview]:
        """Lista las entrevistas de un candidato específico"""
        pass

    @abstractmethod
    async def list_by_interviewer(
        self,
        interviewer_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Interview]:
        """Lista las entrevistas asignadas a un entrevistador"""
        pass

    @abstractmethod
    async def list_by_status(
        self,
        status: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Interview]:
        """Lista las entrevistas por estado"""
        pass

    @abstractmethod
    async def update_status(
        self,
        interview_id: int,
        status: str
    ) -> Optional[Interview]:
        """Actualiza el estado de una entrevista"""
        pass

    @abstractmethod
    async def submit_feedback(
        self,
        interview_id: int,
        feedback: InterviewFeedback
    ) -> Optional[Interview]:
        """Registra el feedback de una entrevista"""
        pass

    @abstractmethod
    async def reschedule(
        self,
        interview_id: int,
        new_time: datetime,
        new_duration: Optional[int] = None
    ) -> Optional[Interview]:
        """Reprograma una entrevista"""
        pass 