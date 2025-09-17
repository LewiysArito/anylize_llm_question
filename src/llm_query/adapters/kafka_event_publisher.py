import json
import abc
import logging
from typing import List, Optional
import uuid
import asyncio

from dataclasses import asdict
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError
from llm_query import config
from llm_query.adapters import integration_events as int_event

DEFAULT_BASE_URL = config.get_kafka_url()
logger = logging.getLogger(__name__)

class AbstractPublisher(abc.ABC):
    @abc.abstractmethod
    
    async def start(self):
        raise NotImplementedError
    async def publish_one(self, topic: str, event: int_event.IntegrationEvent):
        raise NotImplementedError
    async def publish_many(self, topic: str, events: List[int_event.IntegrationEvent]):
        raise NotImplementedError
    async def stop(self):
        raise NotImplementedError

class KafkaPublisher(AbstractPublisher):
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
    
    async def publish_one(self, topic: str, event:int_event.IntegrationEvent):
        await self.start()
        try:
            key = event.event_id or str(uuid.uuid4())
            
            await self.producer.send(
                topic=topic,
                key=key,
                value=asdict(event)
            )
            
            logger.info(f"Message published to {topic} with key {key}")
            
        except KafkaError as e:
            logger.error(f"Failed to publish to {topic}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error publishing to {topic}: {e}")
            raise

    async def publish_many(self, topic: str, events:List[int_event.IntegrationEvent])->List[uuid.UUID]:
        await self.start()
        try:
            send_messages  = []
            for event in events:
                key = event.event_id or str(uuid.uuid4())
                
                send_message = await self.producer.send(
                    topic=topic,
                    key=key,
                    value=asdict(event)
                )
                
                logger.info(f"Message published to {topic} with key {key}")
                send_messages.append(key)
            
            await asyncio.gather(*send_messages)
        
        except KafkaError as e:
            logger.error(f"Failed to publish to {topic}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error publishing to {topic}: {e}")
            raise
    
    async def __aexit__(self,exc_type, exc_val, exc_tb):
        await self.stop()
    
    async def __aenter__(self):
        await self.start()
        return self
    
