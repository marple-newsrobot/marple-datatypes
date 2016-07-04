# Marple Datatypes
This repo contains data type descriptions, for use with e.g. data validators, and metadata about data sets. They are listed in two CSV files: `datasets.csv` and `datatypes.csv`.

## Metadata
`datasets.csv` contains all available datasets, and metadata such as source (e.g. “AMS”), measure types (e.g. “relative”), periodicity (e.g. “quarterly”), etc.

### Columns of datasets.csv
The layout of `datasets.csv` WILL be subject to frequent changes. Do not rely on any column name being there. 

Column name (**example**)

* Name (**SE-7-unemployment-monthly**)
* Source (**AMS**)
* Periodicity (**monthly**)
* Geographic extent (**sweden**)
* Measure (**absolute**)
* Division (**regions/municipalities**)
* Description

## Data types
`datatypes.csv` contains column names that can be used by datasets, and their allowed values, and other characteristics.

Each data type can have one of the following value types:

* `int` – a value that can be parsed by Python as an integer 
* `float` – a value that can be parsed by Python as a floating-point number
* `str` – a value that can be parsed by Python as a string. These data types MUST specify a set of allowed values. Empty strings are considered null.


## Allowed values
Some data types, and some metadata fields, have a predefined set of allowed values (such as regions). Values of one domain may be organized in categories (such as “municipalities”, “counties”).

Allowed values are specified in csv files, structured in folders by domain (value type). `Region` is a value type, with a predefined set of allowed values. These values can belong to different categories: `municipality`, `county`, or `nation`. They are described by the following files:

    regions/municipalities.csv
    regions/counties.csv
    regions/nations.csv

They are referenced in `datatypes.csv` like this: `regions/municipalities`, and `regions/`. Value types with no categorization is collected in `misc/`, such as gender, with four possible values (`male`, `female`, `other`, `unknown`) in `misc/genders.csv`

The allowed values csv's may contain additional identifiers, such as WikiData codes, or start/end dates.