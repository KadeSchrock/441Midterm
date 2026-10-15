from PySide6 import QtCore, QtWidgets
from WidgetEffects import add_shadow

class ResultsPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Heading for the Qdrant results
        self.title = QtWidgets.QLabel("Qdrant Search Results")
        self.title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.title.setObjectName("panelTitle")

        # Read-only area for displaying results
        self.display = QtWidgets.QTextEdit()
        self.display.setReadOnly(True)
        self.display.setPlaceholderText(
            "Search results will appear here..."
        )
         # Add a subtle shadow to the results display
        add_shadow(self.display, blur=16, offset_y=3, opacity=70)

        # Arrange widgets vertically
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.title)
        layout.addWidget(self.display)

    def set_results(self, text):
        # Update the displayed search results
        self.display.setPlainText(text)
