"""
BEA.py

A Library to access the Bureau of Labor Statistics API
"""
#
#Copyright (C) 2012-2013 Oliver Sherouse <Oliver DOT Sherouse AT gmail DOT com>

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not. If not, see <http://www.gnu.org/licenses/>.

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
        monthly observation as a row
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
    results = json.loads(resp["Results"])
    try:
        df = pd.DataFrame({series["seriesID"]: {
            datetime.datetime(int(i["year"]), int(i["period"][-2:]), 1):
            float(i["value"]) for i in series["data"] if i["period"] != "M13"}
            for series in results["series"]})
    except ValueError:
        print(i)
    return(df)
