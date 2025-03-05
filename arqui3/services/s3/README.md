# Servicio de Candidatos

Este es un microservicio construido con FastAPI y GraphQL que implementa la Arquitectura Limpia para gestionar candidatos y sus postulaciones.

## Requisitos

- Python 3.8+
- PostgreSQL
- Apache Kafka
- pip

## Instalación

1. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar la base de datos:
- Crear una base de datos PostgreSQL llamada `candidates_db`
- Ajustar las credenciales en `src/infrastructure/database/config.py` si es necesario

4. Configurar Kafka:
- Asegurarse de que Kafka está ejecutándose en `localhost:9092`
- Los tópicos necesarios son:
  - `application_submitted`
  - `candidate_status_updated`

## Ejecutar el servicio

```bash
uvicorn src.main:app --reload
```

El servicio estará disponible en `http://localhost:8000`
La interfaz GraphQL estará disponible en `http://localhost:8000/graphql`

## Ejemplos de Queries GraphQL

### Enviar una postulación
```graphql
mutation {
  submitApplication(
    input: {
      name: "Juan Pérez"
      email: "juan.perez@email.com"
      resumeUrl: "https://storage.com/resumes/juan-perez-cv.pdf"
      vacancyId: 1
      skills: ["Python", "FastAPI", "PostgreSQL"]
      experienceYears: 5
    }
  ) {
    id
    name
    status
    applicationDate
  }
}
```

### Listar candidatos de una vacante
```graphql
query {
  candidates(vacancyId: 1) {
    id
    name
    email
    status
    skills
    experienceYears
  }
}
```

### Filtrar candidatos
```graphql
query {
  filterCandidates(
    filters: {
      vacancyId: 1
      status: "PENDING"
      requiredSkills: ["Python", "FastAPI"]
      minExperience: 3
    }
  ) {
    id
    name
    skills
    experienceYears
    status
  }
}
```

### Actualizar estado de un candidato
```graphql
mutation {
  updateCandidateStatus(
    candidateId: 1
    status: "INTERVIEWED"
  ) {
    id
    name
    status
  }
}
```

## Eventos de Kafka

El servicio emite dos tipos de eventos:

1. `application_submitted`: Cuando se recibe una nueva postulación
```json
{
  "candidate_id": 1,
  "vacancy_id": 1,
  "candidate_name": "Juan Pérez",
  "candidate_email": "juan.perez@email.com",
  "application_date": "2024-02-23T10:00:00Z"
}
```

2. `candidate_status_updated`: Cuando se actualiza el estado de un candidato
```json
{
  "candidate_id": 1,
  "vacancy_id": 1,
  "new_status": "INTERVIEWED",
  "candidate_name": "Juan Pérez"
}
``` 