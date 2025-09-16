from typing import Callable, Dict, Type
from llm_query.domain import queries

class AsyncQueryDispatcher:
    def __init__(self, query_handlers: Dict[Type[queries.Query], Callable]):
        self.query_handlers = query_handlers
    
    async def dispatch(self, query: queries.Query):
        handler = self.query_handlers[type(query)]
        return await handler(query)