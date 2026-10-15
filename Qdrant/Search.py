from qdrant_client import qdrant_client

'''
This class caches any input put into the pyside6 search bar and sends
The request to the qdrant db
This class is based off of qdrants embedding example at <https://github.com/qdrant/qdrant-client>
'''
class Search:
