import logging
from ..graphql_client import GraphQLClient

logger = logging.getLogger(__name__)

class CandidateService:
    """Servicio para interactuar con el microservicio de candidatos"""
    
    def __init__(self):
        self.client = GraphQLClient("candidate")
    
    def submit_application(self, name, email, resume_url, vacancy_id, skills, experience_years):
        """
        Registra la postulación de un candidato.
        
        Args:
            name (str): Nombre del candidato
            email (str): Email del candidato
            resume_url (str): URL del currículum
            vacancy_id (int): ID de la vacante
            skills (list): Lista de habilidades del candidato
            experience_years (int): Años de experiencia
            
        Returns:
            dict: Información de la aplicación registrada
        """
        mutation = """
        mutation SubmitCandidateApplication($input: CandidateApplicationInput!) {
            submitCandidateApplication(input: $input) {
                id
                name
                status
                applicationDate
            }
        }
        """
        
        variables = {
            "input": {
                "name": name,
                "email": email,
                "resumeUrl": resume_url,
                "vacancyId": vacancy_id,
                "skills": skills,
                "experienceYears": experience_years
            }
        }
        
        response = self.client.execute_mutation(mutation, variables)
        logger.info(f"Respuesta de registro de candidato: {response}")
        return response.get("data", {}).get("submitCandidateApplication")
    
    def get_candidate(self, candidate_id):
        """
        Obtiene la información de un candidato por su ID.
        
        Args:
            candidate_id (int): ID del candidato
            
        Returns:
            dict: Información del candidato
        """
        query = """
        query GetCandidate($candidateId: ID!) {
            getCandidate(candidateId: $candidateId) {
                id
                name
                email
                resumeUrl
                skills
                experienceYears
                status
                applicationDate
            }
        }
        """
        
        variables = {"candidateId": candidate_id}
        
        response = self.client.execute_query(query, variables)
        return response.get("data", {}).get("getCandidate")
    
    def list_candidates_by_vacancy(self, vacancy_id):
        """
        Lista todos los candidatos para una vacante.
        
        Args:
            vacancy_id (int): ID de la vacante
            
        Returns:
            list: Lista de candidatos
        """
        query = """
        query ListCandidatesByVacancy($vacancyId: ID!) {
            listCandidatesByVacancy(vacancyId: $vacancyId) {
                id
                name
                email
                status
                skills
                experienceYears
            }
        }
        """
        
        variables = {"vacancyId": vacancy_id}
        
        response = self.client.execute_query(query, variables)
        return response.get("data", {}).get("listCandidatesByVacancy", [])
    
    def filter_candidates(self, vacancy_id, status=None, required_skills=None, min_experience=None):
        """
        Filtra candidatos según criterios.
        
        Args:
            vacancy_id (int): ID de la vacante
            status (str, optional): Estado de los candidatos
            required_skills (list, optional): Habilidades requeridas
            min_experience (int, optional): Experiencia mínima requerida
            
        Returns:
            list: Lista de candidatos filtrados
        """
        query = """
        query FilterCandidates($filters: CandidateFilters!) {
            filterCandidates(filters: $filters) {
                id
                name
                skills
                status
                experienceYears
            }
        }
        """
        
        variables = {
            "filters": {
                "vacancyId": vacancy_id
            }
        }
        
        if status:
            variables["filters"]["status"] = status
            
        if required_skills:
            variables["filters"]["requiredSkills"] = required_skills
            
        if min_experience:
            variables["filters"]["minExperience"] = min_experience
        
        response = self.client.execute_query(query, variables)
        return response.get("data", {}).get("filterCandidates", []) 