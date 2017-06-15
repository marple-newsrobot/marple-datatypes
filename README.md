[![Build Status](https://travis-ci.org/marple-newsrobot/marple-datatypes.svg?branch=master)](https://travis-ci.org/marple-newsrobot/marple-datatypes)

# Marple Datatypes
This repo contains:

* **datatype descriptions**, for use with e.g. data validators
* **value types** used by both the datatype descriptions, and the dataset metadata

All datatypes are listed in `datatypes.csv`. Value types are in subfolders, organized by domain.

## Data types (datatypes.csv)
`datatypes.csv` contains column names that can be used by datasets, and their value type and a description.

Each data type can have one of the following value types:

* `int` – a value that can be parsed by Python as an integer 
* `float` – a value that can be parsed by Python as a floating-point number
* `str` – a value that can be parsed by Python as a string. This value type is typically accompanied by a set of allowed values. Empty strings are considered null.
* `date` - a ISO 8601 date, e.g. `2016-07-05`, `2016-07-05T13:00:00`, `2016-W27`, or `1981-04`.

## Allowed values
Some data types, and some metadata fields, have a predefined set of allowed values (such as “regions”). In some domains, allowed values may be organized in categories (such as “municipalities”, “counties”).

Allowed values are specified in csv files, structured in folders by domain, e.g.`regions/municipalities.csv`. They are referenced in `datatypes.csv` and `/datasets` like this: `regions/municipalities`, and `regions/*`. Value types with no categorization is collected in `misc/`, such as gender, with four possible values (`male`, `female`, `other`, `unknown`) in `misc/genders.csv`

The allowed values csv's may contain additional identifiers, such as WikiData codes, or start/end dates, that might be useful for a validator.

## Relations

Datatype csv-files can have so called relational columns. Relational columns can define for example parent categories and neighbours. A relational column must contain in id of another entity in `marple-datatypes`.

There are two types of relations:

* `one_to_one`: For example "parent"
* `one_to_many`: For example neighbours. Expects a comma separated list of id's.

Which columns that are interpreted as relational are defined in `relations.csv`.

