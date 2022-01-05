# schemasheets - structuring your data using spreadsheets

Create a data dictionary / schema for your data using simple spreadsheets - no coding required.

- Author your schema as a google sheet or excel spreadsheet
- [Generate schemas](https://linkml.io/linkml/generators/index.html):
   - LinkML
   - SHACL and ShEx
   - JSON-Schema
   - SQL DDL
   - OWL
- Validate data automatically

See the [test google sheets](https://docs.google.com/spreadsheets/d/1wVoaiFg47aT9YWNeRfTZ8tYHN8s8PAuDx5i2HUcDpvQ/edit#gid=55566104) for examples

See also the [examples](examples) folder which has an end-to-end example

## How it works

The following example shows a schema sheet for a schema that is focused around
the concept of a Person. The rows in the sheet describe either *classes* or *slots* (fields)

|record|field|key|multiplicity|range|desc|schema.org
|---|---|---|---|---|---|---|
|`>` class|slot|identifier|cardinality|range|description|`exact_mappings: {curie_prefix: sdo}`
|-|id|yes|1|string|any identifier|identifier
|-|description|no|0..1|string|a textual description|description
|Person||n/a|n/a|n/a|a person,living or dead|Person
|Person|id|yes|1|string|identifier for a person|identifier
|Person, Organization|name|no|1|string|full name|name
|Person|age|no|0..1|decimal|age in years|-
|Person|gender|no|0..1|decimal|age in years|-
|Person|has medical history|no|0..*|MedicalEvent|medical history|-
|MedicalEvent||n/a|n/a|n/a|-|-

 * [personinfo google sheet](https://docs.google.com/spreadsheets/d/1wVoaiFg47aT9YWNeRfTZ8tYHN8s8PAuDx5i2HUcDpvQ/edit#gid=55566104)

The sheet is structured as follows:

- The first line is a header line. You get to decide the column headers
- Subsequent lines starting with `>` are *column descriptors*
   - these provide a way to interpret the columns
   - descriptors can be drawn from the [linkml](https://linkml.io) vocabulary
- Remaining rows are elements of your schema
   - Each element gets its own row
   - A row can represent a class (record, table), field (column), enumeration, or other element types

The most basic schema concepts are *classes* and *slots*

- classes represent record types, similar to tables in a database or sheets in a spreadsheet
- slots represent fields, similar to columns in a database or spreadsheet 

These can be used in combination:

- If a *class* is provided, but a *slot* is not, then the row represents a class. 
- If a *slot* is provided, but a *class* is not, then the row represents a slot (field)
- If both *class* and *slot* are provided, then the row represents the *usage* of a slot in the context of a class


### Generating schemas

Assuming your schema is arranged as a set of sheets (TSV files) in the `src` folder:

```bash
sheets2project -d . src/*.tsv
```

This will generate individual folders for jsonschema, shacl, ... as well as
a website that can be easily hosted on github.

To create only LinkML yaml:

```bash
schemasheets -o my.yaml  src/*.tsv
```


## Simple data dictionaries

This framework allows you to represent complex relation-style schemas
using spreadsheets/TSVs. But it also allows for representation of simple "data dictionaries" or "minimal information lists".
These can be thought of as "wide tables", e.g. representing individual observations or observable units such as persons or samples.

TODO


## Prefixes

If you specify a column descriptor of `prefix`, then rows with that column
populated will represent prefixes. The prefix expansion is specified using [prefix_reference](https://w3id.org/linkml/prefix_reference) 

Example:

|prefix|URI
|---|---|
|`>` prefix|prefix_reference
|sdo|http://schema.org/
|personinfo|https://w3id.org/linkml/examples/personinfo/
|famrel|https://example.org/FamilialRelations#
|GSSO|http://purl.obolibrary.org/obo/GSSO_|

We recommend you specify prefixes in their own sheet.

If prefixes are not provided, and you do not specify `--no-repair` then prefixes
will be inferred using [bioregistry](https://bioregistry.io)

## Schema-level metadata

If you specify a column descriptor of `schema`, then rows with that column
populated will represent schemas.

Example:

|Schema|uri|Desc|Schema Prefix
|---|---|---|---|
|`>` schema|id|description|default_prefix
|PersonInfo|https://w3id.org/linkml/examples/personinfo|Information about people, based on [schema.org](http://schema.org)|personinfo

The list of potential descriptors for a schema can be found by consulting
[SchemaDefinition](https://w3id.org/linkml/SchemaDefinition) in the LinkML metamodel.

Both `id` and `name` are required, these will be auto-filled if you don't fill this in.

Populating the fields `description` and `license` is strongly encouraged.

Currently multiple schemas are not supported, we recommend providing a single-row sheet for
schema metadata

## Enums

Two descriptors are provided for enumerations:

- `enum`
- `permissible_value`

These can be used in combination:

- If `enum` is provided, and `permissible_value` is not, then the row represents an enumeration
- If both `enum` and `permissible_value` are provided, the row represents a particular enum value

The following example includes two enums:

|ValueSet|Value|Mapping|Desc
|---|---|---|---|
|`>` enum|permissible_value|meaning|description
|FamilialRelationshipType|-|-|familial relationships
|FamilialRelationshipType|SIBLING_OF|famrel:01|share the same parent
|FamilialRelationshipType|PARENT_OF|famrel:02|biological parent
|FamilialRelationshipType|CHILD_OF|famrel:03|inverse of parent
|GenderType|-|-|gender
|GenderType|nonbinary man|GSSO:009254|-
|GenderType|nonbinary woman|GSSO:009253|-
|...|...|...|-

 * [enums google sheet](https://docs.google.com/spreadsheets/d/1wVoaiFg47aT9YWNeRfTZ8tYHN8s8PAuDx5i2HUcDpvQ/edit#gid=823426713)
 
All other descriptors are optional, but we recommend you provide descriptions of
both the enumeration and the [meaning](https://w3id.org/linkml/meaning) descriptor which
maps the value to a vocabulary or ontology term.

For more on enumerations, see [the linkml tutorial](https://linkml.io/linkml/intro/tutorial06.html)

## Specifying cardinality

See configschema.yaml for all possible vocabularies, these include:

- UML strings, e.g. '0..1'
- text strings matching the cardinality vocabulary, e.g. 'zero to one'
- codes used in cardinality vocabulary, e.g. O, M, ...

The vocabulary maps to underlying LinkML primitives:

- [required](https://w3id.org/linkml/required)
- [multivalued](https://w3id.org/linkml/multivalued)
- [recommended](https://w3id.org/linkml/recommended)

## Slot-class grids

If you have a large number of fields/columns, with varying applicability/cardinality
across different classes, it can be convenient to specify this as a grid.

An example is a minimal information standard that includes different packages or checklists, e.g. MIxS.

For example:

|term|title|desc|mi_patient|mi_mod|mi_terrestrial|mi_marine|mi_extraterrestrial|
|---|---|---|---|---|---|---|---|
|`>` slot|title|description|cardinality|cardinality|cardinality|cardinality|cardinality|
|`>`|||`applies_to_class: MI patient`|`applies_to_class: MI model organism`|`applies_to_class: MI terrestrial sample`|`applies_to_class: MI marine sample`|`applies_to_class: MI extraterrestrial sample`|
|id|unique identifier|a unique id|M|M|M|M|M|
|alt_ids|other identifiers|any other identifiers|O|O|O|O|O|
|body_site|body site|location where sample is taken from|M|R|-|-|-|
|disease|disease status|disease the patient had|M|O|-|-|-|
|age|age|age|M|R|-|-|-|
|depth|depth|depth in ground or water|-|-|R|R|R|
|alt|altitude|height above sea level|||R|R|R|
|salinity|salinity|salinity|||R|R|R|
|porosity|porosity|porosity||||||
|location|location|location on earth||||||
|astronomical_body|astronomical body|planet or other astronomical object where sample was collected|||||M|

 * [data dictionary google sheet](https://docs.google.com/spreadsheets/d/1wVoaiFg47aT9YWNeRfTZ8tYHN8s8PAuDx5i2HUcDpvQ/edit#gid=1290069715)

Here the `applies_to_class` descriptor indicates that the column value for the slot indicated in the row
is interpreted as slot usage for that class. 

## Metatype fields

In all of the examples above, distinct descriptors are used for class names, slot names, type names, enum names, etc

An alternative pattern is to mix element types in a single sheet, indicate the name of the element using `name` and the type using `metatype`.

For example:

|type|item|applies to|key|multiplicity|range|parents|desc|schema.org|wikidata|belongs|status|notes|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|`>` metatype|name|class|identifier|cardinality|range|is_a|description|`exact_mappings: {curie_prefix: sdo}`|`exact_mappings: {curie_prefix: wikidata}`|in_subset|status|ignore|
|`> vmap: {C: class, F: slot}`|||||||||||||
|`>`|||||||||curie_prefix: wikidata||`vmap: {T: testing, R: release}`||
|F|id||yes|1|string||any identifier|identifier|||||
|F|name|Person, Organization|no|1|string||full name|name|||||
|F|description||no|0..1|string||a textual description|description|||||
|F|age|Person|no|0..1|decimal||age in years||||||
|F|gender|Person|no|0..1|decimal||age in years||||||
|F|has medical history|Person|no|0..*|MedicalEvent||medical history||||T||
|C|Person||||||a person,living or dead|Person|Q215627||R||
|C|Event||||||grouping class for events||Q1656682|a|R||
|C|MedicalEvent|||||Event|a medical encounter|||b|T||
|C|ForProfit|||||Organization|||||||
|C|NonProfit|||||Organization|||Q163740|||foo|

 * [personinfo with tyoes](https://docs.google.com/spreadsheets/d/1wVoaiFg47aT9YWNeRfTZ8tYHN8s8PAuDx5i2HUcDpvQ/edit#gid=509198484)

# Formal specification

In progress. The following is a sketch. Please refer to the above examples for elucidation.

- The first line is a HEADER line.
   - Each column must be non-null and unique
   - In future grouping columns may be possible
- Subsequent lines starting with `>` are *column configurations*
   - A column configuration can be split over multiple lines
   - Each line must be a valid yaml string (note that a single token is valid yaml for that token)
   - The first config line must include a *descriptor*
   - Subsequent lines are *settings* for that descriptor
   - A descriptor can be one of:
      - Any LinkML metamodel slot (e.g. description, comments, required, recommended, multivalued)
      - The keyword `cardinality`
      - An element metatype (schema, prefix, class, enum, slot, type, subset, permissible_value)
   - Setting can be taken from configschema.yaml
      - vmap provides a mapping used to translate column values. E.g. a custom "yes" or "no" to "true" or "false"
      - various keys provide ways to auto-prefix or manipulate strings
- Remaining rows are elements of your schema
   - Each element gets its own row
   - A row can represent a class (record, table), field (column), enumeration, or other element types
   - The type of the row is indicated by whether columns with metatype descriptors are filled
      - E.g. if a column header "field" has a descriptor "slot" then any row with a non-null value is interpreted as a slot
   - If a `metatype` descriptor is present then this is used
   - A row must represent exactly one element type
   - If both class and slot descriptors are present then the row is interpreted as a slot in the context of that class (see slot_usage)
- All sheets/TSVs are combined together into a single LinkML schema as YAML
- This LinkML schema can be translated to other formats as per the LinkML [generators](https://linkml.io/linkml/generators/index.html)

# Working with files / google sheets

This tool takes as input a collection of sheets, which are
stored as TSV files.

You can make use of various ways of managing/organizing these:

- TSVs files maintained in GitHub
- Google sheets
- Excel spreadsheets
- SQLite databases

Tips for each of these and for organizing your information are provided below

## Multiple sheets vs single sheets

It is up to you whether you represent your schema as a single sheet or as multiple sheets

However, if your schema includes a mixture of different element types, you may end up with
a lot of null values if you have a single sheet. It can be more intuitive to "normalize" your schema
description into different sheets:

- sheets for classes/slots
- sheets for enums
- sheets for types

Currently schemasheets has no built in facilities for interacting directly with google sheets - it is up to you to both download and upload these

TODO: scripts for merging/splitting sheets

## Manual upload/download

Note that you can create a URL from a google sheet to the TSV download - TODO

## COGS

We recommend the COGS framework for working with google sheets

- [cogs](https://github.com/ontodev/cogs)

A common pattern is a single sheet document for a schema, with
different sheets/tabs for different parts of the schema

TODO: example

# Working with Excel spreadsheets

Currently no direct support, it is up to you to load/save as individual TSVs

# Working with SQLite

