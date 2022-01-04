# Auto generated from configschema.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-01-02T19:30:04
# Schema: configschema
#
# id: https://w3id.org/linkml/configschema
# description: Data model for configuration of schema sheets.
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import String

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
CARVOC = CurieNamespace('carvoc', 'https://w3id.org/carvoc/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
THIS = CurieNamespace('this', 'https://w3id.org/linkml/configschema/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = THIS


# Types
class ElementReference(str):
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "ElementReference"
    type_model_uri = THIS.ElementReference


# Class references
class ValueMapMapKey(extended_str):
    pass


@dataclass
class ColumnSettings(YAMLRoot):
    """
    configuration for an individual column in a schema sheet.
    These settings are typically specified as YAML blocks beneath
    the relevant column header.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = THIS.ColumnSettings
    class_class_curie: ClassVar[str] = "this:ColumnSettings"
    class_name: ClassVar[str] = "ColumnSettings"
    class_model_uri: ClassVar[URIRef] = THIS.ColumnSettings

    curie_prefix: Optional[str] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    template: Optional[str] = None
    vmap: Optional[Union[Dict[Union[str, ValueMapMapKey], Union[dict, "ValueMap"]], List[Union[dict, "ValueMap"]]]] = empty_dict()
    applies_to_class: Optional[str] = None
    applies_to_slot: Optional[str] = None
    tag: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.curie_prefix is not None and not isinstance(self.curie_prefix, str):
            self.curie_prefix = str(self.curie_prefix)

        if self.prefix is not None and not isinstance(self.prefix, str):
            self.prefix = str(self.prefix)

        if self.suffix is not None and not isinstance(self.suffix, str):
            self.suffix = str(self.suffix)

        if self.template is not None and not isinstance(self.template, str):
            self.template = str(self.template)

        self._normalize_inlined_as_dict(slot_name="vmap", slot_type=ValueMap, key_name="map_key", keyed=True)

        if self.applies_to_class is not None and not isinstance(self.applies_to_class, str):
            self.applies_to_class = str(self.applies_to_class)

        if self.applies_to_slot is not None and not isinstance(self.applies_to_slot, str):
            self.applies_to_slot = str(self.applies_to_slot)

        if self.tag is not None and not isinstance(self.tag, str):
            self.tag = str(self.tag)

        super().__post_init__(**kwargs)


@dataclass
class ValueMap(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = THIS.ValueMap
    class_class_curie: ClassVar[str] = "this:ValueMap"
    class_name: ClassVar[str] = "ValueMap"
    class_model_uri: ClassVar[URIRef] = THIS.ValueMap

    map_key: Union[str, ValueMapMapKey] = None
    map_value: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.map_key):
            self.MissingRequiredField("map_key")
        if not isinstance(self.map_key, ValueMapMapKey):
            self.map_key = ValueMapMapKey(self.map_key)

        if self.map_value is not None and not isinstance(self.map_value, str):
            self.map_value = str(self.map_value)

        super().__post_init__(**kwargs)


# Enumerations
class Cardinality(EnumDefinitionImpl):
    """
    vocabulary for describing cardinality and applicability of slots or fields
    """
    mandatory = PermissibleValue(text="mandatory",
                                         description="At least one value MUST be provided",
                                         meaning=CARVOC.Mandatory)
    optional = PermissibleValue(text="optional",
                                       description="A value MAY be provided",
                                       meaning=CARVOC.Optional)
    recommended = PermissibleValue(text="recommended",
                                             description="A value SHOULD be provided",
                                             meaning=CARVOC.Recommended)
    not_recommended = PermissibleValue(text="not_recommended",
                                                     description="Values are permitted, but SHOULD NOT be filled in",
                                                     meaning=CARVOC.NotRecommended)
    applicable = PermissibleValue(text="applicable",
                                           description="union of optional and mandatory",
                                           meaning=CARVOC.Applicable)
    not_applicable = PermissibleValue(text="not_applicable",
                                                   description="A value MUST NOT be provided",
                                                   meaning=CARVOC.NotApplicable)
    zero_or_one = PermissibleValue(text="zero_or_one",
                                             description="not required, single-valued",
                                             meaning=CARVOC.ZeroToOne)
    exactly_one = PermissibleValue(text="exactly_one",
                                             description="required, single-valued",
                                             meaning=CARVOC.ExactlyOne)
    zero_to_many = PermissibleValue(text="zero_to_many",
                                               description="not required, multi-valued",
                                               meaning=CARVOC.ZeroToMany)
    one_to_many = PermissibleValue(text="one_to_many",
                                             description="required, multi-valued",
                                             meaning=CARVOC.OneToMany)
    single_valued = PermissibleValue(text="single_valued",
                                                 description="not multi-valued",
                                                 meaning=CARVOC.SingleValued)
    multi_valued = PermissibleValue(text="multi_valued",
                                               description="multi-valued",
                                               meaning=CARVOC.MultiValued)
    conditional = PermissibleValue(text="conditional",
                                             description="A qualifier on cardinalities that indicates the interpretation is context-dependent",
                                             meaning=CARVOC.Conditional)
    unconditional = PermissibleValue(text="unconditional",
                                                 description="A qualifier on cardinalities that indicates the interpretation is context-independent",
                                                 meaning=CARVOC.Unconditional)
    conditional_mandatory = PermissibleValue(text="conditional_mandatory",
                                                                 meaning=CARVOC.ConditionalMandatory)

    _defn = EnumDefinition(
        name="Cardinality",
        description="vocabulary for describing cardinality and applicability of slots or fields",
    )

class Shortcuts(EnumDefinitionImpl):

    cardinality = PermissibleValue(text="cardinality")
    ignore = PermissibleValue(text="ignore")
    metatype = PermissibleValue(text="metatype")
    slot = PermissibleValue(text="slot",
                               meaning=LINKML.SlotDefinition)
    enum = PermissibleValue(text="enum",
                               meaning=LINKML.EnumDefinition)

    _defn = EnumDefinition(
        name="Shortcuts",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "class",
                PermissibleValue(text="class",
                                 meaning=LINKML.ClassDefinition) )

# Slots
class slots:
    pass

slots.map_key = Slot(uri=THIS.map_key, name="map_key", curie=THIS.curie('map_key'),
                   model_uri=THIS.map_key, domain=None, range=URIRef)

slots.map_value = Slot(uri=THIS.map_value, name="map_value", curie=THIS.curie('map_value'),
                   model_uri=THIS.map_value, domain=None, range=Optional[str])

slots.columnSettings__curie_prefix = Slot(uri=THIS.curie_prefix, name="columnSettings__curie_prefix", curie=THIS.curie('curie_prefix'),
                   model_uri=THIS.columnSettings__curie_prefix, domain=None, range=Optional[str])

slots.columnSettings__prefix = Slot(uri=THIS.prefix, name="columnSettings__prefix", curie=THIS.curie('prefix'),
                   model_uri=THIS.columnSettings__prefix, domain=None, range=Optional[str])

slots.columnSettings__suffix = Slot(uri=THIS.suffix, name="columnSettings__suffix", curie=THIS.curie('suffix'),
                   model_uri=THIS.columnSettings__suffix, domain=None, range=Optional[str])

slots.columnSettings__template = Slot(uri=THIS.template, name="columnSettings__template", curie=THIS.curie('template'),
                   model_uri=THIS.columnSettings__template, domain=None, range=Optional[str])

slots.columnSettings__vmap = Slot(uri=THIS.vmap, name="columnSettings__vmap", curie=THIS.curie('vmap'),
                   model_uri=THIS.columnSettings__vmap, domain=None, range=Optional[Union[Dict[Union[str, ValueMapMapKey], Union[dict, ValueMap]], List[Union[dict, ValueMap]]]])

slots.columnSettings__applies_to_class = Slot(uri=THIS.applies_to_class, name="columnSettings__applies_to_class", curie=THIS.curie('applies_to_class'),
                   model_uri=THIS.columnSettings__applies_to_class, domain=None, range=Optional[str])

slots.columnSettings__applies_to_slot = Slot(uri=THIS.applies_to_slot, name="columnSettings__applies_to_slot", curie=THIS.curie('applies_to_slot'),
                   model_uri=THIS.columnSettings__applies_to_slot, domain=None, range=Optional[str])

slots.columnSettings__tag = Slot(uri=THIS.tag, name="columnSettings__tag", curie=THIS.curie('tag'),
                   model_uri=THIS.columnSettings__tag, domain=None, range=Optional[str])
