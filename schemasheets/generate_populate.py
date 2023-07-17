import logging
from typing import List

import pkg_resources
import yaml
from click import command, option, Choice
from jsonasobj2 import as_dict
from linkml_runtime import SchemaView

from schemasheets.conf.configschema import ColumnSettings
from schemasheets.schema_exporter import SchemaExporter
from schemasheets.schemasheet_datamodel import TableConfig, ColumnConfig
from typing import List, Dict

# todo write tests

# todo: include read only slots?

# todo: check metamodel if element is deprecated
#  (if it can be included in the report, the deprecation status will be reported!)
#   like subclass_of, subproperty_of ?

# todo check for inlining in addition to checking if a range class has a identifier slot?

# todo support generating an exhaustive and concise report in the same run

# todo: support slots which might require multiple columns for multiple inner keys,
#  like examples (values and description)

root_classes = ['slot_definition', "class_definition"]  # hard coding the intention to do a class slot usage report

# todo could these be semantically derived from the root_classes? other than lexical string splitting?
boilerplate_cols = ['slot', 'class']

# these a slots whose ranges are classes with identifier slots, but they still can't be included in the report
blacklist = [
    'attributes',
    'instantiates',
    'name',
    'slot_usage',
    'slots',
]

# this salvages these slots (by name) from untemplateables
requires_column_settings = {
    "examples values": {
        "name": "examples",
        "ikm_slot": "value",  # todo: what about description?
        "ikm_class": "example",
        "internal_separator": "|",

    },
    "structured_pattern": {
        "name": "structured_pattern",
        "ikm_slot": "syntax",  # todo what about interpolated and partial_match
        "ikm_class": "pattern_expression",
        "internal_separator": "|",

    },
    "unit symbol": {
        "name": "unit",
        "ikm_slot": "symbol",
        # todo what about symbol, exact mappings, ucum_code, derivation, has_quantity_kind, iec61360code
        "ikm_class": "UnitOfMeasure",
        "internal_separator": "|",
    },
}

debug_report = {
    "blacklist_skipped": []
}


def setup_logging(log_file=None, log_level=logging.INFO):
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filename=log_file,
    )


def tabulate_unique_values(value_list):
    """
    tabulate the number of appearances of each unique values in a list

    :param value_list: The list to tabulate, potentially with repeat occurrences of list items.
    :returns: A dict mapping each unique value to the number of times it appears in the list.
    """

    unique_values = set(value_list)
    value_counts = {}
    for value in unique_values:
        count = value_list.count(value)
        value_counts[value] = count

    sorted_value_counts = sorted(value_counts.items(), key=lambda x: x[1], reverse=True)

    return sorted_value_counts


def discover_source_usage(source_view: SchemaView) -> tuple[List[str], List[str]]:
    """
    Discover the meta slots and annotations used in the source code.

    :param source_view: A SchemaView of the source schema.
    :returns: A tuple of the meta slots and annotations that were discovered as used in the source schema.
    """

    discovered_meta_slots = []
    discovered_annotations = []
    source_classes = source_view.all_classes()
    for ck, cv in source_classes.items():
        cv_dict = cv.__dict__
        for cvdk, cvdv in cv_dict.items():
            if cvdv:
                discovered_meta_slots.append(cvdk)

        class_annotations = list(source_view.get_class(ck).annotations.keys())  # TODO this isn't well tested yet
        for ca in class_annotations:
            discovered_annotations.append(ca)

        for cis in source_view.class_induced_slots(ck):
            cis_dict = cis.__dict__

            for cisk, cisv in cis_dict.items():
                if cisv:
                    discovered_meta_slots.append(cisk)

            cis_annotations_dict = as_dict(cis.annotations)
            for a in cis_annotations_dict:
                discovered_annotations.append(a)

    return discovered_meta_slots, discovered_annotations


def do_usage_report(
        style: str,
        meta_view: SchemaView,
        meta_type_names: List[str],
        meta_enum_names: List[str],
        discovered_annotations: List[str],
        discovered_source_slots: List[str],
        logger: logging.Logger,
) -> tuple[TableConfig, Dict[str, Dict[str, str]]]:
    """
    Perform a usage report on the metamodel.

    :param style: The style of the usage report.
    :param meta_view: The metamodel to analyze.
    :param meta_type_names: The list of types discovered in the metamodel.
    :param meta_enum_names: The list of enums discovered in the metamodel.
    :param discovered_annotations: The list of annotations discovered in the source schema.
    :param discovered_source_slots: The list of metaslots used in the source 's SLotDefinitions and ClassDefinitions.
    :param logger: The logger to use.
    :returns: A tuple of the table config and the untemplateable metaslots.
    """

    columns_dict = {}

    # we discover which class-range slots have an identifying slot and then exclude the blacklist slots
    identifiables = {}

    slot_scan_results = {}

    # these are slots whose range is a class lacking an identifying slot
    untemplateables = {}

    discovered_cols = []
    slot_ranges = []

    discovered_annotations = list(set(discovered_annotations))

    discovered_source_slots = list(set(discovered_source_slots) - set(blacklist))
    discovered_source_slots = list(set(discovered_source_slots))
    discovered_source_slots.sort()
    discovered_annotations.sort()
    discovered_source_slots.sort()

    for current_root in root_classes:
        current_induced_slots = meta_view.class_induced_slots(current_root)
        for cis in current_induced_slots:

            temp_dict = {
                "range": cis.range,
                "multivalued": cis.multivalued,
                "type_range": cis.range in meta_type_names,
            }
            if style == "exhaustive" or cis.name in discovered_source_slots:
                if cis.name not in slot_scan_results:
                    slot_scan_results[cis.name] = temp_dict

                else:
                    if slot_scan_results[cis.name] == temp_dict:
                        continue
                    else:
                        logger.warning(f"Redefining {cis.name} from {slot_scan_results[cis.name]} to {temp_dict}")

    for c in boilerplate_cols:
        columns_dict[c] = ColumnConfig(name=c,
                                       maps_to=c,
                                       is_element_type=True,
                                       settings=ColumnSettings()
                                       )

    for rcs_k, rcs_v in requires_column_settings.items():
        if style == "exhaustive" or rcs_v['name'] in discovered_source_slots:
            temp_settings = ColumnSettings()
            if "internal_separator" in rcs_v:
                temp_settings.internal_separator = rcs_v["internal_separator"]
            if "ikm_class" in rcs_v and "ikm_slot" in rcs_v:
                temp_settings.inner_key = rcs_v["ikm_slot"]
            columns_dict[rcs_k] = ColumnConfig(
                name=rcs_v["name"],
                is_element_type=False,
                maps_to=rcs_v["name"],
                metaslot=meta_view.get_slot(rcs_v["name"]),
                settings=temp_settings
            )
            if "ikm_class" in rcs_v and "ikm_slot" in rcs_v:
                columns_dict[rcs_k].inner_key_metaslot = meta_view.induced_slot(rcs_v["ikm_slot"], rcs_v["ikm_class"])

    for ssk, ssv in slot_scan_results.items():
        if ssv["range"] not in meta_type_names and ssv["range"] not in meta_enum_names:
            slot_ranges.append(ssv["range"])

    slot_ranges.sort()

    tabulation_results = tabulate_unique_values(slot_ranges)

    for tabulation_result in tabulation_results:
        current_range = tabulation_result[0]
        # current_count = tabulation_result[1]
        current_identifier = meta_view.get_identifier_slot(current_range)
        if current_identifier:
            identifiables[current_range] = current_identifier.name
        else:
            pass

    requires_column_settings_names = []
    for rcs_k, rcs_v in requires_column_settings.items():
        requires_column_settings_names.append(rcs_v["name"])

    silenced = requires_column_settings_names + ["annotations"]

    for ssrk, ssrv in slot_scan_results.items():
        current_range = ssrv["range"]
        if current_range in meta_type_names or current_range in meta_enum_names:
            discovered_cols.append(ssrk)
        elif current_range in identifiables:
            if ssrk in blacklist:
                debug_report['blacklist_skipped'].append(ssrk)
            else:
                discovered_cols.append(ssrk)
        elif ssrk in silenced:
            continue
        else:
            untemplateables[ssrk] = ssrv

    for da in discovered_annotations:
        columns_dict[da] = ColumnConfig(
            name="annotations",
            is_element_type=False,
            maps_to="annotations",
            metaslot=meta_view.get_slot("annotations"),
            settings=ColumnSettings(inner_key=da),
        )

    discovered_cols.sort()

    for c in discovered_cols:
        c_slug = c.replace(" ", "_")
        ms = meta_view.get_slot(c)
        mv = False
        if ms:
            mv = ms.multivalued
        if mv:
            cs = ColumnSettings(internal_separator="|")
        else:
            cs = ColumnSettings()
        cc = ColumnConfig(
            maps_to=c,
            metaslot=ms,
            name=c_slug,
            settings=cs,
        )
        columns_dict[c] = cc  # use verbatim elements (not slugged) in first row?

    new_tc = TableConfig(
        column_by_element_type={'slot': 'slot', 'class': 'class'},
        columns=columns_dict
    )

    return new_tc, untemplateables


@command()
@option("--verbose", is_flag=True, help="Enable verbose logging.")
@option("--source-path", "-i", required=True,
        help="A filesystem or URL path to the schema that should be analysed and reported.")
@option("--output-path", "-o", required=True)
@option("--debug-report-path", "-d")
@option("--log-file", "-l")
@option("--report-style", "-s", type=Choice(['exhaustive', 'concise']), required=True)
def cli(source_path, output_path, debug_report_path, verbose, log_file, report_style):
    """
    A CLI tool to generate a slot usage schemasheet from the LinkML metamodel and a source schema.

    :param source_path: A filesystem or URL path to the schema that should be analysed and reported
    :param output_path: The filesystem path where the generated schemasheet will be written.
    :param debug_report_path: An optional filesystem path where a YAML report of excluded metaslots will be saved.
    :param verbose: If true, DEBUG logging will be used.
    :param log_file: An optional filesystem path where log messages will be saved.
    :param report_style: exhaustive means that all non-excluded metaslots will be included. concise means that only those metaslots used by the source schema will be included.
    """

    # in some cases it will be better to get this from a local filesystem, not a URL...
    # todo: add script/targets for downloading and merging

    if verbose:
        setup_logging(log_file, logging.DEBUG)
    else:
        setup_logging(log_file)

    logger = logging.getLogger(__name__)

    meta_yaml_path = pkg_resources.resource_filename(
        'linkml_runtime',
        'linkml_model/model/schema/meta.yaml'
    )  # todo proper platform agnostic path

    meta_view = SchemaView(meta_yaml_path, merge_imports=True)

    source_view = SchemaView(source_path, merge_imports=True)

    (discovered_source_slots, discovered_annotations) = discover_source_usage(source_view)

    root_classes.sort()

    meta_types = meta_view.schema.types
    meta_type_names = list(meta_types.keys())

    meta_enum_names = list(meta_view.all_enums().keys())
    meta_enum_names.sort()

    new_tc, untemplateables = do_usage_report(
        discovered_annotations=discovered_annotations,
        discovered_source_slots=discovered_source_slots,
        logger=logger,
        meta_enum_names=meta_enum_names,
        meta_type_names=meta_type_names,
        meta_view=meta_view,
        style=report_style,
    )

    current_exporter = SchemaExporter()
    current_exporter.export(
        schemaview=source_view,
        table_config=new_tc,
        to_file=output_path,
    )

    untemplateable_report = {}
    for uk, uv in untemplateables.items():
        untemplateable_report[uk] = uv["range"]

    debug_report['blacklist'] = blacklist
    debug_report['untemplateables'] = untemplateable_report
    debug_report['untemplateable_skipped'] = list(set(untemplateables).intersection(set(discovered_source_slots)))

    if debug_report_path:
        try:
            with open(debug_report_path, 'w') as yaml_file:
                yaml.safe_dump(debug_report, yaml_file)
            logger.warning(f"Successfully dumped the debug_report to '{debug_report_path}'.")
        except Exception as e:
            logger.warning(f"An error occurred: {e}")


if __name__ == "__main__":
    cli()
