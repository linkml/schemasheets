RUN = poetry run
PROJ = schemasheets

all: all_py test

test:
	$(RUN) pytest

all_py: schemasheets/conf/configschema.py
$(PROJ)/conf/configschema.py: $(PROJ)/conf/configschema.yaml
	$(RUN) gen-python $< > $@.tmp && mv $@.tmp $@

cogs-%:
	$(RUN) cogs $*

sync-examples:
	cp tests/input/{personinfo,enums,prefixes,schema,subsets,types}.tsv examples/input && \
	cp -pr tests/output/personinfo/* examples/output

datamodel-docs: schemasheets/conf/configschema.yaml
	gen-markdown $< -d docs/datamodel/

tests/input/rda-crosswalk.tsv:
	curl -L -s 'https://docs.google.com/spreadsheets/d/1mu9iWZxX4DvtklLIQgEloM8oZfzZdzfJ/export?format=tsv&gid=1108662376' > $@


serve:
	$(RUN) mkdocs serve

gh-deploy:
	$(RUN) mkdocs gh-deploy

examples/output/single_examples.yaml: examples/input/schema.tsv examples/input/prefixes.tsv examples/input/single_examples.tsv
	$(RUN) sheets2linkml --output $@ $^
	$(RUN) python schemasheets/schemaview_vs_examples.py


examples/output/multiple_examples_per_slot.yaml: examples/input/schema.tsv examples/input/prefixes.tsv examples/input/multiple_examples_per_slot.tsv
	$(RUN) sheets2linkml --output $@ $^

.PHONY: clean all test gh-deploy serve datamodel-docs sync-examples cogs-% all_py

clean:
	rm -rf examples/output/*examples*yaml
	rm -rf examples/output/*ttl
