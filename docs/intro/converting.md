# Generating schemas

Although you can use schemasheets without writing any code, some
technical expertise is still required to run scripts to generate
schema *artefacts* from sheets, and to use these.

## Generating a Project

Assuming your schema is arranged as a set of sheets (TSV files) in the `src` folder:

```bash
sheets2project -d . src/*.tsv
```

This will generate individual folders for jsonschema, shacl, ... as well as
a website that can be easily hosted on github.

## Generating a LinkML schema

To create *only* LinkML yaml:

```bash
sheets2linkml -o my.yaml  src/*.tsv
```

