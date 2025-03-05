from typing import List, Optional
import strawberry
from sqlalchemy.orm import Session
from src.domain.models import Evaluation, PsychometricResult, TechnicalResult, TestType, EvaluationStatus
from src.infrastructure.schema import (
    EvaluationType, PsychometricResultType, TechnicalResultType,
    EvaluationInput, PsychometricResultInput, TechnicalResultInput
)
from src.infrastructure.database import get_db, SessionLocal
from datetime import datetime

# Función auxiliar para obtener la sesión de DB de forma síncrona
def get_db_session():
    db = next(get_db())
    try:
        return db
    finally:
        db.close()

def convert_datetime_to_str(dt: datetime) -> str:
    return dt.isoformat() if dt else ""

@strawberry.type
class Query:
    @strawberry.field
    def evaluation(self, id: int) -> Optional[EvaluationType]:
        db = get_db_session()
        eval_db = db.query(Evaluation).filter(Evaluation.id == id).first()
        if not eval_db:
            return None
        return EvaluationType(
            id=eval_db.id,
            candidate_id=eval_db.candidate_id,
            test_type=eval_db.test_type,
            status=eval_db.status,
            score=eval_db.score,
            feedback=eval_db.feedback,
            created_at=convert_datetime_to_str(eval_db.created_at),
            updated_at=convert_datetime_to_str(eval_db.updated_at)
        )

    @strawberry.field
    def evaluations(self) -> List[EvaluationType]:
        db = get_db_session()
        evals_db = db.query(Evaluation).all()
        return [
            EvaluationType(
                id=eval_db.id,
                candidate_id=eval_db.candidate_id,
                test_type=eval_db.test_type,
                status=eval_db.status,
                score=eval_db.score,
                feedback=eval_db.feedback,
                created_at=convert_datetime_to_str(eval_db.created_at),
                updated_at=convert_datetime_to_str(eval_db.updated_at)
            )
            for eval_db in evals_db
        ]

    @strawberry.field
    def evaluations_by_candidate(self, candidate_id: int) -> List[EvaluationType]:
        db = get_db_session()
        evals_db = db.query(Evaluation).filter(Evaluation.candidate_id == candidate_id).all()
        return [
            EvaluationType(
                id=eval_db.id,
                candidate_id=eval_db.candidate_id,
                test_type=eval_db.test_type,
                status=eval_db.status,
                score=eval_db.score,
                feedback=eval_db.feedback,
                created_at=convert_datetime_to_str(eval_db.created_at),
                updated_at=convert_datetime_to_str(eval_db.updated_at)
            )
            for eval_db in evals_db
        ]

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_evaluation(self, input: EvaluationInput) -> EvaluationType:
        db = get_db_session()
        evaluation = Evaluation(
            candidate_id=input.candidate_id,
            test_type=input.test_type,
            status=EvaluationStatus.PENDING,
            score=None,
            feedback=None
        )
        db.add(evaluation)
        db.commit()
        db.refresh(evaluation)
        
        return EvaluationType(
            id=evaluation.id,
            candidate_id=evaluation.candidate_id,
            test_type=evaluation.test_type,
            status=evaluation.status,
            score=evaluation.score,
            feedback=evaluation.feedback,
            created_at=convert_datetime_to_str(evaluation.created_at),
            updated_at=convert_datetime_to_str(evaluation.updated_at)
        )

    @strawberry.mutation
    def update_psychometric_result(self, input: PsychometricResultInput) -> PsychometricResultType:
        db = get_db_session()
        
        evaluation = db.query(Evaluation).filter(Evaluation.id == input.evaluation_id).first()
        if not evaluation:
            raise ValueError(f"No se encontró la evaluación con ID {input.evaluation_id}")
        
        if evaluation.test_type != TestType.PSYCHOMETRIC:
            raise ValueError("Esta evaluación no es de tipo psicotécnico")
        
        result = PsychometricResult(
            evaluation_id=input.evaluation_id,
            personality_traits=input.personality_traits,
            cognitive_score=input.cognitive_score,
            emotional_intelligence=input.emotional_intelligence
        )
        db.add(result)
        
        if input.cognitive_score is not None and input.emotional_intelligence is not None:
            evaluation.score = (input.cognitive_score + input.emotional_intelligence) / 2
        evaluation.status = EvaluationStatus.COMPLETED
        
        db.commit()
        db.refresh(result)
        
        return PsychometricResultType(
            id=result.id,
            evaluation_id=result.evaluation_id,
            personality_traits=result.personality_traits,
            cognitive_score=result.cognitive_score,
            emotional_intelligence=result.emotional_intelligence,
            created_at=convert_datetime_to_str(result.created_at)
        )

    @strawberry.mutation
    def update_technical_result(self, input: TechnicalResultInput) -> TechnicalResultType:
        db = get_db_session()
        
        evaluation = db.query(Evaluation).filter(Evaluation.id == input.evaluation_id).first()
        if not evaluation:
            raise ValueError(f"No se encontró la evaluación con ID {input.evaluation_id}")
        
        if evaluation.test_type != TestType.TECHNICAL:
            raise ValueError("Esta evaluación no es de tipo técnico")
        
        result = TechnicalResult(
            evaluation_id=input.evaluation_id,
            programming_score=input.programming_score,
            problem_solving_score=input.problem_solving_score,
            technical_knowledge=input.technical_knowledge
        )
        db.add(result)
        
        if input.programming_score is not None and input.problem_solving_score is not None:
            evaluation.score = (input.programming_score + input.problem_solving_score) / 2
        evaluation.status = EvaluationStatus.COMPLETED
        
        db.commit()
        db.refresh(result)
        
        return TechnicalResultType(
            id=result.id,
            evaluation_id=result.evaluation_id,
            programming_score=result.programming_score,
            problem_solving_score=result.problem_solving_score,
            technical_knowledge=result.technical_knowledge,
            created_at=convert_datetime_to_str(result.created_at)
        ) 