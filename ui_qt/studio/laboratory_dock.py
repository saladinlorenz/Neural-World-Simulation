"""LaboratoryDock — dock Qt pour les résultats d'expérience."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                               QTextEdit, QTableWidget, QTableWidgetItem,
                               QPushButton, QGroupBox, QFileDialog,
                               QScrollArea, QHeaderView)
from PyQt6.QtCore import Qt

from game.studio_reports import build_report, build_short_summary, interpret_metric
from game.studio_compare import KEYS


class LaboratoryDock(QDockWidget):
    """Dock du laboratoire : résumé, métriques, interprétation, scénario."""

    def __init__(self, controller, parent=None):
        super().__init__("Laboratoire", parent)
        self.controller = controller
        self._result = None
        self._setup_ui()

    def _setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        widget = QWidget()
        self._layout = QVBoxLayout(widget)
        self._layout.setContentsMargins(8, 8, 8, 8)
        self._layout.setSpacing(6)

        # Résumé
        summary_group = QGroupBox("Résumé")
        summary_group.setStyleSheet("QGroupBox { font-weight: bold; color: #3e7cd6; }")
        summary_layout = QVBoxLayout(summary_group)
        summary_layout.setContentsMargins(8, 16, 8, 8)
        self._summary_text = QTextEdit()
        self._summary_text.setReadOnly(True)
        self._summary_text.setMaximumHeight(120)
        self._summary_text.setStyleSheet("font-size: 12px; color: #c8d0da;")
        summary_layout.addWidget(self._summary_text)
        self._layout.addWidget(summary_group)

        # Métriques
        metrics_group = QGroupBox("Métriques")
        metrics_group.setStyleSheet("QGroupBox { font-weight: bold; color: #54b96b; }")
        metrics_layout = QVBoxLayout(metrics_group)
        metrics_layout.setContentsMargins(8, 16, 8, 8)
        self._metrics_table = QTableWidget()
        self._metrics_table.setColumnCount(2)
        self._metrics_table.setHorizontalHeaderLabels(["Métrique", "Valeur"])
        self._metrics_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self._metrics_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        self._metrics_table.verticalHeader().setVisible(False)
        self._metrics_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._metrics_table.setStyleSheet(
            "QTableWidget { font-size: 11px; color: #c8d0da; }"
        )
        metrics_layout.addWidget(self._metrics_table)
        self._layout.addWidget(metrics_group)

        # Interprétation
        interp_group = QGroupBox("Interprétation")
        interp_group.setStyleSheet("QGroupBox { font-weight: bold; color: #e2b44a; }")
        interp_layout = QVBoxLayout(interp_group)
        interp_layout.setContentsMargins(8, 16, 8, 8)
        self._interp_text = QTextEdit()
        self._interp_text.setReadOnly(True)
        self._interp_text.setMaximumHeight(100)
        self._interp_text.setStyleSheet("font-size: 12px; color: #c8d0da;")
        interp_layout.addWidget(self._interp_text)
        self._layout.addWidget(interp_group)

        # Scénario
        scenario_group = QGroupBox("Scénario")
        scenario_group.setStyleSheet("QGroupBox { font-weight: bold; color: #c89ad6; }")
        scenario_layout = QVBoxLayout(scenario_group)
        scenario_layout.setContentsMargins(8, 16, 8, 8)
        self._scenario_text = QTextEdit()
        self._scenario_text.setReadOnly(True)
        self._scenario_text.setMaximumHeight(60)
        self._scenario_text.setStyleSheet("font-size: 12px; color: #c8d0da;")
        scenario_layout.addWidget(self._scenario_text)
        self._layout.addWidget(scenario_group)

        # Exporter
        btn_layout = QHBoxLayout()
        self._btn_txt = QPushButton("Exporter TXT")
        self._btn_md = QPushButton("Exporter Markdown")
        self._btn_json = QPushButton("Exporter JSON")
        for btn in (self._btn_txt, self._btn_md, self._btn_json):
            btn.setStyleSheet(
                "QPushButton { padding: 6px 12px; font-size: 11px; }"
            )
            btn_layout.addWidget(btn)
        self._btn_txt.clicked.connect(self._export_txt)
        self._btn_md.clicked.connect(self._export_md)
        self._btn_json.clicked.connect(self._export_json)
        self._layout.addLayout(btn_layout)

        self._layout.addStretch()

        scroll.setWidget(widget)
        self.setWidget(scroll)

    def set_result(self, result):
        self._result = result
        self.refresh()

    def refresh(self):
        result = self._result
        if result is None:
            self._summary_text.setPlainText("Aucun résultat disponible.")
            self._metrics_table.setRowCount(0)
            self._interp_text.setPlainText("")
            self._scenario_text.setPlainText("")
            return

        report = build_report(result)
        self._summary_text.setPlainText(report)

        self._fill_metrics(result)

        self._fill_interpretation(result)

        scenario = result.get("scenario", "Standard")
        seed = result.get("seed", "?")
        duration = result.get("duration", 0)
        self._scenario_text.setPlainText(
            f"Scénario : {scenario}\nSeed : {seed}\nDurée : {duration} ticks"
        )

    def _fill_metrics(self, result):
        metrics = {
            "population_end": result.get("population_end", 0),
            "deaths": result.get("deaths", 0),
            "births": result.get("births", 0),
            "builds": result.get("builds", 0),
            "harvests": result.get("harvests", 0),
            "messages": result.get("messages", 0),
            "mean_health": result.get("mean_health"),
            "mean_hunger": result.get("mean_hunger"),
            "mean_trust": result.get("mean_trust"),
        }
        labels = {
            "population_end": "Population finale",
            "deaths": "Morts",
            "births": "Naissances",
            "builds": "Constructions",
            "harvests": "Récoltes",
            "messages": "Messages",
            "mean_health": "Santé moyenne",
            "mean_hunger": "Faim moyenne",
            "mean_trust": "Confiance moyenne",
        }
        rows = [(k, v) for k, v in metrics.items() if v is not None]
        self._metrics_table.setRowCount(len(rows))
        for i, (key, val) in enumerate(rows):
            label_item = QTableWidgetItem(labels.get(key, key))
            if isinstance(val, float):
                val_item = QTableWidgetItem(f"{val:.2f}")
            else:
                val_item = QTableWidgetItem(str(val))
            val_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            self._metrics_table.setItem(i, 0, label_item)
            self._metrics_table.setItem(i, 1, val_item)

    def _fill_interpretation(self, result):
        lines = []
        mh_start = result.get("mean_health")
        mh_end = result.get("mean_health_end")
        if mh_start is not None and mh_end is not None:
            t = interpret_metric("health", mh_start, mh_end)
            if t:
                lines.append(f"Santé : {t}")

        mt_start = result.get("mean_trust")
        mt_end = result.get("mean_trust_end")
        if mt_start is not None and mt_end is not None:
            t = interpret_metric("trust", mt_start, mt_end)
            if t:
                lines.append(f"Confiance : {t}")

        mg_start = result.get("mean_hunger")
        mg_end = result.get("mean_hunger_end")
        if mg_start is not None and mg_end is not None:
            t = interpret_metric("hunger", mg_start, mg_end)
            if t:
                lines.append(f"Faim : {t}")

        if not lines:
            summary = build_short_summary(result)
            lines.append(summary)

        self._interp_text.setPlainText("\n".join(lines))

    def _export_txt(self):
        if self._result is None:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Exporter en TXT", "rapport.txt", "Fichiers texte (*.txt)"
        )
        if path:
            from game.studio_export import export_txt
            export_txt(build_report(self._result), path)

    def _export_md(self):
        if self._result is None:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Exporter en Markdown", "rapport.md", "Markdown (*.md)"
        )
        if path:
            from game.studio_export import export_markdown
            metrics = {k: self._result.get(k) for k in [
                "population_end", "deaths", "births", "builds",
                "harvests", "mean_health", "mean_hunger", "mean_trust",
            ] if self._result.get(k) is not None}
            export_markdown(build_report(self._result), metrics=metrics, filepath=path)

    def _export_json(self):
        if self._result is None:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Exporter en JSON", "rapport.json", "JSON (*.json)"
        )
        if path:
            from game.studio_export import export_json
            export_json(self._result, path)
