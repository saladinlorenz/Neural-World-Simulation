"""PopulationDock — dock Qt pour la liste des habitants (avancé)."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                              QTableView, QLineEdit, QComboBox, QLabel,
                              QPushButton, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QSortFilterProxyModel
from PyQt6.QtGui import QColor

from game.ui_snapshots import population_snapshot
from ui_qt.qtimage import pil_to_pixmap
from ..models.population_model import PopulationModel


class _PopulationProxy(QSortFilterProxyModel):
    """Filtre combiné : stade d'âge + recherche texte + vivants/tous.

    Un seul ``QSortFilterProxyModel`` standard ne peut porter qu'une chaîne
    de filtre : le stade et la recherche se marchaient dessus.
    """

    _SEARCH_COLUMNS = (1, 2, 7, 8)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._search = ""
        self._stage = ""
        self.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

    def set_search(self, text):
        self._search = (text or "").strip().lower()
        self.invalidateFilter()

    def set_stage(self, stage):
        self._stage = stage or ""
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        model = self.sourceModel()
        if model is None:
            return True
        if self._stage:
            index = model.index(source_row, 8, source_parent)
            if str(model.data(index, Qt.ItemDataRole.DisplayRole) or "") != self._stage:
                return False
        if self._search:
            for col in self._SEARCH_COLUMNS:
                index = model.index(source_row, col, source_parent)
                value = str(model.data(index, Qt.ItemDataRole.DisplayRole) or "")
                if self._search in value.lower():
                    return True
            return False
        return True


class PopulationDock(QDockWidget):
    """Dock de la population avec tableau triable et filtrable."""

    agent_selected = pyqtSignal(int)

    def __init__(self, controller, parent=None):
        super().__init__("Habitants", parent)
        self.controller = controller
        self._model = PopulationModel()
        self._proxy = _PopulationProxy()
        self._proxy.setSourceModel(self._model)
        self._setup_ui()

    def _setup_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)

        # Compteur
        self._count_label = QLabel("0 habitants")
        layout.addWidget(self._count_label)

        # Recherche
        search_layout = QHBoxLayout()
        self._search = QLineEdit()
        self._search.setPlaceholderText("Filtrer par nom, clan, classe...")
        self._search.textChanged.connect(self._proxy.set_search)
        search_layout.addWidget(self._search)

        clear_btn = QPushButton("X")
        clear_btn.setFixedWidth(24)
        clear_btn.clicked.connect(self._search.clear)
        search_layout.addWidget(clear_btn)
        layout.addLayout(search_layout)

        # Filtres
        filter_layout = QHBoxLayout()

        self._stage_filter = QComboBox()
        self._stage_filter.addItem("Tous les stades", "")
        for stage in ("enfant", "adulte", "ancien"):
            self._stage_filter.addItem(stage, stage)
        self._stage_filter.currentIndexChanged.connect(self._on_stage_changed)
        filter_layout.addWidget(QLabel("Age:"))
        filter_layout.addWidget(self._stage_filter)

        self._alive_filter = QComboBox()
        self._alive_filter.addItem("Vivants", "alive")
        self._alive_filter.addItem("Tous", "all")
        self._alive_filter.currentIndexChanged.connect(self._on_alive_changed)
        filter_layout.addWidget(self._alive_filter)

        layout.addLayout(filter_layout)

        # Bouton Supprimer
        self._remove_btn = QPushButton("Supprimer")
        self._remove_btn.setEnabled(False)
        self._remove_btn.setStyleSheet(
            "QPushButton { background-color: #c0392b; color: white; "
            "padding: 4px 12px; border: none; border-radius: 3px; }"
            "QPushButton:hover { background-color: #e74c3c; }"
            "QPushButton:disabled { background-color: #7f8c8d; color: #bdc3c7; }"
        )
        self._remove_btn.clicked.connect(self._on_remove)
        layout.addWidget(self._remove_btn)

        # Tableau
        self._table = QTableView()
        self._table.setModel(self._proxy)
        self._table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self._table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self._table.setSortingEnabled(True)
        self._table.verticalHeader().setVisible(False)
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.clicked.connect(self._on_click)
        self._table.selectionModel().selectionChanged.connect(self._on_selection_changed)
        layout.addWidget(self._table)

        self.setWidget(widget)

    def refresh(self):
        include_dead = (self._alive_filter.currentData() or "alive") == "all"
        snap = population_snapshot(self.controller.sim, include_dead=include_dead)
        portraits = {}
        try:
            am = self.controller.sim.am
            for row in snap:
                eid = row.get("eid")
                if eid is None:
                    continue
                try:
                    # ``avatar`` renvoie une image PIL : Qt ne sait pas la
                    # dessiner via DecorationRole, la conversion est obligatoire.
                    portraits[eid] = pil_to_pixmap(am.avatar(int(eid), size=24))
                except Exception:
                    pass
        except Exception:
            pass
        self._model.set_snapshot(snap, portraits)
        alive = sum(1 for row in snap if row.get("vivant", True))
        if include_dead:
            self._count_label.setText(f"{alive} vivants / {len(snap)} au total")
        else:
            self._count_label.setText(f"{len(snap)} habitants")
        self._proxy.invalidateFilter()

    def _on_stage_changed(self, *_args):
        self._proxy.set_stage(self._stage_filter.currentData() or "")

    def _on_alive_changed(self, *_args):
        # « Vivants/Tous » change le jeu de données, pas seulement le filtre.
        self.refresh()

    def _selected_eid(self):
        indexes = self._table.selectionModel().selectedRows()
        if not indexes:
            return None
        source_index = self._proxy.mapToSource(indexes[0])
        return self._model.eid_at(source_index.row())

    def _on_selection_changed(self):
        eid = self._selected_eid()
        self._remove_btn.setEnabled(eid is not None)

    def _on_click(self, index):
        source_index = self._proxy.mapToSource(index)
        eid = self._model.eid_at(source_index.row())
        if eid is not None:
            self.controller.execute({"kind": "select_agent", "eid": eid})
            self.agent_selected.emit(eid)

    def _on_remove(self):
        eid = self._selected_eid()
        if eid is None:
            return
        agent = next(
            (a for a in self.controller.sim.agents if a.eid == eid and a.alive),
            None,
        )
        if agent is None:
            return
        reply = QMessageBox.question(
            self,
            "Supprimer un habitant",
            f"Supprimer {agent.name} ? Cette action est irréversible.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.controller.execute({"kind": "remove_agent", "eid": eid})
            self.refresh()
