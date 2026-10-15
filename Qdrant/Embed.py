import uuid
from typing import Any
from QdrantDB import QdrantDB
from qdrant_client import QdrantClient, models

'''
This class contains the workflows needed to embed new information into your qdrant database
'''
class Embed:
    # flag for if embedding with the gpu or not, will be a button in the UI requires cuda if using GPU
    __gpu: bool
    # payloads are always a list of dictionaries with strings as the keys and Any for the content
    # This can be seen from this fragment of the official qdrant example code: payload = [
    #     {"document": "Qdrant has Langchain integrations", "source": "Langchain-docs", },
    #     {"document": "Qdrant also has Llama Index integrations", "source": "LlamaIndex-docs"},
    # ]
    __payload: list[dict[str, Any]]
    __database: QdrantClient

    def __init__(self, gpu: bool, payload: list[dict[str, Any]], database: QdrantClient):
        self.set_gpu(gpu)
        self.set_payload(payload)
        self.set_database(database)

    def embed(self) -> None:
        database = self.get_database()
        payload = self.get_payload()

        docs = [models.Document(text=data["document"], model=QdrantDB.MODEL_NAME) for data in payload]
        # NOTE: id's for now are going to be set to be unique for each url, would need to be changed if not
        # only entering web scraped data, but keeps it simple for the initial demo to only make it work with webscrape
        ids = [Embed.create_payload_id(data["source"]) for data in payload]

        database.upload_collection(
            collection_name=QdrantDB.COLLECTION_NAME,
            vectors=docs,
            ids=ids,
            payload=payload,
        )

    # Static method to make unique ID for each new URL that is added to our database
    @staticmethod
    def create_payload_id(source: str) -> str:
        id = str(uuid.uuid5(uuid.NAMESPACE_URL, source))
        return id

    def get_payload(self) -> list[dict[str, Any]]:
        return self.__payload
    def set_payload(self, payload: list[dict[str, Any]]) -> None:
        self.__payload = payload

    def get_database(self) -> QdrantClient:
        return self.__database
    def set_database(self, database: QdrantClient) -> None:
        self.__database = database

    def get_gpu(self) -> bool:
        return self.__gpu
    def set_gpu(self, gpu) -> None:
        self.__gpu = gpu