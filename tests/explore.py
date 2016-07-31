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


def exp1():
    dfv = dfvalidate.load_csv("../datatypes.csv")

    for df in tfiles():
        errors = dfv.validate(df)
    print errors


exp1()
