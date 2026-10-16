from qdrant_client.http.models import PointGroup, GroupsResult

from Qdrant.QdrantDB import QdrantDB
from qdrant_client import QdrantClient, models
from qdrant_client.models import ScoredPoint

'''
This class caches any input put into the pyside6 search bar and sends
The request to the qdrant db
This class is based off of qdrants embedding example at <https://github.com/qdrant/qdrant-client>
'''
class Search:
    __request: str
    __database: QdrantClient

    def __init__(self, request: str, database: QdrantClient):
        self.set_request(request)
        self.set_database(database)

    def search(self) -> list[PointGroup] :
        database: QdrantClient = self.get_database()
        request: str = self.get_request()
        result: GroupsResult = database.query_points_groups(
            QdrantDB.COLLECTION_NAME,
            query=models.Document(text=request, model=QdrantDB.MODEL_NAME),
            #score_threshold=0.3,
            group_size=50,
            limit=10,
            group_by="source",
            with_payload=True,
            with_vectors=False,
        )
        return result.groups

    def get_request(self) -> str:
        return self.__request
    def set_request(self, request: str):
        self.__request = request

    def get_database(self) -> QdrantClient:
        return self.__database
    def set_database(self, database: QdrantClient):
        self.__database = database