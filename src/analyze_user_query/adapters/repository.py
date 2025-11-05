import abc
import clickhouse_connect as ch

from uuid import UUID
from clickhouse_connect.driver.asyncclient import AsyncClient
from typing import List, Optional
from analyze_user_query.domain import model
from analyze_user_query.adapters.orm import analyze_user_llm_query_mapper
from analyze_user_query.config import get_clickhouse_settings

CLICKHOUSE_HOST = str(get_clickhouse_settings().get("CLICKHOUSE_HOST"))
CLICKHOUSE_PORT = int(get_clickhouse_settings().get("CLICKHOUSE_PORT"))
CLICKHOUSE_PASSWORD = str(get_clickhouse_settings().get("CLICKHOUSE_PASSWORD"))
CLICKHOUSE_USERNAME = str(get_clickhouse_settings().get("CLICKHOUSE_USERNAME"))

async def get_async_client(host=CLICKHOUSE_HOST, port=CLICKHOUSE_PORT,
    password=CLICKHOUSE_PASSWORD, username=CLICKHOUSE_USERNAME)->AsyncClient:
    client = await ch.get_async_client(
        host = host,
        port = port,
        password=password,
        username=username
    )
    return client

class AbstractColumnRepository(abc.ABC):

    @abc.abstractmethod
    async def add(self, analytic: model.AnalyzedUserQuery) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    async def adds(self, analytics: List[model.AnalyzedUserQuery]) -> None:
        raise NotImplementedError
        
    @abc.abstractmethod
    async def get_by_event_id(self, id: UUID) -> Optional[model.AnalyzedUserQuery]:
        raise NotImplementedError
        
    @abc.abstractmethod
    async def get_by_user_id(self, user_ip: int, limit: int = 100) -> List[model.AnalyzedUserQuery]:
        raise NotImplementedError
    
    @abc.abstractmethod
    async def get_by_country(self, country: str) -> List[model.AnalyzedUserQuery]:
        raise NotImplementedError
    
class ClickhouseRepository(AbstractColumnRepository):
    async def __init__(self, session: AsyncClient, mapper = analyze_user_llm_query_mapper):
        if not session:
            session = await get_async_client()
        
        self.session = session
        self.mapper = mapper
    
    async def add(self, analytic: model.AnalyzedUserQuery) -> None:
        values = self.mapper.model_to_tuple(analytic)
        columns_name = [column.name for column in self.mapper.table.columns]
        query = self.mapper.table.generate_sql_for_insert(
            values,
            columns_name
        )
        await self.session.query(query)

    async def adds(self, analytics: List[model.AnalyzedUserQuery]) -> None:
        values = self.mapper.models_to_tuples(analytics)
        columns_name = [column.name for column in self.mapper.table.columns]
        query = self.mapper.table.generate_sql_for_insert(
            values,
            columns_name
        )
        await self.session.query(query)
        
    async def get_by_event_id(self, id: UUID) -> Optional[model.AnalyzedUserQuery]:
        pass
        
    async def get_by_user_id(self, user_ip: int, limit: int = 100) -> List[model.AnalyzedUserQuery]:
        pass
    
    async def get_by_country(self, country: str) -> List[model.AnalyzedUserQuery]:
        pass
