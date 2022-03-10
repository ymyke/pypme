pypme – Python library for PME (Public Market Equivalent) calculation

## Todo

* Check my old code for possible additional testcases.


## PME

- Example calculation:
https://docs.google.com/spreadsheets/d/1LMSBU19oWx8jw1nGoChfimY5asUA4q6Vzh7jRZ_7_HE/edit#gid=0
- Source: https://en.wikipedia.org/wiki/Public_Market_Equivalent#Modified_PME

## Garbage in, garbage out

Note that the library will only perform essential sanity checks and otherwise just works
with what it gets, also with nonsensical data. E.g.:

```python
pmeirr, assetirr, df = verbose_pme(
    cashflows=[-10, 500], prices=[1, 1, 1], pme_prices=[1, 1, 1]
)
```

Results in this df and IRRs of 0:

|      | ('Account', 'CF') | ('Asset', 'Price') | ('Asset', 'NAVpre') | ('Asset', 'CF') | ('Asset', 'NAVpost') | ('PME', 'Price') | ('PME', 'NAVpre') | ('PME', 'CF') | ('PME', 'NAVpost') |
| ---: | ----------------: | -----------------: | ------------------: | --------------: | -------------------: | ---------------: | ----------------: | ------------: | -----------------: |
|    0 |               -10 |                  1 |                   0 |              10 |                   10 |                1 |                 0 |            10 |                 10 |
|    1 |               500 |                  1 |                  10 |            -500 |                 -490 |                1 |                10 |          -500 |               -490 |
|    2 |              -490 |                  1 |                -490 |             490 |                    0 |                1 |              -490 |           490 |                  0 |


## Working w poetry

- https://stackoverflow.com/questions/59882884/vscode-doesnt-show-poetry-virtualenvs-in-select-interpreter-option
  - To store the venv folder locally and make sure vscode can recognize it: `poetry config virtualenvs.in-project true`
  - The article also explains what to do if you already created the venv file.
- Used `poetry env use C:\Users\myken\AppData\Local\Programs\Python\Python39\python.exe` to set specific python version.
- https://towardsdatascience.com/how-to-effortlessly-publish-your-python-package-to-pypi-using-poetry-44b305362f9f
- https://betterprogramming.pub/avoid-the-snake-pit-of-python-package-management-with-poetry-54ab186cf2a4
