<a id="harlem.exporters.base"></a>

# harlem.exporters.base

<a id="harlem.exporters.base.HarExporter"></a>

## HarExporter

```python
class HarExporter()
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/3288cf1f0787c62d65a4b63ed890dae8f1eaed0b/harlem\exporters\base.py#L6)

<a id="harlem.exporters.base.HarExporter.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/3288cf1f0787c62d65a4b63ed890dae8f1eaed0b/harlem\exporters\base.py#L7)

<a id="harlem.exporters.base.HarExporter.get_next_page_id"></a>

#### get\_next\_page\_id

```python
def get_next_page_id() -> str
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/3288cf1f0787c62d65a4b63ed890dae8f1eaed0b/harlem\exporters\base.py#L11)

<a id="harlem.exporters.base.HarExporter.add_page"></a>

#### add\_page

```python
def add_page(page: Page)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/3288cf1f0787c62d65a4b63ed890dae8f1eaed0b/harlem\exporters\base.py#L16)

<a id="harlem.exporters.base.HarExporter.add_entry"></a>

#### add\_entry

```python
def add_entry(entry: Entry)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/3288cf1f0787c62d65a4b63ed890dae8f1eaed0b/harlem\exporters\base.py#L21)

<a id="harlem.exporters.base.HarExporter.start"></a>

#### start

```python
def start()
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/3288cf1f0787c62d65a4b63ed890dae8f1eaed0b/harlem\exporters\base.py#L34)

<a id="harlem.exporters.base.HarExporter.stop"></a>

#### stop

```python
def stop()
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/3288cf1f0787c62d65a4b63ed890dae8f1eaed0b/harlem\exporters\base.py#L38)

<a id="harlem.exporters.composite_exporter"></a>

# harlem.exporters.composite\_exporter

<a id="harlem.exporters.composite_exporter.CompositeHarExporter"></a>

## CompositeHarExporter

```python
class CompositeHarExporter(HarExporter)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/3288cf1f0787c62d65a4b63ed890dae8f1eaed0b/harlem\exporters\composite_exporter.py#L7)

An exporter that delegates to multiple exporters.

<a id="harlem.exporters.concurrent_exporter"></a>

# harlem.exporters.concurrent\_exporter

<a id="harlem.exporters.concurrent_exporter.ExecutorHarExporter"></a>

## ExecutorHarExporter

```python
class ExecutorHarExporter(HarExporter)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/3288cf1f0787c62d65a4b63ed890dae8f1eaed0b/harlem\exporters\concurrent_exporter.py#L9)

An exporter that delegates to another exporter and uses an executor to run the operations concurrently.
Please note that the inner exporter should be thread-safe (or process-safe, if using a ProcessPoolExecutor),
or things might not work properly.

<a id="harlem.exporters.concurrent_exporter.BackgroundThreadHarExporter"></a>

## BackgroundThreadHarExporter

```python
class BackgroundThreadHarExporter(HarExporter)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/3288cf1f0787c62d65a4b63ed890dae8f1eaed0b/harlem\exporters\concurrent_exporter.py#L38)

An exporter that delegates to another exporter and executes it in a separate thread in the background.
Uses a ThreadPoolExecutor with a single worker to work around non-thread-safe exporters.

<a id="harlem.exporters.concurrent_exporter.BackgroundProcessHarExporter"></a>

## BackgroundProcessHarExporter

```python
class BackgroundProcessHarExporter(HarExporter)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/3288cf1f0787c62d65a4b63ed890dae8f1eaed0b/harlem\exporters\concurrent_exporter.py#L72)

An exporter that delegates to another exporter and executes it in a separate process in the background.

<a id="harlem.exporters.io_exporter"></a>

# harlem.exporters.io\_exporter

<a id="harlem.exporters.io_exporter.IoHarExporter"></a>

## IoHarExporter

```python
class IoHarExporter(HarExporter)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/3288cf1f0787c62d65a4b63ed890dae8f1eaed0b/harlem\exporters\io_exporter.py#L10)

An exporter that writes the HAR to an IO object.
Allows manual updates to the file using the update_file method.

<a id="harlem.exporters.io_exporter.IoHarExporter.update_file"></a>

#### update\_file

```python
def update_file()
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/3288cf1f0787c62d65a4b63ed890dae8f1eaed0b/harlem\exporters\io_exporter.py#L42)

Save the HAR to the destination.

<a id="harlem.exporters.io_exporter.FileHarExporter"></a>

## FileHarExporter

```python
class FileHarExporter(IoHarExporter)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/3288cf1f0787c62d65a4b63ed890dae8f1eaed0b/harlem\exporters\io_exporter.py#L57)

An exporter that writes the HAR to a file.
Syntax sugar for IoHarExporter.

<a id="harlem.exporters.live_file_exporter"></a>

# harlem.exporters.live\_file\_exporter

<a id="harlem.exporters.live_file_exporter.LiveFileHarExporter"></a>

## LiveFileHarExporter

```python
class LiveFileHarExporter(HarExporter)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/3288cf1f0787c62d65a4b63ed890dae8f1eaed0b/harlem\exporters\live_file_exporter.py#L12)

An exporter that writes the HAR to a file in real-time.
Allows manual updates to the file using the update_file method.

<a id="harlem.exporters.live_file_exporter.LiveFileHarExporter.update_file"></a>

#### update\_file

```python
def update_file()
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/3288cf1f0787c62d65a4b63ed890dae8f1eaed0b/harlem\exporters\live_file_exporter.py#L87)

Writes the current state of the exporter to the file.

<a id="harlem.exporters.logging_exporter"></a>

# harlem.exporters.logging\_exporter

<a id="harlem.exporters.logging_exporter.LoggingHarExporter"></a>

## LoggingHarExporter

```python
class LoggingHarExporter(HarExporter)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/3288cf1f0787c62d65a4b63ed890dae8f1eaed0b/harlem\exporters\logging_exporter.py#L9)

An exporter that logs the HAR to a logging.logger.
New page and entry objects are dumped to the log's extra field as dictionaries
in the "har_page" and "har_entry" keys.

<a id="harlem.exporters.model_exporter"></a>

# harlem.exporters.model\_exporter

<a id="harlem.exporters.model_exporter.ModelHarExporter"></a>

## ModelHarExporter

```python
class ModelHarExporter(HarExporter)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/3288cf1f0787c62d65a4b63ed890dae8f1eaed0b/harlem\exporters\model_exporter.py#L6)

An exporter that builds a HAR model from pages and entries.

<a id="harlem.exporters.model_exporter.ModelHarExporter.to_model"></a>

#### to\_model

```python
def to_model() -> Har
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/3288cf1f0787c62d65a4b63ed890dae8f1eaed0b/harlem\exporters\model_exporter.py#L22)

Builds and returns the HAR model.

**Returns**:

The HAR model.

