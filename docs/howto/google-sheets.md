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

## gsheets option

For going from sheets to linkml, you can specify `--gsheet-id`, then each argument becomes the name of a sheet. This automatically downloads each sheet and dynamically transforms.

E.g.

```bash
sheets2linkml --gsheet-id 1wVoaiFg47aT9YWNeRfTZ8tYHN8s8PAuDx5i2HUcDpvQ personinfo types prefixes -o personinfo.yaml
```

## COGS

We recommend the COGS framework for working with google sheets

- [cogs](https://github.com/ontodev/cogs)

A common pattern is a single sheet document for a schema, with
different sheets/tabs for different parts of the schema

