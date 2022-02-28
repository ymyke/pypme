from pypme import __version__, calc_pme


def test_version():
    assert __version__ == "0.1.0"


# FIXME Use mark test or whatever it's called.
# FIXME Add many more test data sets.
def test_calc_pme():
    cashflows = [-100, -50, 60, 100]
    prices = [1.00000000, 1.15000000, 1.28939394, 1.18624242, 1.58165657]
    pme_prices = [100, 105, 115, 100, 120]
    pme = calc_pme(cashflows=cashflows, prices=prices, pme_prices=pme_prices)
    assert round(pme*100.0, 2) == 2.02
