# harlem

Harlem is a small Python (3.8+) library for recording Python HTTP traffic to HAR (HTTP Archive) files.

HAR is traditionally a file format for logging of a web browser's interaction with a site.
Harlem extends this functionality to Python programs.

HAR files are very useful for logging, debugging, and more.
They're especially useful since browsers like Chrome and Firefox support importing HAR files
to their developer tools network tab, which can help understanding your application's network activity.

[CLI Usage](#CLI-Usage) |
[Python Usage](#Python-Usage) |
[Documentation](#Documentation) |
[API Reference](#API-Reference) |
[Credits](#Credits)

## Installation

```bash
pip install harlem
```

# Features

Harlem exposes a simple API using a CLI and a simple context manager (for Python usage),
but also provides an advanced API for more control.

Currently supported:
- `requests` recorder
- `aiohttp` recorder
- Extended `_initiator` field for call frames
- Exporting*
  - To a model
  - To a file (or any IO object)
  - To logging
  - Live recording (After every request, with an interval, or with a time based rotation)
  - Concurrent/threaded/asynchronous recording
- Exporting on abnormal exit (e.g. KeyboardInterrupt)

*Read in [Exporter documentation](#Exporters) about why Harlem implements exporting itself.


Planned features (in no particular order):
- Optimize memory usage of live exporting
- Show requests that got connection errors
- Extensive testing for multiple library versions
- `httpx` recorder
- `fastapi` recorder

# Quickstart

## CLI Usage

Harlem's CLI is the simplest way to use Harlem.
You run your program with the `harlem` command, and it will output a HAR file when your program exits.

```bash
# If all you want is to get an HAR file when your program exits, simply do this:
harlem mypackage.main:start my_program_log.har
# Also works with python -m
python -m harlem mypackage.main:start my_program_log.har

# For human readable output, you can indent the output:
harlem mypackage.main:start my_program_log.har --indent 2

# If you want your HAR file to update after every request (useful for long running programs),
# you can use the `--live` argument:
harlem mypackage.main:start my_program_log.har --live
# However, if your program makes a lot of requests, you might only want to update the HAR file every 10 seconds:
harlem mypackage.main:start my_program_log.har --interval-seconds 10
# And to cut back on the amount of data, you can add a time based rotation:
harlem mypackage.main:start my_program_log.har --interval-seconds 10 --retention-seconds 3600

# For even better performance, or for asyncio programs, you can use the `--in-background` argument:
harlem mypackage.main:start my_program_log.har --interval-seconds 10 --in-background thread
# Or in a separate process:
harlem mypackage.main:start my_program_log.har --interval-seconds 10 --in-background process

# All flags have short versions:
harlem mypackage.main:start my_program_log.har -i 2 -l -n 10 -r 3600 -b thread
```
For more information, use the --help flag or see the [CLI-Reference](docs/api-reference/cli.md)

## Python Usage

The `record_to_file()` context manager provides the same functionality as the CLI, but in Python.
It's arguments and semantics are the same as the CLI.

```python
from harlem import record_to_file

with record_to_file("my_program_log.har", live=True):
  my_program()

with record_to_file("my_program_log.har", indent=2, interval_seconds=10, retention_seconds=3600):
  my_program()

with record_to_file("my_program_log.har", interval_seconds=10, in_background="process"):
  my_program()
```

For more information, see the [`record_to_file()` reference](docs/api-reference/record.md#record_to_file)

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

For more information, see the [`record_to_logger()` reference](docs/api-reference/record.md#record_to_logger)

# Documentation

Harlem's full documentation is available in this repository.
All major features, design decisions, and caveats are documented in this file,
and the full API reference is available [here](docs/api-reference/README.md).

## Design

Harlem's API exposes a recorder for each library it supports.
Recorders are generally provided by Harlem itself.

Recorders are context managers that report on any HTTP requests made within their context.
Each recorder accepts an exporter it reports to, and the exporter is responsible for handling the data.

Exporters usually write the data to an external source, but can also be used to log the data,
to return it as a Pydantic model, or anything else.
Harlem encourages writing custom exporters, but provides many built-in exporters for convenience.

## Recorders

Recorders are context managers that record HTTP requests made within their context.
They also support manual `start()` and `stop()` methods, which can be called multiple times.
They all inherit from the `HarRecorder` interface.

Harlem currently  supports the `RequestsHarRecorder` for `requests` recorder,
and the `AiohttpHarRecorder` for `aiohttp` recorder, which both accept no arguments.

For more information, see the [Recorders reference](docs/api-reference/advanced/recorders.md)

### How recorders work

Recorders usually work by patching the library they record,
while also using hooking mechanisms provided by the library for more information.

For example, in `aiohttp`, the `AiohttpHarRecorder` patches the `ClientSession` class to record requests.



## Exporters

Exporters are responsible for handling the data recorded by the recorder.
They all inherit from the `HarExporter` interface.

The provided exporters are:
- `ModelHarExporter` - Exports the data as a Pydantic model
- `LiveFileHarExporter` - Exports the data to a file in real-time
- `LoggingHarExporter` - Logs the data to a logger
- `FileHarExporter` - Exports the data to a file
- `IoHarExporter` - Exports the data to any IO object
- `CompositeHarExporter` - Exports the data to multiple exporters
- `ExecutorHarExporter` - Exports the data in a separate `concurrent.futures.Executor` (not thread-safe)
- `BackgroundThreadHarExporter` - Exports the data in a separate thread
- `BackgroundProcessHarExporter` - Exports the data in a separate process

For more information, see the [Exporters reference](docs/api-reference/advanced/exporters.md)

### Why Harlem implements exporting itself

Initially, it might seem like Harlem is trying to reinvent the wheel by implementing exporting itself.
After all, HAR files are logs, and many logging libraries already have extensive rotation implementations.
So why not just use those?

This boils down to how HAR works. HAR files consist of a list of entries and pages that are generated for each request.
So if we just handed off new entries and pages to a logging library,
we would have to do extra processing to format them into a HAR file externally.

This is useful for more advanced use cases - for example, if you want to save the last 30 days of requests,
it's probably not a good idea to keep all of them in memory, or even in a single file on disk.
Instead, you could use a logging library to save each entry to a separate file, and then merge them into a HAR file when needed.

Harlem *does* support this using `record_to_logger` and `LoggingHarExporter` which logs each entry to a provided logger.

However, Harlem also intends to be simple, and output a complete HAR file which can be imported into an HAR viewer
without any extra processing. Thus, Harlem provides exporters that handle the entire HAR file for many common use cases.

### Concurrent exporters

Some of Harlem's exporters are concurrent, meaning they export the data in a separate thread or process.

Apart from the obvious `ExecutorHarExporter`, `BackgroundThreadHarExporter` (`in_background="thread"`)
and `BackgroundProcessHarExporter` (`in_background="process"`) exporters,
interval-based exporting (which uses `LiveFileHarExporter` internally) also uses a separate thread,
if an interval is provided - to ensure the interval is kept even if no requests are made.

This can be disabled by setting `hard_interval` to `False` when using the `LiveFileHarExporter` API,
or not providing an interval at all (not available in the CLI or `record_to_file()`).

Harlem tries to handle concurrency as good as it can, but it's not perfect.
Harlem sets a 10-second timeout for the`BackgroundProcessHarExporter` to join the process.
It does the same for the live exporter's background thread.
These timeouts are configurable using the `join_timeout` argument.

If, for example, the HAR file is very large, or the file system is very slow, this timeout might be too short.
Using the `BackgroundProcessHarExporter` timeout exceeding can cause corruption of the HAR file.

For the `LiveFileHarExporter`, the thread can not be forcefully stopped, 
so it will always finish updating, even if that means it will continue after the timeout.

Generally, these should be safe to use, even in production environments, as you're unlikely to run into these issues.
And even if you do, none of this should hurt your program, and the worst that could happen is corruption of the HAR
file, or the file being locked for after the timeout. The leaking thread will only be 1 per recording,
which shouldn't be more than 1 for most programs.

However, if you absolutely can not afford to lose data, leak any thread, or have a specific use case 
with a lot of requests and a lot of recordings, it's always recommended to use the `record_to_logger()` or
`LoggingHarExporter`, or simply turn off concurrent features, if performance is not a concern.
This moves the exporting to your logging system, which should be more optimized for your use case.

# Credits
- https://github.com/ahmadnassri/har-schema
- http://www.softwareishard.com/blog/har-12-spec
- https://indigo.re/posts/2020-10-09-har-is-clumsy.html
- Harlem's API is inspired by [loguru](https://github.com/Delgan/loguru)
[py-spy](https://github.com/benfred/py-spy), [tqdm](https://github.com/tqdm/tqdm),
and [uvicorn](https://github.com/encode/uvicorn)
