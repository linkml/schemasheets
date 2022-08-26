from linkml_runtime import SchemaView
from sqlalchemy.sql.ddl import SchemaGenerator

import schemasheets.schemamaker as ss
import os
from linkml_runtime.dumpers import yaml_dumper
import yaml

from schemasheets.schema_exporter import SchemaExporter
from tests import INPUT_DIR, OUTPUT_DIR

SCHEMA = r"""
name: test_schema
id: https://example.com/test_schema
imports:
- linkml:types
prefixes:
  test_schema: https://example.com/test_schema/
  linkml: https://w3id.org/linkml/
default_prefix: test_schema
default_range: string
settings:
  token: "\\S"
classes:
  Person:
    attributes:
      first:
      last:
      full:
        structured_pattern:
          syntax: "{token} {token}"
"""


def test_structured_syntax():
    sm = ss.SchemaMaker()
    sheet_path = str(INPUT_DIR / "structured_syntax.tsv")
    out_path = str(OUTPUT_DIR / "structured_syntax-roundtrip.tsv")
    #schema = sm.create_schema(INPUT_DIR / "structured_syntax.tsv")
    exporter = SchemaExporter(schemamaker=sm)
    sv = SchemaView(SCHEMA)
    #print(yaml_dumper.dumps(sv.schema))
    exporter.export(sv, specification=sheet_path, to_file=out_path)
    schema2 = sm.create_schema(out_path)
    print(yaml_dumper.dumps(schema2))
    assert schema2.slots["full"].structured_pattern.syntax == "{token} {token}"

