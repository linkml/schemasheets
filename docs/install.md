# Installation

## Requirements

Python 3.7 or higher is required.

## Install Schemasheets

Install in the standard way from PyPi:

```bash
pip install schemasheets
```

You can test this works:

```bash
sheets2linkml --help                                                                          
Usage: sheets2linkml [OPTIONS] [TSV_FILES]...

  Convert schemasheets to a LinkML schema

  Example:

     sheets2linkml my_schema/*tsv --output my_schema.yaml

  If your sheets are stored as google sheets, then you can pass in --gsheet-
  id to give the base sheet. In this case arguments should be the names of
  individual tabs

  Example:

      sheets2linkml --gsheet-id 1wVoaiFg47aT9YWNeRfTZ8tYHN8s8PAuDx5i2HUcDpvQ
      personinfo types -o my_schema.yaml

Options:
  -o, --output FILENAME           output file
  -n, --name TEXT                 name of the schema
  --unique-slots / --no-unique-slots
                                  All slots are treated as unique and top
                                  level and do not belong to the specified
                                  class  [default: False]

  --repair / --no-repair          Auto-repair schema  [default: True]
  --gsheet-id TEXT                Google sheets ID. If this is specified then
                                  the arguments MUST be sheet names

  -v, --verbose
  --help                          Show this message and exit.
```

## Docker

If you have Docker installed you can run schemasheets via Docker like this:

```bash
docker run -v $PWD:/work -w /work -ti linkml/schemasheets sheets2linkml --help
```

