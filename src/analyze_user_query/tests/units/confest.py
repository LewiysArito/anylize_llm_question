import pytest
from analyze_user_query.clickhouse_helper import (
    Table, EngineType, Function, Column, String, Date, Array, FixedString, IPv4
)

@pytest.fixture(scope="module")
def sample_analize_user_llm_query_table():
    return Table(
        "analize_user_llm_query",
        EngineType.MERGETREE,
        ["date", "country_code", "language_code", "model_llm"],
        Function("toYYYYMM(date)"),
        None,
        Column("text", String(), False),
        Column("date", Date(), False),
        Column("themes", Array(FixedString(128)), False),
        Column("language_code", FixedString(3), False),
        Column("country_code", FixedString(3), True, "NULL"),
        Column("user_ip", IPv4(), True, "NULL"),
        Column("model_llm", String(), False)
    )