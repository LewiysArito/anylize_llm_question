import pytest
from analyze_user_query.clickhouse_helper import FixedString

@pytest.mark.parametrize("length,expected_str", [
	(8, "FixedString(8)"),
	(16, "FixedString(16)"),
	(32, "FixedString(32)"),
	(64, "FixedString(64)"),
	(128, "FixedString(128)")
])
def test_fixed_string_valid(length, expected_str):
	fixed_string = FixedString(length)
	assert fixed_string.length == length
	assert str(fixed_string) == expected_str

@pytest.mark.parametrize("length", [
	(257)
])
def test_fixed_string_invalid_length(length):
	with pytest.raises(ValueError, match="Max byte equal"):
		FixedString(length)
