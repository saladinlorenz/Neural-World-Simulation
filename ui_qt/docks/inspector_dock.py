"""InspectorDock — dock Qt pour l'inspecteur d'habitant selectionne."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                              QTableView, QLabel, QScrollArea, QFrame,
                              QGroupBox, QGridLayout, QSlider)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from game.ui_snapshots import selected_agent_snapshot, anima_snapshot
from game.ui_registry import C_CORPS, C_COG, C_PERSO, C_EMO, C_BESOIN, C_EXP, C_MEM
from ui_qt.models.anima_model import AnimaModel


class InspectorDock(QDockWidget):
    """Dock inspecteur complet : identite + corps + Anima + relations."""

    def __init__(self, controller, parent=None):
        super().__init__("Inspecteur", parent)
        self.controller = controller
        self._anima_model = AnimaModel()
        self._setup_ui()

    def _setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        widget = QWidget()
        self._layout = QVBoxLayout(widget)
        self._layout.setContentsMargins(8, 8, 8, 8)
        self._layout.setSpacing(6)

        # === Identite ===
        self._identity_label = QLabel("Aucun agent selectionne")
        self._identity_label.setWordWrap(True)
        self._identity_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self._layout.addWidget(self._identity_label)

        # === Etat de base ===
        self._state_label = QLabel("")
        self._state_label.setWordWrap(True)
        self._layout.addWidget(self._state_label)

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
        self._autobio_label = QLabel("")
        self._autobio_label.setWordWrap(True)
        self._autobio_label.setStyleSheet("font-size: 11px;")
        mem_layout.addWidget(self._autobio_label)
        self._layout.addWidget(self._memory_group)

        # === Relations ===
        self._relations_label = QLabel("")
        self._relations_label.setWordWrap(True)
        self._layout.addWidget(self._relations_label)

        # === Goal ===
        self._goal_label = QLabel("")
        self._goal_label.setWordWrap(True)
        self._layout.addWidget(self._goal_label)

        self._layout.addStretch()

        scroll.setWidget(widget)
        self.setWidget(scroll)

    def _create_info_groups(self):
        """Cree les groupes Corps, Cognition, Personnalite, Emotions, Besoins."""
        self._groups = {}
        for key, title, color in [
            ("body", "Corps", C_CORPS),
            ("cog", "Cognition", C_COG),
            ("perso", "Personnalite", C_PERSO),
            ("emo", "Emotions", C_EMO),
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
                lambda k=key, s=slider: self.controller.execute({
                    "kind": "set_agent_stat",
                    "eid": self.controller.ui_state.selected_agent_eid,
                    "stat": k,
                    "value": s.value() / 100.0,
                })
            )
        self._layout.addWidget(needs_group)

    def refresh(self):
        snap = selected_agent_snapshot(self.controller.sim, self.controller.ui_state)
        anima_snap = anima_snapshot(self.controller.sim, self.controller.ui_state)

        if snap is None:
            self._identity_label.setText("Aucun agent selectionne")
            self._state_label.setText("")
            self._anima_model.set_snapshot(None)
            for group, _ in self._groups.values():
                group.setVisible(False)
            self._brain_group.setVisible(False)
            self._inventory_group.setVisible(False)
            self._tool_group.setVisible(False)
            self._memory_group.setVisible(False)
            self._relations_label.setText("")
            self._goal_label.setText("")
            return

        # Identite
        nom = snap.get("nom", "?")
        sex = snap.get("sexe", snap.get("sex", "?"))
        stage = snap.get("stage", "")
        age = snap.get("age_ans", 0)
        cls = snap.get("classe", "")
        clan = snap.get("clan", "")
        gen = snap.get("generation", 0)
        self._identity_label.setText(
            f"<b>{nom}</b> ({sex}) — {stage}, {age:.1f} ans, {cls}, "
            f"clan {clan}, gen {gen}"
        )

        # Etat
        sante = snap.get("sante", 0)
        energie = snap.get("energie", 0)
        faim = snap.get("faim", 0)
        douleur = snap.get("douleur", 0)
        self._state_label.setText(
            f"Sante: {sante:.0%} | Energie: {energie:.0%} | "
            f"Faim: {faim:.0%} | Douleur: {douleur:.1f}"
        )

        # Groupes d'info
        for key, data in [
            ("body", snap.get("corps", {})),
            ("cog", snap.get("cognition", {})),
            ("perso", snap.get("personnalite", {})),
            ("emo", snap.get("emotions", {})),
        ]:
            if key in self._groups:
                group, grid = self._groups[key]
                self._fill_grid(grid, data)
                group.setVisible(bool(data))

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
        brain = snap.get("cerveau", {})
        if brain:
            neurons = brain.get("neurones", 0)
            freq = brain.get("frequence_reflexion", 0)
            rank = brain.get("classement_actions", [])
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
        inventory = snap.get("inventaire", {})
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
        tool = snap.get("outil", None)
        if tool:
            dur = snap.get("durabilite_outil", 0)
            tool_name = tool if isinstance(tool, str) else str(tool)
            self._tool_label.setText(f"{tool_name} (durabilite: {dur})")
            self._tool_group.setVisible(True)
        else:
            self._tool_label.setText("Aucun")
            self._tool_group.setVisible(True)

        # === Memoire / croyances ===
        beliefs = snap.get("croyances_danger", snap.get("memoire", {}))
        episodes = snap.get("episodes", [])
        has_belief = bool(beliefs)
        has_episodes = bool(episodes)
        if has_belief or has_episodes:
            self._memory_group.setVisible(True)
            if has_belief:
                belief_lines = []
                for place_type, belief_val in beliefs.items():
                    if isinstance(belief_val, dict):
                        belief = belief_val.get("belief", belief_val.get("b", "?"))
                        conf = belief_val.get("confidence", belief_val.get("c", 0))
                        belief_lines.append(
                            f"{place_type}: {belief} (confiance: {conf:.0%})"
                        )
                    else:
                        belief_lines.append(f"{place_type}: {belief_val}")
                self._belief_label.setText(
                    "<b>Croyances:</b>\n" + "\n".join(belief_lines)
                )
            else:
                self._belief_label.setText("<b>Croyances:</b> aucune")

            if has_episodes:
                last5 = episodes[-5:]
                epi_lines = []
                for i, ep in enumerate(last5):
                    epi_lines.append(f"  [{i+1}] {ep}")
                self._autobio_label.setText(
                    "<b>Autobiographie:</b>\n" + "\n".join(epi_lines)
                )
            else:
                self._autobio_label.setText("<b>Autobiographie:</b> aucune")
        else:
            self._memory_group.setVisible(False)

        # Anima
        self._anima_model.set_snapshot(anima_snap or snap)

        # Relations
        rels = snap.get("relations", [])
        if rels:
            lines = []
            for r in rels[:5]:
                conf = r.get("confiance", 0)
                aff = r.get("affection", 0)
                vivant = "vivant" if r.get("vivant", False) else "mort"
                lines.append(f"  {r['nom']}: conf={conf:.2f} aff={aff:.2f} ({vivant})")
            self._relations_label.setText(
                "<b>Relations:</b>\n" + "\n".join(lines)
            )
        else:
            self._relations_label.setText("<b>Relations:</b> aucune")

        # Goal
        goal = snap.get("but", {})
        if goal and goal.get("action_nom"):
            dist = goal.get("distance_px")
            dist_str = f", {dist:.0f}px" if dist else ""
            self._goal_label.setText(
                f"<b>But:</b> {goal['action_nom']}{dist_str}"
            )
        else:
            self._goal_label.setText("<b>But:</b> aucun")

    def _extract_needs(self, snap):
        """Extrait les besoins en dictionnaire."""
        return {
            "faim": snap.get("faim", 0),
            "energie": snap.get("energie", 0),
            "soif": snap.get("soif", 0),
            "sommeil": snap.get("sommeil", 0),
            "securite": snap.get("securite", 0),
            "appartenance": snap.get("appartenance", 0),
            "estime": snap.get("estime", 0),
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


def _hex(t):
    return f"#{t[0]:02x}{t[1]:02x}{t[2]:02x}"
