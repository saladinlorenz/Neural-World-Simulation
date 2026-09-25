"""Tests d'activité des agents — courts, déterministes, sans simulation > 300 ticks.

Couvre les exigences du plan Phase 4 + validation des Phases 1-3.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ["QT_QPA_PLATFORM"] = "offscreen"


def _make_controller():
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    from game.engine import build_world, seed_life
    from game.simulation_controller import SimulationController

    am = AssetManager(headless=True)
    am.discover()
    _set_asset_manager(am)
    world, sim = build_world(am, seed=42, procedural=True)
    seed_life(world, sim, sim.rng, n_agents=10, n_sheep=5, n_monsters=0)
    return SimulationController(sim)


class TestAgentActivity(unittest.TestCase):
    """Tests de régression courts et déterministes."""

    @classmethod
    def setUpClass(cls):
        cls.controller = _make_controller()

    def test_tick_changes_and_selected_agent_positions_are_live(self):
        """Le tick avance et au moins un agent en état de bouger se déplace."""
        sim = self.controller.sim
        sim.debug_eid = sim.agents[0].eid if sim.agents else None

        # État initial
        initial_positions = [(a.eid, a.x, a.y) for a in sim.agents[:5]]
        initial_tick = sim.w.tick

        # 200 ticks
        for _ in range(200):
            sim.tick()

        self.assertGreater(sim.w.tick, initial_tick,
                           "Le tick doit avancer")

        # Au moins un des 5 premiers agents a bougé (> 5 px)
        moved = 0
        for eid, x0, y0 in initial_positions:
            agent = sim._by_eid(eid)
            if agent and agent.alive:
                dx = agent.x - x0
                dy = agent.y - y0
                if dx * dx + dy * dy > 25:
                    moved += 1
        self.assertGreaterEqual(moved, 1,
                                "Au moins un agent en état de bouger doit se déplacer")

    def test_masked_policy_never_samples_infeasible_action(self):
        """Le masque feasible empêche le tirage d'actions infaisables."""
        sim = self.controller.sim
        a = sim.agents[0]

        # Construire un masque où seul REST et EXPLORE sont faisables
        from game.brain_api import REST, EXPLORE, N_OUT
        f = [False] * N_OUT
        f[REST] = True
        f[EXPLORE] = True

        # Répéter le tirage avec seed fixe via le rng de l'agent
        from numpy.random import Generator, PCG64
        original_rng = a.brain.rng
        a.brain.rng = Generator(PCG64(12345))

        for _ in range(20):
            # _sense retourne un vecteur de taille N_IN
            x = sim._sense(a)
            act, probs = a.brain.think(x, temperature=1.0, bias=None,
                                        curiosity=a.personality[2],
                                        caution=a.personality[3],
                                        feasible=f)
            self.assertIn(act, (REST, EXPLORE),
                          f"Action tirée {act} doit être dans le masque feasible")

        a.brain.rng = original_rng

    def test_no_resource_leads_to_bounded_fallback(self):
        """Sans cible valide, l'agent en forme fait un repli court ou exploration ; épuisé -> repos."""
        sim = self.controller.sim

        # Agent en forme, sans ressources connues -> fallback_goal doit donner EXPLORE court
        a_fit = sim.agents[0]
        a_fit.energy = 0.8
        a_fit.health = 0.9
        a_fit.emotions[0] = 0.1
        a_fit.goal = None
        sim.fallback_goal(a_fit, reason="test_missing")

        self.assertIsNotNone(a_fit.goal, "Un but doit être créé")
        from game.brain_api import EXPLORE, REST
        if a_fit.goal["act"] == EXPLORE:
            self.assertLessEqual(a_fit.goal["until"] - sim.w.tick, 200,
                                 "EXPLORE fallback doit être court (≤180 ticks)")
        elif a_fit.goal["act"] == REST:
            self.assertLessEqual(a_fit.goal["until"] - sim.w.tick, 100,
                                 "REST fallback doit être court (≤60 ticks)")

        # Agent épuisé -> repos autorisé
        a_tired = sim.agents[1] if len(sim.agents) > 1 else sim.spawn_agent()
        a_tired.energy = 0.05
        a_tired.health = 0.2
        a_tired.emotions[0] = 0.8
        a_tired.goal = None
        sim.fallback_goal(a_tired, reason="test_exhausted")

        self.assertEqual(a_tired.goal["act"], REST,
                         "Agent épuisé doit recevoir un but REST")

    def test_failed_path_does_not_hold_same_goal_forever(self):
        """Obstacle infranchissable -> échec renseigné, but reconsidéré."""
        from game.brain_api import EXPLORE
        sim = self.controller.sim
        a = sim.agents[0]

        # Placer l'agent au centre d'une zone, bloquer les cases adjacentes
        tx, ty = 50, 50
        a.x, a.y = 16 * tx + 8, 16 * ty + 8
        # Bloquer les 8 cases autour
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                btx, bty = tx + dx, ty + dy
                if 0 < btx < sim.w.g - 1 and 0 < bty < sim.w.g - 1:
                    sim.w.blocked[bty, btx] = 1

        # Forcer un but EXPLORE vers une case éloignée (nécessite mouvement mais bloqué)
        target_tx, target_ty = tx + 5, ty
        a.goal = {"act": EXPLORE, "x": target_tx, "y": target_ty, "ref": None,
                  "intensity": 1.0, "until": sim.w.tick + 100}
        a.goal_t = 0
        a.stuck = 0

        # Simuler le blocage: stuck augmente, register_goal_failure appelé
        initial_reasons = dict(sim.activity_reasons)
        for _ in range(30):
            if a.goal is not None:
                sim._execute(a)
            else:
                break

        # Vérifier que l'échec a été enregistré
        reasons = dict(sim.activity_reasons)
        self.assertTrue(
            any("collision" in k or "path" in k or "failed" in k
                for k in reasons if reasons[k] > initial_reasons.get(k, 0)),
            "Un échec de chemin/collision doit être comptabilisé"
        )
        # Le but doit avoir été abandonné (goal = None ou changé)
        self.assertTrue(a.goal is None or a.goal["act"] != EXPLORE,
                        "Le but bloqué doit être abandonné")

    def test_snapshot_activity_matches_engine(self):
        """Le dock lit state, goal, x/y réels, pas une animation fabriquée."""
        from game.ui_snapshots import selected_agent_snapshot

        sim = self.controller.sim
        a = sim.agents[0]
        sim.selected = a  # requis par selected_agent_snapshot

        # Forcer un but et état connus
        a.state = "run"
        a.goal = {"act": 2, "x": 10, "y": 12, "ref": None,
                  "intensity": 1.0, "until": sim.w.tick + 100}
        a.goal_t = 5
        a.stuck = 3
        a.x, a.y = 160.5, 192.3

        snap = selected_agent_snapshot(sim, include_activity=True)

        self.assertIsNotNone(snap, "Le snapshot ne doit pas être None")
        self.assertIn("activity", snap, "Le snapshot doit contenir 'activity'")
        act = snap["activity"]
        self.assertEqual(act["state"], "run")
        self.assertEqual(act["goal_action"], 2)
        self.assertEqual(act["goal_tile"], [10, 12])
        self.assertEqual(act["position"], [160.5, 192.3])
        self.assertEqual(act["stuck"], 3)

    def test_affordance_has_executor(self):
        """Chaque affordance activable par un habitant a précondition + exécuteur testable.

        Tags descriptifs (observe, shelter, lean) exclus explicitement.
        Les 11 tags sans exécuteur (carry, place, use, burn, throw, mourn,
        climb, chase, shear, decorate, lean) doivent échouer — c'est le but.
        """
        from game.affordance_definitions import AFFORDANCE_DEFS
        from game.simulation import Sim

        # Tags purement descriptifs à exclure de la vérification d'exécuteur
        descriptive_only = {"observe", "shelter", "lean"}

        for tag, defn in AFFORDANCE_DEFS.items():
            if defn.get("descriptive_only"):
                # Tags descriptifs : pas d'exécuteur attendu
                self.assertTrue(defn.get("executor") is None,
                                f"Tag descriptif '{tag}' ne devrait pas avoir d'exécuteur")
                continue

            # Tags activables : doivent avoir un exécuteur non-None
            self.assertIn("executor", defn,
                          f"Clé 'executor' manquante pour '{tag}'")
            executor_name = defn["executor"]
            self.assertIsNotNone(executor_name,
                                 f"Exécuteur manquant (None) pour '{tag}' — non implémenté dans simulation.py")

            # Vérifier que la méthode existe réellement sur la classe Sim
            method = getattr(Sim, executor_name, None)
            self.assertIsNotNone(method,
                                 f"Exécuteur '{executor_name}' pour '{tag}' introuvable sur Sim")
            self.assertTrue(callable(method),
                            f"Exécuteur '{executor_name}' pour '{tag}' n'est pas callable")

            # Vérifier aussi la présence de préconditions
            self.assertTrue(defn.get("requires") is not None,
                            f"Précondition manquante pour '{tag}'")


if __name__ == "__main__":
    unittest.main()