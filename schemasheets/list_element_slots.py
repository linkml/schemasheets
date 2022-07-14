import csv
import pprint
from typing import Dict, List

import yaml
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper

meta_source = "https://raw.githubusercontent.com/linkml/linkml-model/main/linkml_model/model/schema/meta.yaml"

meta_element = "schema_definition"

meta_view = SchemaView(meta_source)

slots = meta_view.class_induced_slots(meta_element)

slot_names = [str(slot.alias) for slot in slots]

slot_names.sort()

as_if_tsv = "\t".join(slot_names)

print(as_if_tsv)

# ---

template_hints = [{"name": i.name, "range": i.range, "multivalued": i.multivalued} for i in slots]
pprint.pprint(template_hints)

with open('../template_hints.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['name', 'range', 'multivalued'])
    writer.writeheader()
    writer.writerows(template_hints)

# ---

meta_schema = meta_view.schema

meta_yaml = yaml_dumper.dumps(meta_schema)

meta_dict = yaml.safe_load(meta_yaml)


def dictionary_check(dict_in: Dict, inner_list: List = []) -> None:
    """
    First prints the final entry in the dictionary (most nested) and its key
    Then prints the keys leading into this
    * could be reversed to be more useful, I guess
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


outer_list = dictionary_check(meta_dict)

key_counts = list_to_count_dict(outer_list)

common_keys_lod = [{"key": k, "count": v} for k, v in key_counts.items()]

with open('../key_counts.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['key', 'count'])
    writer.writeheader()
    writer.writerows(common_keys_lod)
