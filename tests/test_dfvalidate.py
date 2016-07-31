#coding=utf-8
import sys
sys.path.append("..")
import dfvalidate
import tempfile
from StringIO import StringIO
import os
import jsonstat


def tfiles():

    files = [
        "~/Dropbox/marple-shared-data/data/jsonstat/BRÅ/reported_crime/crime_code/yearly/9320.json",
        "~/Dropbox/marple-shared-data/data/jsonstat/AMS/unemployment/monthly/count/youth.json",
    ]
    for f in files:
        js = jsonstat.from_file(os.path.expanduser(f))
        yield js.to_data_frame()
        break


def test_load_csv():
    #just load it, watch for exceptions
    dfv = dfvalidate.load_csv("../datatypes.csv")
    si = StringIO(dfv.dumps())


def test_json_save_restore():
    q = dfvalidate.load_csv("../datatypes.csv")
    si = StringIO(q.dumps())
    p = dfvalidate.loads_json(si.getvalue())
    for k, v in q.config.items():
        if k == "updated":
            continue
        if q.config[k] != p.config[k]:
            raise ValueError("compare failed %s" % k)


def test_validate():
    dfv = dfvalidate.load_csv("../datatypes.csv")

    for df in tfiles():
        errors = dfv.validate(df)
        assert len(errors) == 0
