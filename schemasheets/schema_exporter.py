import csv
import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, List, Optional, TextIO, Union

import click
from linkml_runtime.linkml_model import Element, SlotDefinition, SubsetDefinition, ClassDefinition, EnumDefinition, \
    PermissibleValue, \
    TypeDefinition, Example, Annotation
from linkml_runtime.utils.formatutils import underscore
from linkml_runtime.utils.schemaview import SchemaView

from schemasheets.schemamaker import SchemaMaker
from schemasheets.schemasheet_datamodel import TableConfig, T_CLASS, T_SLOT, SchemaSheet, T_ENUM, T_PV, T_TYPE, T_SUBSET

ROW = Dict[str, Any]


def _configuration_has_primary_keys_for(table_config: TableConfig, metatype: str) -> bool:
    for col_name, col_config in table_config.columns.items():
        if col_config.is_element_type and col_config.maps_to == metatype:
            return True
    return False


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

        EITHER a specification OR a table_config must be passed. This informs
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
        if specification is None and table_config is None:
            raise ValueError("Must specify EITHER specification OR table_config")
        for slot in schemaview.all_slots().values():
            self.export_element(slot, None, schemaview, table_config)
        if _configuration_has_primary_keys_for(table_config, T_CLASS):
            for cls in schemaview.all_classes().values():
                self.export_element(cls, None, schemaview, table_config)
                for att in cls.attributes.values():
                    self.export_element(att, cls, schemaview, table_config)
                for su in cls.slot_usage.values():
                    self.export_element(su, cls, schemaview, table_config)
        for e in schemaview.all_enums().values():
            self.export_element(e, None, schemaview, table_config)
            for pv in e.permissible_values.values():
                self.export_element(pv, e, schemaview, table_config)
        for typ in schemaview.all_types().values():
            self.export_element(typ, None, schemaview, table_config)
        for subset in schemaview.all_subsets().values():
            self.export_element(subset, None, schemaview, table_config)
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
            descriptor_rows = schemasheet.table_config_rows
            col0 = list(table_config.columns.keys())[0]
            for row in descriptor_rows:
                row[col0] = row[col0]
                writer.writerow(row)
            for row in self.rows:
                writer.writerow(row)

    def export_element(self, element: Element, parent: Optional[Element], schemaview: SchemaView, table_config: TableConfig):
        """
        Translates an individual schema element to a row

        A row is either a simple row representing a standalone element, or it represents a contextualized element, in
        which case a *parent* element is also provided.

        - A PermissibleValue element *MUST* be contextualized using a parent EnumDefinition
        - A SlotDefinition element *MAY* be contextualized using a parent ClassDefinition

        :param element: the element to be exported, e.g an instance of SlotDefinition, ClassDefinition, ...
        :param parent: contextual element; for slots, the parent may be a class; for permissible value, an Enum
        :param schemaview:
        :param table_config:
        :return:
        """
        # Step 1: determine both primary key (pk) column, a pk of any parent
        pk_col = None
        parent_pk_col = None
        for col_name, col_config in table_config.columns.items():
            if col_config.is_element_type:
                t = col_config.maps_to
                if t == T_CLASS:
                    # slots MAY be contextualized by classes
                    if isinstance(element, ClassDefinition):
                        pk_col = col_name
                    if isinstance(parent, ClassDefinition):
                        parent_pk_col = col_name
                elif t == T_SLOT and isinstance(element, SlotDefinition):
                    pk_col = col_name
                elif t == T_TYPE and isinstance(element, TypeDefinition):
                    pk_col = col_name
                elif t == T_SUBSET and isinstance(element, SubsetDefinition):
                    pk_col = col_name
                elif t == T_ENUM:
                    # permissible values MUST be contextualized by enums
                    if isinstance(element, EnumDefinition):
                        pk_col = col_name
                    if isinstance(parent, EnumDefinition):
                        parent_pk_col = col_name
                elif t == T_PV and isinstance(element, PermissibleValue):
                    pk_col = col_name
                else:
                    pass
        if not pk_col:
            logging.info(f"Skipping element: {element}, no PK")
            return
        # Step 2: iterate through all columns in the spec, and populate a row object
        exported_row = {}
        for col_name, col_config in table_config.columns.items():
            settings = col_config.settings
            # Either: (1) this column is mapped to a metamodel slot (metaslot), or
            # (2) the column is a type designator (e.g. holds a value like "class" or "slot")
            if col_config.metaslot:
                # Lookup the value of the element for this metaslot;
                # e.g. if element = SlotDefinition('phone_no', range='string'), then:
                #  - if the column has a metaslot 'name', v='phone no'
                #  - if the column has a metaslot 'range', v='string'
                v = getattr(element, underscore(col_config.metaslot.name), None)
                if v is not None and v != [] and v != {}:
                    # TODO: consider moving this to a standalone function
                    # inner function to map an atomic value
                    def repl(v: Any) -> Optional[str]:
                        if col_config.maps_to == 'examples':
                            if isinstance(v, Example):
                                return v.value
                            else:
                                raise ValueError(f"Expected Example, got {type(v)} for {v}")
                        if col_config.settings.inner_key:
                            #print(f"LOOKING UP {col_config.settings.inner_key} in {v}")
                            if isinstance(v, Annotation):
                                if v.tag == col_config.settings.inner_key:
                                    return v.value
                                else:
                                    return ''
                            return getattr(v, col_config.settings.inner_key, None)
                        if settings.curie_prefix:
                            pfx = f'{settings.curie_prefix}:'
                            if v.startswith(pfx):
                                return v.replace(pfx, '')
                            else:
                                return None
                        return v
                    # map the value (which may be a collection or an object) to a flat string
                    # representation
                    if isinstance(v, list):
                        v = [repl(v1) for v1 in v if repl(v1) is not None]
                        v = '|'.join(v)
                        if v != '':
                            exported_row[col_name] = v
                    elif isinstance(v, dict):
                        v = [repl(v1) for v1 in v.values() if repl(v1) is not None]
                        v = '|'.join(v)
                        if v != '':
                            exported_row[col_name] = v
                    else:
                        v = repl(v)
                        if v is not None:
                            exported_row[col_name] = str(v)
            elif col_config.is_element_type:
                # the column holds the metatype of the element;
                # e.g if slot=SlotDefinition(...), then the value of a column
                # 'type' that is a type designator, then the value will be 'slot'
                if pk_col == col_name:
                    if isinstance(element, PermissibleValue):
                        # permissible values are treated differently from other metamodel
                        # elements, as they have no name
                        exported_row[col_name] = element.text
                        if not parent_pk_col:
                            raise ValueError(f"Cannot have floating permissible value {element.text}")
                    else:
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


