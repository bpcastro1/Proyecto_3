# Sistema de Gestión de Selección de Personal

Esta aplicación permite gestionar el proceso completo de selección de personal, desde la requisición inicial hasta la contratación final, integrando múltiples microservicios especializados.

## Características

- **Gestión de Requisiciones**: Creación y aprobación de requisiciones de personal.
- **Publicación de Vacantes**: Publicación de vacantes en diversas plataformas.
- **Gestión de Candidatos**: Registro y seguimiento de candidatos.
- **Evaluaciones**: Gestión de pruebas técnicas y psicotécnicas.
- **Entrevistas**: Programación y registro de retroalimentación de entrevistas.
- **Selección Final**: Consolidación de resultados y toma de decisiones de contratación.
- **Reportes**: Generación de informes en PDF y Excel.

## Arquitectura

La aplicación está desarrollada siguiendo una arquitectura de microservicios:

- **Servicio de Requisiciones (s1)**: Gestiona las solicitudes de contratación.
- **Servicio de Vacantes (s2)**: Maneja la publicación y cierre de vacantes.
- **Servicio de Candidatos (s3)**: Administra la información de los candidatos.
- **Servicio de Evaluación (s4)**: Gestiona las pruebas y evaluaciones.
- **Servicio de Entrevistas (s5)**: Coordina las entrevistas y su retroalimentación.
- **Servicio de Selección (s6)**: Consolida la información para la decisión final.
- **API Gateway**: Centraliza las peticiones a todos los servicios.

## Tecnologías Utilizadas

- **Backend**: Python con FastAPI
- **Frontend**: HTML, CSS, JavaScript con Bootstrap
- **Base de Datos**: PostgreSQL
- **Comunicación Asíncrona**: Apache Kafka
- **Documentación API**: Swagger/OpenAPI
- **Reportes**: ReportLab (PDF) y Pandas (Excel)

## Requisitos Previos

1. Python 3.8 o superior
2. PostgreSQL
3. Apache Kafka
4. Microservicios del sistema de selección (s1-s6 y gateway)

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd app
```

2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
   - Copiar el archivo `.env.example` a `.env`
   - Ajustar las variables según la configuración de tu entorno

5. Iniciar la aplicación:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 9000
```

## Uso

Una vez iniciada la aplicación, accede a través de tu navegador:

- **Interfaz de Usuario**: http://localhost:9000
- **Documentación API**: http://localhost:9000/docs
- **Monitoreo**: http://localhost:9000/health y http://localhost:9000/metrics

## Flujo del Proceso

1. **Solicitud de Requisición**: Crear una requisición de personal con detalles del cargo.
2. **Publicación de Vacante**: Publicar la vacante en plataformas internas o externas.
3. **Recepción de Postulaciones**: Registrar candidatos que aplican a la vacante.
4. **Evaluaciones**: Asignar y registrar resultados de pruebas.
5. **Entrevistas**: Programar entrevistas y registrar feedback.
6. **Selección Final**: Generar reporte final y tomar decisión de contratación.
7. **Cierre del Proceso**: Cerrar la vacante una vez completado el proceso.

## Estructura del Proyecto

```
app/
├── src/                    # Código fuente
│   ├── controllers/        # Controladores de la aplicación
│   ├── routes/             # Rutas de la API
│   ├── services/           # Servicios para comunicación con microservicios
│   ├── config.py           # Configuración de la aplicación
│   ├── graphql_client.py   # Cliente GraphQL para comunicación con servicios
│   ├── kafka_client.py     # Cliente Kafka para comunicación asíncrona
│   └── main.py             # Punto de entrada de la aplicación
├── static/                 # Archivos estáticos
│   ├── css/                # Hojas de estilo
│   └── js/                 # Scripts JavaScript
├── templates/              # Plantillas HTML
├── .env                    # Variables de entorno
└── requirements.txt        # Dependencias del proyecto
```

## Contribución

1. Hacer un fork del repositorio
2. Crear una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Hacer commit de tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Hacer push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## Licencia

Este proyecto está licenciado bajo [MIT License](LICENSE). 