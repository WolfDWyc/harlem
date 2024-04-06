import inspect
from typing import Dict, List

from harlem.models.har import Initiator, Stack, CallFrame


def _to_name_value_pairs(d: Dict) -> List[Dict]:
    return [{"name": k, "value": v} for k, v in d.items()]


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
