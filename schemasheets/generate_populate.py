# import os
import pprint

from click import command, option
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from schemasheets.conf.configschema import ColumnSettings
from schemasheets.schema_exporter import SchemaExporter
from schemasheets.schemasheet_datamodel import TableConfig, ColumnConfig

# todo: check metamodel if element is deprecated
#   subclass_of,subproperty_of
#   use verbatim elements (not slugged) in first row?
#   add discovery of the slots that are actually used in SlotDefinitions and ClassDefinitions in the source schema

# todo check for inlining in addition to checking if a range class ahs a identifier slot?
# todo include examples, (discovered) annotations, unit, structured_pattern

root_classes = ['slot_definition', "class_definition"]
blacklist = ['attributes', 'slot_usage', 'slots']
boilerplate_cols = ['slot', 'class']


def tabulate_unique_values(list_):
    """
    tabulate the number of appearances of each unique values in a list

    Args:
        list_ (list): The list to tabulate.

    Returns:
        dict: A dict mapping each unique value to the number of times it appears in the list.
    """

    unique_values = set(list_)
    value_counts = {}
    for value in unique_values:
        count = list_.count(value)
        value_counts[value] = count

    sorted_value_counts = sorted(value_counts.items(), key=lambda x: x[1], reverse=True)

    return sorted_value_counts


@command()
@option("--meta-path", "-m", default="https://w3id.org/linkml/meta",
        help="A filesystem or URL path to the LinkML metamodel schema.")
@option("--meta-staging-path", "-s", default="meta_merged.yaml",
        help="A filesystem path for saving the merged  LinkML metamodel locally.")
@option("--source-path", "-i", default="meta_merged.yaml",
        help="A filesystem or URL path to the schema that should be reported on.")
@option("--output-path", "-o", default="populated_with_generated_spec.tsv")
# @option("--overwrite", "-o", is_flag=True, help="Overwrite the output file if it exists.")
def cli(meta_path, source_path, output_path, meta_staging_path):
    """
    A CLI tool to generate a schemasheet from a metamodel and a schema.
    """

    columns_dict = {}
    identifiables = {}
    slot_scan_results = {}
    untemplateables = {}

    discovered_cols = []
    slot_ranges = []

    meta_view = SchemaView(meta_path, merge_imports=True)

    yaml_dumper.dump(meta_view.schema, meta_staging_path)

    source_view = SchemaView(source_path, merge_imports=True)

    root_classes.sort()

    meta_types = meta_view.schema.types
    meta_type_names = list(meta_types.keys())

    meta_enum_names = list(meta_view.all_enums().keys())
    meta_enum_names.sort()

    print("\n")
    for current_root in root_classes:
        # print(f"{current_root = }")
        current_induced_slots = meta_view.class_induced_slots(current_root)
        for cis in current_induced_slots:

            temp_dict = {"range": cis.range, "multivalued": cis.multivalued, "type_range": cis.range in meta_type_names}
            # cis_slug = cis.name.replace(" ", "_")
            if cis.name not in slot_scan_results:
                slot_scan_results[cis.name] = temp_dict
            # # todo make this a debug logger message
            # else:
            #     if slot_scan_results[cis.name] == temp_dict:
            #         continue
            #     else:
            #         print(f"Redefining {cis.name} from {slot_scan_results[cis.name]} to {temp_dict}")

    for c in boilerplate_cols:
        columns_dict[c] = ColumnConfig(name=c,
                                       maps_to=c,
                                       is_element_type=True,
                                       settings=ColumnSettings()
                                       )
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

    for ssrk, ssrv in slot_scan_results.items():
        current_range = ssrv["range"]
        if current_range in meta_type_names or current_range in meta_enum_names:
            discovered_cols.append(ssrk)
        elif current_range in identifiables:
            if ssrk in blacklist:
                print(f"Skipping {ssrk} because it is in the blacklist")
            else:
                discovered_cols.append(ssrk)
        else:
            untemplateables[ssrk] = ssrv

    pprint.pprint(untemplateables)

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
            name=c,
            settings=cs,
        )
        columns_dict[c_slug] = cc

    new_tc = TableConfig(
        column_by_element_type={'slot': 'slot', 'class': 'class'},
        columns=columns_dict
    )

    current_exporter = SchemaExporter()
    current_exporter.export(
        schemaview=source_view,
        table_config=new_tc,
        to_file=output_path,
    )


if __name__ == "__main__":
    cli()
