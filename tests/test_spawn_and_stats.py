"""Regressions Lot 0 : commandes de spawn et traduction des besoins.

- ``spawn_monster`` avec ``monster_kind`` doit produire exactement ce kind
  (bug Lot 0.6 : le discriminant ``kind`` de la commande fuitait dans le monstre).
- ``spawn_monster`` avec un kind inconnu doit etre refuse, pas tire au hasard.
- ``set_agent_stat`` doit reellement ecrire la valeur sur l'etre pour chacun
  des libelles francais envoyes par l'inspecteur (bug Lot 0.3 : ecritures no-op).
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.ui_commands import execute_command


def _make_sim():
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    from game.engine import build_world, seed_life

    am = AssetManager(headless=True)
    am.discover()
    _set_asset_manager(am)
    world, sim = build_world(am, seed=11, procedural=False, populate_dense=False)
    seed_life(world, sim, sim.rng, n_agents=4, n_sheep=0)
    return sim


class TestSpawnMonsterKind(unittest.TestCase):
    def test_monster_kind_respected(self):
        sim = _make_sim()
        seen = set()
        for _ in range(6):
            result = execute_command(sim, {"kind": "spawn_monster",
                                           "monster_kind": "wolf"})
            self.assertTrue(result.get("ok"), result)
            seen.add(sim.monsters[-1].kind)
        self.assertEqual(seen, {"wolf"})

    def test_unknown_kind_rejected(self):
        sim = _make_sim()
        before = len(sim.monsters)
        result = execute_command(sim, {"kind": "spawn_monster",
                                       "monster_kind": "dragon"})
        self.assertFalse(result.get("ok"))
        self.assertIn("error", result)
        self.assertEqual(len(sim.monsters), before)

    def test_no_kind_is_random_but_valid(self):
        from game.config import MONSTER_KINDS
        sim = _make_sim()
        for _ in range(5):
            result = execute_command(sim, {"kind": "spawn_monster"})
            self.assertTrue(result.get("ok"), result)
            self.assertIn(sim.monsters[-1].kind, MONSTER_KINDS)


class TestSetAgentStat(unittest.TestCase):
    LABELS = ["faim", "soif", "sommeil", "securite", "appartenance",
              "estime", "sante", "energie"]

    def test_each_label_writes(self):
        sim = _make_sim()
        agent = sim.agents[0]
        for label in self.LABELS:
            result = execute_command(sim, {"kind": "set_agent_stat",
                                           "eid": agent.eid,
                                           "stat": label, "value": 0.25})
            self.assertTrue(result.get("ok"), (label, result))
        self.assertAlmostEqual(agent.hunger, 0.25, places=3)
        self.assertAlmostEqual(agent.health, 0.25, places=3)
        self.assertAlmostEqual(agent.energy, 0.25, places=3)
        for value in agent.needs:
            self.assertAlmostEqual(float(value), 0.25, places=3)

    def test_unknown_stat_reports_error(self):
        sim = _make_sim()
        agent = sim.agents[0]
        result = execute_command(sim, {"kind": "set_agent_stat",
                                       "eid": agent.eid,
                                       "stat": "courage", "value": 0.5})
        self.assertFalse(result.get("ok"))
        self.assertIn("error", result)


class TestSpawnAgentWhitelist(unittest.TestCase):
    """Lot D.1 : le dialogue de création passe corps, esprit et nom."""

    def test_full_template_reaches_the_being(self):
        sim = _make_sim()
        before = len(sim.agents)
        result = execute_command(sim, {
            "kind": "spawn_agent",
            "x": 500.0, "y": 500.0,
            "name": "Testeur",
            "sex": "F",
            "n_hid": 64,
            "energy": 0.42,
            "body": [0.1, 0.2, 0.3, 0.4, 0.5],
            "cog": [0.9, 0.8, 0.7, 0.6],
            "personality": [0.5] * 12,
            "emotions": [0.0, 0.9, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1],
            "needs": [0.25, 0.42, 0.3, 0.3, 0.8, 0.5, 0.4],
        })
        self.assertTrue(result.get("ok"), result)
        self.assertEqual(len(sim.agents), before + 1)
        agent = sim.agents[-1]
        self.assertEqual(agent.name, "Testeur")
        self.assertEqual(agent.sex, "F")
        self.assertEqual(agent.brain.n, 64)
        self.assertAlmostEqual(agent.energy, 0.42, places=3)
        self.assertAlmostEqual(float(agent.body[2]), 0.3, places=3)
        self.assertAlmostEqual(float(agent.cog[0]), 0.9, places=3)
        self.assertAlmostEqual(float(agent.emotions[1]), 0.9, places=3)

    def test_bad_shapes_rejected(self):
        sim = _make_sim()
        before = len(sim.agents)
        result = execute_command(sim, {"kind": "spawn_agent",
                                       "body": [0.1, 0.2]})
        self.assertFalse(result.get("ok"))
        self.assertIn("error", result)
        self.assertEqual(len(sim.agents), before)


if __name__ == "__main__":
    unittest.main()
