from PySide6 import QtCore, QtGui, QtWidgets
from WidgetEffects import add_shadow

'''
This class is an amber warning box shown for a URL that could not be scraped.
'''
class WarningCard(QtWidgets.QWidget):
    title_label: QtWidgets.QLabel
    message_label: QtWidgets.QLabel

    def __init__(self, url: str, parent: QtCore.QObject | None = None):
        super().__init__(parent)

        # Rounded card background with a subtle shadow
        self.setObjectName("warningCard")
        add_shadow(self, blur=16, offset_y=3, opacity=70)

        self.title_label = QtWidgets.QLabel("Warning")
        self.title_label.setObjectName("warningTitle")

        self.message_label = QtWidgets.QLabel(
            f"trafilatura could not scrape data from this url: {url}"
        )
        self.message_label.setObjectName("warningText")
        self.message_label.setWordWrap(True)

        layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(4)
        layout.addWidget(self.title_label)
        layout.addWidget(self.message_label)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        # Same Qt-documented workaround as ResultCard: a plain QWidget
        # subclass is not given Qt::WA_StyledBackground, so the QSS
        # background/border/border-radius on #warningCard are drawn here.
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
