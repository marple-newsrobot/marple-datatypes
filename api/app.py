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
sys.path.insert(0,'..')
import settings
pp = pprint.PrettyPrinter(indent=2)
# Get from settings, should point to root folder
DATATYPES_DIR = settings.DATATYPES_DIR
DEFAULT_LANG = settings.DEFAULT_LANG
ALL_DOMAINS = Domain("*/*", datatypes_dir=DATATYPES_DIR)
# Points to root folder
RELATIONS_CSV_PATH = settings.RELATIONS_CSV_PATH
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
    lang = get_lang(request.args)
    domain = get_domain(request.url)
    datatype = Datatype(datatype_id, datatypes_dir=DATATYPES_DIR)
    allowed_values = []
    data = {
        "id": datatype_id,
        "allowed_values": []
    }
    # Get lang and domain from request!
    for allowed_value_id in datatype.allowed_values:
        data["allowed_values"].append(jsonify_item(allowed_value_id, lang, domain))
    
    return jsonify(data)

@app.route("/item/<string:item_id>", methods=['GET'])
def get_item(item_id):
    # TODO: Use "**/*" to fetch all files in all subfolders once glob2 in place
    data = ALL_DOMAINS.row(item_id)
    domain = get_domain(request.url)
    lang = get_lang(request.args)
    # This is something of a hack. The Domain class will include a lot of empty columns/propeties defined in other files
    # Here we clean up those
    data = remove_nan(data)

    # Translate label to selected language
    data["label"] = ALL_DOMAINS.label(item_id,lang=lang)

    # Populate relational properties (parent, neighbours etc)
    # These relations are defined in relations.csv in the root folder
    relations_csv = CsvFile(RELATIONS_CSV_PATH)
    # Ie {u'neighbours': u'one_to_many', u'parent': u'one_to_one'}
    relational_columns = dict(relations_csv.data.to_records())

    for column, relation_type in relational_columns.iteritems():
        if column not in data:
            continue
        if relation_type == "one_to_one":
            related_item_id = data[column] # ie the parent id
            data[column] = jsonify_item(related_item_id, lang, domain)
            
        elif relation_type == "one_to_many":
            related_item_ids = data[column].split(",") #ie neighbours
            data[column] = []
            for related_item_id in related_item_ids:
                data[column].append(jsonify_item(related_item_id, lang, domain))

    data["children"] = []             
    for child_id in ALL_DOMAINS.children(item_id):
        data["children"].append(jsonify_item(child_id, lang, domain))

    return jsonify(data)

def remove_nan(obj): 
    """Remove all NaN values
    """
    for key, value in obj.items():
        if isNaN(value):
            obj.pop(key, None)
    return obj

def get_domain(url):
    return "/".join(url.split("/", 3)[:3]) 

def jsonify_item(item_id, lang, domain):
    return {
        "id": item_id,
        "label": ALL_DOMAINS.label(item_id, lang=lang),
        "path": u"{}/item/{}".format(domain, item_id)
    }

def get_lang(req_args):
    if ('lang' in req_args):
        return req_args['lang']
    return DEFAULT_LANG

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', True)
    app.run(host='0.0.0.0', debug = debug, port=port)

