RUN=poetry run

scripts-all: scripts-clean populated_from_generated_spec.tsv

scripts-clean:
	rm -rf populated_from_generated_spec.tsv
	rm -rf populated_generated_debug_report.yaml
	rm -rf populated_with_generated_spec.tsv
	rm -rf populated_with_generated_spec_log.txt

populated_with_generated_spec.tsv: schemasheets/conf/configschema.yaml
	$(RUN) generate-populate \
		--debug-report-path populated_generated_debug_report.yaml \
		--log-file populated_with_generated_spec_log.txt \
		--output-path $@ \
		--report-style concise \
		--source-path $<

# confirm that the output from generate-populate is a valid schemasheet itself
populated_from_generated_spec.tsv: schemasheets/conf/configschema.yaml populated_with_generated_spec.tsv
	$(RUN) linkml2sheets \
		--output $@ \
		--overwrite \
		--schema  $^

