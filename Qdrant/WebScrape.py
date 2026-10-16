import requests
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import Any

'''
This class is a simple webscraper that uses requests and BeautifulSoup for HTML scraping
langchain is used to make chunking text for qdrant easy 
'''
class WebScrape:
    __url: str

    def __init__(self, url: str):
        self.set_url(url)

    def scrape(self) -> list[dict[str, Any]]:
        url: str = self.get_url()
        html_dump: requests.Response = requests.get(url)
        soup: BeautifulSoup = BeautifulSoup(html_dump.content, 'html.parser')

        # Tags for stuff we don't want to pull into our text that goes into qdrant
        for tag in soup(["script", "style", "nav", "footer", "header",
                     "aside", "form", "iframe", "noscript", "svg"]):
            tag.decompose()
        text: str = soup.get_text(separator="\n")

        # Split text into multiple chunks
        # code from https://docs.langchain.com/oss/python/integrations/splitters
        text_splitter: RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=100)
        chunks: list[str] = text_splitter.split_text(text)
        # Convert list of string into the format Embed.py expects
        payload: list[dict[str, Any]] = []
        for i, chunk in enumerate(chunks):
            payload.append({
                "document": chunk,
                "source": url,
                "chunk_index": i,
                "chunk_count": len(chunks),
            })
        return payload

    def get_url(self) -> str:
        return self.__url
    def set_url(self, url: str) -> None:
        self.__url = url