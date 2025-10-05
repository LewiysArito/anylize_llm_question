import pytest
from analyze_user_query.clickhouse_helper import (Array, Column, DateTime, FixedString, IPv4, Integer, String, Date, EngineType, Table)

@pytest.mark.parametrize("table_name,engine,order_by,partition_by,primary_key,columns,expected_sql_parts", [
    (
        "analize_user_llm_query",
        EngineType.MERGETREE,  
        ["date", "country_code", "language_code", "model_llm"],
        "toYYYYMM(date)",
        None,
        [
            Column("text", String(), False),
            Column("date", Date(), False),
            Column("themes", Array(FixedString(128)), False),
            Column("language_code", FixedString(3), False),
            Column("country_code", FixedString(3), True, "NULL"),
            Column("user_ip", IPv4(), True, "NULL"),
            Column("model_llm", String(), False)
        ],
        "TABLE analize_user_llm_query"
    ),
    (
        "analize_user_action",
        EngineType.MERGETREE,
        ["event_date", "event_name", "country_code"],
        "toYYYYMM(event_date)",
        None,
        [
            Column("event_date", Date(), False),
            Column("event_time", DateTime(), False),
            Column("user_id", Integer(64, True), False),
            Column("event_name", String(), False),
            Column("country_code", FixedString(2), False),
        ],
        "TABLE analize_user_action"
    ),
])
def test_column_creation_and_string_value(table_name,engine,order_by,partition_by,primary_key,columns,expected_sql_parts):
    table = Table(
        table_name,
        engine,
        order_by,
        partition_by,
        primary_key,
        *columns
    )

    assert table.table_name == table_name
    assert table.engine == engine
    assert table.order_by == order_by
    assert table.partition_by ==  partition_by
    assert table.primary_key ==  primary_key
    
    assert str(table) == expected_sql_parts