from datetime import datetime
import strawberry
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

@strawberry.enum
class TestType(str, Enum):
    TECHNICAL = "TECHNICAL"
    PSYCHOMETRIC = "PSYCHOMETRIC"

@strawberry.enum
class EvaluationStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Evaluation(Base):
    __tablename__ = "evaluations"
    
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, nullable=False)
    test_type = Column(SQLEnum(TestType), nullable=False)
    status = Column(SQLEnum(EvaluationStatus), default=EvaluationStatus.PENDING)
    score = Column(Float, nullable=True)
    feedback = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "candidate_id": self.candidate_id,
            "test_type": self.test_type,
            "status": self.status,
            "score": self.score,
            "feedback": self.feedback,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class PsychometricResult(Base):
    __tablename__ = "psychometric_results"
    
    id = Column(Integer, primary_key=True)
    evaluation_id = Column(Integer, ForeignKey("evaluations.id"))
    personality_traits = Column(String, nullable=True)
    cognitive_score = Column(Float, nullable=True)
    emotional_intelligence = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "evaluation_id": self.evaluation_id,
            "personality_traits": self.personality_traits,
            "cognitive_score": self.cognitive_score,
            "emotional_intelligence": self.emotional_intelligence,
            "created_at": self.created_at
        }

class TechnicalResult(Base):
    __tablename__ = "technical_results"
    
    id = Column(Integer, primary_key=True)
    evaluation_id = Column(Integer, ForeignKey("evaluations.id"))
    programming_score = Column(Float, nullable=True)
    problem_solving_score = Column(Float, nullable=True)
    technical_knowledge = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "evaluation_id": self.evaluation_id,
            "programming_score": self.programming_score,
            "problem_solving_score": self.problem_solving_score,
            "technical_knowledge": self.technical_knowledge,
            "created_at": self.created_at
        } 