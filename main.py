from Qdrant.QdrantDB import QdrantDB

def main():
    # Hard set our database path at root to keep it simple for this project
    db = QdrantDB(location="QDRANT_DB").create()
    

if __name__ == "__main__":
    main()
