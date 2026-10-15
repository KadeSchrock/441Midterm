from Qdrant.QdrantDB import QdrantDB

def main():
    # NOTE: Hard set our database path at root to keep it simple for this project
    database = QdrantDB(location="QDRANT_DB").create_database()

if __name__ == "__main__":
    main()
