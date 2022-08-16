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

# template_wizard_clean

target/output/NMDC_schema_slot_class_merged_with_filtered_rels.tsv:
	poetry run template_wizard classes-slots \
		--project_source "https://raw.githubusercontent.com/microbiomedata/nmdc-schema/main/src/schema/nmdc.yaml" \
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

## not used for enums template yet:
##  col_sorting (always alphabetical), selected_classes, populated_dir, all_slot_class_rels, filtered_slot_class_rels, merged_filtered_rels
## todo make subcommands
#target/templates/generated_NMDC_enums.tsv: template_wizard_clean
#	poetry run template_wizard \
#		--project_source "https://raw.githubusercontent.com/microbiomedata/nmdc-schema/main/src/schema/nmdc.yaml" \
#		--template_style enums \
#		--template_dir target/templates \
#  		--populated_dir target/output \


#target/output/generated_NMDC_enums.tsv: target/templates/generated_NMDC_enums.tsv
#	poetry run linkml2sheets \
#		$< \
#  		--schema /Users/MAM/Documents/gitrepos/nmdc-schema/src/schema/nmdc.yaml  \
#  		--output-directory target/output \
#  		--overwrite

## target/output/generated_NMDC_enums.tsv
#target/output/generated_NMDC_enums.yaml:
#	poetry run sheets2linkml \
#		--name NMDC_enums_roundtrip \
#		target/templates/generated_NMDC_enums.tsv > $@

#target/output/include_schema_slot_class.tsv: template_wizard_clean
#	poetry run template_wizard \
#		--project_source "https://raw.githubusercontent.com/include-dcc/include-linkml/main/src/linkml/include_linkml.yaml" \
#		--template_style classes_slots \
#		--template_dir target/templates \
#  		--populated_dir target/output \
#  		--col_sorting alphabetical

#target/templates/generated_IncludePortalV1_enums.tsv: template_wizard_clean
#	poetry run template_wizard \
#		--project_source "https://raw.githubusercontent.com/include-dcc/include-linkml/main/src/linkml/include_linkml.yaml" \
#		--template_style enums \
#		--template_dir target/templates \
#  		--populated_dir target/output

#target/output/include_schema_enums.tsv: target/templates/generated_IncludePortalV1_enums.tsv
#	poetry run linkml2sheets \
#		$< \
#  		--schema /Users/MAM/Documents/gitrepos/include-linkml/src/linkml/include_linkml.yaml \
#  		--output-directory target/output \
#  		--overwrite

target/templates/generated_NMDC_enums.tsv:
	poetry run template_wizard enums \
		--project-source "https://raw.githubusercontent.com/microbiomedata/nmdc-schema/main/src/schema/nmdc.yaml" \
		--template-dir target/templates

target/output/generated_NMDC_classes.tsv:
	poetry run template_wizard named-element \
		--element classes \
		--project-source "https://raw.githubusercontent.com/microbiomedata/nmdc-schema/main/src/schema/nmdc.yaml" \
		--template-dir target/templates \
		--populated_dir target/output

target/output/generated_NMDC_slots.tsv:
	poetry run template_wizard named-element \
		--element slots \
		--project-source "https://raw.githubusercontent.com/microbiomedata/nmdc-schema/main/src/schema/nmdc.yaml" \
		--template-dir target/templates \
		--populated_dir target/output