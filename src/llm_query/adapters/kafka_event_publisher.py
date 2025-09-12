import json
import abc
import logging
from typing import Optional
import uuid
from dataclasses import asdict
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError

from llm_query import config
from llm_query.domain import events

DEFAULT_BASE_URL = config.get_kafka_url()

logger = logging.getLogger(__name__)

class AbstractPublisher(abc.ABC):
    @abc.abstractmethod
    
    async def start(self):
        raise NotImplementedError
    async def publish(self, topic: str, event: events.Event):
        raise NotImplementedError
    async def stop(self):
        raise NotImplementedError

class KafkaPublisher:
    def __init__(self, bootstrap_servers: str = DEFAULT_BASE_URL):
        self.bootstrap_servers = bootstrap_servers
        self.producer: Optional[AIOKafkaProducer] = None

    async def start(self):
        if self.producer is None:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                key_serializer=lambda k: str(k).encode('utf-8') if k else None,
                acks='all'
            )
            await self.producer.start()
            logger.info("Kafka producer started")
    
    async def stop(self):
        if self.producer:
            await self.producer.stop()
            logger.info("Kafka producer stopped")
    
    async def publish(self, topic: str, event:events.Event):
        await self.start()
        
        try:
            key = event.id or str(uuid.uuid4())
            
            await self.producer.send(
                topic=topic,
                key=key,
                value=asdict(event)
            )
            
            logger.info(f"Message published to {topic} with key {key}")
            return key
            
        except KafkaError as e:
            logger.error(f"Failed to publish to {topic}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error publishing to {topic}: {e}")
            raise