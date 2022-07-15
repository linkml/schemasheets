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
		--template_dir work/templates \
  		--populated_dir work/output \
  		--col_sorting by_usage_count \
  		--selected_classes biosample \
  		--selected_classes study

#work/output/experimental_nmdc_class_slot_templ.tsv:
#	# /Users/MAM/Documents/gitrepos/linkml-model/linkml_model/model/schema/meta.yaml
#	# /Users/MAM/Documents/gitrepos/nmdc-schema/src/schema/nmdc.yaml
#	poetry run linkml2sheets work/templates/experimental_nmdc_class_slot_templ.tsv \
#  		--schema /Users/MAM/Documents/gitrepos/nmdc-schema/src/schema/nmdc.yaml  \
#  		--output-directory work/output \
#  		--overwrite