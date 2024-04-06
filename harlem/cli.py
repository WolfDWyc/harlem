import importlib
import logging
from pathlib import Path
from typing import Any, Union

import click

from harlem import record_to_file


class ImportFromStringError(Exception):
    pass


# Taken from https://github.com/encode/uvicorn/blob/master/uvicorn/importer.py
def import_from_string(import_str: Any) -> Any:
    if not isinstance(import_str, str):
        return import_str

    module_str, _, attrs_str = import_str.partition(":")
    if not module_str or not attrs_str:
        message = 'Import string "{import_str}" must be in format "<module>:<attribute>".'
        raise ImportFromStringError(message.format(import_str=import_str))

    try:
        module = importlib.import_module(module_str)
    except ModuleNotFoundError as exc:
        if exc.name != module_str:
            raise exc from None
        message = 'Could not import module "{module_str}".'
        raise ImportFromStringError(message.format(module_str=module_str))

    instance = module
    try:
        for attr_str in attrs_str.split("."):
            instance = getattr(instance, attr_str)
    except AttributeError:
        message = 'Attribute "{attrs_str}" not found in module "{module_str}".'
        raise ImportFromStringError(message.format(attrs_str=attrs_str, module_str=module_str))

    return instance


def a():
    logging.warning("TEST2")


@click.command(
    help="""
Record a HAR file of a Python application. 
Accepts an import string for the application to run and an output file path to write the HAR to.

The import string should be in the format '<module>:<attribute>'. (e.g. 'mypackage.main:start')
"""
)
@click.argument(
    "app",
    type=str,
)
@click.argument(
    "output_path",
    type=click.Path(file_okay=True, dir_okay=False, writable=True, readable=False),
)
@click.option(
    "--indent",
    "-i",
    type=int,
    help="The number of spaces to use for indentation in the output JSON HAR file.",
)
@click.option(
    "--live",
    "-l",
    is_flag=True,
    show_default=True,
    help="Whether to log to the file in real-time or only on exit."
)
@click.option(
    "--interval-seconds",
    "-n",
    type=float,
    help="Write to the file on an interval instead of only on exit. "
         "The file will also be written on exit."
)
@click.option(
    "--retention-seconds",
    "-r",
    type=float,
    help="Optional number of seconds to keep old pages and entries. "
         "If None, old pages and entries will not be removed. "
         "Pages that are too old but still have entries will be kept. "
         "If no interval is set, rotation will only happen after a new page or entry is added. "
         "Rotation will also happen on exit.",
)
@click.option(
    "--in-background",
    "-b",
    type=click.Choice(["thread", "process"]),
    help="Whether to export in the background. "
         "If 'thread', exports in a separate thread. If 'process', exports in a separate process."
)
def main(
        app: str,
        output_path: Path,
        indent: Union[None, int] = None,
        live: bool = False,
        interval_seconds: Union[None, float] = None,
        retention_seconds: Union[None, float] = None,
        in_background: Union[None, str] = None,
):
    app = import_from_string(app)
    with record_to_file(
            output_path,
            indent=indent,
            live=live,
            interval_seconds=interval_seconds,
            retention_seconds=retention_seconds,
            in_background=in_background,
    ):
        app()


if __name__ == '__main__':
    main()
