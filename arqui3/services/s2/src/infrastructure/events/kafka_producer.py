import json
from typing import Any, Dict
from aiokafka import AIOKafkaProducer

class KafkaProducer:
    def __init__(self, bootstrap_servers: str = 'localhost:9092'):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    async def start(self):
        """Inicia el productor de Kafka"""
        await self.producer.start()

    async def stop(self):
        """Detiene el productor de Kafka"""
        await self.producer.stop()

    async def send_message(self, topic: str, message: Dict[str, Any]):
        """Envía un mensaje al tópico especificado"""
        try:
            await self.producer.send_and_wait(topic, message)
        except Exception as e:
            print(f"Error al enviar mensaje a Kafka: {str(e)}")
            raise 