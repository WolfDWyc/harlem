from typing import List, Callable

from harlem.exporters.base import BaseHarExporter
from harlem.recorders.base import BaseHarRecorder


class CompositeHarRecorder(BaseHarRecorder):
    """
    A recorder that listens for requests made by multiple libraries.
    """

    def __init__(
        self,
        recorders: List[Callable[[BaseHarExporter], BaseHarRecorder]],
        exporter: BaseHarExporter,
    ):
        super().__init__(exporter)
        self._recorders = [recorder(exporter) for recorder in recorders]

    def _start(self):
        for recorder in self._recorders:
            recorder._start()

    def _stop(self):
        for recorder in self._recorders:
            recorder._stop()
