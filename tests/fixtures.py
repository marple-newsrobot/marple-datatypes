# encoding: utf-8

import os 
import pytest

def iterate_files(directory):
    """ Iterate all files in folder an subfolders
    """
    for path, subdirs, files in os.walk(directory):
        for filename in files:
            yield os.path.join(path, filename)
         #print(str(f) + os.linesep) 


@pytest.fixture(scope="session")
def get_datatype_files():
    """ Iterate all datatype files in project
    """
    files = []
    for directory in ["misc","periods","regions"]:
        files += [x for x in iterate_files(directory)]

    return files