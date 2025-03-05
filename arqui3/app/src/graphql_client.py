import requests
import json
import logging
from .config import Config

logger = logging.getLogger(__name__)

class GraphQLClient:
    """Cliente para realizar consultas GraphQL a los microservicios"""
    
    def __init__(self, service_name="gateway"):
        """
        Inicializa el cliente GraphQL.
        
        Args:
            service_name (str): Nombre del servicio a consultar 
                               (requisition, vacancy, candidate, evaluation, interview, selection, gateway)
        """
        self.service_url = Config.get_service_url(service_name)
        self.graphql_endpoint = f"{self.service_url}/graphql"
        logger.info(f"Inicializando cliente GraphQL para {service_name} en {self.graphql_endpoint}")
    
    def execute_query(self, query, variables=None):
        """
        Ejecuta una consulta GraphQL.
        
        Args:
            query (str): Consulta GraphQL a ejecutar
            variables (dict, optional): Variables para la consulta
            
        Returns:
            dict: Respuesta de la consulta GraphQL
        """
        headers = {"Content-Type": "application/json"}
        payload = {"query": query}
        
        if variables:
            payload["variables"] = variables
            
        try:
            response = requests.post(
                self.graphql_endpoint,
                headers=headers,
                data=json.dumps(payload)
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en la consulta GraphQL: {str(e)}")
            return {"errors": [{"message": str(e)}]}
            
    def execute_mutation(self, mutation, variables=None):
        """
        Ejecuta una mutación GraphQL.
        
        Args:
            mutation (str): Mutación GraphQL a ejecutar
            variables (dict, optional): Variables para la mutación
            
        Returns:
            dict: Respuesta de la mutación GraphQL
        """
        return self.execute_query(mutation, variables) 