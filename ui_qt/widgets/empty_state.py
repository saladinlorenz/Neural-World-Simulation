"""EmptyState — vue d'etat vide reutilisable dans les docks (Lot E).

Palette Neural Lab (plan UX/UI, section A) :
accent ``#4CC9F0``, texte ``#E7EDF5``, attente ``#91A0B2``,
surface ``#121922`` / bord ``#1D2835``.

Le panneau porte ses propres couleurs de fond : la vue reste lisible en
theme sombre comme en theme clair (le theme global est gere ailleurs).
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
        self.setStyleSheet(
            "QWidget#emptyState {"
            "background-color: #121922;"
            "border: 1px solid #1D2835;"
            "border-radius: 10px;"
            "}"
        )

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(8)
        layout.setContentsMargins(18, 26, 18, 26)

        self.icon_label = QLabel(icon)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet(
            "font-size: 42px; color: #4CC9F0; font-weight: 300;"
            "background: transparent;"
        )

        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet(
            "font-size: 15px; font-weight: 600; color: #E7EDF5;"
            "background: transparent;"
        )

        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setStyleSheet(
            "color: #91A0B2; background: transparent;"
        )
        self.message_label.setMaximumWidth(280)

        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.message_label)

    def set_state(self, icon, title, message):
        """Change l'icone, le titre et le message de la vue vide."""
        self.icon_label.setText(icon)
        self.title_label.setText(title)
        self.message_label.setText(message)
