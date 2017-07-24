# encoding: utf-8


from fixtures import get_datatypes_csv
from glob2 import glob


def test_basics(get_datatypes_csv):
    """ Test there are no id duplicates
    """
    datatypes_csv = get_datatypes_csv
    assert len(datatypes_csv) > 0
    col_names = datatypes_csv[0].keys()

    assert "id" in col_names
    assert "allowed_values" in col_names

def test_allowed_values(get_datatypes_csv):
    """ Make sure all
    """
    datatypes_csv = get_datatypes_csv

    for row in datatypes_csv:
        if row["allowed_values"] == "":
            continue
        glob_expr = row["allowed_values"] + ".csv"
        file_iter = glob(glob_expr)
        files = [x for x in file_iter]
        msg = "{} refers to no files (on '{}' in datatypes.csv)"\
            .format(glob_expr, row["id"])
        assert len(files) > 0, msg
