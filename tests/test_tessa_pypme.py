import pytest
from datetime import datetime, timezone, date
import pandas as pd
from tessa.price import PriceHistory
from pypme.mod_tessa_pme import tessa_xpme, tessa_verbose_xpme


@pytest.mark.parametrize(
    "dates, cashflows, prices, pme_timestamps, pme_prices, target_pme_irr, target_asset_irr",
    [
        (
            [date(2012, 1, 1), date(2013, 1, 1)],
            [-100],
            [1, 1],
            ["2012-01-01"],
            [20],
            0,
            # B/c the function will search for the nearest date which is always the same
            # one b/c there is only one and therefore produce a PME IRR of 0
            0,
        ),
        (
            [date(2012, 1, 1), date(2013, 1, 1)],
            [-100],
            [1, 1],
            ["2012-01-01", "2012-01-02"],
            [20, 40],
            99.62,
            # In this case, the "nearest" option in `tessa_verbose_pme`'s call to
            # `get_indexer` finds the entry at 2012-01-02. Even though it's far away
            # from 2013-01-01, it's still the closest.
            0,
        ),
    ],
)
def test_tessa_xpme(
    mocker,
    dates,
    cashflows,
    prices,
    pme_timestamps,
    pme_prices,
    target_pme_irr,
    target_asset_irr,
):
    """Test both the verbose and non-verbose variant in one go to keep things simple.

    Note that this test does _not_ hit the network since the relevant function gets
    mocked.
    """
    mocker.patch(
        "tessa.price_history",
        return_value=PriceHistory(
            pd.DataFrame(
                {
                    "close": {
                        pd.Timestamp(x): y for x, y in zip(pme_timestamps, pme_prices)
                    }
                }
            ),
            "USD",
        ),
    )
    pme_irr, asset_irr, df = tessa_verbose_xpme(
        dates=dates,
        cashflows=cashflows,
        prices=prices,
        pme_ticker="dummy",
    )
    assert round(pme_irr * 100.0, 2) == round(target_pme_irr, 2)
    assert round(asset_irr * 100.0, 2) == round(target_asset_irr, 2)
    assert isinstance(df, pd.DataFrame)

    pme_irr = tessa_xpme(
        dates=dates,
        cashflows=cashflows,
        prices=prices,
        pme_ticker="dummy",
    )
    assert round(pme_irr * 100.0, 2) == round(target_pme_irr, 2)


def test_tessa_xpme_networked():
    """Test `tessa_xpme` with an actual network/API call."""
    pme_irr, asset_irr, df = tessa_verbose_xpme(
        dates=[
            datetime(2012, 1, 1, tzinfo=timezone.utc),
            datetime(2013, 1, 1, tzinfo=timezone.utc),
        ],
        cashflows=[-100],
        prices=[1, 1.1],
        pme_ticker="MSFT",
    )
    assert round(pme_irr * 100.0, 2) == 5.78
    assert round(asset_irr * 100.0, 2) == 9.97
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 9)
