"""Tests headless — vérifie stabilité après changements."""
import sys, os, time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_brain_132():
    from game.brain import Brain, N_IN, N_OUT, N_STRATEGIES, N_TARGETS
    assert N_IN == 132
    assert N_OUT == 15
    assert N_STRATEGIES == 6
    assert N_TARGETS == 8
    import numpy as np
    rng = np.random.default_rng()
    b = Brain(n_hid=64, rng=rng)
    import numpy as np
    x = np.zeros(N_IN)
    act, probs = b.think(x)
    assert 0 <= act < N_OUT
    assert len(probs) == N_OUT
    assert b._strategy in range(N_STRATEGIES)
    assert b._target in range(N_TARGETS)
    b.learn(0.5)
    b2 = b.copy()
    assert b2.n == b.n
    print("OK test_brain_132")


def test_construction_blueprints():
    from game.construction import HouseBlueprint, blueprint_from_name
    for name in ("coffre", "grenier", "atelier", "puits", "small_house", "storage_hut"):
        tasks = blueprint_from_name(name, 10, 10)
        assert len(tasks) > 0, f"blueprint {name} empty"
    print("OK test_construction_blueprints")


def test_headless_2000():
    from game.engine import build_world
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    am = AssetManager(headless=True).discover()
    am.ensure_procedural_blocks()
    am.ensure_procedural_tools()
    am.ensure_kaykit_resources()
    _set_asset_manager(am)
    import os
    from game.config import ASSETS_DIR
    for f in os.listdir(ASSETS_DIR):
        if "vegetable" in f.lower() and f.endswith(".png") and os.path.isfile(os.path.join(ASSETS_DIR, f)):
            p = os.path.join(ASSETS_DIR, f)
            if os.path.getsize(p) > 1000:
                am.register_grid_items(p, category="nourriture", role="food", cell_w=16, cell_h=16, edible=24.0)
                break
    w, sim = build_world(am, seed=42, procedural=True, n_agents=10)
    t0 = time.time()
    for i in range(2000):
        sim.tick()
    elapsed = time.time() - t0
    assert len(sim.agents) > 0, "all agents dead"
    assert not any(np.isnan(a.x) for a in sim.agents), "NaN position"
    print(f"OK test_headless_2000: pop={len(sim.agents)} deaths={sim.stats.get('deaths',0)} {elapsed:.1f}s")


if __name__ == "__main__":
    import numpy as np
    test_brain_132()
    test_construction_blueprints()
    test_headless_2000()
    print("ALL TESTS PASSED")
