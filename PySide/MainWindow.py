
import sys
from PySide6 import QtWidgets

# Import our custom panel classes from their separate files
from QdrantResultsPanel import ResultsPanel
from SearchPanel import SearchPanel
from AISummaryPanel import SummaryPanel


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create each panel
        self.results_panel = ResultsPanel()
        self.search_panel = SearchPanel()
        self.summary_panel = SummaryPanel()

        # Connect search panel signals to main.py functions
        self.search_panel.urls_submitted.connect(
            self.handle_urls
        )
        self.search_panel.search_submitted.connect(
            self.handle_search
        )

        # Arrange the three panels horizontally
        main_layout = QtWidgets.QHBoxLayout(self)

        main_layout.addWidget(self.results_panel)
        main_layout.addWidget(self.search_panel)
        main_layout.addWidget(self.summary_panel)

        # Set relative widths: 1 : 2 : 1
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 2)
        main_layout.setStretch(2, 1)

    def handle_urls(self, urls):
        # Handle URLs submitted by the search panel
        print("URLs submitted:")

        for url in urls:
            print(url)

        # Placeholder until the web scraper is implemented
        print(f"Received {len(urls)} URL(s).")

    def handle_search(self, search_text):
        # Handle a search submitted by the search panel
        print("Search:", search_text)

        # Placeholder until Qdrant and AI are connected
        self.results_panel.set_results(
            "Qdrant results will appear here."
        )

        self.summary_panel.set_summary(
            "AI summary will appear here."
        )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(1200, 600)
    widget.show()

    sys.exit(app.exec())

