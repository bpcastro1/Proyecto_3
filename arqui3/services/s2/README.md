# Servicio de Vacantes

Este es un microservicio construido con FastAPI y GraphQL que implementa la Arquitectura Limpia para gestionar la publicación de vacantes.

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
- Crear una base de datos PostgreSQL llamada `vacancies_db`
- Ajustar las credenciales en `.env` si es necesario

4. Configurar Kafka:
- Asegurarse de que Kafka está ejecutándose en `localhost:9092`
- Los tópicos necesarios son:
  - `vacancy_published`
  - `vacancy_closed`

## Ejecutar el servicio

```bash
uvicorn src.main:app --reload --port 8002
```

El servicio estará disponible en `http://localhost:8002`
La interfaz GraphQL estará disponible en `http://localhost:8002/graphql`

## Integración con el Gateway

Este servicio está diseñado para trabajar en conjunto con el API Gateway. Para una correcta integración:

1. Asegúrese de que el servicio esté ejecutándose en el puerto 8002 (o actualice la variable `VACANCIES_SERVICE_URL` en el archivo `.env` del gateway).
2. Verifique que las respuestas GraphQL sigan la estructura esperada por el gateway.
3. El gateway expondrá las operaciones de este servicio en `http://localhost:8000/graphql`.
4. Este servicio comunica eventos a otros servicios a través de Kafka, asegúrese de que Kafka esté correctamente configurado.

## Ejemplos de Queries GraphQL

### Publicar una vacante
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
    status
    publicationDate
  }
}
```

### Listar vacantes
```graphql
query {
  vacancies(status: "PUBLISHED") {
    id
    requisitionId
    platforms
    status
    publicationDate
  }
}
```

### Cerrar una vacante
```graphql
mutation {
  closeVacancy(vacancyId: 1) {
    id
    requisitionId
    status
    closingDate
  }
}
```

## Eventos de Kafka

El servicio emite dos tipos de eventos:

1. `vacancy_published`: Cuando una vacante es publicada
```json
{
  "vacancy_id": 1,
  "requisition_id": 1,
  "platforms": ["LINKEDIN", "INDEED"],
  "publication_date": "2024-02-23T10:00:00Z"
}
```

2. `vacancy_closed`: Cuando una vacante es cerrada
```json
{
  "vacancy_id": 1,
  "requisition_id": 1,
  "closing_date": "2024-02-24T15:30:00Z"
} 
```

## Endpoints GraphQL disponibles para el Gateway

### Queries
- `vacancy(vacancyId: Int!)`: Obtiene una vacante por su ID
- `vacancies(status: String)`: Lista todas las vacantes, opcionalmente filtradas por estado

### Mutations
- `publishVacancy(input: VacancyInput!)`: Publica una nueva vacante basada en una requisición aprobada
- `closeVacancy(vacancyId: Int!)`: Cierra una vacante publicada 