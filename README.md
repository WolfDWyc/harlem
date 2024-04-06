# harlem

Harlem is a small Python (3.8+) library for recording Python HTTP traffic to HAR (HTTP Archive) files.

HAR is traditionally a file format for logging of a web browser's interaction with a site.
Harlem extends this functionality to Python programs.

HAR files are very useful for logging, debugging, and more.
They're especially useful since browsers Chrome and Firefox support importing HAR files
to their developer tools network tab, which can help understanding your application's network activity.

# Features

Harlem exposes a simple API using the `record()` context manager,
but also provides a more advanced API for more control.

For some libraries Harlem also exposes standalone parsing functions that create
HAR entries (and not an entire file as opposed to a recorder).

Currently supported:
- `requests` recorder
- Extended `_initiator` field for call frames (when applicable)
- Exporting*
  - To a model
  - To a file (or any IO object)
  - To logging
  - Live recording
    - After every request
    - With an interval
    - With a time based rotation
  - Concurrent/threaded/asynchronous recording

*Read in [Exporter documentation](#Exporters) about why Harlem implements exporting itself.


Planned support:
- Exporters
- `requests` parser
- `aiohttp` recorder/parser
- `httpx` recorder/parser
- `fastapi` recorder/parser

# How to use

## Quick start

If all you want is to get an HAR file when your program finishes, simply do this:

```python
from harlem import record

with record("my_program.har"):
    my_program()

# And that's it! You'll get an HAR file with all the requests made by `my_program()`.

# For human readable output, you can indent the output:

with record("my_program.har", indent=2):
    my_program()

# If you want your HAR file to update after every request (useful for long running programs),
# you can use the `live` argument:

with record("my_program.har", indent=2, live=True):
    my_program()


# However, if your program makes a lot of requests, you might only want to update the HAR file every 10 seconds:

with record("my_program.har", indent=2, live=True, interval_seconds=10):
    my_program()

# And to cut back on the amount of data, you can add a time based rotation:
with record("my_program.har", live=True, interval_seconds=10, retention_seconds=3600):
    my_program()

# ('retention_seconds' also works without 'interval_seconds')

# For even better performance, or for asyncio programs, you can use the `in_background` argument:

with record("my_program.har", live=True, interval_seconds=10, in_background="thread"):
    my_program()
    
# Or in a separate process:

with record("my_program.har", live=True, interval_seconds=10, in_background="process"):
    my_program()
    
# ('in_background' currently only affects the exporting process)

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

#### ModelHarExporter

[W.I.P] Docs in progress




# Credits
- https://github.com/ahmadnassri/har-schema
- http://www.softwareishard.com/blog/har-12-spec
- https://indigo.re/posts/2020-10-09-har-is-clumsy.html
