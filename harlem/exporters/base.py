from abc import abstractmethod

from harlem.models.har import Page, Entry


class BaseHarExporter:
    def __init__(self):
        self._page_count = 0
        self.active = False

    def get_next_page_id(self) -> str:
        page_id = f"page_{self._page_count}"
        self._page_count += 1
        return page_id

    def add_page(self, page: Page):
        if not self.active:
            raise RuntimeError("Exporter cannot add pages when not active.")
        self._add_page(page)

    def add_entry(self, entry: Entry):
        if not self.active:
            raise RuntimeError("Exporter cannot add entries when not active.")
        self._add_entry(entry)

    @abstractmethod
    def _add_page(self, page: Page):
        raise NotImplementedError()

    @abstractmethod
    def _add_entry(self, entry: Entry):
        raise NotImplementedError()

    def start(self):
        self.active = True
        self._start()

    def stop(self):
        self.active = False
        self._stop()

    def _start(self):
        pass

    def _stop(self):
        pass
