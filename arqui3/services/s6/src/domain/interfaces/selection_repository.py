from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.selection import Selection

class SelectionRepository(ABC):
    @abstractmethod
    async def create(self, selection: Selection) -> Selection:
        """Crea una nueva selección"""
        pass

    @abstractmethod
    async def get_by_id(self, selection_id: int) -> Optional[Selection]:
        """Obtiene una selección por su ID"""
        pass

    @abstractmethod
    async def get_by_vacancy_and_candidate(
        self,
        vacancy_id: int,
        candidate_id: int
    ) -> Optional[Selection]:
        """Obtiene una selección por vacante y candidato"""
        pass

    @abstractmethod
    async def list_by_vacancy(self, vacancy_id: int) -> List[Selection]:
        """Lista las selecciones de una vacante específica"""
        pass

    @abstractmethod
    async def list_by_candidate(self, candidate_id: int) -> List[Selection]:
        """Lista las selecciones de un candidato específico"""
        pass

    @abstractmethod
    async def update_report(
        self,
        selection_id: int,
        report: dict
    ) -> Optional[Selection]:
        """Actualiza el reporte de una selección"""
        pass

    @abstractmethod
    async def update_decision(
        self,
        selection_id: int,
        decision: str,
        status: str
    ) -> Optional[Selection]:
        """Actualiza la decisión y estado de una selección"""
        pass 