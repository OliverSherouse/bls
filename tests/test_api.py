import bls


def test_known_value():
    series = bls.get_series('LNS14000000', startyear=1948)
    assert series.iloc[0].round(2) == 3.40

