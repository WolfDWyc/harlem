from concurrent.futures import Executor, ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import Queue, Process
from typing import Literal, Optional

from harlem.exporters.base import HarExporter
from harlem.models.har import Page, Entry


class ExecutorHarExporter(HarExporter):
    """
    An exporter that delegates to another exporter and uses an executor to run the operations concurrently.
    Please note that the inner exporter should be thread-safe (or process-safe, if using a ProcessPoolExecutor),
    or things might not work properly.
    """

    def __init__(self, exporter: HarExporter, executor: Executor):
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


class BackgroundThreadHarExporter(HarExporter):
    """
    An exporter that delegates to another exporter and executes it in a separate thread in the background.
    Uses a ThreadPoolExecutor with a single worker to work around non-thread-safe exporters.
    """

    def __init__(self, exporter: HarExporter):
        """
        :param exporter: The exporter to delegate to.
        """
        super().__init__()
        self._exporter = exporter
        self._executor: Optional[ThreadPoolExecutor] = None

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


class BackgroundProcessHarExporter(HarExporter):
    """
    An exporter that delegates to another exporter and executes it in a separate process in the background.
    """

    def __init__(self, exporter: HarExporter, join_timeout: Optional[float] = 10):
        """
        :param exporter: The exporter to delegate to.
        :param join_timeout: Optional number of seconds to wait for the background process to join when stopping.
        If None, the process will be joined without a timeout.
        """
        super().__init__()
        self._exporter = exporter
        self._queue: Optional[Queue] = None
        self._process: Optional[Process] = None
        self._join_timeout = join_timeout

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
            self._process.join(timeout=self._join_timeout)
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
