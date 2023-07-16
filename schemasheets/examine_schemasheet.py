from schemasheets.schemasheet_datamodel import SchemaSheet

specification = "../populated_with_generated_spec_subset.tsv"

ssheet = SchemaSheet.from_csv(specification, delimiter="\t")

print(ssheet)