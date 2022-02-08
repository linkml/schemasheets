import schemasheets.schemamaker as ss
import os
from linkml_runtime.dumpers import yaml_dumper
import yaml

ROOT = os.path.abspath(os.path.dirname(__file__))
INPUT_DIR = os.path.join(ROOT, 'input')
# OUTPUT_DIR = os.path.join(ROOT, 'output')
INPUT_FILE = "issue-17-multiple-aliases.tsv"
INPUT_PATH = os.path.join(INPUT_DIR, INPUT_FILE)
# OUTPUT_FILE = "issue-17-multiple-aliases.yaml"
# OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

EXPECTED_OUTPUT = """
name: test_schema
id: https://example.com/test_schema
imports:
- linkml:types
prefixes:
  test_schema:
    prefix_prefix: test_schema
    prefix_reference: https://example.com/test_schema/
  linkml:
    prefix_prefix: linkml
    prefix_reference: https://w3id.org/linkml/
default_prefix: test_schema
default_range: string
enums:
  test_enum:
    name: test_enum
    aliases:
    - te_a1
    - te_a2
    permissible_values:
      test_pv:
        text: test_pv
        aliases:
        - tpv_a1
        - tpv_a2
"""


def test_issue_17():
    sm = ss.SchemaMaker()
    schema = sm.create_schema(INPUT_PATH)
    dumped = yaml_dumper.dumps(schema)
    generated_dict = yaml.safe_load(dumped)
    # with open(OUTPUT_PATH, 'r') as stream:
    #     expected_dict = yaml.safe_load(stream)
    expected_dict = yaml.safe_load(EXPECTED_OUTPUT)
    assert generated_dict == expected_dict
