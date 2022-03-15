import csv
import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, List, Optional, TextIO, Union

import click
from linkml_runtime.linkml_model import Element, SlotDefinition
from linkml_runtime.utils.formatutils import underscore
from linkml_runtime.utils.schemaview import SchemaView, ClassDefinition

from schemasheets.schemamaker import SchemaMaker
from schemasheets.schemasheet_datamodel import TableConfig, T_CLASS, T_SLOT, SchemaSheet

ROW = Dict[str, Any]


@dataclass
class SchemaExporter:
    """
    Exports a schema to Schema Sheets TSV format
    """
    schemamaker: SchemaMaker = field(default_factory= lambda: SchemaMaker())
    delimiter = '\t'
    rows: List[ROW] = field(default_factory=lambda: [])

    def export(self, schemaview: SchemaView, specification: str = None,
               to_file: Union[str, Path] = None, table_config: TableConfig = None):
        """
        Exports a schema to a schemasheets TSV

        EITHER a specification OR a table_config must be passed. This imforms
        how schema elements are mapped to rows

        :param schemaview:
        :param specification:
        :param to_file:
        :param table_config:
        :return:
        """
        if specification is not None:
            schemasheet = SchemaSheet.from_csv(specification, delimiter=self.delimiter)
            table_config = schemasheet.table_config
            logging.info(f'Remaining rows={len(schemasheet.rows)}')
        for slot in schemaview.all_slots().values():
            self.export_element(slot, None, schemaview, table_config)
        for cls in schemaview.all_classes().values():
            self.export_element(cls, None, schemaview, table_config)
            for att in cls.attributes.values():
                self.export_element(att, cls, schemaview, table_config)
            for su in cls.slot_usage.values():
                self.export_element(su, cls, schemaview, table_config)
        if to_file:
            if isinstance(to_file, str) or isinstance(to_file, Path):
                stream = open(to_file, 'w', encoding='utf-8')
            else:
                stream = to_file
            writer = csv.DictWriter(
                stream,
                delimiter=self.delimiter,
                fieldnames=table_config.columns.keys())
            writer.writeheader()
            for row in self.rows:
                writer.writerow(row)


    def export_element(self, element: Element, parent: Optional[Element], schemaview: SchemaView, table_config: TableConfig):
        pk_col = None
        parent_pk_col = None
        for col_name, col_config in table_config.columns.items():
            if col_config.is_element_type:
                t = col_config.maps_to
                if t == T_CLASS:
                    if isinstance(element, ClassDefinition):
                        pk_col = col_name
                    if isinstance(parent, ClassDefinition):
                        parent_pk_col = col_name
                elif t == T_SLOT and isinstance(element, SlotDefinition):
                    pk_col = col_name
                else:
                    pass
        if not pk_col:
            return
        exported_row = {}
        for col_name, col_config in table_config.columns.items():
            settings = col_config.settings
            if col_config.metaslot:
                v = getattr(element, underscore(col_config.metaslot.name), None)
                if v is not None and v != [] and v != {}:
                    exclude = False
                    def repl(v: str) -> Optional[str]:
                        if settings.curie_prefix:
                            pfx = f'{settings.curie_prefix}:'
                            if v.startswith(pfx):
                                return v.replace(pfx, '')
                            else:
                                return None
                        return v
                    if isinstance(v, list):
                        v = [repl(v1) for v1 in v if repl(v1) is not None]
                        v = '|'.join(v)
                        if v != '':
                            exported_row[col_name] = v
                    else:
                        v = repl(v)
                        if v is not None:
                            exported_row[col_name] = str(v)
            elif col_config.is_element_type:
                if pk_col == col_name:
                    exported_row[col_name] = element.name
                elif parent_pk_col == col_name:
                    exported_row[col_name] = parent.name
                else:
                    logging.info(f'TODO: {col_name} [{type(element).class_name}] // {col_config}')
            else:
                logging.info(f'IGNORING: {col_name} // {col_config}')
        self.export_row(exported_row)

    def export_row(self, row: ROW):
        self.rows.append(row)

    def is_slot_redundant(self, slot: SlotDefinition, schemaview: SchemaView):
        for c in schemaview.all_classes().values():
            if slot.name in c.slots:
                pass


@click.command()
@click.option('-o', '--output',
              help="output file")
@click.option("-d", "--output-directory",
              help="folder in which to store resulting TSVs")
@click.option("-s", "--schema",
              required=True,
              help="Path to the schema")
@click.option("--overwrite/--no-overwrite",
              default=False,
              show_default=True,
              help="If set, then overwrite existing schemasheet files if they exist")
@click.option("--append-sheet/--no-append-sheet",
              default=False,
              show_default=True,
              help="If set, then append to existing schemasheet files if they exist")
@click.option("--unique-slots/--no-unique-slots",
              default=False,
              show_default=True,
              help="All slots are treated as unique and top level and do not belong to the specified class")
@click.option("-v", "--verbose", count=True)
@click.argument('tsv_files', nargs=-1)
def export_schema(tsv_files, output_directory, output: TextIO, overwrite: bool, append_sheet: bool,
                  schema, unique_slots: bool, verbose: int):
    """
    Convert LinkML schema to schemasheets

    Convert a schema to a single sheet, writing on stdout:

        linkml2sheets -s my_schema.yaml my_schema_spec.tsv > my_schema.tsv

    As above, with explicit output:

        linkml2sheets -s my_schema.yaml my_schema_spec.tsv -o my_schema.tsv

    Convert schema to multisheets, writing output to a folder:

        linkml2sheets -s my_schema.yaml specs/*.tsv -d output

    Convert schema to multisheets, writing output in place:

        linkml2sheets -s my_schema.yaml sheets/*.tsv -d sheets --overwrite

    Convert schema to multisheets, appending output:

        linkml2sheets -s my_schema.yaml sheets/*.tsv -d sheets --append


    """
    if verbose >= 2:
        logging.basicConfig(level=logging.DEBUG)
    elif verbose == 1:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)
    if output is not None and output_directory:
        raise ValueError(f'Cannot combine output-directory and output options')
    if output is not None and len(tsv_files) > 1:
        raise ValueError(f'Cannot use output option with multiple sheets')
    if append_sheet:
        raise NotImplementedError(f'--append-sheet not yet implemented')
    exporter = SchemaExporter()
    sv = SchemaView(schema)
    for f in tsv_files:
        if output_directory:
            outpath: Path = Path(output_directory) / Path(f).name
        else:
            if output is not None:
                outpath = Path(output)
            else:
                outpath = sys.stdout
        if isinstance(outpath, Path) and outpath.exists():
            if overwrite:
                logging.info(f'Overwriting: {outpath}')
            else:
                raise PermissionError(f'Will not overwrite {outpath} unless --overwrite is set')
        exporter.export(sv, specification=f, to_file=outpath)


if __name__ == '__main__':
    export_schema()


