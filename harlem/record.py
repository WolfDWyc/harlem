import logging
import warnings
from contextlib import contextmanager
from pathlib import Path
from typing import Union, Optional, Literal

from harlem.exporters import LoggingHarExporter, BaseHarExporter
from harlem.exporters.concurrent_exporter import (
    BackgroundThreadHarExporter,
    BackgroundProcessHarExporter,
)
from harlem.exporters.io_exporter import FileHarExporter
from harlem.exporters.live_file_exporter import LiveFileHarExporter
from harlem.recorders import RequestsHarRecorder, AiohttpHarRecorder
from harlem.recorders.composite_recorder import CompositeHarRecorder


@contextmanager
def _record(
    exporter: BaseHarExporter,
    in_background: Literal[None, "thread", "process"],
):
    if in_background == "thread":
        exporter = BackgroundThreadHarExporter(exporter)
    elif in_background == "process":
        exporter = BackgroundProcessHarExporter(exporter)
    elif in_background is not None:
        raise ValueError(
            f"Invalid value for in_background: {in_background}, expected None, 'thread', or 'process'."
        )

    # TODO: After more recorders are added, check which are installed and use them.

    with CompositeHarRecorder([RequestsHarRecorder, AiohttpHarRecorder], exporter):
        yield


@contextmanager
def record_to_file(
    path: Union[None, str, Path] = None,
    indent: Optional[int] = None,
    live: bool = False,
    interval_seconds: Optional[float] = None,
    retention_seconds: Optional[float] = None,
    in_background: Literal[None, "thread", "process"] = None,
):
    """
    A simple context-manager API for recording to HAR files.

    :param path: The path to save the HAR to.
    :param indent: The number of spaces to use for indentation in the output JSON HAR file.
    :param live: Whether to log to the file in real-time, or only when the context manager exits.
    :param interval_seconds: Write to the file on an interval instead of only when the context manager exits.
    The file will also be written when the context manager exits.
    :param retention_seconds: Optional number of seconds to keep old pages and entries.
    If None, old pages and entries will not be removed.
    Pages that are too old but still have entries will be kept.
    If no interval is set, rotation will only happen after a new page or entry is added.
    Rotation will also happen when the context manager exits.
    :param in_background: Whether to export in the background.
    If "thread", exports in a separate thread. If "process", exports in a separate process.
    """
    if any((live, interval_seconds, retention_seconds)):
        live = True
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
        warnings.warn(
            "Harlem: You are using the in_background HAR recording option without live recording. "
            "Is this intended? This will only affect the exporting process, not the recording process."
        )

    with _record(exporter, in_background):
        yield


@contextmanager
def record_to_logger(
    logger: Optional[logging.Logger] = None,
    level: Union[int, str] = logging.DEBUG,
    new_page_message: str = "New page added",
    new_entry_message: str = "New entry added",
    in_background: Literal[None, "thread", "process"] = None,
):
    """
    A simple context-manager API for recording new pages and entries to a logger.
    New page and entry objects are dumped to the log's extra field as dictionaries.

    :param logger: The logger to log to.
    If not provided, the default __name__ logger will be used.
    :param level: The log level to log at.
    :param new_page_message: The message to log when a new page is added.
    :param new_entry_message: The message to log when a new entry is added.
    :param in_background: Whether to export in the background.
    If "thread", exports in a separate thread. If "process", exports in a separate process.
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    exporter = LoggingHarExporter(
        logger=logger,
        log_level=level,
        new_page_message=new_page_message,
        new_entry_message=new_entry_message,
    )

    with _record(exporter, in_background):
        yield
