from typing import List
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from sqlalchemy.orm import Session
from src.domain.models import Evaluation, PsychometricResult, TechnicalResult, TestType

class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def generate_excel_report(self, candidate_id: int, output_path: str):
        evaluations = self.db.query(Evaluation).filter(Evaluation.candidate_id == candidate_id).all()
        
        data = []
        for eval in evaluations:
            psychometric = self.db.query(PsychometricResult).filter(
                PsychometricResult.evaluation_id == eval.id
            ).first()
            
            technical = self.db.query(TechnicalResult).filter(
                TechnicalResult.evaluation_id == eval.id
            ).first()
            
            row = {
                'Tipo de Prueba': eval.test_type,
                'Estado': eval.status,
                'Puntuación Final': eval.score,
                'Fecha': eval.created_at
            }
            
            if psychometric:
                row.update({
                    'Rasgos de Personalidad': psychometric.personality_traits,
                    'Puntuación Cognitiva': psychometric.cognitive_score,
                    'Inteligencia Emocional': psychometric.emotional_intelligence
                })
            
            if technical:
                row.update({
                    'Programación': technical.programming_score,
                    'Resolución de Problemas': technical.problem_solving_score,
                    'Conocimiento Técnico': technical.technical_knowledge
                })
            
            data.append(row)
        
        df = pd.DataFrame(data)
        df.to_excel(output_path, index=False)

    def generate_pdf_report(self, candidate_id: int, output_path: str):
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Título
        elements.append(Paragraph(f"Reporte de Evaluación - Candidato {candidate_id}", styles['Title']))
        elements.append(Paragraph("<br/><br/>", styles['Normal']))
        
        evaluations = self.db.query(Evaluation).filter(Evaluation.candidate_id == candidate_id).all()
        
        for eval in evaluations:
            elements.append(Paragraph(f"Evaluación {eval.test_type}", styles['Heading1']))
            
            data = [
                ['Atributo', 'Valor'],
                ['Estado', eval.status],
                ['Puntuación Final', str(eval.score or 'N/A')],
                ['Fecha', eval.created_at.strftime('%Y-%m-%d %H:%M:%S')]
            ]
            
            if eval.test_type == TestType.PSYCHOMETRIC:
                psychometric = self.db.query(PsychometricResult).filter(
                    PsychometricResult.evaluation_id == eval.id
                ).first()
                if psychometric:
                    data.extend([
                        ['Rasgos de Personalidad', psychometric.personality_traits or 'N/A'],
                        ['Puntuación Cognitiva', str(psychometric.cognitive_score or 'N/A')],
                        ['Inteligencia Emocional', str(psychometric.emotional_intelligence or 'N/A')]
                    ])
            elif eval.test_type == TestType.TECHNICAL:
                technical = self.db.query(TechnicalResult).filter(
                    TechnicalResult.evaluation_id == eval.id
                ).first()
                if technical:
                    data.extend([
                        ['Programación', str(technical.programming_score or 'N/A')],
                        ['Resolución de Problemas', str(technical.problem_solving_score or 'N/A')],
                        ['Conocimiento Técnico', technical.technical_knowledge or 'N/A']
                    ])
            
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(table)
            elements.append(Paragraph("<br/><br/>", styles['Normal']))
        
        doc.build(elements) 