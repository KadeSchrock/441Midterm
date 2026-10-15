import os
from qdrant_client import QdrantClient, models

'''
This class contains all responsible code for the creation of a new Qdrant database
'''
class QdrantDB:
    # Hardcoded values for making a single collection and embedding models to keep it simple for now
    COLLECTION_NAME = "Qdrant_Collection"
    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

    __location: str

    def __init__(self, location: str):
        self.set_location(location)

    def create_database(self) -> QdrantClient:
        # Simple check to make sure we only create one DB the first time the app is loaded
        # If it already exists we simply return it
        if os.path.exists(self.get_location()):
            print(f"Database already exists at {self.get_location()}")
            return QdrantClient(path=self.get_location())

        database = QdrantClient(path=self.get_location())
        database.create_collection(
            QdrantDB.COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=database.get_embedding_size(QdrantDB.MODEL_NAME), distance=models.Distance.COSINE)
        )
        return database

    def get_location(self) -> str:
        return self.__location
    def set_location(self, location: str) -> None:
        self.__location = location