"""ParameterDock — dock Qt pour l'édition des paramètres de simulation."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QPushButton, QScrollArea, QFrame,
                              QSpinBox, QDoubleSpinBox, QCheckBox, QComboBox,
                              QMessageBox, QGroupBox, QGridLayout)
from PyQt6.QtCore import Qt, pyqtSignal

from game.studio_parameters import (
    ParameterStore, PARAMETERS, PARAM_BY_KEY, PARAM_GROUPS,
)


class ParameterDock(QDockWidget):
    """Dock d'édition des paramètres regroupés par catégorie."""

    parameters_applied = pyqtSignal()

    def __init__(self, controller, parent=None):
        super().__init__("Paramètres", parent)
        self.controller = controller
        self._store = ParameterStore()
        self._widgets: dict[str, QWidget] = {}
        self._setup_ui()
        self._load_from_sim()

    def _setup_ui(self):
        root = QWidget()
        main_layout = QVBoxLayout(root)
        main_layout.setContentsMargins(8, 8, 8, 8)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)

        by_group = self._store.by_group()
        for group in PARAM_GROUPS:
            params = by_group.get(group, [])
            if not params:
                continue
            group_box = QGroupBox(group)
            grid = QGridLayout()
            grid.setSpacing(6)
            for row, p in enumerate(params):
                grid.addWidget(QLabel(p.label), row, 0)
                widget = self._make_widget(p)
                self._widgets[p.key] = widget
                grid.addWidget(widget, row, 1)
                desc = QLabel(p.description)
                desc.setStyleSheet("color: #888; font-size: 11px;")
                grid.addWidget(desc, row, 2)
            group_box.setLayout(grid)
            scroll_layout.addWidget(group_box)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        btn_layout = QHBoxLayout()

        self._reset_btn = QPushButton("Réinitialiser")
        self._reset_btn.clicked.connect(self._on_reset)
        btn_layout.addWidget(self._reset_btn)

        btn_layout.addStretch()

        self._apply_btn = QPushButton("Appliquer tout")
        self._apply_btn.setStyleSheet(
            "QPushButton { background-color: #2980b9; color: white; "
            "padding: 6px 18px; border: none; border-radius: 3px; }"
            "QPushButton:hover { background-color: #3498db; }"
        )
        self._apply_btn.clicked.connect(self._on_apply)
        btn_layout.addWidget(self._apply_btn)

        main_layout.addLayout(btn_layout)
        self.setWidget(root)

    def _make_widget(self, p):
        if p.ptype == "int":
            spin = QSpinBox()
            spin.setRange(int(p.minimum), int(p.maximum))
            spin.setValue(int(p.default))
            spin.setToolTip(p.key)
            return spin
        elif p.ptype == "float":
            dspin = QDoubleSpinBox()
            dspin.setRange(p.minimum, p.maximum)
            dspin.setDecimals(3)
            dspin.setSingleStep(0.01)
            dspin.setValue(float(p.default))
            dspin.setToolTip(p.key)
            return dspin
        elif p.ptype == "bool":
            cb = QCheckBox()
            cb.setChecked(bool(p.default))
            cb.setToolTip(p.key)
            return cb
        elif p.ptype == "choice":
            combo = QComboBox()
            combo.addItems(p.choices)
            idx = p.choices.index(p.default) if p.default in p.choices else 0
            combo.setCurrentIndex(idx)
            combo.setToolTip(p.key)
            return combo
        return QLabel(str(p.default))

    def _read_value(self, key):
        w = self._widgets.get(key)
        p = PARAM_BY_KEY[key]
        if p.ptype == "int":
            return w.value()
        elif p.ptype == "float":
            return w.value()
        elif p.ptype == "bool":
            return w.isChecked()
        elif p.ptype == "choice":
            return w.currentText()
        return None

    def _on_apply(self):
        errors = []
        for key, w in self._widgets.items():
            try:
                val = self._read_value(key)
                self._store.set(key, val)
            except (ValueError, KeyError) as e:
                errors.append(str(e))
        if errors:
            QMessageBox.warning(
                self, "Erreurs de validation",
                "\n".join(errors),
            )
        else:
            self.controller.sim.parameters = self._store.to_dict()
            self.parameters_applied.emit()

    def _on_reset(self):
        reply = QMessageBox.question(
            self, "Réinitialiser",
            "Réinitialiser tous les paramètres aux valeurs par défaut ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._store.reset()
            self._sync_widgets_from_store()
            self._on_apply()

    def _load_from_sim(self):
        params = getattr(self.controller.sim, "parameters", {})
        if params:
            self._store.from_dict(params)
        self._sync_widgets_from_store()

    def _sync_widgets_from_store(self):
        for key, w in self._widgets.items():
            val = self._store.get(key)
            p = PARAM_BY_KEY[key]
            if p.ptype == "int":
                w.blockSignals(True)
                w.setValue(int(val))
                w.blockSignals(False)
            elif p.ptype == "float":
                w.blockSignals(True)
                w.setValue(float(val))
                w.blockSignals(False)
            elif p.ptype == "bool":
                w.blockSignals(True)
                w.setChecked(bool(val))
                w.blockSignals(False)
            elif p.ptype == "choice":
                w.blockSignals(True)
                idx = p.choices.index(val) if val in p.choices else 0
                w.setCurrentIndex(idx)
                w.blockSignals(False)

    def refresh(self):
        self._load_from_sim()

    def get_store(self):
        return self._store
