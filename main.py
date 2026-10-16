from Qdrant.QdrantDB import QdrantDB
from Qdrant.Embed import Embed
from Qdrant.Search import Search
from Qdrant.WebScrape import WebScrape

def main():
    # NOTE: Hard set our database path at root to keep it simple for this project
    database = QdrantDB(location="QDRANT_DB").create_database()

    ### TEST
    test_str = "What types of chunking strategies are there in qdrant"
    scrape_data = WebScrape(url="https://qdrant.tech/course/beginners/module-2/chunking-strategies/").scrape()
    Embed(gpu=False, payload=scrape_data, database=database).embed()
    result = Search(request=test_str, database=database).search()
    print(result)

if __name__ == "__main__":
    main()
