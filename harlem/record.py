import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Union, Optional, Literal

from harlem.exporters.concurrent_exporter import (
    BackgroundThreadHarExporter,
    BackgroundProcessHarExporter,
)
from harlem.exporters.io_exporter import FileHarExporter
from harlem.exporters.live_file_exporter import LiveFileHarExporter
from harlem.recorders import RequestsHarRecorder


@contextmanager
def record(
    path: Union[None, str, Path] = None,
    indent: Optional[int] = None,
    live: bool = False,
    interval_seconds: Optional[float] = None,
    retention_seconds: Optional[float] = None,
    in_background: Literal[None, "thread", "process"] = None,
):
    """
    A simple context-manager API for recording to HAR files.
    Provides an abstraction over various recorders and exporters.

    :param path: The path to save the HAR to.
    :param indent: The number of spaces to use for indentation in the output JSON HAR file.
    :param live: Whether to log to the file in real-time, or only when the context manager exits.
    If false, all interval and retention options are ignored.
    :param interval_seconds: Optional number of seconds to wait between writes to the file.
    If None, the file will be written every time a new page or entry is added.
    The file will also be written when the context manager exits.
    :param retention_seconds: Optional number of seconds to keep old pages and entries.
    If None, old pages and entries will not be removed.
    Pages that are too old but still have entries will be kept.
    If no interval is set, rotation will only happen after a new page or entry is added.
    Rotation will also happen when the context manager exits.
    :param in_background: Whether to export in the background.
    If "thread", exports in a separate thread. If "process", exports in a separate process.
    """
    if live:
        exporter = LiveFileHarExporter(
            path=path,
            indent=indent,
            interval_seconds=interval_seconds,
            hard_interval=True,
            retention_seconds=retention_seconds,
        )
    else:
        exporter = FileHarExporter(path=path, indent=indent)

    if in_background is not None and not live:
        logging.warning(
            "Harlem: You are using the in_background HAR recording option without live recording. "
            "Is this intended? This will only affect the exporting process, not the recording process."
        )

    if in_background == "thread":
        exporter = BackgroundThreadHarExporter(exporter)
    elif in_background == "process":
        exporter = BackgroundProcessHarExporter(exporter)
    elif in_background is not None:
        raise ValueError(
            f"Invalid value for in_background: {in_background}, expected None, 'thread', or 'process'."
        )

    # TODO: After more recorders are added, check which are installed and use them.

    with RequestsHarRecorder(exporter):
        yield
