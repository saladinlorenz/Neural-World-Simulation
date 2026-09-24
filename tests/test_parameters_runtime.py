"""Lot D — paramètres Studio réellement actifs sur le Sim (runtime)."""
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
    _, sim = build_world(am, seed=42, procedural=True, n_agents=3)
    return sim


def test_apply_parameters_writes_all_targets():
    from game.studio_parameters import (
        ParameterStore, apply_parameters, PARAMETER_TARGETS,
    )

    sim = _make_sim()
    store = ParameterStore()
    store.set("simulation.speed", 5)
    store.set("population.max", 123)
    store.set("population.birth_rate", 0.02)
    store.set("ecology.regrowth", 0.05)
    store.set("ecology.fire_spread", 0.2)
    store.set("anima.episodes_max", 64)
    store.set("performance.max_agents", 50)
    store.set("performance.snapshot_freq", 7)
    store.set("world.food", "faible")
    store.set("world.predators", "faible")
    store.set("anima.institutions", "désactivé")

    apply_parameters(sim, store)

    assert sim.speed == 5
    assert sim.runtime["max_population"] == 123
    assert sim.runtime["birth_rate"] == 0.02
    assert sim.runtime["regrowth_scale"] == 0.05
    assert sim.runtime["fire_spread_scale"] == 0.2
    assert sim.runtime["episodes_max"] == 64
    assert sim.runtime["max_agents_rendered"] == 50
    assert sim.runtime["snapshot_frequency"] == 7
    assert sim.runtime["food_level"] == "faible"
    assert sim.runtime["predators_level"] == "faible"
    assert sim.runtime["institutions_enabled"] is False
    # chaque cible du tableau explicite est couverte par le store
    assert set(PARAMETER_TARGETS) <= set(store.to_dict())


def test_food_level_scales_crop_growth():
    from game.studio_parameters import ParameterStore, apply_parameters
    from game.world import CropPlot

    sim = _make_sim()
    w = sim.w
    sim.clock.light = 1.0
    sim.clock.rain = 0.0

    tx = ty = None
    for y in range(2, w.g - 2):
        for x in range(2, w.g - 2):
            if w.land[y, x] and not w.water[y, x] and w.content[y, x] < 0:
                tx, ty = x, y
                break
        if tx is not None:
            break
    assert tx is not None, "aucune tuile seche disponible"

    def _delta(food_level):
        w.crop_plots.clear()
        w.crop_plots[(tx, ty)] = CropPlot(tx=tx, ty=ty, owner_eid=None,
                                          planted_tick=0)
        store = ParameterStore()
        store.set("world.food", food_level)
        apply_parameters(sim, store)
        before = w.crop_plots[(tx, ty)].growth
        sim._grow_crops()
        return w.crop_plots[(tx, ty)].growth - before

    d_low = _delta("faible")
    d_high = _delta("élevé")
    assert d_low > 0 and d_high > 0
    assert abs((d_high / d_low) - 3.0) < 1e-6, (d_low, d_high)


def test_episodes_max_caps_memory():
    from game.studio_parameters import ParameterStore, apply_parameters

    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    for i in range(50):
        a.remember_anima_episode(i, "test_kind", (10, 10),
                                 importance=0.5, cap=32)
    assert len(a.anima["episodic_memory"]) <= 32

    store = ParameterStore()
    store.set("anima.episodes_max", 10)
    apply_parameters(sim, store)
    assert sim.runtime["episodes_max"] == 10
    assert len(a.anima["episodic_memory"]) <= 10


def test_unknown_param_ignored_silently():
    from game.studio_parameters import ParameterStore, apply_parameters

    sim = _make_sim()
    store = ParameterStore()
    store.from_dict({"unknown.parameter": 42, "simulation.speed": 3})
    assert store.get("unknown.parameter") is None
    assert store.get("simulation.speed") == 3

    try:
        store.set("unknown.parameter", 1)
    except KeyError:
        pass
    else:
        raise AssertionError("set() d'un param inconnu devrait lever KeyError")

    values = apply_parameters(sim, store)
    assert sim.speed == 3
    assert "unknown.parameter" not in values


if __name__ == "__main__":
    test_apply_parameters_writes_all_targets()
    test_food_level_scales_crop_growth()
    test_episodes_max_caps_memory()
    test_unknown_param_ignored_silently()
    print("ALL TESTS PASSED")
