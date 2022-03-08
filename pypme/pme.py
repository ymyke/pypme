"""
"""

from typing import List, Tuple
import pandas as pd
import numpy_financial as npf

# FIXME First w/o timestamps and therefore w/ normal IRR, later to be extended to work
# w/ timestamps and XIRR.

# FIXME Add variant where pme_prices are retrieved on the fly via callback.

# FIXME Should there be one function for IRR (w/o timestamps) and one for XIRR (w/
# timestamps)?


def calc_pme(
    cashflows: List[float],
    prices: List[float],
    pme_prices: List[float],
) -> Tuple[float, pd.DataFrame]:
    """
    - `cashflows` are from a transaction account perspective.
    - `prices` and `pme_prices` need an additional item at the end representing the
      price at the reference date, for which the PME is calculated.
    - Obviously, all prices must be in the same currency.

    Returns a tuple with:
    - PME
    - dataframe containing all the cashflows, prices, and values used to derive the PME
    """
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
            ratio = cf / current_asset_pre  # FIXME div by 0
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
            asset_price,
            current_asset_pre,
            -current_asset_pre,
            0,
            pme_price,
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
    return (npf.irr(df["PME", "CF"]), df)
    # FIXME should this also return the IRR for complete_cashflows?
