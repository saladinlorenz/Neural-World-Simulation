"""MainWindow — QMainWindow principale de l'interface PyQt6."""
from PyQt6.QtWidgets import (QMainWindow, QToolBar, QLabel,
                              QSpinBox, QStatusBar, QPushButton,
                              QInputDialog, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction

from game.ui_snapshots import simulation_snapshot
from game.ui_commands import execute_command
from ui_qt.map.map_view import MapView
from ui_qt.docks.population_dock import PopulationDock
from ui_qt.docks.inspector_dock import InspectorDock
from ui_qt.docks.journal_dock import JournalDock
from ui_qt.docks.society_dock import SocietyDock
from ui_qt.docks.assets_dock import AssetsDock
from ui_qt.docks.tools_dock import ToolsDock
from ui_qt.docks.tile_dock import TileDock
from ui_qt.dialogs import SaveDialog, SpawnAgentDialog, ToolEditorDialog
from ui_qt.theme.theme import apply_theme
from ui_qt.studio.parameter_dock import ParameterDock
from ui_qt.studio.scenario_dialog import ScenarioDialog
from ui_qt.studio.timeline_dock import TimelineDock
from ui_qt.studio.laboratory_dock import LaboratoryDock
from ui_qt.studio.comparison_panel import ComparisonPanel
from ui_qt.studio.world_overlay import WorldOverlay


class MainWindow(QMainWindow):
    """Fenêtre principale PyQt6 avec docks, barre d'outils et carte."""

    def __init__(self, controller, am=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.am = am
        self.setWindowTitle("Univers Vivant — PyQt6")
        self.setMinimumSize(1200, 800)

        apply_theme(self)

        self._setup_toolbar()
        self._setup_central()
        # La barre d'état porte le canal d'erreur : elle doit exister avant
        # les docks, dont la construction peut déjà émettre des commandes.
        self._setup_statusbar()
        self._setup_docks()
        self._setup_timer()
        self._restore_settings()

    def _setup_toolbar(self):
        tb = QToolBar("Controle")
        tb.setObjectName("toolbar_controle")
        tb.setMovable(False)
        self.addToolBar(tb)

        # Pause/Play
        self._pause_action = QAction("Pause", self)
        self._pause_action.setShortcut("Space")
        self._pause_action.triggered.connect(self._on_pause)
        tb.addAction(self._pause_action)

        # Step
        step_action = QAction("Step", self)
        step_action.setShortcut("N")
        step_action.triggered.connect(self._on_step)
        tb.addAction(step_action)

        tb.addSeparator()

        # Vitesse
        tb.addWidget(QLabel(" Vitesse: "))
        self._speed_spin = QSpinBox()
        self._speed_spin.setRange(1, 8)
        self._speed_spin.setValue(self.controller.sim.speed)
        self._speed_spin.valueChanged.connect(self._on_speed)
        tb.addWidget(self._speed_spin)

        tb.addSeparator()

        # Spawn
        spawn_btn = QAction("+ Habitants", self)
        spawn_btn.triggered.connect(
            lambda: self.report_command_result(
                self.controller.execute({"kind": "spawn_agent"})))
        tb.addAction(spawn_btn)

        spawn_sheep = QAction("+ Mouton", self)
        spawn_sheep.triggered.connect(
            lambda: self.report_command_result(
                self.controller.execute({"kind": "spawn_sheep"})))
        tb.addAction(spawn_sheep)

        spawn_monster = QAction("+ Monstre", self)
        spawn_monster.setToolTip(
            "Type de monstre : aléatoire si aucun n'est choisi dans Outils")
        spawn_monster.triggered.connect(self._on_spawn_monster)
        tb.addAction(spawn_monster)

        tb.addSeparator()

        spawn_custom = QAction("Créer un habitant...", self)
        spawn_custom.setShortcut("Ctrl+H")
        spawn_custom.setToolTip("Sexe, clan, classe, cerveau, energie, nom et "
                                "gabarits : le prochain clic sur la carte pose "
                                "cet habitant.")
        spawn_custom.triggered.connect(self._open_spawn_dialog)
        tb.addAction(spawn_custom)

        tool_editor = QAction("Editeur d'outil...", self)
        tool_editor.setToolTip("Dessine un outil 16x16 et l'enregistre au catalogue")
        tool_editor.triggered.connect(self._open_tool_editor)
        tb.addAction(tool_editor)

        tb.addSeparator()

        undo_action = QAction("Annuler", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self._on_undo)
        tb.addAction(undo_action)

        redo_action = QAction("Retablir", self)
        redo_action.setShortcut("Ctrl+Shift+Z")
        redo_action.triggered.connect(self._on_redo)
        tb.addAction(redo_action)

        tb.addSeparator()

        # Suivi caméra
        self._follow_action = QAction("Suivre", self)
        self._follow_action.setCheckable(True)
        self._follow_action.triggered.connect(self._on_follow)
        tb.addAction(self._follow_action)

        tb.addSeparator()

        # Sauvegarde : F5 = slot 0 direct, Maj+F5 = dialogue
        quick_action = QAction("Quicksave", self)
        quick_action.setShortcut("F5")
        quick_action.setToolTip("Sauvegarde immediate dans le slot 0")
        quick_action.triggered.connect(self._on_quicksave)
        tb.addAction(quick_action)

        save_action = QAction("Sauvegarder sous...", self)
        save_action.setShortcut("Shift+F5")
        save_action.triggered.connect(self._on_save)
        tb.addAction(save_action)

        load_action = QAction("Charger (F9)", self)
        load_action.setShortcut("F9")
        load_action.triggered.connect(self._on_load)
        tb.addAction(load_action)

        tb.addSeparator()

        # Theme toggle
        self._theme_action = QAction("Theme sombre", self)
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
        self._overlay_combo.currentIndexChanged.connect(self._on_overlay_change)
        tb.addWidget(QLabel("Vue: "))
        tb.addWidget(self._overlay_combo)

        # Speed presets
        for speed in [1, 2, 4, 8]:
            btn = QPushButton(f"{speed}x")
            btn.setFixedWidth(36)
            btn.clicked.connect(lambda checked, s=speed: self._set_speed(s))
            tb.addWidget(btn)

        # Raccourcis clavier 1..8 : une touche = une vitesse
        for speed in range(1, 9):
            action = QAction("Vitesse %d" % speed, self)
            action.setShortcut(str(speed))
            action.triggered.connect(lambda checked, s=speed: self._set_speed(s))
            self.addAction(action)

        # Nouveau monde (destructif : confirme par _on_new_world)
        new_world = QAction("Nouveau monde...", self)
        new_world.setShortcut("Ctrl+N")
        new_world.triggered.connect(self._on_new_world)
        tb.addAction(new_world)

    def _setup_central(self):
        self._map = MapView(self.controller, self)
        self._map.command_result.connect(self.report_command_result)
        self.setCentralWidget(self._map)

    def _setup_docks(self):
        # Dock Habitants (gauche)
        self._pop_dock = PopulationDock(self.controller, self)
        self._pop_dock.setObjectName("dock_population")
        self._pop_dock.agent_selected.connect(self._on_agent_selected)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._pop_dock)

        # Dock Inspecteur (droite)
        self._inspector_dock = InspectorDock(self.controller, self)
        self._inspector_dock.setObjectName("dock_inspecteur")
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self._inspector_dock)

        # Dock Société (droite, tabulé avec inspecteur)
        self._society_dock = SocietyDock(self.controller, self)
        self._society_dock.setObjectName("dock_societe")
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self._society_dock)
        self.tabifyDockWidget(self._inspector_dock, self._society_dock)

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
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._assets_dock)
        self.tabifyDockWidget(self._pop_dock, self._assets_dock)
        self._assets_dock.asset_selected.connect(self._on_asset_selected)

        # Dock Outils (gauche)
        self._tools_dock = ToolsDock(self.controller, self)
        self._tools_dock.setObjectName("dock_outils")
        self._tools_dock.mode_changed.connect(self._on_mode_changed)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._tools_dock)

        # Dock Journal (bas)
        self._journal_dock = JournalDock(self.controller, self)
        self._journal_dock.setObjectName("dock_journal")
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._journal_dock)

        # Studio docks
        self._param_dock = ParameterDock(self.controller, self)
        self._param_dock.setObjectName("dock_parametres")
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self._param_dock)
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
            (self._tile_dock, "Tuile"),
            (self._society_dock, "Societe"),
            (self._journal_dock, "Journal"),
            (self._param_dock, "Parametres"),
            (self._timeline_dock, "Timeline"),
            (self._lab_dock, "Laboratoire"),
        ):
            vue.addAction(self._dock_action(dock, title))
        vue.addSeparator()
        self._grid_action = QAction("Grille de tuiles", self)
        self._grid_action.setCheckable(True)
        self._grid_action.setChecked(self._map.debug_show_grid)
        self._grid_action.triggered.connect(self._toggle_grid)
        vue.addAction(self._grid_action)
        self._legend_action = QAction("Legende", self)
        self._legend_action.setCheckable(True)
        self._legend_action.setChecked(self._map.show_legend)
        self._legend_action.triggered.connect(self._toggle_legend)
        vue.addAction(self._legend_action)

    def _setup_statusbar(self):
        self._status = QStatusBar()
        self.setStatusBar(self._status)
        self._status_label = QLabel()
        self._status.addWidget(self._status_label)
        self._fps_label = QLabel()
        self._status.addPermanentWidget(self._fps_label)
        self._seed_label = QLabel()
        self._status.addPermanentWidget(self._seed_label)
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
        self.report_command_result(self.controller.execute(cmd))

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
        self._map.update()

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
        self._refresh_all_docks()
        self._status.showMessage("Nouveau monde (%s, graine %d)" % (mode, seed), 4000)

    def _refresh_all_docks(self):
        for dock in (self._pop_dock, self._inspector_dock, self._society_dock,
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

    def _tick(self):
        import time

        now = time.perf_counter()
        dt = now - getattr(self, "_last_tick_at", now)
        self._last_tick_at = now

        sim = self.controller.sim
        self._tick_count += 1

        # Avancer la simulation
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

        # Synchroniser l'état
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

        # Mettre à jour les docks (assets 1x/sec, les autres 4x/sec)
        if self._tick_count % 4 == 0:
            self._pop_dock.refresh()
            self._inspector_dock.refresh()
            self._journal_dock.refresh()
            self._society_dock.refresh()
            self._tools_dock.refresh()
            self._tile_dock.refresh()
        if self._tick_count % 60 == 0:
            self._assets_dock.refresh()

        # Mettre à jour la carte
        if self._tick_count % 2 == 0:
            self._map.update()

        # Indicateur FPS / TPS (moyennes glissantes)
        if dt > 0:
            self._fps_ema = 0.8 * getattr(self, "_fps_ema", 0.0) + 0.2 / dt
            self._tps_ema = 0.8 * getattr(self, "_tps_ema", 0.0) + 0.2 * steps / dt
        if self._tick_count % 4 == 0:
            self._fps_label.setText(
                "%.0f fps - %.1f tps" % (getattr(self, "_fps_ema", 0.0),
                                         getattr(self, "_tps_ema", 0.0)))

        # Mettre a jour la barre d'etat (4x par seconde suffit)
        if self._tick_count % 4 == 0:
            snap = simulation_snapshot(sim, self.controller.ui_state)
            clock = snap.get("clock", {})
            self._status_label.setText(
                f"Tick {snap['tick']} | {clock.get('label', '')} | "
                f"Pop: {snap['population']} | Speed: {snap['speed']} | "
                f"{'Pause' if snap['paused'] else 'Running'}"
            )
            self._seed_label.setText("graine %s" % getattr(sim, "seed", "?"))

        # Mettre à jour les contrôles
        self._pause_action.setText("Reprendre" if sim.paused else "Pause")
        if self._speed_spin.value() != sim.speed:
            self._speed_spin.blockSignals(True)
            self._speed_spin.setValue(sim.speed)
            self._speed_spin.blockSignals(False)

    def _on_pause(self):
        self.controller.execute({"kind": "pause_toggle"})

    def _on_step(self):
        self.controller.execute({"kind": "step"})

    def _on_speed(self, value):
        self.controller.execute({"kind": "set_speed", "speed": value})

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
            self._refresh_all_docks()
            self._status.showMessage("Partie chargee", 3000)

    def _on_agent_selected(self, eid):
        self.report_command_result(
            self.controller.execute({"kind": "select_agent", "eid": eid}))
        self.controller.ui_state.active_tab = "etre"
        self._inspector_dock.raise_()

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
        dlg.exec()

    def _open_comparison(self):
        if not hasattr(self, '_comparison_panel'):
            self._comparison_panel = ComparisonPanel()
            self._comparison_panel.setWindowTitle("Comparaison A/B")
        self._comparison_panel.show()

    def _open_overlay_config(self):
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Overlay", 
            "Utilisez le sélecteur 'Vue' dans la barre d'outils pour changer l'overlay de la carte.")

    def _on_overlay_change(self, index):
        mode = self._overlay_combo.currentData()
        result = self.controller.execute({"kind": "set_overlay", "overlay": mode})
        self.report_command_result(result)
        if result.get("ok") and hasattr(self, '_map') and self._map:
            self._map.set_overlay_mode(self.controller.ui_state.active_overlay)

    def _set_speed(self, speed):
        self.controller.execute({"kind": "set_speed", "speed": speed})

    def closeEvent(self, event):
        self._save_settings()
        super().closeEvent(event)
