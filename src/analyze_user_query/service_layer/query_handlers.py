from typing import Dict, Optional, Type, Callable
from analyze_user_query.domain import queries
from analyze_user_query.adapters import language_detect 
from analyze_user_query.domain import queries
from analyze_user_query.adapters import ollama
from analyze_user_query.adapters import http_ip_geolocation
from analyze_user_query.adapters import taskiq_redis_manager
from analyze_user_query.domain.model import AnalyzedUserQuery

async def analyze_user_query(
    query: queries.AnalyzeUserQuery,
    llm: ollama.AbstractLLMClient,
    redis_task_manager: taskiq_redis_manager.AbstractRedisTaskManager 
)->AnalyzedUserQuery:
    themes = await llm.get_themes_by_query(
        query.raw_text,
        query.model
    )

    language_code = await redis_task_manager.run_task_by_name("definition_language_problem",
        kwargs={
            "event_id": str(query.event_id), 
            "text" : query.raw_text
        }
    )
    country_code = await redis_task_manager.run_task_by_name("definition_region_by_ip",
        kwargs={
            "event_id": str(query.event_id), 
            "ip_address" : str(query.ip_address)
        }
    )
    
    return AnalyzedUserQuery(
        event_id=query.event_id,
        text=query.raw_text,
        date=query.timestamp,
        themes=themes,
        language_code=language_code,
        country_code=country_code,
        user_ip=query.ip_address,
        model_llm=query.model
    ) 

async def get_region_by_ip(
    query: queries.DefineRegionByIp,
    ip_geolocation: http_ip_geolocation.AbstractIpGeolocation
)->Optional[str]:
    country_code = await ip_geolocation.get_country(query.ip_address)
    return country_code

async def get_language_text(
    query: queries.DefineLanguage,
    language_detect: language_detect.AbstractFtlangDetect,
)->str:
    language_code = await language_detect.definition_language(query.text)
    return language_code

QUERY_HANDLERS: Dict[Type[queries.Query], Callable] = {
    queries.AnalyzeUserQuery: analyze_user_query,
    queries.DefineRegionByIp: get_region_by_ip,
    queries.DefineLanguage: get_language_text,
}

