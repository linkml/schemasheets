# Specification (in progress)

The following is an outline. Please refer to the above examples for elucidation.

## Sheet Structure

A sheet is conceptualized as a collection of rows, which is an array of values (cells). Any formatting information is ignored.

Any individual sheet is organized into

- A header row
- Zero or more column configuration rows
- One or more element rows

### Header line

The first row is a **header** row.

- Each column must be non-null and unique
- In future grouping columns may be possible
- There is always exactly one header row
- The header row must be first
- Each value must be unique
- The header row provides an index into subsequent rows

### Column Configurations

Any subsequent rows where the first value start with a `>` character are **column configurations**

- A column configuration can be split over multiple lines
- Each line must be a valid yaml string (note that a single token is valid yaml for that token)
- The first config line must include a *descriptor*
- Subsequent lines are *settings* for that descriptor
- A descriptor can be one of:
   - Any LinkML metamodel slot (e.g. description, comments, range, required, recommended, multivalued)
   - The keyword `cardinality`. See [Cardinality enum](../datamodel/Cardinality/) in datamodel
   - An element metatype (schema, prefix, class, enum, slot, type, subset, permissible_value)
- Setting can be taken from configschema.yaml
   - vmap provides a mapping used to translate column values. E.g. a custom "yes" or "no" to "true" or "false"
   - various keys provide ways to auto-prefix or manipulate strings

### Element Rows

Remaining rows are **elements** of your schema

- Each element gets its own row
- A row can represent a class (record, table), field (column), enumeration, or other element types
- The type of the row is indicated by whether columns with metatype descriptors are filled
   - E.g. if a column header "field" has a descriptor "slot" then any row with a non-null value is interpreted as a slot
- If a `metatype` descriptor is present then this is used
- A row must represent exactly one element type
- If both class and slot descriptors are present then the row is interpreted as a slot in the context of that class (see slot_usage)
- All sheets/TSVs are combined together into a single LinkML schema as YAML
- This LinkML schema can be translated to other formats as per the LinkML [generators](https://linkml.io/linkml/generators/index.html)

## Translating sheets to LinkML
