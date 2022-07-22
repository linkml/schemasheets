.PHONY: clean all gen_and_pop

all: clean target/output/schema.yaml

clean:
	rm -rf target/output/*tsv
	rm -rf target/output/*csv
	rm -rf target/output/*.yaml
	rm -rf target/templates/generated*
	rm -rf target/output/generated*

target/output/slot.tsv:
	poetry run linkml2sheets target/templates/*.tsv \
  		--schema /Users/MAM/Documents/gitrepos/linkml-model/linkml_model/model/schema/meta.yaml  \
  		--output-directory target/output \
  		--overwrite
 target/output/schema.yaml: target/output/slot.tsv
	poetry run sheets2linkml target/output/*.tsv > $@

target/output/key_counts.csv:
	poetry run python schemasheets/list_element_slots.py

gen_and_pop: clean
	poetry run template_wizard \
		--project_source "https://raw.githubusercontent.com/microbiomedata/nmdc-schema/main/src/schema/nmdc.yaml" \
		--template_style classes_slots \
		--template_dir target/templates \
  		--populated_dir target/output \
  		--col_sorting by_usage_count \
  		--selected_classes biosample \
  		--selected_classes study \
  		--all_slot_class_rels target/output/NMDC_schema_slot_class_rels.yaml \
        --filtered_slot_class_rels target/output/NMDC_schema_slot_class_filtered_rels.yaml \
        --merged_filtered_rels target/output/NMDC_schema_slot_class_merged_with_filtered_rels.tsv


roundtrip: gen_and_pop
	poetry run sheets2linkml \
		--name partial_roundtrip \
		target/output/generated_filtered_NMDC_classes_slots.tsv > target/output/generated_filtered_NMDC_classes_slots.yaml

just_pop:
	poetry run linkml2sheets \
		target/templates/generated_NMDC_classes_slots.tsv \
  		--schema /Users/MAM/Documents/gitrepos/nmdc-schema/src/schema/nmdc.yaml  \
  		--output-directory target/output \
  		--overwrite