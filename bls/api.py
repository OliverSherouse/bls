"""
api.py: access the BLS api directly
"""

from __future__ import (print_function, division, absolute_import,
                        unicode_literals)

import datetime
import json
try:
    from urllib.request import Request, urlopen
except ImportError: #python2
    from urllib2 import Request, urlopen


import pandas as pd

BASE_URL = "http://api.bls.gov/publicAPI/v1/timeseries/data/"

def get_series(series, startyear=None, endyear=None):
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
    if type(series) == str:
        series = [series]
    thisyear = datetime.datetime.today().year
    if endyear is None or int(endyear) > thisyear:
        if startyear is None:
            endyear, startyear = thisyear, thisyear - 10
        else:
            endyear = min(int(startyear) + 10, thisyear)
    elif startyear is None:
        startyear = int(endyear) - 10
    data = json.dumps({"seriesid": series,
                       "startyear": str(startyear),
                       "endyear": str(endyear),
                       }).encode()
    headers = {"Content-type": "application/json"}
    resp = urlopen(Request(BASE_URL, data=data, headers=headers)).read()
    resp = json.loads(resp.decode())
    results = resp["Results"]
    df = pd.DataFrame({series["seriesID"]: {
        datetime.datetime(int(i["year"]), int(i["period"][-2:]), 1):
        float(i["value"]) for i in series["data"] if i["period"] != "M13"}
        for series in results["series"]})
    return df[df.columns[0]] if len(df.columns) == 1 else df
