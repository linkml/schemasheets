
# Enum: Shortcuts


A vocabulary of permissible values as column descriptors that do not have an exact equivalent in the LinkML datamodel,
and instead act as shortcuts to either a collection of elements or a type of mapping behavior

URI: [schemasheets:Shortcuts](https://w3id.org/linkml/configschema/Shortcuts)


## Other properties

|  |  |  |
| --- | --- | --- |

## Permissible Values

| Text | Description | Meaning | Other Information |
| :--- | :---: | :---: | ---: |
| cardinality | The column is used to describe the cardinality of a slot, with values from the Cardinality enum |  |  |
| ignore | The column is ignored |  |  |
| metatype | The column describes what kind of element is specified in the row |  |  |
| class | The column is populated with class names | linkml:ClassDefinition |  |
| slot | The column is populated with slot names | linkml:SlotDefinition |  |
| enum | The column is populated with enum names | linkml:EnumDefinition |  |
| schema | The column is populated with schema names | linkml:EnumDefinition |  |
| subset | The column is populated with subset names | linkml:EnumDefinition |  |

