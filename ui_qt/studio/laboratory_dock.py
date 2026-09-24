"""LaboratoryDock — dock Qt pour les résultats d'expérience."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                               QTextEdit, QTableWidget, QTableWidgetItem,
                               QPushButton, QGroupBox, QFileDialog,
                               QScrollArea, QHeaderView, QLabel,
                               QStackedWidget)
from PyQt6.QtCore import Qt, QThread

from game.studio_reports import build_report, build_short_summary, interpret_metric
from game.studio_compare import KEYS
from ui_qt.studio.experiment_worker import ExperimentWorker
from ui_qt.widgets.empty_state import EmptyState


class LaboratoryDock(QDockWidget):
    """Dock du laboratoire : résumé, métriques, interprétation, scénario."""

    def __init__(self, controller, parent=None):
        super().__init__("Laboratoire", parent)
        self.controller = controller
        self._result = None
        self._setup_ui()

    def _setup_ui(self):
        # Racine du dock : pile (vue vide | résultats) + commande A/B.
        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(8, 8, 8, 8)
        root_layout.setSpacing(6)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        widget = QWidget()
        self._layout = QVBoxLayout(widget)
        self._layout.setContentsMargins(0, 0, 0, 0)
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

        # Exporter (toujours visible, même sans résultat)
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
        btn_layout.addStretch()

        self._layout.addStretch()
        scroll.setWidget(widget)

        # ── Lot E : vue vide quand aucun résultat ──
        self.empty_state = EmptyState(
            icon="⚗",
            title="Aucun résultat",
            message="Lancez une expérience A/B pour générer un rapport ici.",
        )
        self._stack = QStackedWidget()
        self._stack.addWidget(self.empty_state)
        self._stack.addWidget(scroll)
        self._content = scroll
        root_layout.addWidget(self._stack)
        root_layout.addLayout(btn_layout)

        # ── Lot F.3 : expérience A/B hors du thread UI ──
        # Reste accessible même quand la vue vide est affichée.
        ab_layout = QHBoxLayout()
        self._ab_btn = QPushButton("Lancer A/B (culture)")
        self._ab_btn.setStyleSheet(
            "QPushButton { background-color: #2980b9; color: white; "
            "padding: 6px 14px; border: none; border-radius: 3px; }"
            "QPushButton:hover { background-color: #3498db; }"
            "QPushButton:disabled { background-color: #555; }"
        )
        self._ab_btn.clicked.connect(self._start_ab)
        ab_layout.addWidget(self._ab_btn)
        self._ab_status = QLabel("")
        ab_layout.addWidget(self._ab_status)
        ab_layout.addStretch()
        root_layout.addLayout(ab_layout)
        self._thread = None
        self._worker = None

        self.setWidget(root)

    # ── Lot F.3 : A/B dans un QThread ──

    def _start_ab(self):
        if self._thread is not None and self._thread.isRunning():
            return
        self._ab_btn.setEnabled(False)
        self._ab_status.setText("Expérience A/B en cours…")

        from game.lab import ExperimentRunner
        from game.engine import build_world
        am = self.controller.sim.am

        def build_fn(seed, n_agents):
            return build_world(am, seed=seed, procedural=False,
                               populate_dense=False, n_agents=n_agents)

        def toggle_fn(sim):
            if getattr(sim, "runtime", None) is None:
                sim.runtime = {}
            sim.runtime["culture_enabled"] = False

        self._thread = QThread(self)
        self._worker = ExperimentWorker(
            ExperimentRunner(), build_fn, seeds=[1, 2],
            feature_name="culture", toggle_fn=toggle_fn,
            ticks=800, agents=10)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_experiment_finished)
        self._worker.failed.connect(self._on_experiment_failed)
        self._worker.finished.connect(self._thread.quit)
        self._worker.failed.connect(self._thread.quit)
        self._thread.finished.connect(self._cleanup_thread)
        self._thread.start()

    def _on_experiment_finished(self, report):
        self._result = report
        self._ab_status.setText("A/B terminé.")
        self.refresh()

    def _on_experiment_failed(self, message):
        self._ab_status.setText(f"Échec : {message}")

    def _cleanup_thread(self):
        self._thread = None
        self._worker = None
        self._ab_btn.setEnabled(True)

    # ── Affichage ──

    def set_result(self, result):
        self._result = result
        self.refresh()

    def refresh(self):
        result = self._result
        if result is None:
            # Lot E : vue vide (les champs restent réinitialisés).
            self._stack.setCurrentWidget(self.empty_state)
            self._summary_text.setPlainText("Aucun résultat disponible.")
            self._metrics_table.setRowCount(0)
            self._interp_text.setPlainText("")
            self._scenario_text.setPlainText("")
            return

        # Lot E : un rapport est disponible -> page contenu.
        self._stack.setCurrentWidget(self._content)

        if "variants" in result:
            self._refresh_ab(result)
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

    def _refresh_ab(self, result):
        """Affichage d'un rapport A/B ({feature, seeds, variants})."""
        on = result.get("variants", {}).get("A_on", {})
        off = result.get("variants", {}).get("B_off", {})
        feature = result.get("feature", "?")
        seeds = result.get("seeds", 0)
        self._summary_text.setPlainText(
            f"Expérience A/B — fonction « {feature} » sur {seeds} graine(s).\n"
            f"A = fonction active, B = fonction désactivée "
            f"(même seed, même durée)."
        )

        labels = {
            "population": "Population finale",
            "deaths": "Morts",
            "births": "Naissances",
            "builds": "Constructions",
            "mean_age": "Âge moyen",
            "mean_health": "Santé moyenne",
            "storages": "Dépôts",
            "sites": "Chantiers",
        }
        keys = [k for k in on if isinstance(on.get(k), (int, float))
                and isinstance(off.get(k), (int, float))]
        self._metrics_table.setRowCount(len(keys))
        for i, key in enumerate(keys):
            a, b = float(on[key]), float(off[key])
            label_item = QTableWidgetItem(labels.get(key, key))
            value_item = QTableWidgetItem(
                f"{a:.2f} / {b:.2f}  (Δ {a - b:+.2f})")
            value_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self._metrics_table.setItem(i, 0, label_item)
            self._metrics_table.setItem(i, 1, value_item)

        lines = []
        for key, phrase in (
            ("population", "population"),
            ("deaths", "mortalité"),
            ("births", "naissances"),
            ("builds", "constructions"),
        ):
            a, b = on.get(key), off.get(key)
            if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
                continue
            delta = a - b
            if abs(delta) < 0.5:
                lines.append(f"{phrase} : sans effet visible.")
            elif delta > 0:
                lines.append(f"{phrase} : la fonction active augmente "
                             f"la valeur de {delta:+.1f}.")
            else:
                lines.append(f"{phrase} : la fonction active diminue "
                             f"la valeur de {delta:+.1f}.")
        self._interp_text.setPlainText("\n".join(lines) or "Aucun écart notable.")
        self._scenario_text.setPlainText(
            f"Scénario : A/B automatique\n"
            f"Fonction : {feature}\n"
            f"Graines : {seeds}"
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
