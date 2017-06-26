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
pp = pprint.PrettyPrinter(indent=2)
DEFAULT_LANG = "en"
SCHEMA_DIR = "schemas"

app = Flask(__name__, static_url_path = "")

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route("/datatypes", methods=['GET'])
def get_datatypes():

    
    return ""


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', False)
    app.run(host='0.0.0.0', debug = debug, port=port)
