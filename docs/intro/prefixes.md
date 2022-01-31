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

## Recommendations

We recommend you specify prefixes in their own sheet.

## Automatic prefixes

If prefixes are not provided, and you do not specify `--no-repair` then prefixes
will be inferred using [bioregistry](https://bioregistry.io)

