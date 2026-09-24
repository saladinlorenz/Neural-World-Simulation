"""Lot G — compatibilité save v2 : charge avec défauts (sans ui_state ni fingerprint)."""
import os
import pickle
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _make_sim():
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    from game.engine import build_world

    am = AssetManager(headless=True).discover()
    am.ensure_procedural_blocks()
    _set_asset_manager(am)
    _, sim = build_world(am, seed=42, procedural=True, n_agents=5)
    return sim, am


def test_load_v2_without_ui_state_and_fingerprint():
    from game.save import save_game, load_game, _slot_path

    sim, am = _make_sim()
    slot = 92
    try:
        save_game(sim, cam=None, slot=slot)
        with open(_slot_path(slot), "rb") as f:
            data = pickle.load(f)

        data["version"] = 2
        data.pop("ui_state", None)
        data.pop("asset_catalog_fingerprint", None)
        with open(_slot_path(slot), "wb") as f:
            pickle.dump(data, f, protocol=5)

        loaded, _ = load_game(am, slot=slot)
        assert loaded is not None, "save v2 non chargee"
        assert loaded.loaded_ui_state is None, "ui_state devrait etre None"
        assert loaded.loaded_catalog_fingerprint is None
        assert len(loaded.agents) == len(sim.agents)
        # tickable apres chargement
        loaded.step()
    finally:
        try:
            os.remove(_slot_path(slot))
        except OSError:
            pass


def test_ui_state_defaults_when_absent():
    from game.ui_state import UIState

    s = UIState()
    s.apply_dict({})  # aucune cle : defauts anglais
    assert s.journal_filter == "all"
    assert s.active_overlay == "normal"


if __name__ == "__main__":
    test_load_v2_without_ui_state_and_fingerprint()
    test_ui_state_defaults_when_absent()
    print("ALL TESTS PASSED")
