"""Calculate PME and get the prices via tessa library (https://github.com/ymyke/tessa).

Args: 

- `pme_ticker`: The ticker symbol/name.
- `pme_source`: The source to look up the ticker from, e.g., "yahoo" or "coingecko".

For both arguments, refer to the tessa library for details.

Refer to the `pme` module to understand other arguments and what the functions return.
"""

from typing import List, Tuple
from datetime import date
import pandas as pd
import tessa
from .pme import verbose_xpme


def pick_prices_from_dataframe(
    dates: List[date], pricedf: pd.DataFrame, which_column: str
) -> List[float]:
    """Return the prices from `pricedf` that are nearest to dates `dates`. Use
    `which_column` to pick the dataframe column.
    """
    return list(
        pricedf.iloc[pricedf.index.get_indexer([x], method="nearest")[0]][which_column]
        for x in dates
    )


def tessa_verbose_xpme(
    dates: List[date],
    cashflows: List[float],
    prices: List[float],
    pme_ticker: str,
    pme_source: tessa.SourceType = "yahoo",
) -> Tuple[float, float, pd.DataFrame]:
    """Calculate PME return vebose information, retrieving PME price information via
    tessa library in real time.
    """
    pmedf = tessa.price_history(pme_ticker, pme_source).df
    return verbose_xpme(
        dates, cashflows, prices, pick_prices_from_dataframe(dates, pmedf, "close")
    )


def tessa_xpme(
    dates: List[date],
    cashflows: List[float],
    prices: List[float],
    pme_ticker: str,
    pme_source: tessa.SourceType = "yahoo",
) -> float:
    """Calculate PME and return the PME IRR only, retrieving PME price information via
    tessa library in real time.
    """
    return tessa_verbose_xpme(dates, cashflows, prices, pme_ticker, pme_source)[0]
