import pytest
from datetime import date
from hypothesis import given, strategies as st, settings, Verbosity
import pandas as pd
from xirr.math import xnpv
from pypme import verbose_pme, pme, verbose_xpme, xpme


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
    """`verbose_pme` works with all kinds of input parameters."""
    pme_irr, asset_irr, df = verbose_pme(cashflows, prices, pme_prices)
    assert round(pme_irr * 100.0, 2) == round(target_pme_irr, 2)
    assert round(asset_irr * 100.0, 2) == round(target_asset_irr, 2)
    assert isinstance(df, pd.DataFrame)


def test_pme():
    """`pme` properly passes args and returns to and back from `verbose_pme`."""
    assert pme([-10, 5], [1, 2, 1], [1, 1, 0.5]) == -0.25


@pytest.mark.parametrize(
    "dates, cashflows, prices, pme_prices, target_pme_irr, target_asset_irr",
    [
        (
            [date(2019, 12, 31), date(2020, 3, 12)],
            [-80005.8],
            [80005.8, 65209.6],
            [1, 1],
            0,
            -64.54,
        ),
        (
            [date(2015, 1, 1), date(2015, 6, 12), date(2016, 2, 15)],
            [-10000, 7500],
            [100, 120, 100],
            [100, 150, 100],
            55.26,
            19.50,
        ),
        ([date(1, 1, 1), date(1, 1, 2)], [-1], [1, 1], [1, 1], 0, 0),
        ([date(1, 1, 1), date(2, 1, 1)], [-1], [1, 1.1], [1, 0.9], -10, 10),
        ([date(1, 1, 1), date(3, 1, 1)], [-1], [1, 1.1], [1, 0.9], -5.13, 4.88),
        ([date(1, 1, 1), date(11, 1, 1)], [-1], [1, 1.1], [1, 0.9], -1.05, 0.96),
    ],
)
def test_verbose_xpme(
    dates, cashflows, prices, pme_prices, target_pme_irr, target_asset_irr
):
    """`verbose_xpme` works with all kinds of input parameters."""
    pme_irr, asset_irr, df = verbose_xpme(dates, cashflows, prices, pme_prices)
    assert round(pme_irr * 100.0, 2) == round(target_pme_irr, 2)
    assert round(asset_irr * 100.0, 2) == round(target_asset_irr, 2)
    assert isinstance(df, pd.DataFrame)


def test_xpme():
    """`xpme` properly passes args and returns to and back from `verbose_xpme`."""
    assert xpme([date(1, 1, 1), date(1, 1, 2)], [-1], [1, 1], [1, 1]) == 0


@pytest.mark.parametrize(
    "list1, list2, list3, exc_pattern",
    [
        ([], [], [], "Must have at least one cashflow"),
        ([1], [], [], "The first cashflow must be negative"),
        ([-1], [0], [], "All prices must be > 0"),
        ([-1], [], [], "Inconsistent input data"),
    ],
)
def test_for_valueerrors(list1, list2, list3, exc_pattern):
    with pytest.raises(ValueError) as exc:
        pme(list1, list2, list3)
    assert exc_pattern in str(exc)


def test_for_non_sorted_dates():
    with pytest.raises(ValueError) as exc:
        xpme([date(2000, 1, 1), date(1900, 1, 1)], [], [], [])
    assert "Dates must be in order" in str(exc)


@st.composite
def same_len_lists(draw):
    n = draw(st.integers(min_value=2, max_value=100))
    floatlist = st.lists(st.floats(), min_size=n, max_size=n)
    datelist = st.lists(st.dates(), min_size=n, max_size=n)
    return (sorted(draw(datelist)), draw(floatlist), draw(floatlist), draw(floatlist))


@given(same_len_lists())
# @settings(verbosity=Verbosity.verbose)
def test_xpme_hypothesis_driven(lists):
    try:
        pme_irr, asset_irr, df = verbose_xpme(
            lists[0], lists[1][:-1], lists[2], lists[3]
        )
    except ValueError as exc:
        assert "The first cashflow" in str(exc) or "All prices" in str(exc)
    except OverflowError as exc:
        assert "Result too large" in str(exc)
    else:
        assert xnpv(df["PME", "CF"], pme_irr) == 0
        assert xnpv(df["Asset", "CF"], asset_irr) == 0
