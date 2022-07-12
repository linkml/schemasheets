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

.PHONY: clean all test gh-deploy serve datamodel-docs sync-examples cogs-% all_py range_override_reasoning temp

clean:
	rm -rf examples/output/*examples*yaml*

bin/robot.jar:
	curl -s https://api.github.com/repos/ontodev/robot/releases/latest  | grep 'browser_download_url.*\.jar"' |  cut -d : -f 2,3 | tr -d \" | wget -O $@ -i -

examples/output/range_override_examples.yaml: examples/input/schema.tsv examples/input/prefixes.tsv examples/input/range_override.tsv
	$(RUN) sheets2linkml --output $@ $^


examples/output/range_override_examples.ttl: examples/output/range_override_examples.yaml
	$(RUN) gen-owl --output $@ --no-type-objects --no-metaclasses $<
	# ERROR:root:Multiple slots with URI: https://w3id.org/linkml/examples/personinfo/slot_for_range_override:
	# ['slot_for_range_override', 'class_for_range_override_slot_for_range_override']; consider giving each a unique slot_uri

examples/output/range_override_examples_reasoned.ttl: examples/output/range_override_examples.ttl bin/robot.jar
	# error doesn't appear in the generated examples/output/range_override_examples.ttl
	- grep -i error $<
	java -jar bin/robot.jar reason --reasoner ELK --input $< --output $@
	@echo But Makefile keeps going!?
	- grep -i error $@

configured_owl_via_project: examples/output/range_override_examples.yaml
	$(RUN) gen-project \
		--include owl \
		--generator-arguments 'owl: {type-objects: false}' \
		--dir examples/output $<

# ---

slot_definition_reports/slot_definition_range_tally.tsv:
	$(RUN) python schemasheets/get_metaclass_slotvals.py \
		--selected_element slot_definition \
		--directory slot_definition_reports

nmdc_verbatims/annotations.tsv:
	$(RUN) python schemasheets/verbatim_sheets.py \
		--schema_source 'https://raw.githubusercontent.com/microbiomedata/nmdc-schema/main/src/schema/nmdc.yaml' \
		--directory nmdc_verbatims

nmdc_roundtrip/nmdc_roundtrip.yaml: nmdc_verbatims/annotations.tsv
	# add
	# internal_separator: "|"
	# for emit_prefixes
	# ---
	# sheets2linkml casts integers to strings?!
	mkdir -p nmdc_roundtrip
	$(RUN) sheets2linkml \
		--output $@ nmdc_verbatims/*

nmdc_roundtrip/nmdc_roundtrip_generated.yaml: nmdc_roundtrip/nmdc_roundtrip.yaml
	- $(RUN) gen-linkml \
		--output $@ \
		--format yaml $<


temp:
	mkdir -p temp
	poetry run linkml2sheets -s tests/output/personinfo.yaml tests/input/personinfo.tsv -d temp