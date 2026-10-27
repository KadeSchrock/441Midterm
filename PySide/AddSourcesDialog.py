from PySide6 import QtCore, QtWidgets
from WidgetEffects import add_shadow

'''
This class is a small dialog for pasting web-source URLs, one per line.
'''
class AddSourcesDialog(QtWidgets.QDialog):
    # Emitted with the list of URLs the user pasted
    sources_submitted = QtCore.Signal(list)

    url_input: QtWidgets.QTextEdit
    submit_button: QtWidgets.QPushButton

    def __init__(self, parent: QtCore.QObject | None = None):
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

        layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.url_input)
        layout.addWidget(self.submit_button)

    def submit_sources(self) -> None:
        text: str = self.url_input.toPlainText()

        urls: list[str] = [
            url.strip()
            for url in text.splitlines()
            if url.strip()
        ]

        if not urls:
            return

        self.sources_submitted.emit(urls)
        self.accept()
