RUN=poetry run

scripts-all: scripts-clean populated_with_generated_spec.tsv

scripts-clean:
	rm -rf populated_with_generated_spec.tsv
	#rm -rf meta_merged.yaml

#		--meta-staging-path $(word 1,$^) \
#		--source-path $(word 2,$^)
populated_with_generated_spec.tsv:
	$(RUN) generate-populate \
		--meta-path "https://w3id.org/linkml/meta" \
		--meta-staging-path meta_merged.yaml \
		--source-path "/Users/MAM/Documents/gitrepos/nmdc-schema/nmdc_schema/nmdc_materialized_patterns.yaml" \
		--output-path $@

populated_from_static_template_safe.tsv: meta_merged.yaml
	$(RUN) linkml2sheets \
		--output $@ \
		--schema  $< \
		--overwrite \
		--verbose populated_with_generated_spec_subset.tsv

# populated_with_generated_spec_template_safe.tsv

# examples/input/multiple_examples_per_slot.tsv
