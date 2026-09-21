"""Tests de la couche neutre UI (ui_state, ui_snapshots, ui_commands, simulation_controller).

Valide que :
- les snapshots ne contiennent que des types simples
- les snapshots sont serialisables JSON
- les commandes valides sont acceptees
- les commandes invalides sont rejetees
- le controller synchronise correctement
- aucune dependance Pygame/Qt dans ces modules
"""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
pygame.init()
pygame.display.set_mode((1, 1))


def _make_sim():
    """Construit un Sim minimal pour les tests."""
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    from game.engine import build_world

    am = AssetManager(headless=True)
    am.discover()
    _set_asset_manager(am)
    world, sim = build_world(am, seed=42, procedural=True)
    return sim, am


class TestUIState(unittest.TestCase):
    def test_defaults(self):
        from game.ui_state import UIState
        s = UIState()
        self.assertEqual(s.active_tab, "etre")
        self.assertEqual(s.active_mode, "agent")
        self.assertIsNone(s.selected_agent_eid)
        self.assertTrue(s.paused)
        self.assertEqual(s.speed, 1)

    def test_sync_from_simulation(self):
        from game.ui_state import UIState
        sim, _ = _make_sim()
        s = UIState()
        s.sync_from_simulation(sim)
        self.assertEqual(s.speed, sim.speed)
        self.assertEqual(s.paused, sim.paused)

    def test_snapshot_dict_types(self):
        from game.ui_state import UIState
        s = UIState()
        d = s.snapshot_dict()
        # Toutes les valeurs doivent etre serialisables JSON
        text = json.dumps(d)
        self.assertIsInstance(text, str)
        restored = json.loads(text)
        self.assertEqual(restored["active_tab"], "etre")


class TestUISnapshots(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sim, cls.am = _make_sim()

    def test_simulation_snapshot(self):
        from game.ui_snapshots import simulation_snapshot
        snap = simulation_snapshot(self.sim)
        self.assertIn("tick", snap)
        self.assertIn("paused", snap)
        self.assertIn("speed", snap)
        self.assertIn("population", snap)
        self.assertIn("clock", snap)
        self.assertIsInstance(snap["tick"], int)
        self.assertIsInstance(snap["paused"], bool)
        # Serialisable JSON
        text = json.dumps(snap)
        self.assertIsInstance(text, str)

    def test_population_snapshot(self):
        from game.ui_snapshots import population_snapshot
        rows = population_snapshot(self.sim)
        self.assertIsInstance(rows, list)
        for row in rows:
            self.assertIn("eid", row)
            self.assertIn("nom", row)
            self.assertIn("vivant", row)
            text = json.dumps(row)
            self.assertIsInstance(text, str)

    def test_selected_agent_snapshot_none(self):
        from game.ui_snapshots import selected_agent_snapshot
        from game.ui_state import UIState
        state = UIState()
        result = selected_agent_snapshot(self.sim, state)
        self.assertIsNone(result)

    def test_journal_snapshot(self):
        from game.ui_snapshots import journal_snapshot
        self.sim.log("Test entry", (255, 0, 0), "monde")
        rows = journal_snapshot(self.sim)
        self.assertIsInstance(rows, list)
        if rows:
            self.assertIn("tick", rows[-1])
            self.assertIn("text", rows[-1])
            text = json.dumps(rows[-1])
            self.assertIsInstance(text, str)

    def test_map_snapshot(self):
        from game.ui_snapshots import map_snapshot
        from game.ui_state import UIState
        state = UIState()
        snap = map_snapshot(self.sim, state)
        self.assertIn("tick", snap)
        self.assertIn("grid", snap)
        self.assertIn("agents", snap)
        self.assertIn("sheep", snap)
        text = json.dumps(snap)
        self.assertIsInstance(text, str)

    def test_tile_snapshot(self):
        from game.ui_snapshots import tile_snapshot
        snap = tile_snapshot(self.sim, 10, 10)
        self.assertIn("tx", snap)
        self.assertIn("ty", snap)
        self.assertIn("dans_monde", snap)
        text = json.dumps(snap)
        self.assertIsInstance(text, str)

    def test_society_snapshot(self):
        from game.ui_snapshots import society_snapshot
        snap = society_snapshot(self.sim)
        self.assertIn("population", snap)
        self.assertIn("stats", snap)
        text = json.dumps(snap)
        self.assertIsInstance(text, str)

    def test_no_numpy_in_snapshots(self):
        """Aucun numpy array ne doit apparaitre dans les snapshots."""
        import numpy as np
        from game.ui_snapshots import simulation_snapshot, population_snapshot, map_snapshot
        from game.ui_state import UIState

        for snap in [
            simulation_snapshot(self.sim),
            population_snapshot(self.sim),
            map_snapshot(self.sim, UIState()),
        ]:
            self._check_no_numpy(snap)

    def _check_no_numpy(self, obj, path=""):
        import numpy as np
        if isinstance(obj, np.ndarray):
            self.fail(f"numpy array trouve dans le snapshot a {path}")
        elif isinstance(obj, dict):
            for k, v in obj.items():
                self._check_no_numpy(v, f"{path}.{k}")
        elif isinstance(obj, (list, tuple)):
            for i, v in enumerate(obj):
                self._check_no_numpy(v, f"{path}[{i}]")


class TestUICommands(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sim, cls.am = _make_sim()

    def test_pause_toggle(self):
        from game.ui_commands import execute_command
        was_paused = self.sim.paused
        result = execute_command(self.sim, {"kind": "pause_toggle"})
        self.assertTrue(result["ok"])
        self.assertEqual(result["paused"], not was_paused)
        # Restaurer
        self.sim.paused = was_paused

    def test_set_speed(self):
        from game.ui_commands import execute_command
        result = execute_command(self.sim, {"kind": "set_speed", "speed": 5})
        self.assertTrue(result["ok"])
        self.assertEqual(result["speed"], 5)
        self.sim.speed = 2

    def test_speed_bounded(self):
        from game.ui_commands import execute_command
        result = execute_command(self.sim, {"kind": "set_speed", "speed": 99})
        self.assertTrue(result["ok"])
        self.assertEqual(result["speed"], 8)
        result = execute_command(self.sim, {"kind": "set_speed", "speed": -1})
        self.assertTrue(result["ok"])
        self.assertEqual(result["speed"], 1)
        self.sim.speed = 2

    def test_select_agent(self):
        from game.ui_commands import execute_command
        if self.sim.agents:
            eid = self.sim.agents[0].eid
            result = execute_command(self.sim, {"kind": "select_agent", "eid": eid})
            self.assertTrue(result["ok"])
            self.assertEqual(result["eid"], eid)
        self.sim.selected = None

    def test_select_agent_invalid(self):
        from game.ui_commands import execute_command
        result = execute_command(self.sim, {"kind": "select_agent", "eid": 99999})
        self.assertFalse(result["ok"])

    def test_unknown_command(self):
        from game.ui_commands import execute_command
        result = execute_command(self.sim, {"kind": "unknown_thing"})
        self.assertFalse(result["ok"])
        self.assertIn("error", result)

    def test_step(self):
        from game.ui_commands import execute_command
        old_tick = int(self.sim.w.tick)
        self.sim.paused = True
        result = execute_command(self.sim, {"kind": "step"})
        self.assertTrue(result["ok"])
        self.assertGreater(int(self.sim.w.tick), old_tick)

    def test_spawn_sheep(self):
        from game.ui_commands import execute_command
        old_count = len(self.sim.sheep)
        result = execute_command(self.sim, {"kind": "spawn_sheep"})
        self.assertTrue(result["ok"])
        self.assertEqual(len(self.sim.sheep), old_count + 1)

    def test_log(self):
        from game.ui_commands import execute_command
        old_len = len(self.sim.journal)
        result = execute_command(self.sim, {"kind": "log", "text": "test log"})
        self.assertTrue(result["ok"])


class TestSimulationController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sim, cls.am = _make_sim()

    def test_snapshot(self):
        from game.simulation_controller import SimulationController
        ctrl = SimulationController(self.sim)
        snap = ctrl.snapshot()
        self.assertIn("simulation", snap)
        self.assertIn("population", snap)
        self.assertIn("selected_agent", snap)
        self.assertIn("journal", snap)
        text = json.dumps(snap)
        self.assertIsInstance(text, str)

    def test_execute(self):
        from game.simulation_controller import SimulationController
        ctrl = SimulationController(self.sim)
        result = ctrl.execute({"kind": "set_speed", "speed": 6})
        self.assertTrue(result["ok"])
        self.assertEqual(self.sim.speed, 6)
        self.sim.speed = 2

    def test_sync(self):
        from game.simulation_controller import SimulationController
        ctrl = SimulationController(self.sim)
        ctrl.sync_from_simulation()
        self.assertEqual(ctrl.ui_state.speed, self.sim.speed)
        self.assertEqual(ctrl.ui_state.paused, self.sim.paused)

    def test_translate_action(self):
        from game.simulation_controller import SimulationController
        ctrl = SimulationController(self.sim)
        cmd = ctrl.translate_action(("pause", None))
        self.assertIsNotNone(cmd)
        self.assertEqual(cmd["kind"], "pause_toggle")

        cmd = ctrl.translate_action(("speed", 1))
        self.assertIsNotNone(cmd)
        self.assertEqual(cmd["kind"], "speed_delta")
        self.assertEqual(cmd["delta"], 1)

    def test_translate_unknown(self):
        from game.simulation_controller import SimulationController
        ctrl = SimulationController(self.sim)
        cmd = ctrl.translate_action(("unknown_action", None))
        self.assertIsNone(cmd)

    def test_handle_legacy_action(self):
        from game.simulation_controller import SimulationController
        ctrl = SimulationController(self.sim)
        was_paused = self.sim.paused
        result = ctrl.handle_legacy_action(("pause", None))
        self.assertIsNotNone(result)
        self.assertTrue(result["ok"])
        self.sim.paused = was_paused


class TestUIRegistry(unittest.TestCase):
    def test_registry_imports(self):
        from game.ui_registry import (
            SECTION_REGISTRY, CARD_REGISTRY, TABS, MODES,
            TAB_MODES, TAB_HINTS, LOG_CATS, CHIP_LABELS, PANELS,
        )
        self.assertIsInstance(SECTION_REGISTRY, list)
        self.assertIsInstance(CARD_REGISTRY, list)
        self.assertIsInstance(TABS, list)
        self.assertIsInstance(MODES, list)
        self.assertIsInstance(TAB_MODES, dict)
        self.assertIsInstance(TAB_HINTS, dict)
        self.assertIsInstance(LOG_CATS, dict)
        self.assertIsInstance(CHIP_LABELS, dict)
        self.assertIsInstance(PANELS, dict)


if __name__ == "__main__":
    unittest.main()
