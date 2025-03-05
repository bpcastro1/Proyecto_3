# Servicio de Evaluación (S4)

Este servicio gestiona las evaluaciones técnicas y psicotécnicas de los candidatos, permitiendo registrar resultados y generar reportes.

## Requisitos Previos

- Python 3.8+
- PostgreSQL
- pip (gestor de paquetes de Python)

## Configuración

1. Crear un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate     # En Windows
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno en el archivo `.env`:
```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

## Ejecutar el Servicio

```bash
cd services/s4
python src/main.py
```

El servicio se iniciará en `http://localhost:8004`

## Pruebas con GraphQL

### Interfaz Gráfica
Accede a la interfaz interactiva de GraphQL en:
```
http://localhost:8004/graphql
```

### Ejemplos de Queries y Mutations

#### 1. Crear Evaluación Técnica
```graphql
mutation {
  createEvaluation(
    input: {
      candidateId: 1,
      testType: TECHNICAL
    }
  ) {
    id
    candidateId
    testType
    status
  }
}
```

#### 2. Crear Evaluación Psicotécnica
```graphql
mutation {
  createEvaluation(
    input: {
      candidateId: 1,
      testType: PSYCHOMETRIC
    }
  ) {
    id
    candidateId
    testType
    status
  }
}
```

#### 3. Registrar Resultado Técnico
```graphql
mutation {
  updateTechnicalResult(
    input: {
      evaluationId: 1,
      programmingScore: 85,
      problemSolvingScore: 90,
      technicalKnowledge: "Excelente conocimiento en Python y bases de datos"
    }
  ) {
    id
    evaluationId
    programmingScore
    problemSolvingScore
    technicalKnowledge
  }
}
```

#### 4. Registrar Resultado Psicotécnico
```graphql
mutation {
  updatePsychometricResult(
    input: {
      evaluationId: 2,
      personalityTraits: "Liderazgo, Trabajo en equipo",
      cognitiveScore: 92,
      emotionalIntelligence: 88
    }
  ) {
    id
    evaluationId
    personalityTraits
    cognitiveScore
    emotionalIntelligence
  }
}
```

#### 5. Consultar Evaluación por ID
```graphql
query {
  evaluation(id: 1) {
    id
    candidateId
    testType
    status
    score
    feedback
    created_at
  }
}
```

#### 6. Listar Todas las Evaluaciones
```graphql
query {
  evaluations {
    id
    candidateId
    testType
    status
    score
  }
}
```

#### 7. Consultar Evaluaciones por Candidato
```graphql
query {
  evaluationsByCandidate(candidateId: 1) {
    id
    testType
    status
    score
    created_at
  }
}
```

## Endpoints REST para Reportes

### Generar Reporte Excel
```bash
curl -X POST http://localhost:8004/reports/1/excel -o reporte_evaluacion.xlsx
```

### Generar Reporte PDF
```bash
curl -X POST http://localhost:8004/reports/1/pdf -o reporte_evaluacion.pdf
```

## Estructura de Datos

### Tipos de Evaluación
- `TECHNICAL`: Evaluación técnica
- `PSYCHOMETRIC`: Evaluación psicotécnica

### Estados de Evaluación
- `PENDING`: Pendiente
- `IN_PROGRESS`: En progreso
- `COMPLETED`: Completada
- `FAILED`: Fallida

### Campos de Resultado Técnico
- `programmingScore`: Puntuación en programación (0-100)
- `problemSolvingScore`: Puntuación en resolución de problemas (0-100)
- `technicalKnowledge`: Descripción del conocimiento técnico

### Campos de Resultado Psicotécnico
- `personalityTraits`: Rasgos de personalidad identificados
- `cognitiveScore`: Puntuación cognitiva (0-100)
- `emotionalIntelligence`: Puntuación de inteligencia emocional (0-100)

## Notas Adicionales

- Los reportes generados incluyen todos los detalles de las evaluaciones del candidato
- Las puntuaciones finales se calculan automáticamente como promedio de las subpuntuaciones
- El servicio maneja automáticamente las fechas de creación y actualización
- Todos los endpoints GraphQL requieren Content-Type: application/json 