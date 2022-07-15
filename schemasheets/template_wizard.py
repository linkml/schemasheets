import csv
import logging
import os
import pprint
from typing import List, Dict

import click
import click_log
import yaml
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper

from schemasheets.schema_exporter import SchemaExporter

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

# todo: reflect the classes that use a slot on slot-only rows

# todo: work on YAML-serialized columns like annotation and alt_descriptions
# todo: style guide, esp use of external terms and consistent grammar

# todo add customized first header BEFORE the unfiltered sheet is written

# todo: group and or describe mappings
# todo: comments, notes, todos distinctions

# todo: generate third row for internal separators and annotation names

class L2sTemplate:
    def __init__(self, meta_view: SchemaView, project_view: SchemaView):
        self.slot_attributes = None
        self.common_keys_lod = None  # todo work on types
        self.class_slots_slotnames = None  # todo work on types
        self.meta_view = meta_view
        self.project_view = project_view

    def get_slot_names(self, element: str, selected_schema: str) -> List[str]:
        slots = []
        if selected_schema == "meta":
            slots = self.meta_view.class_induced_slots(element)
        elif selected_schema == "project":
            slots = self.project_view.class_induced_slots(element)
        # todo was using alias... name doesn't seem to help with undefined slots
        slot_names = [str(slot.alias) for slot in slots]
        return slot_names

    def get_slot_attributes(self, slot_list: List[str]):
        desired_attributes = ["multivalued", "name", "range", "recommended", "required"]
        slot_attributes = {}
        for cs_name, cs_obj in self.meta_view.all_slots().items():
            if cs_name in slot_list:
                for current_desired in desired_attributes:
                    if cs_name not in slot_attributes:
                        slot_attributes[cs_name] = {}
                    slot_attributes[cs_name][current_desired] = getattr(cs_obj, current_desired)
        return slot_attributes

    def build_class_slot_templ(self):
        class_names = self.get_slot_names(element="class_definition", selected_schema="meta")
        slot_names = self.get_slot_names(element="slot_definition", selected_schema="meta")
        class_slots_slotnames = list(set(class_names).union(set(slot_names)))
        class_slots_slotnames.sort()
        current_slot_attributes = self.get_slot_attributes(class_slots_slotnames)
        self.class_slots_slotnames = class_slots_slotnames
        self.slot_attributes = current_slot_attributes

    def count_proj_elem_usage(self):
        project_yaml = yaml_dumper.dumps(self.project_view.schema)
        project_dict = yaml.safe_load(project_yaml)

        outer_list = dictionary_check(project_dict)  # todo rename this

        key_counts = list_to_count_dict(outer_list)

        common_keys_lod = [{"key": k, "count": v} for k, v in key_counts.items()]  # todo rename this

        self.common_keys_lod = common_keys_lod

    def get_frequent_elements(self, count_threshold: int):
        meets_threshold = [i["key"] for i in self.common_keys_lod if i["count"] >= count_threshold]
        return meets_threshold

    def whittle_columns(self):
        pass


def dictionary_check(dict_in: Dict, inner_list: List = []) -> List:
    """
    recursively collects all keys from a dictionary
    """
    for key, value in dict_in.items():
        if isinstance(value, dict):
            dictionary_check(value, inner_list)
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
        if item in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1
    return count_dict


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option('--meta_source',
              default="https://raw.githubusercontent.com/linkml/linkml-model/main/linkml_model/model/schema/meta.yaml",
              help='HTTP or filesystem path to some version of the LinkML meta model'
              )
@click.option('--project_source',
              help='HTTP or filesystem path to your project schema',
              required=True,
              )
@click.option('--template_style',
              default="classes_slots",
              help="Don't make a column for elements that appear less than N times in your project schema.",
              required=True,
              type=click.Choice(['classes_slots']),
              )
@click.option('--min_occurrences',
              default=2,
              help="Don't make a column for elements that appear less than N times in your project schema."
              )
# type=click.Choice(['local', 'ftp'])
# multiple=True
@click.option('--initial_cols',
              type=click.Choice(['class', 'slot']),
              multiple=True,
              default=[
                  "class",
                  "slot",
              ],
              help="Slots that should appear as the left-most columns."
              )
@click.option('--skip_cols',
              type=click.Choice(['slots', 'slot_usage', 'name']),
              multiple=True,
              default=[
                  "slots",
                  "slot_usage",
                  "name",
              ],  # todo annotations?
              help="Slots that should not appear as columns."
              )
@click.option('--col_sorting',
              type=click.Choice(['alphabetical', 'by_usage_count']),
              multiple=False,
              default="alphabetical",
              help="""Besides initial columns,
              should the rest appear alphabetically or in order of use in project schema?"""
              )
@click.option('--template_dir',
              type=click.Path(exists=True, file_okay=False, dir_okay=True),
              required=True,
              help="""Where should the empty template be written? FILENAME WILL BE AUTOGENERATED!""",
              )
@click.option('--populated_dir',
              type=click.Path(exists=True, file_okay=False, dir_okay=True),
              required=True,
              help="""Where should the populated template be written? FILENAME WILL BE AUTOGENERATED!""",
              )
@click.option('--selected_classes',  # todo check if the class is present in the project schema
              multiple=True,
              help="Only show knowledge about these classes and their asserted slots. Defaults to all."
              )
#         always_cols = []  # todo
def cli(meta_source, project_source, template_style, min_occurrences, initial_cols, skip_cols, col_sorting,
        template_dir, populated_dir, selected_classes) -> None:
    """Create a linkml2sheets template based on meta-expected and project-observed elements."""

    logger.info(f"creating meta view from {meta_source}")
    meta_view = SchemaView(meta_source)
    logger.info(f"found schema {meta_view.schema.name} in {meta_source}")

    logger.info(f"creating project view from {meta_source}")
    project_view = SchemaView(project_source)
    logger.info(f"found schema {project_view.schema.name} in {project_source}")

    generated_template = L2sTemplate(meta_view=meta_view, project_view=project_view)

    if template_style == "classes_slots":
        # todo  overwrite handling
        #  bad path should be handled by click?
        template_path = os.path.join(template_dir,
                                     f"generated_{generated_template.project_view.schema.name}_{template_style}.tsv")
        populated_tsv = os.path.join(populated_dir,
                                     f"generated_{generated_template.project_view.schema.name}_{template_style}.tsv")

        generated_template.build_class_slot_templ()

        generated_template.count_proj_elem_usage()

        frequent_elements = generated_template.get_frequent_elements(count_threshold=min_occurrences)

        frequent_relevant = list(set(frequent_elements).intersection(set(generated_template.class_slots_slotnames)))
        special_cols = list(set(initial_cols).union(set(skip_cols)))
        cols_to_sort = list(set(frequent_relevant).difference(set(special_cols)))
        # todo add sort by frequency
        if col_sorting == "alphabetical":
            cols_to_sort.sort()
        elif col_sorting == "by_usage_count":
            count_sorted = sorted(generated_template.common_keys_lod, key=lambda x: x['count'], reverse=True)
            cols_to_sort = [i['key'] for i in count_sorted if i['key'] in cols_to_sort]
        cols_to_emit = list(initial_cols) + cols_to_sort

        row0 = cols_to_emit.copy()
        row1 = cols_to_emit.copy()
        r1c0 = row1[0]
        r1c0 = "> " + r1c0
        row1[0] = r1c0

        logger.info(f"writing template to {template_path}")
        with open(template_path, 'wt') as out_file:
            tsv_writer = csv.writer(out_file, delimiter='\t')
            tsv_writer.writerow(row0)
            tsv_writer.writerow(row1)

        logger.info(f"populating template to {populated_tsv}")
        exporter = SchemaExporter()
        exporter.export(generated_template.project_view, specification=template_path, to_file=populated_tsv)

        if len(selected_classes) > 0:
            sn = generated_template.project_view.schema.name
            filtered_populated = os.path.join(populated_dir,
                                              f"generated_filtered_{sn}_{template_style}.tsv")
            logger.info(f"writing rows relevant to {selected_classes} to {filtered_populated}")
            all_relevant_slots = []
            for current_selected in selected_classes:
                logger.info(f"selected_class: {current_selected}")
                class_relevant_slots = generated_template.get_slot_names(element=current_selected,
                                                                         selected_schema="project")
                class_relevant_slots.sort()
                all_relevant_slots.extend(class_relevant_slots)

            with open(populated_tsv, "r") as f:
                csv_reader = csv.DictReader(f, delimiter='\t')
                unfiltered = list(csv_reader)
            about_class = [i for i in unfiltered if i['class'] in selected_classes]

            about_class_slots = [i for i in unfiltered if i['slot'] in all_relevant_slots and not i['class']]

            filtered_rows = about_class + about_class_slots

            filtered_rows = sorted(filtered_rows, key=lambda x: (x['slot'], x['class']), reverse=False)

            card_strings = {}
            for current_emitted in cols_to_emit:
                card_string = current_emitted
                with_spaces = current_emitted.replace("_", " ")
                emitted_obj = generated_template.meta_view.get_slot(
                    current_emitted)  # todo better upfront name/alias handling
                if not emitted_obj:
                    emitted_obj = generated_template.meta_view.get_slot(
                        with_spaces)  # todo better upfront name/alias handling
                if emitted_obj:
                    min_card = "0"
                    max_card = "1"
                    if emitted_obj['required']:
                        min_card = "1"
                    if emitted_obj['multivalued']:
                        max_card = "*"
                    card_string = f"{current_emitted}: {min_card}..{max_card}"
                    if emitted_obj['recommended']:
                        card_string += " (recommended)"
                    if emitted_obj['range']:
                        card_string += f" x {emitted_obj['range']}"
                    else:
                        card_string += f" x {generated_template.meta_view.schema.default_range}"
                card_strings[current_emitted] = card_string

                row1_mapping = dict(zip(cols_to_emit, row1))

            with open(filtered_populated, 'wt') as out_file:
                tsv_writer = csv.DictWriter(out_file, delimiter='\t', fieldnames=cols_to_emit)
                # tsv_writer.writeheader()
                tsv_writer.writerow(card_strings)
                tsv_writer.writerow(row1_mapping)
                tsv_writer.writerows(filtered_rows)


if __name__ == '__main__':
    cli()
