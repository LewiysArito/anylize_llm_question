import logging
import asyncio
from taskiq import InMemoryBroker

from analyze_user_query import bootstrap
from analyze_user_query.domain import queries
from analyze_user_query.service_layer.query_dispatcher import AsyncQueryDispatcher

logger = logging.getLogger(__name__)
task_broker = InMemoryBroker()
_, dispatcher = bootstrap.bootstrap()

@task_broker.task("definition_language_problem")
async def task_definition_language_problem(text: str)->str:
    query = queries.DefineLanguage(text)
    return await dispatcher.handle(query)

async def start_worker():
    logger.info("Starting TaskIQ worker...")
    await task_broker.startup()
    
    try:
        await task_broker.listen()
    finally:
        await task_broker.shutdown()

if __name__ == "__main__":  
    asyncio.run(start_worker())