import pytest
from analyze_user_query.clickhouse_helper import Column, Decimal, Date32, Integer, FixedString, Boolean

@pytest.mark.parametrize("name,type,nullable,default,expected_str", [
    ("money", Decimal(None, 10, 9), False, None, "money Decimal(10, 9) NOT NULL"),
    ("money", Decimal(32, None, 2), False, 0, "money Decimal32(2) NOT NULL DEFAULT 0"),

    ("date", Date32(), True, None, "date Date32 NULL"),
    ("date", Date32(), False, "today()", "date Date32 NOT NULL DEFAULT today()"), 
    
    ("number", Integer(32), False, 10, "number Int32 NOT NULL DEFAULT 10"),
    ("number", Integer(64), False, None, "number Int64 NOT NULL"),

    ("ip_address", FixedString(16), True, "127.0.0.1", "ip_address FixedString(16) NULL DEFAULT '127.0.0.1'"),
    ("ip_address", FixedString(16), False, "localhost", "ip_address FixedString(16) NOT NULL DEFAULT 'localhost'"),  

    ("is_active", Boolean(), True, True, "is_active Bool NULL DEFAULT True"),
    ("is_deleted", Boolean(), False, False, "is_deleted Bool NOT NULL DEFAULT False"),    
])
def test_column_creation_and_string_value(name, type, nullable, default, expected_str):
    column = Column(
        name=name,
        type=type,
        nullable=nullable,
        default=default
    )

    assert column.name == name
    assert column.type == type
    assert column.nullable == nullable
    assert column.default == default
    
    assert str(column) == expected_str

@pytest.mark.parametrize("name,type", [
    (" ", Boolean()),
    ("", Boolean()),
])
def test_column_raises_error_for_empty_name(name, type):
    with pytest.raises(ValueError, match="Name is cannot be empty"):
        Column(name, type)

@pytest.mark.parametrize("name,invalid_type", [
    ("array", str("faf")),
    ("is_active", bool("")),
])
def test_column_raises_error_for_invalid_type(name, invalid_type):
    with pytest.raises(ValueError, match="Type must be instance of ColumnType"):
        Column(name, invalid_type)