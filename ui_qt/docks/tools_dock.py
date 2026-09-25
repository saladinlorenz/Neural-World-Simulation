"""ToolsDock — dock Qt pour les outils monde."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                              QGridLayout, QPushButton, QLabel, QSlider,
                              QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal

from game.config import BLOCK_MATERIALS, MONSTER_KINDS
from game.ui_registry import MODES, TAB_HINTS

#: Libellés français des types de monstres.
MONSTER_LABELS = {
    "": "Aléatoire",
    "bear": "Ours",
    "wolf": "Loup",
    "snake": "Serpent",
    "beatle": "Scarabée",
}


class ToolsDock(QDockWidget):
    """Dock d'outils monde : poser, gommer, sol, eau, terre, mur, etc."""

    mode_changed = pyqtSignal(str)
    command_result = pyqtSignal(dict)

    def __init__(self, controller, parent=None):
        super().__init__("Outils", parent)
        self.controller = controller
        self._buttons = {}
        self._mat_buttons = {}
        self._updating = False
        self._setup_ui()

    def _setup_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)

        # Grille d'outils — source unique : game/ui_registry.py
        grid = QGridLayout()
        grid.setSpacing(4)
        for i, (tool_id, label) in enumerate(MODES):
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
        layout.addWidget(QLabel("Taille pinceau:"))
        self._brush_slider = QSlider(Qt.Orientation.Horizontal)
        self._brush_slider.setRange(1, 15)
        self._brush_slider.setValue(self.controller.ui_state.brush_size)
        self._brush_slider.valueChanged.connect(self._on_brush)
        layout.addWidget(self._brush_slider)
        self._brush_val = QLabel(str(self._brush_slider.value()))
        layout.addWidget(self._brush_val)

        # Matériau de bloc
        layout.addWidget(QLabel("Materiau bloc:"))
        self._mat_layout = QHBoxLayout()
        current = self.controller.ui_state.block_material
        if current not in BLOCK_MATERIALS:
            current = "bois"
        for mat in BLOCK_MATERIALS:
            btn = QPushButton(mat)
            btn.setCheckable(True)
            btn.setChecked(mat == current)
            btn.clicked.connect(lambda checked, m=mat: self._on_material(m))
            self._mat_layout.addWidget(btn)
            self._mat_buttons[mat] = btn
        layout.addLayout(self._mat_layout)

        # Type de monstre
        layout.addWidget(QLabel("Type de monstre:"))
        self._monster_combo = QComboBox()
        for kind in ("",) + MONSTER_KINDS:
            self._monster_combo.addItem(MONSTER_LABELS.get(kind, kind), kind)
        self._monster_combo.currentIndexChanged.connect(self._on_monster_kind)
        layout.addWidget(self._monster_combo)

        layout.addStretch()
        self.setWidget(widget)

    def _on_tool(self, tool_id):
        result = self.controller.execute({"kind": "set_mode", "mode": tool_id})
        self.command_result.emit(result)
        if not result.get("ok"):
            return
        for tid, btn in self._buttons.items():
            btn.setChecked(tid == tool_id)
        self._hint.setText(TAB_HINTS.get(tool_id, ""))
        self.mode_changed.emit(tool_id)

    def _on_brush(self, value):
        if self._updating:
            return
        result = self.controller.execute({"kind": "set_brush_size", "size": value})
        self.command_result.emit(result)
        if result.get("ok"):
            self._brush_val.setText(str(result["brush_size"]))

    def _on_material(self, material):
        result = self.controller.execute(
            {"kind": "set_block_material", "material": material})
        self.command_result.emit(result)
        if not result.get("ok"):
            return
        for mat, btn in self._mat_buttons.items():
            btn.setChecked(mat == material)

    def _on_monster_kind(self, *_args):
        result = self.controller.execute({
            "kind": "set_monster_kind",
            "monster_kind": self._monster_combo.currentData() or "",
        })
        self.command_result.emit(result)

    def refresh(self):
        ui_state = self.controller.ui_state
        mode = ui_state.active_mode
        for tid, btn in self._buttons.items():
            btn.setChecked(tid == mode)
        self._hint.setText(TAB_HINTS.get(mode, ""))

        self._updating = True
        self._brush_slider.setValue(int(ui_state.brush_size))
        self._updating = False
        self._brush_val.setText(str(int(ui_state.brush_size)))

        material = ui_state.block_material
        if material not in self._mat_buttons:
            material = "bois"
        for mat, btn in self._mat_buttons.items():
            btn.setChecked(mat == material)

        index = self._monster_combo.findData(ui_state.monster_kind or "")
        if index >= 0:
            self._updating = True
            self._monster_combo.setCurrentIndex(index)
            self._updating = False
