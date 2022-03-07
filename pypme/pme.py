"""
"""

from typing import List
import pandas as pd
import numpy_financial as npf

DEBUGMODE = True

# FIXME First w/o timestamps and therefore w/ normal IRR, later to be extended to work
# w/ timestamps and XIRR.

# FIXME Add variant where pme_prices are retrieved on the fly via callback.

# FIXME Add a debug mode? Build a dataframe out of the debug data? -- Or some kind of
# verbose mode that returns more information?

# FIXME Should there be one function for IRR (w/o timestamps) and one for XIRR (w/
# timestamps)?


def calc_pme(
    cashflows: List[float],
    prices: List[float],
    pme_prices: List[float],
) -> float:
    """
    - `cashflows` are from a transaction account perspective.
    - `prices` and `pme_prices` need an additional item at the end representing the
      price at the reference date, for which the PME is calculated.
    - Obviously, all prices must be in the same currency.
    """
    if len(prices) != len(pme_prices) or len(cashflows) != len(prices) - 1:
        raise ValueError("Inconsistent input data")

    current_asset_pre = 0  # The current NAV of the asset
    current_pme_pre = 0  # The current NAV of the PME
    df_rows = []  # To build the dataframe
    pme_cashflows = []
    for cf, price, price_next, pme_price, pme_price_next in zip(
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

        pme_cashflows.append(pme_cf)

        if DEBUGMODE:
            df_rows.append(
                [
                    cf,
                    price,
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
        current_asset_pre = (current_asset_pre + asset_cf) * price_next / price
        current_pme_pre = (current_pme_pre + pme_cf) * pme_price_next / pme_price

    # complete_cashflows = cashflows + [-current_asset_pre]
    pme_cashflows.append(-current_pme_pre)
    print(f"PME Cashflows: {pme_cashflows}")

    if DEBUGMODE:
        df_rows.append(
            [
                current_asset_pre,
                price,
                current_asset_pre,
                -current_asset_pre,
                0,
                pme_price,
                current_pme_pre,
                -current_pme_pre,
                0,
            ]
        )
        return npf.irr(pme_cashflows), pd.DataFrame(
            df_rows,
            columns=pd.MultiIndex.from_arrays(
                [
                    ["Account"] + ["Asset"] * 4 + ["PME"] * 4,
                    ["NAV"] + ["Price", "NAVpre", "CF", "NAVpost"] * 2,
                ]
            ),
        )
    else:
        return npf.irr(pme_cashflows)
    # FIXME should this also return the IRR for complete_cashflows?
