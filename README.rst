bls
===

A Python library for the Bureau of Labor Statistics API.

Use the function `get_series()` to retrieve data. `get_series()` has three
arguments: a series id or sequence of series ids, a start year, and an end
year.

Note that you cannot currently retrieve more than ten years of data. By
default, the last ten years are retrieved. You can specify only the start year
to retrieve the ten years following, only the end year to retrieve the ten:
previous years, or both to retrieve some smaller range.

`bls` is a new module and undergoing very rapid development. Look for new
features in the near future, and report bugs at
<https://github.com/OliverSherouse/bls/issues>.
