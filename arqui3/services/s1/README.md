# Servicio de Requisiciones

Este es un microservicio construido con FastAPI y GraphQL que implementa la Arquitectura Limpia para gestionar requisiciones de personal.

## Requisitos

- Python 3.8+
- PostgreSQL
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
- Crear una base de datos PostgreSQL llamada `requisitions_db`
- Ajustar las credenciales en `.env` si es necesario

## Ejecutar el servicio

```bash
uvicorn src.main:app --reload --port 8001
```

El servicio estará disponible en `http://localhost:8001`
La interfaz GraphQL estará disponible en `http://localhost:8001/graphql`

## Integración con el Gateway

Este servicio está diseñado para trabajar en conjunto con el API Gateway. Para una correcta integración:

1. Asegúrese de que el servicio esté ejecutándose en el puerto 8001 (o actualice la variable `REQUISITIONS_SERVICE_URL` en el archivo `.env` del gateway).
2. Verifique que las respuestas GraphQL sigan la estructura esperada por el gateway.
3. El gateway expondrá las operaciones de este servicio en `http://localhost:8000/graphql`.

## Ejemplos de Queries GraphQL

### Crear una requisición
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
  }
}
```

### Listar requisiciones
```graphql
query {
  requisitions(status: "PENDING") {
    id
    positionName
    status
    createdAt
  }
}
```

### Revisar una requisición
```graphql
mutation {
  reviewRequisition(requisitionId: 1, approve: true) {
    id
    positionName
    status
  }
}
```

## Endpoints GraphQL disponibles para el Gateway

### Queries
- `requisition(requisitionId: Int!)`: Obtiene una requisición por su ID
- `requisitions(status: String)`: Lista todas las requisiciones, opcionalmente filtradas por estado

### Mutations
- `createRequisition(input: RequisitionInput!)`: Crea una nueva requisición
- `reviewRequisition(requisitionId: Int!, approve: Boolean!)`: Aprueba o rechaza una requisición 