from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.requisition import Requisition

class RequisitionRepository(ABC):
    @abstractmethod
    async def create(self, requisition: Requisition) -> Requisition:
        """Crea una nueva requisición"""
        pass

    @abstractmethod
    async def get_by_id(self, requisition_id: int) -> Optional[Requisition]:
        """Obtiene una requisición por su ID"""
        pass

    @abstractmethod
    async def list_by_status(self, status: Optional[str] = None) -> List[Requisition]:
        """Lista las requisiciones filtradas por estado"""
        pass

    @abstractmethod
    async def update_status(self, requisition_id: int, status: str) -> Optional[Requisition]:
        """Actualiza el estado de una requisición"""
        pass 