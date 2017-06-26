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
SCHEMA_DIR = "schemas"
# Get from settings, should point to root folder
DATATYPES_DIR = ".."
# Get from request
LANG = "en"
# Get from request
DOMAIN = "http://marple-datatypes.herokuapp.com"
ALL_DOMAINS = Domain("*/*", datatypes_dir=DATATYPES_DIR)
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
def get_all_datatypes():
    data = []
    file_path = os.path.join(DATATYPES_DIR, "datatypes.csv")
    csv_file = CsvFile(file_path)
    # TODO: Add path
    items = csv_file.to_dictlist()
    return jsonify(items)

@app.route("/datatype/<string:datatype_id>", methods=['GET'])
def get_datatype(datatype_id):
    
    datatype = Datatype(datatype_id, datatypes_dir=DATATYPES_DIR)
    print(datatype)
    allowed_values = []
    data = {
        "id": datatype_id,
        "allowed_values": []
    }
    # Get lang and domain from request!
    for allowed_value_id in datatype.allowed_values:
        data["allowed_values"].append(jsonify_item(allowed_value_id, LANG, DOMAIN))
    
    return jsonify(data)



def jsonify_item(item_id, lang, domain):
    return {
        "id": item_id,
        "label": ALL_DOMAINS.label(item_id, lang=lang),
        "path": u"{}/item/{}".format(domain, item_id)
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', True)
    app.run(host='0.0.0.0', debug = debug, port=port)

