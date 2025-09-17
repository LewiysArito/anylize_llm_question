from typing import Dict, Type, Callable
from llm_query.domain import queries
from llm_query.adapters import ollama
from llm_query.domain import queries

async def handler_generate_response(
    query: queries.GenerateLLMQuery,
    llm: ollama.AbstractLLMClient,
)->str:
    response = await llm.generate(
       model=query.model,
       prompt=query.prompt,
       temperature=query.temperature 
    )

    return response

QUERY_HANDLERS: Dict[Type[queries.Query], Callable] = {
    queries.GenerateLLMQuery: handler_generate_response
}