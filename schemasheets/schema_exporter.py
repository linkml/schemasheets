import csv
import logging
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

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
               to_file: str = None, table_config: TableConfig = None):
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
            with open(to_file, 'w', encoding='utf-8') as stream:
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
                    print(f'TODO: {col_name} [{type(element).class_name}] // {col_config}')
            else:
                print(f'IGNORING: {col_name} // {col_config}')
        self.export_row(exported_row)

    def export_row(self, row: ROW):
        self.rows.append(row)



