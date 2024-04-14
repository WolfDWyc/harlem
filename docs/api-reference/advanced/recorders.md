<a id="harlem.recorders.aiohttp_recorder"></a>

# harlem.recorders.aiohttp\_recorder

<a id="harlem.recorders.aiohttp_recorder.AiohttpHarRecorder"></a>

## AiohttpHarRecorder

```python
class AiohttpHarRecorder(HarRecorder)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\recorders\aiohttp_recorder.py#L186)

A recorder that listens for requests made by the requests library.

<a id="harlem.recorders.base"></a>

# harlem.recorders.base

<a id="harlem.recorders.base.HarRecorder"></a>

## HarRecorder

```python
class HarRecorder()
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\recorders\base.py#L6)

<a id="harlem.recorders.base.HarRecorder.__init__"></a>

#### \_\_init\_\_

```python
def __init__(exporter: HarExporter)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\recorders\base.py#L7)

<a id="harlem.recorders.base.HarRecorder.start"></a>

#### start

```python
def start()
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\recorders\base.py#L18)

Starts recording the network requests.
Can be called multiple times to pause and resume recording.

<a id="harlem.recorders.base.HarRecorder.stop"></a>

#### stop

```python
def stop()
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\recorders\base.py#L26)

Stops recording the network requests.

<a id="harlem.recorders.base.HarRecorder.__enter__"></a>

#### \_\_enter\_\_

```python
def __enter__()
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\recorders\base.py#L35)

<a id="harlem.recorders.base.HarRecorder.__exit__"></a>

#### \_\_exit\_\_

```python
def __exit__(exc_type, exc_val, exc_tb)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\recorders\base.py#L39)

<a id="harlem.recorders.composite_recorder"></a>

# harlem.recorders.composite\_recorder

<a id="harlem.recorders.composite_recorder.CompositeHarRecorder"></a>

## CompositeHarRecorder

```python
class CompositeHarRecorder(HarRecorder)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\recorders\composite_recorder.py#L7)

A recorder that listens for requests made by multiple libraries.

<a id="harlem.recorders.composite_recorder.CompositeHarRecorder.__init__"></a>

#### \_\_init\_\_

```python
def __init__(recorders: List[Callable[[HarExporter], HarRecorder]],
             exporter: HarExporter)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\recorders\composite_recorder.py#L12)

<a id="harlem.recorders.requests_recorder"></a>

# harlem.recorders.requests\_recorder

<a id="harlem.recorders.requests_recorder.RequestsHarRecorder"></a>

## RequestsHarRecorder

```python
class RequestsHarRecorder(HarRecorder)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\recorders\requests_recorder.py#L99)

A recorder that listens for requests made by the requests library.

