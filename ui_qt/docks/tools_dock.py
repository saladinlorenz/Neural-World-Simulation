"""ToolsDock — dock Qt pour les outils monde."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                              QGridLayout, QTabWidget, QPushButton, QLabel,
                              QSlider, QComboBox, QFormLayout, QDoubleSpinBox,
                              QCheckBox)
from PyQt6.QtCore import Qt, pyqtSignal

from game.config import BLOCK_MATERIALS, MONSTER_KINDS
from game.ui_registry import (MODES, TAB_MODES, TAB_HINTS, TAB_TITLES,
                              READONLY_TABS)

#: Libellés français des types de monstres.
MONSTER_LABELS = {
    "": "Aléatoire",
    "bear": "Ours",
    "wolf": "Loup",
    "snake": "Serpent",
    "beatle": "Scarabée",
}

#: Modes pour lesquels le panneau « Paramètres terrain » est affiché.
TERRAIN_MODES = frozenset({
    "flatten", "raise", "carve", "restore", "restore_mountain",
    "paint_grass", "paint_sand", "paint_dirt", "paint_water", "paint_rock",
    "water", "land", "wall",
})

#: Politique sur les objets rencontrés : (libellé, valeur de commande).
OBJECT_POLICIES = (
    ("Supprimer (remove)", "remove"),
    ("Ignorer (skip)", "skip"),
    ("Annuler (cancel)", "cancel"),
)


def _slider_row(slider, value_label):
    """Ligne compacte : curseur extensible + étiquette de valeur."""
    box = QWidget()
    row = QHBoxLayout(box)
    row.setContentsMargins(0, 0, 0, 0)
    row.setSpacing(4)
    row.addWidget(slider, 1)
    row.addWidget(value_label)
    return box


class ToolsDock(QDockWidget):
    """Dock d'outils monde : poser, gommer, sol, eau, terre, mur, etc."""

    mode_changed = pyqtSignal(str)
    command_result = pyqtSignal(dict)

    def __init__(self, controller, parent=None):
        super().__init__("Outils", parent)
        self.controller = controller
        #: tool_id -> liste de boutons (un meme outil peut exister dans
        #: plusieurs onglets, p. ex. « Examiner »).
        self._buttons = {}
        #: tool_id -> index de l'onglet qui le contient.
        self._tab_for_tool = {}
        self._mat_buttons = {}
        self._updating = False
        self._setup_ui()

    def _tab_tools(self):
        """Onglets à afficher : TAB_MODES sans les onglets en lecture seule.

        Tout outil de MODES absent du registre rejoint l'onglet « decor »
        plutôt que de disparaitre de l'interface.
        """
        tabs = [(tab_id, list(tools))
                for tab_id, tools in TAB_MODES.items()
                if tools and tab_id not in READONLY_TABS]
        covered = {tid for _tab, tools in tabs for tid, _label in tools}
        missing = [entry for entry in MODES if entry[0] not in covered]
        if missing:
            for tab_id, tools in tabs:
                if tab_id == "decor":
                    tools.extend(missing)
                    break
            else:
                tabs.append(("decor", list(missing)))
        return tabs

    def _setup_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)

        # Onglets d'outils — source unique : game/ui_registry.TAB_MODES
        self._tabs = QTabWidget()
        for index, (tab_id, tools) in enumerate(self._tab_tools()):
            page = QWidget()
            grid = QGridLayout(page)
            grid.setContentsMargins(4, 4, 4, 4)
            grid.setSpacing(4)
            for i, (tool_id, label) in enumerate(tools):
                btn = QPushButton(label)
                btn.setCheckable(True)
                btn.setToolTip(TAB_HINTS.get(tool_id, ""))
                btn.clicked.connect(lambda checked, tid=tool_id: self._on_tool(tid))
                grid.addWidget(btn, i // 3, i % 3)
                self._buttons.setdefault(tool_id, []).append(btn)
                self._tab_for_tool.setdefault(tool_id, index)
            grid.setColumnStretch(0, 1)
            grid.setColumnStretch(1, 1)
            grid.setColumnStretch(2, 1)
            self._tabs.addTab(page, TAB_TITLES.get(tab_id, tab_id.capitalize()))
        layout.addWidget(self._tabs)

        # Hint
        self._hint = QLabel("")
        self._hint.setWordWrap(True)
        self._hint.setStyleSheet("color: #697281; font-size: 12px;")
        layout.addWidget(self._hint)

        # Slider pinceau (masqué pour Examiner / creer un etre)
        self._brush_box = QWidget()
        _brush_lay = QVBoxLayout(self._brush_box)
        _brush_lay.setContentsMargins(0, 0, 0, 0)
        _brush_lay.setSpacing(4)
        self._brush_title = QLabel("Taille pinceau:")
        self._brush_title.setToolTip(
            "Rayon du pinceau en tuiles.\n"
            "Sert aux outils qui modifient plusieurs tuiles d'un coup : "
            "Gommer, Sol, Bloc, Eau, Terre, Mur et les outils de "
            "sculpture/peinture de terrain.")
        _brush_lay.addWidget(self._brush_title)
        self._brush_slider = QSlider(Qt.Orientation.Horizontal)
        self._brush_slider.setRange(1, 15)
        self._brush_slider.setValue(self.controller.ui_state.brush_size)
        self._brush_slider.setToolTip(self._brush_title.toolTip())
        self._brush_slider.valueChanged.connect(self._on_brush)
        self._brush_val = QLabel(str(self._brush_slider.value()))
        _brush_lay.addWidget(_slider_row(self._brush_slider, self._brush_val))
        layout.addWidget(self._brush_box)

        # Paramètres terrain (masqués hors des modes terrain / peinture)
        state = self.controller.ui_state
        self._terrain_title = QLabel("Paramètres terrain")
        self._terrain_title.setStyleSheet(
            "font-weight: bold; color: #697281; font-size: 12px;")
        self._terrain_title.setToolTip(
            "Réglages des outils de sculpture/peinture du terrain "
            "(Aplanir, Élever, Creuser, Restaurer, Prairie, Sable...).")
        layout.addWidget(self._terrain_title)
        self._terrain_panel = QWidget()
        form = QFormLayout(self._terrain_panel)
        form.setContentsMargins(0, 0, 0, 0)
        form.setSpacing(4)

        # Force (0.01 .. 0.50, curseur 1..50 = valeur x100)
        self._strength_slider = QSlider(Qt.Orientation.Horizontal)
        self._strength_slider.setRange(1, 50)
        self._strength_slider.setValue(
            max(1, min(50, round(float(state.terrain_strength) * 100))))
        self._strength_slider.valueChanged.connect(self._on_terrain_strength)
        self._strength_slider.setToolTip(
            "Force : quantité de matière déplacée par coup "
            "(0.01 léger → 0.50 brutal).")
        self._strength_val = QLabel(f"{float(state.terrain_strength):.2f}")
        form.addRow("Force", _slider_row(self._strength_slider,
                                         self._strength_val))

        # Atténuation (0.1 .. 2.0, curseur 10..200 = valeur x100)
        self._falloff_slider = QSlider(Qt.Orientation.Horizontal)
        self._falloff_slider.setRange(10, 200)
        self._falloff_slider.setValue(
            max(10, min(200, round(float(state.terrain_falloff) * 100))))
        self._falloff_slider.valueChanged.connect(self._on_terrain_falloff)
        self._falloff_slider.setToolTip(
            "Atténuation : adoucissement du bord du pinceau "
            "(0.1 net → 2.0 très diffus).")
        self._falloff_val = QLabel(f"{float(state.terrain_falloff):.2f}")
        form.addRow("Atténuation", _slider_row(self._falloff_slider,
                                               self._falloff_val))

        # Hauteur cible (auto = None)
        target_box = QWidget()
        target_row = QHBoxLayout(target_box)
        target_row.setContentsMargins(0, 0, 0, 0)
        target_row.setSpacing(4)
        self._target_spin = QDoubleSpinBox()
        self._target_spin.setRange(0.0, 1.0)
        self._target_spin.setSingleStep(0.01)
        self._target_spin.setDecimals(2)
        if state.target_height is not None:
            self._target_spin.setValue(float(state.target_height))
        else:
            self._target_spin.setValue(0.5)
        self._target_auto = QCheckBox("auto")
        self._target_spin.setToolTip(
            "Hauteur cible : altitude finale visée (0 = trou, 1 = cime).\n"
            "Cochez « auto » pour suivre la moyenne locale du pinceau.")
        self._target_auto.setToolTip(self._target_spin.toolTip())
        self._target_auto.setChecked(state.target_height is None)
        self._target_spin.setEnabled(state.target_height is not None)
        self._target_spin.valueChanged.connect(self._on_target_height)
        self._target_auto.toggled.connect(self._on_target_auto)
        target_row.addWidget(self._target_spin, 1)
        target_row.addWidget(self._target_auto)
        form.addRow("Hauteur cible", target_box)

        # Mode de pinceau
        self._mode_combo = QComboBox()
        self._mode_combo.addItem("Continu (glisser)", True)
        self._mode_combo.addItem("Un coup (clic)", False)
        self._mode_combo.setCurrentIndex(0 if state.brush_continuous else 1)
        self._mode_combo.setToolTip(
            "Continu : le terrain suit la souris en glissant.\n"
            "Un coup : une seule application par clic.")
        self._mode_combo.currentIndexChanged.connect(self._on_brush_continuous)
        form.addRow("Mode", self._mode_combo)

        # Politique sur les objets
        self._object_combo = QComboBox()
        for label, policy in OBJECT_POLICIES:
            self._object_combo.addItem(label, policy)
        policy_index = self._object_combo.findData(state.object_policy)
        self._object_combo.setCurrentIndex(policy_index if policy_index >= 0
                                           else 0)
        self._object_combo.setToolTip(
            "Que faire des objets (arbres, rochers, blocs) sous le "
            "pinceau ?\nSupprimer = les effacer · Ignorer = sculpter sans "
            "les toucher · Annuler = ne rien faire s'il y en a.")
        self._object_combo.currentIndexChanged.connect(self._on_object_policy)
        form.addRow("Objets", self._object_combo)

        layout.addWidget(self._terrain_panel)

        # Matériau de bloc (visible uniquement avec l'outil « Bloc »)
        self._mat_box = QWidget()
        _mat_lay = QVBoxLayout(self._mat_box)
        _mat_lay.setContentsMargins(0, 0, 0, 0)
        _mat_lay.setSpacing(4)
        _mat_title = QLabel("Materiau bloc:")
        _mat_title.setToolTip(
            "Matériau utilisé par l'outil « Bloc ».\n"
            "Avec l'outil Bloc actif, cliquez sur la carte pour construire "
            "un bloc solide en bois ou en pierre (plusieurs tuiles si le "
            "pinceau est élargi).")
        _mat_lay.addWidget(_mat_title)
        self._mat_hint = QLabel(
            "Sert à l'outil « Bloc » : cliquez sur la carte pour "
            "construire un bloc en bois ou en pierre.")
        self._mat_hint.setWordWrap(True)
        self._mat_hint.setStyleSheet("color: #697281; font-size: 11px;")
        _mat_lay.addWidget(self._mat_hint)
        self._mat_layout = QHBoxLayout()
        current = self.controller.ui_state.block_material
        if current not in BLOCK_MATERIALS:
            current = "bois"
        for mat in BLOCK_MATERIALS:
            btn = QPushButton(mat)
            btn.setCheckable(True)
            btn.setChecked(mat == current)
            btn.setToolTip(f"Construire des blocs en {mat} "
                           "(outil Bloc, ombre Ressources naturelles)")
            btn.clicked.connect(lambda checked, m=mat: self._on_material(m))
            self._mat_layout.addWidget(btn)
            self._mat_buttons[mat] = btn
        _mat_lay.addLayout(self._mat_layout)
        layout.addWidget(self._mat_box)

        # Type de monstre (visible uniquement avec l'outil « Monstre »)
        self._monster_box = QWidget()
        _mon_lay = QVBoxLayout(self._monster_box)
        _mon_lay.setContentsMargins(0, 0, 0, 0)
        _mon_lay.setSpacing(4)
        _mon_title = QLabel("Type de monstre:")
        _mon_title.setToolTip(
            "Espèce ajoutée par l'outil « Monstre » (onglet Étres).\n"
            "Avec l'outil Monstre actif, cliquez sur la carte pour en "
            "faire apparaître un à cet endroit.")
        _mon_lay.addWidget(_mon_title)
        _mon_hint = QLabel(
            "Sert à l'outil « Monstre » (onglet Étres) : cliquez sur la "
            "carte pour en ajouter un.")
        _mon_hint.setWordWrap(True)
        _mon_hint.setStyleSheet("color: #697281; font-size: 11px;")
        _mon_lay.addWidget(_mon_hint)
        self._monster_combo = QComboBox()
        for kind in ("",) + MONSTER_KINDS:
            self._monster_combo.addItem(MONSTER_LABELS.get(kind, kind), kind)
        self._monster_combo.setToolTip(_mon_title.toolTip())
        self._monster_combo.currentIndexChanged.connect(self._on_monster_kind)
        _mon_lay.addWidget(self._monster_combo)
        layout.addWidget(self._monster_box)

        layout.addStretch()
        self.setWidget(widget)
        self._update_sections(state.active_mode)

    def _on_tool(self, tool_id):
        result = self.controller.execute({"kind": "set_mode", "mode": tool_id})
        self.command_result.emit(result)
        if not result.get("ok"):
            return
        self._check_buttons(tool_id)
        self._hint.setText(TAB_HINTS.get(tool_id, ""))
        self._update_sections(tool_id)
        self.mode_changed.emit(tool_id)

    def _check_buttons(self, tool_id):
        for tid, buttons in self._buttons.items():
            for btn in buttons:
                btn.setChecked(tid == tool_id)

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

    # ── Paramètres terrain ──
    def _update_sections(self, mode):
        """Affiche chaque section du dock selon l'outil actif.

        Le pinceau ne sert que pour les outils multi-tuiles, le matériau
        uniquement avec l'outil « Bloc » et le type de monstre uniquement
        avec l'outil « Monstre » : masquer les inutiles évite de laisser
        des boutons dont on ne sait pas à quoi ils servent.
        """
        brush_visible = mode not in {"inspect", "agent", "sheep", "monster"}
        self._brush_box.setVisible(brush_visible)
        self._mat_box.setVisible(mode == "block")
        self._monster_box.setVisible(mode == "monster")
        visible = mode in TERRAIN_MODES
        self._terrain_title.setVisible(visible)
        self._terrain_panel.setVisible(visible)

    def _sync_terrain(self):
        """Resynchronise les widgets terrain depuis ui_state (undo, script)."""
        ui_state = self.controller.ui_state
        self._updating = True
        self._strength_slider.setValue(
            max(1, min(50, round(float(ui_state.terrain_strength) * 100))))
        self._falloff_slider.setValue(
            max(10, min(200, round(float(ui_state.terrain_falloff) * 100))))
        if ui_state.target_height is not None:
            self._target_spin.setValue(float(ui_state.target_height))
        auto = ui_state.target_height is None
        self._target_auto.setChecked(auto)
        self._target_spin.setEnabled(not auto)
        self._mode_combo.setCurrentIndex(
            0 if ui_state.brush_continuous else 1)
        index = self._object_combo.findData(ui_state.object_policy)
        self._object_combo.setCurrentIndex(index if index >= 0 else 0)
        self._updating = False
        self._strength_val.setText(f"{float(ui_state.terrain_strength):.2f}")
        self._falloff_val.setText(f"{float(ui_state.terrain_falloff):.2f}")

    def _on_terrain_strength(self, value):
        if self._updating:
            return
        result = self.controller.execute(
            {"kind": "set_terrain_strength", "value": value / 100.0})
        self.command_result.emit(result)
        if result.get("ok"):
            self._strength_val.setText(
                f"{float(self.controller.ui_state.terrain_strength):.2f}")
        else:
            self._sync_terrain()

    def _on_terrain_falloff(self, value):
        if self._updating:
            return
        result = self.controller.execute(
            {"kind": "set_terrain_falloff", "value": value / 100.0})
        self.command_result.emit(result)
        if result.get("ok"):
            self._falloff_val.setText(
                f"{float(self.controller.ui_state.terrain_falloff):.2f}")
        else:
            self._sync_terrain()

    def _on_target_height(self, value):
        if self._updating or self._target_auto.isChecked():
            return
        result = self.controller.execute(
            {"kind": "set_target_height", "value": float(value)})
        self.command_result.emit(result)
        if not result.get("ok"):
            self._sync_terrain()

    def _on_target_auto(self, checked):
        self._target_spin.setEnabled(not checked)
        if self._updating:
            return
        result = self.controller.execute(
            {"kind": "set_target_height",
             "value": None if checked else float(self._target_spin.value())})
        self.command_result.emit(result)
        if not result.get("ok"):
            self._sync_terrain()

    def _on_brush_continuous(self, index):
        if self._updating:
            return
        result = self.controller.execute(
            {"kind": "set_brush_continuous",
             "continuous": bool(self._mode_combo.currentData())})
        self.command_result.emit(result)
        if not result.get("ok"):
            self._sync_terrain()

    def _on_object_policy(self, index):
        if self._updating:
            return
        result = self.controller.execute(
            {"kind": "set_object_policy",
             "value": self._object_combo.currentData() or "remove"})
        self.command_result.emit(result)
        if not result.get("ok"):
            self._sync_terrain()

    def refresh(self):
        ui_state = self.controller.ui_state
        mode = ui_state.active_mode
        self._check_buttons(mode)
        self._hint.setText(TAB_HINTS.get(mode, ""))
        # L'outil courant peut avoir changé hors dock (clic carte, menu
        # contextuel) : on ouvre son onglet pour que la coche soit visible.
        index = self._tab_for_tool.get(mode)
        if index is not None and self._tabs.currentIndex() != index:
            self._tabs.setCurrentIndex(index)

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

        self._sync_terrain()
        self._update_sections(mode)
