"""AnimaDock — dock Qt pour l'esprit interne de l'habitant selectionne.

Identite, valeurs, trauma, attachements, intention, plan, croyances
sociales, memoire episodique, traces causales, observations, habitudes
et reputation (Lot E.2).
"""
from PyQt6.QtWidgets import (
    QDockWidget,
    QGridLayout,
    QGroupBox,
    QLabel,
    QScrollArea,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ui_qt.widgets.empty_state import EmptyState
from ui_qt.widgets.stat_card import StatCard


def _top_pair(values):
    """Clé dominante d'un dict de scores (Lot F) : renvoie (clé, score).

    Renvoie ``(None, 0.0)`` si le dict est vide ou sans valeur numérique.
    """
    if not isinstance(values, dict) or not values:
        return None, 0.0
    best_key = None
    best_score = float("-inf")
    for key, value in values.items():
        try:
            score = float(value)
        except (TypeError, ValueError):
            continue
        if score > best_score:
            best_key, best_score = key, score
    if best_key is None:
        return None, 0.0
    return best_key, best_score


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

        # === Cartes de résumé (Lot F.2) ===
        cards_grid = QGridLayout()
        cards_grid.setSpacing(6)
        cards_grid.setContentsMargins(0, 2, 0, 2)
        self._cards = {
            "identity": StatCard("Identité dominante", "#A78BFA"),
            "value": StatCard("Valeur la plus haute", "#4CC9F0"),
            "trauma": StatCard("Trauma principal", "#FF6B6B"),
            "intention": StatCard("Intention courante", "#F6BD60"),
            "plan": StatCard("Score de plan", "#62D394"),
            "reputation": StatCard("Réputation sociale", "#F8E16C"),
        }
        for index, card in enumerate(self._cards.values()):
            cards_grid.addWidget(card, index // 2, index % 2)
        layout.addLayout(cards_grid)

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

        # === Empilement vue vide / contenu (Lot E) ===
        # Un seul EmptyState persistant, basculé par refresh().
        self.empty_state = EmptyState(
            icon="◉",
            title="Sélectionnez un habitant",
            message=("Cliquez un habitant sur la carte ou choisissez-en un "
                     "dans Habitants pour inspecter son esprit intérieur."),
        )
        self._stack = QStackedWidget()
        self._stack.addWidget(self.empty_state)
        self._stack.addWidget(scroll)
        self._content = scroll
        self.setWidget(self._stack)

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

    def _clear_tables(self):
        for table in (
            self.identity, self.values, self.trauma,
            self.attachments, self.reputation, self.social,
            self.episodes, self.traces, self.observations,
            self.habits,
        ):
            table.setRowCount(0)

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
            # Lot E : vue vide + tableaux/cartes remis à zéro.
            self._stack.setCurrentWidget(self.empty_state)
            self.title.setText("Selectionnez un habitant")
            self._clear_tables()
            self._clear_cards()
            self.intention_label.setText("Aucune intention")
            self.plan_label.setText("Aucun plan")
            return

        # Lot E : contenu affiché ; Lot F.2 : cartes de résumé en premier.
        self._stack.setCurrentWidget(self._content)
        self._update_cards(anima)
        self.title.setText(f"Anima — {snap.get('name', 'Inconnu')}")

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

    def _clear_cards(self):
        """Vide les cartes de résumé (aucun habitant sélectionné)."""
        for card in self._cards.values():
            card.set_value("—")

    def _update_cards(self, anima):
        """Remplit les six cartes de résumé (Lot F.2).

        Clés réelles du snapshot ``anima`` : ``identity``, ``values``,
        ``trauma`` (dicts de scores 0..1), ``intention`` (dict avec ``kind``
        et ``priority``), ``plan`` (dict avec ``score``) et ``reputation``
        (dict avec ``social`` en -1..1).
        """
        # Identité / valeur / trauma dominantes (logique top_pair du plan).
        for card_key, source in (
            ("identity", "identity"),
            ("value", "values"),
            ("trauma", "trauma"),
        ):
            key, score = _top_pair(anima.get(source, {}))
            card = self._cards[card_key]
            if key is None:
                card.set_value("—")
            else:
                card.set_value(score, text=str(key).title())

        # Intention courante : libellé + priorité (barre).
        intention = anima.get("intention")
        if isinstance(intention, dict):
            kind = str(intention.get("kind") or "—")
            try:
                priority = float(intention.get("priority", 0.0))
            except (TypeError, ValueError):
                priority = 0.0
            self._cards["intention"].set_value(priority, text=kind)
        else:
            self._cards["intention"].set_value("Aucune")

        # Score du meilleur plan (peut dépasser 1 : la barre est bornée).
        plan = anima.get("plan")
        if isinstance(plan, dict):
            try:
                score = float(plan.get("score", 0.0))
            except (TypeError, ValueError):
                score = 0.0
            self._cards["plan"].set_value(score)
        else:
            self._cards["plan"].set_value("—")

        # Réputation sociale : clé « social » (-1..1), pas « updated_tick ».
        reputation = anima.get("reputation")
        social = reputation.get("social") if isinstance(reputation, dict) else None
        if social is None:
            self._cards["reputation"].set_value("—")
        else:
            try:
                self._cards["reputation"].set_value(float(social))
            except (TypeError, ValueError):
                self._cards["reputation"].set_value("—")
