"""SpawnAgentDialog — création d'habitant personnalisé.

Le moteur accepte déjà ``body``, ``cog``, ``personality``, ``emotions``,
``needs``, ``n_hid``, ``energy`` et ``name`` ; ce dialogue les expose tous.
Les valeurs choisies deviennent le gabarit (``ui_state.tpl_*``) du prochain
habitant, comme le faisait l'ancien dashboard Pygame.
"""
from __future__ import annotations

import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QComboBox, QDialog, QFormLayout, QGridLayout,
                              QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                              QPushButton, QScrollArea, QSlider,
                              QSpinBox, QVBoxLayout, QWidget)

from game.config import (BODY_DEFS, COG_DEFS, EMOTION_DEFS, NEED_DEFS,
                         PERSONALITY_DEFS)

#: (clé de commande, attribut de gabarit ui_state, libellés, défauts moteur)
_SECTIONS = [
    ("body", "tpl_body", BODY_DEFS,
     [0.45, 0.45, 0.45, 0.45, 0.45]),
    ("cog", "tpl_cog", COG_DEFS,
     [0.45, 0.45, 0.45, 0.45]),
    ("personality", "tpl_personality", PERSONALITY_DEFS,
     [0.5] * len(PERSONALITY_DEFS)),
    ("emotions", "tpl_emotions", EMOTION_DEFS,
     [0.0, 0.35, 0.0, 0.1, 0.1, 0.0, 0.0, 0.0]),
    ("needs", "tpl_needs", NEED_DEFS,
     [0.25, 0.70, 0.30, 0.30, 0.80, 0.50, 0.40]),
]

_SECTION_TITLES = {
    "body": "Corps",
    "cog": "Cognition",
    "personality": "Personnalité",
    "emotions": "Émotions",
    "needs": "Besoins",
}


class SpawnAgentDialog(QDialog):
    """Définit un habitant complet avant de le poser sur la carte."""

    def __init__(self, controller, am=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.am = am or getattr(controller.sim, "am", None)
        self.setWindowTitle("Créer un habitant")
        self.setMinimumSize(520, 640)
        self._sliders: dict[tuple[str, int], QSlider] = {}
        self._setup_ui()

    # ------------------------------------------------------------------ UI
    def _setup_ui(self):
        ui_state = self.controller.ui_state
        outer = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        panel = QWidget()
        layout = QVBoxLayout(panel)

        identite = QGroupBox("Identité")
        form = QFormLayout(identite)
        self._name = QLineEdit()
        self._name.setPlaceholderText("laisser vide pour un nom aléatoire")
        self._name.setMaxLength(32)
        form.addRow("Nom", self._name)

        self._sex = QComboBox()
        self._sex.addItems(["F", "M"])
        form.addRow("Sexe", self._sex)

        self._color = QComboBox()
        colors = list(self.am.unit_colors()) if self.am else ["blue"]
        self._color.addItems(colors)
        self._color.currentTextChanged.connect(self._refresh_classes)
        form.addRow("Clan (couleur)", self._color)

        self._cls = QComboBox()
        form.addRow("Classe", self._cls)

        self._n_hid = QComboBox()
        for value in (64, 128, 256):
            self._n_hid.addItem(f"{value} neurones cachés", value)
        form.addRow("Cerveau", self._n_hid)

        self._energy = QSpinBox()
        self._energy.setRange(0, 100)
        self._energy.setValue(70)
        form.addRow("Énergie (%)", self._energy)
        layout.addWidget(identite)

        for key, attr, defs, defaults in _SECTIONS:
            layout.addWidget(self._make_section(key, attr, defs, defaults,
                                                  ui_state))

        layout.addStretch(1)
        scroll.setWidget(panel)
        outer.addWidget(scroll)

        buttons = QHBoxLayout()
        reset_btn = QPushButton("Valeurs moteur")
        reset_btn.clicked.connect(self._reset_defaults)
        buttons.addWidget(reset_btn)
        buttons.addStretch(1)
        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(self.reject)
        buttons.addWidget(cancel_btn)
        ok_btn = QPushButton("Créer sur la carte")
        ok_btn.setToolTip("Valide puis active l'outil « Etre » : le prochain "
                          "clic sur la carte pose cet habitant.")
        ok_btn.clicked.connect(self.accept)
        buttons.addWidget(ok_btn)
        outer.addLayout(buttons)

        self._refresh_classes()

    def _make_section(self, key, attr, defs, defaults, ui_state):
        group = QGroupBox(_SECTION_TITLES[key])
        grid = QGridLayout(group)
        stored = getattr(ui_state, attr, None)
        values = None
        if stored is not None and len(stored) == len(defs):
            values = [float(v) for v in stored]
        for row, label in enumerate(defs):
            value = values[row] if values else defaults[row]
            grid.addWidget(QLabel(label), row, 0)
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(0, 100)
            slider.setValue(int(round(max(0.0, min(1.0, value)) * 100)))
            readout = QLabel(f"{value:.2f}")
            slider.valueChanged.connect(
                lambda v, r=readout: r.setText(f"{v / 100.0:.2f}"))
            grid.addWidget(slider, row, 1)
            grid.addWidget(readout, row, 2)
            self._sliders[(key, row)] = slider
        return group

    def _refresh_classes(self):
        color = self._color.currentText() or "blue"
        current = self._cls.currentText()
        self._cls.clear()
        classes = list(self.am.unit_classes(color)) if self.am else ["pawn"]
        self._cls.addItems(classes)
        index = self._cls.findText(current)
        if index >= 0:
            self._cls.setCurrentIndex(index)

    def _reset_defaults(self):
        for key, _attr, defs, defaults in _SECTIONS:
            for row in range(len(defs)):
                self._sliders[(key, row)].setValue(int(round(defaults[row] * 100)))

    # ------------------------------------------------------------------ données
    def _values(self, key):
        defs = next(d for _k, _a, d, _v in _SECTIONS if _k == key)
        return np.clip(np.array(
            [self._sliders[(key, i)].value() / 100.0 for i in range(len(defs))],
            dtype=np.float64), 0.0, 1.0)

    def options(self) -> dict:
        """Commande ``spawn_agent`` complète, prête à être exécutée."""
        opts = {
            "color": self._color.currentText(),
            "cls": self._cls.currentText(),
            "sex": self._sex.currentText(),
            "n_hid": int(self._n_hid.currentData()),
            "energy": self._energy.value() / 100.0,
            "body": self._values("body").tolist(),
            "cog": self._values("cog").tolist(),
            "personality": self._values("personality").tolist(),
            "emotions": self._values("emotions").tolist(),
            "needs": self._values("needs").tolist(),
        }
        name = self._name.text().strip()
        if name:
            opts["name"] = name
        return opts

    def accept(self):
        ui_state = self.controller.ui_state
        for key, attr, _defs, _default in _SECTIONS:
            setattr(ui_state, attr, self._values(key).tolist())
        ui_state.brain_size = int(self._n_hid.currentData())
        ui_state.template_color = self._color.currentText()
        ui_state.template_class = self._cls.currentText()
        ui_state.template_sex = self._sex.currentText()
        ui_state.pending_spawn_agent = self.options()
        ui_state.active_mode = "agent"
        super().accept()
