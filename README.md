# pypme – Python package for PME (Public Market Equivalent) calculation

Based on the [Modified PME
method](https://en.wikipedia.org/wiki/Public_Market_Equivalent#Modified_PME).

## Example

```python
from pypme import verbose_xpme
from datetime import date

pmeirr, assetirr, df = verbose_xpme(
    dates=[date(2015, 1, 1), date(2015, 6, 12), date(2016, 2, 15)],
    cashflows=[-10000, 7500],
    prices=[100, 120, 100],
    pme_prices=[100, 150, 100],
)
```

Will return `0.5525698793027238` and  `0.19495150355969598` for the IRRs and produce this
dataframe:

![Example dataframe](https://raw.githubusercontent.com/ymyke/pypme/main/images/example_df.png)

Notes:
- The `cashflows` are interpreted from a transaction account that is used to buy from an
  asset at price `prices`.
- The corresponding prices for the PME are `pme_prices`.
- The `cashflows` is extended with one element representing the remaining value, that's
  why all the other lists (`dates`, `prices`, `pme_prices`) need to be exactly 1 element
  longer than `cashflows`.

## Variants

- `xpme`: Calculate PME for unevenly spaced / scheduled cashflows and return the PME IRR
  only. In this case, the IRR is always annual.
- `verbose_xpme`: Calculate PME for unevenly spaced / scheduled cashflows and return
  vebose information.
- `pme`: Calculate PME for evenly spaced cashflows and return the PME IRR only. In this
  case, the IRR is for the underlying period.
- `verbose_pme`: Calculate PME for evenly spaced cashflows and return vebose
  information.
- `tessa_xpme` and `tessa_verbose_xpme`: Use live price information via the tessa
  library. See below.

## tessa examples – using tessa to retrieve PME prices online

Use `tessa_xpme` and `tessa_verbose_xpme` to get live prices via the [tessa
library](https://github.com/ymyke/tessa) and use those prices as the PME. Like so:

```python
from datetime import datetime, timezone
from pypme import tessa_xpme

common_args = {
    "dates": [
        datetime(2012, 1, 1, tzinfo=timezone.utc), 
        datetime(2013, 1, 1, tzinfo=timezone.utc)
    ],
    "cashflows": [-100],
    "prices": [1, 1],
}
print(tessa_xpme(pme_ticker="LIT", **common_args))  # source will default to "yahoo"
print(tessa_xpme(pme_ticker="bitcoin", pme_source="coingecko", **common_args))
print(tessa_xpme(pme_ticker="SREN.SW", pme_source="yahoo", **common_args))
```

Note that the dates need to be timezone-aware for these functions.


## Garbage in, garbage out

Note that the package will only perform essential sanity checks and otherwise just works
with what it gets, also with nonsensical data. E.g.:

```python
from pypme import verbose_pme

pmeirr, assetirr, df = verbose_pme(
    cashflows=[-10, 500], prices=[1, 1, 1], pme_prices=[1, 1, 1]
)
```

Results in this df and IRRs of 0:

![Garbage example df](https://raw.githubusercontent.com/ymyke/pypme/main/images/garbage_example_df.png)


## Other noteworthy libraries

- [tessa](https://github.com/ymyke/tessa): Find financial assets and get their price history without worrying about different APIs or rate limiting.
- [strela](https://github.com/ymyke/strela): A python package for financial alerts.


## References

- [Google Sheet w/ reference calculation](https://docs.google.com/spreadsheets/d/1LMSBU19oWx8jw1nGoChfimY5asUA4q6Vzh7jRZ_7_HE/edit#gid=0)
- [Modified PME on Wikipedia](https://en.wikipedia.org/wiki/Public_Market_Equivalent#Modified_PME)
