# Servicio de Entrevistas

Este es un microservicio construido con FastAPI y GraphQL para gestionar las entrevistas de candidatos. Permite programar entrevistas, registrar feedback y gestionar el ciclo de vida completo de las entrevistas.

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
createdb interviews_db

# Configurar las variables de entorno
export DATABASE_URL="postgresql+asyncpg://usuario:contraseña@localhost:5432/interviews_db"
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

1. Obtener una entrevista por ID:
```graphql
query {
  interview(interviewId: 1) {
    id
    candidateId
    interviewerId
    vacancyId
    interviewType
    scheduledTime
    status
    feedback {
      technicalScore
      communicationScore
      cultureFitScore
      recommendation
    }
  }
}
```

2. Listar entrevistas por vacante:
```graphql
query {
  interviewsByVacancy(vacancyId: 1) {
    id
    candidateId
    scheduledTime
    status
  }
}
```

### Mutations GraphQL

1. Programar una entrevista:
```graphql
mutation {
  scheduleInterview(
    input: {
      candidateId: 1
      interviewerId: 2
      vacancyId: 3
      interviewType: "TECHNICAL"
      scheduledTime: "2024-03-01T14:00:00Z"
      durationMinutes: 60
      location: "Google Meet"
    }
  ) {
    id
    scheduledTime
    status
  }
}
```

2. Enviar feedback de entrevista:
```graphql
mutation {
  submitFeedback(
    interviewId: 1
    feedback: {
      strengths: ["Experiencia técnica sólida", "Buena comunicación"]
      weaknesses: ["Poca experiencia en cloud"]
      technicalScore: 4.5
      communicationScore: 4.0
      cultureFitScore: 4.2
      recommendation: "HIRE"
      notes: "Candidato prometedor"
    }
  ) {
    id
    status
    feedback {
      recommendation
      technicalScore
    }
  }
}
```

## Eventos Kafka

El servicio emite los siguientes eventos:

1. `interview_scheduled`:
```json
{
  "interview_id": 1,
  "candidate_id": 1,
  "interviewer_id": 2,
  "vacancy_id": 3,
  "interview_type": "TECHNICAL",
  "scheduled_time": "2024-03-01T14:00:00Z",
  "duration_minutes": 60,
  "location": "Google Meet"
}
```

2. `interview_feedback_submitted`:
```json
{
  "interview_id": 1,
  "candidate_id": 1,
  "interviewer_id": 2,
  "vacancy_id": 3,
  "feedback": {
    "technical_score": 4.5,
    "communication_score": 4.0,
    "culture_fit_score": 4.2,
    "recommendation": "HIRE"
  },
  "submission_time": "2024-03-01T15:00:00Z"
}
```

3. `interview_rescheduled`:
```json
{
  "interview_id": 1,
  "candidate_id": 1,
  "interviewer_id": 2,
  "vacancy_id": 3,
  "new_time": "2024-03-02T14:00:00Z",
  "new_duration": 60,
  "rescheduled_at": "2024-02-28T10:00:00Z"
}
``` 