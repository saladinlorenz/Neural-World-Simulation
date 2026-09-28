"""MainWindow — QMainWindow principale de l'interface PyQt6."""
from PyQt6.QtWidgets import (QMainWindow, QToolBar, QLabel,
                              QSpinBox, QStatusBar, QPushButton,
                              QInputDialog, QMessageBox, QMenu)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction

from game.ui_snapshots import simulation_snapshot
from game.ui_commands import execute_command
from ui_qt.map.map_view import MapView
from ui_qt.docks.population_dock import PopulationDock
from ui_qt.docks.inspector_dock import InspectorDock
from ui_qt.docks.anima_dock import AnimaDock
from ui_qt.docks.journal_dock import JournalDock
from ui_qt.docks.society_dock import SocietyDock
from ui_qt.docks.assets_dock import AssetsDock
from ui_qt.docks.tools_dock import ToolsDock
from ui_qt.docks.tile_dock import TileDock
from ui_qt.dialogs import SaveDialog, SpawnAgentDialog, ToolEditorDialog
from ui_qt.theme.theme import apply_theme, get_theme_name
from ui_qt.widgets.status_pill import StatusPill
from ui_qt.studio.parameter_dock import ParameterDock
from ui_qt.studio.scenario_dialog import ScenarioDialog
from game.studio_scenarios import get_scenario
from ui_qt.studio.timeline_dock import TimelineDock
from ui_qt.studio.laboratory_dock import LaboratoryDock
from ui_qt.studio.comparison_panel import ComparisonPanel
from ui_qt.studio.world_overlay import WorldOverlay


TICK_BUDGET_MS = 50


class MainWindow(QMainWindow):
    """Fenêtre principale PyQt6 avec docks, barre d'outils et carte."""

    def __init__(self, controller, am=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.am = am
        # Le scenario vit sur la fenetre, pas sur ``sim`` : ``reset_world`` et
        # le chargement reconstruisent le Sim et perdraient l'etiquette.
        self._active_scenario = "manual"
        self.setWindowTitle("Univers Vivant — PyQt6")
        self.setMinimumSize(1200, 800)

        apply_theme(self)

        self._setup_toolbar()
        self._setup_central()
        # La barre d'état porte le canal d'erreur : elle doit exister avant
        # les docks, dont la construction peut déjà émettre des commandes.
        self._setup_statusbar()
        self._setup_docks()
        # Lot B-fix : UIState.active_mode vaut « agent » par défaut
        # (game/ui_state.py, valeur verifiee par un test qu'on ne touche pas),
        # donc tout clic sur la carte aurait posé un habitant. On demarre en
        # mode « examen » : le clic selectionne / examine au lieu de creer.
        # Placé après _setup_docks (le dock Outils existe) et avant
        # _restore_settings, pour qu'un chargement puisse surcharger le mode.
        # Le dock Outils reste la source explicite : choisir « Etre », c'est
        # demander des clics repetes pour creer — c'est voulu.
        self.report_command_result(
            self.controller.execute({"kind": "set_mode", "mode": "inspect"}))
        self._tools_dock.refresh()
        self._setup_timer()
        self._restore_settings()
        # main_qt applique ui_state sauvegarde AVANT la creation de la
        # fenetre : l'overlay restaure doit rejoindre combo + carte ici.
        self._apply_active_overlay()

    def add_menu_action(self, menu, text, slot, shortcut=None, tooltip=None):
        """Ajoute une entree de menu (Lot B) avec raccourci optionnel.

        L'action est aussi rattachee a la fenetre : rangee dans un menu de
        bouton, elle doit garder son raccourci actif au niveau fenetre.
        """
        action = QAction(text, self)
        if shortcut:
            action.setShortcut(shortcut)
            self.addAction(action)
        if tooltip:
            action.setToolTip(tooltip)
        action.triggered.connect(slot)
        menu.addAction(action)
        return action

    def _setup_toolbar(self):
        tb = QToolBar("Controle")
        tb.setObjectName("toolbar_controle")
        tb.setMovable(False)
        self.addToolBar(tb)

        # ── Groupe simulation : pause, pas, presets de vitesse ──
        self._pause_action = QAction("Pause", self)
        self._pause_action.setShortcut("Space")
        self._pause_action.setToolTip("Espace : met en pause / reprend la simulation")
        self._pause_action.triggered.connect(self._on_pause)
        tb.addAction(self._pause_action)

        step_action = QAction("Step", self)
        step_action.setShortcut("N")
        step_action.setToolTip("N : avance la simulation d'un tick")
        step_action.triggered.connect(self._on_step)
        tb.addAction(step_action)

        tb.addSeparator()

        # Presets de vitesse (les raccourcis 1..8 sont plus bas)
        for speed in [1, 2, 4, 8]:
            btn = QPushButton("%d×" % speed)
            btn.setFixedWidth(42)
            btn.setToolTip("Vitesse %dx (touche %d du clavier)" % (speed, speed))
            btn.clicked.connect(lambda checked, s=speed: self._set_speed(s))
            tb.addWidget(btn)

        tb.addSeparator()

        # ── Creation d'habitant : une seule QAction Ctrl+H, partagee avec
        # le menu Vue (aucun raccourci duplique) ──
        spawn_custom = QAction("Créer un habitant…", self)
        spawn_custom.setShortcut("Ctrl+H")
        spawn_custom.setToolTip("Sexe, clan, classe, cerveau, energie, nom et "
                                "gabarits : le prochain clic sur la carte pose "
                                "cet habitant.")
        spawn_custom.triggered.connect(self._open_spawn_dialog)
        self.addAction(spawn_custom)
        # Reference partagee avec le menu Vue : une seule QAction garde
        # le raccourci Ctrl+H sans ambiguite.
        self._spawn_custom_action = spawn_custom

        # ── Menu Créer ▾ ──
        create_btn = QPushButton("Créer ▾")
        create_btn.setProperty("role", "primary")
        create_btn.setToolTip("Ajouter un habitant, un mouton ou un monstre")
        create_menu = QMenu(create_btn)
        self.add_menu_action(
            create_menu, "Habitant aléatoire", self._menu_spawn_agent,
            tooltip="Ajoute un habitant aleatoire dans le monde")
        create_menu.addAction(self._spawn_custom_action)
        self.add_menu_action(
            create_menu, "Mouton", self._menu_spawn_sheep,
            tooltip="Ajoute un mouton (nourriture, laine)")
        self.add_menu_action(
            create_menu, "Monstre", self._menu_spawn_monster,
            tooltip="Type de monstre : aleatoire si aucun n'est choisi dans Outils")
        create_menu.addSeparator()
        self.add_menu_action(
            create_menu, "Éditeur d'outil…", self._open_tool_editor,
            tooltip="Dessine un outil 16x16 et l'enregistre au catalogue")
        create_btn.setMenu(create_menu)
        tb.addWidget(create_btn)

        # ── Menu Monde ▾ ──
        world_btn = QPushButton("Monde ▾")
        world_btn.setToolTip("Nouveau monde, scenarios, parametres, export")
        world_menu = QMenu(world_btn)
        self.add_menu_action(
            world_menu, "Nouveau monde…", self._on_new_world, "Ctrl+N",
            "Genere un nouveau monde (la partie actuelle est perdue)")
        self.add_menu_action(world_menu, "Scénarios…", self._open_scenarios)
        self.add_menu_action(
            world_menu, "Paramètres", lambda: self._toggle_dock(self._param_dock))
        # Une seule QAction Ctrl+E : deux actions de fenetre au meme
        # raccourci seraient « ambiguës » et Qt n'activerait aucune des deux.
        # La meme part avec le menu Vue (_setup_docks).
        self._export_action = QAction("Exporter l'image", self)
        self._export_action.setShortcut("Ctrl+E")
        self._export_action.setToolTip("Exporte l'image visible de la carte")
        self._export_action.triggered.connect(self._export_viewport)
        self.addAction(self._export_action)
        world_menu.addAction(self._export_action)
        world_btn.setMenu(world_menu)
        tb.addWidget(world_btn)

        # ── Menu Édition ▾ ──
        edit_btn = QPushButton("Édition ▾")
        edit_btn.setToolTip("Annuler, retablir, grille et legende")
        edit_menu = QMenu(edit_btn)
        self.add_menu_action(edit_menu, "Annuler", self._on_undo, "Ctrl+Z")
        self.add_menu_action(edit_menu, "Rétablir", self._on_redo, "Ctrl+Shift+Z")
        edit_menu.addSeparator()
        # Les memes QAction sont partagees avec le menu Vue (_setup_docks) :
        # un seul objet garde l'etat coche synchronise avec la carte.
        self._grid_action = QAction("Grille", self)
        self._grid_action.setCheckable(True)
        self._grid_action.setToolTip("Affiche ou masque la grille de tuiles")
        self._grid_action.triggered.connect(self._toggle_grid)
        edit_menu.addAction(self._grid_action)
        self._legend_action = QAction("Légende", self)
        self._legend_action.setCheckable(True)
        self._legend_action.setToolTip("Affiche ou masque la legende de la carte")
        self._legend_action.triggered.connect(self._toggle_legend)
        edit_menu.addAction(self._legend_action)
        edit_btn.setMenu(edit_menu)
        tb.addWidget(edit_btn)

        # ── Menu Studio ▾ ──
        studio_btn = QPushButton("Studio ▾")
        studio_btn.setToolTip("Timeline, laboratoire, comparaison A/B")
        studio_menu = QMenu(studio_btn)
        self.add_menu_action(
            studio_menu, "Timeline", lambda: self._toggle_dock(self._timeline_dock))
        self.add_menu_action(
            studio_menu, "Laboratoire", lambda: self._toggle_dock(self._lab_dock))
        self.add_menu_action(
            studio_menu, "Comparaison A/B", self._open_comparison)
        studio_menu.addSeparator()
        self.add_menu_action(
            studio_menu, "Configurer l'overlay", self._open_overlay_config)
        studio_btn.setMenu(studio_menu)
        tb.addWidget(studio_btn)

        tb.addSeparator()

        # ── Groupe lecture / sauvegarde / theme ──
        self._follow_action = QAction("Suivre", self)
        self._follow_action.setCheckable(True)
        self._follow_action.setToolTip(
            "Centre la camera sur l'habitant selectionne "
            "(la selection dans la liste l'active automatiquement)")
        self._follow_action.triggered.connect(self._on_follow)
        tb.addAction(self._follow_action)

        save_btn = QPushButton("Sauvegarder ▾")
        save_btn.setToolTip("F5 : quicksave (slot 0) — Maj+F5 : sauvegarder sous")
        save_menu = QMenu(save_btn)
        self.add_menu_action(
            save_menu, "Quicksave", self._on_quicksave, "F5",
            "Sauvegarde immediate dans le slot 0")
        self.add_menu_action(
            save_menu, "Sauvegarder sous…", self._on_save, "Shift+F5")
        save_btn.setMenu(save_menu)
        tb.addWidget(save_btn)

        load_action = QAction("Charger", self)
        load_action.setShortcut("F9")
        load_action.setToolTip("F9 : charger une partie")
        load_action.triggered.connect(self._on_load)
        self.addAction(load_action)
        tb.addAction(load_action)

        tb.addSeparator()

        # Theme toggle : l'intitule annonce la cible du clic (comme apres un
        # basculement dans _toggle_theme). Neural Lab sombre = defaut.
        self._theme_action = QAction(
            "Theme clair" if get_theme_name() == "sombre" else "Theme sombre",
            self)
        self._theme_action.setToolTip("Bascule entre le theme clair et le theme sombre")
        self._theme_action.triggered.connect(self._toggle_theme)
        tb.addAction(self._theme_action)

        tb.addSeparator()
        # Overlay mode selector
        from PyQt6.QtWidgets import QComboBox
        from ui_qt.studio.world_overlay import MODES as OVERLAY_MODES
        overlay = WorldOverlay()
        self._overlay_combo = QComboBox()
        # Les dix modes sont implémentés : n'en lister que sept rendait
        # culture / institutions / territoires inatteignables.
        for m in OVERLAY_MODES:
            self._overlay_combo.addItem(overlay.mode_label(m), m)
            self._overlay_combo.setItemData(
                OVERLAY_MODES.index(m) if m in OVERLAY_MODES else 0,
                overlay.mode_help(m),
                Qt.ItemDataRole.ToolTipRole,
            )
        self._overlay_combo.currentIndexChanged.connect(self._on_overlay_change)
        self._overlay_combo.setToolTip(
            "Vue normale = monde vivant. Overlay = réponse à UNE seule "
            "question scientifique (jamais cumulés).")
        tb.addWidget(QLabel("Vue: "))
        tb.addWidget(self._overlay_combo)

        # ── Alertes WORLD ALIVE : rares, significatives, actionnables ──
        # Un seul bouton : libellé = alerte la plus grave (+N autres).
        # Clic = sélectionne l'habitant concerné + centre la caméra.
        # Calcul pur O(n) dans _refresh_status (~5 Hz), jamais de spam.
        self._alert_btn = QPushButton("✓ Calme")
        self._alert_btn.setToolTip(
            "Alertes monde vivant : famine, soif, blocage, blessé, "
            "simulation lente. Clic = aller voir.")
        self._alert_btn.setFlat(True)
        self._alert_btn.clicked.connect(self._on_alert_click)
        tb.addWidget(self._alert_btn)
        self._current_alerts = []

        tb.addSeparator()
        # Curseur de vitesse (complement des presets : 1 a 8)
        tb.addWidget(QLabel(" Vitesse: "))
        self._speed_spin = QSpinBox()
        self._speed_spin.setRange(1, 8)
        self._speed_spin.setValue(self.controller.sim.speed)
        self._speed_spin.setToolTip("Vitesse de simulation (1 a 8)")
        self._speed_spin.valueChanged.connect(self._on_speed)
        tb.addWidget(self._speed_spin)

        # Bascule mode détail faible (Phase 6)
        self._low_detail_action = QAction("Détail faible (L)", self, checkable=True)
        self._low_detail_action.setShortcut("L")
        self._low_detail_action.setToolTip(
            "Mode détail faible : points au zoom loin, pas d'ombres/halos/effets")
        self._low_detail_action.toggled.connect(self._toggle_low_detail)
        tb.addAction(self._low_detail_action)

        # Bascule mode performance maximum
        self._perf_mode_action = QAction("Mode performance maximal (M)", self, checkable=True)
        self._perf_mode_action.setShortcut("M")
        self._perf_mode_action.setToolTip(
            "Mode performance : réduit la charge visuelle pour maintenir 60 FPS simulation")
        self._perf_mode_action.toggled.connect(self._toggle_performance_mode)
        tb.addAction(self._perf_mode_action)

        # Raccourcis clavier 1..8 : une touche = une vitesse
        for speed in range(1, 9):
            action = QAction("Vitesse %d" % speed, self)
            action.setShortcut(str(speed))
            action.triggered.connect(lambda checked, s=speed: self._set_speed(s))
            self.addAction(action)

    def _menu_spawn_agent(self):
        """Menu Créer ▾ « Habitant aléatoire » (ancien bouton + Habitants)."""
        result = self.report_command_result(
            self.controller.execute({"kind": "spawn_agent"}))
        if isinstance(result, dict) and result.get("ok"):
            self._status.showMessage(
                "Habitant ajouté — pour en placer un précisément : "
                "dock Outils ▸ Etre puis cliquez sur la carte", 6000)

    def _menu_spawn_sheep(self):
        """Menu Créer ▾ « Mouton » (ancien bouton + Mouton)."""
        result = self.report_command_result(
            self.controller.execute({"kind": "spawn_sheep"}))
        if isinstance(result, dict) and result.get("ok"):
            self._status.showMessage(
                "Mouton ajouté — pour en placer un précisément : "
                "dock Outils ▸ Mouton puis cliquez sur la carte", 6000)

    def _menu_spawn_monster(self):
        """Menu Créer ▾ « Monstre » (ancien bouton + Monstre)."""
        result = self._on_spawn_monster()
        if isinstance(result, dict) and result.get("ok"):
            self._status.showMessage(
                "Monstre ajouté — pour en placer un précisément : "
                "dock Outils ▸ Monstre puis cliquez sur la carte", 6000)

    def _setup_central(self):
        self._map = MapView(self.controller, self)
        self._map.command_result.connect(self.report_command_result)
        #: Tuile survolée par le curseur (Lot E.6).
        self._hover_tile = None
        self._map.hover_changed.connect(self._on_map_hover)
        self._map.map_clicked.connect(self._on_map_clicked)
        self.setCentralWidget(self._map)
        # Les actions Grille / Légende sont créées dans la barre d'outils
        # (avant la carte) : leur état initial suit les défauts de MapView.
        # setChecked n'émet pas triggered : aucun basculement parasite.
        self._grid_action.setChecked(self._map.debug_show_grid)
        self._legend_action.setChecked(self._map.show_legend)

    def _on_map_hover(self, tx, ty):
        self._hover_tile = (int(tx), int(ty))

    def _setup_docks(self):
        # Dock Habitants (gauche)
        self._pop_dock = PopulationDock(self.controller, self)
        self._pop_dock.setObjectName("dock_population")
        self._pop_dock.agent_selected.connect(self._on_agent_selected)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._pop_dock)

        # Dock Inspecteur (droite)
        self._inspector_dock = InspectorDock(self.controller, self)
        self._inspector_dock.setObjectName("dock_inspecteur")
        self._inspector_dock.command_result.connect(self.report_command_result)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self._inspector_dock)

        # Dock Anima (droite, tabule avec inspecteur) : esprit interne
        self._anima_dock = AnimaDock(self.controller, self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self._anima_dock)
        self.tabifyDockWidget(self._inspector_dock, self._anima_dock)

        # Dock Société (droite, tabulé avec inspecteur)
        self._society_dock = SocietyDock(self.controller, self)
        self._society_dock.setObjectName("dock_societe")
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self._society_dock)
        self.tabifyDockWidget(self._inspector_dock, self._society_dock)
        self._society_dock.agent_selected.connect(self._on_agent_selected)
        self._society_dock.command_result.connect(self.report_command_result)

        # Dock Tuile (droite, tabulé avec inspecteur) : examinateur de tuile
        self._tile_dock = TileDock(self.controller, self)
        self._tile_dock.setObjectName("dock_tuile")
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self._tile_dock)
        self.tabifyDockWidget(self._inspector_dock, self._tile_dock)

        # Dock Assets (gauche, tabulé avec habitants)
        self._assets_dock = AssetsDock(self.controller, self)
        self._assets_dock.setObjectName("dock_assets")
        if self.am:
            self._assets_dock.set_asset_manager(self.am)
        self._assets_dock.asset_selected.connect(self._on_asset_selected)
        self._assets_dock.command_result.connect(self.report_command_result)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._assets_dock)
        self.tabifyDockWidget(self._pop_dock, self._assets_dock)

        # Dock Outils (gauche)
        self._tools_dock = ToolsDock(self.controller, self)
        self._tools_dock.setObjectName("dock_outils")
        self._tools_dock.mode_changed.connect(self._on_mode_changed)
        self._tools_dock.command_result.connect(self.report_command_result)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._tools_dock)

        # Dock Journal (bas)
        self._journal_dock = JournalDock(self.controller, self)
        self._journal_dock.setObjectName("dock_journal")
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._journal_dock)

        # Studio docks
        self._param_dock = ParameterDock(self.controller, self)
        self._param_dock.setObjectName("dock_parametres")
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self._param_dock)
        self._param_dock.parameters_applied.connect(self._refresh_all_docks)
        self._param_dock.hide()

        self._timeline_dock = TimelineDock(self.controller, self)
        self._timeline_dock.setObjectName("dock_timeline")
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._timeline_dock)
        self._timeline_dock.hide()

        self._lab_dock = LaboratoryDock(self.controller, self)
        self._lab_dock.setObjectName("dock_laboratoire")
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self._lab_dock)
        self._lab_dock.hide()

        # Studio menu
        studio_menu = self.menuBar().addMenu("Studio")
        studio_menu.addAction("Scénarios...", self._open_scenarios)
        studio_menu.addAction("Paramètres", lambda: self._toggle_dock(self._param_dock))
        studio_menu.addAction("Timeline", lambda: self._toggle_dock(self._timeline_dock))
        studio_menu.addAction("Laboratoire", lambda: self._toggle_dock(self._lab_dock))
        studio_menu.addAction("Comparaison A/B", self._open_comparison)
        studio_menu.addAction("Configurer l'overlay", self._open_overlay_config)

        # Menu Vue : sans lui, un dock ferme etait definitivement perdu.
        vue = self.menuBar().addMenu("Vue")
        for dock, title in (
            (self._pop_dock, "Habitants"),
            (self._assets_dock, "Assets"),
            (self._tools_dock, "Outils"),
            (self._inspector_dock, "Inspecteur"),
            (self._anima_dock, "Anima"),
            (self._tile_dock, "Tuile"),
            (self._society_dock, "Societe"),
            (self._journal_dock, "Journal"),
            (self._param_dock, "Parametres"),
            (self._timeline_dock, "Timeline"),
            (self._lab_dock, "Laboratoire"),
        ):
            vue.addAction(self._dock_action(dock, title))
        vue.addSeparator()
        # Meme QAction que le bouton de la barre d'outils : le raccourci
        # Ctrl+H reste unique et le dialogue est visible meme si la barre
        # est repliee dans le bouton « etendu ».
        vue.addAction(self._spawn_custom_action)
        vue.addSeparator()
        # Meme QAction que le menu « Monde » de la barre d'outils (Ctrl+E) :
        # un seul objet = un seul raccourci, sans ambiguïté.
        vue.addAction(self._export_action)
        # Memes QAction que le menu « Édition » de la barre d'outils :
        # un seul objet coche, tous les endroits restent synchronises.
        vue.addAction(self._grid_action)
        vue.addAction(self._legend_action)

        # Menu Aide : les raccourcis visibles sans fouiller la barre d'outils.
        aide = self.menuBar().addMenu("Aide")
        raccourcis = QAction("Raccourcis clavier", self)
        raccourcis.triggered.connect(self._show_shortcuts)
        aide.addAction(raccourcis)

    def _setup_statusbar(self):
        self._status = QStatusBar()
        self.setStatusBar(self._status)

        # Lot H : la barre d'état se lit en blocs (pills) plutot qu'en une
        # longue phrase. Les pills sont des widgets permanents, a droite ;
        # showMessage (messages temporaires) reste libre a gauche.
        self._clock_pill = StatusPill("⏱ —", "#91A0B2")
        self._season_pill = StatusPill("🌱 —", "#62D394")
        self._weather_pill = StatusPill("🌧 —", "#62D394")
        self._population_pill = StatusPill("◉ 0", "#4CC9F0")
        self._speed_pill = StatusPill("⚡ 1×", "#F6BD60")
        self._state_pill = StatusPill("▮▮ En pause", "#A78BFA")
        self._tile_pill = StatusPill("⌖ —", "#91A0B2")
        self._performance_pill = StatusPill("0 FPS · 0.0 TPS", "#91A0B2")
        for pill in (self._clock_pill, self._season_pill, self._weather_pill,
                     self._population_pill,
                     self._speed_pill, self._state_pill, self._tile_pill,
                     self._performance_pill):
            self._status.addPermanentWidget(pill)

        self._seed_label = QLabel()
        self._status.addPermanentWidget(self._seed_label)
        self._scenario_label = QLabel()
        self._status.addPermanentWidget(self._scenario_label)
        self._error_label = QLabel()
        self._error_label.setStyleSheet("color: #e08a7a;")
        self._status.addPermanentWidget(self._error_label)
        self._error_seq = 0

    def report_command_result(self, result):
        """Canal d'erreur visible : aucun retour de commande n'est jeté."""
        if not isinstance(result, dict):
            return result
        if result.get("ok"):
            self._error_label.clear()
        else:
            self._error_seq += 1
            seq = self._error_seq
            self._error_label.setText(str(result.get("error", "Action refusée")))
            QTimer.singleShot(4000, lambda s=seq: self._expire_error(s))
        return result

    def _expire_error(self, seq):
        # Un message plus récent ne doit pas être effacé par un ancien timer.
        if seq == self._error_seq:
            self._error_label.clear()

    def _on_spawn_monster(self):
        cmd = {"kind": "spawn_monster"}
        monster_kind = getattr(self.controller.ui_state, "monster_kind", "")
        if monster_kind:
            cmd["monster_kind"] = monster_kind
        # Retourne le resultat : le menu Créer en a besoin pour ne promettre
        # « Monstre ajouté » que si le moteur a accepte la commande.
        return self.report_command_result(self.controller.execute(cmd))

    def _open_spawn_dialog(self):
        dlg = SpawnAgentDialog(self.controller, self.am, self)
        if not dlg.exec():
            return
        self._tools_dock.refresh()
        self._status.showMessage(
            "Cliquez sur la carte pour poser l'habitant defini", 6000)

    def _open_tool_editor(self):
        dlg = ToolEditorDialog(self.controller, self)
        if not dlg.exec():
            return
        self._map.asset_cache.clear()
        # Le catalogue a change : les vignettes memorisees sont perimees.
        self._assets_dock.invalidate_thumbnails()
        self._assets_dock.refresh()
        self._status.showMessage(
            "Outil enregistre : %s" % getattr(dlg, "created_path", ""), 6000)

    def _on_undo(self):
        result = self.controller.execute({"kind": "undo"})
        if result.get("changed"):
            self._map.invalidate_all_caches()
        self.report_command_result(result)

    def _on_redo(self):
        result = self.controller.execute({"kind": "redo"})
        if result.get("changed"):
            self._map.invalidate_all_caches()
        self.report_command_result(result)

    def _dock_action(self, dock, title):
        action = QAction(title, self)
        action.setCheckable(True)
        action.setChecked(dock.isVisible())
        action.toggled.connect(dock.setVisible)
        dock.visibilityChanged.connect(action.setChecked)
        return action

    def _toggle_grid(self, checked):
        self._map.debug_show_grid = bool(checked)
        self._map.request_render()

    def _toggle_legend(self, checked):
        self._map.show_legend = bool(checked)
        self._map.update()

    def _on_quicksave(self):
        result = self.controller.execute({"kind": "save", "slot": 0})
        self.report_command_result(result)
        if result.get("ok"):
            self._status.showMessage("Sauvegardee (slot 0)", 3000)

    def _on_new_world(self):
        answer = QMessageBox.question(
            self, "Nouveau monde",
            "Le monde actuel sera perdu s'il n'est pas sauvegarde.\nContinuer ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if answer != QMessageBox.StandardButton.Yes:
            return
        modes = ["procedural", "plat", "vierge"]
        mode, ok = QInputDialog.getItem(self, "Nouveau monde", "Type de monde :",
                                        modes, 0, False)
        if not ok:
            return
        seed, ok = QInputDialog.getInt(self, "Nouveau monde", "Graine :",
                                       int(getattr(self.controller.sim, "seed", 7)),
                                       0, 2 ** 31 - 1)
        if not ok:
            return
        result = self.controller.execute({"kind": "reset_world", "mode": mode,
                                          "seed": seed})
        self.report_command_result(result)
        if not result.get("ok"):
            return
        self.controller.sync_from_simulation()
        self._map._sync_transform_from_controller()
        self._map.invalidate_all_caches()
        self._active_scenario = "manual"
        self._refresh_all_docks()
        self._autosave()
        self._status.showMessage("Nouveau monde (%s, graine %d)" % (mode, seed), 4000)

    def _refresh_all_docks(self):
        for dock in (self._pop_dock, self._inspector_dock, self._anima_dock,
                     self._society_dock,
                     self._journal_dock, self._tools_dock, self._assets_dock,
                     self._tile_dock, self._param_dock, self._timeline_dock,
                     self._lab_dock):
            refresh = getattr(dock, "refresh", None)
            if callable(refresh):
                refresh()

    def _setup_timer(self):
        from game.config import FPS
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(max(1, 1000 // FPS))
        self._tick_count = 0
        # Bases des cadences RÉELLES : FPS = peintures achevées par la carte,
        # TPS = ticks du monde écoulés. Fenêtre glissante fondée sur
        # perf_counter (pas sur le timer de l'UI).
        self._reset_rate_counters()

    def _reset_rate_counters(self):
        """Remet à zéro les bases de mesure FPS/TPS (nouveau Sim, chargement)."""
        from time import perf_counter
        self._rate_sim = self.controller.sim
        self.rate_started = perf_counter()
        self.rate_last_world_tick = int(
            getattr(self._rate_sim.w, "tick", 0))
        self.rate_last_rendered_frames = int(
            getattr(self._map, "rendered_frames", 0))
        self.actual_fps = 0.0
        self.actual_tps = 0.0

    def _tick(self):
        import time

        frame_started = time.perf_counter()

        sim = self.controller.sim
        self._tick_count += 1

        # 1. Simulation
        sim_started = time.perf_counter()
        steps = 0
        if not sim.paused:
            from game.config import SIM_HZ, FPS
            acc = sim.speed * SIM_HZ / FPS
            n = 0
            while acc >= 1.0 and n < 8:
                sim.tick()
                acc -= 1.0
                n += 1
            steps = n
        sim_ms = (time.perf_counter() - sim_started) * 1000.0

        # Perf breakdown from sim.perf
        self.last_perf_sections = sim.perf.summary()

        # 2. Synchroniser l'état, docks, carte
        ui_started = time.perf_counter()
        self.controller.sync_from_simulation()

        # Suivi caméra : centrer sur l'habitant sélectionné si activé
        if self.controller.ui_state.follow_selected:
            sel = getattr(sim, "selected", None)
            if sel is not None and sel.alive:
                from game.config import GRID, TILE
                self._map.transform.center_on(
                    sel.x, sel.y,
                    self._map.width(), self._map.height(),
                    GRID * TILE,
                )
                self._map._sync_controller_from_transform()

        # Mettre à jour les docks (assets 1x/sec, les autres selon le
        # paramètre Performance › Fréquence snapshot).
        self._refresh_live_docks()

        # Mettre à jour la carte (tous les 3 ticks = ~6-7 Hz visuel à 20 FPS)
        MAP_REDRAW_EVERY = 3
        if self._tick_count % MAP_REDRAW_EVERY == 0:
            self._map.request_render()

        ui_ms = (time.perf_counter() - ui_started) * 1000.0
        total_ms = (time.perf_counter() - frame_started) * 1000.0

        # RENDER ms : mesuré DIRECTEMENT par MapView.paintEvent (aucune
        # déduction : total - sim - ui compterait BRAIN deux fois et
        # ignorerait le rendu réellement peint).
        sim.perf.add("ui", ui_ms)

        self.last_perf = {
            "sim_ms": sim_ms,
            "ui_ms": ui_ms,
            "total_ms": total_ms,
            "steps": steps,
        }

        # Mettre a jour la barre d'etat (4x par seconde suffit)
        if self._tick_count % 4 == 0:
            self._refresh_status()

        # Mettre à jour les contrôles
        self._pause_action.setText("Reprendre" if sim.paused else "Pause")
        if self._speed_spin.value() != sim.speed:
            self._speed_spin.blockSignals(True)
            self._speed_spin.setValue(sim.speed)
            self._speed_spin.blockSignals(False)

    def _refresh_live_docks(self):
        """Docks qui suivent la simulation vivante (pas tout le monde).

        Ne rafraîchit que les docks visibles pour économiser l'UI.
        Fréquence par défaut augmentée à 8 ticks (Phase 4).
        En mode performance, les rafraîchissements sont espacés à 25 ticks.
        """
        perf_mode = getattr(self, '_perf_mode', False)
        snap_every = max(1, int(
            (self.controller.sim.runtime or {}).get("snapshot_frequency", 8)))
        if perf_mode:
            snap_every = max(snap_every, 25)
        if self._tick_count % snap_every == 0:
            if self._pop_dock.isVisible():
                self._pop_dock.refresh()
            if self._inspector_dock.isVisible():
                self._inspector_dock.refresh()
            if self._anima_dock.isVisible():
                self._anima_dock.refresh()
            if self._journal_dock.isVisible():
                self._journal_dock.refresh()
            # Docks lourds sautés en mode performance sauf snapshot freq
            if not perf_mode:
                if self._society_dock.isVisible():
                    self._society_dock.refresh()
                if self._tools_dock.isVisible():
                    self._tools_dock.refresh()
                if self._tile_dock.isVisible():
                    self._tile_dock.refresh()
        # Catalogue lourd : une fois par seconde, et seulement a l'ecran.
        if self._tick_count % 60 == 0 and self._assets_dock.isVisible():
            refresh = getattr(self._assets_dock, "refresh_if_dirty", None)
            if callable(refresh):
                refresh()
            else:
                self._assets_dock.refresh()
        # Lot F.2 : la chronologie suit le monde tous les 8 ticks.
        if self._tick_count % 8 == 0 and self._timeline_dock.isVisible():
            self._timeline_dock.refresh()
        if self._tick_count % snap_every == 0 and self._lab_dock.isVisible():
            self._lab_dock.refresh()

    def _refresh_rate_counters(self):
        """Fenêtre glissante ≥ 0,25 s : FPS carte et TPS simulation réels.

        FPS = peintures ``paintEvent`` effectivement achevées (comptées par
        MapView) ; TPS = delta des ticks du monde. Ce n'est PAS le timer de
        l'UI : une pause donne 0 TPS et les vitesses élevées n'affichent que
        les ticks réellement effectués.
        """
        from time import perf_counter
        now = perf_counter()
        elapsed = now - self.rate_started
        if elapsed < 0.25:
            return
        frames_now = int(getattr(self._map, "rendered_frames", 0))
        ticks_now = int(self.controller.sim.w.tick)
        frames = frames_now - self.rate_last_rendered_frames
        ticks = ticks_now - self.rate_last_world_tick
        self.actual_fps = max(0, frames) / elapsed
        self.actual_tps = max(0, ticks) / elapsed
        self.rate_last_rendered_frames = frames_now
        self.rate_last_world_tick = ticks_now
        self.rate_started = now

    def _refresh_status(self):
        """Barre d'etat en blocs : horloge, saison, population, vitesse,
        etat, tuile survolée, performance, graine, scenario (Lot H)."""
        sim = self.controller.sim
        snap = simulation_snapshot(sim, self.controller.ui_state)
        clock = snap.get("clock", {})
        hover = getattr(self, "_hover_tile", None)

        label = str(clock.get("label", "") or "")
        self._clock_pill.setText("⏱ %s" % label if label else "⏱ —")
        season = str(clock.get("season", "") or "")
        self._season_pill.setText("🌱 %s" % season if season else "🌱 —")
        rain = float(clock.get("rain", 0.0))
        wind = clock.get("wind", (0.0, 0.0))
        wstr = "%.2f" % (float(wind[0]) if wind else 0.0)
        self._weather_pill.setText("🌧 %.0f%% · 🌬 %s" % (
            rain * 100, wstr))
        self._population_pill.setText("◉ %d" % snap["population"])
        self._speed_pill.setText("⚡ %d×" % snap["speed"])

        paused = bool(snap["paused"])
        self._state_pill.setText("▮▮ En pause" if paused else "▶ En marche")
        self._state_pill.set_pill_color("#A78BFA" if paused else "#62D394")

        if hover:
            self._tile_pill.setText("⌖ %d,%d" % (hover[0], hover[1]))
        else:
            self._tile_pill.setText("⌖ —")
        # Cadences RÉELLES : FPS = peintures achevées par la carte,
        # TPS = ticks du monde effectivement effectués (la pause donne 0).
        # Un Sim remplacé (chargement, nouveau monde) réinitialise les bases
        # pour éviter un TPS négatif ou artificiellement énorme.
        if getattr(self, "_rate_sim", None) is not sim:
            self._reset_rate_counters()
        self._refresh_rate_counters()

        perf = getattr(self, "last_perf", {})
        pm = getattr(sim, "perf", None)
        sim_ms = pm.average("sim") if pm else perf.get("sim_ms", 0.0)
        brain_ms = pm.average("brain") if pm else 0.0
        # UI et RENDER lus aux sections qu'ils mesurent réellement
        # (render vient de MapView.paintEvent, pas d'une déduction).
        ui_ms = pm.average("ui") if pm else perf.get("ui_ms", 0.0)
        render_ms = pm.average("render") if pm else 0.0
        perf_line = "SIM %.1fms · BRAIN %.1fms · UI %.1fms · RENDER %.1fms" % (
            sim_ms, brain_ms, ui_ms, render_ms)
        total_ms = sim_ms + ui_ms + render_ms
        over_budget = total_ms > TICK_BUDGET_MS
        self._performance_pill.setText(
            "%.0f FPS carte · %.1f TPS sim · %s" % (
                getattr(self, "actual_fps", 0.0),
                getattr(self, "actual_tps", 0.0),
                perf_line,
            ))
        if over_budget:
            self._performance_pill.set_pill_color("#E08A7A")  # warning orange/red
        else:
            self._performance_pill.set_pill_color("#91A0B2")  # default gray

        self._seed_label.setText("graine %s" % getattr(sim, "seed", "?"))
        # ── Alertes WORLD ALIVE (5 Hz, O(n) borné, clic actionnable) ──
        try:
            from game.alerts import compute_alerts, alert_button_text
            self._current_alerts = compute_alerts(
                sim, tps=getattr(self, "actual_tps", None))
            self._alert_btn.setText(alert_button_text(self._current_alerts))
            if self._current_alerts:
                top = self._current_alerts[0]
                sev = top.get("severity", "info")
                color = ("#E08A7A" if sev == "critical"
                         else ("#F6BD60" if sev == "warn" else "#91A0B2"))
                self._alert_btn.setStyleSheet("color: %s; font-weight: bold;" % color)
                tip = "\n".join(
                    "%s — %s" % (a.get("title", "?"), a.get("detail", ""))
                    for a in self._current_alerts)
                self._alert_btn.setToolTip(
                    "Alertes (clic = aller voir) :\n" + tip)
            else:
                self._alert_btn.setStyleSheet("color: #62D394;")
                self._alert_btn.setToolTip(
                    "Alertes monde vivant : famine, soif, blocage, blessé, "
                    "simulation lente. Clic = aller voir.")
        except Exception:
            pass
        # Indicateur LAB WORLD : état réel (mode labo + pause effective),
        # sinon le scénario actif de la fenêtre.
        if bool(getattr(sim, "blank_world", False)):
            lab_text = (
                "LAB WORLD — manual setup — paused"
                if bool(sim.paused)
                else "LAB WORLD — running"
            )
        else:
            lab_text = getattr(self, "_active_scenario", "manual")
        if self._scenario_label.text() != lab_text:
            self._scenario_label.setText(lab_text)

    def _on_pause(self):
        self.report_command_result(self.controller.execute({"kind": "pause_toggle"}))

    def _on_step(self):
        self.report_command_result(self.controller.execute({"kind": "step"}))

    def _on_speed(self, value):
        self.report_command_result(self.controller.execute({"kind": "set_speed", "speed": value}))

    def _toggle_low_detail(self, checked):
        """Bascule le mode détail faible sur la carte (Phase 6)."""
        self._map.low_detail_mode = checked
        if checked:
            self._status.showMessage("Mode détail faible activé (L)", 3000)
        else:
            self._status.showMessage("Mode détail normal", 3000)

    def _toggle_performance_mode(self, checked):
        """Bascule le mode performance maximal.

        En mode performance :
        - La carte ne se rafraîchit que toutes les 25 ticks minimum
        - Les docks lourds sont sautés
        - La qualité des effets est réduite
        """
        self._perf_mode = checked
        self._perf_mode_action.setChecked(checked)
        if checked:
            self._status.showMessage("Mode performance activé (M)", 3000)
            # Forcer un rafraîchissement léger immédiat
            self._map.request_render_now()
        else:
            self._status.showMessage("Mode performance désactivé", 3000)

    def _on_follow(self, checked):
        self.controller.ui_state.follow_selected = checked

    def _on_save(self):
        dlg = SaveDialog(self.controller, mode="save", parent=self)
        if dlg.exec():
            self._status.showMessage("Sauvegardee", 3000)

    def _on_load(self):
        dlg = SaveDialog(self.controller, mode="load", parent=self)
        if dlg.exec():
            self.controller.sync_from_simulation()
            self._map._sync_transform_from_controller()
            self._map.invalidate_all_caches()
            self._active_scenario = "manual"
            self._refresh_all_docks()
            # La commande « load » a restaure ui_state.active_overlay :
            # reposer le combo Vue et le mode de la carte dessus.
            self._apply_active_overlay()
            self._status.showMessage("Partie chargee", 3000)

    def _on_agent_selected(self, eid):
        self.report_command_result(
            self.controller.execute({"kind": "select_agent", "eid": eid}))
        self.controller.ui_state.active_tab = "etre"
        self.controller.ui_state.follow_selected = True
        # setChecked n'émet pas triggered : pas de récursion vers _on_follow.
        self._follow_action.setChecked(True)
        self._inspector_dock.raise_()

    def _on_alert_click(self):
        """Clic alerte → sélectionne + centre (WORLD ALIVE actionnable)."""
        alerts = list(getattr(self, "_current_alerts", []) or [])
        target = next((a for a in alerts if a.get("eid") is not None), None)
        if target is None:
            self._status.showMessage("Aucune alerte localisée — monde calme", 3000)
            return
        try:
            eid = int(target["eid"])
        except (TypeError, ValueError):
            return
        self._on_agent_selected(eid)
        # Centre la caméra sur l'habitant (coordonnées monde réelles).
        try:
            agent = next((a for a in self.controller.sim.agents
                          if a.eid == eid and a.alive), None)
            if agent is not None:
                self._map.transform.center_on(
                    float(agent.x), float(agent.y),
                    self._map.width(), self._map.height())
                self._map.update()
            self._status.showMessage(
                "%s — %s" % (target.get("title", "Alerte"),
                             target.get("detail", "")), 5000)
        except Exception:
            pass

    def _on_map_clicked(self):
        """Un clic sur la carte prend la main : fin du suivi automatique."""
        if self.controller.ui_state.follow_selected:
            self.controller.ui_state.follow_selected = False
            self._follow_action.setChecked(False)

    def _on_asset_selected(self, aid):
        """Un asset choisi dans le catalogue arme l'outil « Poser »."""
        self.report_command_result(self.controller.execute({"kind": "set_mode",
                                                            "mode": "place"}))
        # Le dock Assets est construit avant le dock Outils : un signal émis
        # pendant l'initialisation ne doit pas casser la fenêtre.
        if hasattr(self, "_tools_dock"):
            self._tools_dock.refresh()

    def _on_mode_changed(self, mode):
        # showMessage : ne pas ecraser le libelle tick/population de la barre.
        self._status.showMessage("Outil : %s" % mode, 2500)

    def _show_shortcuts(self):
        QMessageBox.information(
            self, "Raccourcis clavier", """
<table cellspacing="8">
<tr><td><b>Espace</b></td><td>Pause / Reprendre</td></tr>
<tr><td><b>N</b></td><td>Avancer d'un tick (step)</td></tr>
<tr><td><b>1 - 8</b></td><td>Vitesse de simulation</td></tr>
<tr><td><b>Ctrl+H</b></td><td>Creer un habitant personnalise</td></tr>
<tr><td><b>Ctrl+N</b></td><td>Nouveau monde</td></tr>
<tr><td><b>Ctrl+E</b></td><td>Exporter l'image de la carte</td></tr>
<tr><td><b>F5</b></td><td>Quicksave (slot 0)</td></tr>
<tr><td><b>Maj+F5</b></td><td>Sauvegarder sous...</td></tr>
<tr><td><b>F9</b></td><td>Charger une partie</td></tr>
<tr><td><b>Ctrl+Z</b></td><td>Annuler</td></tr>
<tr><td><b>Ctrl+Maj+Z</b></td><td>Retablir</td></tr>
<tr><td><b>Clic droit (glisser)</b></td><td>Deplacer la camera</td></tr>
<tr><td><b>Selection dans la liste Habitants</b></td><td>Suit l'habitant (un clic sur la carte arrete le suivi)</td></tr>
</table>
""")

    def _toggle_theme(self):
        from ui_qt.theme.theme import get_theme_name, set_theme_name, apply_theme
        current = get_theme_name()
        new_theme = "sombre" if current == "clair" else "clair"
        set_theme_name(new_theme)
        apply_theme(self, new_theme)
        self._theme_action.setText(
            "Theme clair" if new_theme == "sombre" else "Theme sombre"
        )

    def _restore_settings(self):
        from ui_qt.theme.theme import get_settings, get_theme_name
        s = get_settings()
        geom = s.value("geometry")
        if geom:
            self.restoreGeometry(geom)
        state = s.value("windowState")
        if state:
            self.restoreState(state)
        # Appliquer le theme sauvegarde
        from ui_qt.theme.theme import apply_theme
        apply_theme(self, get_theme_name())

    def _save_settings(self):
        from ui_qt.theme.theme import get_settings
        s = get_settings()
        s.setValue("geometry", self.saveGeometry())
        s.setValue("windowState", self.saveState())

    def _toggle_dock(self, dock):
        dock.setVisible(not dock.isVisible())

    def _open_scenarios(self):
        dlg = ScenarioDialog(self.controller, self)
        if not dlg.exec():
            return
        key = dlg.get_selected_scenario()
        scenario = get_scenario(key) if key else None
        self._active_scenario = scenario["label"] if scenario else (key or "manual")
        self._refresh_all_docks()
        self._refresh_status()

    def _export_viewport(self):
        """Exporte l'image visible de la carte (Lot F.5)."""
        from PyQt6.QtWidgets import QFileDialog
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter l'image",
            "neural-world-view.png",
            "PNG (*.png)",
        )
        if path:
            ok = self._map.grab().save(path, "PNG")
            if ok:
                self._status.showMessage(f"Image exportée : {path}", 4000)
            else:
                self._status.showMessage("Échec de l'export de l'image", 4000)

    def _open_comparison(self):
        if not hasattr(self, '_comparison_panel'):
            self._comparison_panel = ComparisonPanel()
            self._comparison_panel.setWindowTitle("Comparaison A/B")
            self._comparison_panel.setObjectName("comparison_panel")
        # La feuille du theme rend QWidget transparent : une fenetre sans
        # parent doit recevoir un fond explicite (selectionneur d'id).
        from ui_qt.theme.theme import get_theme_background
        self._comparison_panel.setStyleSheet(
            "#comparison_panel { background: %s; }" % get_theme_background()
        )
        self._comparison_panel.show()

    def _apply_active_overlay(self):
        """Repose ``ui_state.active_overlay`` sur le combo Vue et la carte.

        Appele au demarrage (main_qt restaure l'etat AVANT la fenetre) et
        apres un chargement. Silencieux : un combo ou une carte manquant
        ne doit jamais faire echouer un load.
        """
        try:
            mode = str(getattr(self.controller.ui_state, "active_overlay",
                               "") or "normal")
            combo = getattr(self, "_overlay_combo", None)
            if combo is not None:
                index = combo.findData(mode)
                if index >= 0 and index != combo.currentIndex():
                    # setCurrentIndex emet currentIndexChanged : on bloque
                    # pour ne pas rejouer la commande set_overlay.
                    combo.blockSignals(True)
                    try:
                        combo.setCurrentIndex(index)
                        combo.setToolTip(WorldOverlay().mode_help(mode))
                    finally:
                        combo.blockSignals(False)
            if getattr(self, "_map", None) is not None:
                self._map.set_overlay_mode(mode)
        except Exception:
            pass

    def _open_overlay_config(self):
        """Dialogue « Configurer l'overlay » : mode, légende sur la carte
        et agent de contexte. Chaque changement est appliqué immédiatement
        (rien n'est persisté hors de ui_state pour le mode)."""
        from PyQt6.QtWidgets import (QDialog, QComboBox, QCheckBox,
                                      QDialogButtonBox, QFormLayout,
                                      QVBoxLayout)
        from ui_qt.studio.world_overlay import MODES, CONTEXT_MODES, OVERLAY_HELP

        overlay = WorldOverlay()
        current = str(getattr(self.controller.ui_state, "active_overlay",
                              "normal") or "normal")

        dialog = QDialog(self)
        dialog.setWindowTitle("Configurer l'overlay")
        layout = QVBoxLayout(dialog)
        form = QFormLayout()

        # ── Overlay : mêmes ids/labels que le sélecteur « Vue » ──
        overlay_combo = QComboBox()
        for m in MODES:
            overlay_combo.addItem(overlay.mode_label(m), m)
        index = overlay_combo.findData(current)
        overlay_combo.setCurrentIndex(index if index >= 0 else 0)
        form.addRow("Overlay", overlay_combo)

        # ── Agent de contexte : « Aucun » + habitants vivants ──
        agent_combo = QComboBox()
        agent_combo.addItem("Aucun", None)
        try:
            from game.ui_snapshots import population_snapshot
            for row in population_snapshot(self.controller.sim):
                eid = row.get("eid")
                name = str(row.get("name") or eid)
                agent_combo.addItem(name, eid)
        except Exception:
            pass
        selected = getattr(self.controller.sim, "selected", None)
        sel_eid = getattr(selected, "eid", None) if selected is not None else None
        if sel_eid is not None:
            j = agent_combo.findData(sel_eid)
            if j >= 0:
                agent_combo.setCurrentIndex(j)
        agent_combo.setToolTip(
            "Habitant utilisé par les overlays exigeant une sélection : "
            + ", ".join(sorted(CONTEXT_MODES)) + ".")
        form.addRow("Agent de contexte", agent_combo)
        layout.addLayout(form)

        # ── Légende d'overlay sur la carte (attribut MapView, non persisté) ──
        legend_check = QCheckBox("Afficher la légende de l'overlay sur la carte")
        legend_check.setChecked(bool(getattr(self, "_map", None) is not None
                                     and getattr(self._map,
                                                 "show_overlay_legend", True)))
        layout.addWidget(legend_check)

        # ── Aide du mode choisi (OVERLAY_HELP) ──
        help_label = QLabel(OVERLAY_HELP.get(current, ""))
        help_label.setWordWrap(True)
        layout.addWidget(help_label)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Close)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        def apply_mode(mode):
            help_label.setText(OVERLAY_HELP.get(mode, ""))
            bar = getattr(self, "_overlay_combo", None)
            if bar is not None:
                j = bar.findData(mode)
                if j >= 0:
                    # Même chemin que _on_overlay_change (commande + carte).
                    bar.setCurrentIndex(j)
                    return
            result = self.controller.execute({"kind": "set_overlay",
                                              "overlay": mode})
            self.report_command_result(result)
            if result.get("ok") and getattr(self, "_map", None) is not None:
                self._map.set_overlay_mode(
                    self.controller.ui_state.active_overlay)

        def on_mode_changed(idx):
            mode = overlay_combo.itemData(idx)
            if mode:
                apply_mode(str(mode))

        def on_agent_changed(idx):
            eid = agent_combo.itemData(idx)
            command = ({"kind": "select_agent"} if eid is None
                       else {"kind": "select_agent", "eid": eid})
            self.report_command_result(self.controller.execute(command))

        def on_legend_toggled(checked):
            if getattr(self, "_map", None) is None:
                return
            self._map.show_overlay_legend = bool(checked)
            self._map.update()

        overlay_combo.currentIndexChanged.connect(on_mode_changed)
        agent_combo.currentIndexChanged.connect(on_agent_changed)
        legend_check.toggled.connect(on_legend_toggled)
        dialog.exec()

    def _on_overlay_change(self, index):
        mode = self._overlay_combo.currentData()
        result = self.controller.execute({"kind": "set_overlay", "overlay": mode})
        self.report_command_result(result)
        # Aide contextuelle du mode (Lot F.4)
        from ui_qt.studio.world_overlay import WorldOverlay
        self._overlay_combo.setToolTip(WorldOverlay().mode_help(mode))
        if result.get("ok") and hasattr(self, '_map') and self._map:
            self._map.set_overlay_mode(self.controller.ui_state.active_overlay)

    def _set_speed(self, speed):
        self.report_command_result(self.controller.execute({"kind": "set_speed", "speed": speed}))

    def keyPressEvent(self, event):
        # Flèches/WASD non consommées par le widget focus (labels, boutons…)
        # → navigation de la carte depuis n'importe quel dock ou la toolbar.
        if getattr(self, "_map", None) is not None and \
                self._map.handle_nav_key(event):
            return
        super().keyPressEvent(event)

    def _autosave(self):
        """Écrit la session courante dans le slot 98 : main_qt.py la relit
        au lancement, on retrouve donc le monde exact de la session précédente."""
        if not self.isVisible():
            # Fenêtre jamais affichée = test unitaire : évite d'écrire ~60 Mo
            # à chaque win.close() des suites de tests.
            return False
        from game.save import AUTOSAVE_SLOT, save_game
        try:
            save_game(self.controller.sim, self.controller.camera,
                      slot=AUTOSAVE_SLOT,
                      ui_state=self.controller.ui_state.snapshot_dict())
            return True
        except Exception as exc:
            print("[AUTOSAVE] echec :", exc)
            return False

    def closeEvent(self, event):
        if self.isVisible():
            # Fenêtre jamais affichée = test unitaire : ne pas écraser la
            # géométrie/répartition réelle des docks, ni écrire ~60 Mo
            # d'autosave, à chaque win.close() des suites de tests.
            self._save_settings()
            self._autosave()
        super().closeEvent(event)
