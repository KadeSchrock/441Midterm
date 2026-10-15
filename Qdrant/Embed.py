from qdrant_client import QdrantClient, models

'''
This class contains the workflows needed to embed new information into your qdrant database
'''
class Embed:
    # flag for if embedding with the gpu or not, will be a button in the UI
    __gpu: bool
    __payload

    def __init__(self, gpu: bool):
        self.set_gpu(gpu)

    def embed(self):
        pass



    def get_gpu(self):
        return self.__gpu

    def set_gpu(self, gpu):
        self.__gpu = gpu