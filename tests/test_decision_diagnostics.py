"""Phase 1 — diagnostic réel de décision des habitants.

Tests déterministes et bornés : ils vérifient la classification des
candidats, la trace produite par ``evaluate_candidates``, son exposition
dans le snapshot de l'habitant sélectionné, et son affichage dans
l'inspecteur Qt — sans jamais recalculer les candidats côté UI.
"""
import os
import sys
import unittest

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import game.actioncandidate as ac
from game.actioncandidate import (
    ActionCandidate, classify_candidate, evaluate_candidates,
    STATE_SELECTED, STATE_FEASIBLE, STATE_REJECTED, STATE_INVALID,
    STATE_EXPIRED, REASON_TARGET_MISSING, REASON_DANGER, REASON_ENERGY,
    REASON_MEMORY_OLD, REASON_BLOCKED, REASON_BETTER,
)


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


def _cand(verb="pickup", kind="item", tx=0, ty=0, tid=None,
          cost=0.5, risk=0.0, motive="economy"):
    return ActionCandidate(verb=verb, target_kind=kind, target_id=tid,
                           tx=tx, ty=ty, estimated_cost=cost,
                           estimated_risk=risk, motive=motive)


class _SimFixture(unittest.TestCase):
    """Contrôleur partagé + tuile de l'agent rendue libre et sûre."""

    @classmethod
    def setUpClass(cls):
        cls.controller = _make_controller()
        cls.sim = cls.controller.sim
        cls.agent = next(a for a in cls.sim.agents if a.alive)

    def setUp(self):
        a = self.agent
        w = self.sim.w
        self.tx, self.ty = int(a.tx), int(a.ty)
        self._orig = {
            "land": bool(w.land[self.ty, self.tx]),
            "blocked": bool(w.blocked[self.ty, self.tx]),
            "energy": float(a.energy),
            "belief": dict(a.belief_places),
            "failed": dict(a.failed_targets),
            "seen_food": list(a.seen.get("food", [])),
            "goal": a.goal,
        }
        w.land[self.ty, self.tx] = 1
        w.blocked[self.ty, self.tx] = 0
        a.energy = 0.9
        a.belief_places = {}
        a.failed_targets = {}
        a.seen["food"] = []

    def tearDown(self):
        a = self.agent
        w = self.sim.w
        o = self._orig
        w.land[self.ty, self.tx] = o["land"]
        w.blocked[self.ty, self.tx] = o["blocked"]
        a.energy = o["energy"]
        a.belief_places = o["belief"]
        a.failed_targets = o["failed"]
        a.seen["food"] = o["seen_food"]
        a.goal = o["goal"]


class TestClassifyCandidate(_SimFixture):

    def test_out_of_world_is_invalid(self):
        c = _cand(tx=self.sim.w.g + 5, ty=self.sim.w.g + 5)
        state, reason = classify_candidate(self.sim, self.agent, c)
        self.assertEqual(state, STATE_INVALID)
        self.assertEqual(reason, REASON_TARGET_MISSING)

    def test_blocked_tile_is_invalid(self):
        self.sim.w.blocked[self.ty, self.tx] = 1
        c = _cand(tx=self.tx, ty=self.ty)
        state, reason = classify_candidate(self.sim, self.agent, c)
        self.assertEqual(state, STATE_INVALID)
        self.assertEqual(reason, REASON_BLOCKED)

    def test_water_tile_is_invalid(self):
        self.sim.w.land[self.ty, self.tx] = 0
        self.sim.w.blocked[self.ty, self.tx] = 0
        c = _cand(tx=self.tx, ty=self.ty)
        state, reason = classify_candidate(self.sim, self.agent, c)
        self.assertEqual(state, STATE_INVALID)
        self.assertEqual(reason, REASON_TARGET_MISSING)

    def test_blacklisted_target_is_blocked(self):
        act = ac._verb_action("pickup")
        self.agent.failed_targets[(act, self.tx, self.ty)] = (1, self.sim.w.tick + 500)
        c = _cand(tx=self.tx, ty=self.ty)
        state, reason = classify_candidate(self.sim, self.agent, c)
        self.assertEqual(state, STATE_INVALID)
        self.assertEqual(reason, REASON_BLOCKED)

    def test_dead_follow_target_is_invalid(self):
        c = _cand(verb="follow", kind="agent", tid=999999,
                  tx=self.tx, ty=self.ty)
        state, reason = classify_candidate(self.sim, self.agent, c)
        self.assertEqual(state, STATE_INVALID)
        self.assertEqual(reason, REASON_TARGET_MISSING)

    def test_danger_rejects(self):
        self.agent.belief_places[(self.tx // 8, self.ty // 8)] = 0.9
        c = _cand(tx=self.tx, ty=self.ty)
        state, reason = classify_candidate(self.sim, self.agent, c)
        self.assertEqual(state, STATE_REJECTED)
        self.assertEqual(reason, REASON_DANGER)

    def test_high_estimated_risk_rejects(self):
        c = _cand(tx=self.tx, ty=self.ty, risk=0.8)
        state, reason = classify_candidate(self.sim, self.agent, c)
        self.assertEqual(state, STATE_REJECTED)
        self.assertEqual(reason, REASON_DANGER)

    def test_low_energy_rejects_movement(self):
        self.agent.energy = 0.05
        c = _cand(verb="pickup", tx=self.tx, ty=self.ty)
        state, reason = classify_candidate(self.sim, self.agent, c)
        self.assertEqual(state, STATE_REJECTED)
        self.assertEqual(reason, REASON_ENERGY)

    def test_sit_exempt_from_energy(self):
        self.agent.energy = 0.05
        c = _cand(verb="sit", kind="spot", tx=self.tx, ty=self.ty)
        state, reason = classify_candidate(self.sim, self.agent, c)
        self.assertEqual(state, STATE_FEASIBLE)
        self.assertIsNone(reason)

    def test_stale_memory_expires(self):
        self.agent.seen["food"] = [(self.tx, self.ty, 0.10)]
        c = _cand(verb="pickup", kind="item", tid=None,
                  tx=self.tx, ty=self.ty)
        state, reason = classify_candidate(self.sim, self.agent, c)
        self.assertEqual(state, STATE_EXPIRED)
        self.assertEqual(reason, REASON_MEMORY_OLD)

    def test_perceived_item_is_feasible(self):
        c = _cand(verb="pickup", kind="item", tid=12345,
                  tx=self.tx, ty=self.ty)
        state, reason = classify_candidate(self.sim, self.agent, c)
        self.assertEqual(state, STATE_FEASIBLE)
        self.assertIsNone(reason)


class TestEvaluateCandidates(_SimFixture):

    def _patch(self, candidates):
        original = ac.propose_candidates
        ac.propose_candidates = lambda sim, a: list(candidates)
        self.addCleanup(setattr, ac, "propose_candidates", original)

    def test_best_feasible_is_selected_other_is_better(self):
        cheap = _cand(tx=self.tx, ty=self.ty, cost=0.1)
        pricey = _cand(verb="sit", kind="spot", tx=self.tx, ty=self.ty, cost=0.9)
        self._patch([cheap, pricey])
        trace = evaluate_candidates(self.sim, self.agent)
        self.assertEqual(len(trace), 2)
        by_cost = {round(t["estimated_cost"], 3): t for t in trace}
        self.assertEqual(by_cost[0.1]["state"], STATE_SELECTED)
        self.assertIsNone(by_cost[0.1]["reason"])
        self.assertEqual(by_cost[0.9]["state"], STATE_FEASIBLE)
        self.assertEqual(by_cost[0.9]["reason"], REASON_BETTER)

    def test_selected_is_first_row(self):
        cands = [_cand(tx=self.tx, ty=self.ty, cost=0.05 * i) for i in range(4)]
        self._patch(cands)
        trace = evaluate_candidates(self.sim, self.agent)
        self.assertEqual(trace[0]["state"], STATE_SELECTED)

    def test_limit_to_eight(self):
        cands = [_cand(tx=self.tx, ty=self.ty, cost=0.05 * i) for i in range(12)]
        self._patch(cands)
        trace = evaluate_candidates(self.sim, self.agent)
        self.assertEqual(len(trace), 8)
        self.assertEqual(
            sum(1 for t in trace if t["state"] == STATE_SELECTED), 1)

    def test_invalid_and_rejected_kept_with_reason(self):
        good = _cand(tx=self.tx, ty=self.ty, cost=0.1)
        dangerous = _cand(tx=self.tx, ty=self.ty, cost=0.2, risk=0.9)
        self._patch([good, dangerous])
        trace = evaluate_candidates(self.sim, self.agent)
        states = {round(t["estimated_cost"], 3): t["state"] for t in trace}
        self.assertEqual(states[0.1], STATE_SELECTED)
        self.assertEqual(states[0.2], STATE_REJECTED)

    def test_no_candidate_gives_empty_trace(self):
        self._patch([])
        self.assertEqual(evaluate_candidates(self.sim, self.agent), [])

    def test_does_not_mutate_goal(self):
        self.agent.goal = None
        self._patch([_cand(tx=self.tx, ty=self.ty)])
        evaluate_candidates(self.sim, self.agent)
        self.assertIsNone(self.agent.goal)

    def test_trace_rows_are_plain_and_complete(self):
        self._patch([_cand(tx=self.tx, ty=self.ty)])
        row = evaluate_candidates(self.sim, self.agent)[0]
        import json
        json.dumps(row)
        for key in ("verb", "target_kind", "tx", "ty", "estimated_cost",
                    "estimated_risk", "motive", "score", "state", "reason",
                    "distance"):
            self.assertIn(key, row)


class TestSnapshotPossibilities(_SimFixture):

    def _sample(self):
        return {"verb": "pickup", "target_kind": "item", "target_id": None,
                "tx": self.tx, "ty": self.ty, "distance": 0,
                "estimated_cost": 0.5, "estimated_risk": 0.0,
                "motive": "economy", "score": -0.5,
                "state": STATE_SELECTED, "reason": None}

    def test_base_snapshot_has_no_possibilities(self):
        from game.ui_snapshots import selected_agent_snapshot
        self.sim.selected = self.agent
        snap = selected_agent_snapshot(self.sim)
        self.assertNotIn("possibilities", snap)

    def test_include_activity_exposes_trace(self):
        from game.ui_snapshots import selected_agent_snapshot
        sample = self._sample()
        self.agent.decision_trace = [sample]
        self.sim.selected = self.agent
        snap = selected_agent_snapshot(self.sim, include_activity=True)
        self.assertIn("possibilities", snap)
        self.assertEqual(snap["possibilities"], [sample])
        # copie défensive : pas la même liste que la trace moteur
        self.assertIsNot(snap["possibilities"], self.agent.decision_trace)

    def test_snapshot_never_recomputes(self):
        from game.ui_snapshots import selected_agent_snapshot

        def _boom(*a, **k):
            raise AssertionError("le snapshot ne doit pas recalculer")

        original = ac.evaluate_candidates
        ac.evaluate_candidates = _boom
        self.addCleanup(setattr, ac, "evaluate_candidates", original)
        self.agent.decision_trace = [self._sample()]
        self.sim.selected = self.agent
        snap = selected_agent_snapshot(self.sim, include_activity=True)
        self.assertEqual(len(snap["possibilities"]), 1)


class TestInspectorDockPossibilities(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from PyQt6.QtWidgets import QApplication
        cls.app = QApplication.instance() or QApplication([])
        cls.controller = _make_controller()

    def _agent(self):
        return next(a for a in self.controller.sim.agents if a.alive)

    def _rows(self, a):
        return [
            {"verb": "pickup", "target_kind": "item", "target_id": None,
             "tx": a.tx, "ty": a.ty, "distance": 2, "estimated_cost": 0.5,
             "estimated_risk": 0.0, "motive": "economy", "score": -0.5,
             "state": STATE_SELECTED, "reason": None},
            {"verb": "follow", "target_kind": "agent", "target_id": 7,
             "tx": a.tx, "ty": a.ty, "distance": 3, "estimated_cost": 0.6,
             "estimated_risk": 0.1, "motive": "social", "score": -0.7,
             "state": STATE_REJECTED, "reason": REASON_DANGER},
        ]

    def test_section_renders_rows_without_recompute(self):
        from PyQt6 import QtWidgets
        from ui_qt.main_window import MainWindow

        def _boom(*a, **k):
            raise AssertionError("l'UI ne doit pas recalculer les candidats")

        orig_eval = ac.evaluate_candidates
        orig_prop = ac.propose_candidates
        ac.evaluate_candidates = _boom
        ac.propose_candidates = _boom
        self.addCleanup(setattr, ac, "evaluate_candidates", orig_eval)
        self.addCleanup(setattr, ac, "propose_candidates", orig_prop)

        sim = self.controller.sim
        agent = self._agent()
        agent.decision_trace = self._rows(agent)

        win = MainWindow(self.controller)
        try:
            self.controller.execute({"kind": "select_agent", "eid": agent.eid})
            dock = win._inspector_dock
            dock.refresh()
            self.assertFalse(dock._possibilities_group.isHidden())
            self.assertTrue(dock._possibilities_empty.isHidden())
            # 2 lignes + en-tête : au moins 3 rangées de 6 cellules
            self.assertGreaterEqual(dock._possibilities_grid.count(), 12)
            texts = []
            for i in range(dock._possibilities_grid.count()):
                w = dock._possibilities_grid.itemAt(i).widget()
                if w is not None:
                    texts.append(w.text())
            self.assertIn("Ramasser", texts)
            self.assertIn("choisi", " ".join(texts))
            self.assertIn("danger trop élevé", " ".join(texts))
        finally:
            agent.decision_trace = []
            win.close()
            QtWidgets.QWidget.deleteLater(win)
            self.app.processEvents()

    def test_empty_trace_shows_placeholder(self):
        from PyQt6 import QtWidgets
        from ui_qt.main_window import MainWindow

        sim = self.controller.sim
        agent = self._agent()
        agent.decision_trace = []
        win = MainWindow(self.controller)
        try:
            self.controller.execute({"kind": "select_agent", "eid": agent.eid})
            dock = win._inspector_dock
            dock.refresh()
            self.assertFalse(dock._possibilities_group.isHidden())
            self.assertFalse(dock._possibilities_empty.isHidden())
            self.assertEqual(dock._possibilities_grid.count(), 0)
        finally:
            win.close()
            QtWidgets.QWidget.deleteLater(win)
            self.app.processEvents()

    def test_hidden_when_no_selection(self):
        from PyQt6 import QtWidgets
        from ui_qt.main_window import MainWindow

        sim = self.controller.sim
        win = MainWindow(self.controller)
        try:
            sim.selected = None
            self.controller.ui_state.selected_agent_eid = None
            dock = win._inspector_dock
            dock.refresh()
            self.assertTrue(dock._possibilities_group.isHidden())
            self.assertEqual(dock._possibilities_grid.count(), 0)
        finally:
            win.close()
            QtWidgets.QWidget.deleteLater(win)
            self.app.processEvents()


if __name__ == "__main__":
    unittest.main()
