from concurrent.futures import Executor, ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import Queue, Process
from typing import Literal

from harlem.exporters.base import BaseHarExporter
from harlem.models.har import Page, Entry


class ExecutorHarExporter(BaseHarExporter):
    """
    An exporter that delegates to another exporter and uses an executor to run the operations concurrently.
    Please note that the exporter should be thread-safe (or process-safe, if using a ProcessPoolExecutor).
    """

    def __init__(self, exporter: BaseHarExporter, executor: Executor):
        """
        :param exporter: The exporter to delegate to.
        :param executor: The executor to run the operations concurrently.
        """
        super().__init__()
        self._exporter = exporter
        self._executor = executor

    def _add_page(self, page: Page):
        self._executor.submit(self._exporter._add_page, page)

    def _add_entry(self, entry: Entry):
        self._executor.submit(self._exporter._add_entry, entry)

    def _start(self):
        self._exporter._start()

    def _stop(self):
        self._exporter._stop()


class BackgroundThreadHarExporter(BaseHarExporter):
    """
    An exporter that delegates to another exporter and executes it in a separate thread in the background.
    Uses a ThreadPoolExecutor with a single worker to work around non-thread-safe exporters.
    """

    def __init__(self, exporter: BaseHarExporter):
        """
        :param exporter: The exporter to delegate to.
        """
        super().__init__()
        self._exporter = exporter
        self._executor = None

    def _add_page(self, page: Page):
        self._executor.submit(self._exporter._add_page, page)

    def _add_entry(self, entry: Entry):
        self._executor.submit(self._exporter._add_entry, entry)

    def _start(self):
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._exporter._start()

    def _stop(self):
        self._exporter._stop()
        try:
            self._executor.shutdown()
        except Exception:  # noqa
            pass
        finally:
            self._executor = None


class BackgroundProcessHarExporter(BaseHarExporter):
    """
    An exporter that delegates to another exporter and executes it in a separate process in the background.
    """

    def __init__(self, exporter: BaseHarExporter):
        """
        :param exporter: The exporter to delegate to.
        """
        super().__init__()
        self._exporter = exporter
        self._queue = None
        self._process = None

    def _worker(self):
        self._exporter._start()
        while True:
            item = self._queue.get()
            if item is None:
                self._exporter._stop()
                return
            if item[0] == "page":
                self._exporter._add_page(item[1])
            elif item[0] == "entry":
                self._exporter._add_entry(item[1])

    def _add_page(self, page: Page):
        self._queue.put(("page", page))

    def _add_entry(self, entry: Entry):
        self._queue.put(("entry", entry))

    def _start(self):
        self._queue = Queue()
        self._process = Process(target=self._worker)
        self._process.start()

    def _stop(self):
        try:
            self._queue.put(None)
            self._process.join(timeout=10)
        except Exception:  # noqa
            pass
        finally:
            try:
                self._process.kill()
            except Exception:  # noqa
                pass
            finally:
                self._queue = None
                self._process = None
