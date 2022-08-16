import csv
import logging
import os
import pprint
import re
from dataclasses import dataclass
from typing import List, Dict, Optional, Any

import click
import click_log
import yaml
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import EnumDefinition, PermissibleValue

from schemasheets.schema_exporter import SchemaExporter

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

SLOT_NAME = str
METAMODEL_SLOT_NAME = str
PROJECT_SLOT_NAME = str
SLOT_VALUE = str
SLOT_USAGE_COUNT = int


# todo test first

# todo too much writing to file and reading back in
#  also, there must be something better than LinkML->YAML->Dict

# todo: reflect the classes that use a given slot on slot-only rows (via domain of)
#  see prepare_merged_report() workarround

# todo: work on YAML-serialized alt_descriptions columns

# todo: write a style guide, esp use of external terms and consistent grammar
#  NMDC Schema Style Guide
#  https://docs.google.com/document/d/1KwO5kG79MWuS4eaRn6n9B3Tth4Hg_vo7jPQDqdv-yD4/edit#

# todo: group and or describe mappings
# todo: comments, notes, todos distinctions

# todo: clearer class and method names, docstrings, typing


@dataclass
class TemplateWizard:
    """
    models the intermediate states while converting the metamodel and some project schema into a bare,
    then populated schemsheets template
    """

    meta_view: SchemaView
    project_view: SchemaView

    slot_attributes: Optional[
        Dict[SLOT_NAME, Dict[METAMODEL_SLOT_NAME, SLOT_VALUE]]
    ] = None

    # todo refactor this? dict with name and count had been handy for writing to CSV
    #  but were not doing that anymore
    proj_elem_usage: Optional[List[Dict[PROJECT_SLOT_NAME, Any]]] = None

    class_slots_slotnames: Optional[List[PROJECT_SLOT_NAME]] = None

    def get_element_annotations(self) -> List:
        """
        iteratively collects all element annotations
        """
        elements = self.project_view.all_elements()
        annotations = set()
        for ek, ev in elements.items():
            if ev.annotations:
                for current_annotation in ev.annotations:
                    annotations.add(current_annotation)
        annotations = list(annotations)
        annotations.sort()
        return annotations

    def get_slot_names(self, element: str, selected_schema: str) -> List[str]:
        slots = []
        if selected_schema == "meta":
            slots = self.meta_view.class_induced_slots(element)
        elif selected_schema == "project":
            slots = self.project_view.class_induced_slots(element)
        # todo was using alias... name doesn't seem to help with undefined slots
        slot_names = [str(slot.alias) for slot in slots]
        return slot_names

    def return_slot_attributes(self, slot_list: List[str]):
        desired_attributes = ["multivalued", "name", "range", "recommended", "required"]
        slot_attributes = {}
        for cs_name, cs_obj in self.meta_view.all_slots().items():
            if cs_name in slot_list:
                for current_desired in desired_attributes:
                    if cs_name not in slot_attributes:
                        slot_attributes[cs_name] = {}
                    slot_attributes[cs_name][current_desired] = getattr(
                        cs_obj, current_desired
                    )
        return slot_attributes

    def get_slot_attributes(self):
        class_names = self.get_slot_names(
            element="class_definition", selected_schema="meta"
        )
        slot_names = self.get_slot_names(
            element="slot_definition", selected_schema="meta"
        )
        class_slots_slotnames = list(set(class_names).union(set(slot_names)))
        class_slots_slotnames.sort()
        current_slot_attributes = self.return_slot_attributes(class_slots_slotnames)
        self.class_slots_slotnames = class_slots_slotnames
        self.slot_attributes = current_slot_attributes

    def get_proj_elem_usage(self):
        # todo I'm not convinced that this is getting all frequently used keys
        #  didn't pick up title or notes for NMDC schema
        #  needs merging?
        # todo this DOES pick up keys like annotation and permissible value names, which might not be desirable
        #  see frequent_relevant and ut_meta_elements
        project_yaml = yaml_dumper.dumps(self.project_view.schema)
        project_dict = yaml.safe_load(project_yaml)

        outer_list = traverse_and_collect_dict_keys(project_dict)  # todo rename this

        key_counts = list_to_count_dict(outer_list)

        common_keys_lod = [
            {"key": k, "count": v} for k, v in key_counts.items()
        ]  # todo rename this

        self.proj_elem_usage = common_keys_lod

    def get_frequent_elements(self, count_threshold: int):
        meets_threshold = [
            i["key"] for i in self.proj_elem_usage if i["count"] >= count_threshold
        ]
        under_threshold = [
            i["key"] for i in self.proj_elem_usage if i["count"] < count_threshold
        ]
        return meets_threshold, under_threshold

    def whittle_columns(self):
        pass

    def declare_multivalueds(self, column_list):
        multivalued_indicator = 'internal_separator: "|"'
        multivalued_declarations = []
        for list_item in column_list:
            emission = None
            with_spaces = list_item.replace("_", " ")
            emitted_obj = self.meta_view.get_slot(
                list_item
            )  # todo better upfront name/alias handling
            if not emitted_obj:
                emitted_obj = self.meta_view.get_slot(
                    with_spaces
                )  # todo better upfront name/alias handling
            if emitted_obj:
                if emitted_obj.multivalued:
                    emission = multivalued_indicator
                else:
                    pass
            else:
                pass
            multivalued_declarations.append(emission)
        return multivalued_declarations

    def declare_annoations(self, r0, r1, r2, aa):
        annotation_declarations = []
        for idx, list_item in enumerate(r0):
            if list_item in aa:
                annotation_declarations.append(f"inner_key: {list_item}")
                r1[idx] = "annotations"
            else:
                annotation_declarations.append(r2[idx])

        return r1, annotation_declarations

    def add_card_and_range(self, r0):
        original_to_card_and_range = {}
        with_card_and_range = []
        for list_item in r0:
            with_spaces = list_item.replace("_", " ")
            emitted_obj = self.meta_view.get_slot(
                list_item
            )  # todo better upfront name/alias handling
            if not emitted_obj:
                emitted_obj = self.meta_view.get_slot(
                    with_spaces
                )  # todo better upfront name/alias handling
            if emitted_obj:
                min_card = "0"
                max_card = "1"
                if emitted_obj["required"]:
                    min_card = "1"
                if emitted_obj["multivalued"]:
                    max_card = "*"
                card_string = f"{list_item}: {min_card}..{max_card}"
                if emitted_obj["recommended"]:
                    card_string += " (recommended)"
                if emitted_obj["range"]:
                    card_string += f" x {emitted_obj['range']}"
                else:
                    card_string += f" x {self.meta_view.schema.default_range}"
            else:
                # todo actually, the rang should be the range of the abbreviated element's name,
                #  like class -> class_definition.name.range
                card_string = f"{list_item}: {self.meta_view.schema.default_range}"
            with_card_and_range.append(card_string)
            original_to_card_and_range[list_item] = card_string
        return with_card_and_range, original_to_card_and_range

    def get_slots_to_classes(self, selected_classes=[]):
        classes_selected = False
        if selected_classes:
            classes_selected = True

        slots_to_classes = {}
        classes = list(self.project_view.all_classes().keys())
        for current_class in classes:
            # induced_slots = self.project_view.get_slots_for_class(current_class)
            induced_slots = self.project_view.class_induced_slots(current_class)
            induced_slot_names = [i.name for i in induced_slots]
            for slot_name in induced_slot_names:
                if slot_name in slots_to_classes:
                    if current_class in selected_classes or not classes_selected:
                        slots_to_classes[slot_name].append(current_class)
                elif current_class in selected_classes or not classes_selected:
                    slots_to_classes[slot_name] = [current_class]
        writable = []
        for k, v in slots_to_classes.items():
            unique_classes = list(set(v))
            unique_classes.sort()
            joined_classes = "|".join(unique_classes)
            writable.append({"slot": k, "classes": joined_classes})

        return writable

    def prepare_merged_report(self, populated_template, lhs_header, slot_classes_rels):
        relevant_classes_label = "relevant_classes"
        # todo this shouldn't be hard-coded
        old = "class: string"
        new = "overriding_class"
        rels_direct = {i["slot"]: i["classes"] for i in slot_classes_rels}
        combined_headers = lhs_header.copy()
        combined_rekeyed = list(map(lambda x: x.replace(old, new), combined_headers))
        combined_rekeyed.insert(2, relevant_classes_label)
        merged_list = []
        for i in populated_template:
            row_dict = i
            row_dict[relevant_classes_label] = ""
            current_slot = i[lhs_header[1]]
            if current_slot:
                if current_slot in rels_direct:
                    row_dict[relevant_classes_label] = rels_direct[current_slot]
            val_to_rekey = row_dict[old]
            del row_dict[old]
            row_dict[new] = val_to_rekey
            merged_list.append(row_dict)
        return merged_list, combined_rekeyed

    def get_meta_element_names(self):
        meta_elements = self.meta_view.all_elements()
        meta_element_names = [k for k, v in meta_elements.items()]
        return meta_element_names

    def get_project_element_types(self):
        project_elements = self.project_view.all_elements()
        project_element_types = {
            k: type(v).class_name for k, v in project_elements.items()
        }
        return project_element_types

    def get_types_project_elements(self, project_element_types):
        types_project_elements = {}
        for k, v in project_element_types.items():
            if v in types_project_elements:
                types_project_elements[v].append(k)
            else:
                types_project_elements[v] = [k]
        return types_project_elements


def traverse_and_collect_dict_keys(dict_in: Dict, inner_list: List = []) -> List:
    """
    recursively collects all keys from a dictionary
    """
    for key, value in dict_in.items():
        logger.debug(key)
        if isinstance(value, dict):
            traverse_and_collect_dict_keys(value, inner_list)
            inner_list.append(key)
        else:
            inner_list.append(key)
    return inner_list


def list_to_count_dict(list_in: List) -> Dict:
    """
    Takes a list of strings and returns a dictionary of counts
    """
    count_dict = {}
    for item in list_in:
        logger.debug(item)
        if item in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1
    return count_dict


def make_colspec_row(column_list):
    colspec_row = column_list
    if colspec_row[0]:
        colspec_row[0] = "> " + colspec_row[0]
    else:
        colspec_row[0] = ">"
    return colspec_row


@click.group()
def cli():
    pass


# start slots sub command
@click.command()
@click_log.simple_verbosity_option(logger)
@click.option(
    "--meta-source",
    show_default=True,
    default="https://raw.githubusercontent.com/linkml/linkml-model/main/linkml_model/model/schema/meta.yaml",
    help="HTTP or filesystem path to some version of the LinkML meta model",
)
@click.option(
    "--project-source",
    help="HTTP or filesystem path to your project schema",
    required=True,
)
@click.option(
    "--element",
    type=click.Choice([
        "slots",
        "classes",
    ]),
    multiple=False,
    required=True,
    help="For which meta element do you want a template?",
)
@click.option(
    "--min-occurrences",
    show_default=True,
    default=1,
    help="Don't make a column for elements that appear less than N times in your project schema.",
)
@click.option(
    "--always-include-cols",
    type=click.Choice(["notes"]),
    show_default=True,
    multiple=True,
    default=["notes"],
    help="Slots that should always be included. Order not specified.",
)
@click.option(
    "--complex_cols",
    type=click.Choice(["annotations", "alt_descriptions"]),
    multiple=True,
    show_default=True,
    default=[
        "annotations",
        "alt_descriptions",
    ],
    help="Complex slots that shouldn't appear as direct YAML serializations.",
)  # todo skipped because I (or schemasheets) don't have a solution for these YAML serializations yet
@click.option(
    "--template-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    required=True,
    help="""Where should the empty template be written? FILENAME WILL BE AUTOGENERATED!""",
)
@click.option(
    "--populated_dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    required=True,
    help="""Where should the populated template be written? FILENAME WILL BE AUTOGENERATED!""",
)
def named_element(meta_source, project_source, min_occurrences, always_include_cols, template_dir,
                  populated_dir, complex_cols, element):
    logger.debug(template_dir)

    if element == "slots":
        skip_cols = [
            "class_uri",
            "id_prefixes",
            "name",
            "slots",
            "slot_usage",
        ]
        initial_cols = ["slot", "title"]
    elif element == "classes":
        initial_cols = ["class", "title"]
        skip_cols = [
            'domain',
            'examples',
            'identifier',
            'inlined',
            'inlined_as_list',
            'multivalued',
            'name',
            'range',
            'required',
            'slot',
            'slot_uri',
            'slot_usage',
            'slots',
        ]

    logger.info(f"creating meta view from {meta_source}")
    meta_view = SchemaView(meta_source)
    logger.info(f"found schema {meta_view.schema.name} in {meta_source}")

    logger.info(f"creating project view from {meta_source}")
    project_view = SchemaView(project_source)
    logger.info(f"found schema {project_view.schema.name} in {project_source}")

    wizard_instance = TemplateWizard(meta_view=meta_view, project_view=project_view)

    element_annotations = wizard_instance.get_element_annotations()

    logger.debug(element_annotations)

    template_path = os.path.join(
        template_dir,
        f"generated_{wizard_instance.project_view.schema.name}_{element}.tsv",
    )

    wizard_instance.get_slot_attributes()

    logger.debug(wizard_instance.slot_attributes)

    wizard_instance.get_proj_elem_usage()

    logger.debug(wizard_instance.proj_elem_usage)

    frequent_elements, under_threshold = wizard_instance.get_frequent_elements(
        count_threshold=min_occurrences
    )

    logger.debug(frequent_elements)

    logger.debug(under_threshold)

    meta_element_names = wizard_instance.get_meta_element_names()
    meta_element_names.sort()

    project_element_types = wizard_instance.get_project_element_types()
    logger.debug(project_element_types)

    types_project_elements = wizard_instance.get_types_project_elements(
        project_element_types
    )
    logger.debug(types_project_elements)

    under_threshold.sort()
    logger.info(f"under_threshold: {under_threshold}")
    logger.debug(f"element_annotations: {element_annotations}")
    logger.debug(f"meta_element_names: {meta_element_names}")

    frequent_relevant = list(
        set(frequent_elements).intersection(
            set(wizard_instance.class_slots_slotnames)
        )
    )

    special_cols = list(
        (set(initial_cols).union(set(skip_cols))).union(set(complex_cols))
    )
    cols_to_sort = list(set(frequent_relevant).difference(set(special_cols)))

    cols_to_sort = list(set(cols_to_sort).union(set(always_include_cols)))

    cols_to_sort.sort()

    cols_to_emit = list(initial_cols) + cols_to_sort + element_annotations

    row0 = cols_to_emit.copy()  # intended as user friendly header
    row1 = cols_to_emit.copy()  # meta element names

    row2 = wizard_instance.declare_multivalueds(row0)
    row1, row2 = wizard_instance.declare_annoations(
        r0=row0, r1=row1, r2=row2, aa=element_annotations
    )
    row1 = make_colspec_row(row1)
    row2 = make_colspec_row(row2)
    # row0, original_to_card_and_range = wizard_instance.add_card_and_range(row0)

    logger.info(f"writing template to {template_path}")
    with open(template_path, "wt") as out_file:
        tsv_writer = csv.writer(out_file, delimiter="\t")
        tsv_writer.writerow(row0)
        tsv_writer.writerow(row1)
        tsv_writer.writerow(row2)

    populated_tsv = os.path.join(
        populated_dir,
        f"generated_{wizard_instance.project_view.schema.name}_{element}.tsv",
    )

    logger.info(f"populating template to {populated_tsv}")
    exporter = SchemaExporter()
    exporter.export(
        wizard_instance.project_view,
        specification=template_path,
        to_file=populated_tsv,
    )


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option(
    "--meta-source",
    show_default=True,
    default="https://raw.githubusercontent.com/linkml/linkml-model/main/linkml_model/model/schema/meta.yaml",
    help="HTTP or filesystem path to some version of the LinkML meta model",
)
@click.option(
    "--project-source",
    help="HTTP or filesystem path to your project schema",
    required=True,
)
@click.option(
    "--template-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    required=True,
    help="""Where should the empty template be written? FILENAME WILL BE AUTOGENERATED!""",
)
def enums(meta_source, project_source, template_dir):
    logger.info(f"creating meta view from {meta_source}")
    meta_view = SchemaView(meta_source)
    logger.info(f"found schema {meta_view.schema.name} in {meta_source}")

    logger.info(f"creating project view from {meta_source}")
    project_view = SchemaView(project_source)
    logger.info(f"found schema {project_view.schema.name} in {project_source}")

    wizard_instance = TemplateWizard(meta_view=meta_view, project_view=project_view)

    logger.info(f"Processing enums and permissible values")

    # trying a different approach vis a vis the classes_slots style

    initial_cols = ["enum", "permissible_value", "meaning"]

    # what slots are allowed for enums with induction
    e_slots = wizard_instance.meta_view.induced_class("enum_definition").attributes
    e_slot_keys = list(e_slots.keys())
    e_slot_keys.sort()
    # logger.info(f"enum slots: {e_slot_keys}")

    # what slots are allowed for permissible values with induction
    pv_slots = wizard_instance.meta_view.induced_class("enum_definition").attributes
    pv_slot_keys = list(pv_slots.keys())
    pv_slot_keys.sort()
    # logger.info(f"pv slots: {pv_slot_keys}")

    proj_enums = wizard_instance.project_view.all_enums()
    enum_names = list(proj_enums.keys())
    enum_names.sort()
    # logger.info(f"enum names: {enum_names}")

    # todo common metadata?
    always_do = set()
    desired_ranges = [
        "example",
        "integer",
        "string",
        "subset_definition",
        "uri",
        "uriorcurie",
    ]
    ignored_ranges = "alt_description", "structured_alias"
    cd = wizard_instance.meta_view.induced_class("common_metadata")
    cd_slots = cd.attributes
    for k, v in cd_slots.items():
        if v.range in desired_ranges:
            always_do.add(v.alias)

    # todo remember key vs name vs alias
    # todo maybe include from_schema?
    # todo identify and flag read only cols
    dont_bother_with = ["name", "text"]

    # todo check for requireds, multivalueds and ranges

    e_allowed_and_used = set()
    pv_allowed_and_used = set()
    annotations_used = set()
    for k, v in proj_enums.items():
        e_dict = v.__dict__
        for vk, vv in e_dict.items():
            if vk in e_slot_keys and vk not in dont_bother_with and vv:
                if vk == "permissible_values":
                    for pk, pv in vv.items():
                        p_dict = pv.__dict__
                        for pvk, pvv in p_dict.items():
                            if pvk == "annotations":
                                if pvv:
                                    for inner_key, inner_v in pvv.items():
                                        # logger.info(f"annotations: {inner_key}")
                                        annotations_used.add(inner_key)
                            elif (
                                    pvk in pv_slot_keys
                                    and pvk not in dont_bother_with
                                    and pvv
                            ):
                                # logger.info(f"pv key: {pvk}")
                                alias_check = wizard_instance.meta_view.get_element(
                                    pvk
                                )
                                if alias_check.alias:
                                    # logger.info(
                                    #     f"pv key alias: {alias_check.alias}"
                                    # )
                                    pv_allowed_and_used.add(alias_check.alias)
                                else:
                                    # logger.info(f"pv key: {pvk}")
                                    pv_allowed_and_used.add(pvk)

                else:
                    # todo need underlined form not white-spaced form
                    e_allowed_and_used.add(vk)

    for_row0 = [always_do, e_allowed_and_used, pv_allowed_and_used]

    row0 = list(set().union(*for_row0))
    row0.sort()
    au_list = list(annotations_used)
    au_list.sort()
    row0 = initial_cols + row0 + au_list

    row1 = []
    for i in row0:
        if i in annotations_used:
            row1.append("annotations")
        else:
            row1.append(i)

    row2 = []
    for i in row0:
        # todo determine multivalued columns
        # todo would be better to check in induced slots?

        i_obj = wizard_instance.meta_view.get_slot(i)
        i_multivalued = False
        if i_obj and i_obj.multivalued:
            i_multivalued = True

        with_spaces = i.replace("_", " ")
        ws_multivalued = False
        ws_obj = wizard_instance.meta_view.get_slot(with_spaces)
        if ws_obj and ws_obj.multivalued:
            ws_multivalued = True

        if i_multivalued or ws_multivalued:
            row2.append('internal_separator: "|"')
        elif i in annotations_used:
            row2.append(f"inner_key: {i}")
        else:
            row2.append("")

    row1_decorated = make_colspec_row(row1)
    row2_decorated = make_colspec_row(row2)

    enum_template_file = os.path.join(
        template_dir,
        f"generated_{wizard_instance.project_view.schema.name}_enums.tsv",
    )
    with open(enum_template_file, "w") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerows([row0, row1_decorated, row2_decorated])


@click.command()
@click_log.simple_verbosity_option(logger)
# sources
@click.option(
    "--meta_source",
    show_default=True,
    default="https://raw.githubusercontent.com/linkml/linkml-model/main/linkml_model/model/schema/meta.yaml",
    help="HTTP or filesystem path to some version of the LinkML meta model",
)
@click.option(
    "--project_source",
    help="HTTP or filesystem path to your project schema",
    required=True,
)
@click.option(
    "--min_occurrences",
    show_default=True,
    default=2,
    help="Don't make a column for elements that appear less than N times in your project schema.",
)
@click.option(
    "--initial_cols",
    type=click.Choice(["class", "slot", "title"]),
    multiple=True,
    show_default=True,
    default=["class", "slot", "title"],
    help="Slots that should appear as the left-most columns.",
)
@click.option(
    "--always_include_cols",
    type=click.Choice(["notes"]),
    show_default=True,
    multiple=True,
    default=["notes"],
    help="Slots that should always be included. Order not specified.",
)
@click.option(
    "--complex_cols",
    type=click.Choice(["annotations", "alt_descriptions"]),
    multiple=True,
    show_default=True,
    default=[
        "annotations",
        "alt_descriptions",
    ],
    help="Complex slots that shouldn't appear as direct YAML serializations.",
)  # todo skipped because I (or schemasheets) don't have a solution for these YAML serializations yet
@click.option(
    "--skip_cols",
    type=click.Choice(["slots", "slot_usage", "name"]),
    multiple=True,
    show_default=True,
    default=[
        "slots",
        "slot_usage",
        "name",
    ],
    help="Slots that should not appear as columns.",
)
# always (?) skip these columns.
# name is ambiguous.
# slot usage should be broken out into slot usage rows.
# slots *might* be useful for a class-only template style
@click.option(
    "--col_sorting",
    type=click.Choice(["alphabetical", "by_usage_count"]),
    multiple=False,
    show_default=True,
    default="alphabetical",
    help="""Besides initial columns,
              should the rest appear alphabetically or in order of use in project schema?""",
)
@click.option(
    "--template_dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    required=True,
    help="""Where should the empty template be written? FILENAME WILL BE AUTOGENERATED!""",
)
@click.option(
    "--populated_dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    required=True,
    help="""Where should the populated template be written? FILENAME WILL BE AUTOGENERATED!""",
)
@click.option(
    "--selected_classes",  # todo check if the class is present in the project schema
    multiple=True,
    help="Only show knowledge about these classes and their asserted slots. Defaults to all.",
)
@click.option(
    "--all_slot_class_rels",
    type=click.Path(file_okay=True, dir_okay=False),
    required=False,
    help="""File path for saving all exhaustive slot-class relationships""",
)
@click.option(
    "--filtered_slot_class_rels",
    type=click.Path(file_okay=True, dir_okay=False),
    required=False,
    help="""File path for saving exhaustive report relating selected classes to thier slots""",
)
@click.option(
    "--merged_filtered_rels",
    type=click.Path(file_okay=True, dir_okay=False),
    required=False,
    help="""File path for saving classes_slots report merged with filtered slot-class relationships. 
              Requires --template_style classes_slots --filtered_slot_class_rels""",
)
#         always_cols = []  # todo
def classes_slots(
        meta_source,
        project_source,
        min_occurrences,
        initial_cols,
        always_include_cols,
        skip_cols,
        col_sorting,
        template_dir,
        populated_dir,
        selected_classes,
        complex_cols,
        all_slot_class_rels,
        filtered_slot_class_rels,
        merged_filtered_rels,
) -> None:
    """Create a schemasheets template based on meta-expected and project-observed elements."""

    logger.info(f"creating meta view from {meta_source}")
    meta_view = SchemaView(meta_source)
    logger.info(f"found schema {meta_view.schema.name} in {meta_source}")

    logger.info(f"creating project view from {meta_source}")
    project_view = SchemaView(project_source)
    logger.info(f"found schema {project_view.schema.name} in {project_source}")

    wizard_instance = TemplateWizard(meta_view=meta_view, project_view=project_view)

    # todo doesn't get PV annotations for better or worse since they're not "elements"
    #  also, this list could include annotations that aren't relevant to the selected classes and their slots
    element_annotations = wizard_instance.get_element_annotations()

    # todo: overwrite handling
    #  bad path should be handled by click?
    template_path = os.path.join(
        template_dir,
        f"generated_{wizard_instance.project_view.schema.name}_classes_slots.tsv",
    )
    populated_tsv = os.path.join(
        populated_dir,
        f"generated_{wizard_instance.project_view.schema.name}_classes_slots.tsv",
    )

    wizard_instance.get_slot_attributes()

    wizard_instance.get_proj_elem_usage()

    frequent_elements, under_threshold = wizard_instance.get_frequent_elements(
        count_threshold=min_occurrences
    )

    meta_element_names = wizard_instance.get_meta_element_names()
    meta_element_names.sort()

    project_element_types = wizard_instance.get_project_element_types()
    logger.debug(project_element_types)

    types_project_elements = wizard_instance.get_types_project_elements(
        project_element_types
    )
    logger.debug(types_project_elements)

    under_threshold.sort()
    # print(f"under_threshold: {under_threshold}")
    # print(f"element_annotations: {element_annotations}")
    # print(f"meta_element_names: {meta_element_names}")

    frequent_relevant = list(
        set(frequent_elements).intersection(
            set(wizard_instance.class_slots_slotnames)
        )
    )
    special_cols = list(
        (set(initial_cols).union(set(skip_cols))).union(set(complex_cols))
    )
    cols_to_sort = list(set(frequent_relevant).difference(set(special_cols)))
    cols_to_sort = list(set(cols_to_sort).union(set(always_include_cols)))

    if col_sorting == "alphabetical":
        cols_to_sort.sort()
    elif col_sorting == "by_usage_count":
        count_sorted = sorted(
            wizard_instance.proj_elem_usage,
            key=lambda lx: lx["count"],
            reverse=True,
        )
        cols_to_sort = [i["key"] for i in count_sorted if i["key"] in cols_to_sort]
    cols_to_emit = list(initial_cols) + cols_to_sort + element_annotations

    row0 = cols_to_emit.copy()  # intended as user friendly header
    row1 = cols_to_emit.copy()  # meta element names

    # row2 = None
    row2 = wizard_instance.declare_multivalueds(row0)
    row1, row2 = wizard_instance.declare_annoations(
        r0=row0, r1=row1, r2=row2, aa=element_annotations
    )
    row1 = make_colspec_row(row1)
    row2 = make_colspec_row(row2)
    row0, original_to_card_and_range = wizard_instance.add_card_and_range(row0)

    logger.info(f"writing template to {template_path}")
    with open(template_path, "wt") as out_file:
        tsv_writer = csv.writer(out_file, delimiter="\t")
        tsv_writer.writerow(row0)
        tsv_writer.writerow(row1)
        # if row2:
        tsv_writer.writerow(row2)

    logger.info(f"populating template to {populated_tsv}")
    exporter = SchemaExporter()
    exporter.export(
        wizard_instance.project_view,
        specification=template_path,
        to_file=populated_tsv,
    )

    if len(selected_classes) > 0:

        sn = wizard_instance.project_view.schema.name

        filtered_populated = os.path.join(
            populated_dir, f"generated_filtered_{sn}_classes_slots.tsv"
        )
        logger.info(
            f"writing rows relevant to {selected_classes} to {filtered_populated}"
        )

        all_relevant_slots = []
        for current_selected in selected_classes:
            logger.info(f"selected_class: {current_selected}")
            class_relevant_slots = wizard_instance.get_slot_names(
                element=current_selected, selected_schema="project"
            )
            class_relevant_slots.sort()
            all_relevant_slots.extend(class_relevant_slots)

        with open(populated_tsv, "r") as f:
            csv_reader = csv.DictReader(f, delimiter="\t")
            unfiltered = list(csv_reader)

        header_rows = unfiltered[0:2]
        filtered_rows = []

        class_indicator = original_to_card_and_range["class"]
        slot_indicator = original_to_card_and_range["slot"]
        # lost_track = {}
        for u_row in unfiltered:
            raw_to_normalized = {
                re.sub(r"^>\s+", "", k): v for k, v in u_row.items()
            }
            if raw_to_normalized[class_indicator] in selected_classes:
                filtered_rows.append(u_row)
            if (
                    raw_to_normalized[slot_indicator] in all_relevant_slots
                    and not raw_to_normalized[class_indicator]
            ):
                filtered_rows.append(u_row)

        filtered_rows = sorted(
            filtered_rows,
            key=lambda x: (x[slot_indicator], x[class_indicator]),
            reverse=False,
        )
        writable_rows = header_rows + filtered_rows

        with open(filtered_populated, "wt") as out_file:
            tsv_writer = csv.DictWriter(out_file, delimiter="\t", fieldnames=row0)
            tsv_writer.writeheader()
            tsv_writer.writerows(writable_rows)

    rel_headers = ["slot", "classes"]
    if filtered_slot_class_rels:
        filtered_slots_to_classes = wizard_instance.get_slots_to_classes(
            selected_classes=selected_classes
        )
        with open(filtered_slot_class_rels, "wt") as out_file:
            tsv_writer = csv.DictWriter(
                out_file, delimiter="\t", fieldnames=rel_headers
            )
            tsv_writer.writeheader()
            tsv_writer.writerows(filtered_slots_to_classes)

    if all_slot_class_rels:
        all_slots_to_classes = wizard_instance.get_slots_to_classes()
        with open(all_slot_class_rels, "wt") as out_file:
            tsv_writer = csv.DictWriter(
                out_file, delimiter="\t", fieldnames=rel_headers
            )
            tsv_writer.writeheader()
            tsv_writer.writerows(all_slots_to_classes)

    if (
            filtered_slot_class_rels
            and merged_filtered_rels
    ):
        merged_list, combined_headers = wizard_instance.prepare_merged_report(
            populated_template=writable_rows,
            lhs_header=row0,
            slot_classes_rels=filtered_slots_to_classes,
        )
        merged_list[0]["relevant_classes"] = "ignore"
        with open(merged_filtered_rels, "wt") as out_file:
            tsv_writer = csv.DictWriter(
                out_file, delimiter="\t", fieldnames=combined_headers
            )
            tsv_writer.writeheader()
            tsv_writer.writerows(merged_list)


cli.add_command(classes_slots)
cli.add_command(enums)
cli.add_command(named_element)

if __name__ == "__main__":
    cli()
