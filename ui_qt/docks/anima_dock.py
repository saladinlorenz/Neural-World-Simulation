"""AnimaDock — dock Qt pour l'esprit interne de l'habitant selectionne.

Identite, valeurs, trauma, attachements, intention, plan, croyances
sociales, memoire episodique, traces causales, observations, habitudes
et reputation (Lot E.2).
"""
from PyQt6.QtWidgets import (
    QDockWidget,
    QGroupBox,
    QLabel,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class AnimaDock(QDockWidget):
    """Dock Anima complet (meme donnees que l'inspecteur, en tableaux dedies)."""

    def __init__(self, controller, parent=None):
        super().__init__("Anima", parent)
        self.controller = controller
        self.setObjectName("dock_anima")
        self._build()

    def _build(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        root = QWidget()
        layout = QVBoxLayout(root)

        self.title = QLabel("Selectionnez un habitant")
        self.title.setStyleSheet("font-weight: bold; font-size: 13px;")
        layout.addWidget(self.title)

        self.identity = self._make_table(["Identite", "Valeur"])
        self.values = self._make_table(["Valeur", "Score"])
        self.trauma = self._make_table(["Trauma", "Score"])
        self.attachments = self._make_table(["Attachement", "Score"])
        self.reputation = self._make_table(["Cle", "Reputation"])
        self.social = self._make_table(["Habitant", "Confiance", "Danger", "Fiabilite"])
        self.episodes = self._make_table(
            ["Tick", "Type", "Lieu", "Issue", "Importance"])
        self.traces = self._make_table(
            ["Tick", "Action", "Effet attendu", "Eligibilite"])
        self.observations = self._make_table(["Action", "Recompense", "Tick"])
        self.habits = self._make_table(["Index action", "Habitude"])

        self.intention_label = QLabel("Aucune intention")
        self.plan_label = QLabel("Aucun plan")

        layout.addWidget(self._group("Identite", self.identity))
        layout.addWidget(self._group("Valeurs", self.values))
        layout.addWidget(self._group("Trauma", self.trauma))
        layout.addWidget(self._group("Attachements", self.attachments))
        layout.addWidget(self._group("Reputation", self.reputation))
        layout.addWidget(self._group("Intention", self.intention_label))
        layout.addWidget(self._group("Plan", self.plan_label))
        layout.addWidget(self._group("Croyances sociales", self.social))
        layout.addWidget(self._group("Memoire episodique", self.episodes))
        layout.addWidget(self._group("Traces causales", self.traces))
        layout.addWidget(self._group("Observations", self.observations))
        layout.addWidget(self._group("Habitudes", self.habits))
        layout.addStretch(1)

        scroll.setWidget(root)
        self.setWidget(scroll)

    @staticmethod
    def _make_table(headers):
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setMaximumHeight(180)
        return table

    @staticmethod
    def _group(name, content):
        group = QGroupBox(name)
        layout = QVBoxLayout(group)
        layout.addWidget(content)
        return group

    @staticmethod
    def _fill(table, rows):
        table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            for column_index, value in enumerate(row):
                table.setItem(
                    row_index, column_index, QTableWidgetItem(str(value)))

    def refresh(self):
        snap = self.controller.snapshot_anima()
        anima = (snap or {}).get("anima") if snap else None
        if not snap or anima is None:
            self.title.setText("Selectionnez un habitant")
            for table in (
                self.identity, self.values, self.trauma,
                self.attachments, self.reputation, self.social,
                self.episodes, self.traces, self.observations,
                self.habits,
            ):
                table.setRowCount(0)
            self.intention_label.setText("Aucune intention")
            self.plan_label.setText("Aucun plan")
            return

        self.title.setText(f"Anima — {snap.get('nom', 'Inconnu')}")

        self._fill(self.identity, sorted(anima.get("identity", {}).items()))
        self._fill(self.values, sorted(anima.get("values", {}).items()))
        self._fill(self.trauma, sorted(anima.get("trauma", {}).items()))
        self._fill(self.attachments,
                   sorted(anima.get("attachments", {}).items()))
        self._fill(self.reputation,
                   sorted(anima.get("reputation", {}).items()))

        self.intention_label.setText(
            str(anima.get("intention") or "Aucune intention"))
        self.plan_label.setText(str(anima.get("plan") or "Aucun plan"))

        social_rows = []
        for eid, belief in anima.get("social_beliefs", {}).items():
            if isinstance(belief, dict):
                social_rows.append((
                    eid,
                    f"{float(belief.get('trust', 0.0)):.3f}",
                    f"{float(belief.get('danger', 0.0)):.3f}",
                    f"{float(belief.get('reliability', 0.0)):.3f}",
                ))
        self._fill(self.social, social_rows)

        episode_rows = []
        for item in anima.get("episodes", []):
            if not isinstance(item, dict):
                continue
            place = item.get("place", "")
            if isinstance(place, (tuple, list)) and len(place) >= 2:
                place = f"({place[0]}, {place[1]})"
            episode_rows.append((
                item.get("tick", ""),
                item.get("kind", ""),
                place,
                item.get("outcome", ""),
                f"{float(item.get('importance', 0.0)):.3f}",
            ))
        self._fill(self.episodes, episode_rows)

        trace_rows = []
        for item in anima.get("causal_traces", []):
            if not isinstance(item, dict):
                continue
            trace_rows.append((
                item.get("tick", ""),
                item.get("action", ""),
                item.get("expected_effect", ""),
                f"{float(item.get('eligibility', 0.0)):.3f}",
            ))
        self._fill(self.traces, trace_rows)

        observation_rows = []
        for item in anima.get("observations", []):
            if not isinstance(item, dict):
                continue
            observation_rows.append((
                item.get("action", ""),
                f"{float(item.get('reward', 0.0)):.3f}",
                item.get("tick", ""),
            ))
        self._fill(self.observations, observation_rows)

        self._fill(
            self.habits,
            [(index, f"{float(value):.3f}")
             for index, value in enumerate(anima.get("habits", []))],
        )
