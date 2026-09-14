import math

from dd_engine.calculations import (
    applied_growth, bazin_ceiling, current_pe, dividend_yield,
    gordon_value, graham_value, projective_ceiling, projected_lpa, seal,
)


def test_graham():
    assert math.isclose(graham_value(2.0, 10.0), math.sqrt(450))


def test_bazin():
    assert math.isclose(bazin_ceiling(1.20, 0.06), 20.0)


def test_gordon():
    assert math.isclose(gordon_value(1.0, 0.05, 0.12), 15.0)
    assert gordon_value(1.0, 0.12, 0.12) is None


def test_projective():
    assert math.isclose(projected_lpa(2.0, 0.06, 5), 2.0 * 1.06**5)
    assert math.isclose(projective_ceiling(2.0, 0.07), 2.0 / 0.07)


def test_basic_ratios():
    assert math.isclose(current_pe(20, 2), 10)
    assert math.isclose(dividend_yield(1, 20), 0.05)


def test_growth_cap_and_seal():
    assert applied_growth(0.10, 0.06) == 0.06
    assert seal(70) == "VERDE"
    assert seal(50) == "AMARELO"
    assert seal(49.9) == "VERMELHO"
