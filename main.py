import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "PySide"))

from PySide6 import QtWidgets

from MainWindow import MainWindow
from styles import APP_STYLE


def main():
    app: QtWidgets.QApplication = QtWidgets.QApplication(sys.argv)

    # Apply the global dark theme
    app.setStyleSheet(APP_STYLE)

    window: MainWindow = MainWindow()
    window.resize(1200, 600)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()