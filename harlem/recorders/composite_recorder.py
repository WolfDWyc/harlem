from typing import List, Callable

from harlem.exporters.base import HarExporter
from harlem.recorders.base import HarRecorder


class CompositeHarRecorder(HarRecorder):
    """
    A recorder that listens for requests made by multiple libraries.
    """

    def __init__(
        self,
        recorders: List[Callable[[HarExporter], HarRecorder]],
        exporter: HarExporter,
    ):
        super().__init__(exporter)
        self._recorders = [recorder(exporter) for recorder in recorders]

    def _start(self):
        for recorder in self._recorders:
            recorder._start()

    def _stop(self):
        for recorder in self._recorders:
            recorder._stop()
