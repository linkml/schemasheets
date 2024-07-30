# Schemasheets - make datamodels using spreadsheets

<p align="center">
    <a href="https://github.com/linkml/schemasheets/actions/workflows/main.yml">
        <img alt="Tests" src="https://github.com/linkml/schemasheets/actions/workflows/main.yaml/badge.svg" />
    </a>
    <a href="https://pypi.org/project/linkml">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/linkml" />
    </a>
    <a href="https://pypi.org/project/sssom">
        <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/sssom" />
    </a>
    <a href="https://github.com/linkml/schemasheets/blob/main/LICENSE">
        <img alt="PyPI - License" src="https://img.shields.io/pypi/l/sssom" />
    </a>
    <a href="https://github.com/psf/black">
        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
    </a>
</p>

![linkml logo](https://avatars.githubusercontent.com/u/79337873?s=200&v=4)
![google sheets logo](https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Google_Sheets_logo_%282014-2020%29.svg/175px-Google_Sheets_logo_%282014-2020%29.svg.png)

Create a [data dictionary](https://linkml.io/schemasheets/howto/data-dictionaries/) / schema for your data using simple spreadsheets - *no coding required*.

## About

Schemasheets is a framework for managing your schema using
spreadsheets ([Google Sheets](https://linkml.io/schemasheets/howto/google-sheets/), [Excel](https://linkml.io/schemasheets/howto/excel/)). It works by compiling down to
[LinkML](https://linkml.io), which can itself be compiled to a variety
of formalisms, or used for different purposes like data validation

- [installation](https://linkml.io/schemasheets/install/)
- [basics](https://linkml.io/schemasheets/intro/basics/)

## Documentation

See the [Schema Sheets Manual](https://linkml.io/schemasheets)

## Quick Start

```bash
pip install schemasheets
```

You should then be able to run the following commands:

- sheets2linkml - Convert schemasheets to a LinkML schema
- linkml2sheets - Convert a LinkML schema to schemasheets
- sheets2project - Generate an entire set of schema files (JSON-Schema, SHACL, SQL, ...) from Schemasheets

As an example, take a look at the different tabs in the google sheet with ID [1wVoaiFg47aT9YWNeRfTZ8tYHN8s8PAuDx5i2HUcDpvQ](https://docs.google.com/spreadsheets/d/1wVoaiFg47aT9YWNeRfTZ8tYHN8s8PAuDx5i2HUcDpvQ/edit#gid=55566104)

The personinfo tab contains the bulk of the metadata elements:

|record|field|key|multiplicity|range|desc|schema.org|
|---|---|---|---|---|---|---|
|`>` class|slot|identifier|cardinality|range|description|exact_mappings: {curie_prefix: sdo}|
|`>`|||||||
||id|yes|1|string|any identifier|identifier|
||description|no|0..1|string|a textual description|description|
|Person||n/a|n/a|n/a|a person,living or dead|Person|
|Person|id|yes|1|string|identifier for a person|identifier|
|Person, Organization|name|no|1|string|full name|name|
|Person|age|no|0..1|decimal|age in years||
|Person|gender|no|0..1|decimal|age in years||
|Person|has medical history|no|0..*|MedicalEvent|medical history||
|Event|||||grouping class for events||
|MedicalEvent||n/a|n/a|n/a|a medical encounter||
|ForProfit|||||||
|NonProfit|||||||

This demonstrator schema contains both *record types* (e.g Person, MedicalEvent) as well as *fields* (e.g. id, age, gender)

You can convert this like this:

```bash
sheets2linkml --gsheet-id 1wVoaiFg47aT9YWNeRfTZ8tYHN8s8PAuDx5i2HUcDpvQ personinfo types prefixes -o personinfo.yaml
```

This will generate a LinkML YAML file `personinfo.yaml` from 3 of the tabs in the google sheet

You can also work directly with TSVs:

```
wget https://raw.githubusercontent.com/linkml/schemasheets/main/tests/input/personinfo.tsv 
sheets2linkml personinfo.tsv  -o personinfo.yaml
```

We recommend using [COGS](https://linkml.io/schemasheets/howto/google-sheets/) to synchronize your google sheets with local files using a git-like mechanism

## Examples

- [Person Info Schema](https://docs.google.com/spreadsheets/d/1wVoaiFg47aT9YWNeRfTZ8tYHN8s8PAuDx5i2HUcDpvQ/edit#gid=55566104)
- [Movies Property Graph Schema](https://docs.google.com/spreadsheets/d/1oMrzA41tg_nisdWInnqKJrcvv30dOXuwAhznJYYPSB8/edit?gid=1499822522#gid=1499822522)

## Finding out more

* [Schema Sheets Manual](https://linkml.io/schemasheets)
   * [Specification](https://linkml.io/schemasheets/specification/)
   * [Internal Datamodel](https://linkml.io/schemasheets/datamodel/)
* [linkml/schemasheets](https://github.com/linkml/schemasheets) code repo
* [linkml/linkml](https://github.com/linkml/linkml) main LinkML repo

