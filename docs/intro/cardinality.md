# Specifying cardinality

## About

Cardinality refers to how many values a particular field is required or allowed to have

## Example

In the following schema, the column heading "multiplicity" is mapped to "cardinality":

|record|field|key|multiplicity|range|desc|schema.org
|---|---|---|---|---|---|---|
|`>` class|slot|identifier|cardinality|range|description|`exact_mappings: {curie_prefix: sdo}`
|-|id|yes|1|string|any identifier|identifier
|-|description|no|0..1|string|a textual description|description
|Person|has medical history|no|0..*|MedicalEvent|medical history|-

Here, the cardinalities state:

* there must be exactly one `id`
* there may be a `description`
* zero to many medical history events

## How it works

See [configschema.yaml](https://github.com/linkml/schemasheets/blob/main/schemasheets/conf/configschema.yaml) for all possible vocabularies, these include:

- UML strings, e.g. '0..1'
- text strings matching the cardinality vocabulary, e.g. 'zero to one'
- codes used in cardinality vocabulary, e.g. O, M, ...

The vocabulary maps to underlying LinkML primitives:

- [required](https://w3id.org/linkml/required)
- [multivalued](https://w3id.org/linkml/multivalued)
- [recommended](https://w3id.org/linkml/recommended)

## Cardinality Vocabulary

* [Cardinality vocabulary](https://linkml.io/schemasheets/datamodel/Cardinality/)
* [yaml](https://github.com/linkml/schemasheets/blob/main/schemasheets/conf/configschema.yaml)

