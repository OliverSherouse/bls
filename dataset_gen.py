"""
dataset_gen.py: a script to create full dataset descriptions from bls data

This is a utility script needed to create the searchable datasets in the
bls.datasets module.  Since BLS doesn't have any kind of a coherent catalog of
ids and codes, I use simple descriptions in the datasets.json file in the root
directory to pull all the metadata from the BLS FTP website, parse it, and
create a full json description of all the codes for each part of a full series
id.
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

import json
import os.path
import urllib.error
import urllib.request
import sys

BASEURL = "ftp://ftp.bls.gov/pub/time.series/{0}/{0}.{1}"


def get_lines(data_id, part):
    try:
        url = urllib.request.urlopen(BASEURL.format(data_id, part))
        lines = url.read().decode().splitlines()
    except urllib.error.URLError:
        raise ValueError("Couldn't read url for {}.{}".format(data_id, part))
    firstline = -1
    for i, line in enumerate(lines):
        if len(line.split("\t")) != 1:
            firstline = i
            break
    return lines[firstline:]


def find_likely(split, part, endings):
    if type(endings) == str:
        endings = [endings]
    for i in endings:
        if part + i in split[0]:
            return split[0].index(part + i)
    likely = [i for i in split[0]
              if i.endswith("_name") or i.endswith("_text")]
    if len(likely) != 1:
        raise ValueError
    return split[0].index(likely[0])


def get_part_dict(data_id, part):
    lines = get_lines(data_id, part)
    split = [i.split("\t") for i in lines if i != '']
    if len(split[0]) == 2:
        return tuple((i[1], i[0]) for i in split[1:])
    try:
        label_col = find_likely(split, part, ["_name", "_text"])
    except ValueError:
        raise ValueError("No likely labels for {}.{}".format(data_id, part))
    try:
        code_col = find_likely(split, part, ["_code"])
    except ValueError:
        raise ValueError("No likely codes for {}.{}".format(data_id, part))
    return tuple((i[label_col], i[code_col]) for i in split[1:])


def extend_dataset(dataset):
    for i in dataset["parts"]:
        if i not in dataset:
            dataset[i] = get_part_dict(dataset["id"], i)


def main():
    with open("datasets.json") as inf:
        datasets = json.load(inf)
    for dataset in datasets:
        extend_dataset(dataset)
    with open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),
                           "bls", "datasets.json"), 'w') as outf:
        json.dump(datasets, outf)

if __name__ == "__main__":
    main()
