import os
from qdrant_client import QdrantClient

'''
This class contains all responsible code for the creation of a new Qdrant database
'''
class QdrantDB:
    __location: str

    def __init__(self, location: str):
        self.set_location(location)

    def create(self) -> QdrantClient:
        # Simple check to make sure we only create one DB the first time the app is loaded
        # If it already exists we simply return it
        if os.path.exists(self.get_location()):
            print(f"Database already exists at {self.get_location()}")
            return QdrantClient(path=self.get_location())

        database = QdrantClient(path=self.get_location())
        return database

    def get_location(self):
        return self.__location
    def set_location(self, location: str):
        self.__location = location