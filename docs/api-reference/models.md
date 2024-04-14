<a id="harlem.models.har"></a>

# harlem.models.har

<a id="harlem.models.har.Creator"></a>

## Creator

```python
class Creator(BaseModel)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\models\har.py#L9)

<a id="harlem.models.har.Creator.name"></a>

#### name: `str`

<a id="harlem.models.har.Creator.version"></a>

#### version: `str`

<a id="harlem.models.har.Creator.comment"></a>

#### comment: `Optional[str]`

<a id="harlem.models.har.Browser"></a>

## Browser

```python
class Browser(BaseModel)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\models\har.py#L15)

<a id="harlem.models.har.Browser.name"></a>

#### name: `str`

<a id="harlem.models.har.Browser.version"></a>

#### version: `str`

<a id="harlem.models.har.Browser.comment"></a>

#### comment: `Optional[str]`

<a id="harlem.models.har.PageTimings"></a>

## PageTimings

```python
class PageTimings(BaseModel)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\models\har.py#L21)

<a id="harlem.models.har.PageTimings.onContentLoad"></a>

#### onContentLoad: `Optional[float]`

<a id="harlem.models.har.PageTimings.onLoad"></a>

#### onLoad: `Optional[float]`

<a id="harlem.models.har.PageTimings.comment"></a>

#### comment: `Optional[str]`

<a id="harlem.models.har.Cookie"></a>

## Cookie

```python
class Cookie(BaseModel)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\models\har.py#L27)

<a id="harlem.models.har.Cookie.name"></a>

#### name: `str`

<a id="harlem.models.har.Cookie.value"></a>

#### value: `str`

<a id="harlem.models.har.Cookie.path"></a>

#### path: `Optional[str]`

<a id="harlem.models.har.Cookie.domain"></a>

#### domain: `Optional[str]`

<a id="harlem.models.har.Cookie.expires"></a>

#### expires: `Optional[AwareDatetime]`

<a id="harlem.models.har.Cookie.httpOnly"></a>

#### httpOnly: `Optional[bool]`

<a id="harlem.models.har.Cookie.secure"></a>

#### secure: `Optional[bool]`

<a id="harlem.models.har.Cookie.comment"></a>

#### comment: `Optional[str]`

<a id="harlem.models.har.Header"></a>

## Header

```python
class Header(BaseModel)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\models\har.py#L38)

<a id="harlem.models.har.Header.name"></a>

#### name: `str`

<a id="harlem.models.har.Header.value"></a>

#### value: `str`

<a id="harlem.models.har.Header.comment"></a>

#### comment: `Optional[str]`

<a id="harlem.models.har.Query"></a>

## Query

```python
class Query(BaseModel)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\models\har.py#L44)

<a id="harlem.models.har.Query.name"></a>

#### name: `str`

<a id="harlem.models.har.Query.value"></a>

#### value: `str`

<a id="harlem.models.har.Query.comment"></a>

#### comment: `Optional[str]`

<a id="harlem.models.har.Params"></a>

## Params

```python
class Params(BaseModel)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\models\har.py#L50)

<a id="harlem.models.har.Params.name"></a>

#### name: `str`

<a id="harlem.models.har.Params.value"></a>

#### value: `Optional[str]`

<a id="harlem.models.har.Params.fileName"></a>

#### fileName: `Optional[str]`

<a id="harlem.models.har.Params.contentType"></a>

#### contentType: `Optional[str]`

<a id="harlem.models.har.Params.comment"></a>

#### comment: `Optional[str]`

<a id="harlem.models.har.PostData"></a>

## PostData

```python
class PostData(BaseModel)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\models\har.py#L58)

<a id="harlem.models.har.PostData.mimeType"></a>

#### mimeType: `str`

<a id="harlem.models.har.PostData.text"></a>

#### text: `Optional[str]`

<a id="harlem.models.har.PostData.params"></a>

#### params: `Optional[Union[List, Params]]`

<a id="harlem.models.har.PostData.comment"></a>

#### comment: `Optional[str]`

<a id="harlem.models.har.Content"></a>

## Content

```python
class Content(BaseModel)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\models\har.py#L65)

<a id="harlem.models.har.Content.size"></a>

#### size: `int`

<a id="harlem.models.har.Content.compression"></a>

#### compression: `Optional[int]`

<a id="harlem.models.har.Content.mimeType"></a>

#### mimeType: `str`

<a id="harlem.models.har.Content.text"></a>

#### text: `Optional[str]`

<a id="harlem.models.har.Content.encoding"></a>

#### encoding: `Optional[str]`

<a id="harlem.models.har.Content.comment"></a>

#### comment: `Optional[str]`

<a id="harlem.models.har.BeforeRequest"></a>

## BeforeRequest

```python
class BeforeRequest(BaseModel)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\models\har.py#L74)

<a id="harlem.models.har.BeforeRequest.expires"></a>

#### expires: `Optional[
        constr(
            pattern=r"^(\d{4})(-)?(\d\d)(-)?(\d\d)(T)?(\d\d)(:)?(\d\d)(:)?(\d\d)(\.\d+)?(Z|([+-])(\d\d)(:)?(\d\d))?"
        )
    ]`

<a id="harlem.models.har.BeforeRequest.lastAccess"></a>

#### lastAccess: `constr(
        pattern=r"^(\d{4})(-)?(\d\d)(-)?(\d\d)(T)?(\d\d)(:)?(\d\d)(:)?(\d\d)(\.\d+)?(Z|([+-])(\d\d)(:)?(\d\d))?"
    )`

<a id="harlem.models.har.BeforeRequest.eTag"></a>

#### eTag: `str`

<a id="harlem.models.har.BeforeRequest.hitCount"></a>

#### hitCount: `int`

<a id="harlem.models.har.BeforeRequest.comment"></a>

#### comment: `Optional[str]`

<a id="harlem.models.har.AfterRequest"></a>

## AfterRequest

```python
class AfterRequest(BaseModel)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\models\har.py#L88)

<a id="harlem.models.har.AfterRequest.expires"></a>

#### expires: `Optional[
        constr(
            pattern=r"^(\d{4})(-)?(\d\d)(-)?(\d\d)(T)?(\d\d)(:)?(\d\d)(:)?(\d\d)(\.\d+)?(Z|([+-])(\d\d)(:)?(\d\d))?"
        )
    ]`

<a id="harlem.models.har.AfterRequest.lastAccess"></a>

#### lastAccess: `constr(
        pattern=r"^(\d{4})(-)?(\d\d)(-)?(\d\d)(T)?(\d\d)(:)?(\d\d)(:)?(\d\d)(\.\d+)?(Z|([+-])(\d\d)(:)?(\d\d))?"
    )`

<a id="harlem.models.har.AfterRequest.eTag"></a>

#### eTag: `str`

<a id="harlem.models.har.AfterRequest.hitCount"></a>

#### hitCount: `int`

<a id="harlem.models.har.AfterRequest.comment"></a>

#### comment: `Optional[str]`

<a id="harlem.models.har.Timings"></a>

## Timings

```python
class Timings(BaseModel)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\models\har.py#L102)

<a id="harlem.models.har.Timings.dns"></a>

#### dns: `Optional[float]`

<a id="harlem.models.har.Timings.connect"></a>

#### connect: `Optional[float]`

<a id="harlem.models.har.Timings.blocked"></a>

#### blocked: `Optional[float]`

<a id="harlem.models.har.Timings.send"></a>

#### send: `float`

<a id="harlem.models.har.Timings.wait"></a>

#### wait: `float`

<a id="harlem.models.har.Timings.receive"></a>

#### receive: `float`

<a id="harlem.models.har.Timings.ssl"></a>

#### ssl: `Optional[float]`

<a id="harlem.models.har.Timings.comment"></a>

#### comment: `Optional[str]`

<a id="harlem.models.har.Timings.total"></a>

#### total

```python
@property
def total() -> float
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\models\har.py#L113)

<a id="harlem.models.har.Page"></a>

## Page

```python
class Page(BaseModel)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\models\har.py#L122)

<a id="harlem.models.har.Page.startedDateTime"></a>

#### startedDateTime: `AwareDatetime`

<a id="harlem.models.har.Page.id"></a>

#### id: `str`

<a id="harlem.models.har.Page.title"></a>

#### title: `str`

<a id="harlem.models.har.Page.pageTimings"></a>

#### pageTimings: `PageTimings`

<a id="harlem.models.har.Page.comment"></a>

#### comment: `Optional[str]`

<a id="harlem.models.har.Request"></a>

## Request

```python
class Request(BaseModel)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\models\har.py#L130)

<a id="harlem.models.har.Request.method"></a>

#### method: `str`

<a id="harlem.models.har.Request.url"></a>

#### url: `AnyUrl`

<a id="harlem.models.har.Request.httpVersion"></a>

#### httpVersion: `str`

<a id="harlem.models.har.Request.cookies"></a>

#### cookies: `List[Cookie]`

<a id="harlem.models.har.Request.headers"></a>

#### headers: `List[Header]`

<a id="harlem.models.har.Request.queryString"></a>

#### queryString: `List[Query]`

<a id="harlem.models.har.Request.postData"></a>

#### postData: `Optional[PostData]`

<a id="harlem.models.har.Request.headersSize"></a>

#### headersSize: `int`

<a id="harlem.models.har.Request.bodySize"></a>

#### bodySize: `int`

<a id="harlem.models.har.Request.comment"></a>

#### comment: `Optional[str]`

<a id="harlem.models.har.Response"></a>

## Response

```python
class Response(BaseModel)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\models\har.py#L143)

<a id="harlem.models.har.Response.status"></a>

#### status: `int`

<a id="harlem.models.har.Response.statusText"></a>

#### statusText: `str`

<a id="harlem.models.har.Response.httpVersion"></a>

#### httpVersion: `str`

<a id="harlem.models.har.Response.cookies"></a>

#### cookies: `List[Cookie]`

<a id="harlem.models.har.Response.headers"></a>

#### headers: `List[Header]`

<a id="harlem.models.har.Response.content"></a>

#### content: `Content`

<a id="harlem.models.har.Response.redirectURL"></a>

#### redirectURL: `str`

<a id="harlem.models.har.Response.headersSize"></a>

#### headersSize: `int`

<a id="harlem.models.har.Response.bodySize"></a>

#### bodySize: `int`

<a id="harlem.models.har.Response.comment"></a>

#### comment: `Optional[str]`

<a id="harlem.models.har.Cache"></a>

## Cache

```python
class Cache(BaseModel)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\models\har.py#L156)

<a id="harlem.models.har.Cache.beforeRequest"></a>

#### beforeRequest: `Optional[BeforeRequest]`

<a id="harlem.models.har.Cache.afterRequest"></a>

#### afterRequest: `Optional[AfterRequest]`

<a id="harlem.models.har.Cache.comment"></a>

#### comment: `Optional[str]`

<a id="harlem.models.har.CallFrame"></a>

## CallFrame

```python
class CallFrame(BaseModel)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\models\har.py#L166)

<a id="harlem.models.har.CallFrame.functionName"></a>

#### functionName: `Optional[str]`

<a id="harlem.models.har.CallFrame.scriptId"></a>

#### scriptId: `Optional[str]`

<a id="harlem.models.har.CallFrame.url"></a>

#### url: `Optional[str]`

<a id="harlem.models.har.CallFrame.lineNumber"></a>

#### lineNumber: `Optional[int]`

<a id="harlem.models.har.CallFrame.columnNumber"></a>

#### columnNumber: `Optional[int]`

<a id="harlem.models.har.Stack"></a>

## Stack

```python
class Stack(BaseModel)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\models\har.py#L174)

<a id="harlem.models.har.Stack.callFrames"></a>

#### callFrames: `List[CallFrame]`

<a id="harlem.models.har.Initiator"></a>

## Initiator

```python
class Initiator(BaseModel)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\models\har.py#L178)

<a id="harlem.models.har.Initiator.type"></a>

#### type: `Literal["script", "other"]`

<a id="harlem.models.har.Initiator.stack"></a>

#### stack: `Optional[Stack]`

<a id="harlem.models.har.Entry"></a>

## Entry

```python
class Entry(BaseModel)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\models\har.py#L186)

<a id="harlem.models.har.Entry.pageref"></a>

#### pageref: `Optional[str]`

<a id="harlem.models.har.Entry.startedDateTime"></a>

#### startedDateTime: `AwareDatetime`

<a id="harlem.models.har.Entry.time"></a>

#### time: `float`

<a id="harlem.models.har.Entry.request"></a>

#### request: `Request`

<a id="harlem.models.har.Entry.response"></a>

#### response: `Response`

<a id="harlem.models.har.Entry.cache"></a>

#### cache: `Cache`

<a id="harlem.models.har.Entry.timings"></a>

#### timings: `Timings`

<a id="harlem.models.har.Entry.serverIPAddress"></a>

#### serverIPAddress: `Optional[Union[IPv4Address, IPv6Address]]`

<a id="harlem.models.har.Entry.connection"></a>

#### connection: `Optional[str]`

<a id="harlem.models.har.Entry.comment"></a>

#### comment: `Optional[str]`

<a id="harlem.models.har.Entry.initiator"></a>

#### initiator: `Optional[Initiator]`

<a id="harlem.models.har.Log"></a>

## Log

```python
class Log(BaseModel)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\models\har.py#L200)

<a id="harlem.models.har.Log.version"></a>

#### version: `str`

<a id="harlem.models.har.Log.creator"></a>

#### creator: `Creator`

<a id="harlem.models.har.Log.browser"></a>

#### browser: `Optional[Browser]`

<a id="harlem.models.har.Log.pages"></a>

#### pages: `Optional[List[Page]]`

<a id="harlem.models.har.Log.entries"></a>

#### entries: `List[Entry]`

<a id="harlem.models.har.Log.comment"></a>

#### comment: `Optional[str]`

<a id="harlem.models.har.Har"></a>

## Har

```python
class Har(BaseModel)
```

[[view_source]](https://github.com/WolfDWyc/harlem/blob/9f8f46048005256a8222ca316913bf605877223c/harlem\models\har.py#L209)

<a id="harlem.models.har.Har.log"></a>

#### log: `Log`

