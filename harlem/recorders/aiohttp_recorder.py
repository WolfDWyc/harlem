import time
import time
import warnings
from contextlib import contextmanager
from datetime import datetime, timezone
from http.cookies import SimpleCookie
from ipaddress import IPv6Address, IPv4Address
from types import SimpleNamespace
from typing import Optional, Union, List, Tuple, NamedTuple

import aiohttp
from aiohttp import (
    TraceRequestStartParams,
    TraceRequestChunkSentParams,
    TraceResponseChunkReceivedParams,
)
from aiohttp.tracing import (
    TraceRequestHeadersSentParams,
    TraceRequestRedirectParams,
    TraceConnectionQueuedStartParams,
    TraceConnectionQueuedEndParams,
    TraceConnectionCreateStartParams,
    TraceConnectionCreateEndParams,
    TraceConnectionReuseconnParams,
    TraceDnsResolveHostStartParams,
    TraceDnsResolveHostEndParams,
    TraceRequestEndParams,
)
from aiohttp.typedefs import StrOrURL

from harlem.exporters.base import HarExporter
from harlem.models.har import (
    Entry,
    Request,
    PostData,
    Response,
    Timings,
    Cache,
    Page,
    PageTimings,
)
from harlem.recorders.base import HarRecorder
from harlem.recorders.common import (
    to_name_value_pairs,
    get_initiator,
    to_content,
    to_cookies,
)

EventParams = Union[
    TraceRequestStartParams,
    TraceRequestEndParams,
    TraceRequestChunkSentParams,
    TraceRequestHeadersSentParams,
    TraceRequestRedirectParams,
    TraceResponseChunkReceivedParams,
    TraceConnectionQueuedStartParams,
    TraceConnectionQueuedEndParams,
    TraceConnectionCreateStartParams,
    TraceConnectionCreateEndParams,
    TraceConnectionReuseconnParams,
    TraceDnsResolveHostStartParams,
    TraceDnsResolveHostEndParams,
]

Event = NamedTuple("Event", [("params", EventParams), ("timestamp", float)])


def _to_har_request(events: List[Event]) -> Request:
    request_info = events[-1].params.response.request_info
    headers = to_name_value_pairs(request_info.headers)
    cookie = SimpleCookie()
    cookie.load(request_info.headers.get("Cookie", ""))
    cookies = to_cookies(cookie)
    queryString = to_name_value_pairs(request_info.url.query)

    body = b""
    for event in events:
        if isinstance(event.params, TraceRequestChunkSentParams):
            body += event.params.chunk
    bodySize = len(body) if body else -1

    return Request(
        method=request_info.method,
        url=str(request_info.real_url),
        httpVersion="HTTP/1.1",
        cookies=cookies,
        headers=headers,
        queryString=queryString,
        postData=PostData(
            mimeType=request_info.headers.get("Content-Type", "text/plain"), text=body
        ),
        bodySize=bodySize,
        headersSize=-1,
    )


async def _to_har_response(response: aiohttp.ClientResponse) -> Response:
    data = await response.content.read()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        response.content.unread_data(data)

    return Response(
        status=response.status,
        statusText=response.reason,
        httpVersion="HTTP/1.1",
        cookies=to_cookies(response.cookies),
        headers=to_name_value_pairs(response.headers),
        content=to_content(data, response.headers),
        redirectURL=response.headers.get("Location", ""),
        headersSize=-1,
        bodySize=len(data),
    )


def _to_har_server_ip(
    peername: Tuple[str, int]
) -> Optional[Union[IPv4Address, IPv6Address]]:
    server_ip = peername[0]
    # Check if v4 or v6
    if ":" in server_ip:
        return IPv6Address(server_ip)
    else:
        return IPv4Address(server_ip)


def _to_har_connection(sockname: Tuple[str, int]) -> str:
    return str(sockname[1])


def _to_har_timings(events: List[Event]) -> Timings:
    start_time = events[0].timestamp * 1000
    blocked = -1
    dns_start = None
    dns = -1
    connect_start = None
    connect = -1
    send_start = start_time
    send = -1
    end_send = start_time
    wait = -1
    receive = -1
    for event in events:
        if isinstance(event.params, TraceConnectionQueuedStartParams):
            blocked = event.timestamp * 1000 - start_time
        if isinstance(event.params, TraceDnsResolveHostStartParams):
            dns_start = event.timestamp * 1000
        if isinstance(event.params, TraceDnsResolveHostEndParams):
            dns = event.timestamp * 1000 - dns_start
        if isinstance(event.params, TraceConnectionCreateStartParams):
            connect_start = event.timestamp * 1000
        if isinstance(event.params, TraceConnectionCreateEndParams):
            connect = event.timestamp * 1000 - connect_start
        if isinstance(
            event.params, (TraceRequestHeadersSentParams, TraceRequestChunkSentParams)
        ):
            if dns != -1:
                send_start = dns_start + dns
            if connect != -1:
                send_start = connect_start + connect
            send = event.timestamp * 1000 - send_start
        if isinstance(
            event.params, (TraceRequestEndParams, TraceRequestRedirectParams)
        ):
            end_send = send_start + send
            wait = event.timestamp * 1000 - end_send
            receive = wait
        if isinstance(event.params, TraceResponseChunkReceivedParams):
            receive = event.timestamp * 1000 - end_send

    return Timings(
        blocked=blocked,
        dns=dns,
        connect=connect,
        send=send,
        wait=wait,
        receive=receive,
    )


class _HarlemTraceConfig(aiohttp.TraceConfig):
    pass


class AiohttpHarRecorder(HarRecorder):
    """
    A recorder that listens for requests made by the requests library.
    """

    def __init__(self, exporter: HarExporter):
        super().__init__(exporter)
        self._real_request = None
        self._real_release_connection = None
        self._active = False

    def _start(self):
        if self._active:
            return
        self._active = True
        self._real_request = aiohttp.ClientSession._request

        async def wrapped_request(
            session: aiohttp.ClientSession, method, str_or_url, **kwargs
        ):
            page_id = self._add_page(method, str_or_url)
            self._ensure_hook(session, kwargs, page_id)

            with self._save_connection_details(session):
                return await self._real_request(session, method, str_or_url, **kwargs)

        aiohttp.ClientSession._request = wrapped_request

    def _ensure_hook(self, session: aiohttp.ClientSession, kwargs: dict, page_id: str):
        trace_request_ctx = kwargs.get("trace_request_ctx", SimpleNamespace())
        trace_request_ctx.page_id = page_id
        trace_request_ctx.events = []
        kwargs["trace_request_ctx"] = trace_request_ctx

        for trace_config in session._trace_configs:
            if isinstance(trace_config, _HarlemTraceConfig):
                return

        trace_config = _HarlemTraceConfig()

        trace_config.on_request_start.append(self._on_event)
        trace_config.on_request_chunk_sent.append(self._on_event)
        trace_config.on_request_headers_sent.append(self._on_event)
        trace_config.on_request_redirect.append(self._on_event)
        trace_config.on_response_chunk_received.append(self._on_event)
        trace_config.on_request_end.append(self._on_event)
        trace_config.on_connection_queued_start.append(self._on_event)
        trace_config.on_connection_queued_end.append(self._on_event)
        trace_config.on_connection_create_start.append(self._on_event)
        trace_config.on_connection_create_end.append(self._on_event)
        trace_config.on_connection_reuseconn.append(self._on_event)
        trace_config.on_dns_resolvehost_start.append(self._on_event)
        trace_config.on_dns_resolvehost_end.append(self._on_event)

        trace_config.freeze()

        session._trace_configs.append(trace_config)


    @contextmanager
    def _save_connection_details(self, session: aiohttp.ClientSession):
        real_response_class = session._response_class

        class WrappedClientResponse(real_response_class):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._sockname = None
                self._peername = None

            def __setattr__(self, key, value):
                if key == "_connection" and value:
                    if not self._sockname:
                        if value.transport:
                            self._sockname = value.transport.get_extra_info("sockname")
                    if not self._peername:
                        if value.transport:
                            self._peername = value.transport.get_extra_info("peername")
                super().__setattr__(key, value)

        session._response_class = WrappedClientResponse
        yield
        session._response_class = real_response_class

    async def _on_event(self, _session, trace_config_ctx, params):
        event = Event(params=params, timestamp=time.time())
        print("Event", type(params), event.timestamp)
        trace_config_ctx.trace_request_ctx.events.append(event)
        if isinstance(params, TraceRequestRedirectParams) or isinstance(
            params, TraceRequestEndParams
        ):
            await self._add_entry(
                trace_config_ctx.trace_request_ctx.events,
                trace_config_ctx.trace_request_ctx.page_id,
            )
            self.events = [event]

    async def _add_entry(self, events: List[Event], page: str):
        start_time = datetime.fromtimestamp(events[0].timestamp, timezone.utc)
        timings = _to_har_timings(events)

        response = events[-1].params.response

        entry = Entry(
            pageref=page,
            startedDateTime=start_time,
            time=timings.total,
            request=_to_har_request(events),
            response=await _to_har_response(response),
            cache=Cache(),
            timings=timings,
            serverIPAddress=_to_har_server_ip(response._peername),
            connection=_to_har_connection(response._sockname),
            initiator=get_initiator(
                exclude=7  # Exclude the stack frames from the recorder # TODO: Check if this is correct
            ),
        )

        self._exporter.add_entry(entry)

    def _add_page(self, method: str, str_or_url: StrOrURL) -> str:
        page_id = self._exporter.get_next_page_id()
        self._exporter.add_page(
            Page(
                startedDateTime=datetime.now(timezone.utc),
                id=page_id,
                title=f"aiohttp {method} {str(str_or_url)}",
                pageTimings=PageTimings(),
            )
        )
        return page_id

    def _stop(self):
        if self._active:
            aiohttp.ClientSession._request = self._real_request
            self._active = False
