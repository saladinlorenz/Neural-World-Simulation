"""LaboratoryDock — dock Qt pour les résultats d'expérience."""
import os

from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                               QTextEdit, QTableWidget, QTableWidgetItem,
                               QPushButton, QGroupBox, QFileDialog,
                               QScrollArea, QHeaderView, QLabel,
                               QStackedWidget, QSpinBox)
from PyQt6.QtCore import Qt, QThread

from game.studio_reports import build_report, build_short_summary, interpret_metric
from game.studio_compare import KEYS
from ui_qt.studio.experiment_worker import ExperimentWorker
from ui_qt.widgets.empty_state import EmptyState


def _num(value):
    """float défensif (None si la valeur n'est pas numérique)."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _text(value):
    """Texte d'une valeur de snapshot (une méthode non appelée est appelée)."""
    if value is None:
        return None
    if callable(value):
        try:
            value = value()
        except Exception:
            return None
    return str(value)


def _season_name(value):
    """Nom français de saison (l'indice seul n'est pas lisible)."""
    if value is None:
        return None
    try:
        from game.config import SEASONS
        return str(SEASONS[int(value)])
    except Exception:
        return str(value)


def _format_snapshot(snap):
    """Lignes clés d'un world_snapshot() pour le bloc Résumé."""
    if not isinstance(snap, dict):
        return ""
    lines = []

    head = []
    for key, prefix, fmt in (("tick", "tick ", _text), ("jour", "jour ", _text),
                             ("saison", "", _season_name), ("annee", "an ", _text)):
        if key not in snap:
            continue
        val = fmt(snap[key])
        if val is not None:
            head.append(f"{prefix}{val}")
    if head:
        lines.append("Temps : " + " · ".join(str(h) for h in head))

    pop = []
    if "population" in snap:
        pop.append(f"Population : {snap['population']} en vie")
    if "moutons" in snap:
        pop.append(f"Moutons : {snap['moutons']}")
    if "items" in snap:
        pop.append(f"Objets : {snap['items']}")
    if pop:
        lines.append(" | ".join(pop))

    meteo = []
    for key, label in (("pluie", "pluie"), ("temperature", "température"),
                       ("lumiere", "lumière")):
        val = _num(snap.get(key))
        if val is not None:
            meteo.append(f"{label} {val:.2f}")
    if meteo:
        lines.append("Météo : " + ", ".join(meteo))

    alerts = []
    for key, label in (("feux", "feux en cours"), ("attaques", "attaques"),
                       ("tombes", "tombes"), ("deces", "décès")):
        val = _num(snap.get(key))
        if val:
            alerts.append(f"{int(val)} {label}")
    if alerts:
        lines.append("Alertes : " + ", ".join(alerts))

    if snap.get("champion"):
        lines.append(f"Champion : {snap['champion']}")
    return "\n".join(lines)


class LaboratoryDock(QDockWidget):
    """Dock du laboratoire : résumé, métriques, interprétation, scénario."""

    def __init__(self, controller, parent=None):
        super().__init__("Laboratoire", parent)
        self.controller = controller
        self._result = None
        self._result_kind = None
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
        self._btn_full = QPushButton("Export complet (TXT+MD+CSV+JSON)")
        self._btn_lab = QPushButton("Exporter données lab")
        for btn in (self._btn_txt, self._btn_md, self._btn_json,
                    self._btn_full, self._btn_lab):
            btn.setStyleSheet(
                "QPushButton { padding: 6px 12px; font-size: 11px; }"
            )
            btn_layout.addWidget(btn)
        self._btn_txt.clicked.connect(self._export_txt)
        self._btn_md.clicked.connect(self._export_md)
        self._btn_json.clicked.connect(self._export_json)
        self._btn_full.clicked.connect(self._export_full)
        self._btn_lab.clicked.connect(self._export_lab)
        self._export_status = QLabel("")
        self._export_status.setStyleSheet("font-size: 11px; color: #8fa3b8;")
        btn_layout.addWidget(self._export_status)
        btn_layout.addStretch()

        self._layout.addStretch()
        scroll.setWidget(widget)

        # ── Lot E : vue vide quand aucun résultat ──
        self.empty_state = EmptyState(
            icon="⚗",
            title="Aucun résultat",
            message="Lancez une expérience A/B ou générez un rapport du "
                    "monde courant pour afficher un rapport ici.",
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

        # Rapport du monde courant : jamais désactivé (même pendant un A/B).
        self._world_btn = QPushButton("Rapport du monde courant")
        self._world_btn.setStyleSheet(
            "QPushButton { background-color: #27ae60; color: white; "
            "padding: 6px 14px; border: none; border-radius: 3px; }"
            "QPushButton:hover { background-color: #2ecc71; }"
        )
        self._world_btn.clicked.connect(self._start_world_report)
        ab_layout.addWidget(self._world_btn)

        ab_layout.addWidget(QLabel("Ticks A/B"))
        self._ticks_spin = QSpinBox()
        self._ticks_spin.setRange(100, 5000)
        self._ticks_spin.setValue(800)
        self._ticks_spin.setToolTip("Durée de chaque variante A/B (ticks)")
        ab_layout.addWidget(self._ticks_spin)

        ab_layout.addWidget(QLabel("Graines"))
        self._seeds_spin = QSpinBox()
        self._seeds_spin.setRange(1, 5)
        self._seeds_spin.setValue(2)
        self._seeds_spin.setToolTip("Nombre de graines A/B (1 à 5)")
        ab_layout.addWidget(self._seeds_spin)

        self._ab_status = QLabel("")
        ab_layout.addWidget(self._ab_status)
        ab_layout.addStretch()
        root_layout.addLayout(ab_layout)
        self._thread = None
        self._worker = None

        # Export lab : inutile si l'enregistreur est absent du simulateur.
        if getattr(getattr(self.controller, "sim", None), "lab", None) is None:
            self._btn_lab.setEnabled(False)
            self._btn_lab.setToolTip("Aucun enregistreur lab (sim.lab absent).")

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

        n_seeds = max(1, int(self._seeds_spin.value()))
        ticks = max(100, int(self._ticks_spin.value()))

        def build_fn(seed, n_agents):
            return build_world(am, seed=seed, procedural=False,
                               populate_dense=False, n_agents=n_agents)

        def toggle_fn(sim):
            if getattr(sim, "runtime", None) is None:
                sim.runtime = {}
            sim.runtime["culture_enabled"] = False

        self._thread = QThread(self)
        self._worker = ExperimentWorker(
            ExperimentRunner(), build_fn, seeds=list(range(1, n_seeds + 1)),
            feature_name="culture", toggle_fn=toggle_fn,
            ticks=ticks, agents=10)
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
        self._result_kind = "ab"
        self._ab_status.setText("A/B terminé.")
        self.refresh()

    def _on_experiment_failed(self, message):
        self._ab_status.setText(f"Échec : {message}")

    def _cleanup_thread(self):
        self._thread = None
        self._worker = None
        self._ab_btn.setEnabled(True)

    # ── Rapport du monde courant ──

    @staticmethod
    def _metrics_of(result):
        """Plat des métriques numériques (pour l'export CSV/Markdown)."""
        metrics = {}
        for key in ("population_start", "population_end", "births", "deaths",
                    "builds", "harvests", "messages", "institutions",
                    "mean_health", "mean_hunger", "mean_trust"):
            val = result.get(key)
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                metrics[key] = val
        snap = result.get("snapshot")
        if isinstance(snap, dict):
            for key in ("tick", "pluie", "temperature", "lumiere", "feux",
                        "attaques", "tombes"):
                val = snap.get(key)
                if isinstance(val, (int, float)) and not isinstance(val, bool):
                    metrics[f"snapshot.{key}"] = val
        variants = result.get("variants")
        if isinstance(variants, dict):
            for vname, vdata in variants.items():
                if not isinstance(vdata, dict):
                    continue
                for key, val in vdata.items():
                    if isinstance(val, (int, float)) and not isinstance(val, bool):
                        metrics[f"{vname}.{key}"] = val
        return metrics

    def _build_world_result(self):
        """Rapport « monde courant » : mêmes clés que le chemin A/B simple."""
        from game.diagnostics import world_snapshot

        sim = self.controller.sim
        stats = dict(getattr(sim, "stats", None) or {})
        alive = [a for a in (getattr(sim, "agents", None) or [])
                 if getattr(a, "alive", False)]
        n = len(alive)

        def mean(attr):
            if not n:
                return None
            total = 0.0
            for a in alive:
                val = _num(getattr(a, attr, None))
                if val is None:
                    return None
                total += val
            return total / n

        # Confiance : relations (rel[eid][0] ∈ [-1, 1]) remappées sur 0..1.
        trust_vals = []
        for a in alive:
            for rel in (getattr(a, "rel", None) or {}).values():
                raw = rel[0] if isinstance(rel, (tuple, list)) else rel
                val = _num(raw)
                if val is None:
                    continue
                trust_vals.append(min(1.0, max(0.0, 0.5 + 0.5 * val)))
        mean_trust = sum(trust_vals) / len(trust_vals) if trust_vals else None

        pop_hist = getattr(sim, "pop_hist", None)
        try:
            pop_start = int(pop_hist[0]) if len(pop_hist) else n
        except (TypeError, ValueError, IndexError):
            pop_start = n
        w = getattr(sim, "w", None)
        duration = int(getattr(w, "tick", 0) or 0)

        institutions = 0
        counts = getattr(getattr(sim, "lab", None), "_event_counts", None)
        if counts:
            institutions = int(counts.get("institution", 0) or 0)

        result = {
            "scenario": "Monde courant",
            "seed": int(getattr(sim, "seed", 0) or 0),
            "duration": duration,
            "population_start": pop_start,
            "population_end": n,
            "births": int(stats.get("births", 0) or 0),
            "deaths": int(stats.get("deaths", 0) or 0),
            "builds": int(stats.get("builds", 0) or 0),
            "harvests": int(stats.get("harvests", 0) or 0),
            "messages": int(stats.get("talks", 0) or 0),
            "institutions": institutions,
            "mean_health": mean("health"),
            "mean_hunger": mean("hunger"),
            "mean_trust": mean_trust,
        }
        try:
            snap = world_snapshot(sim)
            score = snap.get("score_champion")
            if isinstance(score, float) and (score != score
                                             or score in (float("inf"),
                                                          float("-inf"))):
                # JSON strict : ±inf n'est pas sérialisable proprement.
                snap["score_champion"] = None
            result["snapshot"] = snap
        except Exception:
            result["snapshot"] = None
        result["metrics"] = self._metrics_of(result)
        return result

    def _start_world_report(self):
        try:
            result = self._build_world_result()
        except Exception as exc:
            self._export_status.setText(
                f"Échec rapport monde : {type(exc).__name__}: {exc}")
            return
        self._result = result
        self._result_kind = "world"
        self._ab_status.setText("Rapport du monde courant généré.")
        self.refresh()

    def _ensure_result(self):
        """Génère le rapport du monde si aucun résultat n'est disponible."""
        if self._result is not None:
            return True
        try:
            result = self._build_world_result()
        except Exception as exc:
            self._export_status.setText(
                f"Échec rapport monde : {type(exc).__name__}: {exc}")
            return False
        self._result = result
        self._result_kind = "world"
        self.refresh()
        return True

    # ── Affichage ──

    def set_result(self, result):
        self._result = result
        self._result_kind = "ab"
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

        if self._result_kind != "world" and "variants" in result:
            self._refresh_ab(result)
            return

        report = build_report(result)
        snapshot = result.get("snapshot")
        snap_text = _format_snapshot(snapshot)
        if snap_text:
            report = f"{report}\n\n— Monde courant —\n{snap_text}"
        self._summary_text.setPlainText(report)

        self._fill_metrics(result)

        self._fill_interpretation(result)

        scenario = result.get("scenario", "Standard")
        seed = result.get("seed", "?")
        duration = result.get("duration", 0)
        lines = [
            f"Scénario : {scenario}",
            f"Seed : {seed}",
            f"Durée : {duration} ticks",
        ]
        if isinstance(snapshot, dict):
            saison = _season_name(snapshot.get("saison"))
            heure = _text(snapshot.get("heure"))
            if saison is not None:
                lines.append(f"Saison : {saison}")
            if heure is not None:
                lines.append(f"Heure : {heure}")
        self._scenario_text.setPlainText("\n".join(lines))

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
        if not self._ensure_result():
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Exporter en TXT", "rapport.txt", "Fichiers texte (*.txt)"
        )
        if path:
            from game.studio_export import export_txt
            export_txt(build_report(self._result), path)

    def _export_md(self):
        if not self._ensure_result():
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
        if not self._ensure_result():
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Exporter en JSON", "rapport.json", "JSON (*.json)"
        )
        if path:
            from game.studio_export import export_json
            export_json(self._result, path)

    def _export_full(self):
        """TXT + MD + CSV + JSON via studio_export.export_full_report."""
        if not self._ensure_result():
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Exporter le rapport complet", "rapport_complet.json",
            "JSON (*.json)"
        )
        if not path:
            return
        directory = os.path.dirname(path) or "."

        data = self._result
        if not data.get("metrics"):
            data = dict(data)
            data["metrics"] = self._metrics_of(data)

        events = []
        try:
            from game.ui_snapshots import journal_snapshot
            for entry in journal_snapshot(self.controller.sim):
                events.append(f"t{entry.get('tick')} : {entry.get('text')}")
        except Exception:
            events = []

        try:
            from game.studio_export import export_full_report
            exports = export_full_report(data, timeline_events=events,
                                         directory=directory)
        except Exception as exc:
            self._export_status.setText(
                f"Échec export complet : {type(exc).__name__}: {exc}")
            return
        message = (f"Export complet ({len(exports)} fichiers) : "
                   f"{exports.get('json') or exports.get('txt', '')}")
        self._export_status.setText(message)
        self._export_status.setToolTip(
            "\n".join(f"{k} : {v}" for k, v in exports.items()))

    def _export_lab(self):
        """Exporte les données du LabRecorder (sim.lab.export)."""
        sim = getattr(self.controller, "sim", None)
        lab = getattr(sim, "lab", None)
        if lab is None:
            self._export_status.setText("Aucune donnée lab (sim.lab absent).")
            self._btn_lab.setEnabled(False)
            return
        try:
            json_path, csv_path = lab.export()
        except Exception as exc:
            self._export_status.setText(
                f"Échec export lab : {type(exc).__name__}: {exc}")
            return
        message = f"Lab exporté : {json_path} / {csv_path}"
        self._export_status.setText(message)
        self._export_status.setToolTip(message)
