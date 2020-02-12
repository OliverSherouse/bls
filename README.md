# bls

A Python library for the Bureau of Labor Statistics API.

| Branch | Status                                                                                                                                                                                               |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| master | [![master branch status](https://github.com/OliverSherouse/bls/workflows/Tests/badge.svg?branch=master)](https://github.com/OliverSherouse/bls/actions?query=workflow%3A%22Tests%22+branch%3Amaster) |
| dev    | [![dev branch status](https://github.com/OliverSherouse/bls/workflows/Tests/badge.svg?branch=dev)](https://github.com/OliverSherouse/bls/actions?query=workflow%3A%22Tests%22+branch%3Adev)          |

Use the function `get_series()` to retrieve data. `get_series()` has four
arguments: a series id or sequence of series ids, a start year, an end year, and
an optional API key.

It is highly recommended that you [register for an API key with
BLS](https://data.bls.gov/registrationEngine/). You can supply the key to the
library by passing it to `get_series()` or by setting an environment variable
called `BLS_API_KEY`.

The timespan returned by the `get_series()` function depends on whether you
specify `startyear`, `endyear`, `api` or some combination thereof, as shown in
the table below:

| startyear | endyear | api | result                                                         |
| --------- | ------- | --- | -------------------------------------------------------------- |
| no        | no      | no  | BLS default (last 3 years)                                     |
| yes       | no      | no  | Ten years starting from `startyear` or until present           |
| no        | yes     | no  | Ten years ending with `endyear`                                |
| yes       | yes     | no  | `startyear` through `endyear` if ten years or fewer else error |
| no        | no      | yes | BLS default (last 3 years)                                     |
| yes       | no      | yes | `startyear` through present                                    |
| no        | yes     | yes | Twenty years ending with `endyear`                             |
| yes       | yes     | yes | `startyear` through `endyear`                                  |

`bls` is under development. Look for new features in the near future, and report
bugs at <https://github.com/OliverSherouse/bls/issues>.
