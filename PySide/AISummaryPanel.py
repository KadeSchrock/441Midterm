
from PySide6 import QtCore, QtWidgets


class SummaryPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Heading for the AI summary
        self.title = QtWidgets.QLabel("AI Summary")
        self.title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        # Read-only area for displaying the summary
        self.display = QtWidgets.QTextEdit()
        self.display.setReadOnly(True)
        self.display.setPlaceholderText(
            "AI summary will appear here..."
        )

        # Arrange widgets vertically
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.title)
        layout.addWidget(self.display)

    def set_summary(self, text):
        # Update the displayed AI summary
        self.display.setPlainText(text)
