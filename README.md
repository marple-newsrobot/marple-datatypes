# Marple Datatypes
This repo contains:

* **datatype descriptions**, for use with e.g. data validators
* **metadata about datasets**
* **value types** used by both the datatype descriptions, and the dataset metadata

All datatypes are listed in `datatypes.csv`. All datasets are listed in `datasets.yaml`, together with a schema. Value types are in subfolders, organized by domain.

## Data types (datatypes.csv)
`datatypes.csv` contains column names that can be used by datasets, and their value type and a description.

Each data type can have one of the following value types:

* `int` – a value that can be parsed by Python as an integer 
* `float` – a value that can be parsed by Python as a floating-point number
* `str` – a value that can be parsed by Python as a string. These data types MUST specify a set of allowed values. Empty strings are considered null.


## Allowed values
Some data types, and some metadata fields, have a predefined set of allowed values (such as “regions”). In some domains, allowed values may be organized in categories (such as “municipalities”, “counties”).

Allowed values are specified in csv files, structured in folders by domain, e.g.`regions/municipalities.csv`. They are referenced in `datatypes.csv` and `datasets.yaml` like this: `regions/municipalities`, and `regions/*`. Value types with no categorization is collected in `misc/`, such as gender, with four possible values (`male`, `female`, `other`, `unknown`) in `misc/genders.csv`

The allowed values csv's may contain additional identifiers, such as WikiData codes, or start/end dates, that might be useful for a validator.

## Metadata (datasets.csv)
`datasets.yamls` contains all available datasets, and metadata such as source (e.g. “AMS”), measure types (e.g. “relative”), periodicity (e.g. “quarterly”), etc.

The layout of `datasets.yaml` WILL be subject to frequent changes. Do not rely on any key being there. See the `schema` key for an overview of currently used keys, and their allowed values.
