.PHONY: clean all gen_and_pop

all: clean work/output/schema.yaml

clean:
	rm -rf work/output/*tsv
	rm -rf work/output/*csv
	rm -rf work/output/*.yaml
	rm -rf work/templates/generated*
	rm -rf work/output/generated*

work/output/slot.tsv:
	poetry run linkml2sheets work/templates/*.tsv \
  		--schema /Users/MAM/Documents/gitrepos/linkml-model/linkml_model/model/schema/meta.yaml  \
  		--output-directory work/output \
  		--overwrite
 work/output/schema.yaml: work/output/slot.tsv
	poetry run sheets2linkml work/output/*.tsv > $@

work/output/key_counts.csv:
	poetry run python schemasheets/list_element_slots.py

gen_and_pop: clean
	poetry run template_wizard \
		--project_source "https://raw.githubusercontent.com/microbiomedata/nmdc-schema/main/src/schema/nmdc.yaml" \
		--template_style classes_slots \
		--template_dir work/templates \
  		--populated_dir work/output \
  		--col_sorting by_usage_count \
  		--selected_classes biosample \
  		--selected_classes study \
  		--all_slot_class_rels work/output/NMDC_schema_slot_class_rels.yaml \
        --filtered_slot_class_rels work/output/NMDC_schema_slot_class_filtered_rels.yaml \
        --merged_filtered_rels work/output/NMDC_schema_slot_class_merged_with_filtered_rels.tsv


roundtrip: gen_and_pop
	poetry run sheets2linkml \
		--name partial_roundtrip \
		work/output/generated_filtered_NMDC_classes_slots.tsv > work/output/generated_filtered_NMDC_classes_slots.yaml

just_pop:
	poetry run linkml2sheets \
		work/templates/generated_NMDC_classes_slots.tsv \
  		--schema /Users/MAM/Documents/gitrepos/nmdc-schema/src/schema/nmdc.yaml  \
  		--output-directory work/output \
  		--overwrite