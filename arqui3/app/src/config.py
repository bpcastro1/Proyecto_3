import os
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno desde el archivo .env
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    # Configuración de la aplicación
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT = int(os.getenv("APP_PORT", "9000"))
    
    # URLs de los microservicios
    REQUISITION_SERVICE_URL = os.getenv("REQUISITION_SERVICE_URL", "http://localhost:8001")
    VACANCY_SERVICE_URL = os.getenv("VACANCY_SERVICE_URL", "http://localhost:8002")
    CANDIDATE_SERVICE_URL = os.getenv("CANDIDATE_SERVICE_URL", "http://localhost:8003")
    EVALUATION_SERVICE_URL = os.getenv("EVALUATION_SERVICE_URL", "http://localhost:8004")
    INTERVIEW_SERVICE_URL = os.getenv("INTERVIEW_SERVICE_URL", "http://localhost:8005")
    SELECTION_SERVICE_URL = os.getenv("SELECTION_SERVICE_URL", "http://localhost:8006")
    GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:8000")
    
    # Configuración de Kafka
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    KAFKA_TOPIC_PREFIX = os.getenv("KAFKA_TOPIC_PREFIX", "recruiting")
    
    @classmethod
    def get_service_url(cls, service_name):
        """Devuelve la URL del servicio solicitado"""
        service_map = {
            "requisition": cls.REQUISITION_SERVICE_URL,
            "vacancy": cls.VACANCY_SERVICE_URL,
            "candidate": cls.CANDIDATE_SERVICE_URL,
            "evaluation": cls.EVALUATION_SERVICE_URL,
            "interview": cls.INTERVIEW_SERVICE_URL, 
            "selection": cls.SELECTION_SERVICE_URL,
            "gateway": cls.GATEWAY_URL
        }
        
        return service_map.get(service_name.lower(), cls.GATEWAY_URL) 