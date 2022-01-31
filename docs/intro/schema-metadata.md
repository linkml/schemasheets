# Schema-level metadata

If you specify a column descriptor of `schema`, then rows with that column
populated will represent schemas.

Example:

|Schema|uri|Desc|Schema Prefix
|---|---|---|---|
|`>` schema|id|description|default_prefix
|PersonInfo|https://w3id.org/linkml/examples/personinfo|Information about people, based on [schema.org](http://schema.org)|personinfo

The list of potential descriptors for a schema can be found by consulting
[SchemaDefinition](https://w3id.org/linkml/SchemaDefinition) in the LinkML metamodel.

Both `id` and `name` are required, these will be auto-filled if you don't fill this in.

Populating the fields `description` and `license` is strongly encouraged.

Currently multiple schemas are not supported, we recommend providing a single-row sheet for
schema metadata
