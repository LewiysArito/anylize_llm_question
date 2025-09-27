import pytest
from analyze_user_query.clickhouse_helper import Integer

@pytest.mark.parametrize("bit,unsigned,expected_str", [
	(8, False, "Int8"),
	(16, False, "Int16"),
	(32, False, "Int32"),
	(64, False, "Int64"),
	(128, False, "Int128"),
	(256, False, "Int256"),
	(8, True, "UInt8"),
	(16, True, "UInt16"),
	(32, True, "UInt32"),
	(64, True, "UInt64"),
])
def test_integer_valid(bit, unsigned, expected_str):
	integer = Integer(bit, unsigned)
	assert integer.bit == bit
	assert integer.unsigned == unsigned
	assert str(integer) == expected_str

@pytest.mark.parametrize("bit", [7, 12, 100, 300])
def test_integer_invalid_bit(bit):
	with pytest.raises(ValueError, match="Integer bit value must be from the following list"):
		Integer(bit)

@pytest.mark.parametrize("bit", [128, 256])
def test_integer_invalid_unsigned(bit):
	with pytest.raises(ValueError, match="Unsigned integer bit value must be from the following list"):
		Integer(bit, unsigned=True)