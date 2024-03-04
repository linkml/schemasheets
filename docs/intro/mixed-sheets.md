# Mixed sheets

In all of the examples above, distinct descriptors are used for class names, slot names, type names, enum names, etc

An alternative pattern is to mix element types in a single sheet, indicate the name of the element using `name` and the type using `metatype`.

For example:

|type|item|applies to|key|multiplicity|range|parents|desc|schema.org|wikidata|belongs|status|notes|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|`>` metatype|name|class|identifier|cardinality|range|is_a|description|`exact_mappings: {curie_prefix: sdo}`|`exact_mappings: {curie_prefix: wikidata}`|in_subset|status|ignore|
|`> vmap: {C: class, F: slot}`|||||||||||||
|`>`|||||||||curie_prefix: wikidata||`vmap: {T: testing, R: release}`||
|F|id||yes|1|string||any identifier|identifier|||||
|F|name|Person, Organization|no|1|string||full name|name|||||
|F|description||no|0..1|string||a textual description|description|||||
|F|age|Person|no|0..1|decimal||age in years||||||
|F|gender|Person|no|0..1|decimal||age in years||||||
|F|has medical history|Person|no|0..*|MedicalEvent||medical history||||T||
|C|Person||||||a person,living or dead|Person|Q215627||R||
|C|Event||||||grouping class for events||Q1656682|a|R||
|C|MedicalEvent|||||Event|a medical encounter|||b|T||
|C|ForProfit|||||Organization|||||||
|C|NonProfit|||||Organization|||Q163740|||foo|

 * [personinfo with types](https://docs.google.com/spreadsheets/d/1wVoaiFg47aT9YWNeRfTZ8tYHN8s8PAuDx5i2HUcDpvQ/edit#gid=509198484)
