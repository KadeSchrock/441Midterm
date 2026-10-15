
from PySide6 import QtCore, QtWidgets
from WidgetEffects import add_shadow

class SearchPanel(QtWidgets.QWidget):

    # Signals sent when the user submits URLs or a search
    urls_submitted = QtCore.Signal(list)
    search_submitted = QtCore.Signal(str)

    def __init__(self):
        super().__init__()

        # search_label
        self.search_label = QtWidgets.QLabel(
            "Hello, what would you like to search?"
        )
        self.search_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.search_label.setObjectName("panelTitle")
         # Add a subtle shadow to the results display
        add_shadow(self.search_label, blur=16, offset_y=3, opacity=70)
        # URL input section
        self.url_label = QtWidgets.QLabel("Web Sources")
        self.url_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.url_label.setObjectName("panelTitle")

        self.url_input = QtWidgets.QTextEdit()
        self.url_input.setPlaceholderText(
            "Paste URLs here, one URL per line..."
        )
         # Add a subtle shadow to the results display
        add_shadow(self.url_input, blur=16, offset_y=3, opacity=70)

        self.url_button = QtWidgets.QPushButton("Submit URLs")
        self.url_button.clicked.connect(self.submit_urls)
         # Add a subtle shadow to the results display
        add_shadow(self.url_button, blur=16, offset_y=3, opacity=70)

        # Search input section
        self.search_input = QtWidgets.QTextEdit()
        self.search_input.setPlaceholderText(
            "Enter your search..."
        )

        self.search_button = QtWidgets.QPushButton("Submit Text Embedding")
        self.search_button.clicked.connect(self.submit_search)
         # Add a subtle shadow to the results display
        add_shadow(self.search_button, blur=16, offset_y=3, opacity=70)
        # Arrange all widgets vertically
        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.url_button)

        layout.addWidget(self.search_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)

    def submit_urls(self):
        # Read the URLs, one per line
        text = self.url_input.toPlainText()

        urls = [
            url.strip()
            for url in text.splitlines()
            if url.strip()
        ]

        # Ignore empty submissions
        if not urls:
            print("Please enter at least one URL.")
            return

        # Notify main.py that URLs were submitted
        self.urls_submitted.emit(urls)

    def submit_search(self):
        # Read the user's search
        search_text = self.search_input.toPlainText().strip()

        # Ignore empty submissions
        if not search_text:
            print("Please enter a search.")
            return

        # Notify main.py that a search was submitted
        self.search_submitted.emit(search_text)
