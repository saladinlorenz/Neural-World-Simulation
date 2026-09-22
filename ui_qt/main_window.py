"""MainWindow — QMainWindow principale de l'interface PyQt6."""
from PyQt6.QtWidgets import (QMainWindow, QToolBar, QLabel,
                              QSpinBox, QStatusBar, QPushButton)
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
from ui_qt.dialogs import SaveDialog
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
        self._setup_docks()
        self._setup_statusbar()
        self._setup_timer()
        self._restore_settings()

    def _setup_toolbar(self):
        tb = QToolBar("Controle")
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
        spawn_btn.triggered.connect(lambda: self.controller.execute({"kind": "spawn_agent"}))
        tb.addAction(spawn_btn)

        spawn_sheep = QAction("+ Mouton", self)
        spawn_sheep.triggered.connect(lambda: self.controller.execute({"kind": "spawn_sheep"}))
        tb.addAction(spawn_sheep)

        spawn_monster = QAction("+ Monstre", self)
        spawn_monster.triggered.connect(lambda: self.controller.execute({"kind": "spawn_monster"}))
        tb.addAction(spawn_monster)

        tb.addSeparator()

        # Suivi caméra
        self._follow_action = QAction("Suivre", self)
        self._follow_action.setCheckable(True)
        self._follow_action.triggered.connect(self._on_follow)
        tb.addAction(self._follow_action)

        tb.addSeparator()

        # Sauvegarde
        save_action = QAction("Sauvegarder (F5)", self)
        save_action.setShortcut("F5")
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
        self._overlay_combo = QComboBox()
        for m in ["normal", "danger", "ressources", "memoire", "relations", "besoins", "anima"]:
            self._overlay_combo.addItem(WorldOverlay().mode_label(m) if hasattr(WorldOverlay, 'mode_label') else m, m)
        self._overlay_combo.currentIndexChanged.connect(self._on_overlay_change)
        tb.addWidget(QLabel("Vue: "))
        tb.addWidget(self._overlay_combo)

        # Speed presets
        for speed in [1, 2, 4, 8]:
            btn = QPushButton(f"{speed}x")
            btn.setFixedWidth(36)
            btn.clicked.connect(lambda checked, s=speed: self._set_speed(s))
            tb.addWidget(btn)

    def _setup_central(self):
        self._map = MapView(self.controller, self)
        self.setCentralWidget(self._map)

    def _setup_docks(self):
        # Dock Habitants (gauche)
        self._pop_dock = PopulationDock(self.controller, self)
        self._pop_dock.agent_selected.connect(self._on_agent_selected)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._pop_dock)

        # Dock Inspecteur (droite)
        self._inspector_dock = InspectorDock(self.controller, self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self._inspector_dock)

        # Dock Société (droite, tabulé avec inspecteur)
        self._society_dock = SocietyDock(self.controller, self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self._society_dock)
        self.tabifyDockWidget(self._inspector_dock, self._society_dock)

        # Dock Assets (gauche, tabulé avec habitants)
        self._assets_dock = AssetsDock(self.controller, self)
        if self.am:
            self._assets_dock.set_asset_manager(self.am)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._assets_dock)
        self.tabifyDockWidget(self._pop_dock, self._assets_dock)

        # Dock Outils (gauche)
        self._tools_dock = ToolsDock(self.controller, self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._tools_dock)

        # Dock Journal (bas)
        self._journal_dock = JournalDock(self.controller, self)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._journal_dock)

        # Studio docks
        self._param_dock = ParameterDock(self.controller, self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self._param_dock)
        self._param_dock.hide()

        self._timeline_dock = TimelineDock(self.controller, self)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._timeline_dock)
        self._timeline_dock.hide()

        self._lab_dock = LaboratoryDock(self.controller, self)
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

    def _setup_statusbar(self):
        self._status = QStatusBar()
        self.setStatusBar(self._status)
        self._status_label = QLabel()
        self._status.addWidget(self._status_label)

    def _setup_timer(self):
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(16)  # ~60 FPS
        self._tick_count = 0

    def _tick(self):
        sim = self.controller.sim
        self._tick_count += 1

        # Avancer la simulation
        if not sim.paused:
            from game.config import SIM_HZ, FPS
            acc = sim.speed * SIM_HZ / FPS
            n = 0
            while acc >= 1.0 and n < 8:
                sim.tick()
                acc -= 1.0
                n += 1

        # Synchroniser l'état
        self.controller.sync_from_simulation()

        # Mettre à jour les docks (assets 1x/sec, les autres 4x/sec)
        if self._tick_count % 4 == 0:
            self._pop_dock.refresh()
            self._inspector_dock.refresh()
            self._journal_dock.refresh()
            self._society_dock.refresh()
            self._tools_dock.refresh()
        if self._tick_count % 60 == 0:
            self._assets_dock.refresh()

        # Mettre à jour la carte
        self._map.update()

        # Mettre à jour la barre d'état (4x par seconde suffit)
        if self._tick_count % 4 == 0:
            snap = simulation_snapshot(sim, self.controller.ui_state)
            clock = snap.get("clock", {})
            self._status_label.setText(
                f"Tick {snap['tick']} | {clock.get('label', '')} | "
                f"Pop: {snap['population']} | Speed: {snap['speed']} | "
                f"{'Pause' if snap['paused'] else 'Running'}"
            )

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
            new_sim = self.controller.sim
            self.controller.sync_from_simulation()
            self._status.showMessage("Partie chargee", 3000)

    def _on_agent_selected(self, eid):
        self.controller.ui_state.selected_agent_eid = eid
        self.controller.ui_state.active_tab = "etre"

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
        if hasattr(self, '_map') and self._map:
            self._map.set_overlay_mode(mode)

    def _set_speed(self, speed):
        self.controller.execute({"kind": "set_speed", "speed": speed})

    def closeEvent(self, event):
        self._save_settings()
        super().closeEvent(event)
