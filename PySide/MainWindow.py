import os
import sys
from typing import Any

from PySide6 import QtWidgets

# Make the project root importable no matter which directory the GUI is launched from
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from styles import APP_STYLE
from SearchPanel import SearchPanel
from SummaryPanel import SummaryPanel
from SearchWorker import SearchWorker
from AddDataWorker import AddDataWorker
from SummarizeWorker import SummarizeWorker

'''
This class is the main application window. It arranges the search panel and
the AI summary panel, owns the background worker threads, and routes their
signals back into the UI.
'''
class MainWindow(QtWidgets.QWidget):
    main_panel: SearchPanel
    summary_panel: SummaryPanel

    __db_location: str
    __worker: SearchWorker | None
    __add_worker: AddDataWorker | None
    __summarize_worker: SummarizeWorker | None
    __last_results: list[dict[str, Any]]
    __last_query: str

    def __init__(self):
        super().__init__()

        # Qdrant database stored at the project root
        self.set_db_location(os.path.join(PROJECT_ROOT, "QDRANT_DB"))
        self.set_worker(None)
        self.set_add_worker(None)
        self.set_summarize_worker(None)
        self.set_last_results([])
        self.set_last_query("")

        # Create each panel
        self.main_panel = SearchPanel()
        self.summary_panel = SummaryPanel()

        # Connect main panel signals
        self.main_panel.urls_submitted.connect(self.handle_urls)
        self.main_panel.search_submitted.connect(self.handle_search)

        # Connect the AI summary button
        self.summary_panel.summarize_requested.connect(self.handle_summarize)

        # Arrange the two panels horizontally
        main_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout(self)

        main_layout.addWidget(self.main_panel)
        main_layout.addWidget(self.summary_panel)

        # Set relative widths: 2 : 1
        main_layout.setStretch(0, 2)
        main_layout.setStretch(1, 1)

    def handle_urls(self, urls: list[str]) -> None:
        # Scrape and embed the URLs submitted via the ADD DATA button
        # in a background thread so the GUI stays responsive
        worker: AddDataWorker = AddDataWorker(urls, self.get_db_location())
        worker.data_added.connect(self.handle_data_added)
        worker.add_failed.connect(self.handle_add_failed)
        self.set_add_worker(worker)
        self.main_panel.add_data_button.setEnabled(False)
        self.main_panel.set_loading(True, "Adding data...")
        worker.start()

    def handle_data_added(self, successful: list[str], failed: list[str], worker: AddDataWorker) -> None:
        # Ignore results from a run that was superseded by a newer one
        if worker is not self.get_add_worker():
            return

        self.main_panel.add_data_button.setEnabled(True)
        self.main_panel.set_loading(False)
        self.main_panel.set_add_results(successful, failed)

    def handle_add_failed(self, error: str, worker: AddDataWorker) -> None:
        # Ignore results from a run that was superseded by a newer one
        if worker is not self.get_add_worker():
            return

        self.main_panel.add_data_button.setEnabled(True)
        self.main_panel.set_loading(False)
        self.main_panel.set_results(f"Adding data failed: {error}")

    def handle_search(self, search_text: str) -> None:
        # Run the search in a background thread while showing the loading indicator
        self.set_last_query(search_text)
        worker: SearchWorker = SearchWorker(search_text, self.get_db_location())
        worker.results_ready.connect(self.handle_results)
        worker.search_failed.connect(self.handle_search_failed)
        self.set_worker(worker)
        self.main_panel.set_loading(True)
        worker.start()

    def handle_results(self, results: list[dict[str, Any]], worker: SearchWorker) -> None:
        # Ignore results from a search that was superseded by a newer one
        if worker is not self.get_worker():
            return

        if not results:
            self.main_panel.placeholder.setText(
                f"No results for '{worker.get_request()}'"
            )

        self.main_panel.set_results(results)
        self.main_panel.set_loading(False)

        # Store results and let the user opt in to a summary
        self.set_last_results(results)
        self.summary_panel.set_has_results(bool(results))
        self.summary_panel.set_summary("")

    def handle_search_failed(self, error: str, worker: SearchWorker) -> None:
        # Ignore results from a search that was superseded by a newer one
        if worker is not self.get_worker():
            return

        self.main_panel.set_loading(False)
        self.main_panel.set_results(f"Search failed: {error}")

    def handle_summarize(self) -> None:
        # Kick off the Gemini call in a background thread
        if not self.get_last_results():
            return

        worker: SummarizeWorker = SummarizeWorker(self.get_last_results(), self.get_last_query())
        worker.summary_ready.connect(self.handle_summary_ready)
        worker.summary_failed.connect(self.handle_summary_failed)
        self.set_summarize_worker(worker)
        self.summary_panel.set_summarizing(True)
        worker.start()

    def handle_summary_ready(self, summary: str, worker: SummarizeWorker) -> None:
        # Ignore results from a run that was superseded by a newer one
        if worker is not self.get_summarize_worker():
            return

        self.summary_panel.set_summarizing(False)
        self.summary_panel.set_summary(summary)

    def handle_summary_failed(self, error: str, worker: SummarizeWorker) -> None:
        # Ignore results from a run that was superseded by a newer one
        if worker is not self.get_summarize_worker():
            return

        self.summary_panel.set_summarizing(False)
        self.summary_panel.set_summary(f"Summary failed: {error}")

    def get_db_location(self) -> str:
        return self.__db_location
    def set_db_location(self, db_location: str) -> None:
        self.__db_location = db_location

    def get_worker(self) -> SearchWorker | None:
        return self.__worker
    def set_worker(self, worker: SearchWorker | None) -> None:
        self.__worker = worker

    def get_add_worker(self) -> AddDataWorker | None:
        return self.__add_worker
    def set_add_worker(self, add_worker: AddDataWorker | None) -> None:
        self.__add_worker = add_worker

    def get_summarize_worker(self) -> SummarizeWorker | None:
        return self.__summarize_worker
    def set_summarize_worker(self, summarize_worker: SummarizeWorker | None) -> None:
        self.__summarize_worker = summarize_worker

    def get_last_results(self) -> list[dict[str, Any]]:
        return self.__last_results
    def set_last_results(self, last_results: list[dict[str, Any]]) -> None:
        self.__last_results = last_results

    def get_last_query(self) -> str:
        return self.__last_query
    def set_last_query(self, last_query: str) -> None:
        self.__last_query = last_query