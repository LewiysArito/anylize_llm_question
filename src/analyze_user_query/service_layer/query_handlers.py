from typing import Dict, Type, Callable
from analyze_user_query.domain import queries
from analyze_user_query.adapters import language_detect 
from analyze_user_query.domain import queries

async def define_language(
    query: queries.DefineLanguage,
    language_detect: language_detect.AbstractFtlangDetect  
):
    return await language_detect.detect_language(query.text)

QUERY_HANDLERS: Dict[Type[queries.Query], Callable] = {
    queries.DefineLanguage: define_language  
}