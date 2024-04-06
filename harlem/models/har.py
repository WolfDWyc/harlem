from __future__ import annotations

from ipaddress import IPv4Address, IPv6Address
from typing import List, Optional, Union, Literal

from pydantic import AnyUrl, AwareDatetime, BaseModel, constr, Field


class Creator(BaseModel):
    name: str
    version: str
    comment: Optional[str] = None


class Browser(BaseModel):
    name: str
    version: str
    comment: Optional[str] = None


class PageTimings(BaseModel):
    onContentLoad: Optional[float] = None
    onLoad: Optional[float] = None
    comment: Optional[str] = None


class Cookie(BaseModel):
    name: str
    value: str
    path: Optional[str] = None
    domain: Optional[str] = None
    expires: Optional[AwareDatetime] = None
    httpOnly: Optional[bool] = None
    secure: Optional[bool] = None
    comment: Optional[str] = None


class Header(BaseModel):
    name: str
    value: str
    comment: Optional[str] = None


class Query(BaseModel):
    name: str
    value: str
    comment: Optional[str] = None


class Params(BaseModel):
    name: str
    value: Optional[str] = None
    fileName: Optional[str] = None
    contentType: Optional[str] = None
    comment: Optional[str] = None


class PostData(BaseModel):
    mimeType: str
    text: Optional[str] = None
    params: Optional[Union[List, Params]] = None
    comment: Optional[str] = None


class Content(BaseModel):
    size: int
    compression: Optional[int] = None
    mimeType: str
    text: Optional[str] = None
    encoding: Optional[str] = None
    comment: Optional[str] = None


class BeforeRequest(BaseModel):
    expires: Optional[
        constr(
            pattern=r"^(\d{4})(-)?(\d\d)(-)?(\d\d)(T)?(\d\d)(:)?(\d\d)(:)?(\d\d)(\.\d+)?(Z|([+-])(\d\d)(:)?(\d\d))?"
        )
    ] = None
    lastAccess: constr(
        pattern=r"^(\d{4})(-)?(\d\d)(-)?(\d\d)(T)?(\d\d)(:)?(\d\d)(:)?(\d\d)(\.\d+)?(Z|([+-])(\d\d)(:)?(\d\d))?"
    )
    eTag: str
    hitCount: int
    comment: Optional[str] = None


class AfterRequest(BaseModel):
    expires: Optional[
        constr(
            pattern=r"^(\d{4})(-)?(\d\d)(-)?(\d\d)(T)?(\d\d)(:)?(\d\d)(:)?(\d\d)(\.\d+)?(Z|([+-])(\d\d)(:)?(\d\d))?"
        )
    ] = None
    lastAccess: constr(
        pattern=r"^(\d{4})(-)?(\d\d)(-)?(\d\d)(T)?(\d\d)(:)?(\d\d)(:)?(\d\d)(\.\d+)?(Z|([+-])(\d\d)(:)?(\d\d))?"
    )
    eTag: str
    hitCount: int
    comment: Optional[str] = None


class Timings(BaseModel):
    dns: Optional[float] = None
    connect: Optional[float] = None
    blocked: Optional[float] = None
    send: float
    wait: float
    receive: float
    ssl: Optional[float] = None
    comment: Optional[str] = None


class Page(BaseModel):
    startedDateTime: AwareDatetime
    id: str
    title: str
    pageTimings: PageTimings
    comment: Optional[str] = None


class Request(BaseModel):
    method: str
    url: AnyUrl
    httpVersion: str
    cookies: List[Cookie]
    headers: List[Header]
    queryString: List[Query]
    postData: Optional[PostData] = None
    headersSize: int
    bodySize: int
    comment: Optional[str] = None


class Response(BaseModel):
    status: int
    statusText: str
    httpVersion: str
    cookies: List[Cookie]
    headers: List[Header]
    content: Content
    redirectURL: str
    headersSize: int
    bodySize: int
    comment: Optional[str] = None


class Cache(BaseModel):
    beforeRequest: Optional[BeforeRequest] = None
    afterRequest: Optional[AfterRequest] = None
    comment: Optional[str] = None


class CallFrame(BaseModel):
    functionName: Optional[str] = None
    scriptId: Optional[str] = None
    url: Optional[str] = None
    lineNumber: Optional[int] = None
    columnNumber: Optional[int] = None


class Stack(BaseModel):
    callFrames: List[CallFrame]


# Note: This part of the schema is based on sample data from Chrome and may not be accurate.
class Initiator(BaseModel):
    type: Literal["script", "other"]
    stack: Optional[Stack] = None


class Entry(BaseModel):
    pageref: Optional[str] = None
    startedDateTime: AwareDatetime
    time: float
    request: Request
    response: Response
    cache: Cache
    timings: Timings
    serverIPAddress: Optional[Union[IPv4Address, IPv6Address]] = None
    connection: Optional[str] = None
    comment: Optional[str] = None
    initiator: Optional[Initiator] = Field(None, serialization_alias="_initiator")


class Log(BaseModel):
    version: str
    creator: Creator
    browser: Optional[Browser] = None
    pages: Optional[List[Page]] = None
    entries: List[Entry]
    comment: Optional[str] = None


class Har(BaseModel):
    log: Log
