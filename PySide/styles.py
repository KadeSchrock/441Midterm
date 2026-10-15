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
"""
