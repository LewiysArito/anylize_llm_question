import asyncio
from uuid import UUID

from analyze_user_query import bootstrap, config
from analyze_user_query.domain import queries
from analyze_user_query.adapters.taskiq_redis_manager import TaskIqRedisTaskManager

logger = config.logger
task_manager = TaskIqRedisTaskManager()
_, dispatcher = bootstrap.bootstrap()

@task_manager.get_broker().task("definition_language_problem")
async def task_definition_language_problem(event_id: UUID, text: str) -> str:
    logger.info(f"Handling id={event_id} for task definition_language_problem")
    query = queries.DefineLanguage(text)
    return await dispatcher.dispatch(query)

@task_manager.get_broker().task("definition_region_by_ip")
async def task_definition_region_by_ip(event_id: UUID, ip_address: str) -> str:
    logger.info(f"Handling id={event_id} for task definition_region_by_ip")
    query = queries.DefineRegionByIp(ip_address)
    return await dispatcher.dispatch(query)

if __name__ == "__main__":
    asyncio.run(task_manager.start_worker())