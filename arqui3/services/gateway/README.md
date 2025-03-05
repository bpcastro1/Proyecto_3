# Gateway del Proceso de Selección de Personal

Este gateway unifica todos los servicios del proceso de selección de personal a través de una única API GraphQL.

## Requisitos Previos

1. **Bases de Datos PostgreSQL**
   - Requisiciones (s1): Puerto 5432
   - Vacantes (s2): Puerto 5433
   - Candidatos (s3): Puerto 5434
   - Evaluaciones (s4): Puerto 5435
   - Entrevistas (s5): Puerto 5436
   - Selección (s6): Puerto 5437

2. **Apache Kafka**
   - Puerto: 9092

3. **Microservicios**
   - Requisiciones (s1): http://localhost:8001
   - Vacantes (s2): http://localhost:8002
   - Candidatos (s3): http://localhost:8003
   - Evaluaciones (s4): http://localhost:8004
   - Entrevistas (s5): http://localhost:8005
   - Selección (s6): http://localhost:8006

## Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: .\venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Iniciar el gateway:
```bash
uvicorn src.main:app --reload --port 8000
```

El gateway estará disponible en:
- API Gateway: http://localhost:8000
- GraphQL Playground: http://localhost:8000/graphql
- Documentación: http://localhost:8000/docs

## Flujo del Proceso de Selección

### 1. Gestión de Requisiciones

#### Crear una Requisición
```graphql
mutation {
  createRequisition(
    input: {
      positionName: "Senior Python Developer"
      functions: ["Desarrollo backend", "Diseño de arquitectura"]
      salaryCategory: "Senior"
      profile: "Desarrollador con 5+ años de experiencia en Python"
    }
  ) {
    id
    positionName
    status
    createdAt
  }
}
```

#### Consultar una Requisición
```graphql
query {
  getRequisition(requisitionId: 1) {
    id
    positionName
    functions
    salaryCategory
    profile
    status
    createdAt
  }
}
```

### 2. Gestión de Vacantes

#### Publicar una Vacante
```graphql
mutation {
  publishVacancy(
    input: {
      requisitionId: 1
      platforms: ["LINKEDIN", "INDEED"]
    }
  ) {
    id
    requisitionId
    platforms
    status
    publicationDate
  }
}
```

#### Consultar Vacantes
```graphql
query {
  vacancies(status: "PUBLISHED") {
    id
    requisitionId
    platforms
    status
    publicationDate
    closingDate
  }
}
```

### 3. Gestión de Candidatos

#### Registrar un Candidato
```graphql
mutation {
  submitCandidateApplication(
    input: {
      name: "Juan Pérez"
      email: "juan@email.com"
      resumeUrl: "https://example.com/cv.pdf"
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

#### Listar Candidatos por Vacante
```graphql
query {
  listCandidatesByVacancy(vacancyId: 1) {
    id
    name
    email
    status
    skills
    experienceYears
  }
}
```

#### Filtrar Candidatos
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
    status
  }
}
```

### 4. Gestión de Evaluaciones

#### Asignar Evaluaciones
```graphql
mutation {
  assignEvaluation(
    input: {
      candidateId: 1
      vacancyId: 1
      tests: [
        {
          name: "Technical Test"
          type: "TECHNICAL"
          durationMinutes: 120
          minScoreRequired: 70
        },
        {
          name: "English Test"
          type: "LANGUAGE"
          durationMinutes: 60
          minScoreRequired: 80
        }
      ]
    }
  ) {
    id
    status
    assignedDate
  }
}
```

#### Enviar Resultados de Prueba
```graphql
mutation {
  submitTestResult(
    input: {
      evaluationId: 1
      testName: "Technical Test"
      score: 85
      comments: "Excelente desempeño en pruebas técnicas"
    }
  ) {
    id
    status
    scores {
      testName
      score
    }
  }
}
```

### 5. Gestión de Entrevistas

#### Programar Entrevista
```graphql
mutation {
  scheduleInterview(
    input: {
      candidateId: 1
      interviewerId: 1
      vacancyId: 1
      interviewType: "TECHNICAL"
      scheduledTime: "2024-03-01T14:00:00Z"
      durationMinutes: 60
      location: "https://meet.google.com/abc-defg-hij"
    }
  ) {
    id
    status
    scheduledTime
  }
}
```

#### Registrar Feedback de Entrevista
```graphql
mutation {
  submitFeedback(
    interviewId: 1
    feedback: {
      strengths: ["Conocimiento técnico sólido", "Buena comunicación"]
      weaknesses: ["Poca experiencia en liderazgo"]
      technicalScore: 85
      communicationScore: 90
      cultureFitScore: 88
      recommendation: "HIRE"
      notes: "Candidato muy prometedor"
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

### 6. Gestión de Selección

#### Generar Reporte Final
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
      additionalNotes: "Candidato recomendado para contratación"
    }
  ) {
    id
    status
    report {
      technicalEvaluation {
        score
        feedback
      }
      hrEvaluation {
        score
        feedback
      }
    }
  }
}
```

#### Ver Proceso de Selección
```graphql
query {
  getSelectionProcess(vacancyId: 1) {
    id
    status
    report {
      technicalEvaluation {
        score
        feedback
      }
      hrEvaluation {
        score
        feedback
      }
    }
    decision
  }
}
```

## Flujo Completo del Proceso

1. Crear una requisición de personal
2. Publicar la vacante en las plataformas seleccionadas
3. Recibir y registrar candidatos
4. Asignar y realizar evaluaciones
5. Programar y realizar entrevistas
6. Generar reporte final y tomar decisión

## Notas Importantes

1. Asegúrese de que todos los servicios estén en ejecución antes de usar el gateway
2. Las credenciales y configuraciones específicas deben establecerse en el archivo `.env`
3. Los errores de los servicios individuales se propagarán a través del gateway
4. Todas las fechas deben proporcionarse en formato ISO 8601

## Manejo de Errores

El gateway proporciona mensajes de error detallados que incluyen:
- Código de error
- Mensaje descriptivo
- Servicio de origen
- Detalles adicionales cuando estén disponibles

## Monitoreo

El gateway expone métricas básicas en `/metrics` y estado de salud en `/health` 