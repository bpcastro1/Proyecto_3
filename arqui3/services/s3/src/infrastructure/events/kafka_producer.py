from aiokafka import AIOKafkaProducer
import json
import os

class KafkaProducer:
    def __init__(self):
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers
        )

    async def start(self):
        """Inicia el productor de Kafka"""
        await self.producer.start()

    async def stop(self):
        """Detiene el productor de Kafka"""
        await self.producer.stop()

    async def send_message(self, topic: str, message: dict):
        """Envía un mensaje al tópico especificado"""
        try:
            value_json = json.dumps(message).encode('utf-8')
            await self.producer.send_and_wait(topic, value_json)
        except Exception as e:
            print(f"Error sending message to Kafka: {e}")
            raise 