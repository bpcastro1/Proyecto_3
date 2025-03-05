import json
import logging
import asyncio
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from .config import Config

logger = logging.getLogger(__name__)

class KafkaClient:
    """Cliente para la comunicación asíncrona con Apache Kafka"""
    
    def __init__(self):
        self.bootstrap_servers = Config.KAFKA_BOOTSTRAP_SERVERS
        self.topic_prefix = Config.KAFKA_TOPIC_PREFIX
        self.producer = None
        self.consumers = {}
        self.kafka_enabled = True  # Flag para controlar si Kafka está habilitado
        
    async def start_producer(self):
        """Inicia el productor de Kafka"""
        try:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            await self.producer.start()
            logger.info("Productor Kafka iniciado")
        except Exception as e:
            logger.warning(f"No se pudo iniciar el productor Kafka: {e}")
            self.kafka_enabled = False
            logger.info("La aplicación funcionará sin Kafka")
    
    async def stop_producer(self):
        """Detiene el productor de Kafka"""
        if self.producer and self.kafka_enabled:
            await self.producer.stop()
            logger.info("Productor Kafka detenido")
    
    async def send_message(self, topic_suffix, message):
        """
        Envía un mensaje a un topic de Kafka.
        
        Args:
            topic_suffix (str): Sufijo del topic (ej. "requisition.created")
            message (dict): Mensaje a enviar
            
        Returns:
            bool: True si el mensaje se envió correctamente, False en caso contrario
        """
        if not self.kafka_enabled or not self.producer:
            logger.warning(f"Kafka no está disponible. Mensaje no enviado: {topic_suffix}")
            return False
            
        try:
            topic = f"{self.topic_prefix}.{topic_suffix}"
            await self.producer.send_and_wait(topic, message)
            logger.info(f"Mensaje enviado a {topic}: {message}")
            return True
        except Exception as e:
            logger.error(f"Error al enviar mensaje a {topic_suffix}: {e}")
            return False
    
    async def start_consumer(self, topic_suffix, callback):
        """
        Inicia un consumidor para un topic específico.
        
        Args:
            topic_suffix (str): Sufijo del topic (ej. "requisition.created")
            callback (callable): Función a llamar cuando se recibe un mensaje
            
        Returns:
            bool: True si el consumidor se inició correctamente, False en caso contrario
        """
        if not self.kafka_enabled:
            logger.warning(f"Kafka no está disponible. Consumidor no iniciado: {topic_suffix}")
            return False
            
        try:
            topic = f"{self.topic_prefix}.{topic_suffix}"
            consumer = AIOKafkaConsumer(
                topic,
                bootstrap_servers=self.bootstrap_servers,
                group_id=f"recruitment_app",
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset="latest"
            )
            
            self.consumers[topic_suffix] = consumer
            
            # Iniciar el consumidor en una tarea separada
            asyncio.create_task(self._consume(consumer, callback))
            logger.info(f"Consumidor iniciado para {topic}")
            return True
        except Exception as e:
            logger.error(f"Error al iniciar consumidor para {topic_suffix}: {e}")
            return False
    
    async def _consume(self, consumer, callback):
        """Proceso interno de consumo de mensajes"""
        try:
            await consumer.start()
            async for msg in consumer:
                try:
                    await callback(msg.value)
                except Exception as e:
                    logger.error(f"Error en callback de consumidor: {e}")
        except Exception as e:
            logger.error(f"Error en consumidor: {e}")
        finally:
            await consumer.stop()
    
    async def stop_consumer(self, topic_suffix):
        """Detiene un consumidor específico"""
        if topic_suffix in self.consumers and self.kafka_enabled:
            await self.consumers[topic_suffix].stop()
            del self.consumers[topic_suffix]
            logger.info(f"Consumidor para {topic_suffix} detenido")
    
    async def stop_all_consumers(self):
        """Detiene todos los consumidores"""
        if self.kafka_enabled:
            for topic_suffix in list(self.consumers.keys()):
                await self.stop_consumer(topic_suffix)
            logger.info("Todos los consumidores detenidos") 