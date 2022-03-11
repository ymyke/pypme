# pypme – Python library for PME (Public Market Equivalent) calculation

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

## Garbage in, garbage out

Note that the library will only perform essential sanity checks and otherwise just works
with what it gets, also with nonsensical data. E.g.:

```python
from pypme import verbose_pme

pmeirr, assetirr, df = verbose_pme(
    cashflows=[-10, 500], prices=[1, 1, 1], pme_prices=[1, 1, 1]
)
```

Results in this df and IRRs of 0:

![Garbage example df](https://raw.githubusercontent.com/ymyke/pypme/main/images/garbage_example_df.png)

## References

- [Google Sheet w/ reference calculation](https://docs.google.com/spreadsheets/d/1LMSBU19oWx8jw1nGoChfimY5asUA4q6Vzh7jRZ_7_HE/edit#gid=0)
- [Modified PME on Wikipedia](https://en.wikipedia.org/wiki/Public_Market_Equivalent#Modified_PME)
