"""EmptyState — vue d'etat vide reutilisable dans les docks (Lot E).

Palette Neural Lab (plan UX/UI, section A) :
accent ``#4CC9F0``, texte ``#E7EDF5``, attente ``#91A0B2``,
surface ``#121922`` / bord ``#1D2835``.

Le panneau porte ses propres couleurs de fond, choisies par thème via
``panel_palette`` : il reste lisible en thème sombre comme en thème clair.
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class EmptyState(QWidget):
    """Panneau centre : icone + titre + message, affiche quand un dock est vide."""

    def __init__(self, icon="◌", title="Rien à afficher", message="", parent=None):
        super().__init__(parent)
        self.setObjectName("emptyState")
        # Fond peint par la feuille de style du widget (requis en theme clair).
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(8)
        layout.setContentsMargins(18, 26, 18, 26)

        self.icon_label = QLabel(icon)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setWordWrap(True)

        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setMaximumWidth(280)

        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.message_label)
        self.refresh_theme()

    def refresh_theme(self):
        """Repeint le panneau selon le theme actif (appele par apply_theme)."""
        from ui_qt.theme.theme import panel_palette

        c = panel_palette("panel")
        self.setStyleSheet(
            "QWidget#emptyState {"
            f"background-color: {c['bg']};"
            f"border: 1px solid {c['border']};"
            "border-radius: 10px;"
            "}"
        )
        self.icon_label.setStyleSheet(
            "font-size: 42px; color: #4CC9F0; font-weight: 300;"
            "background: transparent;"
        )
        self.title_label.setStyleSheet(
            f"font-size: 15px; font-weight: 600; color: {c['text']};"
            "background: transparent;"
        )
        self.message_label.setStyleSheet(
            f"color: {c['muted']}; background: transparent;"
        )

    def set_state(self, icon, title, message):
        """Change l'icone, le titre et le message de la vue vide."""
        self.icon_label.setText(icon)
        self.title_label.setText(title)
        self.message_label.setText(message)
