"""Soak test 10 000 ticks — validation invariants + métriques propreté.

Exécuter : python -m pytest -q tests/test_soak_10k.py -v
"""
import math
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _make_sim():
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    from game.engine import build_world

    am = AssetManager(headless=True).discover()
    am.ensure_procedural_blocks()
    am.ensure_procedural_tools()
    am.ensure_kaykit_resources()
    _set_asset_manager(am)
    _, sim = build_world(am, seed=42, procedural=True, n_agents=3)
    return sim


class TestSoak10k(unittest.TestCase):
    """Lot H — 10 000 ticks avec vérifications à intervalle régulier."""

    TICKS = 10_000
    CHECK_EVERY = 100

    def test_long_run_invariants_and_metrics(self):
        from game.invariants import validate_simulation

        sim = _make_sim()

        for tick in range(self.TICKS):
            sim.step()

            if (tick + 1) % self.CHECK_EVERY == 0:
                # Invariant check à chaque intervalle
                errors = validate_simulation(sim)
                self.assertEqual(errors, [],
                    f"Invariants violés au tick {tick+1}: {errors}")

                # Pas de NaN dans les positions
                for a in sim.agents:
                    if not a.alive:
                        continue
                    self.assertTrue(math.isfinite(a.x),
                        f"NaN position x agent {a.eid} au tick {tick+1}")
                    self.assertTrue(math.isfinite(a.y),
                        f"NaN position y agent {a.eid} au tick {tick+1}")

        # Vérifications finales
        # 1. Métriques de récupération numérique = 0 (si disponible)
        if "numeric_recoveries" in sim.metrics:
            self.assertEqual(sim.metrics["numeric_recoveries"], 0,
                f"numeric_recoveries={sim.metrics['numeric_recoveries']} (devrait être 0)")

        # 2. Erreurs d'actions non gérées = 0
        if "unhandled_action_errors" in sim.metrics:
            self.assertEqual(sim.metrics["unhandled_action_errors"], 0,
                f"unhandled_action_errors={sim.metrics['unhandled_action_errors']} (devrait être 0)")

        # 3. Anomalies de chargement = 0 (si disponible)
        if "load_anomalies" in sim.metrics:
            self.assertEqual(sim.metrics["load_anomalies"], 0,
                f"load_anomalies={sim.metrics['load_anomalies']} (devrait être 0)")

        # 4. Santé et énergie dans [0, 1] pour tous les agents vivants
        for a in sim.agents:
            if not a.alive:
                continue
            self.assertTrue(0.0 <= a.health <= 1.0,
                f"health={a.health} hors [0,1] pour agent {a.eid}")
            self.assertTrue(0.0 <= a.energy <= 1.0,
                f"energy={a.energy} hors [0,1] pour agent {a.eid}")
            self.assertTrue(0.0 <= a.hunger <= 1.0,
                f"hunger={a.hunger} hors [0,1] pour agent {a.eid}")

            # Données Anima finies
            for k, v in a.anima.get("identity", {}).items():
                self.assertTrue(math.isfinite(v),
                    f"NaN identity[{k}] agent {a.eid}")
            for k, v in a.anima.get("values", {}).items():
                self.assertTrue(math.isfinite(v),
                    f"NaN values[{k}] agent {a.eid}")
            for k, v in a.anima.get("trauma", {}).items():
                self.assertTrue(math.isfinite(v),
                    f"NaN trauma[{k}] agent {a.eid}")
            for eid, bdict in a.anima.get("beliefs", {}).get("beings", {}).items():
                if isinstance(bdict, dict):
                    for bk, bv in bdict.items():
                        self.assertTrue(math.isfinite(bv),
                            f"NaN belief[{eid}][{bk}] agent {a.eid}")
            for k, v in a.anima.get("reputation", {}).items():
                if isinstance(v, float):
                    self.assertTrue(math.isfinite(v),
                        f"NaN reputation[{k}] agent {a.eid}")

        # 5. Au moins un agent survivant
        alive_agents = [a for a in sim.agents if a.alive]
        self.assertGreater(len(alive_agents), 0,
            "Tous les agents sont morts avant 10k ticks")

        # 6. Population non-nulle
        self.assertGreater(len(sim.agents), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)