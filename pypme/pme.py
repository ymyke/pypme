from typing import List
import numpy_financial as npf


# FIXME First w/o timestamps and therefore w/ normal IRR, later to be extended to work
# w/ timestamps and XIRR.

# FIXME Add variant where pme_prices are retrieved on the fly via callback.


def calc_pme(
    cashflows: List[float],
    prices: List[float],
    pme_prices: List[float],
) -> float:
    """

    - `prices` and `pme_prices` need on additional item at the end representing the price at the reference date, for which the PME is calculated.
    - Obviously, all prices must be in the same currency.
    """
    current_pre = current_pme_pre = 0
    pme_cashflows = []
    for cf, price, price_next, pme_price, pme_price_next in zip(
        cashflows, prices[:-1], prices[1:], pme_prices[:-1], pme_prices[1:]
    ):
        if cf < 0:
            pme_cashflows.append(cf)
            # Calculate next:
            current_pme_pre = (current_pme_pre + cf) * pme_price_next / pme_price
        else:
            ratio = cf / current_pre  # FIXME div by 0
            pme_cf = current_pme_pre * ratio
            pme_cashflows.append(pme_cf)
            # Calculate next:
            current_pme_pre = (current_pme_pre + pme_cf) * pme_price_next / pme_price
        # Calculate next:
        current_pre = (current_pre + cf) * price_next / price

    # complete_cashflows = cashflows + [-current_pre]
    pme_cashflows.append(-current_pme_pre)

    # print(complete_cashflows)
    # print(pme_cashflows)

    return npf.irr(pme_cashflows)
    # FIXME should this also return the IRR for complete_cashflows?
