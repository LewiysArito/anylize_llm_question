from typing import Tuple
from analyze_user_query.domain import model
from src.analyze_user_query.clickhouse_helper import (
    Array, Column, Date, EngineType, FixedString, Function, IPv4, Mapper, String, Table, UUID  
)

analyze_user_llm_query = Table(
    "analyze_user_llm_query",
    EngineType.MERGETREE, 
    ["date", "country_code", "language_code", "model_llm"],
    Function("toYYYYMM(date)"),
    None,
    Column("event_id", UUID(), False),
    Column("text", String(), False),
    Column("date", Date(), False),
    Column("themes", Array(FixedString(128)), False),
    Column("language_code", FixedString(3), False),
    Column("country_code", FixedString(3), True, "NULL"),
    Column("user_ip", IPv4(), True, "NULL"),
    Column("model_llm", String(), False)
)

def start_mappers() -> Tuple[Mapper, ...]:
    analyze_user_llm_query_mapper = Mapper(model.AnalyzedUserQuery, analyze_user_llm_query)
    return (analyze_user_llm_query_mapper,)

analyze_user_llm_query_mapper,  = start_mappers()
