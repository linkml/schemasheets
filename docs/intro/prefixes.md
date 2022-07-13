# Prefixes

If you specify a column descriptor of `prefix`, then rows with that column
populated will represent prefixes. The prefix expansion is specified using [prefix_reference](https://w3id.org/linkml/prefix_reference) 

## Example

|prefix|URI
|---|---|
|`>` prefix|prefix_reference
|sdo|http://schema.org/
|personinfo|https://w3id.org/linkml/examples/personinfo/
|famrel|https://example.org/FamilialRelations#
|GSSO|http://purl.obolibrary.org/obo/GSSO_|

See:

- the prefixes tab on the [example google sheet](https://docs.google.com/spreadsheets/d/1wVoaiFg47aT9YWNeRfTZ8tYHN8s8PAuDx5i2HUcDpvQ/edit#gid=225448537)
- [tests/input/prefixes.tsv](https://github.com/linkml/schemasheets/blob/main/tests/input/prefixes.tsv) equivalent file in github

## Recommendations

Although prefixes can be combined into one sheet, we recommend you specify prefixes in their own sheet.

## Automatic prefixes

If prefixes are not provided, and you do not specify `--no-repair` then prefixes
will be inferred using [bioregistry](https://bioregistry.io), provided you use common, standard prefixes.

