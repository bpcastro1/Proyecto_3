from typing import List, Optional
import strawberry
from datetime import datetime
import httpx
from .types import (
    Requisition,
    Vacancy,
    Candidate,
    Evaluation,
    Interview,
    Selection,
    RequisitionInput,
    VacancyInput,
    CandidateInput,
    EvaluationInput,
    InterviewInput,
    SelectionInput,
    ReportInput
)
import os

# URLs de los servicios
REQUISITIONS_SERVICE_URL = os.getenv("REQUISITIONS_SERVICE_URL", "http://localhost:8001")
VACANCIES_SERVICE_URL = os.getenv("VACANCIES_SERVICE_URL", "http://localhost:8002")
CANDIDATES_SERVICE_URL = os.getenv("CANDIDATES_SERVICE_URL", "http://localhost:8003")
EVALUATIONS_SERVICE_URL = os.getenv("EVALUATIONS_SERVICE_URL", "http://localhost:8004")
INTERVIEWS_SERVICE_URL = os.getenv("INTERVIEWS_SERVICE_URL", "http://localhost:8005")
SELECTIONS_SERVICE_URL = os.getenv("SELECTIONS_SERVICE_URL", "http://localhost:8006")

async def execute_graphql_query(service_url: str, query: str, variables: dict = None) -> dict:
    """Ejecuta una query GraphQL en el servicio especificado"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{service_url}/graphql",
                json={
                    "query": query,
                    "variables": variables or {}
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"Error en la petición HTTP: {response.status_code}")
            
            result = response.json()
            
            if "errors" in result:
                raise Exception(f"Error GraphQL: {result['errors']}")
                
            return result
    except Exception as e:
        print(f"Error al ejecutar query GraphQL: {str(e)}")
        raise Exception(f"Error al comunicarse con el servicio: {str(e)}")

@strawberry.type
class Query:
    @strawberry.field
    async def get_requisition(self, requisition_id: int) -> Optional[Requisition]:
        query = """
        query GetRequisition($id: Int!) {
            requisition(requisitionId: $id) {
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
        result = await execute_graphql_query(
            REQUISITIONS_SERVICE_URL,
            query,
            {"id": requisition_id}
        )
        if result.get("data", {}).get("requisition"):
            return Requisition(**result["data"]["requisition"])
        return None

    @strawberry.field
    async def list_candidates_by_vacancy(self, vacancy_id: int) -> List[Candidate]:
        query = """
        query ListCandidates($vacancyId: Int!) {
            candidates(vacancyId: $vacancyId) {
                id
                name
                email
                status
                skills
                experienceYears
                applicationDate
            }
        }
        """
        result = await execute_graphql_query(
            CANDIDATES_SERVICE_URL,
            query,
            {"vacancyId": vacancy_id}
        )
        return [Candidate(**c) for c in result.get("data", {}).get("candidates", [])]

    @strawberry.field
    async def get_selection_process(self, vacancy_id: int) -> List[Selection]:
        """Obtiene el proceso de selección completo para una vacante."""
        query = """
        query($vacancyId: Int!) {
            selections(vacancyId: $vacancyId) {
                id
                vacancyId
                candidateId
                status
                report
                decision
                createdAt
            }
        }
        """
        result = await execute_graphql_query(
            SELECTIONS_SERVICE_URL,
            query,
            {"vacancyId": vacancy_id}
        )
        return [Selection(**s) for s in result["data"]["selections"]]

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_requisition(self, input: RequisitionInput) -> Requisition:
        mutation = """
        mutation CreateRequisition($input: RequisitionInput!) {
            createRequisition(input: $input) {
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
        try:
            input_dict = {
                "positionName": input.position_name,
                "functions": input.functions,
                "salaryCategory": input.salary_category,
                "profile": input.profile
            }
            
            result = await execute_graphql_query(
                REQUISITIONS_SERVICE_URL,
                mutation,
                {"input": input_dict}
            )
            
            if not result or "data" not in result or not result["data"] or "createRequisition" not in result["data"]:
                raise Exception("No se recibió una respuesta válida del servicio de requisiciones")
            
            requisition_data = result["data"]["createRequisition"]
            return Requisition(**requisition_data)
            
        except Exception as e:
            raise Exception(f"Error al crear la requisición: {str(e)}")

    @strawberry.mutation
    async def publish_vacancy(self, input: VacancyInput) -> Vacancy:
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
        result = await execute_graphql_query(
            VACANCIES_SERVICE_URL,
            mutation,
            {"input": input.__dict__}
        )
        return Vacancy(**result["data"]["publishVacancy"])

    @strawberry.mutation
    async def submit_candidate_application(self, input: CandidateInput) -> Candidate:
        """Registra la aplicación de un candidato a una vacante."""
        mutation = """
        mutation($input: CandidateInput!) {
            submitApplication(input: $input) {
                id
                name
                email
                resumeUrl
                vacancyId
                status
                skills
                experienceYears
            }
        }
        """
        result = await execute_graphql_query(
            CANDIDATES_SERVICE_URL,
            mutation,
            {"input": input.__dict__}
        )
        return Candidate(**result["data"]["submitApplication"])

    @strawberry.mutation
    async def assign_evaluation(self, input: EvaluationInput) -> Evaluation:
        """Asigna pruebas de evaluación a un candidato."""
        mutation = """
        mutation($input: EvaluationInput!) {
            assignTests(input: $input) {
                id
                candidateId
                vacancyId
                tests
                status
                assignedDate
            }
        }
        """
        result = await execute_graphql_query(
            EVALUATIONS_SERVICE_URL,
            mutation,
            {"input": input.__dict__}
        )
        return Evaluation(**result["data"]["assignTests"])

    @strawberry.mutation
    async def schedule_interview(self, input: InterviewInput) -> Interview:
        """Programa una entrevista para un candidato."""
        mutation = """
        mutation($input: InterviewInput!) {
            scheduleInterview(input: $input) {
                id
                candidateId
                interviewerId
                vacancyId
                interviewType
                scheduledTime
                location
                status
            }
        }
        """
        result = await execute_graphql_query(
            INTERVIEWS_SERVICE_URL,
            mutation,
            {"input": input.__dict__}
        )
        return Interview(**result["data"]["scheduleInterview"])

    @strawberry.mutation
    async def generate_final_report(self, selection_id: int, report: ReportInput) -> Selection:
        """Genera el reporte final de selección para un candidato."""
        mutation = """
        mutation($selectionId: Int!, $report: ReportInput!) {
            generateFinalReport(selectionId: $selectionId, report: $report) {
                id
                vacancyId
                candidateId
                status
                report
                decision
            }
        }
        """
        result = await execute_graphql_query(
            SELECTIONS_SERVICE_URL,
            mutation,
            {"selectionId": selection_id, "report": report.__dict__}
        )
        return Selection(**result["data"]["generateFinalReport"])

schema = strawberry.Schema(query=Query, mutation=Mutation) 