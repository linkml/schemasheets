RUN=poetry run

scripts-all: scripts-clean populated-from-generated-spec.tsv config-less-report.tsv

scripts-clean:
	rm -rf config-less-report.tsv
	rm -rf populated-from-generated-spec.tsv
	rm -rf populated-generated-debug-report.yaml
	rm -rf populated-with-generated-spec-log.txt
	rm -rf populated-with-generated-spec.tsv

populated-with-generated-spec.tsv: schemasheets/conf/configschema.yaml
	$(RUN) linkml2schemasheets-template \
		--debug-report-path populated-generated-debug-report.yaml \
		--log-file populated-with-generated-spec-log.txt \
		--output-path $@ \
		--report-style concise \
		--source-path $<

# confirm that the output from generate-populate is a valid schemasheet itself
populated-from-generated-spec.tsv: schemasheets/conf/configschema.yaml populated-with-generated-spec.tsv
	$(RUN) linkml2sheets \
		--output $@ \
		--overwrite \
		--schema  $^

config-less-report.tsv: populated-with-generated-spec.tsv # is this safe at all? on what platforms?
	grep -v -e '^>' $< > $@