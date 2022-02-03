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

def test_rda_crosswalk():
    sm = SchemaMaker(unique_slots=True)
    schema = sm.create_schema(os.path.join(INPUT_DIR, 'rda-crosswalk.tsv'))
    logging.info(f'SCHEMA={schema}')
    logging.info(f'SCHEMA.cl={schema.classes}')
    logging.info(f'SCHEMA.sl={schema.slots}')
    schema = sm.repair_schema(schema)
    yaml_dumper.dump(schema, to_file=os.path.join(OUTPUT_DIR, 'rda-crosswalk.yaml'))
    yaml = yaml_dumper.dumps(schema)
    #yaml = schema_as_yaml_dump(schema)
    logging.info(yaml)
    #print(yaml)
    sv = SchemaView(yaml)

