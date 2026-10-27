'''
This module contains the global QSS stylesheet applied to the whole application
'''
APP_STYLE = """
/* ==========================================
   GLOBAL APPLICATION
   ========================================== */

QWidget {
    background-color: #191a1c;
    color: #dfe1e5;
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: 13px;
}

/* ==========================================
   PANEL HEADINGS
   Set objectName("panelTitle") on each heading
   ========================================== */

QLabel#panelTitle {
    background-color: transparent;
    color: #f5f5f6;
    font-size: 17px;
    font-weight: 600;
    padding: 8px 2px;
}

QLabel#appTitle {
    background-color: transparent;
    color: #f5f5f6;
    font-size: 26px;
    font-weight: 700;
}

QLabel#appDescription {
    background-color: transparent;
    color: #a5a7af;
    font-size: 13px;
}

/* General labels */
QLabel {
    background-color: transparent;
    color: #c5c7cb;
}

/* ==========================================
   TEXT INPUTS AND OUTPUT PANELS
   ========================================== */

QTextEdit {
    background-color: #222326;
    color: #dfe1e5;

    border: 1px solid #3b3d42;
    border-radius: 6px;

    padding: 10px;

    selection-background-color: #4542a5;
    selection-color: #ffffff;
}

/* Focused text fields */
QTextEdit:focus {
    border: 1px solid #6b63d9;
    background-color: #242529;
}

/* ==========================================
   BUTTONS
   ========================================== */

QPushButton {
    background-color: #5146c8;
    color: #ffffff;

    border: 1px solid #6559dc;
    border-radius: 6px;

    padding: 9px 16px;

    font-weight: 600;
}

/* Hover */
QPushButton:hover {
    background-color: #6257dc;
    border-color: #8177f0;
}

/* Pressed */
QPushButton:pressed {
    background-color: #4036a9;
    border-color: #5146c8;
}

/* Disabled */
QPushButton:disabled {
    background-color: #303136;
    color: #777980;
    border-color: #3b3d42;
}

/* ==========================================
   SCROLLBARS
   ========================================== */

QScrollBar:vertical {
    background-color: #222326;
    width: 10px;
    margin: 0px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #484a50;
    min-height: 28px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background-color: #656770;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
    border: none;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: transparent;
}

QScrollBar:horizontal {
    background-color: #222326;
    height: 10px;
    margin: 0px;
    border: none;
}

QScrollBar::handle:horizontal {
    background-color: #484a50;
    min-width: 28px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #656770;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0px;
    border: none;
}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {
    background: transparent;
}

/* ==========================================
   TOOLTIP
   ========================================== */

QToolTip {
    background-color: #2b2c30;
    color: #f5f5f6;
    border: 1px solid #494b52;
    padding: 6px;
}

/* ==========================================
   SELECTION / FOCUS
   ========================================== */

QTextEdit:disabled {
    color: #777980;
    background-color: #1d1e20;
}

/* ==========================================
    SEARCH BAR (rounded, purple)
    Set objectName("searchInput") /
    objectName("searchButton")
    ========================================== */

QLineEdit#searchInput {
    background-color: #222326;
    color: #dfe1e5;

    border: 2px solid #5146c8;
    border-radius: 24px;

    padding: 9px 18px;
    font-size: 14px;

    selection-background-color: #4542a5;
    selection-color: #ffffff;
}

QLineEdit#searchInput:focus {
    border: 2px solid #8177f0;
    background-color: #242529;
}

QPushButton#searchButton {
    border-radius: 24px;
    padding: 9px 22px;
}

/* Legend row above the AI summary: explains the text colors.
   Set objectName("summaryLegend") */

QLabel#summaryLegend {
    background-color: transparent;
    color: #a5a7af;
    font-size: 11px;
    padding: 2px 2px 6px 2px;
}

/* AI summary field: always-on purple outline,
   matching the search bar
   Set objectName("summaryDisplay") */

QTextEdit#summaryDisplay {
    border: 2px solid #5146c8;
}

QTextEdit#summaryDisplay:focus {
    border: 2px solid #8177f0;
    background-color: #242529;
}

/* ==========================================
    SEARCH RESULTS (Google-style list)
    Set objectName("resultsScroll") on the
    scroll area, objectName("resultTitle"),
    objectName("resultUrl"),
    objectName("resultSnippet") on each
    result label
    ========================================== */

QScrollArea#resultsScroll {
    background-color: transparent;
    border: none;
}

QScrollArea#resultsScroll > QWidget > QWidget {
    background-color: transparent;
}

QLabel#resultTitle {
    background-color: transparent;
    color: #8ab4f8;
    font-size: 16px;
    font-weight: 500;
}

QLabel#resultUrl {
    background-color: transparent;
    color: #34a853;
    font-size: 12px;
}

QLabel#resultSnippet {
    background-color: transparent;
    color: #bdc1c6;
    font-size: 13px;
}

/* Rounded box around each result
   Set objectName("resultCard") on the card widget */
QWidget#resultCard {
    background-color: #222326;
    border: 2px solid #5146c8;
    border-radius: 12px;
    padding: 12px 14px;
}

/* Confidence percent, top-right of each card
   Set objectName("resultScore") */
QLabel#resultScore {
    background-color: transparent;
    color: #8ab4f8;
    font-size: 12px;
    font-weight: 600;
}

/* Loading indicator shown while a search is running
   Set objectName("loadingBar") / objectName("loadingText") */
QProgressBar#loadingBar {
    background-color: #222326;
    border: 1px solid #3b3d42;
    border-radius: 5px;
}

QProgressBar#loadingBar::chunk {
    background-color: #5146c8;
    border-radius: 4px;
}

QLabel#loadingText {
    background-color: transparent;
    color: #a5a7af;
    font-size: 14px;
}

QLabel#resultPlaceholder {
    background-color: transparent;
    color: #777980;
    font-size: 14px;
    padding: 24px 0;
}

/* ==========================================
    WARNING BOX (URL could not be scraped)
    Set objectName("warningCard") on the card
    widget, objectName("warningTitle") and
    objectName("warningText") on its labels
    ========================================== */

QWidget#warningCard {
    background-color: #262115;
    border: 2px solid #b98a1f;
    border-radius: 12px;
    padding: 12px 14px;
}

QLabel#warningTitle {
    background-color: transparent;
    color: #f0c464;
    font-size: 13px;
    font-weight: 600;
}

QLabel#warningText {
    background-color: transparent;
    color: #d9c48a;
    font-size: 13px;
}
"""
