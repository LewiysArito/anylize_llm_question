import json
import logging
import abc
import time

from typing import Any, Dict, Optional
from uuid import UUID
import uuid
from taskiq.kicker import AsyncKicker
from taskiq import TaskiqResult
from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker

from analyze_user_query import config

DEFAULT_URL_BROKER = config.get_urls_redis().get("url_broker")
DEFAULT_URL_BACKEND_RESULT= config.get_urls_redis().get("url_backend_result")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AbstractRedisTaskManager(abc.ABC):
    @abc.abstractmethod
    async def start_worker(self) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    async def shutdown_worker(self) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_broker(self) -> RedisStreamBroker:
        raise NotImplementedError

    @abc.abstractmethod
    def run_task_by_name(self, task_name: str, task_id: Optional[UUID]=None, kwargs = {}) -> Any:
        raise NotImplementedError

class TaskIqRedisTaskManager(AbstractRedisTaskManager):
    def __init__(self, 
            redis_url_broker = DEFAULT_URL_BROKER,
            redis_url_backend_result = DEFAULT_URL_BACKEND_RESULT,
        ):
        self._is_running = False
        self.broker = RedisStreamBroker(url=redis_url_broker).with_result_backend(
            RedisAsyncResultBackend(redis_url_backend_result,
            result_ex_time=20
        ))
    
    async def start_worker(self) -> None:
        if self._is_running:
            logger.warning("TaskIQ worker is already running")
            return
            
        logger.info("Starting TaskIQ Redis worker...")
        self.broker.is_worker_process = True

        await self.broker.startup()
        self._is_running = True
        try:
            async for message in self.broker.listen():
                new_data = json.loads(message.data.decode())
                await self._execute_task(new_data)
        except Exception as e:
            logger.error(f"TaskIQ worker error: {e}")
            raise
        finally:
            self._is_running = False
            await self.broker.shutdown()
            logger.info("TaskIQ worker shutdown completed")
    
    async def _execute_task(self, data: Dict[str, Any]) -> None:
        task_func = self.broker.find_task(data.get("task_name"))

        if task_func is None:
            logger.error(f"No registered task found for: {data.get("task_name")}")
        
        start_time = time.time()
        if len(data.get("args")) > 0:
            result_value = await task_func(*data.get("args"))
        elif len(data.get("kwargs").keys()) > 0:
            result_value = await task_func(**data.get("kwargs"))
        else:
            result_value = await task_func()
        
        execution_time = time.time() - start_time
        
        result = TaskiqResult(
            is_err=False,
            return_value=result_value,
            execution_time=execution_time,
        )
        await self.broker.result_backend.set_result(
            data.get("task_id"),
            result
        )
        logger.info(f"Task {data.get("task_name")} completed with result: {result}")

    async def shutdown_worker(self) -> None:
        logger.info("Shutting down TaskIQ worker...")
        if self._is_running:
            await self.broker.shutdown()
            self._is_running = False
        else:
            logger.info("TaskIQ worker was not running")

    def get_broker(self) -> RedisStreamBroker:
        return self.broker
        
    async def run_task_by_name(self, task_name: str, task_id: Optional[UUID]=None, kwargs = {}) -> Any:
        await self.broker.startup()
        async_kicker = AsyncKicker(task_name, self.broker, labels={})
        
        if not task_id:
          task_id = uuid.uuid4()
        
        async_kicker.custom_task_id = task_id
        taskiq = await async_kicker.kiq(**kwargs)
        
        result = await taskiq.wait_result()
        await self.broker.shutdown()
        return result.return_value
    
    @property
    def is_running(self) -> bool:
        return self._is_running