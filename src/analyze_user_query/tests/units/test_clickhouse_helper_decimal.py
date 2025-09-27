import pytest
from analyze_user_query.clickhouse_helper import Decimal

@pytest.mark.parametrize("bit,p,s,expected_str", [
	(32, None, 2, "Decimal32(2)"),
    (64, None, 4, "Decimal64(4)"),
    (128, None, 6, "Decimal128(6)"),
    (256, None, 8, "Decimal256(8)"),
    
    (None, 9, 2, "Decimal(9, 2)"),
    (None, 18, 4, "Decimal(18, 4)"),
    (None, 38, 6, "Decimal(38, 6)"),
])
def test_decimal_valid(bit, p, s, expected_str):
	decimal = Decimal(bit, p, s)
	assert decimal.bit == bit
	assert decimal.p == p
	assert decimal.s == s
	assert str(decimal) == expected_str