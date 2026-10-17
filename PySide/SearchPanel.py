
from PySide6 import QtCore, QtGui, QtWidgets
from WidgetEffects import add_shadow


class AddSourcesDialog(QtWidgets.QDialog):
    """Small dialog for pasting web-source URLs, one per line."""

    sources_submitted = QtCore.Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Web Sources")
        self.resize(560, 400)

        self.url_input = QtWidgets.QTextEdit()
        self.url_input.setPlaceholderText(
            "Paste URLs here, one URL per line..."
        )
        add_shadow(self.url_input, blur=16, offset_y=3, opacity=70)

        self.submit_button = QtWidgets.QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_sources)
        add_shadow(self.submit_button, blur=16, offset_y=3, opacity=70)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.url_input)
        layout.addWidget(self.submit_button)

    def submit_sources(self):
        text = self.url_input.toPlainText()

        urls = [
            url.strip()
            for url in text.splitlines()
            if url.strip()
        ]

        if not urls:
            return

        self.sources_submitted.emit(urls)
        self.accept()


class ResultCard(QtWidgets.QWidget):
    """One Google-style search result: title, confidence, URL, snippet.

    Clicking the snippet expands/collapses the full text,
    clicking the title or URL opens the source website.
    """

    # Snippets longer than this are truncated until expanded
    SNIPPET_LIMIT = 220

    def __init__(self, title, url, snippet, score=None, parent=None):
        super().__init__(parent)

        self.url = url
        self.full_text = snippet
        self.expanded = False

        # Rounded card background with a subtle shadow
        self.setObjectName("resultCard")
        add_shadow(self, blur=16, offset_y=3, opacity=70)

        self.title_label = QtWidgets.QLabel(title)
        self.title_label.setObjectName("resultTitle")
        self.title_label.setCursor(
            QtCore.Qt.CursorShape.PointingHandCursor
        )
        self.title_label.setToolTip(url)
        self.title_label.mousePressEvent = self.open_url

        header = QtWidgets.QHBoxLayout()
        header.addWidget(self.title_label)
        header.addStretch(1)

        if score is not None:
            # Confidence of the top hit from the Qdrant query
            self.score_label = QtWidgets.QLabel(
                f"confidence: {score * 100:.0f}%"
            )
            self.score_label.setObjectName("resultScore")
            header.addWidget(self.score_label)

        self.url_label = QtWidgets.QLabel(url)
        self.url_label.setObjectName("resultUrl")
        self.url_label.setCursor(
            QtCore.Qt.CursorShape.PointingHandCursor
        )
        self.url_label.mousePressEvent = self.open_url

        self.snippet_label = QtWidgets.QLabel(self._short_text())
        self.snippet_label.setObjectName("resultSnippet")
        self.snippet_label.setWordWrap(True)
        self.snippet_label.setCursor(
            QtCore.Qt.CursorShape.PointingHandCursor
        )
        self.snippet_label.mousePressEvent = self.toggle_expanded

        layout = QtWidgets.QVBoxLayout(self)
        # Keep the content inset from the card's rounded border
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(4)
        layout.addLayout(header)
        layout.addWidget(self.url_label)
        layout.addWidget(self.snippet_label)

    def paintEvent(self, event):
        # A plain QWidget subclass is not given Qt::WA_StyledBackground by the
        # stylesheet engine, so the QSS background/border/border-radius on
        # #resultCard are never painted. Draw the styled background explicitly
        # (Qt-documented workaround) so the rounded purple card outline shows.
        option = QtWidgets.QStyleOption()
        option.initFrom(self)
        painter = QtGui.QPainter(self)
        self.style().drawPrimitive(
            QtWidgets.QStyle.PrimitiveElement.PE_Widget,
            option,
            painter,
            self,
        )
        painter.end()
        super().paintEvent(event)

    def _short_text(self):
        # Truncated version of the snippet shown until expanded
        if len(self.full_text) <= self.SNIPPET_LIMIT:
            return self.full_text
        return self.full_text[: self.SNIPPET_LIMIT].rstrip() + "…"

    def open_url(self, event):
        # Open the result URL in the default browser
        if self.url:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.url))
        event.accept()

    def toggle_expanded(self, event):
        # Toggle between the short snippet and the full text
        self.expanded = not self.expanded
        self.snippet_label.setText(
            self.full_text if self.expanded else self._short_text()
        )
        event.accept()


class SearchPanel(QtWidgets.QWidget):
    """Main panel: ADD DATA button, search bar, and Qdrant results.

    set_results() accepts either a list of result dicts with the keys
    "title", "url", and "snippet", or a plain string shown as a
    single snippet-only entry.
    """

    # Signals sent when the user submits URLs or a search
    urls_submitted = QtCore.Signal(list)
    search_submitted = QtCore.Signal(str)

    def __init__(self):
        super().__init__()

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

        search_row = QtWidgets.QHBoxLayout()
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
        loading_layout = QtWidgets.QHBoxLayout(self.loading_widget)
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

        self._cards = []

        top_row = QtWidgets.QHBoxLayout()
        top_row.addWidget(self.add_data_button)
        top_row.addStretch(1)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(top_row)
        layout.addLayout(search_row)
        layout.addWidget(self.results_title)
        layout.addWidget(self.results_scroll)

    def open_add_sources(self):
        dialog = AddSourcesDialog(self)
        dialog.sources_submitted.connect(self.urls_submitted.emit)
        dialog.exec()

    def submit_search(self):
        search_text = self.search_input.text().strip()

        if not search_text:
            return

        self.search_submitted.emit(search_text)

    def set_loading(self, loading):
        # Show/hide the loading indicator while a search is running
        self.loading_widget.setVisible(loading)
        self.placeholder.setVisible(not loading and not self._cards)

    def set_results(self, results):
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

        for item in results:
            card = ResultCard(
                item.get("title", ""),
                item.get("url", ""),
                item.get("snippet", ""),
                item.get("score"),
            )
            # Insert before the trailing stretch
            self.results_layout.insertWidget(
                self.results_layout.count() - 1, card
            )
            self._cards.append(card)

    def _clear_results(self):
        for card in self._cards:
            self.results_layout.removeWidget(card)
            card.deleteLater()
        self._cards.clear()
