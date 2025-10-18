import pytest
import pytest
from analyze_user_query.clickhouse_helper import Array, FixedString, Integer, UUID, String

@pytest.mark.parametrize("item_type, expected_str", [
    (Integer(16, False), "Array(Int16)"),
    (FixedString(10), "Array(FixedString(10))"),
    (UUID(), "Array(UUID)"),
    (String(), "Array(String)")
])
def test_array_valid(item_type, expected_str):
    arr = Array(item_type=item_type)
    assert isinstance(arr.item_type, type(item_type))
    assert str(arr) == expected_str

@pytest.mark.parametrize("nested, expected_str", [
    (Array(Integer(16, False)), "Array(Array(Int16))"),
    (Array(FixedString(10)), "Array(Array(FixedString(10)))"),
])
def test_array_nested(nested, expected_str):
    nested = Array(item_type=nested)
    assert str(nested) == expected_str