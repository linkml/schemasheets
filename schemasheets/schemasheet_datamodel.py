"""Core data model for a SchemaSheet."""
import csv
from dataclasses import dataclass
from typing import Union, Dict, List, Any
import pkgutil
from pathlib import PurePath, Path
from functools import lru_cache
import logging
import yaml
from linkml_runtime.linkml_model import SlotDefinition, ClassDefinition, SchemaDefinition, \
    PermissibleValue, EnumDefinition, TypeDefinition, SubsetDefinition, Prefix
from linkml_runtime.linkml_model.meta import Setting

from linkml_runtime.utils.schemaview import SchemaView

from schemasheets.conf.configschema import ColumnSettings, Shortcuts

COL_NAME = str
DESCRIPTOR = str
ROW = Dict[str, Any]

# Vocabulary for types
T_SCHEMA = 'schema'
T_CLASS = 'class'
T_SLOT = 'slot'
T_ATTRIBUTE = 'attribute'
T_ENUM = 'enum'
T_PV = 'permissible_value'
T_TYPE = 'type'
T_SUBSET = 'subset'
T_PREFIX = 'prefix'
T_SETTING = 'setting'

tmap = {
    T_SCHEMA: SchemaDefinition,
    T_CLASS: ClassDefinition,
    T_SLOT: SlotDefinition,
    T_ATTRIBUTE: SlotDefinition,
    T_ENUM: EnumDefinition,
    T_PV: PermissibleValue,
    T_TYPE: TypeDefinition,
    T_SUBSET: SubsetDefinition,
    T_PREFIX: Prefix,
    T_SETTING: Setting,
}




@dataclass
class ColumnConfig:
    """
    Configuration for a single column in a schema sheet
    """
    name: COL_NAME
    maps_to: DESCRIPTOR = None
    settings: ColumnSettings = None
    metaslot: SlotDefinition = None
    inner_key_metaslot: SlotDefinition = None
    is_element_type: bool = None

    def merge_settings(self, settings: ColumnSettings) -> None:
        """
        merges specified settings into current settings

        :param settings: settings to be merged
        """
        for k, v in vars(settings).items():
            if v:
                setattr(self.settings, k, v)

    def add_info(self, info: Union[Dict, DESCRIPTOR]) -> None:
        """
        Adds configuration/settings in the form of a dict object.

        Information can be incrementally added:

        - the first piece of information should be the descriptor
        - after that individual settings can be added

        :param info: configuration
        :return:
        """
        logging.debug(f"Adding info to {self.name}: {info}")
        if self.maps_to is None:
            # The first descriptor row describes what the column maps to
            self.settings = ColumnSettings()
            if isinstance(info, dict):
                items = list(info.items())
                if len(items) != 1:
                    raise ValueError(f'Unexpected settings: {info}')
                else:
                    item = items[0]
                    self.maps_to = item[0]
                    if isinstance(item[1], dict):
                        settings = ColumnSettings(**item[1])
                    else:
                        raise ValueError(f'Expected dict after first element of {items}')
                    self.merge_settings(settings)
            else:
                self.maps_to = info
            mm = get_metamodel()
            snmap = mm.slot_name_mappings()
            for k, v in snmap.items():
                if k != v.name:
                    logging.info(f"Mismatch between slot_name_mapping key {k} slot name {v.name}")
            # TODO: use alias
            snmap['uri'] = snmap['type_uri']
            if self.maps_to.startswith("metaslot."):
                maps_to = self.maps_to.replace("metaslot.", "")
                self.metaslot = snmap[maps_to]
                self.maps_to = maps_to
            elif self.maps_to in snmap and self.maps_to != 'type':
                self.metaslot = snmap[self.maps_to]
            else:
                if self.maps_to not in tmap and self.maps_to not in Shortcuts:
                    raise ValueError(f'Cannot interpret: {self.maps_to}')
        else:
            settings = ColumnSettings(**info)
            self.merge_settings(settings)
            if settings.inner_key:
                snmap = get_metamodel().slot_name_mappings()
                if settings.inner_key in snmap:
                    self.inner_key_metaslot = snmap[settings.inner_key]



@dataclass
class TableConfig:
    """
    Configuration for an entire table / schema sheet

    """
    name: str = None
    """table name"""

    columns: Dict[COL_NAME, ColumnConfig] = None
    """maps column names to config"""

    column_by_element_type: Dict[str, COL_NAME] = None
    """maps element types (schema, class, ...) to the name of the column that represents them"""

    metatype_column: COL_NAME = None
    """Column that represents the metatype designator"""

    name_column: COL_NAME = None
    """Column that represents that name of the entity"""

    def add_info(self, col: COL_NAME, info: Union[Dict, DESCRIPTOR]) -> None:
        """
        Wrapper for :ref:`ColumnConfig.add_info`

        :param col:
        :param info:
        """
        if col not in self.columns:
            self.columns[col] = ColumnConfig(col)
        self.columns[col].add_info(info)
        if self.columns[col].maps_to == 'metatype':
            if self.metatype_column and self.metatype_column != col:
                raise ValueError(f'Multiple metatype columns not allowed: {self.metatype_column}, {col}')
            self.metatype_column = col
        if self.columns[col].maps_to == 'name':
            if self.name_column:
                raise ValueError(f'Multiple name columns not allowed: {self.name_column}, {col}')
            self.name_column = col
        if self.column_by_element_type is None:
            self.column_by_element_type = {}
        for c, cc in self.columns.items():
            if cc.maps_to in tmap:
                self.column_by_element_type[cc.maps_to] = c
                cc.is_element_type = True


@dataclass
class SchemaSheet:
    """
    A SchemaSheet consists of:

    - a collection of rows, each row representing a schema element
    - a TableConfiguration
    """
    table_config: TableConfig
    rows: List[ROW]
    start_line_number: int
    table_config_rows: List[ROW] = None

    @classmethod
    def from_csv(cls, path: str, delimiter='\t'):
        with open(path, newline='') as tsv_file:
            reader = csv.DictReader(tsv_file, delimiter=delimiter)
            return cls.from_dictreader(reader)

    @staticmethod
    def from_dictreader(reader: csv.DictReader) -> "SchemaSheet":
        """
        Reads a schemasheets TSV file parsing only header info

        :param reader:
        :return:
        """
        table_config = TableConfig(columns={})
        rows = []
        line_num = 1
        table_config_rows = []
        descriptor_line_count = 0
        for row in reader:
            logging.debug(f"ROW: {row}")
            # google sheets
            if "" in row:
                del row[""]
            k0 = list(row.keys())[0]
            if row[k0].startswith('>'):
                table_config_rows.append(row)
                line_num += 1
                descriptor_line_count += 1
                for k, v in row.items():
                    if v is not None and v.startswith('>'):
                        v = v.replace('>', '')
                    if v:
                        meta_obj = yaml.safe_load(v)
                        table_config.add_info(k, meta_obj)
                    else:
                        if line_num == 2:
                            # TODO: consider auto-interpreting
                            raise ValueError(f'Enter an interpretation for {k}')
                        logging.debug(f'Empty val for {k} in line {line_num}')
            else:
                rows.append(row)
        if descriptor_line_count == 0:
            logging.warning(f"No descriptor line found in {line_num} lines. Start line_num = {line_num}")
        return SchemaSheet(table_config=table_config,
                           table_config_rows=table_config_rows,
                           rows=rows,
                           start_line_number=line_num)

    def load_table_config(self, config: Union[dict, str, Path]) -> None:
        """
        Loads a table configuration from a file or dict

        :param config:
        :return:
        """
        if not isinstance(config, dict):
            with open(config) as f:
                config = yaml.safe_load(f)
                return self.load_table_config(config)
        for k, v in config.items():
            if isinstance(v, list):
                for v1 in v:
                    self.table_config.add_info(k, v1)
            else:
                self.table_config.add_info(k, v)

@lru_cache()
def get_metamodel() -> SchemaView:
    """
    Returns the LinkML schema metamodel as a SchemaView object

    this can be retired when https://github.com/linkml/linkml-runtime/pull/100/
    is in major release
    :return:
    """
    package = 'linkml_runtime.linkml_model.meta'
    full_path = PurePath('model') / 'schema'
    data = pkgutil.get_data(package, f'{full_path}/meta.yaml')
    return SchemaView(data.decode("utf-8"))

@lru_cache()
def get_configmodel() -> SchemaView:
    """
    Returns the Config schema metamodel as a SchemaView object

    this can be retired when https://github.com/linkml/linkml-runtime/pull/100/
    is in major release
    :return:
    """
    package = 'schemasheets.conf.configschema'
    data = pkgutil.get_data(package, f'configschema.yaml')
    return SchemaView(data.decode("utf-8"))
