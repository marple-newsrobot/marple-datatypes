# encoding: utf-8

import os
import pytest
import csvkit as csv
from collections import defaultdict

def iterate_files(directory, file_extension=None):
    """ Iterate all files in folder an subfolders

        :param directory: Path to base dir to start iterating from
        :param file_extension: "csv" or ".csv"
    """
    if file_extension is not None:
        if file_extension[0] is not ".":
            file_extension = "." + file_extension

    for path, subdirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(path, filename)

            _name, _extension = os.path.splitext(file_path)

            if file_extension is None:
                yield file_path
            elif _extension == file_extension:
                yield file_path
            else:
                continue


@pytest.fixture(scope="session")
def get_datatype_files():
    """ Iterate all datatype files in project
    """
    files = []
    for directory in ["misc","periods","regions"]:
        file_iterator = iterate_files(directory, file_extension="csv")
        files += [x for x in file_iterator]

    return files


@pytest.fixture(scope="session")
def get_ids(get_datatype_files):
    """ Get a list of all ids in project
    """
    files = get_datatype_files
    ids = []
    for file_path in files:
        with open(file_path) as f:
            reader = csv.DictReader(f)
            ids += [ x["id"] for x in reader ]

    return ids


@pytest.fixture(scope="session")
def get_datatypes_csv():
    """ Get content of datatypes.csv
    """
    with open("datatypes.csv") as f:
        return [x for x in csv.DictReader(f)]


@pytest.fixture(scope="session")
def get_relations():
    """ Returns the content of relations.csv grouped by
        "relation_type" as json

        {
            "one_to_one": [ "parent"],
            "one_to_many": ["neighbours"]
        }
    """
    relations = defaultdict(list)
    with open("relations.csv") as f:
        for row in csv.DictReader(f):
            id_ = row["id"]
            relation_type = row["relation_type"]
            relations[relation_type].append(id_)

    return relations

