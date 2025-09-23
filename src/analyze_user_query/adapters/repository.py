import abc
import logging
from uuid import UUID
import clickhouse_connect as ch
from clickhouse_connect.driver.asyncclient import AsyncClient
from typing import List, Optional
from analyze_user_query.domain import model

logger = logging.getLogger(__name__)

class AbstractColumnRepository(abc.ABC):

    @abc.abstractmethod
    async def add(self, analytic: model.Analytic) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    async def add_batch(self, analytics: List[model.Analytic]) -> None:
        raise NotImplementedError
        
    @abc.abstractmethod
    async def get_by_event_id(self, id: UUID) -> Optional[model.Analytic]:
        raise NotImplementedError
        
    @abc.abstractmethod
    async def get_by_user_id(self, user_ip: int, limit: int = 100) -> List[model.Analytic]:
        raise NotImplementedError
    
    @abc.abstractmethod
    async def get_by_country(self, country: str) -> List[model.Analytic]:
        raise NotImplementedError
    
class ClickhouseRepository(AbstractColumnRepository):
    def __init__(self, session: AsyncClient):
        super().__init__()
        self.session = session

    async def add(self, analytic: model.Analytic) -> None:
        pass
    
    async def add_batch(self, analytics: List[model.Analytic]) -> None:
        pass
        
    async def get_by_event_id(self, id: UUID) -> Optional[model.Analytic]:
        pass
        
    async def get_by_user_id(self, user_ip: int, limit: int = 100) -> List[model.Analytic]:
        pass
    
    async def get_by_country(self, country: str) -> List[model.Analytic]:
        pass