.PHONY: clean all work w2

all: clean work/output/schema.yaml

clean:
	rm -rf work/output/*tsv
	rm -rf work/output/*.yaml

work/output/slot.tsv:
	poetry run linkml2sheets work/templates/*.tsv \
  		--schema /Users/MAM/Documents/gitrepos/linkml-model/linkml_model/model/schema/meta.yaml  \
  		--output-directory work/output \
  		--overwrite
 work/output/schema.yaml: work/output/slot.tsv
	poetry run sheets2linkml work/output/*.tsv > $@
