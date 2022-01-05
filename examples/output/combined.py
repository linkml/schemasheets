# Auto generated from combined.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-01-05T12:15:41
# Schema: PersonInfo
#
# id: https://w3id.org/linkml/examples/personinfo
# description: Information about people, based on [schema.org](http://schema.org)
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
from linkml_runtime.linkml_model.types import Decimal, String
from linkml_runtime.utils.metamodelcore import Decimal

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
GSSO = CurieNamespace('GSSO', 'http://purl.obolibrary.org/obo/GSSO_')
FAMREL = CurieNamespace('famrel', 'https://example.org/FamilialRelations#')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
PERSONINFO = CurieNamespace('personinfo', 'https://w3id.org/linkml/examples/personinfo/')
SDO = CurieNamespace('sdo', 'http://schema.org/')
WIKIDATA = CurieNamespace('wikidata', 'http://www.wikidata.org/entity/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = PERSONINFO


# Types
class DecimalDegree(float):
    """ A decimal degree expresses latitude or longitude as decimal fractions """
    type_class_uri = XSD.decimal
    type_class_curie = "xsd:decimal"
    type_name = "DecimalDegree"
    type_model_uri = PERSONINFO.DecimalDegree


class Lang(str):
    """ language tag """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "Lang"
    type_model_uri = PERSONINFO.Lang


# Class references
class PersonId(extended_str):
    pass


@dataclass
class Person(YAMLRoot):
    """
    a person,living or dead
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.Person
    class_class_curie: ClassVar[str] = "personinfo:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.Person

    id: Union[str, PersonId] = None
    name: str = None
    age: Optional[Decimal] = None
    gender: Optional[Decimal] = None
    has_medical_history: Optional[Union[Union[dict, "MedicalEvent"], List[Union[dict, "MedicalEvent"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PersonId):
            self.id = PersonId(self.id)

        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
            self.name = str(self.name)

        if self.age is not None and not isinstance(self.age, Decimal):
            self.age = Decimal(self.age)

        if self.gender is not None and not isinstance(self.gender, Decimal):
            self.gender = Decimal(self.gender)

        if not isinstance(self.has_medical_history, list):
            self.has_medical_history = [self.has_medical_history] if self.has_medical_history is not None else []
        self.has_medical_history = [v if isinstance(v, MedicalEvent) else MedicalEvent(**as_dict(v)) for v in self.has_medical_history]

        super().__post_init__(**kwargs)


@dataclass
class Organization(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.Organization
    class_class_curie: ClassVar[str] = "personinfo:Organization"
    class_name: ClassVar[str] = "Organization"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.Organization

    name: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
            self.name = str(self.name)

        super().__post_init__(**kwargs)


class Event(YAMLRoot):
    """
    grouping class for events
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.Event
    class_class_curie: ClassVar[str] = "personinfo:Event"
    class_name: ClassVar[str] = "Event"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.Event


class MedicalEvent(Event):
    """
    a medical encounter
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.MedicalEvent
    class_class_curie: ClassVar[str] = "personinfo:MedicalEvent"
    class_name: ClassVar[str] = "MedicalEvent"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.MedicalEvent


@dataclass
class ForProfit(Organization):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.ForProfit
    class_class_curie: ClassVar[str] = "personinfo:ForProfit"
    class_name: ClassVar[str] = "ForProfit"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.ForProfit

    name: str = None

@dataclass
class NonProfit(Organization):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.NonProfit
    class_class_curie: ClassVar[str] = "personinfo:NonProfit"
    class_name: ClassVar[str] = "NonProfit"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.NonProfit

    name: str = None

# Enumerations
class FamilialRelationshipType(EnumDefinitionImpl):
    """
    familial relationships
    """
    SIBLING_OF = PermissibleValue(text="SIBLING_OF",
                                           description="share the same parent",
                                           meaning=FAMREL["01"])
    PARENT_OF = PermissibleValue(text="PARENT_OF",
                                         description="biological parent",
                                         meaning=FAMREL["02"])
    CHILD_OF = PermissibleValue(text="CHILD_OF",
                                       description="inverse of parent",
                                       meaning=FAMREL["03"])

    _defn = EnumDefinition(
        name="FamilialRelationshipType",
        description="familial relationships",
    )

class GenderType(EnumDefinitionImpl):
    """
    gender
    """
    _defn = EnumDefinition(
        name="GenderType",
        description="gender",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "nonbinary man",
                PermissibleValue(text="nonbinary man",
                                 meaning=GSSO["009254"]) )
        setattr(cls, "nonbinary woma",
                PermissibleValue(text="nonbinary woma",
                                 meaning=GSSO["009253"]) )

# Slots
class slots:
    pass

slots.id = Slot(uri=PERSONINFO.id, name="id", curie=PERSONINFO.curie('id'),
                   model_uri=PERSONINFO.id, domain=None, range=URIRef)

slots.description = Slot(uri=PERSONINFO.description, name="description", curie=PERSONINFO.curie('description'),
                   model_uri=PERSONINFO.description, domain=None, range=Optional[str])

slots.name = Slot(uri=PERSONINFO.name, name="name", curie=PERSONINFO.curie('name'),
                   model_uri=PERSONINFO.name, domain=None, range=Optional[str])

slots.age = Slot(uri=PERSONINFO.age, name="age", curie=PERSONINFO.curie('age'),
                   model_uri=PERSONINFO.age, domain=None, range=Optional[str])

slots.gender = Slot(uri=PERSONINFO.gender, name="gender", curie=PERSONINFO.curie('gender'),
                   model_uri=PERSONINFO.gender, domain=None, range=Optional[str])

slots.has_medical_history = Slot(uri=PERSONINFO.has_medical_history, name="has medical history", curie=PERSONINFO.curie('has_medical_history'),
                   model_uri=PERSONINFO.has_medical_history, domain=None, range=Optional[str])

slots.Person_id = Slot(uri=PERSONINFO.id, name="Person_id", curie=PERSONINFO.curie('id'),
                   model_uri=PERSONINFO.Person_id, domain=Person, range=Union[str, PersonId])

slots.Person_name = Slot(uri=PERSONINFO.name, name="Person_name", curie=PERSONINFO.curie('name'),
                   model_uri=PERSONINFO.Person_name, domain=Person, range=str)

slots.Person_age = Slot(uri=PERSONINFO.age, name="Person_age", curie=PERSONINFO.curie('age'),
                   model_uri=PERSONINFO.Person_age, domain=Person, range=Optional[Decimal])

slots.Person_gender = Slot(uri=PERSONINFO.gender, name="Person_gender", curie=PERSONINFO.curie('gender'),
                   model_uri=PERSONINFO.Person_gender, domain=Person, range=Optional[Decimal])

slots.Person_has_medical_history = Slot(uri=PERSONINFO.has_medical_history, name="Person_has medical history", curie=PERSONINFO.curie('has_medical_history'),
                   model_uri=PERSONINFO.Person_has_medical_history, domain=Person, range=Optional[Union[Union[dict, "MedicalEvent"], List[Union[dict, "MedicalEvent"]]]])

slots.Organization_name = Slot(uri=PERSONINFO.name, name="Organization_name", curie=PERSONINFO.curie('name'),
                   model_uri=PERSONINFO.Organization_name, domain=Organization, range=str)