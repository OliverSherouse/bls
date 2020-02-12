import datetime

import bls
import pandas as pd
import pytest


@pytest.fixture
def nokey():
    key = bls.api._KEY.key
    bls.api.unset_api_key()
    yield
    bls.api.set_api_key(key)


def test_monthly_value():
    assert bls.get_series("LNS14000000", startyear=1948, endyear=1948)["1948-01"] == 3.4


def test_monthly_value_multiple():
    assert (
        bls.get_series(["LNS14000000", "LNS14000001"], startyear=1948, endyear=1948)
        .xs("1948-01")
        .equals(pd.Series({"LNS14000000": 3.4, "LNS14000001": 3.4}))
    )


def test_quarterly_value():
    assert (
        bls.get_series("CIU2020000000000A", startyear=2001, endyear=2001)["2001-Q1"]
        == 3.8
    )


def test_annual_value():
    assert (
        bls.get_series("TUU10100AA01000007", startyear=2009, endyear=2009)["2009"]
        == 148720
    )


def test_key_till_thisyear():
    series = bls.get_series("LNS14000000", startyear=1948)
    years = series.index.year
    assert (years.min(), years.max()) == (1948, datetime.date.today().year)


def test_key_end_twenty_years():
    series = bls.get_series("LNS14000000", endyear=2018)
    years = series.index.year
    assert (years.min(), years.max()) == (1999, 2018)


# These tests are unreliable because of API limits
# def test_no_key_start_tenyears(nokey):
#     series = bls.get_series('LNS14000000', startyear=1948)
#     years = series.index.year
#     assert (years.min(), years.max()) == (1948, 1957)


# def test_no_key_end_ten_years(nokey):
#     series = bls.get_series('LNS14000000', endyear=2018)
#     years = series.index.year
#     assert (years.min(), years.max()) == (2009, 2018)


def test_error_no_key_too_many_years(nokey):
    with pytest.raises(ValueError):
        bls.get_series("LNS14000000", startyear=1948, endyear=2018)


def test_error_no_data():
    with pytest.raises(ValueError):
        bls.get_series("LNS14000000", startyear=1900, endyear=1900)
