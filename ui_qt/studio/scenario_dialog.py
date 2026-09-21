"""ScenarioDialog — QDialog pour choisir et lancer un scénario."""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                              QListWidget, QListWidgetItem, QPushButton,
                              QTextEdit, QGroupBox, QGridLayout)
from PyQt6.QtCore import Qt

from game.studio_scenarios import (
    list_scenarios, get_scenario, apply_scenario, scenario_summary,
)
from game.studio_parameters import PARAM_BY_KEY


class ScenarioDialog(QDialog):
    """Fenêtre de sélection et lancement de scénarios."""

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Scénarios de simulation")
        self.setMinimumSize(640, 480)
        self._selected_key = None
        self._setup_ui()
        self._populate_list()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(12)

        # Colonne gauche : liste
        left = QVBoxLayout()
        left.addWidget(QLabel("Scénarios disponibles"))
        self._list = QListWidget()
        self._list.currentRowChanged.connect(self._on_select)
        left.addWidget(self._list)
        layout.addLayout(left, 2)

        # Colonne droite : détails
        right = QVBoxLayout()

        self._title_label = QLabel()
        self._title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        right.addWidget(self._title_label)

        self._desc_label = QLabel()
        self._desc_label.setWordWrap(True)
        right.addWidget(self._desc_label)

        info_group = QGroupBox("Détails")
        info_grid = QGridLayout()
        info_grid.addWidget(QLabel("Durée recommandée:"), 0, 0)
        self._duration_label = QLabel()
        info_grid.addWidget(self._duration_label, 0, 1)
        info_group.setLayout(info_grid)
        right.addWidget(info_group)

        self._summary_box = QTextEdit()
        self._summary_box.setReadOnly(True)
        self._summary_box.setMaximumHeight(120)
        right.addWidget(QLabel("Résumé"))
        right.addWidget(self._summary_box)

        self._params_box = QGroupBox("Paramètres appliqués")
        self._params_grid = QGridLayout()
        self._params_grid.setSpacing(4)
        self._params_box.setLayout(self._params_grid)
        right.addWidget(self._params_box)

        right.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self._cancel_btn = QPushButton("Annuler")
        self._cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self._cancel_btn)
        self._launch_btn = QPushButton("Lancer")
        self._launch_btn.setEnabled(False)
        self._launch_btn.setStyleSheet(
            "QPushButton { background-color: #27ae60; color: white; "
            "padding: 6px 18px; border: none; border-radius: 3px; }"
            "QPushButton:hover { background-color: #2ecc71; }"
            "QPushButton:disabled { background-color: #7f8c8d; color: #bdc3c7; }"
        )
        self._launch_btn.clicked.connect(self._on_launch)
        btn_layout.addWidget(self._launch_btn)
        right.addLayout(btn_layout)

        layout.addLayout(right, 3)

    def _populate_list(self):
        self._list.clear()
        for key, label, desc in list_scenarios():
            item = QListWidgetItem(label)
            item.setData(Qt.ItemDataRole.UserRole, key)
            item.setToolTip(desc)
            self._list.addItem(item)

    def _on_select(self, row):
        item = self._list.item(row)
        if not item:
            return
        key = item.data(Qt.ItemDataRole.UserRole)
        self._selected_key = key
        scenario = get_scenario(key)
        if not scenario:
            return
        self._title_label.setText(scenario["label"])
        self._desc_label.setText(scenario["description"])
        self._duration_label.setText(f"{scenario['duration_recommended']} ticks")
        self._summary_box.setPlainText(scenario_summary(key))

        # Afficher les paramètres
        while self._params_grid.count():
            w = self._params_grid.takeAt(0).widget()
            if w:
                w.deleteLater()
        row_idx = 0
        for pkey, pval in scenario["parameters"].items():
            pdef = PARAM_BY_KEY.get(pkey)
            label = pdef.label if pdef else pkey
            self._params_grid.addWidget(QLabel(label), row_idx, 0)
            self._params_grid.addWidget(QLabel(str(pval)), row_idx, 1)
            row_idx += 1
        self._launch_btn.setEnabled(True)

    def _on_launch(self):
        if not self._selected_key:
            return
        try:
            store = self.controller.sim.parameter_store
        except AttributeError:
            from game.studio_parameters import ParameterStore
            store = ParameterStore()
            self.controller.sim.parameter_store = store
        apply_scenario(store, self._selected_key)
        self.controller.sim.parameters = store.to_dict()
        self.accept()

    def get_selected_scenario(self):
        return self._selected_key
