"""app — setup de l'application PyQt6."""
import sys
from PyQt6.QtWidgets import QApplication


def create_app(argv=None):
    """Crée et configure l'application PyQt6."""
    app = QApplication(argv or sys.argv)
    app.setApplicationName("Univers Vivant")
    app.setApplicationDisplayName("Univers Vivant — PyQt6")
    return app
