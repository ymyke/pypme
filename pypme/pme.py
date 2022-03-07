"""
"""

from typing import List
import numpy_financial as npf

DEBUGMODE = True

# FIXME First w/o timestamps and therefore w/ normal IRR, later to be extended to work
# w/ timestamps and XIRR.

# FIXME Add variant where pme_prices are retrieved on the fly via callback.

# FIXME Add a debug mode? Build a dataframe out of the debug data?

# FIXME Should there be one function for IRR (w/o timestamps) and one for XIRR (w/
# timestamps)?


def calc_pme(
    cashflows: List[float],
    prices: List[float],
    pme_prices: List[float],
) -> float:
    """
    - Cashflow semantics: A cashflow < 0 signifies a buy (investment) of the respective
      asset, a cashflow > 0 a sell (divestment).
    - `prices` and `pme_prices` need on additional item at the end representing the
      price at the reference date, for which the PME is calculated.
    - Obviously, all prices must be in the same currency.
    """
    if len(prices) != len(pme_prices) or len(cashflows) != len(prices) - 1:
        raise ValueError("Inconsistent input data")

    current_pre = 0  # The current NAV of the original asset
    current_pme_pre = 0  # The current NAV of the PME asset
    pme_cashflows = []
    for cf, price, price_next, pme_price, pme_price_next in zip(
        cashflows, prices[:-1], prices[1:], pme_prices[:-1], pme_prices[1:]
    ):
        if cf < 0:
            # Simply buy from the PME whatever the original cashflow is:
            pme_cf = cf
        else:
            # Calculate the cashflow's ratio of the original asset's NAV at this point
            # in time and sell that ratio of the PME:
            ratio = cf / current_pre  # FIXME div by 0
            pme_cf = current_pme_pre * ratio

        pme_cashflows.append(pme_cf)

        if DEBUGMODE:
            print(
                f"{current_pre:8.2f} {cf:8.2f} {current_pre + cf:8.2f}  |  "
                f"{current_pme_pre:8.2f} {pme_cf:8.2f} {current_pme_pre + pme_cf:8.2f}"
            )

        # Calculate next:
        current_pre = (current_pre + cf) * price_next / price
        current_pme_pre = (current_pme_pre + pme_cf) * pme_price_next / pme_price

    # complete_cashflows = cashflows + [-current_pre]
    pme_cashflows.append(-current_pme_pre)
    print(f"PME Cashflows: {pme_cashflows}")

    return npf.irr(pme_cashflows)
    # FIXME should this also return the IRR for complete_cashflows?
