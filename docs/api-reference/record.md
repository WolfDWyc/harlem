<a id="harlem.record"></a>

# harlem.record

<a id="harlem.record.record_to_file"></a>

#### record\_to\_file

```python
@contextmanager
def record_to_file(path: Union[None, str, Path] = None,
                   indent: Optional[int] = None,
                   live: bool = False,
                   interval_seconds: Optional[float] = None,
                   retention_seconds: Optional[float] = None,
                   in_background: Literal[None, "thread", "process"] = None)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\record.py#L39)

A simple context-manager API for recording to HAR files.

**Arguments**:

- `path`: The path to save the HAR to.
- `indent`: The number of spaces to use for indentation in the output JSON HAR file.
- `live`: Whether to log to the file in real-time, or only when the context manager exits.
- `interval_seconds`: Write to the file on an interval instead of only when the context manager exits.
The file will also be written when the context manager exits.
- `retention_seconds`: Optional number of seconds to keep old pages and entries.
If None, old pages and entries will not be removed.
Pages that are too old but still have entries will be kept.
If no interval is set, rotation will only happen after a new page or entry is added.
Rotation will also happen when the context manager exits.
- `in_background`: Whether to export in the background.
If "thread", exports in a separate thread. If "process", exports in a separate process.

<a id="harlem.record.record_to_logger"></a>

#### record\_to\_logger

```python
@contextmanager
def record_to_logger(logger: Optional[logging.Logger] = None,
                     level: Union[int, str] = logging.DEBUG,
                     new_page_message: str = "New HAR page added",
                     new_entry_message: str = "New HAR entry added",
                     in_background: Literal[None, "thread", "process"] = None)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\record.py#L86)

A simple context-manager API for recording new pages and entries to a logger.

New page and entry objects are dumped to the log's extra field as dictionaries
in the "har_page" and "har_entry" keys.

**Arguments**:

- `logger`: The logger to log to.
If not provided, the default __name__ logger will be used.
- `level`: The log level to log at.
- `new_page_message`: The message to log when a new page is added.
- `new_entry_message`: The message to log when a new entry is added.
- `in_background`: Whether to export in the background.
If "thread", exports in a separate thread. If "process", exports in a separate process.

