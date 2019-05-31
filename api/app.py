# encoding: utf-8
from flask import Flask, jsonify, abort, request, make_response, url_for
from marple.datatypes import Domain, Datatype
from marple.csv import CsvFile
from marple.utils import isNaN, parse_lingual_object
import csvkit as csv
import os
import json
import numpy as np
from settings import DATATYPES_DIR, DEFAULT_LANG, RELATIONS_CSV_PATH

ALL_DOMAINS = Domain("**/*", datatypes_dir=DATATYPES_DIR)
ALLOWED_LANGUAGES = ["en","sv"]

app = Flask(__name__, static_url_path = "")

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route("/", methods=['GET'])
def index():
    """Entry point."""
    lang = get_lang(request.args)
    domain = get_domain(request.url)
    return jsonify({
        "endpoints": [
            {
                "id": "datatype",
                "description": "Get all datatypes",
                "path": domain + "/datatype",
            }
        ]
        })

@app.route("/datatype", methods=['GET'])
def get_all_datatypes():
    """List all datatypes."""
    lang = get_lang(request.args)
    data = []
    file_path = os.path.join(DATATYPES_DIR, "datatypes.csv")
    csv_file = CsvFile(file_path)
    items = csv_file.to_dictlist()

    for item in items:
        item_data = {
            "id": item["id"],
            "label": parse_lingual_object(item, lang=lang, prefix="label"),
            "path": "{}/datatype/{}?lang={}"\
                .format(get_domain(request.url), item['id'], lang)
        }
        data.append(item_data)

    return jsonify(data)


@app.route("/datatype/<string:datatype_id>", methods=['GET'])
def get_datatype(datatype_id):
    """Get a datatype by id."""
    lang = get_lang(request.args)
    domain = get_domain(request.url)
    try:
        datatype = Datatype(datatype_id, datatypes_dir=DATATYPES_DIR, lang=lang)
    except ValueError:
        # Throw 404 error if datatype is missing
        abort(404)

    allowed_values = []
    data = {
        "id": datatype_id,
        "label": datatype.label,
        "allowed_values": [],
    }

    for allowed_value_id in datatype.allowed_values:
        # Make list of allowed values with ids, labels and paths
        item = jsonify_item(allowed_value_id, lang, domain)
        data["allowed_values"].append(item)

    return jsonify(data)


@app.route("/item/<string:item_id>", methods=['GET'])
def get_item(item_id):
    """ Get an item by id.
    {
        "id": "my_item",
        "label": "My item",
        "data": {
            # Raw data from the csv file
            "region_level": "nation",
            "custom_data": "my_custom_data"
        },
        "children": [],
    }
    """
    try:
        data = ALL_DOMAINS.row(item_id)
    except KeyError:
        abort(404)

    domain = get_domain(request.url)
    lang = get_lang(request.args)
    # Clean null values that come from file merge
    data = remove_nan(data)

    # Start building the object to return here
    item_data = {
        "id": item_id,
        "label": ALL_DOMAINS.label(item_id, lang=lang),
        "data": {},
    }

    # Add all cell values to data property
    for key, value in data.iteritems():
        if key not in item_data:
            item_data["data"][key] = value

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
            item_data[column] = jsonify_item(related_item_id, lang, domain)

        elif relation_type == "one_to_many":
            related_item_ids = data[column].split(",") #ie neighbours
            item_data[column] = []
            for related_item_id in related_item_ids:
                item = jsonify_item(related_item_id, lang, domain)
                item_data[column].append(item)

    item_data["children"] = []
    for child_id in ALL_DOMAINS.children(item_id):
        item = jsonify_item(child_id, lang, domain)
        item_data["children"].append(item)

    return jsonify(item_data)

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
    item = {
        "id": item_id,
        "label": ALL_DOMAINS.label(item_id, lang=lang),
        "path": u"{}/item/{}?lang={}".format(domain, item_id,lang)
    }
    for key, value in ALL_DOMAINS.row(item_id).iteritems():
        if key in item:
            continue
        if isNaN(value):
            continue
        item[key] = value

    return item



def get_lang(req_args):
    """ Get languge from request
    """
    if 'lang' in req_args:
        lang = req_args["lang"]
        if lang not in ALLOWED_LANGUAGES:
            return DEFAULT_LANG

        return lang
    return DEFAULT_LANG

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', False)
    app.run(host='0.0.0.0', debug = debug, port=port)
