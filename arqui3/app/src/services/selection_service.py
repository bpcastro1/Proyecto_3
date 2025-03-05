import logging
from ..graphql_client import GraphQLClient

logger = logging.getLogger(__name__)

class SelectionService:
    """Servicio para interactuar con el microservicio de selección"""
    
    def __init__(self):
        self.client = GraphQLClient("selection")
    
    def generate_final_report(self, selection_id, technical_evaluation, hr_evaluation, additional_notes=""):
        """
        Genera el reporte final para un proceso de selección.
        
        Args:
            selection_id (int): ID del proceso de selección
            technical_evaluation (dict): Evaluación técnica {"score", "feedback"}
            hr_evaluation (dict): Evaluación de RRHH {"score", "feedback"}
            additional_notes (str, optional): Notas adicionales
            
        Returns:
            dict: Información del reporte generado
        """
        mutation = """
        mutation GenerateFinalReport($selectionId: ID!, $report: FinalReportInput!) {
            generateFinalReport(selectionId: $selectionId, report: $report) {
                id
                status
                report {
                    technicalEvaluation {
                        score
                        feedback
                    }
                    hrEvaluation {
                        score
                        feedback
                    }
                }
            }
        }
        """
        
        variables = {
            "selectionId": selection_id,
            "report": {
                "technicalEvaluation": technical_evaluation,
                "hrEvaluation": hr_evaluation,
                "additionalNotes": additional_notes
            }
        }
        
        response = self.client.execute_mutation(mutation, variables)
        logger.info(f"Respuesta de generación de reporte final: {response}")
        return response.get("data", {}).get("generateFinalReport")
    
    def make_hiring_decision(self, selection_id, decision, reason=""):
        """
        Registra la decisión final de contratación.
        
        Args:
            selection_id (int): ID del proceso de selección
            decision (str): Decisión (HIRE, REJECT)
            reason (str, optional): Motivo de la decisión
            
        Returns:
            dict: Información actualizada del proceso de selección
        """
        mutation = """
        mutation MakeHiringDecision($selectionId: ID!, $decision: String!, $reason: String) {
            makeHiringDecision(selectionId: $selectionId, decision: $decision, reason: $reason) {
                id
                status
                decision
            }
        }
        """
        
        variables = {
            "selectionId": selection_id,
            "decision": decision,
            "reason": reason
        }
        
        response = self.client.execute_mutation(mutation, variables)
        return response.get("data", {}).get("makeHiringDecision")
    
    def get_selection_process(self, vacancy_id):
        """
        Obtiene la información de un proceso de selección por ID de vacante.
        
        Args:
            vacancy_id (int): ID de la vacante
            
        Returns:
            dict: Información del proceso de selección
        """
        query = """
        query GetSelectionProcess($vacancyId: ID!) {
            getSelectionProcess(vacancyId: $vacancyId) {
                id
                status
                report {
                    technicalEvaluation {
                        score
                        feedback
                    }
                    hrEvaluation {
                        score
                        feedback
                    }
                }
                decision
            }
        }
        """
        
        variables = {"vacancyId": vacancy_id}
        
        response = self.client.execute_query(query, variables)
        return response.get("data", {}).get("getSelectionProcess")
    
    def list_selection_processes(self, status=None):
        """
        Lista todos los procesos de selección, opcionalmente filtrados por estado.
        
        Args:
            status (str, optional): Estado de los procesos a filtrar
            
        Returns:
            list: Lista de procesos de selección
        """
        query = """
        query ListSelectionProcesses($status: String) {
            selectionProcesses(status: $status) {
                id
                vacancyId
                status
                decision
            }
        }
        """
        
        variables = {"status": status} if status else {}
        
        response = self.client.execute_query(query, variables)
        return response.get("data", {}).get("selectionProcesses", []) 