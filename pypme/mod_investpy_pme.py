"""Calculate PME and get the prices from Investing.com via the `investpy` module.

Important: The Investing API has rate limiting measures in place and will block you if
you hit the API too often. You will notice by getting 429 errors (or maybe
also/alternatively 503). Wait roughly 2 seconds between each consecutive call to the API
via the functions in this module.

Args: 
- pme_type: One of "stock", "etf", "fund", "crypto", "bond", "index", "certificate".
  Defaults to "stock".
- pme_ticker: The ticker symbol/name.
- pme_country: The ticker's country of residence. Defaults to "united states".

Refer to the `pme` module to understand other arguments and what the functions return.
"""

from typing import List, Tuple
from datetime import date
import pandas as pd
import investpy
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


def get_historical_data(ticker: str, type: str, **kwargs) -> pd.DataFrame:
    """Small wrapper to make the investpy interface accessible in a more unified fashion."""
    kwargs[type] = ticker
    if type == "crypto" and "country" in kwargs:
        del kwargs["country"]
    return getattr(investpy, "get_" + type + "_historical_data")(**kwargs)


def investpy_verbose_pme(
    dates: List[date],
    cashflows: List[float],
    prices: List[float],
    pme_ticker: str,
    pme_type: str = "stock",
    pme_country: str = "united states",
) -> Tuple[float, float, pd.DataFrame]:
    """Calculate PME return vebose information, retrieving PME price information from
    Investing.com in real time.
    """
    pmedf = get_historical_data(
        pme_ticker,
        pme_type,
        country=pme_country,
        from_date=dates[0].strftime("%d/%m/%Y"),
        to_date=dates[-1].strftime("%d/%m/%Y"),
    )
    return verbose_xpme(
        dates, cashflows, prices, pick_prices_from_dataframe(dates, pmedf, "Close")
    )


def investpy_pme(
    dates: List[date],
    cashflows: List[float],
    prices: List[float],
    pme_ticker: str,
    pme_type: str = "stock",
    pme_country: str = "united states",
) -> Tuple[float, float, pd.DataFrame]:
    """Calculate PME and return the PME IRR only, retrieving PME price information from
    Investing.com in real time.
    """
    return investpy_verbose_pme(
        dates, cashflows, prices, pme_ticker, pme_type, pme_country
    )[0]
