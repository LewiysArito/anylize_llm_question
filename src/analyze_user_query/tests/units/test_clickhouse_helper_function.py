import pytest
from analyze_user_query.clickhouse_helper import Function

@pytest.mark.parametrize("value,function_name,arguments,string", [
    ("AVG(count)", "AVG", ["count"], "AVG(count)"),
    ("AVG(count*price)", "AVG", ["count", "price"], "AVG(count*price)"),
    ("today()", "today", [], "today()"),
    ("AVG( count * price )", "AVG", ["count", "price"], "AVG( count * price )"),
])
def test_function_valid(value, function_name, arguments, string):
    function = Function(value)
    assert str(function) == string
    assert function.function_name == function_name
    assert function.arguments == arguments

@pytest.mark.parametrize("value", [
    ("(abv, acd)"),
    ("()"),
    (None)
])
def test_function_is_not_valid(value):
    with pytest.raises(ValueError, match=f"Invalid function format"):
        function = Function(value)


