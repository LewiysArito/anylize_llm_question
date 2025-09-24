from dataclasses import asdict
from datetime import datetime
import json
import logging
import abc
import asyncio

from typing import List, Optional
from uuid import UUID
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError
from ipaddress import IPv4Address

from analyze_user_query import bootstrap, config
from analyze_user_query.domain import commands
from analyze_user_query.domain.model import DataUserQuery
from analyze_user_query.service_layer.messagebus import AsyncMessageBus

logger = logging.getLogger(__name__)
DEFAULT_BASE_URL = config.get_kafka_url()
bus, _ = bootstrap.bootstrap()

class AbstractEventConsumer(abc.ABC):
    @abc.abstractmethod
    async def start(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    async def stop(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    async def handle_user_query_for_analytics(bus: AsyncMessageBus):
        raise NotImplementedError

    @abc.abstractmethod
    async def main():
        raise NotImplementedError

class KafkaConsumer(AbstractEventConsumer):
    def __init__(self, topics: List[str] = ["llm_anylize"], bootstrap_servers = DEFAULT_BASE_URL, bus = bus):
        self.consumer: Optional[AIOKafkaConsumer] = None
        self.bootstrap_servers = bootstrap_servers
        self.topics = topics
        self.bus = bus

    async def handle_user_query_for_analytics(self, data_user_query: DataUserQuery):
        cmd = commands.AnylizeUserQuery(asdict(data_user_query))
        self.bus.handle(cmd)        

    async def main(self):
        await self.start()

        try:
            async for msg in self.consumer:
                logger.info(f"handling message {msg}")
                message = json.loads(msg.value)
                data_user_query = DataUserQuery(
                    event_id=UUID(message["event_id"]),
                    ip_address=IPv4Address(message["ip_address"]),
                    timestamp=datetime.strptime(message["timestamp"], "%Y-%m-%d %H:%M:%S"),
                    **message
                )
                await self.handle_user_query_for_analytics(data_user_query, bus)

        except KafkaError:
            logger.exception(f"Kafka error {e}")
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
        finally:
            await self.stop()

    async def start(self):
        if self.consumer is None:
            self.consumer = AIOKafkaConsumer(
                *self.topics,
                bootstrap_servers=self.bootstrap_servers,
                group_id="base_group",
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                key_serializer=lambda k: str(k).encode('utf-8') if k else None,
            )

        await self.consumer.start()
        logger.info(f"Kafka consumer for topics started: {self.topics}")
    
    async def stop(self):
        if self.consumer:
            await self.consumer.stop()
            logger.info("Kafka consumer stopped")
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()
    
    async def __aenter__(self):
        await self.start()
        return self
    
if __name__ == "__main__":
    kafka_consumer = KafkaConsumer()  
    asyncio.run(kafka_consumer.main())