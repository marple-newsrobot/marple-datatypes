#coding=utf-8
import jsonstat
import json
import datetime
import os
import pandas as pd
import glob
import copy
__version__ = 1


def load_json(filename):
    'Opens file and load JSON dump of schema'
    with open(filename) as f:
        blob = f.read()
    return loads_json(blob)


def loads_json(blob):
    'Load JSON dump of schema'
    dfv = DataframeValidator()

    obj = json.loads(blob)
    for k, v in obj.items():
        if k in dfv.config:

            dfv.config[k] = v
    dfv.config["version"] = __version__
    dfv._update_allowed_values_encoding
    return dfv


def load_csv(src):
    '''Generate schema accroding to csv format
    id,nullable,required,description,value_type,allowed_values
    where allowed_values i file path of CSV:s with ID columns with allowed values
    '''

    base_dir, _ = os.path.split(src)
    df = pd.read_csv(src, encoding="utf-8")

    #get allowed values, only if column is used
    zdf = df[~df["allowed_values"].isnull()].copy()["id allowed_values".split(
    )].dropna()
    vv = {}

    values = zdf["allowed_values"].unique()
    for v in values:
        s = set()
        glb = os.path.join(base_dir, v + ".csv")
        for g in glob.glob(glb):
            q = set(pd.read_csv(g)["id"].unique())
            s = s.union(q)
        vv[v] = sorted(s)

    values = zdf["allowed_values"].apply(lambda x: vv[x])
    names = zdf["id"]
    av = dict(zip(names, values))

    config = {}
    config["allowed_values"] = av

    #update other columns
    df = df.set_index("id")
    config["nullable"] = list(df[df["nullable"] == False].index)
    config["required"] = list(df[df["required"] == True].index)
    config["names"] = list(df.index)
    config["value_type"] = dict(zip(df.index, df["value_type"].apply(
        lambda x: x.split())))

    return DataframeValidator(config)


class DataframeValidator(object):
    '''Dataframe validator, validates a pandas dataframe according to a validation schema'''

    def __init__(self, config={}):
        self.config = {
            'allowed_values': {},
            'created': datetime.datetime.utcnow().isoformat(),
            'names': [],
            'nullable': [],
            'required': [],
            'updated': datetime.datetime.utcnow().isoformat(),
            'value_type': {},
            'version': __version__,
        }
        self.config.update(config)
        self._update_allowed_values_encoding()

    def _update_allowed_values_encoding(self):
        def unicode_bitte(x):
            if type(x) == type(u''):
                return x
            elif type(x) == type(b''):
                return x.decode("utf-8")

        for k, v in self.config["allowed_values"].items():

            self.config["allowed_values"][k] = sorted(
                [unicode_bitte(x) for x in v])

    def set(self, name):
        """Convience function, returns a set from the 'config' object"""
        return set(self.config[name])

    def clone(self):
        """Deepclone of the object"""
        config = copy.copy(self.config)
        clone = DataframeValidator(config)
        return clone

    def dumps(self):
        '''JSON dump of schema'''
        clone = self.clone()
        clone.config["updated"] = datetime.datetime.utcnow().isoformat()
        return json.dumps(clone.config, sort_keys=True, indent=1)

    def validate(self, df):
        """Validate a pandas dataframe according to the schema"""

        result = []
        sdf = set(df.columns)

        def efmt(desc, column, row="N/A"):
            f = {'desc': desc, 'column': column, 'row': row}
            return "'%(desc)s' column:%(column)s row:%(row)s" % f

        for name in self.set("nullable").intersection(sdf):
            indexes = df[df[name].isnull() == True].index
            for z in indexes:
                result.append(efmt("None value in non-nullable column",
                                   column=name, ))

        for name in sdf - self.set("names"):
            result.append(efmt("Unkown column name", column=name, row="N/A"))

        for name in self.set("required") - sdf:
            result.append(efmt("Required column missing",
                               column=name,
                               row="N/A"))

        for name in sdf:
            if name not in self.set("allowed_values"):
                continue
            n = self.config["allowed_values"][name]
            # print df[df[name].isin(n) == False].index
            for r in df[df[name].isin(n) == False].index:
                result.append(efmt("Allowed values mismatch",
                                   column=name,
                                   row=r))
        return result
