from PySide6 import QtCore, QtGui, QtWidgets
from WidgetEffects import add_shadow

'''
This class renders one Google-style search result: title, confidence,
URL, and snippet.
Clicking the snippet expands/collapses the full text,
clicking the title or URL opens the source website.
'''
class ResultCard(QtWidgets.QWidget):
    # Snippets longer than this are truncated until expanded
    SNIPPET_LIMIT = 220

    title_label: QtWidgets.QLabel
    score_label: QtWidgets.QLabel
    url_label: QtWidgets.QLabel
    snippet_label: QtWidgets.QLabel

    __url: str
    __full_text: str
    __expanded: bool

    def __init__(self, title: str, url: str, snippet: str, score: float | None = None, parent: QtCore.QObject | None = None):
        super().__init__(parent)
        self.set_url(url)
        self.set_full_text(snippet)
        self.set_expanded(False)

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

        header: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()
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

        layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(self)
        # Keep the content inset from the card's rounded border
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(4)
        layout.addLayout(header)
        layout.addWidget(self.url_label)
        layout.addWidget(self.snippet_label)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        # A plain QWidget subclass is not given Qt::WA_StyledBackground by the
        # stylesheet engine, so the QSS background/border/border-radius on
        # #resultCard are never painted. Draw the styled background explicitly
        # (Qt-documented workaround) so the rounded purple card outline shows.
        option: QtWidgets.QStyleOption = QtWidgets.QStyleOption()
        option.initFrom(self)
        painter: QtGui.QPainter = QtGui.QPainter(self)
        self.style().drawPrimitive(
            QtWidgets.QStyle.PrimitiveElement.PE_Widget,
            option,
            painter,
            self,
        )
        painter.end()
        super().paintEvent(event)

    def _short_text(self) -> str:
        # Truncated version of the snippet shown until expanded
        full_text: str = self.get_full_text()
        if len(full_text) <= ResultCard.SNIPPET_LIMIT:
            return full_text
        return full_text[: ResultCard.SNIPPET_LIMIT].rstrip() + "…"

    def open_url(self, event: QtGui.QMouseEvent) -> None:
        # Open the result URL in the default browser
        url: str = self.get_url()
        if url:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))
        event.accept()

    def toggle_expanded(self, event: QtGui.QMouseEvent) -> None:
        # Toggle between the short snippet and the full text
        self.set_expanded(not self.get_expanded())
        self.snippet_label.setText(
            self.get_full_text() if self.get_expanded() else self._short_text()
        )
        event.accept()

    def get_url(self) -> str:
        return self.__url
    def set_url(self, url: str) -> None:
        self.__url = url

    def get_full_text(self) -> str:
        return self.__full_text
    def set_full_text(self, full_text: str) -> None:
        self.__full_text = full_text

    def get_expanded(self) -> bool:
        return self.__expanded
    def set_expanded(self, expanded: bool) -> None:
        self.__expanded = expanded
