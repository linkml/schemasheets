import logging
import os

from linkml.generators.projectgen import ProjectGenerator, ProjectConfiguration
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.schemaview import SchemaView

from schemasheets.schema_exporter import SchemaExporter
from schemasheets.schemamaker import SchemaMaker, get_metamodel, SchemaSheetRowException

ROOT = os.path.abspath(os.path.dirname(__file__))
INPUT_DIR = os.path.join(ROOT, 'input')
OUTPUT_DIR = os.path.join(ROOT, 'output')

def test_export_slots():
    """
    Tests linkml2sheets
    """
    sm = SchemaMaker()
    fn = os.path.join(INPUT_DIR, 'personinfo.tsv')
    out_fn = os.path.join(OUTPUT_DIR, 'personinfo-roundtrip.tsv')
    # sheets2linkml
    schema = sm.create_schema(fn)
    exporter = SchemaExporter(schemamaker=sm)
    sv = SchemaView(schema)
    # linkml2sheets, using original sheets as specification
    exporter.export(sv, specification=fn, to_file=out_fn)
    for row in exporter.rows:
        print(row)
    assert {'record': 'Person', 'field': 'age', 'range': 'decimal', 'desc': 'age in years'} in exporter.rows
    assert {'record': 'ForProfit', 'parents': 'Organization'} in exporter.rows
    # tests curie contraction
    assert {'record': 'Person', 'field': 'id', 'key': 'True', 'range': 'string',
            'desc': 'identifier for a person', 'schema.org': 'identifier'} in exporter.rows

