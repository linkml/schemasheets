import codecs
import contextlib
import os
import sys
import csv
import logging
import tempfile
from urllib.request import urlopen

import click
import yaml
from dataclasses import dataclass
from typing import List, Union, Any, Dict, Tuple, Generator, TextIO

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import Annotation, Example
from linkml_runtime.linkml_model.meta import SchemaDefinition, ClassDefinition, Prefix, \
    SlotDefinition, EnumDefinition, PermissibleValue, SubsetDefinition, TypeDefinition, Element
from linkml_runtime.utils.schemaview import SchemaView, re

from schemasheets.schemasheet_datamodel import ColumnConfig, TableConfig, get_configmodel, get_metamodel, COL_NAME, \
    DESCRIPTOR, \
    tmap, T_CLASS, T_PV, T_SLOT, T_SUBSET, T_SCHEMA, T_ENUM, T_PREFIX, T_TYPE, SchemaSheet
from schemasheets.conf.configschema import Cardinality
from schemasheets.utils.google_sheets import gsheets_download_url
from schemasheets.utils.prefixtool import guess_prefix_expansion


class SchemaSheetRowException(Exception):
    pass


@dataclass
class SchemaMaker:
    """
    Engine for making LinkML schemas from Schema Sheets
    """
    schema: SchemaDefinition = None
    element_map: Dict[Tuple[str, str], Element] = None
    metamodel: SchemaView = None
    cardinality_vocabulary: str = None
    default_name: str = None
    unique_slots: bool = None
    gsheet_id: str = None

    def create_schema(self, csv_files: Union[str, List[str]], **kwargs) -> SchemaDefinition:
        """
        Create a LinkML schema from a collection of Schema Sheets

        :param csv_files: schema sheets
        :param kwargs:
        :return: generated schema
        """
        n = self.default_name
        if n is None:
            n = 'TEMP'
        self.schema = SchemaDefinition(id=n, name=n, default_prefix=n, default_range='string')
        if not isinstance(csv_files, list):
            csv_files = [csv_files]
        for f in csv_files:
            self.merge_sheet(f, **kwargs)
        self.schema.imports.append('linkml:types')
        self.schema.prefixes['linkml'] = Prefix('linkml', 'https://w3id.org/linkml/')
        self._tidy_slot_usage()
        prefix = self.schema.default_prefix
        if prefix not in self.schema.prefixes:
            logging.error(f'Prefix {prefix} not declared: using default')
            self.schema.prefixes[prefix] = Prefix(prefix, f'https://example.org/{prefix}/')
        return self.schema

    def _tidy_slot_usage(self):
        """
        removes all slot usages marked inapplicable

        :return:
        """
        for cn, c in self.schema.classes.items():
            inapplicable_slots = [sn for sn, s in c.slot_usage.items() if 'inapplicable' in s.annotations]
            for sn in inapplicable_slots:
                c.slots.remove(sn)
                del c.slot_usage[sn]


    def merge_sheet(self, file_name: str, delimiter='\t') -> None:
        """
        Merge information from the given schema sheet into the current schema

        :param file_name: schema sheet
        :param delimiter: default is tab
        :return:
        """
        logging.info(f'READING {file_name} D={delimiter}')
        #with self.ensure_file(file_name) as tsv_file:
        #    reader = csv.DictReader(tsv_file, delimiter=delimiter)
        with self.ensure_csvreader(file_name, delimiter=delimiter) as reader:
            schemasheet = SchemaSheet.from_dictreader(reader)
            line_num = schemasheet.start_line_number
            # TODO: check why this doesn't work
            #while rows and all(x for x in rows[-1] if not x):
            #    print(f'TRIMMING: {rows[-1]}')
            #    rows.pop()
            logging.info(f'ROWS={len(schemasheet.rows)}')
            for row in schemasheet.rows:
                try:
                    self.add_row(row, schemasheet.table_config)
                    line_num += 1
                except ValueError as e:
                    raise SchemaSheetRowException(f'Error in line {line_num}, row={row}') from e

    def add_row(self, row: Dict[str, Any], table_config: TableConfig):
        for element in self.row_focal_element(row, table_config):
            if isinstance(element, Prefix):
                name = element.prefix_prefix
            elif isinstance(element, PermissibleValue):
                name = element.text
            else:
                logging.debug(f'EL={element} in {row}')
                name = element.name
            logging.debug(f'ADDING: {row} // {name}')
            for k, v in row.items():
                if k not in table_config.columns:
                    raise ValueError(f'Expected to find {k} in {table_config.columns.keys()}')
                cc = table_config.columns[k]
                v = self.normalize_value(v, cc)
                if v:
                    # special case: class-context provided by settings
                    if cc.settings.applies_to_class:
                        actual_element = list(self.row_focal_element(row, table_config, column=k))[0]
                    else:
                        actual_element = element
                    logging.debug(f'SETTING {name} {cc.maps_to} = {v}')
                    if cc.maps_to == 'cardinality':
                        self.set_cardinality(actual_element, v)
                    elif cc.metaslot:
                        if cc.maps_to == 'examples':
                            for vi in v:
                                actual_element.examples.append(Example(value=vi))
                        elif cc.maps_to == 'annotations':
                            if cc.settings.inner_key:
                                ann = Annotation(cc.settings.inner_key, v)
                                actual_element.annotations[ann.tag] = ann
                            else:
                                anns = yaml.load(v[0])
                                for ann_key, ann_val in anns.items():
                                    actual_element.annotations[ann_key] = ann_val
                        elif isinstance(v, list):
                            #print(f'SETTING {k} to {v}')
                            setattr(actual_element, cc.maps_to, getattr(actual_element, cc.maps_to, []) + v)
                        elif isinstance(v, dict):
                            for v_k, v_v in v.items():
                                curr_dict = getattr(actual_element, cc.maps_to)
                                curr_dict[v_k] = v_v
                        else:
                            if cc.settings.inner_key:
                                curr_val = getattr(actual_element, cc.maps_to).get(cc.settings.inner_key, None)
                            else:
                                curr_val = getattr(actual_element, cc.maps_to)
                            if curr_val and curr_val != 'TEMP' and curr_val != v and \
                                    not isinstance(actual_element, SchemaDefinition) and \
                                    not isinstance(actual_element, Prefix):
                                logging.warning(f'Overwriting value for {k}, was {curr_val}, now {v}')
                                raise ValueError(f'Cannot reset value for {k}, was {curr_val}, now {v}')
                            if cc.settings.inner_key:
                                getattr(actual_element, cc.maps_to)[cc.settings.inner_key] = v
                            else:
                                setattr(actual_element, cc.maps_to, v)
                    elif cc.is_element_type:
                        logging.debug(f'Already accounted for {k}')
                    elif cc.maps_to == 'metatype':
                        logging.debug(f'Already accounted for {k}')
                    elif cc.maps_to == 'ignore':
                        logging.debug(f'Ignoring {k}')
                    else:
                        raise ValueError(f'No mapping for {k}; cc={cc}')

    def get_current_element(self, elt: Element) -> Union[Element, PermissibleValue]:
        """
        Look up an element in the current schema

        :param elt: proxy for element to look up
        :return:
        """
        sc = self.schema
        if isinstance(elt, SchemaDefinition):
            # TODO: consider multiple shemas per sheet
            return sc
        elif isinstance(elt, PermissibleValue):
            return elt
        else:
            if isinstance(elt, ClassDefinition):
                ix = sc.classes
            elif isinstance(elt, SlotDefinition):
                ix = sc.slots
            elif isinstance(elt, EnumDefinition):
                ix = sc.enums
            elif isinstance(elt, TypeDefinition):
                ix = sc.types
            elif isinstance(elt, SubsetDefinition):
                ix = sc.subsets
            else:
                raise ValueError(f'TODO: implement for type {type(elt)} in {elt}')
            if elt.name not in ix:
                ix[elt.name] = elt
            return ix[elt.name]

    def row_focal_element(self, row: Dict[str, Any], table_config: TableConfig,
                          column: COL_NAME = None) -> Generator[None, Element, None]:
        """
        Each row must have a single focal element, i.e the row is about a class, a slot, an enum, ...

        :param row:
        :param table_config:
        :return:
        """
        vmap = {}
        main_elt = None
        if table_config.metatype_column:
            tc = table_config.metatype_column
            if tc in row:
                typ = self.normalize_value(row[tc], table_config.columns[tc])
                if not table_config.name_column:
                    raise ValueError(f'name column must be set when type column ({tc}) is set; row={row}')
                name_val = row[table_config.name_column]
                if not name_val:
                    raise ValueError(f'name column must be set when type column ({tc}) is set')
                if typ == 'class':
                    vmap[T_CLASS] = [self.get_current_element(ClassDefinition(name_val))]
                elif typ == 'slot':
                    vmap[T_SLOT] = [self.get_current_element(SlotDefinition(name_val))]
                else:
                    raise ValueError(f'Unknown metatype: {typ}')
        if table_config.column_by_element_type is None:
            raise ValueError(f'No table_config.column_by_element_type')
        for k, elt_cls in tmap.items():
            if k in table_config.column_by_element_type:
                col = table_config.column_by_element_type[k]
                if col in row:
                    v = self.normalize_value(row[col])
                    if v:
                        if '|' in v:
                            vs = v.split('|')
                        else:
                            vs = [v]
                        if elt_cls == Prefix:
                            if len(vs) != 1:
                                raise ValueError(f'Cardinality of prefix col must be 1; got: {vs}')
                            pfx = Prefix(vs[0], 'TODO')
                            self.schema.prefixes[pfx.prefix_prefix] = pfx
                            vmap[k] = [pfx]
                        elif elt_cls == SchemaDefinition:
                            if len(vs) != 1:
                                raise ValueError(f'Cardinality of schema col must be 1; got: {vs}')
                            self.schema.name = vs[0]
                            vmap[k] = [self.schema]
                        else:
                            vmap[k] = [self.get_current_element(elt_cls(v)) for v in vs]
        def check_excess(descriptors):
            diff = set(vmap.keys()) - set(descriptors + [T_SCHEMA])
            if len(diff) > 0:
                raise ValueError(f'Excess slots: {diff}')
        if column:
            cc = table_config.columns[column]
            if cc.settings.applies_to_class:
                if T_CLASS in vmap and vmap[T_CLASS]:
                    raise ValueError(f'Cannot use applies_to_class in class-focused row')
                else:
                    cls = self.get_current_element(ClassDefinition(cc.settings.applies_to_class))
                    vmap[T_CLASS] = [cls]
        if T_SLOT in vmap:
            check_excess([T_SLOT, T_CLASS])
            if len(vmap[T_SLOT]) != 1:
                raise ValueError(f'Cardinality of slot field must be 1; got {vmap[T_SLOT]}')
            main_elt = vmap[T_SLOT][0]
            if T_CLASS in vmap:
                # TODO: attributes
                c: ClassDefinition
                for c in vmap[T_CLASS]:
                    #c: ClassDefinition = vmap[T_CLASS]
                    if main_elt.name not in c.slots:
                        c.slots.append(main_elt.name)
                    if self.unique_slots:
                        yield main_elt
                    else:
                        c.slot_usage[main_elt.name] = SlotDefinition(main_elt.name)
                        main_elt = c.slot_usage[main_elt.name]
                        yield main_elt
            else:
                yield main_elt
        elif T_CLASS in vmap:
            check_excess([T_CLASS])
            for main_elt in vmap[T_CLASS]:
                yield main_elt
        elif T_ENUM in vmap:
            check_excess([T_ENUM, T_PV])
            if len(vmap[T_ENUM]) != 1:
                raise ValueError(f'Cardinality of enum field must be 1; got {vmap[T_ENUM]}')
            this_enum: EnumDefinition = vmap[T_ENUM][0]
            if T_PV in vmap:
                for pv in vmap[T_PV]:
                    #pv = PermissibleValue(text=v)
                    this_enum.permissible_values[pv.text] = pv
                    yield pv
            else:
                yield this_enum
        elif T_PREFIX in vmap:
            for main_elt in vmap[T_PREFIX]:
                yield main_elt
        elif T_TYPE in vmap:
            for main_elt in vmap[T_TYPE]:
                yield main_elt
        elif T_SUBSET in vmap:
            for main_elt in vmap[T_SUBSET]:
                yield main_elt
        elif T_SCHEMA in vmap:
            for main_elt in vmap[T_SCHEMA]:
                yield main_elt
        else:
            raise ValueError(f'Could not find a focal element for {row}')

    def normalize_value(self, v: str, column_config: ColumnConfig = None) -> Any:
        """
        Given a row/column value, normalize it according to general rules and sheet settings

        General rules:

        - The strings "", ".", and "n/a" will be treated as if empty/None
        - for boolean descriptors, the values "yes" and "no" are permissible for True/False
        - leading and trailing whitespace is trimmed/stripped

        Specific settings:

        - See configschema for all options

        For example, if this method is called with a value v and a column config that has
        a regex pattern, then the regex is used to extract the value from v

        :param v:
        :param column_config: optional
        :return:
        """
        if column_config:
            metaslot = column_config.metaslot
        else:
            metaslot = None
        if v == '.':
            v = None
        elif v == '':
            v = None
        elif v == 'n/a':
            v = None
        if v and (v.startswith(' ') or v.endswith(' ')):
            if column_config:
                logging.warning(f'Stripping value: "{v}" for {column_config.name}')
            else:
                logging.warning(f'Stripping value: "{v}" (no column config)')
            v = v.strip()
        if v and column_config:
            re_match = column_config.settings.regular_expression_match
            if re_match:
                m = re.search(re_match, v)
                if m:
                    v = m.group(1)
                else:
                    logging.error(f'No match using {column_config.settings.regular_expression_match} on {v}')
                    v = None
            if column_config.settings.curie_prefix:
                if ':' in v:
                    logging.warning(f'Will not prefix {v} with {column_config.settings.curie_prefix} as it is already prefixed')
                else:
                    v = f'{column_config.settings.curie_prefix}:{v}'
            if column_config.settings.prefix:
                v = f'{column_config.settings.prefix}{v}'
            if column_config.settings.suffix:
                v = f'{column_config.settings.suffix}{v}'
            if column_config.settings.vmap:
                vmap = column_config.settings.vmap
                if v in vmap:
                    v = vmap[v].map_value
                elif '*' in vmap:
                    v = vmap['*'].map_value
                else:
                    logging.warning(f'No mapping for {v}, passing through')
        if metaslot and metaslot.range:
            rng = metaslot.range
            if rng == 'boolean':
                bmap = {
                    'yes': True,
                    'no': False,
                    'true': True,
                    'false': False
                }
                if v and v.lower() in bmap:
                    v = bmap[v.lower()]
                else:
                    v = bool(v)
        if metaslot and metaslot.multivalued and not column_config.settings.inner_key:
            if not isinstance(v, list):
                if v is None:
                    v = []
                else:
                    if column_config.settings.internal_separator:
                        v = v.split(column_config.settings.internal_separator)
                    else:
                        v = [v]
        return v


    def set_cardinality(self, element: SlotDefinition, card: str) -> None:
        """
        Sets the cardinality of a slot, allowing a variety of vocabularies.

        See configschema.yaml for all possible vocabularies, these include:

        - UML strings, e.g. '0..1'
        - text strings matching the cardinality vocabulary, e.g. 'zero to one'
        - codes used in cardinality vocabulary, e.g. O, M, ...

        The vocabulary maps to underlying LinkML primitives:

        - required
        - multivalued
        - recommended

        :param element: slot
        :param card: cardinality term
        :return: None
        """
        if not card:
            return
        # shortcuts for UML
        if card == '1':
            card = '1..1'
        if card == '*':
            card = '0..*'
        # parse UML strings as a simple grammar
        if '..' in card:
            [min, max] = card.split('..')
            element.required = int(min) > 0
            element.multivalued = max == '*' or int(max) > 1
        else:
            # lookup in cardinality vocabulary
            sv = get_configmodel()
            cvocab = self.cardinality_vocabulary
            if cvocab is None:
                cvocab = 'code'
            matches = []
            pvs = sv.get_enum('Cardinality').permissible_values
            for pv in pvs.values():
                annv = pv.annotations.get(cvocab)
                if card and annv and annv.value == card:
                    matches.append(pv)
                if card == pv.text:
                    matches.append(pv)
            if len(matches) > 1:
                raise ValueError(f'Ambiguous matches to {card}: {matches}')
            if matches:
                match = matches[0]
                if match.text == Cardinality.not_applicable.text:
                    # this slot usage will be removed post-processing
                    element.annotations['inapplicable'] = Annotation('inapplicable', 'true')
                maps_to_ann = match.annotations.get('maps_to')
                if maps_to_ann:
                    yobj = yaml.safe_load(maps_to_ann.value)
                    for k, v in yobj.items():
                        if k == 'required':
                            element.required = v
                        elif k == 'multivalued':
                            element.multivalued = v
                        elif k == 'recommended':
                            element.recommended = v
            else:
                raise ValueError(f'Cannot parse cardinality: {card} // {pvs.keys()}')

    def repair_schema(self, schema: SchemaDefinition) -> SchemaDefinition:
        sv = SchemaView(schema)
        #pfx = schema.default_prefix
        #if pfx not in schema.prefixes:
        #    schema.prefixes[pfx] = Prefix(pfx, f'http://example.org/{pfx}/')
        #    logging.info(f'Set default prefix: {schema.prefixes[pfx]}')
        prefixes = set()
        for e in list(sv.all_elements(imports=False).values()):
            # TODO: this does not include slot_usage
            map_ix = sv.get_mappings(e.name)
            for t, curies in map_ix.items():
                #print(f'xxx: {e.name} {t} N = {len(curies)} ex={e.exact_mappings}')
                if curies:
                    #print(f'REPAIRING: {e.name} N = {curies}')
                    for curie in curies:
                        if ':' in curie:
                            prefixes.add(curie.split(':')[0])
        namespaces = sv.namespaces()
        for pfx in prefixes:
            if pfx not in namespaces:
                logging.debug(f'Guessing prefix expansion: {pfx}')
                pfx_ref = guess_prefix_expansion(pfx)
                if not pfx_ref:
                    pfx_ref = f'http://example.org/{pfx}/'
                schema.prefixes[pfx] = Prefix(pfx, pfx_ref)
                logging.warning(f'Filling in missing prefix for: {pfx} => {pfx_ref}')
        # reset indexes
        sv = SchemaView(schema)
        subsets = set()
        for e in sv.all_elements().values():
            subsets.update(set(e.in_subset))
        for s in subsets:
            if s not in schema.subsets:
                schema.subsets[s] = SubsetDefinition(s)
        return schema

    @contextlib.contextmanager
    def ensure_file(self, file_name: str) -> str:
        if self.gsheet_id:
            url = gsheets_download_url(self.gsheet_id, file_name)
            stream = urlopen(url)
            yield codecs.iterdecode(stream, 'utf-8')
        else:
            with open(file_name) as file:
                yield file

    @contextlib.contextmanager
    def ensure_csvreader(self, file_name: str, delimiter=None) -> str:
        if self.gsheet_id:
            url = gsheets_download_url(self.gsheet_id, file_name)
            stream = urlopen(url)
            text_stream = codecs.iterdecode(stream, 'utf-8')
            reader = csv.DictReader(text_stream, delimiter=",")
            yield reader
        else:
            with open(file_name) as file:
                reader = csv.DictReader(file, delimiter=delimiter)
                yield reader


@click.command()
@click.option('-o', '--output',
              type=click.File(mode="w"),
              default=sys.stdout,
              help="output file")
@click.option("-n", "--name",
              help="name of the schema")
@click.option("--unique-slots/--no-unique-slots",
              default=False,
              show_default=True,
              help="All slots are treated as unique and top level and do not belong to the specified class")
@click.option("--repair/--no-repair",
              default=True,
              show_default=True,
              help="Auto-repair schema")
@click.option("--gsheet-id",
              help="Google sheets ID. If this is specified then the arguments MUST be sheet names")
@click.option("-v", "--verbose", count=True)
@click.argument('tsv_files', nargs=-1)
def convert(tsv_files, gsheet_id, output: TextIO, name, repair, unique_slots: bool, verbose: int):
    """
    Convert schemasheets to a LinkML schema

    Example:

       sheets2linkml my_schema/*tsv --output my_schema.yaml

    If your sheets are stored as google sheets, then you can pass in --gsheet-id to give the base sheet.
    In this case arguments should be the names of individual tabs

    Example:

        sheets2linkml --gsheet-id 1wVoaiFg47aT9YWNeRfTZ8tYHN8s8PAuDx5i2HUcDpvQ personinfo types -o my_schema.yaml
    """
    if verbose >= 2:
        logging.basicConfig(level=logging.DEBUG)
    elif verbose == 1:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)
    sm = SchemaMaker()
    sm.gsheet_id = gsheet_id
    sm.default_name = name
    sm.unique_slots = unique_slots
    schema = sm.create_schema(list(tsv_files))
    if repair:
        schema = sm.repair_schema(schema)
    output.write(yaml_dumper.dumps(schema))


if __name__ == '__main__':
    convert()




            

