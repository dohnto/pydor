#!/usr/bin/env python

from __future__ import print_function
import click
import itertools
import requests.exceptions
import logging
import json

import pydor
import tablib
import tablib.formats
import pydor.tools.tablib_text_module

# add custom text output module of tablib
tablib.formats.available += (pydor.tools.tablib_text_module,)

# get all format titles
OUTPUT_FORMATS = map(lambda m: m.title, tablib.formats.available)

@click.group()
def cli():
    pass

def _list(generator, limit, output, insecure):
    try:
        if limit == 0:
            # list all
            items = [[n] for n in generator]
        else:
            items = [[n] for n in itertools.islice(generator, limit)]

        dataset = tablib.Dataset(headers=["name"])
        map(dataset.append, items)
        click.echo(getattr(dataset, output))
    except requests.exceptions.SSLError as e:
        logging.fatal(e.message)
        click.echo("Consider using --insecure")


@click.command()
@click.argument('REGISTRY')
@click.option('--limit', default=20, help='number of namespaces to show')
@click.option('--output', default=pydor.tools.tablib_text_module.title, type=click.Choice(OUTPUT_FORMATS), show_default=True)
@click.option('--insecure', default=False, is_flag=True)
def list(registry, limit, output, insecure):
    generator = pydor.API(registry, insecure=insecure).Catalog()
    _list(generator, limit, output, insecure)


@click.command()
@click.argument('IMAGE')
@click.option('--limit', default=20, help='number of tags to show')
@click.option('--output', default=pydor.tools.tablib_text_module.title, type=click.Choice(OUTPUT_FORMATS))
@click.option('--insecure', default=False, is_flag=True)
def tags(image, limit, output, insecure):
    ri = pydor.Image.from_image(image)

    generator = pydor.API(ri.registry, insecure=insecure).Tags(ri.repository)
    _list(generator, limit, output, insecure)


@click.command()
@click.argument('TYPE', type=click.Choice(pydor.MANIFEST_PROPERTIES))
@click.argument('IMAGE')
@click.option('--output', default=pydor.tools.tablib_text_module.title, type=click.Choice(OUTPUT_FORMATS))
@click.option('--insecure', default=False, is_flag=True)
def inspect(type, image, output, insecure):
    ri = pydor.Image.from_image(image)

    manifest = pydor.Manifest(pydor.API(ri.registry, insecure=insecure).Manifest(ri.repository, ri.reference).get())

    inspected_object = getattr(manifest, type)

    dataset = tablib.Dataset(headers=inspected_object.headers)
    map(dataset.append, inspected_object.data)
    click.echo(getattr(dataset, output))


@click.command()
@click.argument('IMAGE')
@click.option('--insecure', default=False, is_flag=True)
def manifest(image, insecure):
    ri = pydor.Image.from_image(image)

    manifest = pydor.Manifest(pydor.API(ri.registry, insecure=insecure).Manifest(ri.repository, ri.reference).get())
    click.echo(json.dumps(manifest.json, indent=4))

cli.add_command(list)
cli.add_command(tags)
cli.add_command(inspect)
cli.add_command(manifest)


if __name__ == '__main__':
    cli()