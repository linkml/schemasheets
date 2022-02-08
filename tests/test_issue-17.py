import schemasheets.schemamaker as ss
import os
from linkml_runtime.dumpers import yaml_dumper
import yaml

# import pprint

ROOT = os.path.abspath(os.path.dirname(__file__))
INPUT_DIR = os.path.join(ROOT, 'input')
OUTPUT_DIR = os.path.join(ROOT, 'output')
INPUT_FILE = "issue-17-multiple-aliases.tsv"
INPUT_PATH = os.path.join(INPUT_DIR, INPUT_FILE)
OUTPUT_FILE = "issue-17-multiple-aliases.yaml"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILE)


def test_issue_17():
    # compare as Schemas, dicts, or YAML strings?
    sm = ss.SchemaMaker()
    schema = sm.create_schema(INPUT_PATH)
    dumped = yaml_dumper.dumps(schema)
    generated_dict = yaml.safe_load(dumped)
    with open(OUTPUT_PATH, 'r') as stream:
        expected_dict = yaml.safe_load(stream)
    assert generated_dict == expected_dict
