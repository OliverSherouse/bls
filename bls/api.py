"""
api.py: access the BLS api directly
"""

from __future__ import (print_function, division, absolute_import,
                        unicode_literals)

import datetime
import os
import requests
import json
import pandas as pd

BASE_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

listsum = lambda iterable: sum(iterable, [])
_headers = {'Content-type': 'application/json'}


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

    # Process keywords and set defaults
    if type(series) == str:
        series = [series]
    thisyear = datetime.datetime.today().year
    if not (endyear and int(endyear) <= thisyear):
        endyear = thisyear
    if not startyear:
        startyear = thisyear - 9

    results = []
    sectionyear = min(startyear + 9, endyear)
    data = {
        "seriesid": series,
        "startyear": str(startyear),
        "endyear": str(sectionyear)
    }
    if key:
        data.update({
            'registrationkey': key,
            'catalog': catalog,
            'calculations': calculations,
            'annualaverages': annualaverages
        })

    # Collect the API results 10 years at a time
    while startyear <= endyear:
        key = key or _KEY.key
        data.update({
            "startyear": str(startyear),
            "endyear": str(sectionyear)
        })

        results.append(requests.post(BASE_URL, 
            data=json.dumps(data),
            headers=_headers).json()["Results"])
        startyear, sectionyear = sectionyear + 1, min(sectionyear + 10, endyear)

    num_decades = len(results)
    num_series = len(results[0]['series'])

    merged = { 
            'series': [{ 
                'data': listsum([results[j]['series'][0]['data'] \
                        for j in range(num_decades)]),
                'seriesID': results[0]['series'][i]['seriesID'], 
                } for i in range(num_series)]
            }

    return merged 


def parse_series(series):
    if not len(series['data']):
        raise ValueError(
            'No data received for series {}! Are your parameters correct?'
            .format(series['SeriesID'])
        )
    df = pd.DataFrame(series['data'])
    freq = df['period'].iloc[0][0]
    if freq == 'A':
        return (
            df.assign(date=pd.to_datetime(df['year']))
            .set_index('date')
            .to_period(freq='A-JAN')
            ['value']
        )
    if freq == 'Q':
        return (
            df.assign(date=pd.to_datetime(
                df['year']
                .str.cat(df['period'].str.replace('Q0', 'Q'))
            ))
            .set_index('date')
            .to_period(freq='Q')
            ['value']
        )
    if freq == 'M':
        return (
            df.assign(date=pd.to_datetime(
                df['year']
                .str.cat(df['period'].str.replace('M', '-'))
            ))
            [df['period'] != 'M13']
            .set_index('date')
            .to_period(freq='M')
            ['value']
        )
    raise ValueError('Unknown period format: {}'.format(df['period'].iloc[0]))


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
        series["seriesID"]: parse_series(series)
        for series in results["series"]
    })
    df = df.applymap(float)
    return df[df.columns[0]] if len(df.columns) == 1 else df

