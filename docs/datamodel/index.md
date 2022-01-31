
# Schemasheets-Mappings schema


This is the datamodel for Schemasheets Configurations.

Note that for most purposes you will likely not need to consult this.

The key class is [ColumnSettings](ColumnSettings)

Two controlled vocabularies are specified here:

- [Cardinality](Cardinality) - terms and abbreviations that can be used for cardinality
- [Shortcuts](Shortcuts) - species column configurations


### Classes

 * [ColumnSettings](ColumnSettings.md) - configuration for an individual column in a schema sheet.
 * [ValueMap](ValueMap.md) - A key-value dictionary

### Mixins


### Slots

 * [➞applies_to_class](columnSettings__applies_to_class.md) - if a value C is specified, then this column in the relevant row is interpreted as
 * [➞applies_to_slot](columnSettings__applies_to_slot.md)
 * [➞curie_prefix](columnSettings__curie_prefix.md) - CURIE prefix prepended to column value. This may be used for column that describe mapping or class/slot uri properties of the element. For example, with column settings `exact_mapping: {curie_prefix: dcterms}`, an element row with column value `contributor`, the value will be transformed to `dcterms:contributor`
 * [➞prefix](columnSettings__prefix.md) - string to be prefixed onto the column value
 * [➞suffix](columnSettings__suffix.md) - string to be suffixied onto the column value
 * [➞tag](columnSettings__tag.md)
 * [➞template](columnSettings__template.md) - jinja templated format string
 * [➞vmap](columnSettings__vmap.md) - Specifies a mapping for column values
 * [map_key](map_key.md) - key in the dictionary
 * [map_value](map_value.md) - key in the dictionary

### Enums

 * [Cardinality](Cardinality.md) - vocabulary for describing cardinality and applicability of slots or fields.
 * [Shortcuts](Shortcuts.md) - A vocabulary of permissible values as column descriptors that do not have an exact equivalent in the LinkML datamodel,

### Subsets


### Types


#### Built in

 * **Bool**
 * **Decimal**
 * **ElementIdentifier**
 * **NCName**
 * **NodeIdentifier**
 * **URI**
 * **URIorCURIE**
 * **XSDDate**
 * **XSDDateTime**
 * **XSDTime**
 * **float**
 * **int**
 * **str**

#### Defined

 * [ElementReference](types/ElementReference.md)  (**str**)  - A pointer to an element in a datamodel
 * [Boolean](types/Boolean.md)  (**Bool**)  - A binary (true or false) value
 * [Date](types/Date.md)  (**XSDDate**)  - a date (year, month and day) in an idealized calendar
 * [Datetime](types/Datetime.md)  (**XSDDateTime**)  - The combination of a date and time
 * [Decimal](types/Decimal.md)  (**Decimal**)  - A real number with arbitrary precision that conforms to the xsd:decimal specification
 * [Double](types/Double.md)  (**float**)  - A real number that conforms to the xsd:double specification
 * [Float](types/Float.md)  (**float**)  - A real number that conforms to the xsd:float specification
 * [Integer](types/Integer.md)  (**int**)  - An integer
 * [Ncname](types/Ncname.md)  (**NCName**)  - Prefix part of CURIE
 * [Nodeidentifier](types/Nodeidentifier.md)  (**NodeIdentifier**)  - A URI, CURIE or BNODE that represents a node in a model.
 * [Objectidentifier](types/Objectidentifier.md)  (**ElementIdentifier**)  - A URI or CURIE that represents an object in the model.
 * [String](types/String.md)  (**str**)  - A character string
 * [Time](types/Time.md)  (**XSDTime**)  - A time object represents a (local) time of day, independent of any particular day
 * [Uri](types/Uri.md)  (**URI**)  - a complete URI
 * [Uriorcurie](types/Uriorcurie.md)  (**URIorCURIE**)  - a URI or a CURIE
