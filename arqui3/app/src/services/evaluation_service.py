import logging
import os
import requests
from ..graphql_client import GraphQLClient
from ..config import Config

logger = logging.getLogger(__name__)

class EvaluationService:
    """Servicio para interactuar con el microservicio de evaluaciones"""
    
    def __init__(self):
        self.client = GraphQLClient("evaluation")
        self.service_url = Config.EVALUATION_SERVICE_URL
    
    def assign_evaluation(self, candidate_id, vacancy_id, tests):
        """
        Asigna pruebas a un candidato.
        
        Args:
            candidate_id (int): ID del candidato
            vacancy_id (int): ID de la vacante
            tests (list): Lista de pruebas a asignar [{"name", "type", "durationMinutes", "minScoreRequired"}]
            
        Returns:
            dict: Información de la evaluación asignada
        """
        mutation = """
        mutation AssignEvaluation($input: EvaluationAssignmentInput!) {
            assignEvaluation(input: $input) {
                id
                status
                assignedDate
            }
        }
        """
        
        variables = {
            "input": {
                "candidateId": candidate_id,
                "vacancyId": vacancy_id,
                "tests": tests
            }
        }
        
        response = self.client.execute_mutation(mutation, variables)
        logger.info(f"Respuesta de asignación de evaluación: {response}")
        return response.get("data", {}).get("assignEvaluation")
    
    def submit_test_result(self, evaluation_id, test_name, score, comments=""):
        """
        Registra el resultado de una prueba.
        
        Args:
            evaluation_id (int): ID de la evaluación
            test_name (str): Nombre de la prueba
            score (float): Puntuación obtenida
            comments (str, optional): Comentarios sobre la prueba
            
        Returns:
            dict: Información de la evaluación actualizada
        """
        mutation = """
        mutation SubmitTestResult($input: TestResultInput!) {
            submitTestResult(input: $input) {
                id
                status
                scores {
                    testName
                    score
                }
            }
        }
        """
        
        variables = {
            "input": {
                "evaluationId": evaluation_id,
                "testName": test_name,
                "score": score,
                "comments": comments
            }
        }
        
        response = self.client.execute_mutation(mutation, variables)
        return response.get("data", {}).get("submitTestResult")
    
    def get_evaluation(self, evaluation_id):
        """
        Obtiene la información de una evaluación por su ID.
        
        Args:
            evaluation_id (int): ID de la evaluación
            
        Returns:
            dict: Información de la evaluación
        """
        query = """
        query GetEvaluation($evaluationId: ID!) {
            getEvaluation(evaluationId: $evaluationId) {
                id
                candidateId
                vacancyId
                status
                assignedDate
                completedDate
                scores {
                    testName
                    score
                    comments
                }
            }
        }
        """
        
        variables = {"evaluationId": evaluation_id}
        
        response = self.client.execute_query(query, variables)
        return response.get("data", {}).get("getEvaluation")
    
    def get_evaluations_by_candidate(self, candidate_id):
        """
        Obtiene todas las evaluaciones de un candidato.
        
        Args:
            candidate_id (int): ID del candidato
            
        Returns:
            list: Lista de evaluaciones
        """
        query = """
        query GetEvaluationsByCandidate($candidateId: ID!) {
            evaluationsByCandidate(candidateId: $candidateId) {
                id
                status
                assignedDate
                completedDate
                scores {
                    testName
                    score
                }
            }
        }
        """
        
        variables = {"candidateId": candidate_id}
        
        response = self.client.execute_query(query, variables)
        return response.get("data", {}).get("evaluationsByCandidate", [])
    
    def download_excel_report(self, candidate_id, output_path=None):
        """
        Descarga un reporte en Excel para un candidato.
        
        Args:
            candidate_id (int): ID del candidato
            output_path (str, optional): Ruta donde guardar el archivo
            
        Returns:
            str: Ruta del archivo descargado
        """
        endpoint = f"{self.service_url}/reports/{candidate_id}/excel"
        
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            
            if not output_path:
                # Crear directorio temporal si no existe
                os.makedirs("tmp", exist_ok=True)
                output_path = f"tmp/evaluation_report_{candidate_id}.xlsx"
                
            with open(output_path, "wb") as file:
                file.write(response.content)
                
            logger.info(f"Reporte Excel descargado en {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error descargando reporte Excel: {str(e)}")
            raise
    
    def download_pdf_report(self, candidate_id, output_path=None):
        """
        Descarga un reporte en PDF para un candidato.
        
        Args:
            candidate_id (int): ID del candidato
            output_path (str, optional): Ruta donde guardar el archivo
            
        Returns:
            str: Ruta del archivo descargado
        """
        endpoint = f"{self.service_url}/reports/{candidate_id}/pdf"
        
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            
            if not output_path:
                # Crear directorio temporal si no existe
                os.makedirs("tmp", exist_ok=True)
                output_path = f"tmp/evaluation_report_{candidate_id}.pdf"
                
            with open(output_path, "wb") as file:
                file.write(response.content)
                
            logger.info(f"Reporte PDF descargado en {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error descargando reporte PDF: {str(e)}")
            raise 