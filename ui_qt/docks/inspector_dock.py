"""InspectorDock — dock Qt pour l'inspecteur d'habitant selectionne."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                              QTableView, QLabel, QScrollArea, QFrame,
                              QGroupBox, QGridLayout, QSlider,
                              QStackedWidget)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor

from game.ui_snapshots import selected_agent_snapshot, anima_snapshot
from game.ui_registry import C_CORPS, C_COG, C_PERSO, C_EMO, C_BESOIN, C_EXP, C_MEM
from game.diagnostics import action_name
from ui_qt.models.anima_model import AnimaModel
from ui_qt.widgets.empty_state import EmptyState
from ui_qt.widgets.stat_card import StatCard


class InspectorDock(QDockWidget):
    """Dock inspecteur complet : identite + corps + Anima + relations."""

    command_result = pyqtSignal(dict)

    #: Cartes visuelles (Lot F.1) : (cle interne, titre, couleur Neural Lab).
    #: Les valeurs proviennent de ``health`` et ``needs_named`` du snapshot.
    CARD_SPECS = [
        ("sante", "Santé", "#62D394"),
        ("energie", "Énergie", "#F6BD60"),
        ("faim", "Faim", "#FF6B6B"),
        ("soif", "Soif", "#4CC9F0"),
        ("sommeil", "Sommeil", "#A78BFA"),
        ("securite", "Sécurité", "#F8E16C"),
        ("appartenance", "Appartenance", "#B8C4FF"),
        ("estime", "Estime", "#74D9F5"),
    ]

    #: Libellés français du diagnostic de décision (Phase 1). Clés = valeurs
    #: brutes de la trace moteur ; l'UI ne fait que traduire, jamais recalculer.
    POSS_VERB = {"pickup": "Ramasser", "sit": "S'asseoir", "follow": "Suivre",
                 "talk": "Parler"}
    POSS_TARGET = {"item": "objet", "spot": "lieu",
                   "agent": "habitant", "terrain": "terrain"}
    POSS_STATE = {"selected": "choisi", "feasible": "faisable",
                  "rejected": "rejeté", "invalid": "invalide",
                  "expired": "périmé"}

    def __init__(self, controller, parent=None):
        super().__init__("Inspecteur", parent)
        self.controller = controller
        self._anima_model = AnimaModel()
        # Cache UI-only : évite de reconstruire la grille à l'identique.
        self._decision_revision = None
        self._setup_ui()

    def _setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        widget = QWidget()
        self._layout = QVBoxLayout(widget)
        self._layout.setContentsMargins(8, 8, 8, 8)
        self._layout.setSpacing(6)

        # === Identite (portrait + etat civil) ===
        head = QHBoxLayout()
        head.setSpacing(8)
        self._portrait = QLabel()
        self._portrait.setFixedSize(52, 52)
        self._portrait.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._portrait.setStyleSheet(
            "background-color: #1a2332; border: 1px solid #39424f; border-radius: 4px;"
        )
        head.addWidget(self._portrait)

        head_texts = QVBoxLayout()
        head_texts.setSpacing(2)
        self._identity_label = QLabel("Aucun agent selectionne")
        self._identity_label.setWordWrap(True)
        self._identity_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        head_texts.addWidget(self._identity_label)

        # === Etat de base ===
        self._state_label = QLabel("")
        self._state_label.setWordWrap(True)
        head_texts.addWidget(self._state_label)

        # === Position (monde + tuile) ===
        self._position_label = QLabel("")
        self._position_label.setWordWrap(True)
        self._position_label.setStyleSheet("font-size: 11px; color: #697281;")
        head_texts.addWidget(self._position_label)

        # === Metadonnees (temperature, mort naturelle) ===
        self._meta_label = QLabel("")
        self._meta_label.setWordWrap(True)
        self._meta_label.setStyleSheet("font-size: 11px; color: #697281;")
        head_texts.addWidget(self._meta_label)

        head.addLayout(head_texts, 1)
        self._layout.addLayout(head)

        # === Cartes visuelles (Lot F.1) ===
        # Rangée de cartes Santé / besoins, mise à jour dans refresh().
        cards_grid = QGridLayout()
        cards_grid.setSpacing(6)
        cards_grid.setContentsMargins(0, 2, 0, 2)
        self._cards = {}
        for index, (key, title, color) in enumerate(self.CARD_SPECS):
            card = StatCard(title, color)
            self._cards[key] = card
            cards_grid.addWidget(card, index // 2, index % 2)
        self._layout.addLayout(cards_grid)

        # === Groupes d'info ===
        self._create_info_groups()

        # === Cerveau badge (apres Besoins) ===
        self._brain_group = QGroupBox("Cerveau")
        self._brain_group.setStyleSheet(
            f"QGroupBox {{ font-weight: bold; color: {_hex(C_COG)}; }}"
        )
        brain_layout = QVBoxLayout(self._brain_group)
        brain_layout.setContentsMargins(8, 16, 8, 8)
        brain_layout.setSpacing(2)
        self._brain_neurons_label = QLabel("")
        self._brain_neurons_label.setStyleSheet("font-size: 11px;")
        self._brain_freq_label = QLabel("")
        self._brain_freq_label.setStyleSheet("font-size: 11px;")
        self._brain_badge = QLabel("")
        self._brain_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._brain_badge.setStyleSheet(
            "background-color: #1a2332; border: 1px solid #3e7cd6; "
            "border-radius: 4px; padding: 4px 8px; font-size: 11px; color: #d0d8e0;"
        )
        brain_layout.addWidget(self._brain_neurons_label)
        brain_layout.addWidget(self._brain_freq_label)
        brain_layout.addWidget(self._brain_badge)
        self._layout.addWidget(self._brain_group)

        # === Inventaire (apres Cerveau) ===
        self._inventory_group = QGroupBox("Inventaire")
        self._inventory_group.setStyleSheet(
            f"QGroupBox {{ font-weight: bold; color: {_hex(C_EXP)}; }}"
        )
        inv_layout = QVBoxLayout(self._inventory_group)
        inv_layout.setContentsMargins(8, 16, 8, 8)
        inv_layout.setSpacing(2)
        self._inventory_label = QLabel("")
        self._inventory_label.setWordWrap(True)
        self._inventory_label.setStyleSheet("font-size: 11px;")
        inv_layout.addWidget(self._inventory_label)
        self._layout.addWidget(self._inventory_group)

        # === Outil (apres Inventaire) ===
        self._tool_group = QGroupBox("Outil")
        self._tool_group.setStyleSheet(
            f"QGroupBox {{ font-weight: bold; color: {_hex(C_BESOIN)}; }}"
        )
        tool_layout = QVBoxLayout(self._tool_group)
        tool_layout.setContentsMargins(8, 16, 8, 8)
        tool_layout.setSpacing(2)
        self._tool_label = QLabel("")
        self._tool_label.setWordWrap(True)
        self._tool_label.setStyleSheet("font-size: 11px;")
        tool_layout.addWidget(self._tool_label)
        self._layout.addWidget(self._tool_group)

        # === Tableau Anima ===
        anima_box = QGroupBox("Anima")
        anima_layout = QVBoxLayout(anima_box)
        self._table = QTableView()
        self._table.setModel(self._anima_model)
        self._table.verticalHeader().setVisible(False)
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.setMinimumHeight(200)
        anima_layout.addWidget(self._table)
        self._layout.addWidget(anima_box)

        # === Memoire (apres Anima) ===
        self._memory_group = QGroupBox("Memoire")
        self._memory_group.setStyleSheet(
            f"QGroupBox {{ font-weight: bold; color: {_hex(C_MEM)}; }}"
        )
        mem_layout = QVBoxLayout(self._memory_group)
        mem_layout.setContentsMargins(8, 16, 8, 8)
        mem_layout.setSpacing(4)
        self._belief_label = QLabel("")
        self._belief_label.setWordWrap(True)
        self._belief_label.setStyleSheet("font-size: 11px;")
        mem_layout.addWidget(self._belief_label)
        self._spatial_label = QLabel("")
        self._spatial_label.setWordWrap(True)
        self._spatial_label.setStyleSheet("font-size: 11px;")
        mem_layout.addWidget(self._spatial_label)
        self._autobio_label = QLabel("")
        self._autobio_label.setWordWrap(True)
        self._autobio_label.setStyleSheet("font-size: 11px;")
        mem_layout.addWidget(self._autobio_label)
        self._life_label = QLabel("")
        self._life_label.setWordWrap(True)
        self._life_label.setStyleSheet("font-size: 11px;")
        mem_layout.addWidget(self._life_label)
        self._layout.addWidget(self._memory_group)

        # === Relations ===
        self._relations_label = QLabel("")
        self._relations_label.setWordWrap(True)
        self._layout.addWidget(self._relations_label)

        # === Activite (Phase 3 : bloc « activity » du snapshot) ===
        self._activity_group = QGroupBox("Activité")
        self._activity_group.setStyleSheet(
            f"QGroupBox {{ font-weight: bold; color: {_hex(C_COG)}; }}"
        )
        act_layout = QVBoxLayout(self._activity_group)
        act_layout.setContentsMargins(8, 16, 8, 8)
        act_layout.setSpacing(2)
        self._activity_state_label = QLabel("")
        self._activity_action_label = QLabel("")
        self._activity_target_label = QLabel("")
        self._activity_stuck_label = QLabel("")
        for act_lbl in (self._activity_state_label, self._activity_action_label,
                        self._activity_target_label, self._activity_stuck_label):
            act_lbl.setWordWrap(True)
            act_lbl.setStyleSheet("font-size: 11px;")
            act_layout.addWidget(act_lbl)
        self._layout.addWidget(self._activity_group)

        # === Decision Trace (section compacte : 10 éléments moteur) ===
        self._dtrace_group = QGroupBox("Decision Trace")
        self._dtrace_group.setStyleSheet(
            f"QGroupBox {{ font-weight: bold; color: {_hex(C_COG)}; }}"
        )
        dt_layout = QVBoxLayout(self._dtrace_group)
        dt_layout.setContentsMargins(8, 16, 8, 8)
        dt_layout.setSpacing(1)
        self._dtrace_labels = []
        for _ in range(10):
            lbl = QLabel("")
            lbl.setWordWrap(True)
            lbl.setStyleSheet("font-size: 11px;")
            dt_layout.addWidget(lbl)
            self._dtrace_labels.append(lbl)
        self._layout.addWidget(self._dtrace_group)

        # === Possibilités évaluées (Phase 1 : diagnostic de décision) ===
        # Lecture seule de la trace capturée par le moteur : l'UI ne recalcule
        # jamais les candidats et ne balaie jamais le monde.
        self._possibilities_group = QGroupBox("Possibilités évaluées")
        self._possibilities_group.setStyleSheet(
            f"QGroupBox {{ font-weight: bold; color: {_hex(C_EXP)}; }}"
        )
        poss_layout = QVBoxLayout(self._possibilities_group)
        poss_layout.setContentsMargins(8, 16, 8, 8)
        poss_layout.setSpacing(2)
        self._possibilities_grid = QGridLayout()
        self._possibilities_grid.setContentsMargins(0, 0, 0, 0)
        self._possibilities_grid.setSpacing(2)
        poss_layout.addLayout(self._possibilities_grid)
        self._possibilities_empty = QLabel("Aucune possibilité évaluée récemment.")
        self._possibilities_empty.setStyleSheet("font-size: 11px; color: #697281;")
        poss_layout.addWidget(self._possibilities_empty)
        self._layout.addWidget(self._possibilities_group)

        # === Délibération (pensée sélectionnée visible) ===
        # Résumé de la dernière délibération : besoin dominant, émotion,
        # candidats, choix, raison, échec.
        self._deliberation_group = QGroupBox("Délibération")
        self._deliberation_group.setStyleSheet(
            f"QGroupBox {{ font-weight: bold; color: {_hex(C_COG)}; }}"
        )
        delib_layout = QVBoxLayout(self._deliberation_group)
        delib_layout.setContentsMargins(8, 16, 8, 8)
        delib_layout.setSpacing(2)
        self._delib_need_label = QLabel("")
        self._delib_emotion_label = QLabel("")
        self._delib_selected_label = QLabel("")
        self._delib_reason_label = QLabel("")
        self._delib_failure_label = QLabel("")
        for lbl in (self._delib_need_label, self._delib_emotion_label,
                    self._delib_selected_label, self._delib_reason_label,
                    self._delib_failure_label):
            lbl.setWordWrap(True)
            lbl.setStyleSheet("font-size: 11px;")
            delib_layout.addWidget(lbl)
        self._layout.addWidget(self._deliberation_group)

        # === Contexte local (perception immédiate) ===
        self._local_context_group = QGroupBox("Contexte local")
        self._local_context_group.setStyleSheet(
            f"QGroupBox {{ font-weight: bold; color: {_hex(C_EMO)}; }}"
        )
        lc_layout = QVBoxLayout(self._local_context_group)
        lc_layout.setContentsMargins(8, 16, 8, 8)
        lc_layout.setSpacing(2)
        self._local_context_label = QLabel("")
        self._local_context_label.setWordWrap(True)
        self._local_context_label.setStyleSheet("font-size: 11px;")
        lc_layout.addWidget(self._local_context_label)
        self._layout.addWidget(self._local_context_group)

        # === Mémoire lieux pertinents (place_memories, borné à 8) ===
        self._places_group = QGroupBox("Lieux mémorisés")
        self._places_group.setStyleSheet(
            f"QGroupBox {{ font-weight: bold; color: {_hex(C_MEM)}; }}"
        )
        places_layout = QVBoxLayout(self._places_group)
        places_layout.setContentsMargins(8, 16, 8, 8)
        places_layout.setSpacing(2)
        self._places_label = QLabel("")
        self._places_label.setWordWrap(True)
        self._places_label.setStyleSheet("font-size: 11px;")
        places_layout.addWidget(self._places_label)
        self._layout.addWidget(self._places_group)

        # === Communication (dernier envoi / réception, moteur seul) ===
        self._comm_group = QGroupBox("Communication")
        self._comm_group.setStyleSheet(
            f"QGroupBox {{ font-weight: bold; color: {_hex(C_PERSO)}; }}"
        )
        comm_layout = QVBoxLayout(self._comm_group)
        comm_layout.setContentsMargins(8, 16, 8, 8)
        comm_layout.setSpacing(2)
        self._comm_said_label = QLabel("")
        self._comm_heard_label = QLabel("")
        for lbl in (self._comm_said_label, self._comm_heard_label):
            lbl.setWordWrap(True)
            lbl.setStyleSheet("font-size: 11px;")
            comm_layout.addWidget(lbl)
        self._layout.addWidget(self._comm_group)

        # === Goal ===
        self._goal_label = QLabel("")
        self._goal_label.setWordWrap(True)
        self._layout.addWidget(self._goal_label)

        self._layout.addStretch()

        scroll.setWidget(widget)

        # === Empilement vue vide / contenu (Lot E) ===
        # Un seul EmptyState persistant : refresh() bascule la page courante.
        self.empty_state = EmptyState(
            icon="◎",
            title="Aucun habitant sélectionné",
            message="Cliquez un habitant sur la carte pour afficher sa fiche complète.",
        )
        self._stack = QStackedWidget()
        self._stack.addWidget(self.empty_state)
        self._stack.addWidget(scroll)
        self._content = scroll
        self.setWidget(self._stack)

    def _create_info_groups(self):
        """Cree les groupes Corps, Cognition, Personnalite, Emotions, Besoins."""
        self._groups = {}
        for key, title, color in [
            ("body", "Corps", C_CORPS),
            ("cog", "Cognition", C_COG),
            ("perso", "Personnalite", C_PERSO),
            ("emo", "Emotions", C_EMO),
            ("skills", "Competences", C_EXP),
        ]:
            group = QGroupBox(title)
            group.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {_hex(color)}; }}")
            grid = QGridLayout(group)
            grid.setContentsMargins(8, 16, 8, 8)
            grid.setSpacing(2)
            self._groups[key] = (group, grid)
            self._layout.addWidget(group)

        needs_group = QGroupBox("Besoins")
        needs_group.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {_hex(C_BESOIN)}; }}")
        needs_grid = QGridLayout(needs_group)
        needs_grid.setContentsMargins(8, 16, 8, 8)
        needs_grid.setSpacing(4)
        self._groups["needs"] = (needs_group, needs_grid)
        self._needs_sliders = {}
        self._needs_labels = {}
        need_keys = ["faim", "soif", "energie", "sommeil", "sante", "securite", "appartenance", "estime"]
        for i, key in enumerate(need_keys):
            lbl = QLabel(f"{key}:")
            lbl.setStyleSheet("color: #697281; font-size: 11px;")
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(0, 100)
            slider.setValue(0)
            val_lbl = QLabel("0%")
            val_lbl.setStyleSheet("font-size: 11px;")
            val_lbl.setFixedWidth(36)
            needs_grid.addWidget(lbl, i, 0)
            needs_grid.addWidget(slider, i, 1)
            needs_grid.addWidget(val_lbl, i, 2)
            self._needs_sliders[key] = slider
            self._needs_labels[key] = val_lbl
            slider.valueChanged.connect(lambda v, lbl=val_lbl: lbl.setText(f"{v}%"))
            slider.sliderReleased.connect(
                lambda k=key, s=slider: self._on_set_stat(k, s)
            )

        # === Famille ===
        family_group = QGroupBox("Famille")
        family_group.setStyleSheet(
            f"QGroupBox {{ font-weight: bold; color: {_hex(C_PERSO)}; }}"
        )
        fam_layout = QVBoxLayout(family_group)
        fam_layout.setContentsMargins(8, 16, 8, 8)
        fam_layout.setSpacing(2)
        self._family_label = QLabel("")
        self._family_label.setWordWrap(True)
        self._family_label.setStyleSheet("font-size: 11px;")
        fam_layout.addWidget(self._family_label)
        self._layout.addWidget(family_group)
        self._groups["family"] = (family_group, None)

    def _on_set_stat(self, stat_key, slider):
        result = self.controller.execute({
            "kind": "set_agent_stat",
            "eid": self.controller.ui_state.selected_agent_eid,
            "stat": stat_key,
            "value": slider.value() / 100.0,
        })
        self.command_result.emit(result)

    def refresh(self):
        snap = selected_agent_snapshot(self.controller.sim,
                                       self.controller.ui_state,
                                       include_activity=True)
        anima_snap = anima_snapshot(self.controller.sim, self.controller.ui_state)

        if snap is None:
            # Lot E : la vue vide remplace le contenu, les champs restent
            # effacés (les tests lisent encore ces labels).
            self._stack.setCurrentWidget(self.empty_state)
            self._clear_cards()
            self._identity_label.setText("Aucun agent selectionne")
            self._state_label.setText("")
            self._position_label.setText("")
            self._meta_label.setText("")
            self._portrait.clear()
            self._brain_neurons_label.setText("")
            self._brain_freq_label.setText("")
            self._brain_badge.setText("")
            self._inventory_label.setText("")
            self._tool_label.setText("")
            self._family_label.setText("")
            for key, slider in self._needs_sliders.items():
                slider.blockSignals(True)
                slider.setValue(0)
                slider.blockSignals(False)
                self._needs_labels[key].setText("0%")
            self._belief_label.setText("")
            self._spatial_label.setText("")
            self._autobio_label.setText("")
            self._life_label.setText("")
            self._anima_model.set_snapshot(None)
            for group, _ in self._groups.values():
                group.setVisible(False)
            self._brain_group.setVisible(False)
            self._inventory_group.setVisible(False)
            self._tool_group.setVisible(False)
            self._memory_group.setVisible(False)
            self._relations_label.setText("")
            self._goal_label.setText("")
            self._activity_group.setVisible(False)
            self._activity_state_label.setText("")
            self._activity_action_label.setText("")
            self._activity_target_label.setText("")
            self._activity_stuck_label.setText("")
            self._possibilities_group.setVisible(False)
            self._clear_grid(self._possibilities_grid)
            self._possibilities_empty.setVisible(False)
            self._dtrace_group.setVisible(False)
            for lbl in self._dtrace_labels:
                lbl.setText("")
            self._deliberation_group.setVisible(False)
            self._delib_need_label.setText("")
            self._delib_emotion_label.setText("")
            self._delib_selected_label.setText("")
            self._delib_reason_label.setText("")
            self._delib_failure_label.setText("")
            self._local_context_group.setVisible(False)
            self._local_context_label.setText("")
            self._places_group.setVisible(False)
            self._places_label.setText("")
            self._comm_group.setVisible(False)
            self._comm_said_label.setText("")
            self._comm_heard_label.setText("")
            self._decision_revision = None
            return

        # Lot E : contenu affiché ; Lot F.1 : cartes rafraîchies en premier.
        self._stack.setCurrentWidget(self._content)
        self._update_cards(snap)

        # Identite
        name = snap.get("name", "?")
        sex = snap.get("sex", "?")
        stage = snap.get("stage", "")
        age = snap.get("age_years", 0)
        cls = snap.get("class", "")
        clan = snap.get("clan", "")
        gen = snap.get("generation", 0)
        self._identity_label.setText(
            f"<b>{name}</b> ({sex}) — {stage}, {age:.1f} ans, {cls}, "
            f"clan {clan}, gen {gen}"
        )

        # Portrait (avatar PIL -> QPixmap, meme source que le dock Habitants)
        try:
            from ui_qt.qtimage import pil_to_pixmap
            self._portrait.setPixmap(pil_to_pixmap(
                self.controller.sim.am.avatar(int(snap.get("eid", 0)), size=48)))
        except Exception:
            self._portrait.clear()

        # Etat (``state`` = etape courante du cerveau, deja dans le snapshot)
        needs = snap.get("needs_named", {}) or {}
        health = snap.get("health", 0)
        energy = needs.get("énergie", 0)
        hunger = needs.get("faim", 0)
        pain = snap.get("pain", 0)
        state = snap.get("state", "—")
        self._state_label.setText(
            f"Etat: {state} | Sante: {health:.0%} | "
            f"Energie: {energy:.0%} | Faim: {hunger:.0%} | "
            f"Douleur: {pain:.1f}"
        )

        # Position (change pendant le deplacement)
        position = snap.get("position", {})
        self._position_label.setText(
            f"Monde {float(position.get('x', 0.0)):.0f},"
            f"{float(position.get('y', 0.0)):.0f} | "
            f"Tuile {position.get('tx', '—')},{position.get('ty', '—')}"
        )

        # Metadonnees : temperature (meteo) + age de mort naturelle attendu
        self._meta_label.setText(
            f"Temperature: {snap.get('temperature', 0.0):.2f} | "
            f"Mort naturelle a "
            f"{snap.get('natural_death_age_years', 0.0):.1f} ans"
        )

        # Groupes d'info
        for key, data in [
            ("body", snap.get("body_named", {})),
            ("cog", snap.get("cognition_named", {})),
            ("perso", snap.get("personality_named", {})),
            ("emo", snap.get("emotions_named", {})),
        ]:
            if key in self._groups:
                group, grid = self._groups[key]
                self._fill_grid(grid, data)
                group.setVisible(bool(data))

        # Competences (changent apres chaque action qui reussit)
        if "skills" in self._groups:
            group, grid = self._groups["skills"]
            skills = snap.get("skills_named", {})
            self._fill_grid(grid, skills)
            group.setVisible(bool(skills))

        # Needs — sliders editables
        needs = self._extract_needs(snap)
        if needs:
            for key, val in needs.items():
                if key in self._needs_sliders:
                    self._needs_sliders[key].blockSignals(True)
                    self._needs_sliders[key].setValue(int(val * 100))
                    self._needs_sliders[key].blockSignals(False)
                    self._needs_labels[key].setText(f"{int(val * 100)}%")
            self._groups["needs"][0].setVisible(True)
        else:
            self._groups["needs"][0].setVisible(False)

        # === Cerveau ===
        brain = snap.get("brain", {})
        if brain:
            neurons = brain.get("neurons", 0)
            freq = brain.get("think_frequency", 0)
            rank = brain.get("action_ranking", [])
            self._brain_neurons_label.setText(f"Nombre de neurones: {neurons}")
            self._brain_freq_label.setText(f"Frequence de reflexion: {freq}")
            if rank:
                top3 = ", ".join(str(r) for r in rank[:3])
                self._brain_badge.setText(f"Top actions: {top3}")
            else:
                self._brain_badge.setText("Aucun classement")
            self._brain_group.setVisible(True)
        else:
            self._brain_group.setVisible(False)

        # === Inventaire ===
        inventory = snap.get("inventory", {})
        if inventory:
            lines = []
            for item, qty in inventory.items():
                if isinstance(qty, (int, float)) and qty != 1:
                    lines.append(f"{item}: {qty}")
                else:
                    lines.append(str(item))
            self._inventory_label.setText("\n".join(lines))
            self._inventory_group.setVisible(True)
        else:
            self._inventory_label.setText("Vide")
            self._inventory_group.setVisible(True)

        # === Outil ===
        # ``tool`` est une fiche ``asset_info`` (dict), pas une chaîne : un
        # ``str(tool)`` affichait le dictionnaire brut.
        tool = snap.get("tool", None)
        if isinstance(tool, dict):
            dur = snap.get("tool_durability", 0)
            self._tool_label.setText(f"{tool.get('nom', '?')} (durabilité: {dur})")
            self._tool_group.setVisible(True)
        elif tool:
            self._tool_label.setText(str(tool))
            self._tool_group.setVisible(True)
        else:
            self._tool_label.setText("Aucun")
            self._tool_group.setVisible(True)

        # === Memoire / croyances ===
        beliefs = snap.get("danger_beliefs", {}) or {}
        spatial = snap.get("memory", {}) or {}
        episodes = snap.get("episodes", [])
        life_events = snap.get("life", [])
        has_belief = bool(beliefs)
        has_spatial = any(bool(v) for v in spatial.values())
        has_episodes = bool(episodes)
        has_life = bool(life_events)
        if has_belief or has_spatial or has_episodes or has_life:
            self._memory_group.setVisible(True)
            if has_belief:
                belief_lines = []
                for cell, danger in list(beliefs.items())[:12]:
                    if isinstance(cell, (tuple, list)) and len(cell) == 2:
                        belief_lines.append(
                            f"cellule ({cell[0]}, {cell[1]}) : danger {danger:.0%}"
                        )
                    elif isinstance(danger, dict):
                        conf = danger.get("confidence", danger.get("c", 0))
                        belief_lines.append(
                            f"{cell}: {danger.get('belief', danger.get('b', '?'))} "
                            f"(confiance: {conf:.0%})"
                        )
                    else:
                        belief_lines.append(f"{cell}: {danger}")
                self._belief_label.setText(
                    "<b>Croyances:</b>\n" + "\n".join(belief_lines)
                )
            else:
                self._belief_label.setText("<b>Croyances:</b> aucune")

            if has_spatial:
                spatial_lines = []
                for cat, marks in spatial.items():
                    if not marks:
                        continue
                    strengths = [float(m.get("strength", 0.0)) for m in marks
                                 if isinstance(m, dict)]
                    strongest = max(strengths) if strengths else 0.0
                    spatial_lines.append(
                        f"{cat}: {len(marks)} lieu(x), force max {strongest:.0%}"
                    )
                self._spatial_label.setText(
                    "<b>Mémoire spatiale:</b>\n" + "\n".join(spatial_lines)
                )
            else:
                self._spatial_label.setText("<b>Mémoire spatiale:</b> aucune")

            if has_episodes:
                last5 = episodes[-5:]
                epi_lines = []
                for i, ep in enumerate(last5):
                    epi_lines.append(f"  [{i+1}] {_format_episode(ep)}")
                self._autobio_label.setText(
                    "<b>Autobiographie:</b>\n" + "\n".join(epi_lines)
                )
            else:
                self._autobio_label.setText("<b>Autobiographie:</b> aucune")

            if has_life:
                life_lines = [f"  • {_format_event(ev)}" for ev in life_events[-8:]]
                self._life_label.setText(
                    "<b>Événements de vie:</b>\n" + "\n".join(life_lines)
                )
            else:
                self._life_label.setText("<b>Événements de vie:</b> aucun")
        else:
            self._memory_group.setVisible(False)
            self._belief_label.setText("")
            self._spatial_label.setText("")
            self._autobio_label.setText("")
            self._life_label.setText("")

        # Anima
        self._anima_model.set_snapshot(anima_snap or snap)

        # Famille (noms lisibles, pas seulement des eids)
        family = snap.get("family", {}) or {}
        children = list(family.get("children", []) or [])
        self._family_label.setText(
            "\n".join([
                f"Partenaire : {self._agent_label(family.get('partner_eid'))}",
                f"Pere : {self._agent_label(family.get('father_eid'))}",
                f"Mere : {self._agent_label(family.get('mother_eid'))}",
                "Enfants : " + (
                    ", ".join(self._agent_label(eid) for eid in children)
                    if children else "—"
                ),
            ])
        )
        self._groups["family"][0].setVisible(True)

        # Relations
        rels = snap.get("relations", [])
        if rels:
            lines = []
            for r in rels[:5]:
                conf = r.get("trust", 0)
                aff = r.get("affection", 0)
                alive = "vivant" if r.get("alive", False) else "mort"
                lines.append(
                    f"  {r.get('name', '?')}: conf={conf:.2f} "
                    f"aff={aff:.2f} ({alive})"
                )
            self._relations_label.setText(
                "<b>Relations:</b>\n" + "\n".join(lines)
            )
        else:
            self._relations_label.setText("<b>Relations:</b> aucune")

        # === Activite (donnees reelles du bloc « activity ») ===
        activity = snap.get("activity", {}) or {}
        goal_action = activity.get("goal_action")
        if goal_action is None:
            action_text = "Aucun but"
        else:
            action_text = action_name(self.controller.sim, goal_action)
        goal_tile = activity.get("goal_tile")
        if goal_tile:
            target_text = f"({goal_tile[0]}, {goal_tile[1]})"
        else:
            target_text = "—"
        self._activity_state_label.setText(
            f"État : {activity.get('state', '—')}"
        )
        self._activity_action_label.setText(f"Action : {action_text}")
        self._activity_target_label.setText(f"Cible : {target_text}")
        self._activity_stuck_label.setText(
            f"Bloqué : {int(activity.get('stuck', 0))}"
        )
        self._activity_group.setVisible(True)

        # === Délibération (pensée sélectionnée visible) ===
        # Pression avec valeurs : decision_trace riche si présent, sinon
        # le résumé deliberation historique. L'UI traduit, jamais recalcule.
        deliberation = snap.get("deliberation", {}) or {}
        decision_trace = snap.get("decision_trace", {}) or {}
        need_name = deliberation.get("dominant_need", "—")
        need_val = None
        emo_name = deliberation.get("dominant_emotion", "—")
        emo_val = None
        if isinstance(decision_trace.get("dominant_need"), dict):
            need_name = decision_trace["dominant_need"].get("name", need_name)
            need_val = decision_trace["dominant_need"].get("value")
        if isinstance(decision_trace.get("dominant_emotion"), dict):
            emo_name = decision_trace["dominant_emotion"].get("name", emo_name)
            emo_val = decision_trace["dominant_emotion"].get("value")
        if deliberation or decision_trace:
            self._deliberation_group.setVisible(True)
            if isinstance(need_val, (int, float)):
                self._delib_need_label.setText(
                    f"<b>Besoin dominant :</b> {need_name} {need_val:.0%}"
                )
            else:
                self._delib_need_label.setText(
                    f"<b>Besoin dominant :</b> {need_name}"
                )
            if isinstance(emo_val, (int, float)):
                self._delib_emotion_label.setText(
                    f"<b>Émotion dominante :</b> {emo_name} {emo_val:.0%}"
                )
            else:
                self._delib_emotion_label.setText(
                    f"<b>Émotion dominante :</b> {emo_name}"
                )
            selected = deliberation.get("selected")
            if selected:
                verb = selected.get("verb", "—")
                target_kind = selected.get("target_kind", "—")
                target_id = selected.get("target_id")
                tx = selected.get("tx")
                ty = selected.get("ty")
                score = selected.get("score", 0)
                if target_id is not None:
                    cible = f"{target_kind} #{target_id}"
                else:
                    cible = f"{target_kind} ({tx},{ty})"
                self._delib_selected_label.setText(
                    f"<b>Choix :</b> {verb} → {cible} (score: {score:.2f})"
                )
            else:
                self._delib_selected_label.setText("<b>Choix :</b> aucun")
            reason = deliberation.get("reason", "")
            self._delib_reason_label.setText(
                f"<b>Raison :</b> {reason}" if reason else "<b>Raison :</b> —"
            )
            failure = (decision_trace.get("failure_reason", "")
                         or deliberation.get("failure_reason", ""))
            self._delib_failure_label.setText(
                f"<b>Échec :</b> {failure}" if failure else "<b>Échec :</b> aucun"
            )
        else:
            self._deliberation_group.setVisible(False)

        # === Contexte local (perception immédiate) ===
        local_ctx = snap.get("local_context", {}) or {}
        if local_ctx:
            self._local_context_group.setVisible(True)
            lines = []
            for key, value in local_ctx.items():
                if isinstance(value, float):
                    lines.append(f"  {key}: {value:.2f}")
                else:
                    lines.append(f"  {key}: {value}")
            self._local_context_label.setText(
                "<b>Perception locale :</b>\n" + "\n".join(lines)
            )
        else:
            self._local_context_group.setVisible(False)

        # === Decision Trace (consolidation compacte des 10 éléments) ===
        self._fill_decision_trace(snap)

        # === Possibilités évaluées (trace réelle, aucune recomputation) ===
        # Refresh intelligent : on ne reconstruit la grille que si la
        # révision décision a changé (eid, tick, échec, activité, comm).
        revision = self._decision_revision_of(snap)
        if revision != self._decision_revision:
            self._decision_revision = revision
            self._fill_possibilities(snap)

        # === Lieux mémorisés pertinents (bornés à 8, moteur seul) ===
        places = snap.get("relevant_memories", []) or []
        if places:
            lines = []
            for row in places[:8]:
                lines.append(
                    f"  {row.get('category', '?')} à "
                    f"({row.get('tx', '?')},{row.get('ty', '?')}) · "
                    f"conf {float(row.get('confidence', 0.0)):.0%} · "
                    f"danger {float(row.get('estimated_danger', 0.0)):.0%} · "
                    f"{row.get('source', '')}"
                )
            self._places_label.setText("\n".join(lines))
            self._places_group.setVisible(True)
        else:
            self._places_group.setVisible(False)
            self._places_label.setText("")

        # === Communication (dernier envoi / réception) ===
        said = snap.get("last_said", {}) or {}
        heard = snap.get("last_heard", {}) or {}
        if said or heard:
            self._comm_group.setVisible(True)
            self._comm_said_label.setText(
                f"Envoyé : {self._format_comm(said)}" if said
                else "Envoyé : —"
            )
            self._comm_heard_label.setText(
                f"Reçu : {self._format_comm(heard)}" if heard
                else "Reçu : —"
            )
        else:
            self._comm_group.setVisible(False)
            self._comm_said_label.setText("")
            self._comm_heard_label.setText("")

        # Goal (action + destination + expiration)
        goal = snap.get("goal", {})
        if goal and goal.get("action_name"):
            dist = goal.get("distance_px")
            dist_str = f", {dist:.0f}px" if dist else ""
            target_x = goal.get("target_x")
            target_y = goal.get("target_y")
            target_str = ""
            if target_x is not None and target_y is not None:
                target_str = f" → ({target_x}, {target_y})"
            until = goal.get("until_tick")
            until_str = f", jusqu'au tick {until}" if until is not None else ""
            self._goal_label.setText(
                f"<b>But:</b> {goal['action_name']}{target_str}"
                f"{dist_str}{until_str}"
            )
        else:
            self._goal_label.setText("<b>But:</b> aucun")

    def _update_cards(self, snap):
        """Remplit les cartes visuelles (Lot F.1) avec les vraies clés.

        Santé = ``health`` ; les sept autres cartes = ``needs_named``
        (libellés NEED_DEFS : faim, énergie, soif, sommeil, sécurité,
        appartenance, estime). Toutes ces valeurs sont déjà en 0..1.
        """
        needs = snap.get("needs_named", {}) or {}
        values = {
            "sante": snap.get("health", 0.0),
            "energie": needs.get("énergie", 0.0),
            "faim": needs.get("faim", 0.0),
            "soif": needs.get("soif", 0.0),
            "sommeil": needs.get("sommeil", 0.0),
            "securite": needs.get("sécurité", 0.0),
            "appartenance": needs.get("appartenance", 0.0),
            "estime": needs.get("estime", 0.0),
        }
        for key, value in values.items():
            card = self._cards.get(key)
            if card is None:
                continue
            try:
                card.set_value(float(value), suffix="%")
            except (TypeError, ValueError):
                card.set_value("—")

    def _clear_cards(self):
        """Vide toutes les cartes (aucun habitant sélectionné)."""
        for card in self._cards.values():
            card.set_value("—")

    def _clear_grid(self, grid):
        """Retire tous les widgets d'un QGridLayout."""
        while grid.count():
            item = grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    @staticmethod
    def _decision_revision_of(snap: dict) -> tuple:
        """Révision UI-only : identique => on ne reconstruit pas la grille."""
        trace = snap.get("decision_trace", {}) or {}
        activity = snap.get("activity", {}) or {}
        possibilities = snap.get("possibilities", []) or []
        sel = next((r for r in possibilities
                    if r.get("state") == "selected"), None) or {}
        return (
            snap.get("eid"),
            trace.get("tick"),
            trace.get("failure_tick"),
            trace.get("failure_reason"),
            sel.get("verb"), sel.get("target_kind"), sel.get("target_id"),
            round(float(sel.get("score", 0.0)), 4) if sel else None,
            len(possibilities),
            activity.get("state"), activity.get("goal_action"),
            activity.get("stuck"),
            (snap.get("last_heard", {}) or {}).get("tick"),
            (snap.get("last_said", {}) or {}).get("tick"),
            (snap.get("last_decision", {}) or {}).get("tick"),
            (snap.get("last_decision", {}) or {}).get("act"),
        )

    @staticmethod
    def _format_comm(evt: dict) -> str:
        """Formate un événement talk / need_help borné (moteur seul)."""
        if not isinstance(evt, dict) or not evt:
            return "—"
        topic = evt.get("topic", evt.get("kind", "?"))
        tick = evt.get("tick", "—")
        if evt.get("kind") == "need_help":
            return (f"need_help de #{evt.get('requester_eid', '?')} "
                    f"(tick {tick})")
        speaker = evt.get("speaker_eid", "?")
        listener = evt.get("listener_eid", "?")
        return f"{topic} #{speaker} → #{listener} (tick {tick})"

    def _fill_decision_trace(self, snap):
        """Remplit la section compacte « Decision Trace » (10 éléments).

        Lecture seule du snapshot : aucune recomputation moteur.
        1 besoin · 2 émotion · 3 but · 4 activité · 5 candidats ·
        6 choix · 7 raison · 8 échec · 9 reçu · 10 envoyé.
        """
        deliberation = snap.get("deliberation", {}) or {}
        trace = snap.get("decision_trace", {}) or {}
        activity = snap.get("activity", {}) or {}
        goal = snap.get("goal", {}) or {}
        possibilities = snap.get("possibilities", []) or []
        said = snap.get("last_said", {}) or {}
        heard = snap.get("last_heard", {}) or {}

        # 1. Besoin dominant (fusion : nom le plus parlant des 2 sources)
        need = deliberation.get("dominant_need", "") or "—"
        nd = trace.get("dominant_need")
        if isinstance(nd, dict):
            nd_name = str(nd.get("name", "") or "")
            nd_val = float(nd.get("value", 0.0) or 0.0)
            if nd_name:
                need = f"{nd_name} {nd_val:.0%}"
            elif isinstance(need, dict):
                need = "—"
        self._dtrace_labels[0].setText(f"<b>1. Besoin :</b> {need}")

        # 2. Émotion dominante
        emo = deliberation.get("dominant_emotion", "") or "—"
        ed = trace.get("dominant_emotion")
        if isinstance(ed, dict):
            ed_name = str(ed.get("name", "") or "")
            ed_val = float(ed.get("value", 0.0) or 0.0)
            if ed_name:
                emo = f"{ed_name} {ed_val:.0%}"
            elif isinstance(emo, dict):
                emo = "—"
        self._dtrace_labels[1].setText(f"<b>2. Émotion :</b> {emo}")

        # 3. But courant / action / cible (snapshot goal, repli activité)
        goal_snap = snap.get("goal", {}) or {}
        action_text = ""
        if goal_snap.get("action") is not None:
            action_text = str(goal_snap.get("action_name") or "")
        if not action_text and activity.get("goal_action") is not None:
            action_text = action_name(self.controller.sim,
                                      activity.get("goal_action")) or ""
        if not action_text or action_text.lower() in ("—", "aucune", "aucun"):
            action_text = "aucun"
        gx, gy = goal_snap.get("target_x"), goal_snap.get("target_y")
        if gx is None or gy is None:
            gt = activity.get("goal_tile")
            if gt:
                gx, gy = gt[0], gt[1]
        target_text = f"→ ({int(gx)},{int(gy)})" if gx is not None and gy is not None else ""
        self._dtrace_labels[2].setText(
            f"<b>3. But :</b> {action_text} {target_text}"
        )

        # 4. Activité persistante + étape
        kind = activity.get("kind", "—")
        stage = activity.get("stage", "—")
        if kind and kind != "—":
            self._dtrace_labels[3].setText(
                f"<b>4. Activité :</b> {kind} · étape {stage}"
            )
        else:
            self._dtrace_labels[3].setText("<b>4. Activité :</b> aucune")

        # 5. Candidats évalués (jusqu'à 8).
        #    Source de vérité = les actions notées par le cerveau à la
        #    dernière délibération (c'est ce que le moteur évalue réellement
        #    dans _decide). Les ActionCandidate (cibles concrètes) ne sont
        #    produites que par le diagnostic : repli uniquement.
        last_dec = snap.get("last_decision", {}) or {}
        top = (last_dec.get("top") or [])[:8]
        if top:
            chosen_act = last_dec.get("act")
            parts = []
            for t in top:
                name = str(t.get("name", "?"))
                prob = float(t.get("prob", 0.0) or 0.0)
                mark = "faisable" if t.get("feasible") else "non faisable"
                arrow = "→ " if t.get("act") == chosen_act else ""
                parts.append(f"{arrow}{name} {prob:.0%} ({mark})")
            self._dtrace_labels[4].setText(
                "<b>5. Candidats :</b> " + " · ".join(parts)
            )
        elif possibilities:
            parts = []
            for row in possibilities[:8]:
                v = self.POSS_VERB.get(row.get("verb"), row.get("verb", "?"))
                st = self.POSS_STATE.get(row.get("state", ""), row.get("state", ""))
                sc = float(row.get("score", 0.0))
                reason = row.get("reason")
                entry = f"{v} ({st} {sc:.2f}"
                entry += f" — {reason})" if reason else ")"
                parts.append(entry)
            self._dtrace_labels[4].setText(
                "<b>5. Candidats (cibles) :</b> " + " · ".join(parts)
            )
        else:
            self._dtrace_labels[4].setText("<b>5. Candidats :</b> aucun")

        # 6. Candidat sélectionné — ordre de vérité :
        #    a) activité en cours = aucune délibération ce tick (le moteur
        #       sort avant _decide) ; on l'explique et on rappelle le
        #       dernier choix historique s'il existe ;
        #    b) décision réellement retenue par _decide ;
        #    c) pick du diagnostic = hypothèse, jamais présenté comme réel.
        sel = next((r for r in possibilities
                    if r.get("state") == "selected"), None)
        sel_desc = deliberation.get("selected") or {}
        has_dec = bool(last_dec.get("act_name")
                       and last_dec.get("act_name") != "—")

        def _decision_text(prefix):
            prob = float(last_dec.get("prob", 0.0) or 0.0)
            tick = last_dec.get("tick", "?")
            repli = (last_dec.get("initial_act_name")
                     and last_dec.get("initial_act") != last_dec.get("act"))
            if repli:
                # Après repli, la prob de l'action retenue est souvent ~0 :
                # on affiche celle de l'action initiale, bien plus parlante.
                ip = float(last_dec.get("initial_prob", 0.0) or 0.0)
                return (f"{prefix}{last_dec['act_name']} (repli, tick {tick})"
                        f" — « {last_dec['initial_act_name']} » à {ip:.0%}"
                        f" non faisable")
            # Les alternatives complètes sont déjà en ligne 5.
            return (f"{prefix}{last_dec['act_name']} "
                    f"({prob:.0%}, tick {tick})")

        if activity.get("kind"):
            if has_dec:
                text = _decision_text("")
                text = (f"<b>6. Choix :</b> aucun — délibération en attente "
                        f"(activité « {activity.get('kind')} » en cours)"
                        f" · dernier choix : {text}")
            else:
                text = (f"<b>6. Choix :</b> aucun — délibération en attente "
                        f"(activité « {activity.get('kind')} » en cours)")
            self._dtrace_labels[5].setText(text)
        elif has_dec:
            self._dtrace_labels[5].setText(_decision_text(
                "<b>6. Choix :</b> "))
        elif sel:
            verb_t = self.POSS_VERB.get(sel.get("verb"), sel.get("verb", "?"))
            kind_t = self.POSS_TARGET.get(
                sel.get("target_kind"), sel.get("target_kind", "?"))
            tid = sel.get("target_id")
            cible = f"{kind_t} #{tid}" if tid is not None else (
                f"{kind_t} ({sel.get('tx')},{sel.get('ty')})")
            self._dtrace_labels[5].setText(
                f"<b>6. Choix :</b> {verb_t} → {cible} "
                f"(hypothèse — pas encore délibéré)"
            )
        elif sel_desc:
            self._dtrace_labels[5].setText(
                f"<b>6. Choix :</b> {sel_desc.get('verb','?')}"
            )
        else:
            self._dtrace_labels[5].setText("<b>6. Choix :</b> aucun")

        # 7. Raison : l'activité explique l'absence de délibération, sinon
        #    la raison réelle du choix moteur, sinon le diagnostic.
        if activity.get("kind"):
            reason = (f"l'activité « {activity.get('kind')} » pilote l'agent "
                      f"(étape {activity.get('stage', '?')}) — pas de "
                      f"délibération ce tick")
        else:
            reason = (last_dec.get("reason", "")
                      or deliberation.get("reason", ""))
        self._dtrace_labels[6].setText(
            f"<b>7. Raison :</b> {reason}" if reason
            else "<b>7. Raison :</b> —"
        )

        # 8. Dernier échec / interruption
        failure = (trace.get("failure_reason", "")
                   or deliberation.get("failure_reason", ""))
        self._dtrace_labels[7].setText(
            f"<b>8. Échec :</b> {failure}" if failure
            else "<b>8. Échec :</b> aucun"
        )

        # 9. Dernière communication reçue
        if heard:
            topic = heard.get("topic") or heard.get("kind", "?")
            tick = heard.get("tick", "?")
            who = heard.get("speaker_name") or heard.get("requester_eid", "")
            suffix = f" de {who}" if who not in ("", None) else ""
            self._dtrace_labels[8].setText(
                f"<b>9. Reçu :</b> {topic}{suffix} (tick {tick})"
            )
        else:
            self._dtrace_labels[8].setText("<b>9. Reçu :</b> —")

        # 10. Dernière communication envoyée
        if said:
            topic = said.get("topic") or said.get("kind", "?")
            tick = said.get("tick", "?")
            who = said.get("listener_name") or said.get("listener_eid", "")
            suffix = f" → {who}" if who not in ("", None) else ""
            self._dtrace_labels[9].setText(
                f"<b>10. Envoyé :</b> {topic}{suffix} (tick {tick})"
            )
        else:
            self._dtrace_labels[9].setText("<b>10. Envoyé :</b> —")

        self._dtrace_group.setVisible(True)

    def _fill_possibilities(self, snap):
        """Affiche la trace de décision : Action | Cible | Distance | Risque |
        Score | État. ``snap`` provient du snapshot (déjà évalué par le
        moteur) ; cette méthode ne fait que le mettre en forme.

        Deux sources, par ordre de vérité :
        1. les ``ActionCandidate`` (cibles concrètes) quand le diagnostic en
           a produit — c'est la forme historique de cette grille ;
        2. à défaut, les actions notées par le cerveau à la dernière
           délibération : elles sont presque toujours disponibles, alors que
           les cibles sont vides dans un monde sans objet/voisin proche.
        """
        rows = snap.get("possibilities", []) or []
        last_dec = snap.get("last_decision", {}) or {}
        top = (last_dec.get("top") or [])[:8]
        grid = self._possibilities_grid
        self._clear_grid(grid)
        self._possibilities_group.setVisible(True)
        if not rows and not top:
            self._possibilities_empty.setVisible(True)
            return
        self._possibilities_empty.setVisible(False)

        for col, header in enumerate(
                ("Action", "Cible", "Distance", "Risque", "Score", "État")):
            lbl = QLabel(f"<b>{header}</b>")
            lbl.setStyleSheet("font-size: 10px; color: #697281;")
            grid.addWidget(lbl, 0, col)

        if rows:
            for r, row in enumerate(rows[:8], start=1):
                verb = self.POSS_VERB.get(row.get("verb"), row.get("verb", "—"))
                kind = self.POSS_TARGET.get(
                    row.get("target_kind"), row.get("target_kind", ""))
                tid = row.get("target_id")
                if tid is not None:
                    cible = f"{kind} #{tid}"
                else:
                    cible = f"{kind} ({row.get('tx')},{row.get('ty')})"
                state_raw = row.get("state", "—")
                state = self.POSS_STATE.get(state_raw, state_raw)
                reason = row.get("reason")
                state_text = f"{state} — {reason}" if reason else state
                cells = (
                    str(verb),
                    str(cible),
                    str(row.get("distance", 0)),
                    f"{float(row.get('estimated_risk', 0.0)):.2f}",
                    f"{float(row.get('score', 0.0)):.2f}",
                    str(state_text),
                )
                selected = state_raw == "selected"
                for col, text in enumerate(cells):
                    lbl = QLabel(text)
                    if selected and col == 5:
                        lbl.setStyleSheet(
                            "font-size: 10px; color: #62D394; font-weight: bold;")
                    else:
                        lbl.setStyleSheet("font-size: 10px;")
                    grid.addWidget(lbl, r, col)
            return

        # Source 2 : actions notées par le cerveau (pas de cible concrète).
        chosen_act = last_dec.get("act")
        tick = last_dec.get("tick", "?")
        for r, t in enumerate(top, start=1):
            is_choice = t.get("act") == chosen_act
            prob = float(t.get("prob", 0.0) or 0.0)
            feasible = bool(t.get("feasible"))
            state_text = "faisable" if feasible else "non faisable"
            cells = (
                f"{'→ ' if is_choice else ''}{t.get('name', '?')}",
                "—", "—", "—",
                f"{prob:.2f}",
                state_text,
            )
            for col, text in enumerate(cells):
                lbl = QLabel(text)
                if is_choice and col in (0, 5):
                    lbl.setStyleSheet(
                        "font-size: 10px; color: #62D394; font-weight: bold;")
                else:
                    lbl.setStyleSheet("font-size: 10px;")
                grid.addWidget(lbl, r, col)
        note = QLabel(f"Actions notées par le cerveau — délibération tick {tick}.")
        note.setStyleSheet("font-size: 10px; color: #697281;")
        grid.addWidget(note, len(top) + 1, 0, 1, 6)

    def _agent_label(self, eid):
        """Libelle lisible d'un habitant par son eid (vivant ou defunt)."""
        if eid is None:
            return "—"
        try:
            eid = int(eid)
        except (TypeError, ValueError):
            return "—"
        for agent in self.controller.sim.agents:
            if agent.eid == eid:
                suffix = "" if agent.alive else ", mort"
                return f"{agent.name} (#{eid}{suffix})"
        for rec in getattr(self.controller.sim, "deceased", ()):
            if isinstance(rec, dict) and rec.get("eid") == eid:
                return f"{rec.get('name', '?')} (#{eid}, mort)"
        return f"#{eid}"

    def _extract_needs(self, snap):
        """Extrait les besoins en dictionnaire (cles = cles des sliders)."""
        needs = snap.get("needs_named", {}) or {}
        return {
            "faim": needs.get("faim", 0),
            "energie": needs.get("énergie", 0),
            "soif": needs.get("soif", 0),
            "sommeil": needs.get("sommeil", 0),
            "securite": needs.get("sécurité", 0),
            "appartenance": needs.get("appartenance", 0),
            "estime": needs.get("estime", 0),
            "sante": snap.get("health", 0),
        }

    def _fill_grid(self, grid, data):
        """Remplit un QGridLayout avec des paires label/valeur."""
        # Clear existing
        while grid.count():
            item = grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not data:
            return
        for i, (key, val) in enumerate(data.items()):
            row, col = divmod(i, 2)
            lbl = QLabel(f"{key}:")
            lbl.setStyleSheet("color: #697281; font-size: 11px;")
            val_lbl = QLabel(f"{val:.2f}" if isinstance(val, float) else str(val))
            val_lbl.setStyleSheet("font-size: 11px;")
            grid.addWidget(lbl, row, col * 2)
            grid.addWidget(val_lbl, row, col * 2 + 1)


def _format_episode(ep):
    """Entree d'``agent.episodes`` : ``(tick, type, data)`` -> texte lisible."""
    if isinstance(ep, (tuple, list)) and len(ep) >= 2:
        tick, kind = ep[0], ep[1]
        data = ep[2] if len(ep) > 2 else None
        text = f"t{tick} · {kind}"
        if isinstance(data, dict) and data:
            detail = ", ".join(
                f"{key}={value:.2f}" if isinstance(value, float)
                else f"{key}={value}"
                for key, value in data.items()
            )
        elif data:
            detail = str(data)
        else:
            detail = ""
        return f"{text} — {detail}" if detail else text
    return str(ep)


def _format_event(ev):
    """Entree d'``agent.life`` : texte simple ou ``(type, nom)``."""
    if isinstance(ev, (tuple, list)) and len(ev) >= 2:
        return " — ".join(str(part) for part in ev[:2])
    return str(ev)


def _hex(t):
    return f"#{t[0]:02x}{t[1]:02x}{t[2]:02x}"
