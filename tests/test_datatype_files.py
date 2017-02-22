# encoding: utf-8


from fixtures import get_datatype_files, get_ids
import csvkit as csv

def get_duplicates(l):
    return set([x for x in l if l.count(x) > 1])

def test_id_uniqueness(get_ids):
    """ Test there are no id duplicates
    """
    ids = get_ids
    duplicates = get_duplicates(ids)
    assert len(duplicates) == 0

def test_parent_validity(get_datatype_files, get_ids):
    """ Make sure that all values in parent columns are
        valid indecies
    """
    files, ids = get_datatype_files, get_ids
    for file_path in files:
        with open(file_path) as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            if "parent" in headers:
                for row in reader:
                    parent = row["parent"]
                    if (parent is not None) and (parent != ''):
                        assert parent in ids


