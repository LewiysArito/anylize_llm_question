import logging
import asyncio
from uuid import UUID

from analyze_user_query import bootstrap
from analyze_user_query.domain import queries
from analyze_user_query.adapters.taskiq_redis_manager import TaskIqRedisTaskManager


logger = logging.getLogger(__name__)
task_manager = TaskIqRedisTaskManager()
_, dispatcher = bootstrap.bootstrap()

@task_manager.get_broker().task("definition_language_problem")
async def task_definition_language_problem(event_id: UUID, text: str) -> str:
    logger.info(f"Handling id={event_id} for task definition_language_problem")
    query = queries.DefineLanguage(text)
    return await dispatcher.dispatch(query)

if __name__ == "__main__":
    asyncio.run(task_manager.get_broker().startup())