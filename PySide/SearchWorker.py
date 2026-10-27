from typing import Any
from urllib.parse import urlparse

from PySide6 import QtCore
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointGroup

from Qdrant.QdrantDB import QdrantDB
from Qdrant.Search import Search

'''
This class runs a Qdrant search off the GUI thread so the loading
indicator can animate while the query is being embedded.
'''
class SearchWorker(QtCore.QThread):
    # Emitted when the search finishes: the list of result dicts and this worker
    results_ready = QtCore.Signal(list, object)
    # Emitted when the search raises an error: the error message and this worker
    search_failed = QtCore.Signal(str, object)

    __request: str
    __location: str

    def __init__(self, request: str, location: str, parent: QtCore.QObject | None = None):
        super().__init__(parent)
        self.set_request(request)
        self.set_location(location)

    def run(self) -> None:
        try:
            # Create the client in this thread: a local Qdrant client
            # can only be used from the thread that created it
            database: QdrantClient = QdrantDB(location=self.get_location()).create_database()
            groups: list[PointGroup] = Search(request=self.get_request(), database=database).search()

            results: list[dict[str, Any]] = [
                {
                    "title": urlparse(group.id).netloc or group.id,
                    "url": group.id,
                    "snippet": group.hits[0].payload["document"],
                    "score": group.hits[0].score,
                }
                for group in groups
            ]
            self.results_ready.emit(results, self)
        except Exception as error:
            self.search_failed.emit(str(error), self)

    def get_request(self) -> str:
        return self.__request
    def set_request(self, request: str) -> None:
        self.__request = request

    def get_location(self) -> str:
        return self.__location
    def set_location(self, location: str) -> None:
        self.__location = location
