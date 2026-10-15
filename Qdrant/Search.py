from QdrantDB import QdrantDB
from qdrant_client import QdrantClient, models

'''
This class caches any input put into the pyside6 search bar and sends
The request to the qdrant db
This class is based off of qdrants embedding example at <https://github.com/qdrant/qdrant-client>
'''
class Search:
    __request: str
    __database: QdrantClient

    def __init__(self, request: str):
        self.set_request(request)

    def search(self):
        database = self.get_database()
        request = self.get_request()
        result = database.query_points(
            QdrantDB.COLLECTION_NAME,
            query=models.Document(text=request, model=QdrantDB.MODEL_NAME)
        ).points
        return result

    def get_request(self) -> str:
        return self.__request
    def set_request(self, request: str):
        self.__request = request

    def get_database(self) -> QdrantClient:
        return self.__database
    def set_database(self, database: QdrantClient):
        self.__database = database