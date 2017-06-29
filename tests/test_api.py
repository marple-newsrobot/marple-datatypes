# encoding: utf-8

import os 
import pytest
import csvkit as csv
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import api.app as api
import unittest
import json
#from api.app import *

class TestAPI(unittest.TestCase):


	def test_datatypes(self):
		api.app.testing = True
		self.app = api.app.test_client()
		res = self.app.get("/datatype")
		data = json.loads(res.data)
		assert isinstance(data, list)
		assert len(data) != 0

if __name__ == '__main__':
    unittest.main()
