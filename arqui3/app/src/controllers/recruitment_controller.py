import logging
from ..services.requisition_service import RequisitionService
from ..services.vacancy_service import VacancyService
from ..services.candidate_service import CandidateService
from ..services.evaluation_service import EvaluationService
from ..services.interview_service import InterviewService
from ..services.selection_service import SelectionService
from ..kafka_client import KafkaClient

logger = logging.getLogger(__name__)

class RecruitmentController:
    """Controlador para manejar el flujo del proceso de selección"""
    
    def __init__(self):
        self.requisition_service = RequisitionService()
        self.vacancy_service = VacancyService()
        self.candidate_service = CandidateService()
        self.evaluation_service = EvaluationService()
        self.interview_service = InterviewService()
        self.selection_service = SelectionService()
        self.kafka_client = KafkaClient()
        
    async def create_requisition(self, position_name, functions, salary_category, profile):
        """
        Crea una nueva requisición de personal.
        
        Args:
            position_name (str): Nombre del cargo
            functions (list): Lista de funciones del cargo
            salary_category (str): Categoría salarial
            profile (str): Perfil del candidato requerido
            
        Returns:
            tuple: (requisition, error_message) donde:
                  - requisition es la información de la requisición creada o None si hay error
                  - error_message es None si no hay error o un mensaje descriptivo si lo hay
        """
        requisition, error_message = self.requisition_service.create_requisition(
            position_name, functions, salary_category, profile
        )
        
        if requisition is None:
            # Propagar el mensaje de error
            return None, error_message
            
        # Notificar a través de Kafka
        await self.kafka_client.send_message(
            "requisition.created",
            {
                "requisition_id": requisition["id"],
                "position_name": requisition["positionName"],
                "status": requisition["status"]
            }
        )
            
        return requisition, None
    
    async def publish_vacancy(self, requisition_id, platforms):
        """
        Publica una vacante para una requisición aprobada.
        
        Args:
            requisition_id (int): ID de la requisición
            platforms (list): Plataformas donde publicar
            
        Returns:
            tuple: (vacancy, error_message) donde:
                  - vacancy es la información de la vacante publicada o None si hay error
                  - error_message es None si no hay error o un mensaje descriptivo si lo hay
        """
        # Verificar que la requisición exista y esté aprobada
        requisition, error_message = self.requisition_service.get_requisition(requisition_id)
        
        if not requisition:
            logger.error(f"Requisición {requisition_id} no encontrada: {error_message}")
            return None, error_message or f"Requisición {requisition_id} no encontrada"
            
        if requisition["status"] != "APPROVED":
            error_msg = f"Requisición {requisition_id} no está aprobada"
            logger.error(error_msg)
            return None, error_msg
            
        # Publicar la vacante
        vacancy = self.vacancy_service.publish_vacancy(requisition_id, platforms)
        
        if vacancy:
            # Notificar a través de Kafka
            await self.kafka_client.send_message(
                "vacancy.published",
                {
                    "vacancy_id": vacancy["id"],
                    "requisition_id": vacancy["requisitionId"],
                    "platforms": vacancy["platforms"]
                }
            )
            
        return vacancy, None
    
    async def register_candidate(self, name, email, resume_url, vacancy_id, skills, experience_years):
        """
        Registra un nuevo candidato para una vacante.
        
        Args:
            name (str): Nombre del candidato
            email (str): Email del candidato
            resume_url (str): URL del currículum
            vacancy_id (int): ID de la vacante
            skills (list): Habilidades del candidato
            experience_years (int): Años de experiencia
            
        Returns:
            dict: Información del candidato registrado
        """
        # Verificar que la vacante exista y esté publicada
        vacancy = self.vacancy_service.get_vacancy(vacancy_id)
        
        if not vacancy:
            logger.error(f"Vacante {vacancy_id} no encontrada")
            return None
            
        if vacancy["status"] != "PUBLISHED":
            logger.error(f"Vacante {vacancy_id} no está publicada")
            return None
            
        # Registrar el candidato
        candidate = self.candidate_service.submit_application(
            name, email, resume_url, vacancy_id, skills, experience_years
        )
        
        if candidate:
            # Notificar a través de Kafka
            await self.kafka_client.send_message(
                "candidate.registered",
                {
                    "candidate_id": candidate["id"],
                    "name": candidate["name"],
                    "vacancy_id": vacancy_id
                }
            )
            
        return candidate
    
    async def assign_candidate_evaluation(self, candidate_id, vacancy_id, tests):
        """
        Asigna pruebas de evaluación a un candidato.
        
        Args:
            candidate_id (int): ID del candidato
            vacancy_id (int): ID de la vacante
            tests (list): Lista de pruebas a asignar
            
        Returns:
            dict: Información de la evaluación asignada
        """
        # Verificar que el candidato exista
        candidate = self.candidate_service.get_candidate(candidate_id)
        
        if not candidate:
            logger.error(f"Candidato {candidate_id} no encontrado")
            return None
            
        # Asignar evaluación
        evaluation = self.evaluation_service.assign_evaluation(
            candidate_id, vacancy_id, tests
        )
        
        if evaluation:
            # Notificar a través de Kafka
            await self.kafka_client.send_message(
                "evaluation.assigned",
                {
                    "evaluation_id": evaluation["id"],
                    "candidate_id": candidate_id,
                    "vacancy_id": vacancy_id
                }
            )
            
        return evaluation
    
    async def register_test_result(self, evaluation_id, test_name, score, comments=""):
        """
        Registra el resultado de una prueba.
        
        Args:
            evaluation_id (int): ID de la evaluación
            test_name (str): Nombre de la prueba
            score (float): Puntuación obtenida
            comments (str, optional): Comentarios
            
        Returns:
            dict: Información de la evaluación actualizada
        """
        result = self.evaluation_service.submit_test_result(
            evaluation_id, test_name, score, comments
        )
        
        if result:
            # Notificar a través de Kafka
            await self.kafka_client.send_message(
                "test.completed",
                {
                    "evaluation_id": result["id"],
                    "test_name": test_name,
                    "score": score
                }
            )
            
        return result
    
    async def schedule_candidate_interview(self, candidate_id, interviewer_id, vacancy_id, 
                                         interview_type, scheduled_time, duration_minutes, location):
        """
        Programa una entrevista para un candidato.
        
        Args:
            candidate_id (int): ID del candidato
            interviewer_id (int): ID del entrevistador
            vacancy_id (int): ID de la vacante
            interview_type (str): Tipo de entrevista
            scheduled_time (str): Fecha y hora programada
            duration_minutes (int): Duración en minutos
            location (str): Ubicación o enlace
            
        Returns:
            dict: Información de la entrevista programada
        """
        interview = self.interview_service.schedule_interview(
            candidate_id, interviewer_id, vacancy_id, interview_type,
            scheduled_time, duration_minutes, location
        )
        
        if interview:
            # Notificar a través de Kafka
            await self.kafka_client.send_message(
                "interview.scheduled",
                {
                    "interview_id": interview["id"],
                    "candidate_id": candidate_id,
                    "scheduled_time": scheduled_time
                }
            )
            
        return interview
    
    async def register_interview_feedback(self, interview_id, strengths, weaknesses, 
                                        technical_score, communication_score, 
                                        culture_fit_score, recommendation, notes=""):
        """
        Registra el feedback de una entrevista.
        
        Args:
            interview_id (int): ID de la entrevista
            strengths (list): Fortalezas del candidato
            weaknesses (list): Debilidades del candidato
            technical_score (int): Puntuación técnica
            communication_score (int): Puntuación de comunicación
            culture_fit_score (int): Puntuación de ajuste cultural
            recommendation (str): Recomendación
            notes (str, optional): Notas adicionales
            
        Returns:
            dict: Información de la entrevista actualizada
        """
        feedback = self.interview_service.submit_feedback(
            interview_id, strengths, weaknesses, technical_score,
            communication_score, culture_fit_score, recommendation, notes
        )
        
        if feedback:
            # Notificar a través de Kafka
            await self.kafka_client.send_message(
                "interview.feedback",
                {
                    "interview_id": feedback["id"],
                    "recommendation": feedback["feedback"]["recommendation"]
                }
            )
            
        return feedback
    
    async def generate_selection_report(self, selection_id, technical_evaluation, hr_evaluation, additional_notes=""):
        """
        Genera el reporte final para un proceso de selección.
        
        Args:
            selection_id (int): ID del proceso de selección
            technical_evaluation (dict): Evaluación técnica
            hr_evaluation (dict): Evaluación de RRHH
            additional_notes (str, optional): Notas adicionales
            
        Returns:
            dict: Información del reporte generado
        """
        report = self.selection_service.generate_final_report(
            selection_id, technical_evaluation, hr_evaluation, additional_notes
        )
        
        if report:
            # Notificar a través de Kafka
            await self.kafka_client.send_message(
                "selection.report",
                {
                    "selection_id": report["id"],
                    "status": report["status"]
                }
            )
            
        return report
    
    async def make_final_decision(self, selection_id, decision, reason=""):
        """
        Registra la decisión final de contratación.
        
        Args:
            selection_id (int): ID del proceso de selección
            decision (str): Decisión (HIRE, REJECT)
            reason (str, optional): Motivo de la decisión
            
        Returns:
            dict: Información actualizada del proceso
        """
        result = self.selection_service.make_hiring_decision(
            selection_id, decision, reason
        )
        
        if result:
            # Notificar a través de Kafka
            await self.kafka_client.send_message(
                "selection.decision",
                {
                    "selection_id": result["id"],
                    "decision": result["decision"]
                }
            )
            
            # Si se decidió contratar, cerrar la vacante
            if decision == "HIRE":
                # Obtener la vacante asociada al proceso de selección
                selection = self.selection_service.get_selection_process(result["id"])
                if selection:
                    vacancy_id = selection.get("vacancyId")
                    if vacancy_id:
                        self.vacancy_service.close_vacancy(vacancy_id, "FILLED")
            
        return result
    
    async def close_vacancy_without_hiring(self, vacancy_id, reason="CANCELLED"):
        """
        Cierra una vacante sin contratar a ningún candidato.
        
        Args:
            vacancy_id (int): ID de la vacante
            reason (str): Motivo del cierre
            
        Returns:
            dict: Información de la vacante cerrada
        """
        result = self.vacancy_service.close_vacancy(vacancy_id, reason)
        
        if result:
            # Notificar a través de Kafka
            await self.kafka_client.send_message(
                "vacancy.closed",
                {
                    "vacancy_id": result["id"],
                    "status": result["status"],
                    "reason": reason
                }
            )
            
        return result 