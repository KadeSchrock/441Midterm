import sys
from PySide6 import QtCore, QtWidgets, QtGui


'''
Container for all other PySide6 UI elements
AI was used for the generation of the GUI code as was permitted by assignment
'''
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.greeting = "Hello, what would you like to search?"

        # ==========================================
        # LEFT COLUMN: Qdrant Search Results
        # ==========================================

        # Heading for the search results
        self.results_label = QtWidgets.QLabel("Qdrant Search Results")
        self.results_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        # Text area for displaying retrieved search results
        self.results_display = QtWidgets.QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setPlaceholderText(
            "Search results will appear here..."
        )

        # Arrange the heading above the results display
        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(self.results_label)
        left_layout.addWidget(self.results_display)

        # Put the left column elements inside a container
        left_column = QtWidgets.QWidget()
        left_column.setLayout(left_layout)

        # ==========================================
        # MIDDLE COLUMN: URLs and Search Input
        # ==========================================

        # URL section heading
        self.url_label = QtWidgets.QLabel("Web Sources")
        self.url_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        # Multiline input for pasting URLs
        self.url_input = QtWidgets.QTextEdit()
        self.url_input.setPlaceholderText(
            "Paste URLs here, one URL per line..."
        )

        # Button for submitting URLs
        self.url_submit_button = QtWidgets.QPushButton("Submit URLs")
        self.url_submit_button.clicked.connect(self.submit_urls)

        # Greeting displayed above the search input
        self.label = QtWidgets.QLabel(self.greeting)
        self.label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        # Multiline input for the user's search
        self.input_field = QtWidgets.QTextEdit()
        self.input_field.setPlaceholderText("Enter your search...")

        # Button for submitting the search
        self.submit_button = QtWidgets.QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_search)

        # Arrange the middle column elements vertically
        middle_layout = QtWidgets.QVBoxLayout()

        # Add the URL submission section
        middle_layout.addWidget(self.url_label)
        middle_layout.addWidget(self.url_input)
        middle_layout.addWidget(self.url_submit_button)

        # Add the search section
        middle_layout.addWidget(self.label)
        middle_layout.addWidget(self.input_field)
        middle_layout.addWidget(self.submit_button)

        # Put the middle column elements inside a container
        middle_column = QtWidgets.QWidget()
        middle_column.setLayout(middle_layout)

        # ==========================================
        # RIGHT COLUMN: AI Summary
        # ==========================================

        # Heading for the AI summary
        self.summary_label = QtWidgets.QLabel("AI Summary")
        self.summary_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        # Text area for displaying the AI-generated summary
        self.summary_display = QtWidgets.QTextEdit()
        self.summary_display.setReadOnly(True)
        self.summary_display.setPlaceholderText(
            "AI summary will appear here..."
        )

        # Arrange the heading above the summary display
        right_layout = QtWidgets.QVBoxLayout()
        right_layout.addWidget(self.summary_label)
        right_layout.addWidget(self.summary_display)

        # Put the right column elements inside a container
        right_column = QtWidgets.QWidget()
        right_column.setLayout(right_layout)

        # ==========================================
        # MAIN LAYOUT: Three Columns Side by Side
        # ==========================================

        # QHBoxLayout arranges the three columns horizontally
        main_layout = QtWidgets.QHBoxLayout(self)

        # Add the three columns to the main layout
        main_layout.addWidget(left_column)
        main_layout.addWidget(middle_column)
        main_layout.addWidget(right_column)

        # Set relative column widths:
        # Left = 1 part, Middle = 2 parts, Right = 1 part
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 2)
        main_layout.setStretch(2, 1)

    # ==========================================
    # SEARCH FUNCTION
    # ==========================================

    def submit_search(self):
        # Get the user's input and remove extra whitespace
        search_text = self.input_field.toPlainText().strip()

        # Ignore empty searches
        if not search_text:
            print("Please enter a search.")
            return

        # Print the search to the terminal for now
        print("Search:", search_text)

        # Placeholder until Qdrant and AI are connected
        self.results_display.setPlainText(
            "Qdrant results will appear here."
        )
        self.summary_display.setPlainText(
            "AI summary will appear here."
        )

    # ==========================================
    # URL SUBMISSION FUNCTION
    # ==========================================

    def submit_urls(self):
        # Get the text from the URL input area
        url_text = self.url_input.toPlainText().strip()

        # Split the input into individual URLs,
        # ignoring blank lines
        urls = [
            url.strip()
            for url in url_text.splitlines()
            if url.strip()
        ]

        # Don't submit if no URLs were entered
        if not urls:
            print("Please enter at least one URL.")
            return

        # Print the submitted URLs to the terminal
        print("URLs submitted:")
        for url in urls:
            print(url)

        # Placeholder until the web scraper is implemented
        print(
            f"Ready to send {len(urls)} URL(s) "
            "to the web scraper."
        )


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(1200, 600)
    widget.show()

    sys.exit(app.exec())
