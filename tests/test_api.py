import bls


def test_monthly_value():
    assert bls.get_series('LNS14000000', startyear=1948)['1948-01'] == 3.4


def test_quarterly_value():
    assert (
        bls.get_series('CIU2020000000000A', startyear=2001)['2001-Q1'] == 3.8
    )


def test_annual_value():
    assert (
        bls.get_series('TUU10100AA01000007', startyear=2009)['2009'] == 148720
    )
