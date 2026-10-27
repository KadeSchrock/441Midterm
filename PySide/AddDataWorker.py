from typing import Any

from PySide6 import QtCore
from qdrant_client import QdrantClient

from Qdrant.QdrantDB import QdrantDB
from Qdrant.WebScrape import WebScrape
from Qdrant.Embed import Embed

'''
This class scrapes and embeds each submitted URL off the GUI thread so the
interface stays responsive while the pages are fetched and chunked.
A URL that fails to scrape or embed is skipped and reported in the
failed list instead of aborting the whole batch.
'''
class AddDataWorker(QtCore.QThread):
    # Emitted when the batch finishes: the successful URLs, the failed URLs, and this worker
    data_added = QtCore.Signal(list, list, object)
    # Emitted when the whole batch raises an error: the error message and this worker
    add_failed = QtCore.Signal(str, object)

    __urls: list[str]
    __location: str

    def __init__(self, urls: list[str], location: str, parent: QtCore.QObject | None = None):
        super().__init__(parent)
        self.set_urls(urls)
        self.set_location(location)

    def run(self) -> None:
        try:
            # Create the client in this thread: a local Qdrant client
            # can only be used from the thread that created it
            database: QdrantClient = QdrantDB(location=self.get_location()).create_database()

            successful: list[str] = []
            failed: list[str] = []
            for url in self.get_urls():
                try:
                    payload: list[dict[str, Any]] = WebScrape(url=url).scrape()
                    if payload:
                        Embed(gpu=False, payload=payload, database=database).embed()
                        successful.append(url)
                    else:
                        failed.append(url)
                except Exception:
                    failed.append(url)

            self.data_added.emit(successful, failed, self)
        except Exception as error:
            self.add_failed.emit(str(error), self)

    def get_urls(self) -> list[str]:
        return self.__urls
    def set_urls(self, urls: list[str]) -> None:
        self.__urls = urls

    def get_location(self) -> str:
        return self.__location
    def set_location(self, location: str) -> None:
        self.__location = location
