# encoding: utf-8
from flask import Flask, jsonify, abort, request, make_response, url_for
from marple.datatypes import Domain
from marple.schema import Datatype
from marple.csv import CsvFile
from marple.utils import isNaN
import csvkit as csv
import os
from copy import deepcopy
import pprint
import sys
pp = pprint.PrettyPrinter(indent=2)
DEFAULT_LANG = "en"
SCHEMA_DIR = "schemas"
# Get from settings, should point to root folder
DATATYPES_DIR = ".."
# Get from request
LANG = "en"
# Get from request
DOMAIN = "http://marple-datatypes.herokuapp.com"

# Points to root folder
RELATIONS_CSV_PATH = "../relations.csv"
app = Flask(__name__, static_url_path = "")

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route("/datatype", methods=['GET'])
def get_datatypes():
    ALL_DOMAINS = Domain("*/*", datatypes_dir=DATATYPES_DIR)
    data = []
    file_path = os.path.join(DATATYPES_DIR, "datatypes.csv")
    csv_file = CsvFile(file_path)
    # TODO: Add path
    return jsonify(csv_file.to_dictlist())
    pp.pprint(csv_file.to_dictlist())
    return ""


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', True)
    app.run(host='0.0.0.0', debug = debug, port=port)

