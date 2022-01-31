# Basics

Schemasheets allow you to write schemas to manage your data without writing any code. You keep the source for your schema as a spreadsheet (e.g. in google sheets), and convert to LinkML

## Example

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

You can see this example as a google sheet:

 * [personinfo google sheet](https://docs.google.com/spreadsheets/d/1wVoaiFg47aT9YWNeRfTZ8tYHN8s8PAuDx5i2HUcDpvQ/edit#gid=55566104)

The sheet is structured as follows:

## Header Line

The first line is a header line. You get to decide the column headers

|record|field|key|multiplicity|range|desc|schema.org
|---|---|---|---|---|---|---|

## Column Descriptors

- Subsequent lines starting with `>` are *column descriptors*
   - these provide a way to interpret the columns
   - descriptors can be drawn from the [linkml](https://linkml.io) vocabulary

## Schema Elements

Remaining rows are *elements* of your schema

- Each element gets its own row
- A row can represent a class (record, table), field (column), enumeration, or other element types

|record|field|key|multiplicity|range|desc|schema.org
|---|---|---|---|---|---|---|
|`>` class|slot|identifier|cardinality|range|description|`exact_mappings: {curie_prefix: sdo}`

## Core Concepts

The most basic schema concepts are *classes* and *slots*

- classes represent record types, similar to tables in a database or sheets in a spreadsheet
- slots represent fields, similar to columns in a database or spreadsheet 

These can be used in combination:

- If a *class* is provided, but a *slot* is not, then the row represents a class. 
- If a *slot* is provided, but a *class* is not, then the row represents a slot (field)
- If both *class* and *slot* are provided, then the row represents the *usage* of a slot in the context of a class

