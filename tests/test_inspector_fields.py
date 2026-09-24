"""Lot A : clés anglaises du snapshot agent + champs inspecteur remplis."""
import json
import os
import sys
import unittest

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

EXPECTED_KEYS = {
    "eid", "name", "alive", "sex", "class", "clan", "generation",
    "age_years", "stage", "natural_death_age_years", "avatar_idx",
    "position", "state", "health", "pain", "temperature",
    "needs_named", "emotions_named", "personality_named", "body_named",
    "cognition_named", "skills_named", "inventory", "tool",
    "tool_durability", "goal", "brain", "memory", "danger_beliefs",
    "relations", "family", "episodes", "life",
}

DECEASED_KEYS = {
    "eid", "name", "alive", "sex", "class", "clan", "generation",
    "age_years", "stage", "health", "needs_named", "death_tick",
}

GOAL_KEYS = {
    "action", "action_name", "target_x", "target_y",
    "distance_px", "until_tick", "intensity", "stuck_ticks",
}

BRAIN_KEYS = {"neurons", "think_frequency", "action_ranking"}

SKILLS_KEYS = {"harvest", "building", "combat", "social"}

FAMILY_KEYS = {"partner_eid", "father_eid", "mother_eid", "children"}

FRENCH_KEYS = {
    "nom", "vivant", "sexe", "classe", "age_ans", "mort_naturelle_ans",
    "etat", "sante", "douleur", "personnalite", "corps", "competences",
    "inventaire", "outil", "durabilite_outil", "but", "cerveau",
    "neurones", "frequence_reflexion", "classement_actions", "memoire",
    "croyances_danger", "vie", "tick_deces",
}


def _make_controller():
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    from game.engine import build_world, seed_life
    from game.simulation_controller import SimulationController

    am = AssetManager(headless=True)
    am.discover()
    _set_asset_manager(am)
    world, sim = build_world(am, seed=7, procedural=False, populate_dense=False)
    seed_life(world, sim, sim.rng, n_agents=6, n_sheep=0)
    return SimulationController(sim)


class TestAgentSnapshotEnglishKeys(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.controller = _make_controller()
        cls.sim = cls.controller.sim
        cls.agent = next(a for a in cls.sim.agents if a.alive)

    def test_exact_key_set(self):
        from game.diagnostics import agent_snapshot
        snap = agent_snapshot(self.sim, self.agent)
        self.assertEqual(set(snap), EXPECTED_KEYS)

    def test_no_french_top_level_keys(self):
        from game.diagnostics import agent_snapshot
        snap = agent_snapshot(self.sim, self.agent)
        self.assertFalse(set(snap) & FRENCH_KEYS)

    def test_needs_named_uses_need_defs_labels(self):
        from game.config import NEED_DEFS
        from game.diagnostics import agent_snapshot
        snap = agent_snapshot(self.sim, self.agent)
        self.assertEqual(set(snap["needs_named"]), set(NEED_DEFS))
        for value in snap["needs_named"].values():
            self.assertIsInstance(value, float)

    def test_skills_named_english_subkeys(self):
        from game.diagnostics import agent_snapshot
        snap = agent_snapshot(self.sim, self.agent)
        self.assertEqual(set(snap["skills_named"]), SKILLS_KEYS)

    def test_goal_and_brain_english_subkeys(self):
        from game.diagnostics import agent_snapshot
        snap = agent_snapshot(self.sim, self.agent)
        self.assertEqual(set(snap["goal"]), GOAL_KEYS)
        self.assertEqual(set(snap["brain"]), BRAIN_KEYS)

    def test_family_and_memory_keys(self):
        from game.diagnostics import agent_snapshot
        from game.entities import MEM_CATS
        snap = agent_snapshot(self.sim, self.agent)
        self.assertEqual(set(snap["family"]), FAMILY_KEYS)
        self.assertEqual(set(snap["memory"]), set(MEM_CATS))
        for marks in snap["memory"].values():
            for mark in marks:
                self.assertEqual(set(mark), {"x", "y", "strength"})
        self.assertIsInstance(snap["life"], list)
        self.assertIsInstance(snap["episodes"], list)

    def test_relations_english_subkeys_when_present(self):
        from game.diagnostics import agent_snapshot
        other = next(
            a for a in self.sim.agents if a.alive and a.eid != self.agent.eid
        )
        self.agent.rel[other.eid] = [0.5, 0.2]
        try:
            snap = agent_snapshot(self.sim, self.agent)
            self.assertTrue(snap["relations"])
            rel = snap["relations"][0]
            self.assertEqual(
                set(rel), {"eid", "name", "trust", "affection", "alive"}
            )
        finally:
            self.agent.rel.pop(other.eid, None)

    def test_json_serializable_fresh_snapshot(self):
        from game.diagnostics import agent_snapshot
        snap = agent_snapshot(self.sim, self.agent)
        json.dumps(snap)

    def test_deceased_row_english_keys(self):
        from game.config import NEED_DEFS
        from game.diagnostics import deceased_row
        row = deceased_row(self.sim, self.agent)
        self.assertEqual(set(row), DECEASED_KEYS)
        self.assertFalse(row["alive"])
        # Les besoins restants sont purgés à la mort : seuls faim/énergie
        # survivent, mais toujours sous les libellés NEED_DEFS.
        self.assertTrue(set(row["needs_named"]) <= set(NEED_DEFS))
        self.assertEqual(
            set(row["needs_named"]), {NEED_DEFS[0], NEED_DEFS[1]}
        )

    def test_population_rows_english_keys(self):
        from game.ui_snapshots import population_snapshot
        rows = population_snapshot(self.sim)
        self.assertTrue(rows)
        for row in rows:
            self.assertIn("name", row)
            self.assertIn("alive", row)
            self.assertIn("age_years", row)
            self.assertIn("health", row)
            self.assertIn("needs_named", row)
            self.assertNotIn("nom", row)
            self.assertNotIn("vivant", row)
            self.assertNotIn("age_ans", row)
            self.assertNotIn("sante", row)

    def test_selected_snapshot_via_ui_state(self):
        from game.ui_snapshots import selected_agent_snapshot
        snap = selected_agent_snapshot(self.sim, self.controller.ui_state)
        if snap is None:
            self.controller.execute(
                {"kind": "select_agent", "eid": self.agent.eid}
            )
            snap = selected_agent_snapshot(
                self.sim, self.controller.ui_state
            )
        self.assertIsNotNone(snap)
        self.assertEqual(set(snap), EXPECTED_KEYS)


class TestInspectorDockFields(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from PyQt6.QtWidgets import QApplication
        cls.app = QApplication.instance() or QApplication([])
        cls.controller = _make_controller()

    def _agent(self):
        return next(a for a in self.controller.sim.agents if a.alive)

    def test_refresh_fills_all_labels(self):
        from PyQt6 import QtWidgets
        from ui_qt.main_window import MainWindow

        sim = self.controller.sim
        agent = self._agent()
        # Inject deterministic data into the four memory sections.
        agent.seen["food"] = [(agent.tx, agent.ty, 0.8)]
        agent.belief_places[(0, 0)] = 0.5
        agent.episodes.append((sim.w.tick, "test", {}))
        agent.life.append("event de test")
        agent.rel[self._other_eid(agent)] = [0.5, 0.2]

        win = MainWindow(self.controller)
        try:
            self.controller.execute({"kind": "select_agent", "eid": agent.eid})
            dock = win._inspector_dock
            dock.refresh()

            self.assertIn(agent.name, dock._identity_label.text())
            self.assertTrue(dock._state_label.text())
            self.assertTrue(dock._position_label.text())
            self.assertTrue(dock._meta_label.text())
            self.assertIn("Mort naturelle", dock._meta_label.text())
            self.assertTrue(dock._goal_label.text())
            self.assertTrue(dock._relations_label.text())
            self.assertTrue(dock._family_label.text())
            self.assertIn(
                "Mémoire spatiale", dock._spatial_label.text()
            )
            self.assertIn(
                "Événements de vie", dock._life_label.text()
            )
            self.assertIn("Croyances", dock._belief_label.text())
            self.assertIn("Autobiographie", dock._autobio_label.text())
            pix = dock._portrait.pixmap()
            self.assertIsNotNone(pix)
            self.assertFalse(pix.isNull())
            self.assertFalse(dock._memory_group.isHidden())
        finally:
            win.close()
            QtWidgets.QWidget.deleteLater(win)
            self.app.processEvents()

    def _other_eid(self, agent):
        return next(
            a.eid for a in self.controller.sim.agents
            if a.alive and a.eid != agent.eid
        )

    def test_clear_when_no_selection(self):
        from PyQt6 import QtWidgets
        from ui_qt.main_window import MainWindow

        sim = self.controller.sim
        win = MainWindow(self.controller)
        try:
            sim.selected = None
            self.controller.ui_state.selected_agent_eid = None
            dock = win._inspector_dock
            dock.refresh()
            self.assertEqual(
                dock._identity_label.text(),
                "Aucun agent selectionne",
            )
            pix = dock._portrait.pixmap()
            self.assertTrue(pix is None or pix.isNull())
            self.assertTrue(dock._memory_group.isHidden())
            self.assertTrue(dock._belief_label.text() == "")
            self.assertTrue(dock._spatial_label.text() == "")
            self.assertTrue(dock._life_label.text() == "")
        finally:
            win.close()
            QtWidgets.QWidget.deleteLater(win)
            self.app.processEvents()


if __name__ == "__main__":
    unittest.main()
