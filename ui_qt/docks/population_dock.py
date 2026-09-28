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
        self._last_revision = -1
        self._last_filter_signature = ""
        self._refresh_timer = None
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
        self._search.textChanged.connect(self._on_search_changed)
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

        # Un dock réaffiché repart d'un instantané frais : des habitants
        # ont pu mourir pendant qu'il était caché, et le modèle ne doit
        # jamais conserver de lignes « vivantes » périmées.
        self.visibilityChanged.connect(
            lambda visible: self.refresh() if visible else None)

        # Periodic refresh during simulation (every 30 ticks max)
        self._refresh_timer = None
        self._start_periodic_refresh()

        # Bouton Supprimer
        self._remove_btn = QPushButton("Supprimer")
        self._remove_btn.setEnabled(False)
        self._remove_btn.setStyleSheet(
            "QPushButton { background-color: #c0392b; color: white; "
            "padding: 4px 12px; border: none; border-radius: 3px; }"
            "QPushButton:hover { background-color: #e74c3c; }"
            # Désactivé : fond clair + texte sombre (contraste ~5:1), au lieu
            # de #7f8c8d/#bdc3c7 (~2:1) qui rendait « Supprimer » illisible.
            "QPushButton:disabled { background-color: #bdc3c7; color: #34495e; }"
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
        stage_filter = self._stage_filter.currentData() or ""
        search_text = (self._search.text() or "").strip().lower()
        filter_signature = f"{include_dead}|{stage_filter}|{search_text}"

        sim = self.controller.sim
        revision = getattr(sim, 'population_revision', -1)

        # Skip refresh if revision and filters unchanged and not forced
        if (revision == self._last_revision and
            filter_signature == self._last_filter_signature and
            self._last_revision != -1):
            return

        self._last_revision = revision
        self._last_filter_signature = filter_signature

        snap = population_snapshot(sim, include_dead=include_dead)
        portraits = {}
        try:
            am = sim.am
            for row in snap:
                eid = row.get("eid")
                if eid is None:
                    continue
                try:
                    portraits[eid] = pil_to_pixmap(am.avatar(int(eid), size=24))
                except Exception:
                    pass
        except Exception:
            pass
        self._model.set_snapshot(snap, portraits, revision=revision, filter_signature=filter_signature)
        alive = sum(1 for row in snap if row.get("alive", True))
        if include_dead:
            self._count_label.setText(f"{alive} vivants / {len(snap)} au total")
        else:
            self._count_label.setText(f"{len(snap)} habitants")
        self._proxy.invalidateFilter()

    def _on_stage_changed(self, *_args):
        self._proxy.set_stage(self._stage_filter.currentData() or "")
        self.refresh()

    def _on_alive_changed(self, *_args):
        # « Vivants/Tous » change le jeu de données, pas seulement le filtre.
        self.refresh()

    def _on_search_changed(self):
        self._proxy.set_search(self._search.text())
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
            result = self.controller.execute({"kind": "remove_agent", "eid": eid})
            if not result.get("ok", False):
                error = result.get("error", "Erreur inconnue")
                QMessageBox.warning(
                    self,
                    "Échec de la suppression",
                    f"Impossible de supprimer l'habitant : {error}",
                    QMessageBox.StandardButton.Ok,
                )

    def _start_periodic_refresh(self):
        """Start periodic refresh timer (every ~500ms = ~30 ticks at 60 TPS)."""
        if self._refresh_timer is not None:
            return
        from PyQt6.QtCore import QTimer
        self._refresh_timer = QTimer(self)
        self._refresh_timer.setInterval(500)  # ~500ms
        self._refresh_timer.timeout.connect(self._periodic_refresh)
        self._refresh_timer.start()

    def _periodic_refresh(self):
        """Periodic refresh during simulation - only if revision changed."""
        sim = self.controller.sim
        revision = getattr(sim, 'population_revision', -1)
        if revision != self._last_revision:
            self.refresh()
