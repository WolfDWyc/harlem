import base64
import inspect
from datetime import datetime, timezone
from http.cookies import SimpleCookie
from typing import Dict, List, Mapping

from harlem.models.har import Initiator, Stack, CallFrame, Content, Cookie


def to_name_value_pairs(mapping: Mapping) -> List[Dict]:
    return [{"name": k, "value": v} for k, v in mapping.items()]


def to_content(data: bytes, headers: Mapping) -> Content:
    return Content(
        size=len(data),
        mimeType=headers.get("Content-Type", "text/plain"),
        text=base64.b64encode(data).decode(),
        encoding="base64",
    )


def to_cookies(cookie: SimpleCookie) -> List[Cookie]:
    return [
        Cookie(
            name=c.key,
            value=c.value,
            path=c["path"] if c.get("path") else None,
            domain=c["domain"] if c.get("domain") else None,
            expires=(
                datetime.strptime(c["expires"], "%a, %d-%b-%Y %H:%M:%S GMT").replace(
                    tzinfo=timezone.utc
                )
                if c.get("expires")
                else None
            ),
            httpOnly=True if c.get("httponly") else False,
            secure=True if c.get("secure") else False,
        )
        for c in cookie.values()
    ]


def get_initiator(exclude: int = 0) -> Initiator:
    call_frames = []
    frame = inspect.currentframe()
    while frame:
        call_frames.append(
            CallFrame(
                lineNumber=frame.f_lineno,
                url=frame.f_code.co_filename,
                functionName=frame.f_code.co_name,
            )
        )
        frame = frame.f_back

    return Initiator(type="script", stack=Stack(callFrames=call_frames[exclude:]))
