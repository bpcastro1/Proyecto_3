# Servicio de Selección

Este es un microservicio construido con FastAPI y GraphQL para gestionar el proceso de selección de candidatos. Permite generar reportes finales, tomar decisiones sobre candidatos y gestionar el ciclo completo de selección.

## Requisitos

- Python 3.8+
- PostgreSQL
- Apache Kafka
- pip

## Instalación

1. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar la base de datos PostgreSQL:
```bash
# Crear la base de datos
createdb selections_db

# Configurar las variables de entorno
export DATABASE_URL="postgresql+asyncpg://usuario:contraseña@localhost:5432/selections_db"
```

4. Configurar Kafka:
```bash
# Configurar la variable de entorno para Kafka
export KAFKA_BOOTSTRAP_SERVERS="localhost:9092"
```

## Ejecución

Para ejecutar el servicio:

```bash
uvicorn src.main:app --reload
```

El servicio estará disponible en:
- API REST: http://localhost:8000
- GraphQL: http://localhost:8000/graphql
- Documentación: http://localhost:8000/docs

## Ejemplos de Uso

### Queries GraphQL

1. Obtener una selección por ID:
```graphql
query {
  selection(selectionId: 1) {
    id
    vacancyId
    candidateId
    report
    decision
    status
  }
}
```

2. Listar selecciones por vacante:
```graphql
query {
  selectionsByVacancy(vacancyId: 1) {
    id
    candidateId
    status
    decision
  }
}
```

### Mutations GraphQL

1. Crear una selección:
```graphql
mutation {
  createSelection(
    input: {
      vacancyId: 1
      candidateId: 2
    }
  ) {
    id
    status
  }
}
```

2. Generar reporte final:
```graphql
mutation {
  generateFinalReport(
    selectionId: 1
    report: {
      technicalEvaluation: {
        score: 85
        feedback: "Excelente conocimiento técnico"
      }
      hrEvaluation: {
        score: 90
        feedback: "Buena comunicación y actitud"
      }
      additionalNotes: "Candidato prometedor"
    }
  ) {
    id
    status
    report
  }
}
```

3. Seleccionar candidato:
```graphql
mutation {
  selectCandidate(
    selectionId: 1
    decision: "HIRE"
  ) {
    id
    status
    decision
  }
}
```

## Eventos Kafka

El servicio emite los siguientes eventos:

1. `selection_report_generated`:
```json
{
  "selection_id": 1,
  "vacancy_id": 1,
  "candidate_id": 2,
  "report_summary": {
    "technical_evaluation": {
      "score": 85,
      "feedback": "Excelente conocimiento técnico"
    },
    "hr_evaluation": {
      "score": 90,
      "feedback": "Buena comunicación y actitud"
    }
  },
  "generation_date": "2024-03-01T14:00:00Z"
}
```

2. `candidate_selection_decision`:
```json
{
  "selection_id": 1,
  "vacancy_id": 1,
  "candidate_id": 2,
  "decision": "HIRE",
  "status": "SELECTED",
  "decision_date": "2024-03-01T15:00:00Z"
} 