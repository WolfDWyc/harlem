from harlem.common import to_har_model
from harlem.exporters.base import HarExporter
from harlem.models.har import Page, Entry, Har


class ModelHarExporter(HarExporter):
    """
    An exporter that builds a HAR model from pages and entries.
    """

    def __init__(self):
        super().__init__()
        self._pages = []
        self._entries = []

    def _add_page(self, page: Page):
        self._pages.append(page)

    def _add_entry(self, entry: Entry):
        self._entries.append(entry)

    def to_model(self) -> Har:
        """
        Builds and returns the HAR model.
        :return: The HAR model.
        """
        return to_har_model(self._pages, self._entries)
