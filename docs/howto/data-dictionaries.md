TODO: this is not yet complete, do not link from index until complete

# Simple data dictionaries

A data dictionary is a file (or collection of files) which unambiguously declares, defines and annotates all the variables collected in a project and associated to a dataset (_definition: [FAIR cookbook](https://faircookbook.elixir-europe.org/content/recipes/interoperability/creating-data-dictionary.html)).

Schemasheets is an idea framework for managing a data dictionary.

## Example Data Dictionary

The [FAIR Cookbook](https://faircookbook.elixir-europe.org) provides an example of a data dictionary for tracking various aspects of
a research subject or model organism, including:

 - subject_id
 - species
 - strain (for model organisms)
 - age + age unit
 - etc

See [Example](https://faircookbook.elixir-europe.org/content/recipes/interoperability/creating-data-dictionary.html#an-example-of-data-dictionary).

Let's start by copying this directly into a google sheet.

You can see this on the v1 tab of [this sheet](https://docs.google.com/spreadsheets/d/1bUMX6P8JkgbHwZHR7RU5XbBsbhrKwaBftk7XuDz6xJc/edit#gid=0)

File Name | Variable Name | Variable Label | Variable Ontology ID or RDFtype | Variable ID Source | Variable Statistical Type | Variable Data Type | Variable Size | Max Allowed Value | Min Allowed Value | Regex | Allowed Value Shorthands | Allowed Value Descriptions | Computed Value | Unique (alone) | Unique (Combined with) | Required | Collection Form Name | Comments
-- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | --
1_Subjects.txt | SUBJECT_ID | Subject number | https://schema.org/identifier | https://schema.org | categorical variable | integer |   |   |   |   |   |   |   | Y |   | Y | FORM 1 |
1_Subjects.txt | SPECIES | Species name | https://schema.org/name | https://schema.org | categorical variable | string |   |   |   |   |   |   |   |   |   |   | FORM 1 |
1_Subjects.txt | STRAIN | Strain | TODO substitute broken link https://bioschemas.org/profiles/Taxon/0.6-RELEASE/identifier | https://schemas.org/ | categorical variable | string |   |   |   |   |   | http://purl.obolibrary.org/obo/NCBITaxon_40674 |   |   |   |   | FORM 1 |
1_Subjects.txt | AGE | Age at study initiation | https://bioschemas.org/types/BioSample/0.1-RELEASE-2019_06_19 | https://bioschemas.org/ | continuous variable | integer |   |   |   |   |   |   |   |   |   | Y | FORM 1 |
1_Subjects.txt | AGE_UNIT | Age unit | http://purl.obolibrary.org/obo/UO_0000003 | http://purl.obolibrary.org/obo/uo | categorial variable | string |   |   |   |   |   |   |   |   |   | Y | FORM 1 |
1_Subjects.txt | SEX | Sex | https://schema.org/gender | https://schema.org | categorical variable | enum |   |   |   |   | M;F | M=male;F=female |   |   |   |   | FORM 1 |

## Adding a descriptor row

Our first task is to add a descriptor row that describes how each column heading maps to a LinkML metamodel element.

Here we will tackle this incrementally, starting with the first 3 columns, we will map to:

- [class][https://w3id.org/linkml/ClassDefinition]
- [slot][https://w3id.org/linkml/SlotDefinition]
- [title][https://w3id.org/linkml/title]

The table now looks like this:

|File Name|Variable Name|Variable Label|
|---|---|---|
|`>` class|slot|title|
|1_Subjects.txt|SUBJECT_ID|Subject number|
|1_Subjects.txt|SPECIES|Species name|
|1_Subjects.txt|STRAIN|Strain|
|1_Subjects.txt|AGE|Age at study initiation|
|1_Subjects.txt|AGE_UNIT|Age unit|
|1_Subjects.txt|SEX|Sex|
|1_Subjects.txt|SOMEDATE|Date of acquiring subject|
|1_Subjects.txt|HEMOGLOBIN|Hematology: Hemoglobin|
|1_Subjects.txt|HEMOGLOBIN_UNIT|Hemoglobin unit|
|1_Subjects.txt|HEIGHT|Body size|
|1_Subjects.txt|HEIGHT_UNIT|Body size unit|
|1_Subjects.txt|WEIGHT|Body weight|
|1_Subjects.txt|WEIGHT_UNIT|Body weight unit|
|1_Subjects.txt|BMI|Body mass index|
|1_Subjects.txt|LAB|Laboratory|
|2_Samples.txt|SAMPLE_ID|Sample ID|
|2_Samples.txt|SAMPLE_SITE|Sample collection site|
|2_Samples.txt|ANALYTE_TYPE|Type of analysis|
|2_Samples.txt|GENOTYPING_CENTER|GENOTYPING_CENTER|
|2_Samples.txt|SEQUENCING_CENTER|SEQUENCING_CENTER|
|3_SampleMapping.txt|SUBJECT_ID|Subject number|
|3_SampleMapping.txt|SAMPLE_ID|Sample ID|

Our choice of how to map the first column is a bit odd, and reflects a slight mismatch between
schemasheets/LinkML, which aims to describe a data model that can be used for *multiple instantiations of the same format* and a data dictionary that is oriented around describing *a single distribution*.

Here we are implicitly creating classes/records like "1_Subjects.txt" which doesn't really conform to standard
class naming conventions in LinkML. Later we will explore rewriting these with names like "Subject", "Sample", and "SampleMapping"

TODO

For the second column, the choice of ALL-CAPS for slot name also goes against standard naming conventions, but
this doesn't really matter so much, and the title (col 3) is the string that should be used in user-facing applications
like Data Harmonizer.



## Modifications

- We modified the minimum and maximum values which were specified using commas instead of periods for decimal notation
- The "regex" field had a value YYYY-MM-DD, but this isn't an actual regex

This framework allows you to represent complex relation-style schemas
using spreadsheets/TSVs. But it also allows for representation of simple "data dictionaries" or "minimal information lists".
These can be thought of as "wide tables", e.g. representing individual observations or observable units such as persons or samples.

TODO



