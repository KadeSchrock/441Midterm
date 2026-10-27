from PySide6 import QtCore, QtWidgets
from WidgetEffects import add_shadow
from summary_format import render_summary, THEME_BLUE, THEME_TEXT

'''
This class is the right-hand panel with a Generate button and a read-only
summary display.
The button emits summarize_requested only when the user clicks it,
so the Gemini API key is never hit until the user opts in.
'''
class SummaryPanel(QtWidgets.QWidget):
    # Emitted when the user clicks the Generate button
    summarize_requested = QtCore.Signal()

    title: QtWidgets.QLabel
    legend: QtWidgets.QLabel
    display: QtWidgets.QTextEdit
    loading_widget: QtWidgets.QWidget
    loading_bar: QtWidgets.QProgressBar
    loading_label: QtWidgets.QLabel
    summarize_button: QtWidgets.QPushButton

    def __init__(self):
        super().__init__()

        # Heading for the AI summary
        self.title = QtWidgets.QLabel("AI Summary")
        self.title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.title.setObjectName("panelTitle")

        # Legend explaining the text colors used in the summary
        self.legend = QtWidgets.QLabel(
            f'<span style="color:{THEME_BLUE};">●</span> GenAI text'
            f'&nbsp;&nbsp;&nbsp;'
            f'<span style="color:{THEME_TEXT};">●</span> From database'
        )
        self.legend.setObjectName("summaryLegend")
        self.legend.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )

        # Read-only area for displaying the summary
        self.display = QtWidgets.QTextEdit()
        self.display.setObjectName("summaryDisplay")
        self.display.setReadOnly(True)
        self.display.setPlaceholderText(
            "AI summary will appear here..."
        )
        # Add a subtle shadow to the results display
        add_shadow(self.display, blur=16, offset_y=3, opacity=70)

        # Loading indicator shown while the summary is being generated;
        # it takes over the display's space until the text arrives
        self.loading_widget = QtWidgets.QWidget()
        self.loading_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.loading_widget.setVisible(False)
        loading_layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(self.loading_widget)
        loading_layout.addStretch(1)
        self.loading_bar = QtWidgets.QProgressBar()
        self.loading_bar.setObjectName("loadingBar")
        self.loading_bar.setRange(0, 0)  # indeterminate mode
        self.loading_bar.setTextVisible(False)
        self.loading_bar.setFixedSize(160, 18)
        self.loading_label = QtWidgets.QLabel("Generating summary...")
        self.loading_label.setObjectName("loadingText")
        loading_layout.addWidget(
            self.loading_bar,
            alignment=QtCore.Qt.AlignmentFlag.AlignHCenter,
        )
        loading_layout.addWidget(
            self.loading_label,
            alignment=QtCore.Qt.AlignmentFlag.AlignHCenter,
        )
        loading_layout.addStretch(1)

        # Button the user must click to trigger the Gemini call
        self.summarize_button = QtWidgets.QPushButton("Generate AI Summary")
        self.summarize_button.setObjectName("summarizeButton")
        self.summarize_button.setEnabled(False)  # off until results exist
        self.summarize_button.clicked.connect(self.summarize_requested.emit)
        add_shadow(self.summarize_button, blur=16, offset_y=3, opacity=70)

        # Arrange widgets vertically
        layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.title)
        layout.addWidget(self.legend)
        layout.addWidget(self.display)
        layout.addWidget(self.loading_widget)
        layout.addWidget(self.summarize_button)

    def set_summary(self, text: str) -> None:
        # Update the displayed AI summary.  The raw <> markers are
        # stripped and the AI-generated spans are highlighted in the
        # theme blue, with headings / bold / bullets rendered as rich text
        document: str = render_summary(text)
        if document:
            self.display.setHtml(document)
        else:
            self.display.clear()

    def set_has_results(self, has_results: bool) -> None:
        # Enable / disable the button based on whether a search returned data
        self.summarize_button.setEnabled(has_results)

    def set_summarizing(self, busy: bool) -> None:
        # Show a "working" state while the API call is in flight:
        # the button is disabled and the display is swapped for the
        # loading indicator until the summary arrives
        self.summarize_button.setEnabled(not busy)
        self.summarize_button.setText(
            "Generating..." if busy else "Generate AI Summary"
        )
        self.display.setVisible(not busy)
        self.loading_widget.setVisible(busy)
