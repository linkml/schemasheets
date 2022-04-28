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
- If a `metatype` descriptor is used:
    - the type of the row is indicated by the metatype value (one of: class, slot, enum, type, schema)
    - a name field must be  present, this indicates the name of the element
- If a `metatype` descriptor is note used:
    - some combination of class, slot, enum, permissible value schema, type are used to determine the row type plus the name
    - if both class and slot are populated the row is interpreted as `slot_usage`
    - if only class is populated the row is a class element with name determined by the value of the class column
    - if only slot is populated the row is a slot element with name determined by the value of the slot column
    - if only type is populated the row is a type element with name determined by the value of the type column
    - if only enum is populated the row is a enum element with name determined by the value of the enum column
    - if both enum and permissible_value are populated the row is a permissible value element for that enum
    - if permissible_value must not be populated without enum being populated
    - if only schema is populated the row is a scheme element with name determined by the value of the schema column
    - schema column may be populated in conjunction with any of the combination above to place the element in a schema
    - all other combinations are forbidden
- All sheets/TSVs are combined together into a single LinkML schema as YAML
- This LinkML schema can be translated to other formats as per the LinkML [generators](https://linkml.io/linkml/generators/index.html)

## Translating sheets to LinkML
