
import os
import sys
from urllib.parse import urlparse
from PySide6 import QtCore, QtWidgets

# Make the project root importable no matter which directory the GUI is launched from
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from styles import APP_STYLE
from SearchPanel import SearchPanel
from AISummaryPanel import SummaryPanel
from Qdrant.QdrantDB import QdrantDB
from Qdrant.Search import Search
from Qdrant.WebScrape import WebScrape
from Qdrant.Embed import Embed


class SearchWorker(QtCore.QThread):
    """Runs a Qdrant search off the GUI thread so the loading
    indicator can animate while the query is being embedded."""

    results_ready = QtCore.Signal(list, object)
    search_failed = QtCore.Signal(str, object)

    def __init__(self, request, location, parent=None):
        super().__init__(parent)
        self.request = request
        self.location = location

    def run(self):
        try:
            # Create the client in this thread: a local Qdrant client
            # can only be used from the thread that created it
            database = QdrantDB(location=self.location).create_database()
            groups = Search(request=self.request, database=database).search()

            results = [
                {
                    "title": urlparse(group.id).netloc or group.id,
                    "url": group.id,
                    "snippet": group.hits[0].payload["document"],
                    "score": group.hits[0].score,
                }
                for group in groups
            ]
            self.results_ready.emit(results, self)
        except Exception as error:
            self.search_failed.emit(str(error), self)


class AddDataWorker(QtCore.QThread):
    """Scrapes and embeds each submitted URL off the GUI thread so the
    interface stays responsive while the pages are fetched and chunked."""

    data_added = QtCore.Signal(list, object)
    add_failed = QtCore.Signal(str, object)

    def __init__(self, urls, location, parent=None):
        super().__init__(parent)
        self.urls = urls
        self.location = location

    def run(self):
        try:
            # Create the client in this thread: a local Qdrant client
            # can only be used from the thread that created it
            database = QdrantDB(location=self.location).create_database()

            for url in self.urls:
                payload = WebScrape(url=url).scrape()
                if payload:
                    Embed(gpu=False, payload=payload, database=database).embed()

            self.data_added.emit(self.urls, self)
        except Exception as error:
            self.add_failed.emit(str(error), self)


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Qdrant database stored at the project root
        self.db_location = os.path.join(PROJECT_ROOT, "QDRANT_DB")
        self.worker = None
        self.add_worker = None

        # Create each panel
        self.main_panel = SearchPanel()
        self.summary_panel = SummaryPanel()

        # Connect main panel signals
        self.main_panel.urls_submitted.connect(self.handle_urls)
        self.main_panel.search_submitted.connect(self.handle_search)

        # Arrange the two panels horizontally
        main_layout = QtWidgets.QHBoxLayout(self)

        main_layout.addWidget(self.main_panel)
        main_layout.addWidget(self.summary_panel)

        # Set relative widths: 2 : 1
        main_layout.setStretch(0, 2)
        main_layout.setStretch(1, 1)

    def handle_urls(self, urls):
        # Scrape and embed the URLs submitted via the ADD DATA button
        # in a background thread so the GUI stays responsive
        worker = AddDataWorker(urls, self.db_location)
        worker.data_added.connect(self.handle_data_added)
        worker.add_failed.connect(self.handle_add_failed)
        self.add_worker = worker
        self.main_panel.add_data_button.setEnabled(False)
        worker.start()

    def handle_data_added(self, urls, worker):
        # Ignore results from a run that was superseded by a newer one
        if worker is not self.add_worker:
            return

        self.main_panel.add_data_button.setEnabled(True)
        self.main_panel.set_results(
            f"Added {len(urls)} source(s) to the database."
        )

    def handle_add_failed(self, error, worker):
        if worker is not self.add_worker:
            return

        self.main_panel.add_data_button.setEnabled(True)
        self.main_panel.set_results(f"Adding data failed: {error}")

    def handle_search(self, search_text):
        # Run the search in a background thread while showing the loading indicator
        worker = SearchWorker(search_text, self.db_location)
        worker.results_ready.connect(self.handle_results)
        worker.search_failed.connect(self.handle_search_failed)
        self.worker = worker
        self.main_panel.set_loading(True)
        worker.start()

    def handle_results(self, results, worker):
        # Ignore results from a search that was superseded by a newer one
        if worker is not self.worker:
            return

        if not results:
            self.main_panel.placeholder.setText(
                f"No results for '{worker.request}'"
            )

        self.main_panel.set_results(results)
        self.main_panel.set_loading(False)

        self.summary_panel.set_summary(
            "AI summary will appear here."
        )

    def handle_search_failed(self, error, worker):
        if worker is not self.worker:
            return

        self.main_panel.set_loading(False)
        self.main_panel.set_results(f"Search failed: {error}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # Apply the global dark theme
    app.setStyleSheet(APP_STYLE)

    widget = MyWidget()
    widget.resize(1200, 600)
    widget.show()

    sys.exit(app.exec())
