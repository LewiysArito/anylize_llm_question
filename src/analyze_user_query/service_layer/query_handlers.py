from typing import Dict, Type, Callable
from anylize_user_query.domain import queries
from anylize_user_query.adapters import ollama
from anylize_user_query.domain import queries

QUERY_HANDLERS: Dict[Type[queries.Query], Callable] = {
}