# harlem

Harlem is a small Python (3.8+) library for recording Python HTTP traffic to HAR (HTTP Archive) files.

HAR is traditionally a file format for logging of a web browser's interaction with a site.
Harlem extends this functionality to Python programs.

HAR files are very useful for logging, debugging, and more.
They're especially useful since browsers like Chrome and Firefox support importing HAR files
to their developer tools network tab, which can help understanding your application's network activity.

[CLI Usage](#CLI-Usage) |
[Python API](#Python-Quick-Start) |
[Advanced Documentation](#Advanced-Documentation) |
[Credits](#Credits)

## Installation

```bash
pip install harlem
```

# Features

Harlem exposes a simple API using a CLI and a simple context manager (for Python usage),
but also provides an advanced API for more control.

For some libraries Harlem also exposes standalone parsing functions that create
HAR entries (and not an entire file as opposed to a recorder).

Currently supported:
- `requests` recorder
- Extended `_initiator` field for call frames
- Exporting*
  - To a model
  - To a file (or any IO object)
  - To logging
  - Live recording
    - After every request
    - With an interval
    - With a time based rotation
  - Concurrent/threaded/asynchronous recording
- Exporting on abnormal exit (e.g. KeyboardInterrupt)

*Read in [Exporter documentation](#Exporters) about why Harlem implements exporting itself.


Planned features:
- Optimize memory usage of live exporting
- Show requests that got connection errors
- `requests` parser
- `aiohttp` recorder/parser
- `httpx` recorder/parser
- `fastapi` recorder/parser

# CLI Usage

If all you want is to get an HAR file when your program exits, simply do this:

```bash
harlem mypackage.main:start my_program.har

# Also works with python -m
python -m harlem mypackage.main:start my_program.har

# For human readable output, you can indent the output:
harlem mypackage.main:start my_program.har --indent 2

# If you want your HAR file to update after every request (useful for long running programs),
# you can use the `--live` argument:
harlem mypackage.main:start my_program.har --live

# However, if your program makes a lot of requests, you might only want to update the HAR file every 10 seconds:
harlem mypackage.main:start my_program.har --interval-seconds 10

# And to cut back on the amount of data, you can add a time based rotation:
harlem mypackage.main:start my_program.har --interval-seconds 10 --retention-seconds 3600

# For even better performance, or for asyncio programs, you can use the `--in-background` argument:
harlem mypackage.main:start my_program.har --interval-seconds 10 --in-background thread

# Or in a separate process:
harlem mypackage.main:start my_program.har --interval-seconds 10 --in-background process

# All flags have short versions:
harlem mypackage.main:start my_program.har -i 2 -l -n 10 -r 3600 -b thread
```
For more information, use the --help flag:
```
Usage: harlem [OPTIONS] APP OUTPUT_PATH                                       
                                                                              
  Record a HAR file of a Python application.  Accepts an import string for the
  application to run and an output file path to write the HAR to.             
                                                                              
  The import string should be in the format '<module>:<attribute>'. (e.g.     
  'main:start')                                                               
                                                                              
Options:                                                                      
  -i, --indent INTEGER            The number of spaces to use for indentation 
                                  in the output JSON HAR file.                
  -l, --live                      Whether to log to the file in real-time, or 
                                  only when the context manager exits. If     
                                  false, all interval and retention options   
                                  are ignored. Defaults to False.             
  -n, --interval-seconds FLOAT    Optional number of seconds to wait between  
                                  writes to the file. If None, the file will
                                  be written every time a new page or entry is
                                  added. The file will also be written on
                                  exit.
  -r, --retention-seconds FLOAT   Optional number of seconds to keep old pages
                                  and entries. If None, old pages and entries
                                  will not be removed. Pages that are too old
                                  but still have entries will be kept. If no
                                  interval is set, rotation will only happen
                                  after a new page or entry is added. Rotation
                                  will also happen on exit.
  -b, --in-background [thread|process]
                                  Whether to export in the background. If
                                  'thread', exports in a separate thread. If
                                  'process', exports in a separate process.
  --help                          Show this message and exit.
```


# Python Usage

## Quick start

The `record_to_file()` context manager is the simplest way to use Harlem from Python.
It's arguments and semantics are the same as the CLI.

```python
from harlem import record_to_file

with record_to_file("my_program.har", live=True):
  my_program()

with record_to_file("my_program.har", indent=2, interval_seconds=10, retention_seconds=3600):
  my_program()

with record_to_file("my_program.har", interval_seconds=10, in_background="process"):
  my_program()
```

For non-cli usage, another common use case is to use the `record_to_logger()` context manager.
This will log each new entry and page to the log's extra field.

This may be useful for large programs, where you don't want to keep the entire HAR file in memory -
or even on disk, but to export it to your logging system.

This will require minimal processing to convert the log entries to a HAR file when you need to view them.
This processing is partially provided using the `to_har_model()` function which accepts a list of pages and entries.

```python
from harlem import record_to_logger

# Simple usage:
with record_to_logger(): # Logs to the default logger
  my_program()
  
# Or with some more customization:
with record_to_logger(
    logger=my_logger,
    level=logging.INFO,
    new_page_message="New page logged using harlem",
    new_entry_message="New entry logged using harlem",
    in_background="thread" # Same semantics as the CLI/record_to_file in_background option
):
    my_program()
```


## Advanced Documentation

Since harlem is very small, the documentation is fully available here (and in docstrings).

### How it works

Harlem's API works by exposing a recorder for each library it supports.
Recorders are generally provided by Harlem itself.

Recorders are context managers that report on any HTTP requests made within their context.
Each recorder accepts an exporter it reports to, and the exporter is responsible for handling the data.

Exporters usually write the data to an external source, but can also be used to log the data,
to return it as a Pydantic model, or anything else.
Harlem encourages writing custom exporters, but provides many built-in exporters for convenience.

### Recorders

Recorders are context managers that record HTTP requests made within their context.
They also support manual `start()` and `stop()` methods, which can be called multiple times.

Harlem currently only supports the `RequestsHarRecorder` for `requests` recorder, which accepts no arguments.

### Exporters

Exporters are responsible for handling the data recorded by the recorder.

#### Why Harlem implements exporting itself

Initially, it might seem like Harlem is trying to reinvent the wheel by implementing exporting itself.
After all, HAR files are logs, and many logging libraries already have extensive rotation implementations.
So why not just use those?

This boils down to how HAR works. HAR files consist of a list of entries and pages that are generated for each request.
So if we just handed off new entries and pages to a logging library,
we would have to do extra processing to format them into a HAR file.

This is useful for more advanced use cases - for example, if you want to save the last 30 days of requests,
it's probably not a good idea to keep all of them in memory, or even in a single file on disk.
Instead, you could use a logging library to save each entry to a separate file, and then merge them into a HAR file when needed.

Harlem *does* support this using `record_to_logger` and `LoggingHarExporter` which logs each entry to a provided logger.

However, Harlem also intends to be simple, and output a complete HAR file which can be imported into an HAR viewer
without any extra processing. This is why Harlem implements exporting itself.

#### ModelHarExporter

[W.I.P] Docs in progress




# Credits
- https://github.com/ahmadnassri/har-schema
- http://www.softwareishard.com/blog/har-12-spec
- https://indigo.re/posts/2020-10-09-har-is-clumsy.html
- Harlem's API is inspired by [loguru](https://github.com/Delgan/loguru)
[py-spy](https://github.com/benfred/py-spy), [tqdm](https://github.com/tqdm/tqdm),
and [uvicorn](https://github.com/encode/uvicorn)
