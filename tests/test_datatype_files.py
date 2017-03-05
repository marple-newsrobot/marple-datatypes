# encoding: utf-8


from fixtures import get_datatype_files, get_ids, get_relations
import csvkit as csv

def get_duplicates(l):
    return set([x for x in l if l.count(x) > 1])




def test_id_uniqueness(get_ids):
    """ Test there are no id duplicates
    """
    ids = get_ids
    duplicates = get_duplicates(ids)
    assert len(duplicates) == 0

def test_one_to_one_relations(get_datatype_files, get_ids, get_relations):
    """ Make sure that all values in eg. parent columns are
        valid indecies
    """
    files, ids, relations = get_datatype_files, get_ids, get_relations
    one_to_one_relations = relations["one_to_one"]
    for file_path in files:
        with open(file_path) as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            for col in one_to_one_relations:
                if col in headers:
                    for row in reader:
                        value = row[col]
                        if (value is not None) and (value != ''):
                            msg = u"{} in column {} is not a valid index"\
                                    .format(value, col)
                            assert value in ids

def test_one_to_many_relations(get_datatype_files, get_ids, get_relations):
    """ Make sure that all values in eg. neighbous columns are
        valid indecies
    """
    files, ids, relations = get_datatype_files, get_ids, get_relations
    one_to_many_relations = relations["one_to_many"]
    for file_path in files:
        with open(file_path) as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            for col in one_to_many_relations:
                if col in headers:
                    for row in reader:
                        values = row[col].split(",")
                        for value in values:
                            if (value is not None) and (value != ''):
                                msg = u"{} in column {} is not a valid index"\
                                    .format(value, col)
                                assert value in ids, msg


