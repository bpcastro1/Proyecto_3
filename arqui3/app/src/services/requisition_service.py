import logging
from ..graphql_client import GraphQLClient

logger = logging.getLogger(__name__)

class RequisitionService:
    """Servicio para interactuar con el microservicio de requisiciones"""
    
    def __init__(self):
        self.client = GraphQLClient("requisition")
    
    def create_requisition(self, position_name, functions, salary_category, profile):
        """
        Crea una nueva requisición de personal.
        
        Args:
            position_name (str): Nombre del cargo
            functions (list): Lista de funciones del cargo
            salary_category (str): Categoría salarial
            profile (str): Perfil del candidato requerido
            
        Returns:
            tuple: (resultado, error_message) donde:
                  - resultado es la requisición creada o None si hay error
                  - error_message es None si no hay error o un mensaje descriptivo si lo hay
        """
        mutation = """
        mutation CreateRequisition($input: RequisitionInput!) {
            createRequisition(input: $input) {
                id
                positionName
                status
                createdAt
            }
        }
        """
        
        variables = {
            "input": {
                "positionName": position_name,
                "functions": functions,
                "salaryCategory": salary_category,
                "profile": profile
            }
        }
        
        response = self.client.execute_mutation(mutation, variables)
        logger.info(f"Respuesta de creación de requisición: {response}")
        
        # Verifica si response es None 
        if response is None:
            return None, "Error de conexión con el servicio de requisiciones"
            
        # Verifica si hay errores en la respuesta
        if "errors" in response:
            try:
                # Intenta extraer un mensaje de error más específico
                error_message = response.get("errors", [{}])[0].get("message", "Error desconocido")
                
                # Si es un error de validación, extrae la información específica
                if "validation error" in error_message:
                    # Dividir el mensaje por saltos de línea reales
                    error_lines = error_message.split('\n')
                    
                    if len(error_lines) >= 3:
                        # La segunda línea suele contener el nombre del campo
                        field_name = error_lines[1].strip()
                        # La tercera línea suele contener el mensaje específico
                        error_detail = error_lines[2].strip()
                        
                        # Crear un mensaje más amigable
                        error_message = f"Error de validación en el campo '{field_name}': {error_detail}"
                    else:
                        error_message = f"Error de validación: {error_message}"
                
                logger.error(f"Error en la creación de requisición: {error_message}")
                return None, error_message
            except Exception as e:
                logger.error(f"Error al procesar el mensaje de error: {str(e)}")
                return None, "Error al crear la requisición"
                
        # Si no hay datos en la respuesta
        if not response.get("data") or not response.get("data").get("createRequisition"):
            return None, "No se pudo crear la requisición"
            
        return response.get("data", {}).get("createRequisition"), None
    
    def get_requisition(self, requisition_id):
        """
        Obtiene la información de una requisición por su ID.
        
        Args:
            requisition_id (int): ID de la requisición
            
        Returns:
            tuple: (requisition, error_message) donde:
                  - requisition es la información de la requisición o None si hay error
                  - error_message es None si no hay error o un mensaje descriptivo si lo hay
        """
        query = """
        query GetRequisition($requisitionId: ID!) {
            getRequisition(requisitionId: $requisitionId) {
                id
                positionName
                functions
                salaryCategory
                profile
                status
                createdAt
            }
        }
        """
        
        variables = {"requisitionId": requisition_id}
        
        response = self.client.execute_query(query, variables)
        
        # Verificar errores
        if response is None:
            return None, "Error de conexión con el servicio de requisiciones"
            
        if "errors" in response:
            try:
                error_message = response.get("errors", [{}])[0].get("message", "Error desconocido")
                
                # Si es un error de validación, extrae la información específica
                if "validation error" in error_message:
                    # Dividir el mensaje por saltos de línea reales
                    error_lines = error_message.split('\n')
                    
                    if len(error_lines) >= 3:
                        # La segunda línea suele contener el nombre del campo
                        field_name = error_lines[1].strip()
                        # La tercera línea suele contener el mensaje específico
                        error_detail = error_lines[2].strip()
                        
                        # Crear un mensaje más amigable
                        error_message = f"Error de validación en el campo '{field_name}': {error_detail}"
                    else:
                        error_message = f"Error de validación: {error_message}"
                
                logger.error(f"Error al obtener requisición: {error_message}")
                return None, error_message
            except Exception as e:
                logger.error(f"Error al procesar el mensaje de error: {str(e)}")
                return None, f"Error al obtener la requisición {requisition_id}"
            
        requisition = response.get("data", {}).get("getRequisition")
        if not requisition:
            return None, f"No se encontró la requisición con ID {requisition_id}"
            
        return requisition, None
    
    def list_requisitions(self, status=None):
        """
        Lista todas las requisiciones, opcionalmente filtradas por estado.
        
        Args:
            status (str, optional): Estado de las requisiciones a filtrar
            
        Returns:
            tuple: (requisitions, error_message) donde:
                  - requisitions es la lista de requisiciones o [] si hay error
                  - error_message es None si no hay error o un mensaje descriptivo si lo hay
        """
        query = """
        query ListRequisitions($status: String) {
            requisitions(status: $status) {
                id
                positionName
                status
                createdAt
            }
        }
        """
        
        variables = {"status": status} if status else {}
        
        response = self.client.execute_query(query, variables)
        
        # Verificar errores
        if response is None:
            return [], "Error de conexión con el servicio de requisiciones"
            
        if "errors" in response:
            try:
                error_message = response.get("errors", [{}])[0].get("message", "Error desconocido")
                
                # Si es un error de validación, extrae la información específica
                if "validation error" in error_message:
                    # Dividir el mensaje por saltos de línea reales
                    error_lines = error_message.split('\n')
                    
                    if len(error_lines) >= 3:
                        # La segunda línea suele contener el nombre del campo
                        field_name = error_lines[1].strip()
                        # La tercera línea suele contener el mensaje específico
                        error_detail = error_lines[2].strip()
                        
                        # Crear un mensaje más amigable
                        error_message = f"Error de validación en el campo '{field_name}': {error_detail}"
                    else:
                        error_message = f"Error de validación: {error_message}"
                
                logger.error(f"Error al listar requisiciones: {error_message}")
                return [], error_message
            except Exception as e:
                logger.error(f"Error al procesar el mensaje de error: {str(e)}")
                return [], "Error al listar requisiciones"
            
        requisitions = response.get("data", {}).get("requisitions", [])
        return requisitions, None 