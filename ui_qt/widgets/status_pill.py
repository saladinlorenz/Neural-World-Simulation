"""StatusPill — badge court de la barre d'état (Lot H)."""
from PyQt6.QtWidgets import QLabel


class StatusPill(QLabel):
    """Bloc court de la barre d'état : texte court + couleur d'accent."""

    def __init__(self, text="", color="#4CC9F0", parent=None):
        super().__init__(text, parent)
        self._pill_color = color
        self._apply_style()

    def set_pill_color(self, color):
        """Change la couleur du texte (inchangee si deja identique)."""
        if color == self._pill_color:
            return
        self._pill_color = color
        self._apply_style()

    def pill_color(self):
        return self._pill_color

    def refresh_theme(self):
        """Repeint le badge selon le theme actif (appele par apply_theme)."""
        self._apply_style()

    def _apply_style(self):
        from ui_qt.theme.theme import panel_palette

        c = panel_palette("card")
        self.setStyleSheet(
            f"background: {c['bg']}; border: 1px solid {c['border']}; "
            f"border-radius: 8px; padding: 3px 7px; color: {self._pill_color};"
        )
