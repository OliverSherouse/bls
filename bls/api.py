"""
api.py: access the BLS api directly
"""

from __future__ import (print_function, division, absolute_import,
                        unicode_literals)

import datetime


import os
import requests
import pandas as pd

BASE_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"


class _Key(object):

    def __init__(self):
        self.key = os.environ.get('BLS_API_KEY')


_KEY = _Key()


def set_api_key(key):
    _KEY.key = key


def unset_api_key():
    _KEY.key = None


def _get_json(series, startyear=None, endyear=None, key=None,
              catalog=False, calculations=False, annualaverages=False):
    if type(series) == str:
        series = [series]
    thisyear = datetime.datetime.today().year
    if endyear is None or int(endyear) > thisyear:
        if startyear is None:
            endyear, startyear = thisyear, thisyear - 9
        else:
            endyear = min(int(startyear) + 9, thisyear)
    elif startyear is None:
        startyear = int(endyear) - 10
    # TODO: daisy-chain requests to cover full timespan
    key = key if key is not None else _KEY.key
    data = {
        "seriesid": series,
        "startyear": startyear,
        "endyear": endyear
    }
    if key is not None:
        data.update({
            'registrationkey': key,
            'catalog': catalog,
            'calculations': calculations,
            'annualaverages': annualaverages
        })

    return requests.post(BASE_URL, data=data).json()["Results"]


def get_series(series, startyear=None, endyear=None, key=None,
               catalog=False, calculations=False, annualaverages=False):
    """
    Retrieve one or more series from BLS. Note that only ten years may be
    retrieved at a time

    :series: a series id or sequence of series ids to retrieve
    :startyear: The first year for which  to retrieve data. Defaults to ten
        years before the endyear
    :endyear: The last year for which to retrieve data. Defaults to ten years
        after the startyear, if given, or else the current year
    :returns: a pandas DataFrame object with each series as a column and each
        monthly observation as a row. If only one series is requested, a pandas
        Series object is returned instead of a DataFrame.
    """
    results = _get_json(series, startyear, endyear, key, catalog,
                        calculations, annualaverages)
    df = pd.DataFrame({
        series["seriesID"]: {
            "-".join((i['year'], i['period'])): i["value"]
            for i in series["data"]
            if i["period"] != "M13"
        } for series in results["series"]})
    df.index = pd.to_datetime(df.index)
    df = df.applymap(float)
    return df[df.columns[0]] if len(df.columns) == 1 else df
