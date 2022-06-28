# import prefixcommons as pc
import errno
import logging
import os
from typing import Dict

import click
import click_log
import pandas as pd
from linkml_runtime import SchemaView

import urllib3

# todo how to remember the yaml_dumper import

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

pd.set_option("display.max_columns", None)


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option("--selected_element", required=True)
@click.option(
    "--directory",
    required=True,
    help="Destination directory element reports",
    default="element_reports",
)
def cli(selected_element: str, directory: str):
    """
    :param selected_element:
    :param directory:
    :return:
    """

    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    memorable = "linkml:meta.yaml"
    # todo how to remember what case to use?
    # selected_element = "schema_definition"
    # # selected_element = "prefix"

    expanded = "https://w3id.org/linkml/meta.yaml"

    # todo or add a column with the selected_element value?
    first_col = f"{selected_element}_slot"

    meta_view = SchemaView(expanded)

    sis_dict, sis_names = element_to_is_dict(meta_view, "slot_definition")
    eis_dict, eis_names = element_to_is_dict(meta_view, selected_element)

    lod = []
    type_dict = {}
    type_tally: Dict[str, int] = {}
    for en in eis_names:
        ev = eis_dict[en]
        current_dict = {first_col: en}
        for sn in sis_names:
            if sn in ev:
                if ev[sn]:
                    verbatim_range = sis_dict[sn].range

                    # if sn in type_dict:
                    #     type_tally[sn] = type_tally[sn] + 1
                    # else:
                    #     type_dict[sn] = sis_dict[sn].range
                    #     type_tally[sn] = 1

                    if sn not in type_dict:
                        type_dict[sn] = verbatim_range

                    if verbatim_range in type_tally:
                        type_tally[verbatim_range] = type_tally[verbatim_range] + 1
                    else:
                        type_tally[verbatim_range] = 1

                    final = ""
                    # todo might want special handling for examples
                    # somehow the X_definitions have their names cast to strings
                    # todo: sis_dict doesn't consider the fact
                    #  that a slot might have different usage in some meta classes?
                    if sis_dict[sn].multivalued and verbatim_range in [
                        "string",
                        "class_definition",
                        "slot_definition",
                        "subset_definition",
                        "uri",
                        "uriorcurie",
                    ]:
                        final = "|".join(ev[sn])
                    else:
                        final = ev[sn]
                    current_dict[sn] = final
                    if sn == "range":
                        current_range_name = ev[sn]
                        cr_obj = meta_view.get_element(current_range_name)
                        cr_obj_type = type(cr_obj).class_name
                        current_dict["UNOFFICIAL_range_type"] = cr_obj_type
        lod.append(current_dict)
    df = pd.DataFrame(lod)

    col_names = list(df.columns)
    col_names.remove(first_col)
    col_names.sort()
    col_names = [first_col] + col_names
    df = df[col_names]

    tally_frame = pd.DataFrame(list(type_tally.items()), columns=["range", "count"])
    tally_frame.sort_values(
        by=["count", "range"], ascending=[False, True], inplace=True
    )
    tsv_file = os.path.join(directory, f"{selected_element}_range_tally.tsv")
    tally_frame.to_csv(tsv_file, sep="\t", index=False)

    type_frame = pd.DataFrame(list(type_dict.items()), columns=["slot", "range"])
    type_frame.sort_values(by="slot", ascending=True, inplace=True)
    tsv_file = os.path.join(directory, f"{selected_element}_slot_ranges.tsv")
    type_frame.to_csv(tsv_file, sep="\t", index=False)

    tsv_file = os.path.join(directory, f"{selected_element}_slot_vals.tsv")
    # df.sort_values(by="count", ascending=False, inplace=True)
    df.to_csv(tsv_file, sep="\t", index=False)

    # todo attempt to get URL for meta.yaml from "linkml:meta.yaml" alone
    # Slot: default_curi_maps
    # ordered list of prefixcommon biocontexts to be fetched to resolve id prefixes and inline prefix variables
    # meta_url = pc.expand_uri(memorable)
    # print(meta_url)

    # prefix = "linkml"
    # prefix_expansion = "https://w3id.org/linkml/"
    # w3id_expansion = "https://linkml.github.io/linkml-model/linkml/meta.yaml"

    # todo: why are some of these file NOT imported into meta.yaml?
    # https://github.com/linkml/linkml-model/tree/main/linkml_model/model/schema
    # datasets.yaml
    # meta.yaml
    # validation.yaml

    # https://linkml.github.io/linkml-model/linkml/meta.yaml
    # imports:
    #   - linkml:types
    #   - linkml:mappings
    #   - linkml:extensions
    #   - linkml:annotations

    # annotations.yaml
    # extensions.yaml
    # mappings.yaml
    # types.yaml


def element_to_is_dict(view: SchemaView, element):
    eis = view.class_induced_slots(element)
    # todo why is replacing whitespace with an underscore necessary? for broad mappings etc
    #  or use alias instead?
    eis_names = [i.name.replace(" ", "_") for i in eis]
    eis_dict = dict(zip(eis_names, eis))
    eis_names.sort()
    return eis_dict, eis_names


def flatten_some_lists(possible_list, slot_def):
    # todo add super flexible typing?
    flatten_eligible = [
        "class_definition",
        "ncname",
        "slot_definition",
        "string",
        "subset_definition",
        "uri",
        "uriorcurie",
    ]
    if slot_def.multivalued and slot_def.range in flatten_eligible:
        final = "|".join(possible_list)
    elif slot_def.multivalued and slot_def.range == "example":
        temp = []
        for i in possible_list:
            temp.append(i.value)
        final = "|".join(temp)
    else:
        final = possible_list
    return final


if __name__ == "__main__":
    cli()

# x = Example()
# x.
