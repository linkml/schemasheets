import os
from pathlib import Path

import pytest
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.schemaview import SchemaView

from schemasheets.schema_exporter import SchemaExporter
from schemasheets.schemamaker import SchemaMaker
from tests import INPUT_DIR, OUTPUT_DIR


@pytest.mark.parametrize("source_dir,init_args,roundtrip,delimiter", [
    ("personinfo-schema", {"use_attributes": True, "unique_slots": True}, True, ","),
    ("kg-example-schema", {"use_attributes": False, "unique_slots": True}, True, ","),
    ("kg-example-schema", {"use_attributes": True, "unique_slots": True}, True, ","),
])
def test_example_schema(source_dir, init_args, roundtrip, delimiter):
    sm = SchemaMaker(**init_args)
    src_dir = Path(INPUT_DIR) / source_dir
    # glob csv files from INPUT_DIR/source_dir
    csv_files = list(src_dir.glob('*.csv'))
    schema = sm.create_schema(csv_files, delimiter=delimiter)
    schema = sm.repair_schema(schema)
    yaml_dumper.dump(schema, to_file=os.path.join(OUTPUT_DIR, f'{source_dir}.yaml'))
    yaml = yaml_dumper.dumps(schema)
    sv = SchemaView(yaml)
    if roundtrip:
        # linkml2sheets, using original sheets as specification
        # (note that this ignores the main data in the TSV)
        roundtrip_dir = Path(OUTPUT_DIR) / "roundtrip" / source_dir
        roundtrip_dir.mkdir(parents=True, exist_ok=True)
        # print(f"CSV files: {csv_files}")
        for file in csv_files:
            exporter = SchemaExporter(schemamaker=sm, delimiter=delimiter)
            file = str(file)
            file_base = file.split("/")[-1]
            to_file = str(roundtrip_dir / file_base)
            # print(f"Writing schema to {to_file} using {file}")
            exporter.export(sv, specification=file, to_file=to_file)


