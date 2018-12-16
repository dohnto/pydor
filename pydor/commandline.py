#!/usr/bin/env python

from __future__ import print_function
import click
import itertools
import requests.exceptions
import logging
import json
import functools

import pydor
import tablib
import tablib.formats
import pydor.tools.tablib_text_module
import pydor.errors

# add custom text output module of tablib
tablib.formats.available += (pydor.tools.tablib_text_module,)

# get all format titles
OUTPUT_FORMATS = ["json", "xls", "yaml", "csv", "dbf", "tsv", "html", "latex", "xlsx", "ods", "txt"]


def catch_http_errors():
    def decorator(f):
        def g(*args, **kwargs):
            try:
                result = f(*args, **kwargs)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == requests.codes.unauthorized:
                    error_message = ""
                    try:
                        error_message = e.response.json()["errors"][0]["message"]
                    except KeyError:
                        pass
                    click.echo("{} ... Authorization not implemented yet... exiting".format(error_message))
                    click.get_current_context().exit(pydor.errors.NOT_IMPLEMENTED)
                else:
                    raise e
            return result
        return functools.update_wrapper(g, f)
    return decorator


@click.group()
def cli():
    """
    Pydor is a command line utility for remote querying of Docker Registry v2.
    """


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
    except pydor.errors.EntityNotFound as e:
        click.echo(e.message, err=True)
        click.get_current_context().exit(pydor.errors.ENTITY_NOT_FOUND)
    except requests.exceptions.SSLError as e:
        logging.fatal(e.message)
        click.echo("Consider using --insecure")
        click.get_current_context().exit(pydor.errors.SSL_ERROR_CODE)


@click.command()
@click.argument('REGISTRY')
@click.option(
    '--limit', default=20, show_default=True,
    help='Number of repositories to show. Use 0 to show all (but note that this might be very time consuming operation).'
)
@click.option('--output', default=pydor.tools.tablib_text_module.title, type=click.Choice(OUTPUT_FORMATS),
              show_default=True, help="Output format.")
@click.option('--insecure', default=False, is_flag=True, show_default=True,
              help="If set to true, the registry certificates will not be validated.")
@catch_http_errors()
def list(registry, limit, output, insecure):
    """
    List repositories present in docker registry.

    Examples:

    \b
        pydor list quay.io
        pydor list --limit=0 quay.io
        pydor list --output=json quay.io
    """
    generator = pydor.API(registry, insecure=insecure).Catalog()
    _list(generator, limit, output, insecure)


@click.command()
@click.argument('REPOSITORY')
@click.option(
    '--limit', default=20,
    help='Number of tags to show. Use 0 to show all (but note that this might be very time consuming operation).',
    show_default=True)
@click.option('--output', default=pydor.tools.tablib_text_module.title, type=click.Choice(OUTPUT_FORMATS),
              help="Output format.", show_default=True)
@click.option('--insecure', default=False, is_flag=True,
              help="If set to true, the registry certificates will not be validated.", show_default=True)
@catch_http_errors()
def tags(repository, limit, output, insecure):
    """
    List tags of a given repository.

    Examples:

    \b
        pydor tags quay.io/coreos/etcd
        pydor tags --limit=0 quay.io/coreos/etcd
        pydor tags --output=yaml quay.io/coreos/etcd
    """
    ri = pydor.Image.from_image(repository)

    generator = pydor.API(ri.registry, insecure=insecure).Tags(ri.repository)
    _list(generator, limit, output, insecure)


@click.command()
@click.argument('IMAGE')
@click.option('--insecure', default=False, is_flag=True,
              help="If set to true, the registry certificates will not be validated.", show_default=True)
@catch_http_errors()
def manifest(image, insecure):
    """
    Retrieve a manifest from a docker registry.

    Examples:

    \b
        pydor manifest quay.io/coreos/etcd:latest

    """
    ri = pydor.Image.from_image(image)

    manifest = pydor.Manifest(pydor.API(ri.registry, insecure=insecure).Manifest(ri.repository, ri.reference).get())
    click.echo(json.dumps(manifest.json, indent=4))


@click.command(short_help="Inspect an attribute of a docker image in docker registry.")
@click.argument('TYPE', type=click.Choice(pydor.MANIFEST_PROPERTIES))
@click.argument('IMAGE')
@click.option('--output', default=pydor.tools.tablib_text_module.title, type=click.Choice(OUTPUT_FORMATS), show_default=True, help="Output format.")
@click.option('--insecure', default=False, is_flag=True,
              help="If set to true, the registry certificates will not be validated.", show_default=True)
@catch_http_errors()
def inspect(type, image, output, insecure):
    """
    Inspect an attribute of a docker image in remote docker registry. TYPE is one of [labels, author, entrypoint, cmd]

    Examples:

    \b
        pydor inspect cmd quay.io/coreos/etcd:latest
    """

    ri = pydor.Image.from_image(image)

    manifest = pydor.Manifest(pydor.API(ri.registry, insecure=insecure).Manifest(ri.repository, ri.reference).get())

    inspected_object = getattr(manifest, type)

    dataset = tablib.Dataset(headers=inspected_object.headers)
    map(dataset.append, inspected_object.data)
    click.echo(getattr(dataset, output))


@click.command(short_help="Ping a docker registry to check if the address is a valid docker registry and is responding.")
@click.argument('REGISTRY')
@click.option('--insecure', default=False, is_flag=True,
              help="If set to true, the registry certificates will not be validated.", show_default=True)
@catch_http_errors()
def ping(registry, insecure):
    """
    Ping a docker registry to check if the address is a valid docker registry and is responding.

    Examples:

    \b
        pydor ping quay.io
    """
    try:
        response = pydor.API(registry, insecure).Base().get()
    except requests.exceptions.SSLError as e:
        logging.fatal(e.message)
        click.echo("Consider using --insecure")
        click.get_current_context().exit(pydor.errors.SSL_ERROR_CODE)

    if response.status_code == requests.codes.ok:
        click.echo("OK")
    elif response.status_code == requests.codes.not_found:
        click.echo("Error: registry does not implement v2 API")
        click.get_current_context().exit(pydor.errors.NOT_V2_REGISTRY)
    elif response.status_code == requests.codes.unauthorized:
        click.echo("Authorization not implemented yet... exiting")
        click.get_current_context().exit(pydor.errors.NOT_IMPLEMENTED)
    else:
        raise NotImplementedError()


@click.command(short_help="Checks whether image reference exists")
@click.argument('IMAGE')
@click.option('--insecure', default=False, is_flag=True,
              help="If set to true, the registry certificates will not be validated.", show_default=True)
def exists(image, insecure):
    """
    Checks whether image reference exists

    Examples:

    \b
        pydor exists quay.io/gilliam/base:latest
    """
    try:
        ri = pydor.Image.from_image(image)
        response = pydor.API(ri.registry, insecure).Manifest(ri.repository, ri.tag or ri.digest).get()
    except requests.exceptions.SSLError as e:
        logging.fatal(e.message)
        click.echo("Consider using --insecure")
        click.get_current_context().exit(pydor.errors.SSL_ERROR_CODE)
    except requests.exceptions.HTTPError as e:
        response = e.response

    if response.status_code == requests.codes.ok:
        click.echo("OK")
    elif response.status_code == requests.codes.not_found:
        click.echo("NOT FOUND")
        click.get_current_context().exit(pydor.errors.IMAGE_NOT_FOUND)
    elif response.status_code == requests.codes.unauthorized:
        click.echo("Received unauthorized... Authorization not implemented yet... exiting")
        click.get_current_context().exit(pydor.errors.NOT_IMPLEMENTED)
    else:
        raise NotImplementedError()


cli.add_command(list)
cli.add_command(tags)
cli.add_command(inspect)
cli.add_command(manifest)
cli.add_command(ping)
cli.add_command(exists)
cli.add_command(delete)

if __name__ == '__main__':
    cli()
