from datetime import datetime, timezone
from functools import partial
from ipaddress import IPv6Address, IPv4Address
from itertools import chain
from socket import socket
from typing import Optional, Union

import requests
from yarl import URL

from harlem.exporters.base import BaseHarExporter
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
from harlem.recorders.base import BaseHarRecorder
from harlem.recorders.common import to_name_value_pairs, get_initiator, to_content


def _to_har_request(request: requests.PreparedRequest) -> Request:
    headers = to_name_value_pairs(dict(request.headers))
    cookies = to_name_value_pairs(dict(request._cookies))  # TODO: parse cookies
    url = request.url
    queryString = to_name_value_pairs(URL(url).query)
    if isinstance(request.body, str):
        body = request.body
        bodySize = len(request.body.encode())
    elif isinstance(request.body, bytes):
        body = request.body.decode()
        bodySize = len(request.body)
    else:
        bodySize = -1
        body = None

    return Request(
        method=request.method,
        url=request.url,
        httpVersion="HTTP/1.1",
        cookies=cookies,
        headers=headers,
        queryString=queryString,
        postData=PostData(
            mimeType=request.headers.get("Content-Type", "text/plain"), text=body
        ),
        bodySize=bodySize,
        headersSize=-1,
    )


def _to_har_response(response: requests.Response) -> Response:
    return Response(
        status=response.status_code,
        statusText=response.reason,
        httpVersion="HTTP/1.1",
        cookies=to_name_value_pairs(dict(response.cookies)),
        headers=to_name_value_pairs(dict(response.headers)),
        content=to_content(response.content, response.headers),
        redirectURL=response.headers.get("Location", ""),
        headersSize=-1,
        bodySize=len(response.content),
    )


def _get_socket(response: requests.Response) -> Optional[socket]:
    last_queue_item = response.raw._pool.pool.queue[-1]
    if last_queue_item is None:
        return None
    return last_queue_item.sock


def _to_har_server_ip(
    response: requests.Response,
) -> Optional[Union[IPv4Address, IPv6Address]]:
    sock = _get_socket(response)
    if sock is None:
        return None

    server_ip = sock.getpeername()[0]
    # Check if v4 or v6
    if ":" in server_ip:
        return IPv6Address(server_ip)
    else:
        return IPv4Address(server_ip)


def _to_har_connection(response: requests.Response) -> str:
    sock = _get_socket(response)
    if sock is None:
        return ""
    return str(sock.getsockname()[1])


class RequestsHarRecorder(BaseHarRecorder):
    """
    A recorder that listens for requests made by the requests library.
    """

    def __init__(self, exporter: BaseHarExporter):
        super().__init__(exporter)
        self._real_request = None
        self._active = False

    def _start(self):
        if self._active:
            return
        self._active = True
        self._real_request = requests.sessions.Session.request

        def wrapped_request(session, method, url, **kwargs):
            page_id = self._add_page(method, url)
            self._add_hook(kwargs, page_id)

            response = self._real_request(session, method, url, **kwargs)
            return response

        requests.sessions.Session.request = wrapped_request

    def _add_hook(self, kwargs: dict, page_id: str):
        hook = partial(self._add_entry, page=page_id)

        if "hooks" in kwargs:
            if "response" in kwargs["hooks"]:
                kwargs["hooks"]["response"] = chain(kwargs["hooks"]["response"], [hook])
            else:
                kwargs["hooks"]["response"] = [hook]
        else:
            kwargs["hooks"] = {"response": [hook]}

    def _add_entry(
        self, response: requests.Response, page: Optional[str], *args, **kwargs
    ):
        elapsed = response.elapsed
        start_time = datetime.now(timezone.utc) - elapsed
        entry = Entry(
            pageref=page,
            startedDateTime=start_time,
            time=elapsed.total_seconds() * 1000,
            request=_to_har_request(response.request),
            response=_to_har_response(response),
            cache=Cache(),
            timings=Timings(wait=-1, receive=-1, send=-1),
            serverIPAddress=_to_har_server_ip(response),
            connection=_to_har_connection(response),
            initiator=get_initiator(
                exclude=6  # Exclude the stack frames from the recorder
            ),
        )
        self._exporter.add_entry(entry)

    def _add_page(self, method: str, url: str) -> str:
        page_id = self._exporter.get_next_page_id()
        self._exporter.add_page(
            Page(
                startedDateTime=datetime.now(timezone.utc),
                id=page_id,
                title=f"requests {method} {url}",
                pageTimings=PageTimings(),
            )
        )
        return page_id

    def _stop(self):
        if self._active:
            requests.sessions.Session.request = self._real_request
            self._active = False
