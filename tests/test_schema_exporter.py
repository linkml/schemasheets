import logging
import os

from linkml.utils.schema_builder import SchemaBuilder
from linkml.utils.schema_fixer import SchemaFixer
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import TypeDefinition, Annotation
from linkml_runtime.utils.introspection import package_schemaview
from linkml_runtime.utils.schemaview import SchemaView, SchemaDefinition, SlotDefinition, ClassDefinition, YAMLRoot
from schemasheets.schema_exporter import SchemaExporter
from schemasheets.schemamaker import SchemaMaker
from schemasheets.schemasheet_datamodel import SchemaSheet

ROOT = os.path.abspath(os.path.dirname(__file__))
INPUT_DIR = os.path.join(ROOT, 'input')
OUTPUT_DIR = os.path.join(ROOT, 'output')
SHEET = os.path.join(INPUT_DIR, 'personinfo.tsv')
ROUNDTRIPPED_SHEET = os.path.join(OUTPUT_DIR, 'personinfo-roundtrip.tsv')
MINISHEET = os.path.join(OUTPUT_DIR, 'mini.tsv')
TEST_SPEC = os.path.join(INPUT_DIR, 'test-spec.tsv')
ENUM_SPEC = os.path.join(INPUT_DIR, 'enums.tsv')
TYPES_SPEC = os.path.join(INPUT_DIR, 'types.tsv')
PREFIXES_SPEC = os.path.join(INPUT_DIR, 'prefixes.tsv')
SLOT_SPEC = os.path.join(INPUT_DIR, 'slot-spec.tsv')

EXPECTED = [
    {
        'field': 'id',
        'key': 'true',  # https://github.com/linkml/schemasheets/issues/67
        'range': 'string',
        'desc': 'any identifier',
        'schema.org': 'identifier',
        ## TODO
        ##  'multiplicity': '1',
    },
    {
        'record': 'Person',
        'field': 'age',
        'range': 'decimal',
        'desc': 'age in years'
    },
    {
        'record': 'ForProfit',
        'parents': 'Organization'
    },
    {
        'field': 'name'
    },
    # tests curie contraction
    {
        'record': 'Person',
        'field': 'id',
        'key': 'true',
        'range': 'string',
        'desc': 'identifier for a person',
        'schema.org': 'identifier'
    },
]


def test_roundtrip_schema():
    """
    Tests linkml2sheets by round-tripping from the standard personinfo schema in YAML
    """
    sm = SchemaMaker()
    # sheets2linkml, from SHEET
    schema = sm.create_schema(SHEET)
    exporter = SchemaExporter(schemamaker=sm)
    sv = SchemaView(schema)
    # linkml2sheets, using original sheets as specification
    # (note that this ignores the main data in the TSV)

    exporter.export(sv, specification=SHEET, to_file=ROUNDTRIPPED_SHEET)
    for row in exporter.rows:
        logging.info(row)
    for record in EXPECTED:
        assert record in exporter.rows


def _roundtrip(schema: SchemaDefinition, specification: str, must_pass=True) -> SchemaDefinition:
    """
    Tests a roundtrip from a Schema object to sheets, and then back to a schema, using
    the specified specification

    :param schema:
    :param specification:
    :return:
    """
    sm = SchemaMaker()
    exporter = SchemaExporter(schemamaker=sm)
    sv = SchemaView(schema)
    exporter.export(schemaview=sv, specification=specification, to_file=MINISHEET)
    # for row in exporter.rows:
    #    print(row)
    schema2 = sm.create_schema(MINISHEET)
    sv2 = SchemaView(schema2)
    for e in sv.all_elements().values():
        e2 = sv2.get_element(e.name)
        if e2 is None:
            if not must_pass:
                continue
            raise ValueError(f"Could not find {e}")
        e2.from_schema = e.from_schema
        for s, v in vars(e).items():
            v2 = getattr(e2, s, None)
            if v != v2:
                logging.error(f"   UNEXPECTED {s}: {v} ?= {v2} // {type(v2)}")
            if must_pass:
                assert v == v2
    return schema2


def test_dynamic():
    """
    tests dynamically building up a schema and exporting
    """
    sb = SchemaBuilder()
    sf = SchemaFixer()
    sb.add_class('A', [])
    sb.add_class('M1', [])
    sb.add_class('M2', [])
    s1 = SlotDefinition('s1', title="ts1", description='s1', range="Y")
    s2 = SlotDefinition('s2', title="ts2", description='s2', range="string")
    s3 = SlotDefinition('s3', title="ts2", description='s3', range="integer")
    s2X = SlotDefinition('s2', pattern="^\\S+$")
    sb.add_class('X', ['s1', 's2'], slot_usage={'s2': s2X},
                 description='d1', is_a="A", mixins=["M1"])
    sb.add_class('Y', ['s2', 's3'], description='d2', is_a="A", mixins=["M1", "M2"])

    # adding these give a "slot already present' error. it appears that they are implicitly added
    #   when adding classes that use them
    #   after having switched from LinkML 1.3 to 1.5

    sb.add_defaults()
    schema = sb.schema

    _roundtrip(schema, TEST_SPEC)


def test_inner_key():
    """
    Tests the use of inner_key with annotations

    See https://github.com/linkml/schemasheets/issues/59
    """
    sb = SchemaBuilder()
    sf = SchemaFixer()
    a = Annotation("display_hint", "hello")
    a2 = Annotation("more_words", "profound_words")
    s = SlotDefinition("s1")
    c = ClassDefinition("X",
                        slots=["s1"],
                        slot_usage={s.name: s},
                        annotations={a.tag: a, a2.tag: a2})
    schema = sb.schema
    schema.classes[c.name] = c
    c = schema.classes['X']
    assert isinstance(c, ClassDefinition)
    print(type(c.annotations))
    assert isinstance(c.annotations, dict)
    assert isinstance(c.slot_usage, dict)
    _roundtrip(schema, os.path.join(INPUT_DIR, 'test-spec-ann.tsv'))


def test_enums():
    """
    tests a specification that is dedicated to enums
    """
    sb = SchemaBuilder()
    sb.add_enum('E', ['V1', 'V2'])
    sb.add_defaults()
    schema = sb.schema
    # TODO: add this functionality to SchemaBuilder
    e = schema.enums['E']
    e.description = 'test desc'
    _roundtrip(schema, ENUM_SPEC)


def test_prefixes():
    """
    tests a specification that is dedicated to prefixes
    """
    sb = SchemaBuilder()
    sb.add_prefix("ex", "https://example.org/")
    sb.add_defaults()
    schema = sb.schema
    schema_recapitulated = _roundtrip(schema, PREFIXES_SPEC)
    assert "ex" in schema_recapitulated.prefixes
    assert schema_recapitulated.prefixes["ex"].prefix_reference == "https://example.org/"
    assert "linkml" in schema_recapitulated.prefixes


def test_types():
    """
    tests a specification that is dedicated to types
    """
    sb = SchemaBuilder()
    schema = sb.schema
    # TODO: add this functionality to SchemaBuilder
    t = TypeDefinition('MyString', description='my string', typeof='string')
    schema.types[t.name] = t
    _roundtrip(schema, TYPES_SPEC)


def test_parse_specification_from_tsv():
    """
    Tests parsing of specification rows from TSV
    """
    schemasheet = SchemaSheet.from_csv(TEST_SPEC)
    table_config = schemasheet.table_config
    mixins_config = table_config.columns["mixins"]
    assert "|" == mixins_config.settings.internal_separator


def test_export_metamodel():
    metamodel_sv = package_schemaview('linkml_runtime.linkml_model.meta')
    metamodel_schema = metamodel_sv.schema
    roundtripped_schema = _roundtrip(metamodel_schema, TEST_SPEC, must_pass=False)
    logging.info(yaml_dumper.dumps(roundtripped_schema))


def test_export_metamodel_slots():
    sm = SchemaMaker()
    metamodel_sv = package_schemaview('linkml_runtime.linkml_model.meta')
    metamodel_schema = metamodel_sv.schema
    exporter = SchemaExporter(schemamaker=sm)
    sv = SchemaView(metamodel_schema)
    exporter.export(sv, specification=SLOT_SPEC, to_file=MINISHEET)
    all_of_slot_rows = [row for row in exporter.rows if row['slot'] == 'all_of']
    assert 1 == len(all_of_slot_rows)
    [s] = [row for row in exporter.rows if row['slot'] == 'status']
    # NOTE: this test may be too rigid, if the metamodel documentation changes then the results
    # of this will change
    examples = s['examples']
    assert 'bibo:draft' == examples
