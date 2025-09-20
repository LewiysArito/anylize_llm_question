from typing import Dict, Type, Callable
from analyze_user_query.domain import queries
from analyze_user_query.adapters import ollama
from analyze_user_query.domain import queries

QUERY_HANDLERS: Dict[Type[queries.Query], Callable] = {
}