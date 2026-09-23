"""Tests zones spatiales (Lot G.2) + état UI sauvegardé (Save v3)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _make_sim():
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    from game.engine import build_world

    am = AssetManager(headless=True).discover()
    am.ensure_procedural_blocks()
    _set_asset_manager(am)
    w, sim = build_world(am, seed=7, procedural=True, n_agents=3)
    return sim, am


def test_district_zone_roundtrip():
    from game.zones import District, PredatorZone
    from game.save import save_game, load_game, _slot_path

    sim, am = _make_sim()
    d = District(id="q1", name="Marche", x0=5, y0=5, x1=10, y1=12,
                 residents={1, 2}, created_tick=3)
    z = PredatorZone(id="z1", name="Clancage", x0=20, y0=20, x1=30, y1=30,
                     allowed_kinds={"wolf"}, hard_boundary=True, visible=False)
    sim.districts["q1"] = d
    sim.predator_zones["z1"] = z

    m = sim.spawn_monster(x=24 * 16, y=24 * 16, kind="wolf")
    assert m is not None
    assert m.zone_id == "z1", f"zone_id spawn attendu z1, obtenu {m.zone_id}"

    slot = 95
    try:
        save_game(sim, cam=None, slot=slot)
        loaded, _ = load_game(am, slot=slot)
        assert loaded is not None
        assert "q1" in loaded.districts
        assert loaded.districts["q1"].residents == {1, 2}
        assert "z1" in loaded.predator_zones
        assert loaded.predator_zones["z1"].allowed_kinds == {"wolf"}
        lm = [x for x in loaded.monsters if x.eid == m.eid]
        assert lm and lm[0].zone_id == "z1", "zone_id monstre perdu"
    finally:
        try:
            os.remove(_slot_path(slot))
        except OSError:
            pass
    print("OK test_district_zone_roundtrip")


def test_can_monster_enter():
    from game.zones import PredatorZone, can_monster_enter

    sim, _ = _make_sim()
    z = PredatorZone(id="z1", name="zone", x0=10, y0=10, x1=15, y1=15)
    sim.predator_zones["z1"] = z
    m = sim.spawn_monster(x=12 * 16, y=12 * 16, kind="wolf")
    assert can_monster_enter(sim, m, 12, 12) is True
    assert can_monster_enter(sim, m, 40, 40) is False
    m.zone_id = None
    assert can_monster_enter(sim, m, 40, 40) is True
    print("OK test_can_monster_enter")


def test_ui_state_save_roundtrip():
    from game.save import save_game, load_game, _slot_path

    sim, am = _make_sim()
    slot = 94
    ui = {"favs": [3, 7], "recents": [9], "brain_size": 64,
          "active_overlay": "memoire"}
    try:
        save_game(sim, cam=None, slot=slot, ui_state=ui)
        loaded, _ = load_game(am, slot=slot)
        assert loaded is not None
        assert loaded.loaded_ui_state == ui, "ui_state perdu"
        fp = loaded.loaded_catalog_fingerprint
        assert fp and len(fp) == 64, f"empreinte absente: {fp!r}"
    finally:
        try:
            os.remove(_slot_path(slot))
        except OSError:
            pass
    print("OK test_ui_state_save_roundtrip")


def test_ui_state_apply_dict():
    from game.ui_state import UIState

    s = UIState()
    s.apply_dict({"favs": [1, 2], "brain_size": 32, "selected_tile": (4, 5),
                  "unknown_key": "ignored"})
    assert s.favs == [1, 2]
    assert s.brain_size == 32
    assert s.selected_tile == (4, 5)
    assert not hasattr(s, "unknown_key")
    print("OK test_ui_state_apply_dict")


def test_overlay_context_modes_gate():
    from game.simulation import Sim

    sim, _ = _make_sim()
    sim.selected = None
    from ui_qt.studio.world_overlay import CONTEXT_MODES, WorldOverlay
    assert "memoire" in CONTEXT_MODES
    assert "ressources" not in CONTEXT_MODES
    ov = WorldOverlay()
    help_text = ov.mode_help("memoire")
    assert help_text, "mode_help vide"
    print("OK test_overlay_context_modes_gate")


if __name__ == "__main__":
    test_district_zone_roundtrip()
    test_can_monster_enter()
    test_ui_state_save_roundtrip()
    test_ui_state_apply_dict()
    test_overlay_context_modes_gate()
    print("ALL TESTS PASSED")
