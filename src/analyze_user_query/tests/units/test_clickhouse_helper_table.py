import pytest
from analyze_user_query.clickhouse_helper import (Array, Column, DateTime, FixedString, IPv4, Integer, String, Date, EngineType, Table, Function)


@pytest.mark.parametrize("table_name,engine,order_by,partition_by,primary_key,columns,expected_sql_parts", [
    (
        "analize_user_llm_query",
        EngineType.MERGETREE,  
        ["date", "country_code", "language_code", "model_llm"],
        Function("toYYYYMM(date)"),
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
        Function("toYYYYMM(event_date)"),
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
    assert table.partition_by == partition_by
    assert table.primary_key ==  primary_key
    
    assert str(table) == expected_sql_parts

def test_empty_table_name():
    with pytest.raises(ValueError, match="Table name cannot be empty"):
        table = Table(
            "",
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

@pytest.mark.parametrize("engine", [
    (str), (Array), (Integer)
])
def test_none_engine_type_value(engine):
    with pytest.raises(TypeError, match="Engine must be instance of EngineType"):
        table = Table(
            "analize_user_llm_query",
            engine, 
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

@pytest.mark.parametrize("columns", [
    (
        str("123"), 
        Array(String())
    ), 
    (
        FixedString(23),
        Integer(32)
    )
])
def test_not_provide_column_value(columns):
    with pytest.raises(ValueError, match="At least one Column must be provided"):
        table = Table(
            "analize_user_llm_query",
            EngineType.MERGETREE, 
            ["date", "country_code", "language_code", "model_llm"],
            "toYYYYMM(date)",
            None,
            *columns
        )

@pytest.mark.parametrize("primary_key", [
    ("test"), 
    (["data", "table"]),
])
def test_primary_key_not_found_between_column(primary_key):
    with pytest.raises(ValueError, match="not found in table columns"):
        table = Table(
            "analize_user_llm_query",
            EngineType.MERGETREE, 
            ["date", "country_code", "language_code", "model_llm"],
            Function("toYYYYMM(data)"),
            primary_key,
            Column("text", String(), False),
            Column("date", Date(), False),
            Column("themes", Array(FixedString(128)), False),
            Column("language_code", FixedString(3), False),
            Column("country_code", FixedString(3), True, "NULL"),
            Column("user_ip", IPv4(), True, "NULL"),
            Column("model_llm", String(), False)
        )

@pytest.mark.parametrize("primary_key", [
    ("country_code"), 
    (["date", "user_ip"])
])
def test_primary_key_for_not_null_column(primary_key):
    with pytest.raises(ValueError, match="cannot be nullable"):
        table = Table(
            "analize_user_llm_query",
            EngineType.MERGETREE, 
            ["date", "country_code", "language_code", "model_llm"],
            Function("toYYYYMM(date)"),
            primary_key,
            Column("text", String(), False),
            Column("date", Date(), False),
            Column("themes", Array(FixedString(128)), False),
            Column("language_code", FixedString(3), False),
            Column("country_code", FixedString(3), True, "NULL"),
            Column("user_ip", IPv4(), True, "NULL"),
            Column("model_llm", String(), False)
        )

@pytest.mark.parametrize("partition_by", [
    (Function("toYYYYMM(data)")), 
    ("month"),
])
def test_partition_by_not_found_between_column(partition_by):
    with pytest.raises(ValueError, match="cannot be used"):
        table = Table(
            "analize_user_llm_query",
            EngineType.MERGETREE, 
            ["date", "country_code", "language_code", "model_llm"],
            partition_by,
            None,
            Column("text", String(), False),
            Column("date", Date(), False),
            Column("themes", Array(FixedString(128)), False),
            Column("language_code", FixedString(3), False),
            Column("country_code", FixedString(3), True, "NULL"),
            Column("user_ip", IPv4(), True, "NULL"),
            Column("model_llm", String(), False)
        )

@pytest.mark.parametrize("order_by", [
    ("data"), 
    (["date", "country_code", "language"]),
])
def test_order_by_not_found_between_column(order_by):
    with pytest.raises(ValueError, match="not found in table columns"):
        table = Table(
            "analize_user_llm_query",
            EngineType.MERGETREE, 
            order_by,
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
@pytest.mark.parametrize("order_by,primary_key", [
    ("date", ["date", "language_code"]),
    (["date", "language_code"], ["date", "language_code", "model_llm"]),
]) 
def test_len_order_by_column_less_then_primary_column(order_by, primary_key):
    with pytest.raises(ValueError, match="must be less or equal ORDER BY length"):
        table = Table(
            "analize_user_llm_query",
            EngineType.MERGETREE, 
            order_by,
            Function("toYYYYMM(date)"),
            primary_key,
            Column("text", String(), False),
            Column("date", Date(), False),
            Column("themes", Array(FixedString(128)), False),
            Column("language_code", FixedString(3), False),
            Column("country_code", FixedString(3), True, "NULL"),
            Column("user_ip", IPv4(), True, "NULL"),
            Column("model_llm", String(), False)
        )

@pytest.mark.parametrize("name,type,nullable", [
    ("text", String(), False),
    ("date", Date(), False),
]) 
def test_add_existing_column(name, type, nullable):
    table = Table(
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
    with pytest.raises(ValueError, match="already exists"):
        table.add_column(Column(name, type, nullable))

@pytest.mark.parametrize("table_obj,sql_string", [
    (
        Table(
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
        ),
        """
        CREATE TABLE analize_user_llm_query
        (
            text String NOT NULL,
            date Date NOT NULL,
            themes Array(FixedString(128)) NOT NULL,
            language_code FixedString(3) NOT NULL,
            country_code FixedString(3) NULL DEFAULT NULL,
            user_ip IPv4 NULL DEFAULT NULL,
            model_llm String NOT NULL
        )
        ENGINE = MergeTree
        PARTITION BY toYYYYMM(date)
        ORDER BY (date, country_code, language_code, model_llm)
        """
    )
]) 
def test_generate_sql_for_create(table_obj, sql_string): 
    generate_sql = table_obj.generate_sql_for_create().strip()
    sql_string = sql_string.strip()
    assert generate_sql.split() == sql_string.split()

@pytest.mark.parametrize("values,columns,sql_string", [
    (
        [("Hello world", "2025-10-20", ["theme1", "theme2"], "en", "US", "192.168.1.1", "gpt-4")],
        None,
        """
        INSERT INTO analize_user_llm_query (text, date, themes, language_code, country_code, user_ip, model_llm) 
        VALUES 
            ('Hello world', '2025-10-20', ['theme1', 'theme2'], 'en', 'US', '192.168.1.1', 'gpt-4')
        """
    ),
    (
        [("Сколько нужно учить геометрию, чтобы ее хорошо понимать", "2025-10-22", ["geometry", "education", "duration"], "ru", "RU", "192.168.10.23", "gemeni-3.1"),
        ("How many people like ice cream?", "2025-10-20", ["ice cream", "people"], "en", "FR", "192.168.1.10", "gemeni-3.1")],
        None,
        """
        INSERT INTO analize_user_llm_query (text, date, themes, language_code, country_code, user_ip, model_llm) 
        VALUES 
            ('Сколько нужно учить геометрию, чтобы ее хорошо понимать', '2025-10-22', ['geometry', 'education', 'duration'], 'ru', 'RU', '192.168.10.23', 'gemeni-3.1'),
            ('How many people like ice cream?', '2025-10-20', ['ice cream', 'people'], 'en', 'FR', '192.168.1.10', 'gemeni-3.1')
        """
    ),
    (
        [("Hello", "2025-10-20", "en", "gpt-4")],
        ["text", "date", "language_code", "model_llm"],
        """
        INSERT INTO analize_user_llm_query (text, date, language_code, model_llm)
            VALUES
            ('Hello', '2025-10-20', 'en', 'gpt-4')
        """
    ),
    (
        [("Сколько дней в 2025 году?", "2025-10-20", ["theme"], "ru", None, None, "model")],
        None,
        """
        INSERT INTO analize_user_llm_query (text, date, themes, language_code, country_code, user_ip, model_llm) 
            VALUES
            ('Сколько дней в 2025 году?', '2025-10-20', ['theme'], 'ru', NULL, NULL, 'model')
        """
    ),
    (
        [("Text", "2025-10-22", [], "eng", "FR", "192.168.1.20", "model")],
        None,
        """
        INSERT INTO analize_user_llm_query (text, date, themes, language_code, country_code, user_ip, model_llm) 
            VALUES 
            ('Text', '2025-10-22', [], 'eng', 'FR', '192.168.1.20', 'model')
        """
    ),
    (
        [("O''Reilly", "2025-10-20", ["test"], "en", "US", "192.168.1.1", "gpt-4")],
        None,
        """
        INSERT INTO analize_user_llm_query (text, date, themes, language_code, country_code, user_ip, model_llm) 
            VALUES 
            ("O''Reilly", '2025-10-20', ['test'], 'en', 'US', '192.168.1.1', 'gpt-4')
        """
    ),
])
def test_generate_sql_for_insert(values, columns, sql_string): 
    table = Table(
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
    generate_sql = table.generate_sql_for_insert(values, columns).strip()
    sql_string = sql_string.strip()
    
    generate_sql_normalized = ' '.join(generate_sql.split())
    sql_string_normalized = ' '.join(sql_string.split())

    assert generate_sql_normalized == sql_string_normalized

@pytest.mark.parametrize("values,columns", [
    (
        [("Hello world", "2025-10-20", ["theme1", "theme2"], "en", "US", "192.168.1.1", "gpt-4")],
        ["text", "date", "language_code", "model"],
    )
])
def test_generate_sql_for_insert_column_not_found_in_table(values,columns):
    table = Table(
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

    with pytest.raises(ValueError, match="Column 'model' not found in table"):
        table.generate_sql_for_insert(values, columns)

@pytest.mark.parametrize("values,columns", [
    (
        [("Hello world", "2025-10-20", ["theme1", "theme2"], "en", "US", "192.168.1.1", "gpt-4")],
        ["text", "date", "language_code", "model_llm"],
    )
])
def test_generate_sql_for_insert_invalid_columns_count(values,columns):
    table = Table(
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

    with pytest.raises(ValueError, match="Each row of values must match the number of specified columns"):
        table.generate_sql_for_insert(values, columns)

@pytest.mark.parametrize("columns,where,group_by,having,order_by,limit,sql_string", [
    (None, None, None, None, None, None, "SELECT * FROM analize_user_llm_query"),
    (["text", "language_code", "country_code"], None, None, None, None, None, "SELECT text, language_code, country_code FROM analize_user_llm_query"),
    (None, [("date", "=", Function("today()"))], None, None, None, None, "SELECT * FROM analize_user_llm_query WHERE date = today()")
])
def test_generate_sql_for_select(columns, where, group_by, having, order_by, limit, sql_string): 
    table = Table(
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
    generate_sql = table.generate_sql_for_select(columns,where,group_by, having,order_by,limit).strip()
    sql_string = sql_string.strip()
    
    generate_sql_normalized = ' '.join(generate_sql.split())
    sql_string_normalized = ' '.join(sql_string.split())

    assert generate_sql_normalized == sql_string_normalized