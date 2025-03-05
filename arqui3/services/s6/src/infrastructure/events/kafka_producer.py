import json
import os
from typing import Any, Dict
from aiokafka import AIOKafkaProducer

class KafkaProducer:
    def __init__(self):
        self.producer = None
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def send_message(self, topic: str, message: Dict[str, Any]):
        if not self.producer:
            raise RuntimeError("El productor de Kafka no está inicializado")
        await self.producer.send_and_wait(topic, message) 