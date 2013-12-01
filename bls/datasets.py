"""
datasets.py: generate datasets objects from json representations
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

import json
import os.path


class Dataset(object):
    def __init__(self, rep):
        self.code = rep["id"]
        self.description = rep["description"]
        self.parts = rep["parts"]
        self._defaults = {i: rep[i][0][1] for i in self.parts}
        self._parts = {i: dict(rep[i]) for i in self.parts}

    def search(self, part, query):
        terms = [i.casefold() for i in query.split()]
        results = [i for i in self._parts[part].keys()
                   if all([j in i.casefold() for j in terms])]
        return {i: self._parts[part][i] for i in results}

    def get_id(self, *args, **kwargs):
        id_code = [self.code]
        for part in self.parts:
            if part in kwargs:
                if kwargs[part] in self._parts[part]:
                    partcode = self._parts[part][kwargs[part]]
                elif kwargs[part] in self._parts[part].values():
                    partcode = kwargs[part]
                else:
                    raise ValueError('Unrecognized value "{}" for {}'.format(
                        kwargs[part], part))
            else:
                partcode = self._defaults[part]
            id_code.append(partcode)
        return "".join(id_code)

with open(os.path.join(os.path.dirname(__file__), "datasets.json")) as inf:
    ids = json.load(inf)

DATASETS = [Dataset(i) for i in ids]

def search_datasets(query):
    terms = [i.casefold() for i in query.split()]
    return {i.description: i for i in DATASETS
            if all([j in i.description.casefold() for j in terms])}
