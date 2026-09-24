"""JournalDock — dock Qt pour le journal filtrable (avancé)."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                              QTableView, QComboBox, QPushButton, QLabel,
                              QLineEdit, QFileDialog)
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtGui import QColor

from game.config import JOURNAL_MAXLEN
from game.ui_snapshots import journal_snapshot
from game.ui_registry import JOURNAL_CATEGORIES, ALL_CATEGORIES
from ..models.journal_model import JournalModel


class _JournalSortProxy(QSortFilterProxyModel):
    """Tri par valeurs brutes : ``QSortFilterProxyModel`` compare le texte
    affiché par défaut, donc « 10:00 » passerait avant « 9:00 »."""

    def lessThan(self, left, right):
        left_value = left.data(Qt.ItemDataRole.UserRole)
        right_value = right.data(Qt.ItemDataRole.UserRole)
        if left_value is None or right_value is None:
            return super().lessThan(left, right)
        try:
            return left_value < right_value
        except TypeError:
            return str(left_value) < str(right_value)


class JournalDock(QDockWidget):
    """Dock journal avec filtres par catégorie, recherche texte, export."""

    def __init__(self, controller, parent=None):
        super().__init__("Journal", parent)
        self.controller = controller
        self._model = JournalModel()
        self._proxy = _JournalSortProxy(self)
        self._proxy.setSourceModel(self._model)
        self._setup_ui()

    def _setup_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)

        # Ligne de titre : compteur + bouton repliable (Lot G)
        title_layout = QHBoxLayout()
        self._count_label = QLabel("0 entrees")
        title_layout.addWidget(self._count_label)
        title_layout.addStretch()
        # Version robuste du plan : le bouton vit dans le dock lui-meme,
        # pas dans le titleBarWidget (fragile selon les styles).
        self._expand_button = QPushButton("Déplier")
        self._expand_button.setCheckable(True)
        self._expand_button.setToolTip(
            "Déplie le journal (vue complete) ou le replie (mode compact)")
        self._expand_button.toggled.connect(self._on_expanded)
        title_layout.addWidget(self._expand_button)
        layout.addLayout(title_layout)

        # Compact par defaut : le journal ne doit pas prendre toute la fenetre.
        self.setMinimumHeight(150)
        self.setMaximumHeight(260)

        # Filtres en ligne
        filter_layout = QHBoxLayout()

        # Categorie
        self._filter_combo = QComboBox()
        self._filter_combo.addItem("All", ALL_CATEGORIES)
        for cat, meta in JOURNAL_CATEGORIES.items():
            self._filter_combo.addItem(meta["label"], cat)
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
        self._table.setModel(self._proxy)
        self._table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self._table.verticalHeader().setVisible(False)
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.setSortingEnabled(True)
        layout.addWidget(self._table)

        self.setWidget(widget)

    def filtered_entries(self, max_entries=None):
        """Source unique du filtrage catégorie + recherche (affichage/export).

        ``None`` laisse le plafond par defaut de ``journal_snapshot`` : passer
        explicitement ``None`` casserait le tranchage interne.
        """
        cat = self._filter_combo.currentData() or ALL_CATEGORIES
        search = self._search.text()
        if max_entries is None:
            return journal_snapshot(self.controller.sim, category=cat,
                                    search=search)
        return journal_snapshot(self.controller.sim, category=cat,
                                search=search, max_entries=max_entries)

    def refresh(self):
        snap = self.filtered_entries()
        self._model.set_snapshot(snap)
        self._count_label.setText(f"{len(snap)} entrees")

    def _on_expanded(self, expanded):
        """Lot G : replie (compact) ou déplie le dock journal."""
        if expanded:
            self.setMinimumHeight(420)
            self.setMaximumHeight(16777215)
            self._expand_button.setText("Replier")
        else:
            self.setMinimumHeight(150)
            self.setMaximumHeight(260)
            self._expand_button.setText("Déplier")

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

        # L'affichage est plafonné à 200 lignes ; un export doit vider tout
        # le tampon du moteur.
        snap = self.filtered_entries(max_entries=JOURNAL_MAXLEN)

        if fmt == "json":
            import json
            with open(path, "w", encoding="utf-8") as f:
                json.dump(snap, f, ensure_ascii=False, indent=2)

        elif fmt == "csv":
            # Colonnes fixes via la source unique du registre (Lot E.5).
            from game.ui_registry import export_journal_csv
            export_journal_csv(snap, path)

        elif fmt == "txt":
            with open(path, "w", encoding="utf-8") as f:
                for e in snap:
                    mm, ss = divmod(int(e.get("tick", 0) / 60), 60)
                    cat_label = e.get("category", "")
                    text = e.get("text", "")
                    cnt = e.get("count", 1)
                    suffix = f"  x{cnt}" if cnt > 1 else ""
                    f.write(f"[{mm:02}:{ss:02}] [{cat_label}] {text}{suffix}\n")
