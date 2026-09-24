"""StatCard — carte visuelle titre + valeur + barre (Lot F).

Palette Neural Lab : fond ``#19222D``, bord ``#2A394A``,
texte ``#E7EDF5``, barre sombre ``#0E141C``. Les couleurs sont
explicites pour rester lisibles en theme sombre comme en theme clair.
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QLabel, QProgressBar, QVBoxLayout


class StatCard(QFrame):
    """Carte compacte : titre colore, valeur et barre de progression fine."""

    def __init__(self, title, color="#4CC9F0", parent=None):
        super().__init__(parent)
        self.setObjectName("statCard")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._color = color
        self.setStyleSheet(
            "QFrame#statCard {"
            "background: #19222D;"
            "border: 1px solid #2A394A;"
            "border-radius: 8px;"
            "}"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 7, 8, 7)
        layout.setSpacing(4)

        self.title = QLabel(title)
        self.title.setWordWrap(True)
        self.title.setStyleSheet(
            f"color: {color}; font-weight: 600; font-size: 11px;"
            "background: transparent;"
        )

        self.value = QLabel("—")
        self.value.setStyleSheet(
            "font-size: 16px; font-weight: 600; color: #E7EDF5;"
            "background: transparent;"
        )

        self.bar = QProgressBar()
        self.bar.setRange(0, 100)
        self.bar.setTextVisible(False)
        self.bar.setFixedHeight(5)
        self.bar.setStyleSheet(
            "QProgressBar { background: #0E141C; border: none;"
            " border-radius: 2px; }"
            f"QProgressBar::chunk {{ background: {color}; border-radius: 2px; }}"
        )

        layout.addWidget(self.title)
        layout.addWidget(self.value)
        layout.addWidget(self.bar)

    def set_title(self, title):
        """Change le titre (libelle colore) de la carte."""
        self.title.setText(str(title))

    def set_value(self, value, suffix="", text=None):
        """Met à jour la valeur et la barre.

        * ``value`` numérique (0..1) → pourcentage affiché + barre remplie ;
        * ``value`` chaîne → texte brut, barre vide ;
        * ``text`` affiche un libellé (ex. clé dominante) tout en pilotant
          la barre avec ``value``.
        """
        if isinstance(value, str):
            self.value.setText(value if text is None else str(text))
            self.bar.setValue(0)
            return
        try:
            number = float(value)
        except (TypeError, ValueError):
            self.value.setText("—" if text is None else str(text))
            self.bar.setValue(0)
            return
        if text is None:
            self.value.setText(f"{number * 100:.0f}{suffix}")
        else:
            self.value.setText(str(text))
        self.bar.setValue(max(0, min(100, int(round(number * 100)))))
