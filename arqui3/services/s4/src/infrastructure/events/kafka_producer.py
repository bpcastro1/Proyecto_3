import json
import logging
from typing import Any, Dict
from aiokafka import AIOKafkaProducer

logger = logging.getLogger(__name__)

class KafkaProducer:
    def __init__(self, bootstrap_servers: str = 'localhost:9092'):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
        self.is_connected = False

    async def start(self):
        """Inicia el productor de Kafka"""
        try:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            await self.producer.start()
            self.is_connected = True
            logger.info("Conexión exitosa con Kafka")
        except Exception as e:
            logger.warning(f"No se pudo conectar con Kafka: {str(e)}")
            self.is_connected = False

    async def stop(self):
        """Detiene el productor de Kafka"""
        if self.producer and self.is_connected:
            try:
                await self.producer.stop()
                self.is_connected = False
            except Exception as e:
                logger.error(f"Error al detener el productor de Kafka: {str(e)}")

    async def send_message(self, topic: str, message: Dict[str, Any]):
        """Envía un mensaje al tópico especificado"""
        if not self.is_connected:
            logger.warning(f"No se pudo enviar el mensaje a Kafka (topic: {topic}): No hay conexión")
            return

        try:
            await self.producer.send_and_wait(topic, message)
            logger.info(f"Mensaje enviado exitosamente a Kafka (topic: {topic})")
        except Exception as e:
            logger.error(f"Error al enviar mensaje a Kafka (topic: {topic}): {str(e)}") 