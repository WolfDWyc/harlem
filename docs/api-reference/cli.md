<a id="harlem.cli"></a>

# harlem.cli

<a id="harlem.cli.main"></a>

#### main

```python
@click.command(help="""
Record a HAR file of a Python application. 
Accepts an import string for the application to run and an output file path to write the HAR to.

The import string should be in the format '<module>:<attribute>'. (e.g. 'mypackage.main:start')
""")
@click.argument(
    "app",
    type=str,
)
@click.argument(
    "output_path",
    type=click.Path(file_okay=True,
                    dir_okay=False,
                    writable=True,
                    readable=False),
)
@click.option(
    "--indent",
    "-i",
    type=int,
    help=
    "The number of spaces to use for indentation in the output JSON HAR file.",
)
@click.option(
    "--live",
    "-l",
    is_flag=True,
    show_default=True,
    help="Whether to log to the file in real-time or only on exit.",
)
@click.option(
    "--interval-seconds",
    "-n",
    type=float,
    help="Write to the file on an interval instead of only on exit. "
    "The file will also be written on exit.",
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
    "If 'thread', exports in a separate thread. If 'process', exports in a separate process.",
)
def main(app: str,
         output_path: Path,
         indent: Union[None, int] = None,
         live: bool = False,
         interval_seconds: Union[None, float] = None,
         retention_seconds: Union[None, float] = None,
         in_background: Union[None, str] = None)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\cli.py#L105)

