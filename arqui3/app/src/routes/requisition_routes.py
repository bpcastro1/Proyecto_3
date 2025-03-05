from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from ..controllers.recruitment_controller import RecruitmentController

router = APIRouter(prefix="/requisitions", tags=["Requisiciones"])

# Modelos de datos
class RequisitionInput(BaseModel):
    position_name: str
    functions: List[str]
    salary_category: str
    profile: str

class RequisitionResponse(BaseModel):
    id: int
    position_name: str
    status: str
    created_at: str

# Dependencia para obtener el controlador
def get_controller():
    return RecruitmentController()

@router.post("/", response_model=RequisitionResponse)
async def create_requisition(
    requisition: RequisitionInput,
    controller: RecruitmentController = Depends(get_controller)
):
    """Crea una nueva requisición de personal"""
    result, error_message = await controller.create_requisition(
        requisition.position_name,
        requisition.functions,
        requisition.salary_category,
        requisition.profile
    )
    
    if not result:
        # Usar el mensaje de error específico del servicio
        raise HTTPException(
            status_code=400, 
            detail=error_message or "Error al crear la requisición. Verifique que todos los campos cumplan con los requisitos."
        )
        
    # Convertir las claves de camelCase a snake_case para el modelo de respuesta
    return {
        "id": result["id"],
        "position_name": result["positionName"],
        "status": result["status"],
        "created_at": result["createdAt"]
    }

@router.get("/{requisition_id}")
async def get_requisition(
    requisition_id: int,
    controller: RecruitmentController = Depends(get_controller)
):
    """Obtiene una requisición por su ID"""
    result, error_message = controller.requisition_service.get_requisition(requisition_id)
    
    if not result:
        raise HTTPException(
            status_code=404, 
            detail=error_message or f"Requisición {requisition_id} no encontrada"
        )
        
    return result

@router.get("/")
async def list_requisitions(
    status: Optional[str] = None,
    controller: RecruitmentController = Depends(get_controller)
):
    """Lista todas las requisiciones, opcionalmente filtradas por estado"""
    result, error_message = controller.requisition_service.list_requisitions(status)
    
    if error_message:
        # Solo devolvemos error si hay un mensaje específico, ya que una lista vacía es un resultado válido
        raise HTTPException(
            status_code=400, 
            detail=error_message
        )
        
    return result 