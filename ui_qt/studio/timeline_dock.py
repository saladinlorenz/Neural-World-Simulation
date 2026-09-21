"""TimelineDock — dock Qt pour la chronologie des événements."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                              QTableWidget, QTableWidgetItem, QLineEdit,
                              QComboBox, QPushButton, QFileDialog, QLabel,
                              QHeaderView, QAbstractItemView)
from PyQt6.QtCore import Qt

from game.studio_timeline import (
    build_timeline, filter_events, format_event, CATEGORIES,
)
from game.ui_snapshots import journal_snapshot


class TimelineDock(QDockWidget):
    """Dock chronologie avec filtres et export."""

    def __init__(self, controller, parent=None):
        super().__init__("Chronologie", parent)
        self.controller = controller
        self._events = []
        self._setup_ui()

    def _setup_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)

        # Barre de filtres
        filter_layout = QHBoxLayout()

        self._cat_combo = QComboBox()
        self._cat_combo.addItems(CATEGORIES)
        self._cat_combo.currentTextChanged.connect(self._apply_filter)
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
        self._table.verticalHeader().setVisible(False)
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
        cat = self._cat_combo.currentText()
        text = self._search.text().strip().lower()
        filtered = filter_events(self._events, category=cat)
        if text:
            filtered = [
                e for e in filtered
                if text in format_event(e).lower()
            ]
        self._populate_table(filtered)

    def _populate_table(self, events):
        self._table.setRowCount(len(events))
        for i, ev in enumerate(events):
            tick = ev.get("tick", 0)
            day = tick // 100 + 1
            hour = tick % 100
            day_item = QTableWidgetItem(f"J{day} — {hour:02d}h")
            day_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self._table.setItem(i, 0, day_item)

            cat_item = QTableWidgetItem(ev.get("category", ""))
            cat_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self._table.setItem(i, 1, cat_item)

            sentence = format_event(ev)
            self._table.setItem(i, 2, QTableWidgetItem(sentence))
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
