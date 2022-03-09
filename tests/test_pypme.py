import pytest
import pandas as pd
from pypme import __version__, verbose_pme


def test_version():
    assert __version__ == "0.1.0"


@pytest.mark.parametrize(
    "cashflows, prices, pme_prices, target_pme_irr, target_asset_irr",
    [
        (
            [-100, -50, 60, 100],
            [1.00000000, 1.15000000, 1.28939394, 1.18624242, 1.58165657],
            [100, 105, 115, 100, 120],
            2.02,
            7.77,
        ),
        ([-10, 5], [1, 2, 1], [1, 1, 0.5], -25, 15.14),
        ([-10, 1], [1, 1, 1], [1, 1, 1], 0, 0),
    ],
)
def test_verbose_pme(cashflows, prices, pme_prices, target_pme_irr, target_asset_irr):
    pme_irr, asset_irr, df = verbose_pme(
        cashflows=cashflows, prices=prices, pme_prices=pme_prices
    )
    assert round(pme_irr * 100.0, 2) == round(target_pme_irr, 2)
    assert round(asset_irr * 100.0, 2) == round(target_asset_irr, 2)
    assert isinstance(df, pd.DataFrame)
