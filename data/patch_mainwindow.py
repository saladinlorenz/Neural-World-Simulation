import io

p = "ui_qt/main_window.py"
src = io.open(p, encoding="utf-8", newline="").read()


def rep(old, new, count=1):
    global src
    assert src.count(old) == count, (src.count(old), old[:80])
    src = src.replace(old, new)


rep("""from PyQt6.QtWidgets import (QMainWindow, QToolBar, QLabel,
                              QSpinBox, QStatusBar, QPushButton)""",
"""from PyQt6.QtWidgets import (QMainWindow, QToolBar, QLabel,
                              QSpinBox, QStatusBar, QPushButton,
                              QInputDialog, QMessageBox)""")

rep("""        # Sauvegarde
        save_action = QAction("Sauvegarder (F5)", self)
        save_action.setShortcut("F5")
        save_action.triggered.connect(self._on_save)
        tb.addAction(save_action)
""",
"""        # Sauvegarde : F5 = slot 0 direct, Maj+F5 = dialogue
        quick_action = QAction("Quicksave", self)
        quick_action.setShortcut("F5")
        quick_action.setToolTip("Sauvegarde immediate dans le slot 0")
        quick_action.triggered.connect(self._on_quicksave)
        tb.addAction(quick_action)

        save_action = QAction("Sauvegarder sous...", self)
        save_action.setShortcut("Shift+F5")
        save_action.triggered.connect(self._on_save)
        tb.addAction(save_action)
""")

rep("""        # Speed presets
        for speed in [1, 2, 4, 8]:
            btn = QPushButton(f"{speed}x")
            btn.setFixedWidth(36)
            btn.clicked.connect(lambda checked, s=speed: self._set_speed(s))
            tb.addWidget(btn)
""",
"""        # Speed presets
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
""")

rep("""        self._status_label = QLabel()
        self._status.addWidget(self._status_label)
        self._error_label = QLabel()""",
"""        self._status_label = QLabel()
        self._status.addWidget(self._status_label)
        self._fps_label = QLabel()
        self._status.addPermanentWidget(self._fps_label)
        self._seed_label = QLabel()
        self._status.addPermanentWidget(self._seed_label)
        self._error_label = QLabel()""")

rep("""        studio_menu.addAction("Configurer l'overlay", self._open_overlay_config)
""",
"""        studio_menu.addAction("Configurer l'overlay", self._open_overlay_config)

        # Menu Vue : sans lui, un dock ferme etait definitivement perdu.
        vue = self.menuBar().addMenu("Vue")
        for dock, title in (
            (self._pop_dock, "Habitants"),
            (self._assets_dock, "Assets"),
            (self._tools_dock, "Outils"),
            (self._inspector_dock, "Inspecteur"),
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
""")

rep("""    def _setup_timer(self):""",
"""    def _dock_action(self, dock, title):
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
            "Le monde actuel sera perdu s'il n'est pas sauvegarde.\\nContinuer ?",
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
                     self._param_dock, self._timeline_dock, self._lab_dock):
            refresh = getattr(dock, "refresh", None)
            if callable(refresh):
                refresh()

    def _setup_timer(self):""")

rep("""    def _tick(self):
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
""",
"""    def _tick(self):
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
""")

rep("""        # Mettre à jour la barre d'état (4x par seconde suffit)
        if self._tick_count % 4 == 0:
            snap = simulation_snapshot(sim, self.controller.ui_state)
            clock = snap.get("clock", {})
            self._status_label.setText(
                f"Tick {snap['tick']} | {clock.get('label', '')} | "
                f"Pop: {snap['population']} | Speed: {snap['speed']} | "
                f"{'Pause' if snap['paused'] else 'Running'}"
            )
""",
"""        # Indicateur FPS / TPS (moyennes glissantes)
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
""")

rep("""    def _on_mode_changed(self, mode):
        self._status_label.setText(f"Outil : {mode}")
""",
"""    def _on_mode_changed(self, mode):
        # showMessage : ne pas ecraser le libelle tick/population de la barre.
        self._status.showMessage("Outil : %s" % mode, 2500)
""")

rep("""    def _on_load(self):
        dlg = SaveDialog(self.controller, mode="load", parent=self)
        if dlg.exec():
            self.controller.sync_from_simulation()
            self._map._sync_transform_from_controller()
            self._map.invalidate_all_caches()
            self._status.showMessage("Partie chargee", 3000)
""",
"""    def _on_load(self):
        dlg = SaveDialog(self.controller, mode="load", parent=self)
        if dlg.exec():
            self.controller.sync_from_simulation()
            self._map._sync_transform_from_controller()
            self._map.invalidate_all_caches()
            self._refresh_all_docks()
            self._status.showMessage("Partie chargee", 3000)
""")

io.open(p, "w", encoding="utf-8", newline="").write(src)
print("main_window patched")
