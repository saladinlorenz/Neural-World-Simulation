"""Lot H — soak 10000 ticks : invariants + garde-fous NaN.

Audit manuel associé (hors CI, ~10 min, config réelle) :
    python main_qt.py --procedural 1 --seed 7 --agents 60 --sheep 40 --speed 1
    → sans freeze, inspecteur rempli, institutions après activité de stockage,
      reputation non vide après ~120 ticks, overlays EN, timeline peuplée.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TICKS = 10000
N_AGENTS = 3


def _make_sim():
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    from game.engine import build_world

    am = AssetManager(headless=True).discover()
    am.ensure_procedural_blocks()
    am.ensure_procedural_tools()
    am.ensure_kaykit_resources()
    _set_asset_manager(am)
    _, sim = build_world(am, seed=7, procedural=True, n_agents=N_AGENTS)
    return sim


def test_long_run_no_invariant_failure():
    from game.invariants import validate_simulation

    sim = _make_sim()
    for _ in range(TICKS):
        sim.step()

    errors = validate_simulation(sim)
    assert errors == [], errors

    for a in sim.agents:
        if not a.alive:
            continue
        for k, v in a.anima.get("identity", {}).items():
            assert math.isfinite(v), f"NaN identity[{k}]"
        for k, v in a.anima.get("values", {}).items():
            assert math.isfinite(v), f"NaN values[{k}]"
        for k, v in a.anima.get("trauma", {}).items():
            assert math.isfinite(v), f"NaN trauma[{k}]"
        for eid, bdict in a.anima.get("beliefs", {}).get("beings", {}).items():
            if isinstance(bdict, dict):
                for bk, bv in bdict.items():
                    assert math.isfinite(bv), f"NaN belief[{eid}][{bk}]"
        for k, v in a.anima.get("reputation", {}).items():
            if isinstance(v, float):
                assert math.isfinite(v), f"NaN reputation[{k}]"


if __name__ == "__main__":
    test_long_run_no_invariant_failure()
    print("ALL TESTS PASSED")
