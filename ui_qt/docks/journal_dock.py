"""JournalDock — dock Qt pour le journal filtrable (avancé)."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                              QTableView, QComboBox, QPushButton, QLabel,
                              QLineEdit, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from game.config import JOURNAL_MAXLEN
from game.ui_snapshots import journal_snapshot
from game.ui_registry import LOG_TITLES
from ..models.journal_model import JournalModel


class JournalDock(QDockWidget):
    """Dock journal avec filtres par catégorie, recherche texte, export."""

    def __init__(self, controller, parent=None):
        super().__init__("Journal", parent)
        self.controller = controller
        self._model = JournalModel()
        self._setup_ui()

    def _setup_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)

        # Compteur
        self._count_label = QLabel("0 entrees")
        layout.addWidget(self._count_label)

        # Filtres en ligne
        filter_layout = QHBoxLayout()

        # Categorie
        self._filter_combo = QComboBox()
        self._filter_combo.addItem("Tous", "tous")
        for cat, title in LOG_TITLES.items():
            self._filter_combo.addItem(title, cat)
        self._filter_combo.currentIndexChanged.connect(self._on_filter)
        filter_layout.addWidget(QLabel("Categorie:"))
        filter_layout.addWidget(self._filter_combo)

        # Recherche texte
        self._search = QLineEdit()
        self._search.setPlaceholderText("Rechercher dans le journal...")
        self._search.textChanged.connect(self._on_filter)
        filter_layout.addWidget(self._search)

        layout.addLayout(filter_layout)

        # Boutons d'action
        btn_layout = QHBoxLayout()

        export_json = QPushButton("Exporter JSON")
        export_json.clicked.connect(lambda: self._export("json"))
        btn_layout.addWidget(export_json)

        export_csv = QPushButton("Exporter CSV")
        export_csv.clicked.connect(lambda: self._export("csv"))
        btn_layout.addWidget(export_csv)

        export_txt = QPushButton("Exporter TXT")
        export_txt.clicked.connect(lambda: self._export("txt"))
        btn_layout.addWidget(export_txt)

        layout.addLayout(btn_layout)

        # Tableau
        self._table = QTableView()
        self._table.setModel(self._model)
        self._table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self._table.verticalHeader().setVisible(False)
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.setSortingEnabled(True)
        layout.addWidget(self._table)

        self.setWidget(widget)

    def refresh(self):
        cat = self._filter_combo.currentData() or "tous"
        search = self._search.text()
        snap = journal_snapshot(self.controller.sim, category=cat, search=search)
        self._model.set_snapshot(snap)
        self._count_label.setText(f"{len(snap)} entrees")

    def _on_filter(self):
        self.refresh()

    def _export(self, fmt):
        path, _ = QFileDialog.getSaveFileName(
            self, "Exporter le journal",
            f"journal.{fmt}",
            f"{fmt.upper()} (*.{fmt})"
        )
        if not path:
            return

        cat = self._filter_combo.currentData() or "tous"
        search = self._search.text()
        # L'affichage est plafonné à 200 lignes ; un export doit vider tout
        # le tampon du moteur.
        snap = journal_snapshot(self.controller.sim, category=cat, search=search,
                                max_entries=JOURNAL_MAXLEN)

        if fmt == "json":
            import json
            with open(path, "w", encoding="utf-8") as f:
                json.dump(snap, f, ensure_ascii=False, indent=2)

        elif fmt == "csv":
            import csv
            # Les colonnes sont dérivées des lignes réelles : une liste figée
            # faisait lever ValueError dès qu'une clé supplémentaire
            # (``color``) apparaissait dans le snapshot.
            fieldnames = []
            for entry in snap:
                for key in entry:
                    if key not in fieldnames:
                        fieldnames.append(key)
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames or ["tick"])
                writer.writeheader()
                writer.writerows(snap)

        elif fmt == "txt":
            with open(path, "w", encoding="utf-8") as f:
                for e in snap:
                    mm, ss = divmod(int(e.get("tick", 0) / 60), 60)
                    cat_label = e.get("category", "")
                    text = e.get("text", "")
                    cnt = e.get("count", 1)
                    suffix = f"  x{cnt}" if cnt > 1 else ""
                    f.write(f"[{mm:02}:{ss:02}] [{cat_label}] {text}{suffix}\n")
