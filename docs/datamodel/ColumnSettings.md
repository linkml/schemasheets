
# Class: ColumnSettings


configuration for an individual column in a schema sheet.

These settings are typically specified as YAML blocks beneath
the relevant column header, for example:

```
> class
```

URI: [schemasheets:ColumnSettings](https://w3id.org/linkml/configschema/ColumnSettings)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[ValueMap],[ValueMap]<vmap%200..*-++[ColumnSettings&#124;curie_prefix:string%20%3F;prefix:string%20%3F;suffix:string%20%3F;template:string%20%3F;applies_to_class:ElementReference%20%3F;applies_to_slot:ElementReference%20%3F;tag:string%20%3F])](https://yuml.me/diagram/nofunky;dir:TB/class/[ValueMap],[ValueMap]<vmap%200..*-++[ColumnSettings&#124;curie_prefix:string%20%3F;prefix:string%20%3F;suffix:string%20%3F;template:string%20%3F;applies_to_class:ElementReference%20%3F;applies_to_slot:ElementReference%20%3F;tag:string%20%3F])

## Attributes


### Own

 * [➞curie_prefix](columnSettings__curie_prefix.md)  <sub>0..1</sub>
     * Description: CURIE prefix prepended to column value. This may be used for column that describe mapping or class/slot uri properties of the element. For example, with column settings `exact_mapping: {curie_prefix: dcterms}`, an element row with column value `contributor`, the value will be transformed to `dcterms:contributor`
     * Range: [String](types/String.md)
 * [➞prefix](columnSettings__prefix.md)  <sub>0..1</sub>
     * Description: string to be prefixed onto the column value
     * Range: [String](types/String.md)
 * [➞suffix](columnSettings__suffix.md)  <sub>0..1</sub>
     * Description: string to be suffixied onto the column value
     * Range: [String](types/String.md)
 * [➞template](columnSettings__template.md)  <sub>0..1</sub>
     * Description: jinja templated format string
     * Range: [String](types/String.md)
 * [➞vmap](columnSettings__vmap.md)  <sub>0..\*</sub>
     * Description: Specifies a mapping for column values
     * Range: [ValueMap](ValueMap.md)
 * [➞applies_to_class](columnSettings__applies_to_class.md)  <sub>0..1</sub>
     * Description: if a value C is specified, then this column in the relevant row is interpreted as
pertaining to C
     * Range: [ElementReference](types/ElementReference.md)
 * [➞applies_to_slot](columnSettings__applies_to_slot.md)  <sub>0..1</sub>
     * Range: [ElementReference](types/ElementReference.md)
 * [➞tag](columnSettings__tag.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
