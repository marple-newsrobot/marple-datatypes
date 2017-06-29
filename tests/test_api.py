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

class ApiTest(unittest.TestCase):

	def test_datatypes(self):
		api.app.testing = True
		self.app = api.app.test_client()
		res = self.app.get("/datatype")
		data = json.loads(res.data)
		assert isinstance(data, list)
		assert len(data) != 0
		self.children(data)


	def children(self, data):
		for item in data:
			res = self.app.get(clear_path(item['path']))
			item_data = json.loads(res.data)
			assert isinstance(item_data, dict)
			assert bool(item_data)
			if ('allowed_values' in item_data):
				self.children(item_data['allowed_values'])

def clear_path(path):
		return "/" + ("/".join(path.split("/", 3)[3:]))
	    #return "/".join(url.split("/", 3)[:3]) 
if __name__ == '__main__':
    unittest.main()
