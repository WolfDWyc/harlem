import time
from pathlib import Path
from threading import Thread
from typing import Union, cast, IO, Optional

from harlem.common import to_har_model
from harlem.exporters.base import HarExporter
from harlem.exporters.common import save_to_io
from harlem.models.har import Page, Entry


class LiveFileHarExporter(HarExporter):
    """
    An exporter that writes the HAR to a file in real-time.
    Allows manual updates to the file using the update_file method.
    """

    def __init__(
        self,
        path: Union[str, Path],
        indent: Optional[int] = None,
        interval_seconds: Optional[float] = None,
        hard_interval: bool = True,
        retention_seconds: Optional[float] = None,
        join_timeout: Optional[float] = 10,
    ):
        """
        :param path: The path to save the HAR to.
        :param indent: The number of spaces to use for indentation in the output JSON HAR file.
        If None, the file will be written without indentation.
        :param interval_seconds: Optional number of seconds to wait between writes to the file.
        If None, the file will be written every time a new page or entry is added.
        The file will also be written when the context manager exits.
        :param hard_interval: Whether to enforce the interval even if no new pages or entries are added.
        Uses a separate thread to write to the file at the specified interval.
        If this is set to False, the file may not be written every interval if no new pages or entries are added.
        Ignored if interval_seconds is None.
        :param retention_seconds: Optional number of seconds to keep old pages and entries.
        If None, old pages and entries will not be removed.
        Pages that are too old but still have entries will be kept.
        If no interval is set, rotation will only happen after a new page or entry is added.
        Rotation will also happen when the context manager exits.
        :param join_timeout: Optional number of seconds to wait for the background thread to join when stopping.
        If None, the thread will be joined without a timeout.
        Only used if interval_seconds is not None and hard_interval is True.
        """
        super().__init__()
        self._path = Path(path)
        self._indent = indent
        self._pages = []
        self._entries = []
        self._interval_seconds = interval_seconds
        self._hard_interval = hard_interval
        self._join_timeout = join_timeout
        self._retention_seconds = retention_seconds
        self._last_save = 0
        self._scheduler: Optional[Thread] = None

    def _remove_old(self):
        if self._retention_seconds is None:
            return
        now = time.time()

        new_entries = []
        used_page_ids = set()
        for entry in self._entries:
            if now - entry.startedDateTime.timestamp() > self._retention_seconds:
                continue

            new_entries.append(entry)
            used_page_ids.add(entry.pageref)

        self._entries = new_entries

        new_pages = []
        for page in self._pages:
            is_old = (
                time.time() - page.startedDateTime.timestamp() > self._retention_seconds
            )
            if page.id not in used_page_ids and is_old:
                continue

            new_pages.append(page)

        self._pages = new_pages

    def update_file(self):
        """
        Writes the current state of the exporter to the file.
        """
        self._remove_old()  # TODO: Should this be done before or checking the interval?

        with open(self._path, "w", encoding="utf-8") as file:
            save_to_io(
                to_har_model(self._pages, self._entries),
                cast(IO[str], file),
                self._indent,
            )

    def _update_if_needed(self):
        if self._interval_seconds is not None:
            if self._hard_interval:
                return
            now = time.time()
            if now - self._last_save < self._interval_seconds:
                return
            self._last_save = now

        self.update_file()

    def _scheduled_update(self):
        start_time = time.monotonic()
        while self.active:
            self.update_file()
            time.sleep(
                self._interval_seconds
                - ((time.monotonic() - start_time) % self._interval_seconds)
            )

    def _start(self):
        if self._interval_seconds is not None and self._hard_interval:
            self._scheduler = Thread(target=self._scheduled_update)
            self._scheduler.start()

    def _stop(self):
        try:
            if self._scheduler:
                self._scheduler.join(timeout=self._join_timeout)
            self.update_file()
        except Exception:  # noqa
            pass
        finally:
            self._scheduler = None

    def _add_page(self, page: Page):
        self._pages.append(page)
        self._update_if_needed()

    def _add_entry(self, entry: Entry):
        self._entries.append(entry)
        self._update_if_needed()
