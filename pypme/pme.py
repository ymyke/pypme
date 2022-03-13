"""Calculate PME (Public Market Equivalent) for both evenly and unevenly spaced
cashflows. Calculation according to
https://en.wikipedia.org/wiki/Public_Market_Equivalent#Modified_PME

Args:
- `dates`: The points in time. (Only for `xpme` variants.)
- `cashflows`: The cashflows from a transaction account perspective.
- `prices`: Asset's prices at each interval / point in time.
- `pme_prices`: PME's prices at each interval / point in time.

Note:
- Both `prices` and `pme_prices` need an additional item at the end for the last
  interval / point in time, for which the PME is calculated.
- `cashflows` has one fewer entry than the other lists because the last cashflow is
  implicitly assumed to be the current NAV at that time.

Verbose versions return a tuple with:
- PME IRR
- Asset IRR
- Dataframe containing all the cashflows, prices, and values used to derive the PME
"""

from typing import List, Tuple
from datetime import date
import pandas as pd
import numpy_financial as npf
from xirr.math import listsXirr


def verbose_pme(
    cashflows: List[float],
    prices: List[float],
    pme_prices: List[float],
) -> Tuple[float, float, pd.DataFrame]:
    """Calculate PME for evenly spaced cashflows and return vebose information."""
    if len(cashflows) == 0:
        raise ValueError("Must have at least one cashflow")
    if not any(x < 0 for x in cashflows):
        raise ValueError(
            "At least one cashflow must be negative, i.e., a buy of some of the asset"
        )
    if not all(x > 0 for x in prices + pme_prices):
        raise ValueError("All prices must be > 0")
    if len(prices) != len(pme_prices) or len(cashflows) != len(prices) - 1:
        raise ValueError("Inconsistent input data")

    current_asset_pre = 0  # The current NAV of the asset
    current_pme_pre = 0  # The current NAV of the PME
    df_rows = []  # To build the dataframe
    for cf, asset_price, asset_price_next, pme_price, pme_price_next in zip(
        cashflows, prices[:-1], prices[1:], pme_prices[:-1], pme_prices[1:]
    ):
        if cf < 0:
            # Simply buy from the asset and the PME the cashflow amount:
            asset_cf = pme_cf = -cf
        else:
            # Calculate the cashflow's ratio of the asset's NAV at this point in time
            # and sell that ratio of the PME:
            asset_cf = -cf
            ratio = cf / current_asset_pre
            pme_cf = -current_pme_pre * ratio

        df_rows.append(
            [
                cf,
                asset_price,
                current_asset_pre,
                asset_cf,
                current_asset_pre + asset_cf,
                pme_price,
                current_pme_pre,
                pme_cf,
                current_pme_pre + pme_cf,
            ]
        )

        # Calculate next:
        current_asset_pre = (
            (current_asset_pre + asset_cf) * asset_price_next / asset_price
        )
        current_pme_pre = (current_pme_pre + pme_cf) * pme_price_next / pme_price

    df_rows.append(
        [
            current_asset_pre,
            asset_price_next,
            current_asset_pre,
            -current_asset_pre,
            0,
            pme_price_next,
            current_pme_pre,
            -current_pme_pre,
            0,
        ]
    )
    df = pd.DataFrame(
        df_rows,
        columns=pd.MultiIndex.from_arrays(
            [
                ["Account"] + ["Asset"] * 4 + ["PME"] * 4,
                ["CF"] + ["Price", "NAVpre", "CF", "NAVpost"] * 2,
            ]
        ),
    )
    return (npf.irr(df["PME", "CF"]), npf.irr(df["Asset", "CF"]), df)


def pme(
    cashflows: List[float],
    prices: List[float],
    pme_prices: List[float],
) -> float:
    """Calculate PME for evenly spaced cashflows and return the PME IRR only."""
    return verbose_pme(cashflows, prices, pme_prices)[0]


def verbose_xpme(
    dates: List[date],
    cashflows: List[float],
    prices: List[float],
    pme_prices: List[float],
) -> Tuple[float, float, pd.DataFrame]:
    """Calculate PME for unevenly spaced / scheduled cashflows and return vebose
    information.

    Requires the points in time as `dates` as an input parameter in addition to the ones
    required by `pme()`.
    """
    if len(dates) != len(prices):
        raise ValueError("Inconsistent input data")
    df = verbose_pme(cashflows, prices, pme_prices)[2]
    df["Dates"] = dates
    df.set_index("Dates", inplace=True)
    return listsXirr(dates, df["PME", "CF"]), listsXirr(dates, df["Asset", "CF"]), df


def xpme(
    dates: List[date],
    cashflows: List[float],
    prices: List[float],
    pme_prices: List[float],
) -> float:
    """Calculate PME for unevenly spaced / scheduled cashflows and return the PME IRR
    only.
    """
    return verbose_xpme(dates, cashflows, prices, pme_prices)[0]
