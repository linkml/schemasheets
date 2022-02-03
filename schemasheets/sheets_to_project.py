import logging
import os

import click
import yaml
from typing import List, Union, Any, Dict, Tuple, Generator

from linkml.generators.projectgen import ProjectConfiguration, ProjectGenerator
from linkml_runtime.dumpers import yaml_dumper

from schemasheets.schemamaker import SchemaMaker


@click.command()
@click.option("--dir", "-d",
              help="directory in which to place generated files. E.g. linkml_model, biolink_model")
@click.option("--repair/--no-repair",
              default=True,
              show_default=True,
              help="Automatically repair missing schema elements")
@click.option("-n", "--name",
              default="schema",
              show_default=True,
              help="name of the schema")
@click.option("--generator-arguments", "-A",
              help="yaml configuration for generators")
@click.option("--config-file", "-C",
              type=click.File('rb'),
              help="path to yaml configuration")
@click.option("--exclude", "-X",
              multiple=True,
              help="list of artefacts to be excluded")  # TODO: make this an enum
@click.option("--include", "-I",
              multiple=True,
              help="list of artefacts to be included. If not set, defaults to all")  # TODO: make this an enum
@click.option("--unique-slots/--no-unique-slots",
              default=False,
              show_default=True,
              help="All slots are treated as unique and top level and do not belong to the specified class")
@click.option("-v", "--verbose", count=True)
@click.argument('tsv_files', nargs=-1)
def multigen(tsv_files, dir, verbose: int, repair: bool, name,
             unique_slots: bool,
             exclude: List[str], include: List[str], config_file, generator_arguments: str, **kwargs):
    """
    Generate an entire set of schema files from Schemasheets

    Generate all downstream artefacts using default configuration:

       sheets2linkml --output my_schema.yaml my_schema/*tsv


    """
    if verbose >= 2:
        logging.basicConfig(level=logging.DEBUG)
    elif verbose == 1:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)
    project_config = ProjectConfiguration()
    if config_file is not None:
        for k, v in yaml.safe_load(config_file).items():
            setattr(project_config, k, v)
    if exclude:
        project_config.excludes = list(exclude)
    if include:
        project_config.includes = list(include)
    if generator_arguments is not None:
        try:
            project_config.generator_args = yaml.safe_load(generator_arguments)
        except Exception:
            raise Exception(f'Argument must be a valid YAML blob')
        logging.info(f'generator args: {project_config.generator_args}')
    if dir is None:
        dir = '.'
    project_config.directory = dir
    sm = SchemaMaker()
    if name:
        sm.default_name = name
    sm.unique_slots = unique_slots
    schema = sm.create_schema(list(tsv_files))
    if repair:
        schema = sm.repair_schema(schema)
    out_file = os.path.join(dir, f'{name}.yaml')
    yaml_dumper.dump(schema, to_file=out_file)
    gen = ProjectGenerator()
    gen.generate(out_file, project_config)


if __name__ == '__main__':
    multigen()
