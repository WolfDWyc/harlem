from pathlib import Path
from typing import Union, IO, Optional

from harlem.common import to_har_model
from harlem.exporters.base import HarExporter
from harlem.exporters.common import save_to_io
from harlem.models.har import Page, Entry


class IoHarExporter(HarExporter):
    """
    An exporter that writes the HAR to an IO object.
    Allows manual updates to the file using the update_file method.
    """

    def __init__(
        self,
        destination: Union[IO[str], str, Path] = None,
        indent: Optional[int] = None,
    ):
        """
        :param destination: The destination to save the HAR to. Can be a file path, a file object, or a string.
        If a string is provided, it will be treated as a file path.
        File objects must be opened in text mode, and preferably with UTF-8 encoding.
        :param indent: The number of spaces to use for indentation in the output JSON HAR file.
        """
        super().__init__()
        self._pages = []
        self._entries = []
        self._destination = destination
        self._indent = indent

    def _add_page(self, page: Page):
        self._pages.append(page)

    def _add_entry(self, entry: Entry):
        self._entries.append(entry)

    def _stop(self):
        self.update_file()

    def update_file(self):
        """
        Save the HAR to the destination.
        """
        if isinstance(self._destination, (str, Path)):
            with open(self._destination, "w", encoding="utf-8") as f:
                save_to_io(to_har_model(self._pages, self._entries), f, self._indent)
        else:
            save_to_io(
                to_har_model(self._pages, self._entries),
                self._destination,
                self._indent,
            )


class FileHarExporter(IoHarExporter):
    """
    An exporter that writes the HAR to a file.
    Syntax sugar for IoHarExporter.
    """

    def __init__(self, path: Union[str, Path], indent: Optional[int] = None):
        super().__init__(destination=path, indent=indent)
