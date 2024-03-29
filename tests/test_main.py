import pytest as pytest

from main import is_variation_okay


@pytest.mark.parametrize('expected_input,user_input,expected', [
    ('Lxe2 Dxe2 Dxd4+ De3 Dxa1', 'Lxe2 Dxe2 Dxd4+ Kh1 Dxa1', True),
    ('De6+ Kh7 Dxe7', 'De6+ Kh8 Dxe7', True),
    ('Lxf3 17. Sxf3 Dxf3', 'Lxf3 Lxf6 Txg2+ Kh1 Tg1+ Kxg1 Tg8+ Lg5 Txg5#', False)
])
def test_is_variation_okay__scenario__result(expected_input, user_input, expected):
    # given
    # fixtures

    # when
    actual = is_variation_okay(expected_input, user_input)
    
    # then
    assert actual == expected