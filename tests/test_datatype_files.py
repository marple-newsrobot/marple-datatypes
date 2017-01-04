# encoding: utf-8


from fixtures import get_datatype_files
import csvkit as csv

def get_duplicates(l):
    return set([x for x in l if l.count(x) > 1])

def test_id_uniqueness(get_datatype_files):
    """ Test there are no id duplicates
    """
    ids = []
    for file_path in get_datatype_files:
        with open(file_path) as f:
            reader = csv.DictReader(f)
            ids += [ x["id"] for x in reader ]

    duplicates = get_duplicates(ids)
    assert len(duplicates) == 0

