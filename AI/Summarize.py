from google import genai
from google.genai import Client
from google.genai.types import GenerateContentResponse


class Summarize:
    __qdrant_results: str

    def __init__(self, qdrant_results: str):
        self.set_qdrant_results(qdrant_results)

    def summarize_qdrant(self) -> str | None:
        client: Client = genai.Client(api_key=Summarize.API_KEY)
        qdrant_results: str = self.get_qdrant_results()
        system_prompt: str = (f"Summarize the top three results from qdrant. Denote anything you generate inside of <>"
                              f"and keep the rest as is that way we can tell what is AI and what is not, add a layer of your own explanation on top of"
                              f"just summarizing and denote this as a well in the response")

        response: GenerateContentResponse = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=f"{system_prompt}: {qdrant_results}"
        )
        return response.text

    def get_qdrant_results(self) -> str:
        return self.__qdrant_results
    def set_qdrant_results(self, qdrant_results: str) -> None:
        self.__qdrant_results = qdrant_results