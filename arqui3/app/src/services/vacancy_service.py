import logging
from ..graphql_client import GraphQLClient

logger = logging.getLogger(__name__)

class VacancyService:
    """Servicio para interactuar con el microservicio de vacantes"""
    
    def __init__(self):
        self.client = GraphQLClient("vacancy")
    
    def publish_vacancy(self, requisition_id, platforms):
        """
        Publica una vacante en las plataformas seleccionadas.
        
        Args:
            requisition_id (int): ID de la requisición
            platforms (list): Lista de plataformas donde publicar 
                             (ej. ["LINKEDIN", "INDEED"])
            
        Returns:
            dict: Información de la vacante publicada
        """
        mutation = """
        mutation PublishVacancy($input: VacancyInput!) {
            publishVacancy(input: $input) {
                id
                requisitionId
                platforms
                status
                publicationDate
            }
        }
        """
        
        variables = {
            "input": {
                "requisitionId": requisition_id,
                "platforms": platforms
            }
        }
        
        response = self.client.execute_mutation(mutation, variables)
        logger.info(f"Respuesta de publicación de vacante: {response}")
        return response.get("data", {}).get("publishVacancy")
    
    def get_vacancy(self, vacancy_id):
        """
        Obtiene la información de una vacante por su ID.
        
        Args:
            vacancy_id (int): ID de la vacante
            
        Returns:
            dict: Información de la vacante
        """
        query = """
        query GetVacancy($vacancyId: ID!) {
            getVacancy(vacancyId: $vacancyId) {
                id
                requisitionId
                platforms
                status
                publicationDate
                closingDate
            }
        }
        """
        
        variables = {"vacancyId": vacancy_id}
        
        response = self.client.execute_query(query, variables)
        return response.get("data", {}).get("getVacancy")
    
    def list_vacancies(self, status=None):
        """
        Lista todas las vacantes, opcionalmente filtradas por estado.
        
        Args:
            status (str, optional): Estado de las vacantes a filtrar
            
        Returns:
            list: Lista de vacantes
        """
        query = """
        query ListVacancies($status: String) {
            vacancies(status: $status) {
                id
                requisitionId
                platforms
                status
                publicationDate
                closingDate
            }
        }
        """
        
        variables = {"status": status} if status else {}
        
        response = self.client.execute_query(query, variables)
        return response.get("data", {}).get("vacancies", [])
    
    def close_vacancy(self, vacancy_id, reason="FILLED"):
        """
        Cierra una vacante.
        
        Args:
            vacancy_id (int): ID de la vacante
            reason (str): Motivo del cierre (FILLED, CANCELLED)
            
        Returns:
            dict: Información de la vacante cerrada
        """
        mutation = """
        mutation CloseVacancy($vacancyId: ID!, $reason: String!) {
            closeVacancy(vacancyId: $vacancyId, reason: $reason) {
                id
                status
                closingDate
            }
        }
        """
        
        variables = {
            "vacancyId": vacancy_id,
            "reason": reason
        }
        
        response = self.client.execute_mutation(mutation, variables)
        return response.get("data", {}).get("closeVacancy") 