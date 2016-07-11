# Marple Datatypes
This repo contains:

* **datatype descriptions**, for use with e.g. data validators
* **metadata about datasets**
* **value types** used by both the datatype descriptions, and the dataset metadata

All datatypes are listed in `datatypes.csv`. All datasets are listed in in the subfolders of  `/datasets`, together with a schema. Value types are in subfolders, organized by domain.

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

## Metadata (datasets)
`/datasets` contains all available datasets, and metadata such as source (e.g. “AMS”), measure types (e.g. “rate”), periodicity (e.g. “quarterly”), etc.

Every endpoint (end folder) contains a `datasets.csv` that lists available datasets of that domain. The folder path + the value of the id column in `datasets.csv` constitutes the id of the dataset. For example `AMS/unemployment/by_month/count/youth` is the id of the monthly youth unemployment dataset.

The root folder contains a `schema.csv` file that defines the available metadata of each dataset. The schema applies to all datasets in subfolders. Subfolders can also contain `schema.csv` files. These schemas are treated as extensions of the base schema.

The layout of `/datasets` WILL be subject to frequent changes. Do not rely on any key being there. 
