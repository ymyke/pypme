import pytest
from pypme import __version__, calc_pme


def test_version():
    assert __version__ == "0.1.0"


# FIXME Add many more test data sets.


@pytest.mark.parametrize(
    "cashflows, prices, pme_prices, target_pme_irr",
    [
        (
            [-100, -50, 60, 100],
            [1.00000000, 1.15000000, 1.28939394, 1.18624242, 1.58165657],
            [100, 105, 115, 100, 120],
            2.02,
        ),
        ([-10, 5], [1, 2, 1], [1, 1, 0.5], -25),
    ],
)
def test_calc_pme(cashflows, prices, pme_prices, target_pme_irr):
    pme_irr = calc_pme(cashflows=cashflows, prices=prices, pme_prices=pme_prices)
    assert round(pme_irr * 100.0, 2) == round(target_pme_irr, 2)
