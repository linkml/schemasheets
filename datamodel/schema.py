# Auto generated from schema.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-01-01T14:00:06
# Schema: TEMP
#
# id: TEMP
# description:
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
TEMP = CurieNamespace('TEMP', 'http://example.org/TEMP/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
SDO = CurieNamespace('sdo', 'http://example.org/sdo/')
WIKIDATA = CurieNamespace('wikidata', 'http://www.wikidata.org/entity/')
DEFAULT_ = TEMP


# Types

# Class references
class PersonId(extended_str):
    pass


@dataclass
class Person(YAMLRoot):
    """
    a person,living or dead
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEMP.Person
    class_class_curie: ClassVar[str] = "TEMP:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = TEMP.Person

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

    class_class_uri: ClassVar[URIRef] = TEMP.Organization
    class_class_curie: ClassVar[str] = "TEMP:Organization"
    class_name: ClassVar[str] = "Organization"
    class_model_uri: ClassVar[URIRef] = TEMP.Organization

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

    class_class_uri: ClassVar[URIRef] = TEMP.Event
    class_class_curie: ClassVar[str] = "TEMP:Event"
    class_name: ClassVar[str] = "Event"
    class_model_uri: ClassVar[URIRef] = TEMP.Event


class MedicalEvent(Event):
    """
    a medical encounter
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEMP.MedicalEvent
    class_class_curie: ClassVar[str] = "TEMP:MedicalEvent"
    class_name: ClassVar[str] = "MedicalEvent"
    class_model_uri: ClassVar[URIRef] = TEMP.MedicalEvent


@dataclass
class ForProfit(Organization):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEMP.ForProfit
    class_class_curie: ClassVar[str] = "TEMP:ForProfit"
    class_name: ClassVar[str] = "ForProfit"
    class_model_uri: ClassVar[URIRef] = TEMP.ForProfit

    name: str = None

@dataclass
class NonProfit(Organization):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TEMP.NonProfit
    class_class_curie: ClassVar[str] = "TEMP:NonProfit"
    class_name: ClassVar[str] = "NonProfit"
    class_model_uri: ClassVar[URIRef] = TEMP.NonProfit

    name: str = None

# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=TEMP.id, name="id", curie=TEMP.curie('id'),
                   model_uri=TEMP.id, domain=None, range=URIRef)

slots.description = Slot(uri=TEMP.description, name="description", curie=TEMP.curie('description'),
                   model_uri=TEMP.description, domain=None, range=Optional[str])

slots.name = Slot(uri=TEMP.name, name="name", curie=TEMP.curie('name'),
                   model_uri=TEMP.name, domain=None, range=Optional[str])

slots.age = Slot(uri=TEMP.age, name="age", curie=TEMP.curie('age'),
                   model_uri=TEMP.age, domain=None, range=Optional[str])

slots.gender = Slot(uri=TEMP.gender, name="gender", curie=TEMP.curie('gender'),
                   model_uri=TEMP.gender, domain=None, range=Optional[str])

slots.has_medical_history = Slot(uri=TEMP.has_medical_history, name="has medical history", curie=TEMP.curie('has_medical_history'),
                   model_uri=TEMP.has_medical_history, domain=None, range=Optional[str])

slots.Person_id = Slot(uri=TEMP.id, name="Person_id", curie=TEMP.curie('id'),
                   model_uri=TEMP.Person_id, domain=Person, range=Union[str, PersonId])

slots.Person_name = Slot(uri=TEMP.name, name="Person_name", curie=TEMP.curie('name'),
                   model_uri=TEMP.Person_name, domain=Person, range=str)

slots.Person_age = Slot(uri=TEMP.age, name="Person_age", curie=TEMP.curie('age'),
                   model_uri=TEMP.Person_age, domain=Person, range=Optional[Decimal])

slots.Person_gender = Slot(uri=TEMP.gender, name="Person_gender", curie=TEMP.curie('gender'),
                   model_uri=TEMP.Person_gender, domain=Person, range=Optional[Decimal])

slots.Person_has_medical_history = Slot(uri=TEMP.has_medical_history, name="Person_has medical history", curie=TEMP.curie('has_medical_history'),
                   model_uri=TEMP.Person_has_medical_history, domain=Person, range=Optional[Union[Union[dict, "MedicalEvent"], List[Union[dict, "MedicalEvent"]]]])

slots.Organization_name = Slot(uri=TEMP.name, name="Organization_name", curie=TEMP.curie('name'),
                   model_uri=TEMP.Organization_name, domain=Organization, range=str)