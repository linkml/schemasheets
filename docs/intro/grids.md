# Overriding fields

## Use Case

Previously we saw example of how to define fields (slots). The
characteristics of these fields remained the same even if they were
used with different classes

If you have a large number of fields/columns, with varying applicability/cardinality
across different classes, it can be convenient to specify this as a grid.

## Example

An example is a minimal information standard that includes different
packages or checklists, e.g. MIxS. Here we may want a slot such as
"soil sample depth" to be mandatory for soil samples, optional for
other kinds of samples.

Example sheet:

|term|title|desc|mi_patient|mi_mod|mi_terrestrial|mi_marine|mi_extraterrestrial|
|---|---|---|---|---|---|---|---|
|`>` slot|title|description|cardinality|cardinality|cardinality|cardinality|cardinality|
|`>`|||`applies_to_class: MI patient`|`applies_to_class: MI model organism`|`applies_to_class: MI terrestrial sample`|`applies_to_class: MI marine sample`|`applies_to_class: MI extraterrestrial sample`|
|id|unique identifier|a unique id|M|M|M|M|M|
|alt_ids|other identifiers|any other identifiers|O|O|O|O|O|
|body_site|body site|location where sample is taken from|M|R|-|-|-|
|disease|disease status|disease the patient had|M|O|-|-|-|
|age|age|age|M|R|-|-|-|
|depth|depth|depth in ground or water|-|-|R|R|R|
|alt|altitude|height above sea level|||R|R|R|
|salinity|salinity|salinity|||R|R|R|
|porosity|porosity|porosity||||||
|location|location|location on earth||||||
|astronomical_body|astronomical body|planet or other astronomical object where sample was collected|||||M|

 * [data dictionary google sheet](https://docs.google.com/spreadsheets/d/1wVoaiFg47aT9YWNeRfTZ8tYHN8s8PAuDx5i2HUcDpvQ/edit#gid=1290069715)

Here the `applies_to_class` descriptor indicates that the column value for the slot indicated in the row
is interpreted as slot usage for that class. 

## More information

See [slot usage](https://linkml.io/linkml/intro/tutorial07.html#customizing-slots-in-the-context-of-classes-slot-usage)
