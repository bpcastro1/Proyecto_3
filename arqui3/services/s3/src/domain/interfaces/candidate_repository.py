from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.candidate import Candidate

class CandidateRepository(ABC):
    @abstractmethod
    async def create(self, candidate: Candidate) -> Candidate:
        """Crea un nuevo candidato"""
        pass

    @abstractmethod
    async def get_by_id(self, candidate_id: int) -> Optional[Candidate]:
        """Obtiene un candidato por su ID"""
        pass

    @abstractmethod
    async def list_by_vacancy(self, vacancy_id: int) -> List[Candidate]:
        """Lista los candidatos de una vacante específica"""
        pass

    @abstractmethod
    async def list_by_filters(
        self,
        vacancy_id: Optional[int] = None,
        status: Optional[str] = None,
        skills: Optional[List[str]] = None,
        min_experience: Optional[int] = None
    ) -> List[Candidate]:
        """Lista los candidatos según los filtros especificados"""
        pass

    @abstractmethod
    async def update_status(self, candidate_id: int, status: str) -> Optional[Candidate]:
        """Actualiza el estado de un candidato"""
        pass

    @abstractmethod
    async def add_notes(self, candidate_id: int, notes: str) -> Optional[Candidate]:
        """Añade notas a un candidato"""
        pass 