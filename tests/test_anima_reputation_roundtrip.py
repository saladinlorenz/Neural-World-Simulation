"""Lot F — update_reputation remplit le dict et survit au save/load."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _make_sim(seed=42, n_agents=3):
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    from game.engine import build_world

    am = AssetManager(headless=True).discover()
    am.ensure_procedural_blocks()
    _set_asset_manager(am)
    _, sim = build_world(am, seed=seed, procedural=True, n_agents=n_agents)
    return sim, am


def test_update_reputation_fills_dict():
    sim, _ = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.rep = 7.5
    a.rel = {1: [0.4, 0.1], 2: [-0.3, 0.0]}

    sim.update_reputation(a)
    rep = a.anima["reputation"]
    assert set(rep) == {"social", "trust_balance", "updated_tick"}
    assert abs(rep["social"] - 0.75) < 1e-9
    assert abs(rep["trust_balance"] - 0.1) < 1e-9  # 0.4 - 0.3
    assert rep["updated_tick"] == sim.w.tick


def test_social_clamped_to_unit():
    sim, _ = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.rep = 100.0
    sim.update_reputation(a)
    assert a.anima["reputation"]["social"] == 1.0

    a.rep = -100.0
    sim.update_reputation(a)
    assert a.anima["reputation"]["social"] == -1.0


def test_reputation_auto_updated_after_120_ticks():
    sim, _ = _make_sim(seed=7)
    for _ in range(130):
        sim.step()
    alive = [a for a in sim.agents if a.alive]
    assert alive, "aucun agent vivant apres 130 ticks"
    filled = [a for a in alive if a.anima.get("reputation")]
    assert filled, "reputation vide apres ~120 ticks"
    for a in filled:
        rep = a.anima["reputation"]
        assert "social" in rep and "updated_tick" in rep
        assert math.isfinite(rep["social"])


def test_reputation_save_load_roundtrip():
    from game.save import save_game, load_game, _slot_path

    sim, am = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.rep = 3.2
    a.rel = {9: [0.25, -0.1]}
    sim.update_reputation(a)
    before = dict(a.anima["reputation"])

    slot = 93
    try:
        save_game(sim, cam=None, slot=slot)
        loaded, _ = load_game(am, slot=slot)
        assert loaded is not None
        a2 = next((x for x in loaded.agents if x.eid == a.eid), None)
        assert a2 is not None, "agent absent apres load"
        assert a2.anima["reputation"] == before, (
            before, a2.anima["reputation"])
    finally:
        try:
            os.remove(_slot_path(slot))
        except OSError:
            pass


if __name__ == "__main__":
    test_update_reputation_fills_dict()
    test_social_clamped_to_unit()
    test_reputation_auto_updated_after_120_ticks()
    test_reputation_save_load_roundtrip()
    print("ALL TESTS PASSED")
