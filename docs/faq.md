# FAQ

## How can I get more help?

The best way to get help is to ask [on the github issue tracker](https://github.com/linkml/schemasheets/issues)

## Is there a specification?

Schemasheets has its own specification:

- [https://linkml.io/schemasheets/specification/](https://linkml.io/schemasheets/specification/)

This is separate from the main LinkML specification

## Where do I ask questions about LinkML?

See the [LinkML FAQ](https://linkml.io/linkml/faq/index.html)

## Why would I want to use schemasheets?

Schemasheets are designed for easy, efficient and rapid collection of metadata elements and column headers for wide-table data

- Lists of column headers/metadata elements and their associated information are easily managed
- Enumerations can be explicitly provided - and mapped to ontologies
- A flexible approach allows for schemas to be broken out over different sheets in different ways

## When should I *not* use schemasheets?

Schemasheets works best for wide-table data, or "tidy" data, in which any individual observation or data point can have many variables or metadata elements associated with them

If your data follows higher "normal forms" or is narrow then you may be better authoring directly in LinkML yaml.

Schemasheets also works best when you want to involve non-technical people is modeling decisions and in definitions of metadata elements. Most domain experts are comfortable looking at lists of things in spreadsheets.

If your modeling team is quite technical, we recommend authoring your schema directly in LinkML YAML

## Can I use schemasheets to make JSON-Schema?

Why, yes you can!

You can chain together `sheets2linkml` and `gen-json-schema` - or use `sheets2project`

Note that of course if your JSON is highly nested, then it may not make sense to manage the schema in a spreadsheet-like form.
Schemasheets works best for "wide-table" data

## Can I use schemasheets to make SHACL Shape Schemas?

Indeed, you certainly can!

You can chain together `sheets2linkml` and `gen-shacl` - or use `sheets2project`

Note that of course if your RDF is highly relational, then it may not make sense to manage the schema in a spreadsheet-like form.
Schemasheets works best for "wide-table" data

## Can I use schemasheets to make SQL DDL?

I'm glad you asked, this is indeed possible

You can chain together `sheets2linkml` and `gen-sqlddl` - or use `sheets2project`

## Can I make a nice looking website for my schema?

Definitely!

You can chain together `sheets2linkml` and `gen-doc` - or use `sheets2project`

This will make a static site ready for publishing on GitHub!







