from typing import List

from harlem.exporters.base import BaseHarExporter
from harlem.models.har import Entry, Page


class CompositeHarExporter(BaseHarExporter):
    """
    An exporter that delegates to multiple exporters.
    """

    def __init__(self, exporters: List[BaseHarExporter]):
        """
        :param exporters: List of exporters to delegate to.
        """
        super().__init__()
        self._exporters = exporters

    def _start(self):
        for exporter in self._exporters:
            exporter.start()

    def _stop(self):
        for exporter in self._exporters:
            exporter.stop()

    def _add_page(self, page: Page):
        for exporter in self._exporters:
            exporter._add_page(page)

    def _add_entry(self, entry: Entry):
        for exporter in self._exporters:
            exporter._add_entry(entry)
