"""StatusPill — badge court de la barre d'état (Lot H)."""
from PyQt6.QtWidgets import QLabel

#: Style commun a toutes les pills (palette Neural Lab).
PILL_BASE = (
    "background: #19222D; border: 1px solid #2A394A; "
    "border-radius: 8px; padding: 3px 7px;"
)


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

    def _apply_style(self):
        self.setStyleSheet(f"{PILL_BASE} color: {self._pill_color};")
