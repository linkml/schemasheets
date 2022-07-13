# Specification (in progress)

The following is an outline. Please refer to the above examples for elucidation.

## Sheet Structure

 - A sheet is a collection of one or more tables
 - A table is a named list of rows
 - A row is an array of values (cells)
 - A value is a UTF-8 string

_Note_: we follow google terminology here, with a sheet being the encompassing structure, and each containing tabs

Any formatting information (color, font, etc) is ignored

Any individual table is organized into

- Exactly one header row. This MUST be first.
- Zero or more column configuration rows. These MUST come after the header row, and must start with `>`
- Zero or more *element rows*
 
### Header line

The first row in a table is a **header** row.

- Each element of this row is called a column
- Each column must be non-null and unique
- There is always exactly one header row
- The header row must be first
- Each column must be unique

The header row provides an index into subsequent rows

In future, grouping columns may be possible.

### Column Configurations

Any subsequent rows where the first value start with a `>` character are **column configurations**

- A column configuration can be split over multiple lines. Each such subsequent line must start with `>`
- The `>` marks to delimit column configurations, and is subsequently ignored for parsing
- Each line must be a valid yaml string
     - note that a single token is valid yaml for that token
- The first config line must include a *descriptor*
- Subsequent lines are *settings* for that descriptor
- A descriptor can be one of:
   - Any LinkML metamodel slot (e.g. description, comments, range, required, recommended, multivalued)
   - The keyword `cardinality`. See [Cardinality enum](https://linkml.io/schemasheets/datamodel/Cardinality/) in datamodel
   - An element metatype (one of: schema, prefix, class, enum, slot, type, subset, permissible_value)
   - A YAML object whose key is a descriptor and with values representing settings
- Setting can be taken from [the schemasheets datamodel](https://linkml.io/schemasheets/datamodel/)
   - vmap provides a **value mapping** used to translate column values. E.g. a custom "yes" or "no" to "true" or "false"
   - curie_prefix auto-prefixes the value in the cell with a curie prefix
   - inner_key indicates that the column represents a complex/nested object, and the cell value populates that key
   

### Element Rows

Remaining rows are **elements** of your schema

- Each element gets its own row
- A row must represent a unique element, which may be a:
    - class (record, table)
    - field (column)
    - slot usage (a field in the context of a class)
    - enumeration
    - permissible value
    - schema
    - prefix
    - type
    - subset
- If a `metatype` descriptor is used:
    - the type of the row is indicated by the metatype value (one of: class, slot, enum, type, schema)
    - a name field must be  present, this indicates the name of the element
- If a `metatype` descriptor is not used:
    - some combination of class, slot, enum, permissible value schema, type are used to determine the row type plus the name
    - if both class and slot are populated the row is interpreted as `slot_usage` (i.e a field in the context of a class)
    - if only class is populated the row is a class element with name determined by the value of the class column
    - if only slot is populated the row is a slot element with name determined by the value of the slot column
    - if only type is populated the row is a type element with name determined by the value of the type column
    - if only enum is populated the row is a enum element with name determined by the value of the enum column
    - if both enum and permissible_value are populated the row is a permissible value element for that enum
    - permissible_value must not be populated without enum being populated
    - if only schema is populated the row is a schema element with name determined by the value of the schema column
    - schema column may be populated in conjunction with any of the combination above to place the element in a schema
    - all other combinations are forbidden
- All other columns are interpreted according to the column configuration for that column
   - the column configuration includes curie_prefix then the value is prefixed with this value
   - if the column configuration specifies a vmap this is used to map the provided values
   - a column that is mapped to `example` automatically maps to `example.value`
- All sheets/TSVs are combined together into a single LinkML schema as YAML
- This LinkML schema can be translated to other formats as per the LinkML [generators](https://linkml.io/linkml/generators/index.html)


