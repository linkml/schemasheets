# Exporting a schema to schemasheets

## Use Case

Sometimes you might want to export from an existing LinkML schema to schemasheets - 
for example to migrate the source of some or part of a schema to sheet-based editing.

The `sheets2linkml` command will convert schemasheet(s) to a LinkML schema

The reverse operation `linkml2sheets` will convert a LinkML schema to schemasheets

## Status

__THIS COMMAND IS ONLY PARTIALLY IMPLEMENTED__ -- not all parts of the specification are considered.
However, you may still find this useful for "bootstrapping" schema sheets

## Usage

Type

```bash
linkml2sheets --help
```

to get complete help

Broadly there are two usage scenarios:

- when you have a single sheet
- when your schema is mapped to multiple sheets (e.g. enums and slots in different sheets)

In both cases you need two inputs

1. A linkml schema, specified in yaml
2. One or more schemasheets that serve as the specification
    - these do not need to have any data
    - they do need the columns used and column descriptors

### Single-sheet usage

Here you pass a single TSV specification on the command line

You can use the `--output` (`-o`) option to write output to a single sheet file.
Or omit this to write on stdout.

### Multi-sheet usage

Here you multiple TSV specifications on the command line

You must use the `--directory` (`-d`) option to specify which directory
the files are written to. The filenames will be the same.

So for example, if you had a folder:

```
sheets/
  enums.tsv
  slots.tsv
```

where:

- each tsv contains minimally the column specifications,
- you pass in `sheets/*tsv` as input
- you pass `--directory output`

Then you will generate a folder:

```
output/
  enums.tsv
  slots.tsv
```

the headers will be the same as the TSVs in the input,
but it will include "data" rows, where each row is a matching
schema element

the input and output directory can be identical, but
you will need to pass in `--overwrite` to explicitly overwrite,
this guards against accidental overwrites.

## Converting between two different schemasheet specs

schemasheets allows *custom* sheet formats that map to the LinkML standard.

you can use the combination of sheets2linkml and linkml2sheets to convert between two sheet specifications.

For example, let's say for schema1.tsv, you use a spreadsheet with the following headers:

- record: `> class`
- field: `> slot`
- cardinality: `> cardinality`
- info: `> description`

and for schema2.tsv you have:

- table: `> class`
- attribute: `> slot`
- required: `> required`
- multivalued: `> multivalued`
- description: `> description`

(here each list element is a column, and the part after the `>` is the 2nd row)

If you do:

```bash
sheets2linkml schema1.tsv > schema1.yaml
linkml2sheets -s schema1.yaml schema2.tsv > schema2_full.tsv
```

then this will effectively map schema1.tsv onto the format for schema2.tsv.
And you can swap the arguments to go in the reverse direction.
