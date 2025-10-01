import re
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

@pytest.mark.parametrize("bit,p,s", [
    (32, None, -1),
    (64, None, -10)
])
def test_decimal_positive_s_value(bit, p, s):
    with pytest.raises(ValueError, match="Value s must be positive"):
        Decimal(bit, p, s)

@pytest.mark.parametrize("bit,p,s", [
    (None, -10, 1),
    (None, -20, 50)
])
def test_decimal_positive_p_value(bit, p, s):
    with pytest.raises(ValueError, match="Value p must be positive"):
        Decimal(bit, p, s)

@pytest.mark.parametrize("bit,p,s", [
    (64, 10, 9),
    (128, 15, 13)
])
def test_decimal_without_p_when_use_bit(bit, p, s):
    pattern = re.escape("Cannot use p when used bit. Use either Decimal(p, s)")
    with pytest.raises(ValueError, match=pattern):
        Decimal(bit, p, s)

@pytest.mark.parametrize("bit,p,s", [
    (None, 9, None),
    (None, None, 10)
])
def test_decimal_require_s_and_p_when_bit_is_none(bit, p, s):
    pattern = re.escape("For Decimal(p, s) both precision (p) and scale (s) must be specified")
    with pytest.raises(ValueError, match=pattern):
        Decimal(bit, p, s)

@pytest.mark.parametrize("bit,p,s", [
    (63, None, 10),
    (126, None, 24)
])    
def test_decimal_valid_bits(bit, p, s):
    with pytest.raises(ValueError, match="Bit must be from the following list"):
        Decimal(bit, p, s)

@pytest.mark.parametrize("bit,p,s", [
    (32, None, 10),
    (64, None, 20),
    (128, None, 40),
    (256, None, 80),
]) 
def test_decimal_valid_s_value_for_certain_bit(bit, p, s):
    pattern = re.escape(f"For Decimal{bit} scale (s) max value must be")
    with pytest.raises(ValueError, match=pattern):
        Decimal(bit, p, s)

@pytest.mark.parametrize("bit,p,s", [
    (None, 79, 70),
]) 
def test_decimal_valid_max_p_when_bit_is_none(bit, p, s):
    pattern = re.escape("Precision (p) must be")
    with pytest.raises(ValueError, match=pattern):
        Decimal(bit, p, s)

@pytest.mark.parametrize("bit,p,s", [
    (None, 60, 61),
    (None, 30, 32),
]) 
def test_decimal_p_more_then_s(bit, p, s):
    pattern = re.escape("Scale (s) must be less or equal to precision (p)")
    with pytest.raises(ValueError, match=pattern):
        Decimal(bit, p, s)

