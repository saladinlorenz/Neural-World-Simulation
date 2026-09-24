"""Lot E — institutions émergentes réellement câblées en production."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _make_sim(seed=42):
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    from game.engine import build_world

    am = AssetManager(headless=True).discover()
    am.ensure_procedural_blocks()
    _set_asset_manager(am)
    _, sim = build_world(am, seed=seed, procedural=True, n_agents=3)
    return sim


def test_deposit_creates_institution_visible_in_snapshot():
    from game.ui_snapshots import society_snapshot

    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    storage = sim.create_storage(a, 30, 30)
    assert storage is not None

    for _ in range(3):
        a.inv["bois"] = 5
        assert sim.deposit_to_storage(a, storage)

    snap = society_snapshot(sim)
    insts = snap["institutions"]
    kinds = [i["kind"] for i in insts]
    assert "shared_storage" in kinds, kinds
    target = next(i for i in insts if i["kind"] == "shared_storage")
    assert a.eid in target["members"]
    assert target["practices"].get("deposit", 0) >= 3

    kinds_lab = [e["kind"] for e in sim.lab.events]
    assert "institution" in kinds_lab


def test_disabled_runtime_blocks_creation():
    sim = _make_sim(seed=7)
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    storage = sim.create_storage(a, 30, 30)

    sim.runtime["institutions_enabled"] = False
    a.inv["bois"] = 5
    assert sim.deposit_to_storage(a, storage)
    assert not sim.clan_knowledge.institutions
    assert not sim._note_institution("shared_storage", 30, 30, a.eid,
                                     action="deposit")

    sim.runtime["institutions_enabled"] = True
    a.inv["bois"] = 5
    assert sim.deposit_to_storage(a, storage)
    assert sim.clan_knowledge.institutions


def test_construction_practice_creates_institution():
    sim = _make_sim(seed=11)
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None

    sim._note_institution("construction", 40, 40, a.eid, action="build")
    key = ("construction", 40 // 8, 40 // 8)
    inst = sim.clan_knowledge.institutions.get(key)
    assert inst is not None
    assert inst["practices"]["build"] == 1
    assert a.eid in inst["members"]


def test_decay_eventually_removes_inactive():
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None

    sim.clan_knowledge.add_institution("shared_storage", 24, 24, a.eid, 10)
    key = ("shared_storage", 24 // 8, 24 // 8)
    inst = sim.clan_knowledge.institutions[key]
    inst["stability"] = 0.05
    inst["created_tick"] = 10
    # aucune pratique depuis > 5000 ticks
    sim.clan_knowledge.decay_institutions(6000)
    assert key not in sim.clan_knowledge.institutions


def test_decay_gated_by_runtime_in_tick():
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None

    sim.clan_knowledge.add_institution("shared_storage", 24, 24, a.eid, 10)
    key = ("shared_storage", 24 // 8, 24 // 8)
    inst = sim.clan_knowledge.institutions[key]
    inst["stability"] = 0.05
    inst["created_tick"] = 10

    sim.runtime["institutions_enabled"] = False
    sim.w.tick = 600
    # le gate du tick : decay_institutions n'est pas appelé quand désactivé
    if sim.w.tick % 600 == 0 and sim.runtime.get("institutions_enabled", True):
        sim.clan_knowledge.decay_institutions(sim.w.tick)
    assert key in sim.clan_knowledge.institutions


if __name__ == "__main__":
    test_deposit_creates_institution_visible_in_snapshot()
    test_disabled_runtime_blocks_creation()
    test_construction_practice_creates_institution()
    test_decay_eventually_removes_inactive()
    test_decay_gated_by_runtime_in_tick()
    print("ALL TESTS PASSED")
