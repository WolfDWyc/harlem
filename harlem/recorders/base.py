from abc import abstractmethod

from harlem.exporters.base import HarExporter


class HarRecorder:
    def __init__(self, exporter: HarExporter):
        self._exporter = exporter

    @abstractmethod
    def _start(self):
        raise NotImplementedError()

    @abstractmethod
    def _stop(self):
        raise NotImplementedError()

    def start(self):
        """
        Starts recording the network requests.
        Can be called multiple times to pause and resume recording.
        """
        self._start()
        self._exporter.start()

    def stop(self):
        """
        Stops recording the network requests.
        """
        try:
            self._stop()
        finally:
            self._exporter.stop()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
