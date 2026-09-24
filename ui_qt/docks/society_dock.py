"""SocietyDock — dock Qt pour les stats de société."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                              QTableView, QTableWidget, QTableWidgetItem,
                              QLabel, QHeaderView)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor

from game.ui_snapshots import society_snapshot
from ui_qt.models.society_model import SocietyModel
from ui_qt.widgets.population_history_widget import PopulationHistoryWidget


class SocietyDock(QDockWidget):
    """Dock société avec stats démographiques et sociales."""

    agent_selected = pyqtSignal(int)

    def __init__(self, controller, parent=None):
        super().__init__("Societe", parent)
        self.controller = controller
        self._model = SocietyModel()
        self._setup_ui()

    def _setup_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)

        self._table = QTableView()
        self._table.setModel(self._model)
        self._table.verticalHeader().setVisible(False)
        self._table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self._table)

        # Historique de population (Lot E.3)
        layout.addWidget(QLabel("Historique de population"))
        self._population_history = PopulationHistoryWidget()
        layout.addWidget(self._population_history)

        # Institutions emergentes (Lot E.3)
        layout.addWidget(QLabel("Institutions"))
        self._institutions_table = QTableWidget()
        self._institutions_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers)
        self._institutions_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows)
        self._institutions_table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection)
        self._institutions_table.verticalHeader().setVisible(False)
        self._institutions_table.setAlternatingRowColors(True)
        self._institutions_table.setColumnCount(5)
        self._institutions_table.setHorizontalHeaderLabels(
            ["Type", "Membres", "Stabilite", "Confiance", "Age"]
        )
        inst_header = self._institutions_table.horizontalHeader()
        inst_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for col in (1, 2, 3, 4):
            inst_header.setSectionResizeMode(
                col, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self._institutions_table)

        # Section Relations
        layout.addWidget(QLabel("Relations"))
        self._relations_table = QTableWidget()
        self._relations_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._relations_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._relations_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self._relations_table.verticalHeader().setVisible(False)
        self._relations_table.horizontalHeader().setStretchLastSection(True)
        self._relations_table.setAlternatingRowColors(True)
        self._relations_table.setRowCount(0)
        self._relations_table.setColumnCount(5)
        self._relations_table.setHorizontalHeaderLabels(
            ["Agent 1", "Agent 2", "Type", "Confiance", "Affinité"]
        )
        header = self._relations_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self._relations_table)
        self._relations_table.cellClicked.connect(self._on_relation_clicked)

        self.setWidget(widget)

    def refresh(self):
        snap = society_snapshot(self.controller.sim)
        self._model.set_snapshot(snap)
        self._population_history.set_values(
            snap.get("population_history", []))
        self._populate_institutions(snap.get("institutions", []))
        self._populate_relations(snap.get("relations", []))

    def _populate_institutions(self, institutions):
        self._institutions_table.setRowCount(len(institutions))
        for row, inst in enumerate(institutions):
            self._institutions_table.setItem(
                row, 0, QTableWidgetItem(str(inst.get("kind", ""))))
            self._institutions_table.setItem(
                row, 1, QTableWidgetItem(str(len(inst.get("members", [])))))
            self._institutions_table.setItem(
                row, 2, QTableWidgetItem(f'{inst.get("stability", 0.0):.2f}'))
            self._institutions_table.setItem(
                row, 3, QTableWidgetItem(f'{inst.get("trust", 0.0):.2f}'))
            self._institutions_table.setItem(
                row, 4, QTableWidgetItem(str(inst.get("age", 0))))

    def _populate_relations(self, relations):
        self._relations_table.setRowCount(len(relations))
        for row, rel in enumerate(relations):
            item1 = QTableWidgetItem(rel["name1"])
            item1.setData(Qt.ItemDataRole.UserRole, int(rel.get("eid1", -1)))
            self._relations_table.setItem(row, 0, item1)
            self._relations_table.setItem(row, 1, QTableWidgetItem(rel["name2"]))
            self._relations_table.setItem(row, 2, QTableWidgetItem(rel["type"]))
            self._relations_table.setItem(
                row, 3, QTableWidgetItem(f'{rel["confiance"]:+.2f}')
            )
            self._relations_table.setItem(
                row, 4, QTableWidgetItem(f'{rel["affinite"]:+.2f}')
            )

    def _on_relation_clicked(self, row, _column):
        item = self._relations_table.item(row, 0)
        if item is None:
            return
        eid = item.data(Qt.ItemDataRole.UserRole)
        if eid is None or int(eid) < 0:
            return
        self.controller.execute({"kind": "select_agent", "eid": int(eid)})
        self.agent_selected.emit(int(eid))
