# Enums

## About

Enumerations can be thought of as "dropdowns" or picklists in data
entry forms. Minimally, the enum is a predefined set of strings. These
strings can optionally be provided with more metadata, such as
descriptions or assignment of controlled vocabulary/ontology terms

## How it works

Two descriptors are provided for enumerations:

- `enum`
- `permissible_value`

These can be used in combination:

- If `enum` is provided, and `permissible_value` is not, then the row represents an enumeration
- If both `enum` and `permissible_value` are provided, the row represents a particular enum value

## Example

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

## More info

For more on enumerations, see [the linkml tutorial](https://linkml.io/linkml/intro/tutorial06.html)
