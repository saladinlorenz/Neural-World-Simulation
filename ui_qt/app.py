"""app — setup de l'application PyQt6."""
import sys
from PyQt6.QtWidgets import QApplication


def create_app(argv=None):
    """Crée et configure l'application PyQt6."""
    app = QApplication(argv or sys.argv)
    app.setApplicationName("Univers Vivant")
    app.setApplicationDisplayName("Univers Vivant — PyQt6")
    # Lot A : le thème (Neural Lab sombre par défaut) est posé des la creation
    # de la QApplication, pour que tout dialogue neuf parte du bon rendu.
    from ui_qt.theme.theme import apply_theme
    apply_theme(app)
    return app
