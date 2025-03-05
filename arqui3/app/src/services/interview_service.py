import logging
from ..graphql_client import GraphQLClient

logger = logging.getLogger(__name__)

class InterviewService:
    """Servicio para interactuar con el microservicio de entrevistas"""
    
    def __init__(self):
        self.client = GraphQLClient("interview")
    
    def schedule_interview(self, candidate_id, interviewer_id, vacancy_id, interview_type, 
                          scheduled_time, duration_minutes, location):
        """
        Programa una entrevista.
        
        Args:
            candidate_id (int): ID del candidato
            interviewer_id (int): ID del entrevistador
            vacancy_id (int): ID de la vacante
            interview_type (str): Tipo de entrevista (TECHNICAL, HR, CULTURAL)
            scheduled_time (str): Fecha y hora programada (formato ISO)
            duration_minutes (int): Duración en minutos
            location (str): Ubicación o enlace de la entrevista
            
        Returns:
            dict: Información de la entrevista programada
        """
        mutation = """
        mutation ScheduleInterview($input: InterviewScheduleInput!) {
            scheduleInterview(input: $input) {
                id
                status
                scheduledTime
            }
        }
        """
        
        variables = {
            "input": {
                "candidateId": candidate_id,
                "interviewerId": interviewer_id,
                "vacancyId": vacancy_id,
                "interviewType": interview_type,
                "scheduledTime": scheduled_time,
                "durationMinutes": duration_minutes,
                "location": location
            }
        }
        
        response = self.client.execute_mutation(mutation, variables)
        logger.info(f"Respuesta de programación de entrevista: {response}")
        return response.get("data", {}).get("scheduleInterview")
    
    def submit_feedback(self, interview_id, strengths, weaknesses, technical_score, 
                       communication_score, culture_fit_score, recommendation, notes=""):
        """
        Registra el feedback de una entrevista.
        
        Args:
            interview_id (int): ID de la entrevista
            strengths (list): Fortalezas del candidato
            weaknesses (list): Debilidades del candidato
            technical_score (int): Puntuación técnica (0-100)
            communication_score (int): Puntuación de comunicación (0-100)
            culture_fit_score (int): Puntuación de ajuste cultural (0-100)
            recommendation (str): Recomendación (HIRE, REJECT, CONSIDER)
            notes (str, optional): Notas adicionales
            
        Returns:
            dict: Información de la entrevista actualizada
        """
        mutation = """
        mutation SubmitFeedback($interviewId: ID!, $feedback: FeedbackInput!) {
            submitFeedback(interviewId: $interviewId, feedback: $feedback) {
                id
                status
                feedback {
                    recommendation
                    technicalScore
                }
            }
        }
        """
        
        variables = {
            "interviewId": interview_id,
            "feedback": {
                "strengths": strengths,
                "weaknesses": weaknesses,
                "technicalScore": technical_score,
                "communicationScore": communication_score,
                "cultureFitScore": culture_fit_score,
                "recommendation": recommendation,
                "notes": notes
            }
        }
        
        response = self.client.execute_mutation(mutation, variables)
        return response.get("data", {}).get("submitFeedback")
    
    def get_interview(self, interview_id):
        """
        Obtiene la información de una entrevista por su ID.
        
        Args:
            interview_id (int): ID de la entrevista
            
        Returns:
            dict: Información de la entrevista
        """
        query = """
        query GetInterview($interviewId: ID!) {
            getInterview(interviewId: $interviewId) {
                id
                candidateId
                interviewerId
                vacancyId
                interviewType
                status
                scheduledTime
                durationMinutes
                location
                feedback {
                    strengths
                    weaknesses
                    technicalScore
                    communicationScore
                    cultureFitScore
                    recommendation
                    notes
                }
            }
        }
        """
        
        variables = {"interviewId": interview_id}
        
        response = self.client.execute_query(query, variables)
        return response.get("data", {}).get("getInterview")
    
    def list_interviews_by_candidate(self, candidate_id):
        """
        Lista todas las entrevistas de un candidato.
        
        Args:
            candidate_id (int): ID del candidato
            
        Returns:
            list: Lista de entrevistas
        """
        query = """
        query ListInterviewsByCandidate($candidateId: ID!) {
            interviewsByCandidate(candidateId: $candidateId) {
                id
                interviewType
                status
                scheduledTime
                feedback {
                    recommendation
                }
            }
        }
        """
        
        variables = {"candidateId": candidate_id}
        
        response = self.client.execute_query(query, variables)
        return response.get("data", {}).get("interviewsByCandidate", []) 