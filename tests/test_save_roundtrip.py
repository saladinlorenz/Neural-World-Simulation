"""Tests sauvegarde — roundtrip save/load, champ version, CropPlot.watered."""
import os
import sys

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
    w, sim = build_world(am, seed=42, procedural=True, n_agents=5)
    return sim, am


def test_save_version_field():
    import pickle
    from game.save import save_game, _slot_path
    from game.world import CropPlot

    sim, _ = _make_sim()
    plot = CropPlot(tx=10, ty=10, owner_eid=None, planted_tick=0)
    plot.watered = True
    sim.w.crop_plots[(10, 10)] = plot

    slot = 99
    try:
        save_game(sim, cam=None, slot=slot)
        path = _slot_path(slot)
        with open(path, "rb") as f:
            data = pickle.load(f)
        assert data.get("version") == 3, f"version attendue=3, obtenue={data.get('version')}"
    finally:
        try:
            os.remove(_slot_path(slot))
        except OSError:
            pass
    print("OK test_save_version_field")


def test_save_roundtrip_watered():
    from game.save import save_game, load_game, _slot_path
    from game.world import CropPlot

    sim, am = _make_sim()
    plot = CropPlot(tx=12, ty=15, owner_eid=None, planted_tick=0)
    plot.watered = True
    plot.growth = 0.42
    sim.w.crop_plots[(12, 15)] = plot

    slot = 98
    try:
        save_game(sim, cam=None, slot=slot)
        loaded, _ = load_game(am, slot=slot)
        assert loaded is not None, "load_game a retourne (None, None)"
        cp = loaded.w.crop_plots.get((12, 15))
        assert cp is not None, "CropPlot (12,15) absent apres load"
        assert cp.watered is True, f"watered perdu: {cp.watered}"
        assert abs(cp.growth - 0.42) < 1e-6, f"growth perdu: {cp.growth}"
    finally:
        try:
            os.remove(_slot_path(slot))
        except OSError:
            pass
    print("OK test_save_roundtrip_watered")


def test_load_future_version_rejected():
    import pickle
    from game.save import load_game, _slot_path

    sim, am = _make_sim()
    slot = 97
    try:
        fake = {"version": 99, "land": sim.w.land}
        with open(_slot_path(slot), "wb") as f:
            pickle.dump(fake, f, protocol=5)
        try:
            load_game(am, slot=slot)
            raise AssertionError("load_game aurait du rejeter version 99")
        except ValueError as e:
            assert "99" in str(e)
    finally:
        try:
            os.remove(_slot_path(slot))
        except OSError:
            pass
    print("OK test_load_future_version_rejected")


if __name__ == "__main__":
    test_save_version_field()
    test_save_roundtrip_watered()
    test_load_future_version_rejected()
    print("ALL TESTS PASSED")
