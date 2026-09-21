"""SocietyDock — dock Qt pour les stats de société."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                              QTableView, QTableWidget, QTableWidgetItem,
                              QLabel, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from game.ui_snapshots import society_snapshot
from ui_qt.models.society_model import SocietyModel


class SocietyDock(QDockWidget):
    """Dock société avec stats démographiques et sociales."""

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

        self.setWidget(widget)

    def refresh(self):
        snap = society_snapshot(self.controller.sim)
        self._model.set_snapshot(snap)
        self._populate_relations(snap.get("relations", []))

    def _populate_relations(self, relations):
        self._relations_table.setRowCount(len(relations))
        for row, rel in enumerate(relations):
            self._relations_table.setItem(row, 0, QTableWidgetItem(rel["name1"]))
            self._relations_table.setItem(row, 1, QTableWidgetItem(rel["name2"]))
            self._relations_table.setItem(row, 2, QTableWidgetItem(rel["type"]))
            self._relations_table.setItem(
                row, 3, QTableWidgetItem(f'{rel["confiance"]:+.2f}')
            )
            self._relations_table.setItem(
                row, 4, QTableWidgetItem(f'{rel["affinite"]:+.2f}')
            )
