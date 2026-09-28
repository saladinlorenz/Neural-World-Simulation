"""TimelineDock — dock Qt pour la chronologie des événements."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                              QTableWidget, QTableWidgetItem, QLineEdit,
                              QComboBox, QPushButton, QFileDialog, QLabel,
                              QHeaderView, QAbstractItemView, QSpinBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from game.studio_timeline import build_timeline, filter_events, format_event
from game.ui_registry import JOURNAL_CATEGORIES, ALL_CATEGORIES
from game.ui_snapshots import journal_snapshot


class TimelineDock(QDockWidget):
    """Dock chronologie avec filtres et export."""

    def __init__(self, controller, parent=None, on_event=None):
        super().__init__("Chronologie", parent)
        self.controller = controller
        #: Callback optionnel (event -> None) branchable par main_window.
        self.on_event = on_event
        self._events = []
        self._visible = []
        self._setup_ui()

    def _setup_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)

        # Barre de filtres
        filter_layout = QHBoxLayout()

        self._cat_combo = QComboBox()
        # Même registre que le dock Journal (ids EN, libellés du registre).
        self._cat_combo.addItem("All", ALL_CATEGORIES)
        for cat, meta in JOURNAL_CATEGORIES.items():
            self._cat_combo.addItem(meta["label"], cat)
        self._cat_combo.currentIndexChanged.connect(self._apply_filter)
        filter_layout.addWidget(QLabel("Catégorie:"))
        filter_layout.addWidget(self._cat_combo)

        self._search = QLineEdit()
        self._search.setPlaceholderText("Rechercher...")
        self._search.returnPressed.connect(self._apply_filter)
        filter_layout.addWidget(self._search)

        search_btn = QPushButton("Filtrer")
        search_btn.clicked.connect(self._apply_filter)
        filter_layout.addWidget(search_btn)

        layout.addLayout(filter_layout)

        # Ligne 2 : fourchette de ticks + importance (déclenchée par « Filtrer »)
        range_layout = QHBoxLayout()

        range_layout.addWidget(QLabel("Tick début:"))
        self._min_tick = QSpinBox()
        self._min_tick.setRange(0, 10_000_000)
        self._min_tick.setToolTip("Tick de départ du filtre (0 = début)")
        range_layout.addWidget(self._min_tick)

        range_layout.addWidget(QLabel("Tick fin:"))
        self._max_tick = QSpinBox()
        self._max_tick.setRange(0, 10_000_000)
        self._max_tick.setToolTip("Tick de fin du filtre (0 = illimité)")
        range_layout.addWidget(self._max_tick)

        range_layout.addWidget(QLabel("Importance:"))
        self._importance = QSpinBox()
        self._importance.setRange(0, 5)
        self._importance.setValue(0)
        self._importance.setToolTip("Importance minimale (0 = toutes)")
        range_layout.addWidget(self._importance)

        reset_btn = QPushButton("Réinitialiser")
        reset_btn.clicked.connect(self._reset_filters)
        range_layout.addStretch()
        range_layout.addWidget(reset_btn)

        layout.addLayout(range_layout)

        # Compteur
        self._count_label = QLabel("0 événements")
        layout.addWidget(self._count_label)

        # Tableau
        self._table = QTableWidget()
        self._table.setColumnCount(3)
        self._table.setHorizontalHeaderLabels(["Jour", "Catégorie", "Événement"])
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self._table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self._table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self._table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._table.setSortingEnabled(False)
        self._table.verticalHeader().setVisible(False)
        self._table.cellDoubleClicked.connect(self._on_row_double_clicked)
        layout.addWidget(self._table)

        # Export
        export_layout = QHBoxLayout()
        export_layout.addStretch()
        self._export_btn = QPushButton("Exporter...")
        self._export_btn.clicked.connect(self._on_export)
        export_layout.addWidget(self._export_btn)
        layout.addLayout(export_layout)

        self.setWidget(widget)

    def refresh(self):
        snap = journal_snapshot(self.controller.sim)
        self._events = build_timeline(snap)
        self._apply_filter()

    def _apply_filter(self):
        cat = self._cat_combo.currentData() or ALL_CATEGORIES
        text = self._search.text().strip().lower()
        # 0 = « illimité » sur les deux bornes (état réinitialisable).
        min_tick = self._min_tick.value() or None
        max_tick = self._max_tick.value() or None
        filtered = filter_events(self._events, category=cat,
                                 min_tick=min_tick, max_tick=max_tick)
        if text:
            filtered = [
                e for e in filtered
                if text in format_event(e).lower()
            ]
        # filter_events ne gère pas l'importance → filtrage côté client.
        min_imp = self._importance.value()
        if min_imp > 0:
            filtered = [
                e for e in filtered
                if float(e.get("importance", 0.0) or 0.0) >= min_imp
            ]
        self._populate_table(filtered)

    def _reset_filters(self):
        """Remet tous les filtres à leur état initial puis rafraîchit."""
        self._cat_combo.blockSignals(True)
        self._cat_combo.setCurrentIndex(0)
        self._cat_combo.blockSignals(False)
        self._search.clear()
        self._min_tick.setValue(0)
        self._max_tick.setValue(0)
        self._importance.setValue(0)
        self._apply_filter()

    def _on_row_double_clicked(self, row, column):
        """Double-clic : sélection de l'agent/lieu de l'événement, sans plantage."""
        if row < 0 or row >= len(self._visible):
            return
        ev = self._visible[row]
        if self.on_event is not None:
            try:
                self.on_event(ev)
            except Exception:
                pass
            return
        controller = getattr(self, "controller", None)
        if controller is None or not hasattr(controller, "execute"):
            return
        try:
            actors = list(ev.get("actors") or [])
            if actors:
                controller.execute({"kind": "select_agent", "eid": int(actors[0])})
                return
            place = ev.get("place")
            if isinstance(place, (tuple, list)) and len(place) >= 2:
                controller.execute({"kind": "select_tile",
                                    "tx": int(place[0]), "ty": int(place[1])})
        except Exception:
            return

    def _populate_table(self, events):
        self._visible = list(events)
        self._table.setRowCount(len(events))
        for i, ev in enumerate(events):
            tick = ev.get("tick", 0)
            day = tick // 100 + 1
            hour = tick % 100
            day_item = QTableWidgetItem(f"J{day} — {hour:02d}h (t={tick})")
            day_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self._table.setItem(i, 0, day_item)

            cat_id = ev.get("category", "")
            meta = JOURNAL_CATEGORIES.get(cat_id, {})
            label = meta.get("label", cat_id)
            count = int(ev.get("count", 1) or 1)
            if count > 1:
                label = f"{label} ×{count}"
            cat_item = QTableWidgetItem(label)
            cat_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            color = meta.get("color")
            if color:
                cat_item.setForeground(QColor(color))
            self._table.setItem(i, 1, cat_item)

            sentence_item = QTableWidgetItem(format_event(ev))
            if color and i % 2 == 1:
                # Bande subtile : fond à 12 % de la couleur de catégorie.
                tint = QColor(color)
                tint.setAlpha(31)
                sentence_item.setBackground(tint)
            self._table.setItem(i, 2, sentence_item)
        self._count_label.setText(f"{len(events)} événement{'s' if len(events) != 1 else ''}")

    def _on_export(self):
        path, fmt = QFileDialog.getSaveFileName(
            self, "Exporter la chronologie",
            "timeline.txt",
            "Fichier texte (*.txt);;CSV (*.csv);;JSON (*.json)",
        )
        if not path:
            return
        if fmt.startswith("JSON"):
            self._export_json(path)
        elif fmt.startswith("CSV"):
            self._export_csv(path)
        else:
            self._export_txt(path)

    def _export_txt(self, path):
        with open(path, "w", encoding="utf-8") as f:
            for ev in self._events:
                f.write(format_event(ev) + "\n")

    def _export_csv(self, path):
        import csv
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Jour", "Heure", "Catégorie", "Événement"])
            for ev in self._events:
                tick = ev.get("tick", 0)
                w.writerow([
                    tick // 100 + 1,
                    f"{tick % 100:02d}",
                    ev.get("category", ""),
                    format_event(ev),
                ])

    def _export_json(self, path):
        import json
        data = []
        for ev in self._events:
            tick = ev.get("tick", 0)
            data.append({
                "day": tick // 100 + 1,
                "hour": tick % 100,
                "category": ev.get("category", ""),
                "kind": ev.get("kind", ""),
                "title": ev.get("title", ""),
                "text": ev.get("text", ""),
                "actors": ev.get("actors", []),
                "importance": ev.get("importance", 0.0),
            })
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
