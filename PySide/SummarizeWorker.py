from typing import Any

from PySide6 import QtCore

from AI.Summarize import Summarize

'''
This class calls the Gemini API off the GUI thread so the interface
stays responsive while the summary is being generated.
'''
class SummarizeWorker(QtCore.QThread):
    # Emitted when the summary is ready: the summary text and this worker
    summary_ready = QtCore.Signal(str, object)
    # Emitted when the Gemini call raises an error: the error message and this worker
    summary_failed = QtCore.Signal(str, object)

    __results: list[dict[str, Any]]
    __query: str

    def __init__(self, results: list[dict[str, Any]], query: str, parent: QtCore.QObject | None = None):
        super().__init__(parent)
        self.set_results(results)
        self.set_query(query)

    def run(self) -> None:
        try:
            results: list[dict[str, Any]] = self.get_results()
            query: str = self.get_query()

            # Include the user's search query for context, then the top 3 results
            top3: str = "\n\n".join(
                f"{i}. {item['snippet']}"
                for i, item in enumerate(results[:3], 1)
            )
            context: str = f"User searched for: {query}\n\nTop results:\n{top3}"
            summary: str | None = Summarize(qdrant_results=context).summarize_qdrant()
            self.summary_ready.emit(summary or "No summary returned.", self)
        except Exception as error:
            self.summary_failed.emit(str(error), self)

    def get_results(self) -> list[dict[str, Any]]:
        return self.__results
    def set_results(self, results: list[dict[str, Any]]) -> None:
        self.__results = results

    def get_query(self) -> str:
        return self.__query
    def set_query(self, query: str) -> None:
        self.__query = query
