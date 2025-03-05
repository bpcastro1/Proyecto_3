from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from src.domain.entities.evaluation import Evaluation, EvaluationStatus
from src.domain.repositories.evaluation_repository import EvaluationRepository
from src.infrastructure.events.kafka_producer import KafkaProducer
from src.domain.models import PsychometricResult, TechnicalResult, TestType

__all__ = [
    'AssignTestsUseCase',
    'SubmitTestResultUseCase',
    'ListEvaluationsUseCase',
    'GetCandidateEvaluationsUseCase'
]

class AssignTestsUseCase:
    """Caso de uso para asignar pruebas a un candidato"""
    def __init__(self, db: Session):
        self.db = db

    def execute(self, candidate_id: int, test_type: TestType):
        evaluation = Evaluation(
            candidate_id=candidate_id,
            test_type=test_type,
            status=EvaluationStatus.PENDING
        )
        self.db.add(evaluation)
        self.db.commit()
        self.db.refresh(evaluation)
        return evaluation

class SubmitTestResultUseCase:
    """Caso de uso para enviar el resultado de una prueba"""
    def __init__(self, db: Session):
        self.db = db

    def execute(self, evaluation_id: int, result_data: dict):
        evaluation = self.db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
        if not evaluation:
            raise ValueError("Evaluation not found")

        if evaluation.test_type == TestType.PSYCHOMETRIC:
            result = PsychometricResult(
                evaluation_id=evaluation_id,
                personality_traits=result_data.get('personality_traits'),
                cognitive_score=result_data.get('cognitive_score'),
                emotional_intelligence=result_data.get('emotional_intelligence')
            )
        else:
            result = TechnicalResult(
                evaluation_id=evaluation_id,
                programming_score=result_data.get('programming_score'),
                problem_solving_score=result_data.get('problem_solving_score'),
                technical_knowledge=result_data.get('technical_knowledge')
            )

        self.db.add(result)
        evaluation.status = EvaluationStatus.COMPLETED
        self.db.commit()
        return result

class ListEvaluationsUseCase:
    """Caso de uso para listar evaluaciones por vacante"""
    def __init__(self, db: Session):
        self.db = db

    def execute(self):
        return self.db.query(Evaluation).all()

class GetCandidateEvaluationsUseCase:
    """Caso de uso para obtener evaluaciones de un candidato"""
    def __init__(self, db: Session):
        self.db = db

    def execute(self, candidate_id: int):
        return self.db.query(Evaluation).filter(Evaluation.candidate_id == candidate_id).all() 