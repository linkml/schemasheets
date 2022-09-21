# Working with Excel spreadsheets

Currently there no direct support for working with Excel formats.
You must export to TSV format prior to running `sheets2linkml'

We are hoping to provide more extensive support for Excel starting in 2023.

## Tips

- schemasheets will not catch errors introduced by Excel, including
   - gene names turned into dates
- be sure to save as TSV, tabs are the default delimiter in schemasheets
- avoid using non UTF-8 characters
- avoid using color, font, etc
- We recommend maintain as .tsv (not .xlsx) tracked in GitHub
