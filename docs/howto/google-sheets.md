# Google sheets

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

## Example

TODO
