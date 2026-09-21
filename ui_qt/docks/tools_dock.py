"""ToolsDock — dock Qt pour les outils monde."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                              QGridLayout, QPushButton, QLabel, QSlider)
from PyQt6.QtCore import Qt, pyqtSignal


class ToolsDock(QDockWidget):
    """Dock d'outils monde : poser, gommer, sol, eau, terre, mur, etc."""

    mode_changed = pyqtSignal(str)

    TOOLS = [
        ("place", "Poser"), ("erase", "Gommer"), ("floor", "Sol"),
        ("block", "Bloc"),
        ("agent", "Etre"), ("sheep", "Mouton"), ("monster", "Monstre"),
        ("inspect", "Examiner"),
        ("water", "Eau"), ("land", "Terre"), ("wall", "Mur"),
        ("carve", "Sculpter"), ("restore", "Restaurer"),
    ]

    HINTS = {
        "place": "clic = poser l'asset / glisser = peindre",
        "erase": "clic = effacer les objets",
        "floor": "clic = peindre le sol",
        "water": "glisser = transformer terre en eau",
        "land": "glisser = transformer eau en terre",
        "wall": "glisser = placer des rochers",
        "carve": "glisser = creuser les montagnes",
        "restore": "glisser = restaurer le terrain",
        "block": "clic = construire un bloc",
        "agent": "clic = inserer un etre",
        "sheep": "clic = ajouter un mouton",
        "monster": "clic = ajouter un monstre",
        "inspect": "clic = examiner",
    }

    def __init__(self, controller, parent=None):
        super().__init__("Outils", parent)
        self.controller = controller
        self._buttons = {}
        self._setup_ui()

    def _setup_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)

        # Grille d'outils
        grid = QGridLayout()
        grid.setSpacing(4)
        for i, (tool_id, label) in enumerate(self.TOOLS):
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, tid=tool_id: self._on_tool(tid))
            grid.addWidget(btn, i // 3, i % 3)
            self._buttons[tool_id] = btn
        layout.addLayout(grid)

        # Hint
        self._hint = QLabel("")
        self._hint.setWordWrap(True)
        self._hint.setStyleSheet("color: #697281; font-size: 12px;")
        layout.addWidget(self._hint)

        # Slider pinceau
        brush_label = QLabel("Taille pinceau:")
        layout.addWidget(brush_label)
        self._brush_slider = QSlider(Qt.Orientation.Horizontal)
        self._brush_slider.setRange(1, 15)
        self._brush_slider.setValue(3)
        self._brush_slider.valueChanged.connect(self._on_brush)
        layout.addWidget(self._brush_slider)
        self._brush_val = QLabel("3")
        layout.addWidget(self._brush_val)

        # Material
        mat_label = QLabel("Materiau bloc:")
        layout.addWidget(mat_label)
        self._mat_layout = QHBoxLayout()
        for mat in ("bois", "pierre"):
            btn = QPushButton(mat)
            btn.setCheckable(True)
            btn.setChecked(mat == "bois")
            btn.clicked.connect(lambda checked, m=mat: self._on_material(m))
            self._mat_layout.addWidget(btn)
        layout.addLayout(self._mat_layout)

        layout.addStretch()
        self.setWidget(widget)

    def _on_tool(self, tool_id):
        self.controller.ui_state.active_mode = tool_id
        for tid, btn in self._buttons.items():
            btn.setChecked(tid == tool_id)
        self._hint.setText(self.HINTS.get(tool_id, ""))
        self.mode_changed.emit(tool_id)

    def _on_brush(self, value):
        self.controller.ui_state.brush_size = value
        self._brush_val.setText(str(value))

    def _on_material(self, material):
        self.controller.ui_state.block_material = material
        for i in range(self._mat_layout.count()):
            btn = self._mat_layout.itemAt(i).widget()
            if btn:
                btn.setChecked(btn.text() == material)

    def refresh(self):
        mode = self.controller.ui_state.active_mode
        for tid, btn in self._buttons.items():
            btn.setChecked(tid == mode)
        self._hint.setText(self.HINTS.get(mode, ""))
        self._brush_slider.setValue(self.controller.ui_state.brush_size)
