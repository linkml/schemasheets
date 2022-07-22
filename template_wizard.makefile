.PHONY: template_wizard_clean template_wizard_all 

template_wizard_all: template_wizard_clean target/output/schema.yaml

template_wizard_clean:
	rm -rf target/output/*tsv
	rm -rf target/output/*csv
	rm -rf target/output/*.yaml
	rm -rf target/templates/generated*
	rm -rf target/output/generated*
	mkdir -p target/input
	mkdir -p target/templates
	mkdir -p target/output


#target/output/slot.tsv:
#	poetry run linkml2sheets target/templates/*.tsv \
#  		--schema /Users/MAM/Documents/gitrepos/linkml-model/linkml_model/model/schema/meta.yaml  \
#  		--output-directory target/output \
#  		--overwrite
  		
# target/output/schema.yaml: target/output/slot.tsv
#	poetry run sheets2linkml target/output/*.tsv > $@

target/output/key_counts.csv:
	poetry run python schemasheets/list_element_slots.py

target/output/NMDC_schema_slot_class_merged_with_filtered_rels.tsv: template_wizard_clean
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


target/output/NMDC_schema_slot_class_merged_with_filtered_rels.yaml: target/output/NMDC_schema_slot_class_merged_with_filtered_rels.tsv
	poetry run sheets2linkml \
		--name NMDC_slot_class_roundtrip \
		$< > $@

#just_pop:
#	poetry run linkml2sheets \
#		target/templates/generated_NMDC_classes_slots.tsv \
#  		--schema /Users/MAM/Documents/gitrepos/nmdc-schema/src/schema/nmdc.yaml  \
#  		--output-directory target/output \
#  		--overwrite