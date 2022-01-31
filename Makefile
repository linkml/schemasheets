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

serve:
	$(RUN) mkdocs serve

gh-deploy:
	$(RUN) mkdocs gh-deploy
