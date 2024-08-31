import logging
import os

from linkml.generators.projectgen import ProjectGenerator, ProjectConfiguration
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.schemaview import SchemaView

from schemasheets.schemamaker import SchemaMaker, get_metamodel, SchemaSheetRowException

ROOT = os.path.abspath(os.path.dirname(__file__))
INPUT_DIR = os.path.join(ROOT, 'input')
OUTPUT_DIR = os.path.join(ROOT, 'output')
PROBLEM_DIR = os.path.join(INPUT_DIR, 'problem_cases')

def test_meta():
    sv = get_metamodel()
    #logging.info(sv)

def test_classes_slots():
    sm = SchemaMaker()
    schema = sm.create_schema(os.path.join(INPUT_DIR, 'personinfo.tsv'))
    logging.info(f'SCHEMA={schema}')
    logging.info(f'SCHEMA.cl={schema.classes}')
    logging.info(f'SCHEMA.sl={schema.slots}')
    yaml_dumper.dump(schema, to_file=os.path.join(OUTPUT_DIR, 'personinfo.yaml'))
    yaml = yaml_dumper.dumps(schema)
    #yaml = schema_as_yaml_dump(schema)
    logging.info(yaml)
    #print(yaml)
    person_cls = schema.classes['Person']
    organization_cls = schema.classes['Organization']
    for s in ['id', 'name', 'age', 'gender', 'has medical history']:
        assert s in schema.slots
        assert s in person_cls.slots
    assert schema.slots['id'].identifier
    assert schema.slots['id'].exact_mappings == ['sdo:identifier']
    assert person_cls.slot_usage['id'].identifier
    assert person_cls.slot_usage['has medical history'].multivalued
    assert person_cls.status == 'release'
    anns = schema.slots['description'].annotations
    assert anns
    assert anns['special']
    assert anns['special'].value == 'my_val'
    assert anns['special2'].value == 'my_val2'
    assert not person_cls.slot_usage['has medical history'].required
    assert person_cls.slot_usage['has medical history'].status == 'testing'
    assert 'name' in organization_cls.slots
    assert len(person_cls.exact_mappings) == 2
    assert 'wikidata:Q215627' in person_cls.exact_mappings
    assert 'sdo:Person' in person_cls.exact_mappings

def test_metatype():
    sm = SchemaMaker()
    schema = sm.create_schema(os.path.join(INPUT_DIR, 'personinfo_with_types.tsv'))
    logging.info(f'SCHEMA={schema}')
    logging.info(f'SCHEMA.cl={schema.classes}')
    logging.info(f'SCHEMA.sl={schema.slots}')
    yaml_dumper.dump(schema, to_file=os.path.join(OUTPUT_DIR, 'personinfo.yaml'))
    yaml = yaml_dumper.dumps(schema)
    #yaml = schema_as_yaml_dump(schema)
    logging.info(yaml)
    #print(yaml)
    person_cls = schema.classes['Person']
    organization_cls = schema.classes['Organization']
    for s in ['id', 'name', 'age', 'gender', 'has medical history']:
        assert s in schema.slots
    for c in ['Person', 'Event', 'MedicalEvent', 'Organization', 'ForProfit', 'NonProfit']:
        assert c in schema.classes
    assert schema.slots['id'].identifier
    assert schema.slots['id'].exact_mappings == ['sdo:identifier']
    assert person_cls.slot_usage['name'].description
    assert person_cls.slot_usage['has medical history'].multivalued
    assert person_cls.status == 'release'
    assert not person_cls.slot_usage['has medical history'].required
    assert person_cls.slot_usage['has medical history'].status == 'testing'
    assert 'name' in organization_cls.slots
    assert len(person_cls.exact_mappings) == 2
    assert 'wikidata:Q215627' in person_cls.exact_mappings
    assert 'sdo:Person' in person_cls.exact_mappings

def test_cardinality():
    sm = SchemaMaker()
    schema = sm.create_schema(os.path.join(INPUT_DIR, 'cardinality_test.tsv'))
    logging.info(f'SCHEMA={schema}')
    logging.info(f'SCHEMA.cl={schema.classes}')
    logging.info(f'SCHEMA.sl={schema.slots}')
    yaml_dumper.dump(schema, to_file=os.path.join(OUTPUT_DIR, 'personinfo.yaml'))
    yaml = yaml_dumper.dumps(schema)
    #yaml = schema_as_yaml_dump(schema)
    logging.info(yaml)
    #print(yaml)
    person_cls = schema.classes['Person']
    organization_cls = schema.classes['Organization']
    for s in ['id', 'name', 'age', 'gender', 'has medical history']:
        assert s in schema.slots
        assert s in person_cls.slots
    assert schema.slots['id'].identifier
    assert schema.slots['id'].exact_mappings == ['sdo:identifier']
    assert person_cls.slot_usage['id'].identifier
    assert person_cls.slot_usage['has medical history'].multivalued
    assert person_cls.status == 'release'
    assert not person_cls.slot_usage['has medical history'].required
    assert person_cls.slot_usage['has medical history'].status == 'testing'
    assert 'name' in organization_cls.slots
    assert len(person_cls.exact_mappings) == 2
    assert 'wikidata:Q215627' in person_cls.exact_mappings
    assert 'sdo:Person' in person_cls.exact_mappings

def test_prefixes():
    sm = SchemaMaker()
    schema = sm.create_schema(os.path.join(INPUT_DIR, 'prefixes.tsv'))
    yaml = yaml_dumper.dumps(schema)
    #yaml = schema_as_yaml_dump(schema)
    logging.info(yaml)
    assert schema.prefixes['sdo'].prefix_reference == 'http://schema.org/'

def test_types():
    sm = SchemaMaker()
    schema = sm.create_schema(os.path.join(INPUT_DIR, 'types.tsv'))
    yaml = yaml_dumper.dumps(schema)
    #yaml = schema_as_yaml_dump(schema)
    logging.info(yaml)
    assert schema.types['DecimalDegree'].base == 'float'

def test_subsets():
    sm = SchemaMaker()
    schema = sm.create_schema(os.path.join(INPUT_DIR, 'subsets.tsv'))
    yaml = yaml_dumper.dumps(schema)
    #yaml = schema_as_yaml_dump(schema)
    logging.info(yaml)
    assert schema.subsets['a']

def test_enums():
    sm = SchemaMaker()
    schema = sm.create_schema(os.path.join(INPUT_DIR, 'enums.tsv'))
    yaml = yaml_dumper.dumps(schema)
    #yaml = schema_as_yaml_dump(schema)
    logging.info(yaml)
    e = schema.enums['FamilialRelationshipType']
    assert e.description
    pvs = e.permissible_values
    for k, pv in pvs.items():
        logging.info(f' {k} == {pv}')
        assert pv.meaning
        assert pv.description
    assert pvs['SIBLING_OF'].meaning == 'famrel:01'

    #assert schema.prefixes['sdo'].prefix_reference = 'http://schema.org/'

def test_schema():
    sm = SchemaMaker()
    schema = sm.create_schema(os.path.join(INPUT_DIR, 'schema.tsv'))
    yaml = yaml_dumper.dumps(schema)
    #yaml = schema_as_yaml_dump(schema)
    logging.info(yaml)
    assert schema.name == 'PersonInfo'
    assert schema.id.startswith('https')
    assert schema.default_prefix == 'personinfo'
    assert schema.description

def test_datadict():
    """
    uses data dictionary sheet to test per-column slot-usage setting

    datadict.tsv includes cardinality columns for each class in the schema
    (MI patient, MI model organism, ...)
    the descriptors for these columns provide values for cardinality/applicability
    for each slot row in these column values.

    E.g. the row for 'depth' in column 'MI marine sample' has a value of 'R',
    this maps to "recommended" in the cardinality enum, so the slot usage
    for marine samples for the depth slot will be set to recommended
    """
    sm = SchemaMaker()
    schema = sm.create_schema(os.path.join(INPUT_DIR, 'datadict.tsv'))
    sv = SchemaView(schema)
    yaml = yaml_dumper.dumps(schema)
    #yaml = schema_as_yaml_dump(schema)
    #print(yaml)
    patient_cls = schema.classes['MI patient']
    assert patient_cls.slot_usage['id'].required
    for cls in [schema.classes[x] for x in ['MI patient', 'MI model organism', 'MI terrestrial sample', 'MI marine sample']]:
        assert cls.slot_usage['id'].required
        assert not cls.slot_usage['id'].recommended
        assert not cls.slot_usage['id'].multivalued
        assert not cls.slot_usage['alt_ids'].required
        for sn in ['depth', 'alt', 'salinity']:
            if cls.name == 'MI patient' or cls.name == 'MI model organism':
                assert sn not in cls.slot_usage
                assert sn not in cls.slots
                assert sn not in [x.name for x in sv.class_induced_slots(cls.name)]
            else:
                assert sn in cls.slots
                assert cls.slot_usage[sn].recommended

def test_combined():
    sm = SchemaMaker()
    sheets = ['schema', 'prefixes', 'enums', 'types', 'subsets', 'personinfo']
    files = [os.path.join(INPUT_DIR, f'{s}.tsv') for s in sheets]
    schema = sm.create_schema(files)
    yaml = yaml_dumper.dumps(schema)
    #yaml = schema_as_yaml_dump(schema)
    logging.info(yaml)
    outf = os.path.join(OUTPUT_DIR, 'combined.yaml')
    yaml_dumper.dump(schema, to_file=outf)
    pgen = ProjectGenerator()
    project_config = ProjectConfiguration()
    project_config.directory = str(os.path.join(OUTPUT_DIR, 'personinfo'))
    pgen.generate(outf, project_config)

def test_autofill():
    """
    Tests for automatic filling in / repair of incomplete information
    :return:
    """
    sm = SchemaMaker()
    sheets = ['personinfo']
    files = [os.path.join(INPUT_DIR, f'{s}.tsv') for s in sheets]
    schema = sm.create_schema(files)
    sm.repair_schema(schema)
    yaml = yaml_dumper.dumps(schema)
    outf = os.path.join(OUTPUT_DIR, 'combined_autofill.yaml')
    yaml_dumper.dump(schema, to_file=outf)
    pgen = ProjectGenerator()
    project_config = ProjectConfiguration()
    project_config.directory = str(os.path.join(OUTPUT_DIR, 'personinfo_autofill'))
    pgen.generate(outf, project_config)

PROBLEMS = {
    'no_element_case': SchemaSheetRowException,
    'multiple_element_case': SchemaSheetRowException,
    'inconsistent_value_case': SchemaSheetRowException,
}

def test_problem_cases():
    """
    tests deliberately erroneous cases
    """
    sm = SchemaMaker()
    for k, exception_type in PROBLEMS.items():
        file = os.path.join(PROBLEM_DIR, f'{k}.tsv')
        raised = False
        try:
            schema = sm.create_schema(file)
        except exception_type as e:
            print(f'Expected error: {e}')
            raised = True
        assert raised

def test_load_table_config():
    """
    tests loading of table configuration

    Same as personinfo test, but we provide a separate config
    :return:
    """
    sm = SchemaMaker(table_config_path=os.path.join(INPUT_DIR, 'personinfo-descriptors.yaml'))
    schema = sm.create_schema(os.path.join(INPUT_DIR, 'personinfo-no-descriptors.tsv'))
    yaml_dumper.dump(schema, to_file=os.path.join(OUTPUT_DIR, 'personinfo.yaml'))
    yaml = yaml_dumper.dumps(schema)
    logging.info(yaml)
    print(yaml)
    person_cls = schema.classes['Person']
    organization_cls = schema.classes['Organization']
    for s in ['id', 'name', 'age', 'gender', 'has medical history']:
        assert s in schema.slots
        assert s in person_cls.slots
    assert schema.slots['id'].identifier
    assert schema.slots['id'].exact_mappings == ['sdo:identifier']
    assert person_cls.slot_usage['id'].identifier
    assert person_cls.slot_usage['has medical history'].multivalued
    assert person_cls.status == 'release'
    anns = schema.slots['description'].annotations
    assert anns
    assert anns['special']
    assert anns['special'].value == 'my_val'
    assert anns['special2'].value == 'my_val2'
    assert not person_cls.slot_usage['has medical history'].required
    assert person_cls.slot_usage['has medical history'].status == 'testing'
    assert 'name' in organization_cls.slots
    assert len(person_cls.exact_mappings) == 2
    assert 'wikidata:Q215627' in person_cls.exact_mappings
    assert 'sdo:Person' in person_cls.exact_mappings


def test_classes_slots_anyof():
    """testing any_of in the slots"""
    sm = SchemaMaker()
    schema = sm.create_schema(os.path.join(INPUT_DIR, 'personinfo_anyof.tsv'))
    logging.info(f'SCHEMA={schema}')
    logging.info(f'SCHEMA.cl={schema.classes}')
    logging.info(f'SCHEMA.sl={schema.slots}')
    yaml_dumper.dump(schema, to_file=os.path.join(OUTPUT_DIR, 'personinfo.yaml'))
    yaml = yaml_dumper.dumps(schema)
    logging.info(yaml)
    person_cls = schema.classes['Person']
    assert person_cls.slot_usage["age"].any_of[0].range == "decimal"
    assert person_cls.slot_usage["age"].any_of[1].range == "integer"
