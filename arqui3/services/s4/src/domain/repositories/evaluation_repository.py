from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ..entities.evaluation import Evaluation

class EvaluationRepository(ABC):
    @abstractmethod
    async def create(self, evaluation: Evaluation) -> Evaluation:
        """Crea una nueva evaluación"""
        pass

    @abstractmethod
    async def get_by_id(self, evaluation_id: int) -> Optional[Evaluation]:
        """Obtiene una evaluación por su ID"""
        pass

    @abstractmethod
    async def list_by_vacancy(self, vacancy_id: int) -> List[Evaluation]:
        """Lista todas las evaluaciones para una vacante"""
        pass

    @abstractmethod
    async def list_by_candidate(self, candidate_id: int) -> List[Evaluation]:
        """Lista todas las evaluaciones para un candidato"""
        pass

    @abstractmethod
    async def update_test_result(
        self,
        evaluation_id: int,
        test_result: Dict[str, Any]
    ) -> Optional[Evaluation]:
        """Actualiza el resultado de una prueba"""
        pass

    @abstractmethod
    async def update_status(
        self,
        evaluation_id: int,
        status: str
    ) -> Optional[Evaluation]:
        """Actualiza el estado de una evaluación"""
        pass 