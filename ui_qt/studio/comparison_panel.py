"""Panneau de comparaison A/B entre deux expériences."""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QFileDialog, QTextEdit,
    QSplitter, QGroupBox, QStackedWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui_qt.widgets.empty_state import EmptyState


class ComparisonPanel(QWidget):
    """Panel for comparing two experiment results side by side."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._result_a = None
        self._result_b = None
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Header
        header = QHBoxLayout()
        self._title = QLabel("Comparaison A/B")
        self._title.setStyleSheet("font-size: 14px; font-weight: bold;")
        header.addWidget(self._title)
        header.addStretch()
        
        self._load_a_btn = QPushButton("Charger A")
        self._load_a_btn.clicked.connect(lambda: self._load_result("a"))
        header.addWidget(self._load_a_btn)
        
        self._load_b_btn = QPushButton("Charger B")
        self._load_b_btn.clicked.connect(lambda: self._load_result("b"))
        header.addWidget(self._load_b_btn)
        
        layout.addLayout(header)
        
        # Labels for each experiment
        exp_layout = QHBoxLayout()
        self._label_a = QLabel("Expérience A : —")
        self._label_a.setStyleSheet("padding: 4px; background: #1a2332; border-radius: 4px;")
        exp_layout.addWidget(self._label_a)
        self._label_b = QLabel("Expérience B : —")
        self._label_b.setStyleSheet("padding: 4px; background: #1a2332; border-radius: 4px;")
        exp_layout.addWidget(self._label_b)
        layout.addLayout(exp_layout)

        # ── Lot E : vue vide tant que les deux expériences ne sont pas chargées ──
        self.empty_state = EmptyState(
            icon="⇄",
            title="Aucune comparaison",
            message="Chargez deux expériences (A et B) pour afficher le tableau comparatif.",
        )

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(6)

        # Summary text
        self._summary = QTextEdit()
        self._summary.setReadOnly(True)
        self._summary.setMaximumHeight(100)
        self._summary.setPlaceholderText("Chargez deux expériences pour les comparer...")
        content_layout.addWidget(self._summary)

        # Comparison table
        self._table = QTableWidget()
        self._table.setColumnCount(4)
        self._table.setHorizontalHeaderLabels(["Métrique", "A", "B", "Différence"])
        self._table.horizontalHeader().setStretchLastSection(True)
        content_layout.addWidget(self._table)

        # Pile vue vide / contenu (les boutons du header restent visibles)
        self._stack = QStackedWidget()
        self._stack.addWidget(self.empty_state)
        self._stack.addWidget(content)
        self._content = content
        layout.addWidget(self._stack)
        
        # Export button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        export_btn = QPushButton("Exporter")
        export_btn.clicked.connect(self._export)
        btn_layout.addWidget(export_btn)
        layout.addLayout(btn_layout)
    
    def _load_result(self, which):
        path, _ = QFileDialog.getOpenFileName(
            self, f"Charger expérience {which.upper()}",
            "", "JSON (*.json)"
        )
        if not path:
            return
        import json
        with open(path, "r", encoding="utf-8") as f:
            result = json.load(f)
        
        if which == "a":
            self._result_a = result
            self._label_a.setText(
                f"Expérience A : {result.get('scenario', '?')} "
                f"(seed {result.get('seed', '?')})"
            )
        else:
            self._result_b = result
            self._label_b.setText(
                f"Expérience B : {result.get('scenario', '?')} "
                f"(seed {result.get('seed', '?')})"
            )
        
        self._update_comparison()
    
    def _update_comparison(self):
        if not self._result_a or not self._result_b:
            # Lot E : tant que les deux expériences ne sont pas chargées,
            # la vue vide reste affichée (les libellés A/B restent visibles).
            self._stack.setCurrentWidget(self.empty_state)
            return

        # Lot E : comparaison possible -> page contenu.
        self._stack.setCurrentWidget(self._content)

        from game.studio_compare import compare_results, compare_summary
        
        rows = compare_results(self._result_a, self._result_b)
        summary = compare_summary(self._result_a, self._result_b)
        
        self._summary.setText(summary)
        
        self._table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self._table.setItem(i, 0, QTableWidgetItem(row["label"]))
            self._table.setItem(i, 1, QTableWidgetItem(f"{row['a']:.2f}"))
            self._table.setItem(i, 2, QTableWidgetItem(f"{row['b']:.2f}"))
            diff_item = QTableWidgetItem(f"{row['difference']:+.2f}")
            if row["difference"] > 0:
                diff_item.setForeground(Qt.GlobalColor.green)
            elif row["difference"] < 0:
                diff_item.setForeground(Qt.GlobalColor.red)
            self._table.setItem(i, 3, diff_item)
    
    def _export(self):
        if not self._result_a or not self._result_b:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Exporter comparaison", "comparison.json", "JSON (*.json)"
        )
        if path:
            from game.studio_compare import compare_results, compare_summary
            data = {
                "a": self._result_a,
                "b": self._result_b,
                "rows": compare_results(self._result_a, self._result_b),
                "summary": compare_summary(self._result_a, self._result_b),
            }
            import json
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
