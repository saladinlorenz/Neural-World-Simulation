"""Lot D.5 : undo/redo des outils monde (game/history.py).

Un coup de pinceau glissé doit produire UNE seule entrée d'historique,
l'annulation doit restaurer exactement les tranches numpy capturées, et
les piles doivent rester bornées à 50 entrées.
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
    world, sim = build_world(am, seed=21, procedural=False, populate_dense=False)
    seed_life(world, sim, sim.rng, n_agents=2, n_sheep=0)
    return sim


def _land_row(sim, ty, x0, x1):
    return [int(v) for v in sim.w.land[ty, x0:x1]]


class TestWorldHistory(unittest.TestCase):
    def test_paint_then_undo_restores(self):
        sim = _make_sim()
        tx = ty = 500
        x0, x1 = tx - 4, tx + 5
        before = _land_row(sim, ty, x0, x1)
        self.assertTrue(any(before))

        result = execute_command(sim, {"kind": "paint_tile", "tx": tx, "ty": ty,
                                       "mode": "water", "radius": 3})
        self.assertTrue(result.get("ok"), result)
        after = _land_row(sim, ty, x0, x1)
        self.assertNotEqual(after, before)

        undo = execute_command(sim, {"kind": "undo"})
        self.assertTrue(undo.get("ok"), undo)
        self.assertTrue(undo.get("changed"))
        self.assertEqual(_land_row(sim, ty, x0, x1), before)

        redo = execute_command(sim, {"kind": "redo"})
        self.assertTrue(redo.get("ok"), redo)
        self.assertEqual(_land_row(sim, ty, x0, x1), after)

        undo2 = execute_command(sim, {"kind": "undo"})
        self.assertTrue(undo2.get("changed"))
        self.assertEqual(_land_row(sim, ty, x0, x1), before)

    def test_drag_is_one_history_entry(self):
        sim = _make_sim()
        ty = 400
        before = _land_row(sim, ty, 300, 312)
        for i, tx in enumerate(range(302, 309)):
            result = execute_command(sim, {"kind": "paint_tile", "tx": tx,
                                           "ty": ty, "mode": "water",
                                           "radius": 2, "group": 77})
            self.assertTrue(result.get("ok"), result)
        execute_command(sim, {"kind": "end_stroke"})
        self.assertNotEqual(_land_row(sim, ty, 300, 312), before)

        undo = execute_command(sim, {"kind": "undo"})
        self.assertTrue(undo.get("changed"))
        # Une seule annulation doit tout restaurer : une entree par glisser.
        self.assertEqual(_land_row(sim, ty, 300, 312), before)
        self.assertFalse(execute_command(sim, {"kind": "undo"}).get("changed"))

    def test_failed_command_leaves_no_entry(self):
        sim = _make_sim()
        result = execute_command(sim, {"kind": "paint_tile", "tx": 10, "ty": 10,
                                       "mode": "lave", "radius": 2})
        self.assertFalse(result.get("ok"))
        self.assertFalse(execute_command(sim, {"kind": "undo"}).get("changed"))

    def test_stack_capped_at_50(self):
        sim = _make_sim()
        for i in range(60):
            result = execute_command(sim, {"kind": "paint_tile",
                                           "tx": 100 + i, "ty": 100,
                                           "mode": "land", "radius": 1})
            self.assertTrue(result.get("ok"), result)
        depth = 0
        while execute_command(sim, {"kind": "undo"}).get("changed"):
            depth += 1
            self.assertLessEqual(depth, 50)
        self.assertEqual(depth, 50)


if __name__ == "__main__":
    unittest.main()
