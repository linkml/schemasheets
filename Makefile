RUN = poetry run
PROJ = fairstructure

all: all_py test

test:
	$(RUN) pytest

all_py: fairstructure/conf/configschema.py
$(PROJ)/conf/configschema.py: $(PROJ)/conf/configschema.yaml
	$(RUN) gen-python $< > $@.tmp && mv $@.tmp $@

cogs-%:
	$(RUN) cogs $*
