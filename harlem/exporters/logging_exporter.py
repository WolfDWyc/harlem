import logging
from logging import Logger

from harlem.exporters.base import HarExporter
from harlem.exporters.common import dump_model_to_dict
from harlem.models.har import Page, Entry


class LoggingHarExporter(HarExporter):
    """
    An exporter that logs the HAR to a logging.logger.
    New page and entry objects are dumped to the log's extra field as dictionaries
    in the "har_page" and "har_entry" keys.
    """

    def __init__(
        self,
        logger: Logger,
        log_level: int = logging.DEBUG,
        new_page_message: str = "New HAR page added",
        new_entry_message: str = "New HAR entry added",
    ):
        """
        :param logger: The logger to log to.
        :param log_level: The log level to log at.
        :param new_page_message: The message to log when a new page is added.
        :param new_entry_message: The message to log when a new entry is added.
        """
        super().__init__()
        self._logger = logger
        self._log_level = log_level
        self._new_page_message = new_page_message
        self._new_entry_message = new_entry_message

    def _add_page(self, page: Page):
        self._logger.log(
            self._log_level,
            self._new_page_message,
            extra={"har_page": dump_model_to_dict(page)},
        )

    def _add_entry(self, entry: Entry):
        self._logger.log(
            self._log_level,
            self._new_entry_message,
            extra={"har_entry": dump_model_to_dict(entry)},
        )
