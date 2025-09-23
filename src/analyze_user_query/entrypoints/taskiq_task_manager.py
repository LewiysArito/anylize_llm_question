import logging
import asyncio
from taskiq_aio_kafka import AioKafkaBroker
from ftlangdetect import detect

from analyze_user_query import bootstrap, config

logger = logging.getLogger(__name__)
DEFAULT_BASE_URL = config.get_kafka_url()

bus = bootstrap.bootstrap()
broker = AioKafkaBroker(bootstrap_servers=DEFAULT_BASE_URL)
broker.configure_producer()
broker.configure_consumer()

async def definition_language_problem(text: str):
    code_country = asyncio.to_thread(detect, text)["lang"]
    return code_country.upper()

@broker.task("definition_language_problem")
async def task_definition_language_problem(text: str):
    return await definition_language_problem(text)