from PySide6 import QtCore, QtWidgets


class ResultsPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Heading for the Qdrant results
        self.title = QtWidgets.QLabel("Qdrant Search Results")
        self.title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        # Read-only area for displaying results
        self.display = QtWidgets.QTextEdit()
        self.display.setReadOnly(True)
        self.display.setPlaceholderText(
            "Search results will appear here..."
        )

        # Arrange widgets vertically
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.title)
        layout.addWidget(self.display)

    def set_results(self, text):
        # Update the displayed search results
        self.display.setPlainText(text)
