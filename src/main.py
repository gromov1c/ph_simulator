"""
Entry Point for the pH Calculator Application.
Initializes the QApplication and main window to start the application.
"""
import sys

from pHCalculatorApp import pHCalculatorApp
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

def run_app():

    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)

    window = pHCalculatorApp()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(run_app())
