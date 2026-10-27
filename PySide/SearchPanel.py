from typing import Any

from PySide6 import QtCore, QtWidgets
from WidgetEffects import add_shadow
from AddSourcesDialog import AddSourcesDialog
from ResultCard import ResultCard
from WarningCard import WarningCard

'''
This class is the main panel with the ADD DATA button, the search bar,
and the Qdrant search results.
set_results() accepts either a list of result dicts with the keys
"title", "url", and "snippet", or a plain string shown as a
single snippet-only entry.
'''
class SearchPanel(QtWidgets.QWidget):
    # Signals sent when the user submits URLs or a search
    urls_submitted = QtCore.Signal(list)
    search_submitted = QtCore.Signal(str)

    add_data_button: QtWidgets.QPushButton
    search_input: QtWidgets.QLineEdit
    search_button: QtWidgets.QPushButton
    results_title: QtWidgets.QLabel
    results_scroll: QtWidgets.QScrollArea
    results_container: QtWidgets.QWidget
    results_layout: QtWidgets.QVBoxLayout
    loading_widget: QtWidgets.QWidget
    loading_bar: QtWidgets.QProgressBar
    loading_label: QtWidgets.QLabel
    placeholder: QtWidgets.QLabel

    __cards: list[QtWidgets.QWidget]

    def __init__(self):
        super().__init__()
        self.set_cards([])

        # ADD DATA button (top-left)
        self.add_data_button = QtWidgets.QPushButton("ADD DATA")
        self.add_data_button.clicked.connect(self.open_add_sources)
        add_shadow(self.add_data_button, blur=16, offset_y=3, opacity=70)

        # Search bar (rounded, purple)
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText("Enter your search...")
        self.search_input.returnPressed.connect(self.submit_search)

        self.search_button = QtWidgets.QPushButton("Search")
        self.search_button.setObjectName("searchButton")
        self.search_button.clicked.connect(self.submit_search)
        add_shadow(self.search_button, blur=16, offset_y=3, opacity=70)

        search_row: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        search_row.addWidget(self.search_input)
        search_row.addWidget(self.search_button)

        # Qdrant results (Google-style list)
        self.results_title = QtWidgets.QLabel("Qdrant Search Results")
        self.results_title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.results_title.setObjectName("panelTitle")

        self.results_scroll = QtWidgets.QScrollArea()
        self.results_scroll.setObjectName("resultsScroll")
        self.results_scroll.setWidgetResizable(True)
        self.results_scroll.setFrameShape(
            QtWidgets.QFrame.Shape.NoFrame
        )

        self.results_container = QtWidgets.QWidget()
        self.results_layout = QtWidgets.QVBoxLayout(self.results_container)
        self.results_layout.setContentsMargins(0, 0, 0, 0)
        self.results_layout.setSpacing(18)

        # Loading indicator shown while a search is running
        self.loading_widget = QtWidgets.QWidget()
        self.loading_widget.setVisible(False)
        loading_layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout(self.loading_widget)
        loading_layout.setContentsMargins(0, 40, 0, 40)
        self.loading_bar = QtWidgets.QProgressBar()
        self.loading_bar.setObjectName("loadingBar")
        self.loading_bar.setRange(0, 0)  # indeterminate mode
        self.loading_bar.setTextVisible(False)
        self.loading_bar.setFixedSize(56, 20)
        self.loading_label = QtWidgets.QLabel("Searching...")
        self.loading_label.setObjectName("loadingText")
        loading_layout.addStretch(1)
        loading_layout.addWidget(self.loading_bar)
        loading_layout.addWidget(self.loading_label)
        loading_layout.addStretch(1)

        self.placeholder = QtWidgets.QLabel(
            "Search results will appear here..."
        )
        self.placeholder.setObjectName("resultPlaceholder")
        self.placeholder.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.results_layout.addWidget(self.loading_widget)
        self.results_layout.addWidget(self.placeholder)
        self.results_layout.addStretch(1)

        self.results_scroll.setWidget(self.results_container)

        top_row: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
        top_row.addWidget(self.add_data_button)
        top_row.addStretch(1)

        layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(top_row)
        layout.addLayout(search_row)
        layout.addWidget(self.results_title)
        layout.addWidget(self.results_scroll)

    def open_add_sources(self) -> None:
        dialog: AddSourcesDialog = AddSourcesDialog(self)
        dialog.sources_submitted.connect(self.urls_submitted.emit)
        dialog.exec()

    def submit_search(self) -> None:
        search_text: str = self.search_input.text().strip()

        if not search_text:
            return

        self.search_submitted.emit(search_text)

    def set_loading(self, loading: bool, label: str = "Searching...") -> None:
        # Show/hide the loading indicator while a search or an
        # add-data run is in progress
        self.loading_label.setText(label)
        self.loading_widget.setVisible(loading)
        self.placeholder.setVisible(not loading and not self.get_cards())

    def set_results(self, results: list[dict[str, Any]] | str) -> None:
        # Update the displayed search results
        self._clear_results()

        if isinstance(results, str):
            results = [
                {"title": "", "url": "", "snippet": results}
            ]

        if not results:
            self.placeholder.setVisible(True)
            return

        self.placeholder.setVisible(False)

        cards: list[QtWidgets.QWidget] = self.get_cards()
        for item in results:
            card: ResultCard = ResultCard(
                item.get("title", ""),
                item.get("url", ""),
                item.get("snippet", ""),
                item.get("score"),
            )
            # Insert before the trailing stretch
            self.results_layout.insertWidget(
                self.results_layout.count() - 1, card
            )
            cards.append(card)

    def set_add_results(self, successful: list[str], failed: list[str]) -> None:
        # Show the outcome of an add-data run: a success message card
        # followed by one warning box for every URL that could not be
        # scraped
        self._clear_results()

        if successful:
            message: str = f"Added {len(successful)} source(s) to the database."
        else:
            message = "No sources could be added to the database."

        self.placeholder.setVisible(False)

        cards: list[QtWidgets.QWidget] = self.get_cards()

        card: ResultCard = ResultCard("", "", message)
        self.results_layout.insertWidget(
            self.results_layout.count() - 1, card
        )
        cards.append(card)

        for url in failed:
            warning: WarningCard = WarningCard(url)
            self.results_layout.insertWidget(
                self.results_layout.count() - 1, warning
            )
            cards.append(warning)

    def _clear_results(self) -> None:
        for card in self.get_cards():
            self.results_layout.removeWidget(card)
            card.deleteLater()
        self.get_cards().clear()

    def get_cards(self) -> list[QtWidgets.QWidget]:
        return self.__cards
    def set_cards(self, cards: list[QtWidgets.QWidget]) -> None:
        self.__cards = cards
