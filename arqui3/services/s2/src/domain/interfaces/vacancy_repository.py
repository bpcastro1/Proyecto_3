from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from ..entities.vacancy import Vacancy

class VacancyRepository(ABC):
    @abstractmethod
    async def create(self, vacancy: Vacancy) -> Vacancy:
        """Crea una nueva vacante"""
        pass

    @abstractmethod
    async def get_by_id(self, vacancy_id: int) -> Optional[Vacancy]:
        """Obtiene una vacante por su ID"""
        pass

    @abstractmethod
    async def list_by_status(self, status: Optional[str] = None) -> List[Vacancy]:
        """Lista las vacantes filtradas por estado"""
        pass

    @abstractmethod
    async def update_status(self, vacancy_id: int, status: str, date: datetime) -> Optional[Vacancy]:
        """Actualiza el estado de una vacante y su fecha correspondiente"""
        pass

    @abstractmethod
    async def get_by_requisition_id(self, requisition_id: int) -> Optional[Vacancy]:
        """Obtiene una vacante por su requisition_id"""
        pass 