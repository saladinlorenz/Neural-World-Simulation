"""Lot B — TimelineDock : refresh sans crash, combo = ids du registre partagé."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ["QT_QPA_PLATFORM"] = "offscreen"


def _make_controller():
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    from game.engine import build_world
    from game.simulation_controller import SimulationController

    am = AssetManager(headless=True).discover()
    am.ensure_procedural_blocks()
    _set_asset_manager(am)
    _, sim = build_world(am, seed=42, procedural=True, n_agents=3)
    return SimulationController(sim)


_APP = None


def _app():
    global _APP
    from PyQt6.QtWidgets import QApplication
    _APP = QApplication.instance()
    if _APP is None:
        _APP = QApplication(sys.argv)
    return _APP


def test_combo_matches_registry():
    from game.ui_registry import JOURNAL_CATEGORIES, ALL_CATEGORIES

    _app()
    controller = _make_controller()
    from ui_qt.studio.timeline_dock import TimelineDock
    dock = TimelineDock(controller)

    assert dock._cat_combo.count() == 1 + len(JOURNAL_CATEGORIES)
    assert dock._cat_combo.itemData(0) == ALL_CATEGORIES
    ids = [dock._cat_combo.itemData(i) for i in range(dock._cat_combo.count())]
    assert ids == [ALL_CATEGORIES] + list(JOURNAL_CATEGORIES)
    dock.close()


def test_refresh_keeps_journal_categories():
    _app()
    controller = _make_controller()
    sim = controller.sim
    sim.log("Le ciel se couvre.", (100, 140, 200), "world")
    sim.log("Un habitant s'est éteint.", (140, 80, 80), "death")

    from ui_qt.studio.timeline_dock import TimelineDock
    dock = TimelineDock(controller)
    dock.refresh()
    assert dock._events, "timeline vide apres refresh"

    cats = {e["category"] for e in dock._events}
    assert "world" in cats, f"categorie world perdue: {cats}"
    assert "death" in cats, f"categorie death perdue: {cats}"

    world_idx = dock._cat_combo.findData("world")
    assert world_idx > 0
    dock._cat_combo.setCurrentIndex(world_idx)  # declenche _apply_filter
    assert dock._table.rowCount() >= 1
    assert all(e["category"] == "world"
               for e in dock._events if e["category"] == "world")
    dock.close()


if __name__ == "__main__":
    test_combo_matches_registry()
    test_refresh_keeps_journal_categories()
    print("ALL TESTS PASSED")
