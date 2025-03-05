from typing import List, Optional, Dict, Any
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.evaluation import Evaluation, EvaluationStatus
from src.domain.repositories.evaluation_repository import EvaluationRepository
from src.infrastructure.database.models import EvaluationModel

class EvaluationRepositoryImpl(EvaluationRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, evaluation: Evaluation) -> Evaluation:
        db_evaluation = EvaluationModel(
            candidate_id=evaluation.candidate_id,
            vacancy_id=evaluation.vacancy_id,
            tests=evaluation.tests,
            scores=evaluation.scores,
            comments=evaluation.comments,
            status=evaluation.status,
            assigned_date=evaluation.assigned_date,
            completion_date=evaluation.completion_date,
            created_at=evaluation.created_at
        )
        self.session.add(db_evaluation)
        await self.session.commit()
        await self.session.refresh(db_evaluation)
        return self._to_domain(db_evaluation)

    async def get_by_id(self, evaluation_id: int) -> Optional[Evaluation]:
        result = await self.session.execute(
            select(EvaluationModel).where(EvaluationModel.id == evaluation_id)
        )
        db_evaluation = result.scalar_one_or_none()
        return self._to_domain(db_evaluation) if db_evaluation else None

    async def list_by_vacancy(self, vacancy_id: int) -> List[Evaluation]:
        result = await self.session.execute(
            select(EvaluationModel).where(EvaluationModel.vacancy_id == vacancy_id)
        )
        return [self._to_domain(db_eval) for db_eval in result.scalars().all()]

    async def list_by_candidate(self, candidate_id: int) -> List[Evaluation]:
        result = await self.session.execute(
            select(EvaluationModel).where(EvaluationModel.candidate_id == candidate_id)
        )
        return [self._to_domain(db_eval) for db_eval in result.scalars().all()]

    async def update_test_result(
        self,
        evaluation_id: int,
        test_result: Dict[str, Any]
    ) -> Optional[Evaluation]:
        evaluation = await self.get_by_id(evaluation_id)
        if not evaluation:
            return None

        db_evaluation = await self.session.get(EvaluationModel, evaluation_id)
        db_evaluation.scores = db_evaluation.scores or []
        db_evaluation.scores.append(test_result)
        db_evaluation.status = EvaluationStatus.IN_PROGRESS
        
        await self.session.commit()
        await self.session.refresh(db_evaluation)
        return self._to_domain(db_evaluation)

    async def update_status(
        self,
        evaluation_id: int,
        status: str
    ) -> Optional[Evaluation]:
        db_evaluation = await self.session.get(EvaluationModel, evaluation_id)
        if not db_evaluation:
            return None

        db_evaluation.status = status
        if status in [EvaluationStatus.COMPLETED, EvaluationStatus.FAILED]:
            db_evaluation.completion_date = datetime.utcnow()

        await self.session.commit()
        await self.session.refresh(db_evaluation)
        return self._to_domain(db_evaluation)

    def _to_domain(self, db_evaluation: EvaluationModel) -> Evaluation:
        return Evaluation(
            id=db_evaluation.id,
            candidate_id=db_evaluation.candidate_id,
            vacancy_id=db_evaluation.vacancy_id,
            tests=db_evaluation.tests,
            scores=db_evaluation.scores,
            comments=db_evaluation.comments,
            status=db_evaluation.status,
            assigned_date=db_evaluation.assigned_date,
            completion_date=db_evaluation.completion_date,
            created_at=db_evaluation.created_at
        ) 