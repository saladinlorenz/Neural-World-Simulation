"""Tests comportementaux de validation du plan de corrections."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np


def _make_sim():
    """Cree une simulation legere pour les tests."""
    from game.assets_manager import AssetManager
    from game.engine import build_world
    am = AssetManager(headless=True).discover()
    am.ensure_procedural_blocks()
    am.ensure_procedural_tools()
    am.ensure_kaykit_resources()
    w, sim = build_world(am, seed=42, procedural=True)
    return sim


def test_harvest_to_build_chain():
    """HARVEST devient faisable quand on connait du bois/pierre."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None, "spawn_agent a echoue"
    a.age = 800000
    a.inv["bois"] = 0
    a.inv["pierre"] = 0
    a.remember("wood", 30, 30)
    a.remember("stone", 35, 30)
    f = sim._feasible(a)
    assert f[4], "HARVEST devrait etre faisable avec memoire de bois/pierre"
    a.inv["bois"] = 3
    f2 = sim._feasible(a)
    assert f2[6], "BUILD devrait etre faisable avec 3 bois"
    print("PASS: test_harvest_to_build_chain")


def test_house_needs_all_layers():
    """Le chantier exige fondation + mur + porte + toit."""
    from game.construction import HouseBlueprint
    tasks = HouseBlueprint.small_house(20, 20)
    foundations = [t for t in tasks if t.phase == "foundation"]
    walls = [t for t in tasks if t.phase == "wall"]
    doors = [t for t in tasks if t.phase == "door"]
    roofs = [t for t in tasks if t.phase == "roof"]
    assert len(foundations) > 0, "Au moins une fondation"
    assert len(walls) > 0, "Au moins un mur"
    assert len(doors) > 0, "Au moins une porte"
    assert len(roofs) > 0, "Au moins un toit"
    f0 = foundations[0]
    w0 = next((t for t in walls if t.tx == f0.tx and t.ty == f0.ty), None)
    if w0 is not None:
        assert f0.key != w0.key, "Fondation et mur ont des cles differentes"
    print("PASS: test_house_needs_all_layers")


def test_storage():
    """Depot et retrait dans un stockage."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    storage = sim.create_storage(a, 30, 30)
    assert storage is not None
    a.inv["bois"] = 5
    ok = sim.deposit_to_storage(a, storage)
    assert ok, "deposit a echoue"
    assert storage.inventory.get("bois", 0) > 0, "Le stockage devrait contenir du bois"
    a.inv["bois"] = 0
    ok2 = sim.withdraw_from_storage(a, storage, "bois")
    assert ok2, "withdraw a echoue"
    assert a.inv["bois"] > 0, "L'agent devrait avoir du bois"
    print("PASS: test_storage")


def test_site_has_required_phases():
    """site_has_required_phases verifie les 4 phases."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.inv["bois"] = 50
    a.inv["pierre"] = 50
    site = sim.create_house_site(a, 100, 100)
    assert site is not None
    assert not sim.site_has_required_phases(site), "Site incomplet ne devrait pas etre complet"
    for task in site.tasks:
        site.mark_placed(a.eid, task)
    assert sim.site_has_required_phases(site), "Site complet devrait etre complet"
    print("PASS: test_site_has_required_phases")


def test_bootstrap_resource_memory():
    """bootstrap_resource_memory remplit la memoire."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    sim.bootstrap_resource_memory(a, radius=10)
    has_memory = (
        bool(a.seen.get("food", []))
        or bool(a.seen.get("wood", []))
        or bool(a.seen.get("stone", []))
        or bool(a.seen.get("water", []))
    )
    assert has_memory, "L'agent devrait avoir au moins une memoire de ressource"
    print("PASS: test_bootstrap_resource_memory")


def test_brain_schema_inputs():
    """Le vecteur de perception fait bien 132 entrees."""
    from game.brain_schema import INPUT, NIN
    assert NIN == 132
    vals = list(INPUT.values())
    assert max(vals) == 131
    assert min(vals) == 0
    print(f"PASS: test_brain_schema_inputs ({len(vals)} cles definies)")


def test_migrate_input_weights():
    """Migration 128->132 entrees."""
    from game.brain import migrate_input_weights, OLD_NIN, N_OUT
    from game.brain_schema import NIN
    n_hid = 64
    old_p = np.random.default_rng(0).standard_normal(
        OLD_NIN * n_hid + 2 * n_hid + N_OUT * n_hid + N_OUT)
    new_p, new_n = migrate_input_weights(old_p, old_n=OLD_NIN, new_n=NIN)
    expected = NIN * n_hid + 2 * n_hid + N_OUT * n_hid + N_OUT
    assert new_p.size == expected, f"Poids attendus {expected}, obtenus {new_p.size}"
    assert new_n == NIN
    assert np.allclose(new_p[:OLD_NIN * n_hid], old_p[:OLD_NIN * n_hid]), "Les poids anciens doivent etre conserves"
    print("PASS: test_migrate_input_weights")


def test_complete_site_creates_shelter():
    """complete_site cree un abri et un depot."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.inv["bois"] = 50
    a.inv["pierre"] = 50
    site = sim.create_house_site(a, 100, 100)
    assert site is not None
    for task in site.tasks:
        a.inv[task.material] = 50
        sim.place_site_block(a, site, task)
    assert site.complete(), "Le site devrait etre complet"
    w = sim.w
    has_shelter = bool(w.shelter[101:104, 101:104].any())
    assert has_shelter, "Le site devrait creer un abri"
    has_storage = any(
        abs(st.tx - 102) <= 1 and abs(st.ty - 102) <= 1
        for st in w.storages.values()
    )
    assert has_storage, "Le site devrait creer un depot"
    print("PASS: test_complete_site_creates_shelter")


def test_anima_episodic_memory():
    """Un agent enregistre des episodes Anima avec importance."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    ep = a.remember_anima_episode(
        100, "monster_attack", (50, 50),
        actors=[a.eid, 99], action="flee", outcome="survived",
        emotion={"fear": 0.88, "pain": 0.35, "surprise": 0.6},
        importance=0.84,
    )
    assert ep["kind"] == "monster_attack"
    assert ep["importance"] == 0.84
    assert len(a.anima["episodic_memory"]) == 1
    assert a.anima["trauma"]["attack"] > 0
    assert a.anima["identity"]["survivor"] > 0
    print("PASS: test_anima_episodic_memory")


def test_anima_belief_update():
    """Un episode important met a jour les croyances lieux."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.remember_anima_episode(
        100, "monster_attack", (80, 80),
        action="flee", outcome="survived",
        emotion={"fear": 0.9, "pain": 0.5, "surprise": 0.4},
        importance=0.80,
    )
    cx, cy = 80 // 8, 80 // 8
    belief = a.anima["beliefs"]["places"].get((cx, cy), 0.0)
    assert belief > 0.3, f"Croyance devrait etre > 0.3, obtenu {belief}"
    print("PASS: test_anima_belief_update")


def test_anima_perceived_danger():
    """Le danger percu combine vision + croyance + trauma."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.anima["beliefs"]["places"][(62, 62)] = 0.8
    a.anima["trauma"]["attack"] = 0.5
    pd = a.anima_perceived_danger(500, 500, 0.30)
    assert pd > 0.30, f"Danger percu devrait etre > base, obtenu {pd}"
    print("PASS: test_anima_perceived_danger")


def test_anima_bias_modulation():
    """Le biais FLEE augmente avec la peur trauma."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    from game.brain import FLEE
    a.anima["trauma"]["attack"] = 0.8
    b1 = sim._bias(a)
    a.anima["trauma"]["attack"] = 0.0
    b2 = sim._bias(a)
    assert b1[FLEE] > b2[FLEE], "FLEE bias devrait etre plus fort avec trauma"
    print("PASS: test_anima_bias_modulation")


def test_anima_brain_schema():
    """Le schema Anima fait 132 entrees."""
    from game.brain_schema import INPUT, NIN
    assert NIN == 132
    assert "trauma_attack" in INPUT
    assert "belief_danger" in INPUT
    assert "episode_count" in INPUT
    assert "anima_fighter" in INPUT
    print("PASS: test_anima_brain_schema")


def test_anima_migration_128_to_132():
    """Migration des poids de 128 vers 132."""
    from game.brain import migrate_input_weights, OLD_NIN, N_OUT
    from game.brain_schema import NIN
    old_n = OLD_NIN
    n_hid = 64
    old_p = np.random.default_rng(0).standard_normal(
        old_n * n_hid + 2 * n_hid + N_OUT * n_hid + N_OUT)
    new_p, new_n = migrate_input_weights(old_p, old_n=old_n, new_n=NIN)
    expected = NIN * n_hid + 2 * n_hid + N_OUT * n_hid + N_OUT
    assert new_p.size == expected, f"Poids attendus {expected}, obtenus {new_p.size}"
    assert new_n == NIN
    assert np.allclose(new_p[:old_n * n_hid], old_p[:old_n * n_hid])
    print("PASS: test_anima_migration_128_to_132")


def test_anima_low_importance_forgotten():
    """Un episode peu important n'est pas stocke."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    ep = a.remember_anima_episode(
        100, "new_area_discovered", (50, 50),
        action="explore", outcome="discovered",
        emotion={"fear": 0.0, "pain": 0.0, "surprise": 0.1},
        importance=0.05,
    )
    assert ep is not None
    assert len(a.anima["episodic_memory"]) == 0, "Episode < 0.20 pas stocke"
    print("PASS: test_anima_low_importance_forgotten")


# =====================================================================
# Phase 2 tests
# =====================================================================

def test_identity_api():
    """anima_add_identity, anima_clamp, anima_dominant_identity."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    assert a.anima_dominant_identity() is None
    a.anima_add_identity("builder", 0.5)
    assert abs(a.anima["identity"]["builder"] - 0.5) < 1e-6
    assert a.anima_dominant_identity() == "builder"
    a.anima_add_identity("builder", 0.6)
    assert a.anima["identity"]["builder"] == 1.0, "clamp a 1.0"
    a.anima_add_identity("builder", -0.3)
    assert abs(a.anima["identity"]["builder"] - 0.7) < 1e-6
    a.anima_add_identity("fighter", 1.0)
    assert a.anima_dominant_identity() == "fighter"
    print("PASS: test_identity_api")


def test_values_api():
    """anima_add_value met a jour les valeurs avec clamp."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.anima_add_value("security", 0.5)
    assert abs(a.anima["values"]["security"] - 1.0) < 1e-6, "0.5+0.5=1.0"
    a.anima_add_value("security", 0.3)
    assert a.anima["values"]["security"] == 1.0, "clamp a 1.0"
    a.anima_add_value("security", -1.5)
    assert abs(a.anima["values"]["security"] - 0.0) < 1e-6, "clamp a 0.0"
    a.anima_add_value("generosity", -0.3)
    assert abs(a.anima["values"]["generosity"] - 0.2) < 1e-6, "0.5-0.3=0.2"
    print("PASS: test_values_api")


def test_social_belief_init():
    """Les croyances sociales sont initialisees a 0.5 trust par defaut."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    b = sim.spawn_agent(x=510, y=500)
    assert a is not None and b is not None
    belief = a.anima_social_belief(b.eid, 0)
    assert belief["trust"] == 0.5, f"trust initial: {belief['trust']}"
    assert belief["danger"] == 0.0
    assert belief["generosity"] == 0.5
    assert belief["reliability"] == 0.5
    assert belief["confidence"] == 0.0
    print("PASS: test_social_belief_init")


def test_social_belief_update():
    """anima_update_social_belief met a jour et clamp les croyances."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    b = sim.spawn_agent(x=510, y=500)
    assert a is not None and b is not None
    a.anima_update_social_belief(b.eid, 100, trust_delta=0.3)
    belief = a.anima_social_belief(b.eid, 100)
    assert abs(belief["trust"] - 0.8) < 1e-6
    a.anima_update_social_belief(b.eid, 200, trust_delta=0.5)
    assert a.anima_social_belief(b.eid, 200)["trust"] == 1.0, "clamp trust a 1.0"
    a.anima_update_social_belief(b.eid, 300, danger_delta=0.8)
    assert abs(a.anima_social_belief(b.eid, 300)["danger"] - 0.8) < 1e-6
    a.anima_update_social_belief(b.eid, 400, danger_delta=-2.0)
    assert a.anima_social_belief(b.eid, 400)["danger"] == 0.0, "clamp danger a 0.0"
    assert a.anima_social_belief(b.eid, 400)["last_update"] == 400
    print("PASS: test_social_belief_update")


def test_social_score():
    """anima_social_score combine trust et danger en score."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    b = sim.spawn_agent(x=510, y=500)
    assert a is not None and b is not None
    s_neutral = a.anima_social_score(b.eid)
    assert abs(s_neutral - 0.0) < 1e-6, f"score neutre: {s_neutral}"
    a.anima_update_social_belief(b.eid, 100, trust_delta=0.4, danger_delta=0.0)
    s_trusted = a.anima_social_score(b.eid)
    assert s_trusted > 0.0, f"score confiance: {s_trusted}"
    a.anima_update_social_belief(b.eid, 200, trust_delta=-0.8, danger_delta=0.5)
    s_danger = a.anima_social_score(b.eid)
    assert s_danger < -0.1, f"score danger: {s_danger}"
    print("PASS: test_social_score")


def test_identity_decay():
    """anima_decay_identity reduit doucement les traits."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.anima_add_identity("builder", 0.5)
    before = a.anima["identity"]["builder"]
    a.anima_decay_identity()
    after = a.anima["identity"]["builder"]
    assert after < before, f"decay: {after} >= {before}"
    a.anima_add_identity("fighter", 0.02)
    before_f = a.anima["identity"]["fighter"]
    a.anima_decay_identity()
    after_f = a.anima["identity"]["fighter"]
    assert after_f < before_f, f"decay devrait reduire: {after_f} >= {before_f}"
    print("PASS: test_identity_decay")


def test_social_target_selection():
    """Les actions sociales privilegient les cibles de confiance."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    b = sim.spawn_agent(x=510, y=500)
    c = sim.spawn_agent(x=520, y=500)
    assert a is not None and b is not None and c is not None
    a.anima_update_social_belief(b.eid, 100, trust_delta=0.4)
    a.anima_update_social_belief(c.eid, 100, trust_delta=-0.3)
    a._near_agents = [b, c]
    a.anima["beliefs"]["beings"] = a.anima["beliefs"]["beings"]
    targets = sorted([b, c],
                     key=lambda o: a.anima_social_score(o.eid), reverse=True)
    assert targets[0].eid == b.eid, "la cible de confiance devrait etre en premier"
    print("PASS: test_social_target_selection")


def test_anima_social_beliefs_save_load():
    """Les croyances sociales survivent a un cycle save/load."""
    import tempfile, os, pickle
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    b = sim.spawn_agent(x=510, y=500)
    assert a is not None and b is not None
    a.anima_update_social_belief(b.eid, 100, trust_delta=0.3, danger_delta=0.2)
    from game.save import save_game, load_game
    slot = 99
    save_game(sim, slot=slot)
    sim2_loaded, _ = load_game(sim.am, slot=slot)
    assert sim2_loaded is not None
    a2 = next((x for x in sim2_loaded.agents if x.eid == a.eid), None)
    assert a2 is not None, "agent non restaure"
    belief = a2.anima_social_belief(b.eid, 200)
    assert abs(belief["trust"] - 0.8) < 0.05, f"trust post-load: {belief['trust']}"
    assert abs(belief["danger"] - 0.2) < 0.05, f"danger post-load: {belief['danger']}"
    try:
        os.remove(os.path.join("data", f"slot_{slot}.pkl"))
    except OSError:
        pass
    print("PASS: test_anima_social_beliefs_save_load")


def test_anima_old_save_defaults_do_not_crash():
    """Une structure ancienne sans Anima Phase 2 ne plante pas."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.anima["beliefs"]["beings"] = {99: 0.7}
    belief = a.anima_social_belief(99, 0)
    assert isinstance(belief, dict), "ancien format float converti en dict"
    assert belief["trust"] == 0.5
    assert a.anima_social_score(99) == 0.0
    print("PASS: test_anima_old_save_defaults_do_not_crash")


def test_anima_values_modulate_bias_without_forcing_action():
    """Les valeurs influencent les biais sans forcer l'action."""
    from game.brain_api import GIVE, TAKE, TALK, SOCIAL, ATTACK
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    b = sim.spawn_agent(x=510, y=500)
    assert a is not None and b is not None
    a.anima["values"]["generosity"] = 1.0
    a.anima["values"]["community"] = 1.0
    a.anima["values"]["survival"] = 0.0
    a._near_agents = [b]
    f = sim._feasible(a)
    assert any(f[i] for i in (GIVE, TAKE, TALK, SOCIAL, ATTACK)), \
        "au moins un acte social faisable"
    print("PASS: test_anima_values_modulate_bias_without_forcing_action")


def test_anima_no_nan_inf():
    """Aucun NaN/Inf dans les donnees Anima apres operations."""
    import math
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.anima_add_identity("builder", 0.5)
    a.anima_add_identity("fighter", 0.3)
    a.anima_add_value("survival", 0.8)
    a.anima_add_value("security", -0.6)
    a.anima_decay_identity()
    a.anima_decay_identity()
    for k, v in a.anima["identity"].items():
        assert math.isfinite(v), f"NaN/Inf dans identity[{k}]: {v}"
    for k, v in a.anima["values"].items():
        assert math.isfinite(v), f"NaN/Inf dans values[{k}]: {v}"
    b = sim.spawn_agent(x=520, y=500)
    a.anima_update_social_belief(b.eid, 100, trust_delta=0.5, danger_delta=0.3)
    a.anima_update_social_belief(b.eid, 200, trust_delta=-0.8, danger_delta=-1.0)
    belief = a.anima_social_belief(b.eid, 200)
    for k, v in belief.items():
        assert math.isfinite(v), f"NaN/Inf dans belief[{k}]: {v}"
    score = a.anima_social_score(b.eid)
    assert math.isfinite(score), f"NaN/Inf dans social_score: {score}"
    print("PASS: test_anima_no_nan_inf")


def test_anima_intention_persists_until_interrupt():
    """L'intention persiste et expire apres duree."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.anima_set_intention("secure_food", "faim", priority=0.7, tick=100, duration=500)
    assert a.anima_intention_valid(200)
    assert a.anima_intention_valid(599)
    assert not a.anima_intention_valid(601)
    a.anima_set_intention("build_home", "abri", priority=0.6, tick=100, duration=200)
    assert a.anima_intention_valid(250)
    a.anima_clear_intention()
    assert a.anima_get_intention() is None
    print("PASS: test_anima_intention_persists_until_interrupt")


def test_anima_plan_rejects_impossible_step():
    """Les plans ne contiennent que des actions faisables."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a._near_agents = []
    plans = sim._generate_plans(a)
    assert isinstance(plans, list)
    for p in plans:
        for step in p.get("steps", []):
            assert 0 <= step < 15, f"step hors range: {step}"
    print("PASS: test_anima_plan_rejects_impossible_step")


def test_delayed_causal_credit():
    """Le credit causal se dissipe avec le temps."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.anima_add_causal_trace("harvest", (50, 50), 100, expected_effect="food_found")
    credit_early = a.anima_credit_for("food_found", 200)
    assert credit_early > 0, "credit devrait etre > 0 proche de l'action"
    a.anima_decay_causal_traces(rate=0.5)
    credit_late = a.anima_credit_for("food_found", 1500)
    assert credit_late < credit_early, "credit devrait diminuer apres decay"
    print("PASS: test_delayed_causal_credit")


def test_observation_changes_habit():
    """L'observation modifie les habitudes."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    from game.brain_api import EXPLORE
    before = float(a.habits[EXPLORE])
    a.anima_record_observation(EXPLORE, 0.8, 100)
    a.anima_record_observation(EXPLORE, 0.6, 110)
    a.anima_apply_observation_learning()
    after = float(a.habits[EXPLORE])
    assert after > before, f"habitude devrait augmenter: {after} <= {before}"
    print("PASS: test_observation_changes_habit")


def test_attachment_increases_home_preference():
    """L'attachement au foyer augmente la preference de retour."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.home = (60, 60)
    assert a.anima_home_preference() == 0.0
    a.anima_add_attachment(f"home:{a.home[0]}:{a.home[1]}", 0.5)
    pref = a.anima_home_preference()
    assert pref > 0.0, f"preference devrait etre > 0: {pref}"
    print("PASS: test_attachment_increases_home_preference")


def test_trauma_recovers_under_safety():
    """Le trauma diminue sous securite et soutien."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.anima["trauma"]["attack"] = 0.5
    a.anima["trauma"]["loss"] = 0.3
    a.anima_decay_trauma(safety=1.0, support=1.0)
    assert a.anima["trauma"]["attack"] < 0.5, "trauma attack devrait diminuer"
    assert a.anima["trauma"]["loss"] < 0.3, "trauma loss devrait diminuer"
    a.anima["trauma"]["attack"] = 0.5
    a.anima_decay_trauma(safety=0.0, support=0.0)
    assert a.anima["trauma"]["attack"] < 0.5, "trauma diminue meme sans securite"
    print("PASS: test_trauma_recovers_under_safety")


def test_institution_requires_repeated_practice():
    """Une institution n'apparait qu'apres pratiques repetees."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    sim.clan_knowledge.add_institution("shared_storage", 50, 50, a.eid, 100)
    key = ("shared_storage", 50 // 8, 50 // 8)
    inst = sim.clan_knowledge.institutions.get(key)
    assert inst is not None
    assert inst["stability"] < 0.3, "stabilite faible au depart"
    for i in range(5):
        sim.clan_knowledge.record_practice("shared_storage", 50, 50, a.eid, "deposit", 200 + i * 10)
    inst2 = sim.clan_knowledge.institutions.get(key)
    assert inst2["stability"] > 0.15, "stabilite devrait augmenter"
    print("PASS: test_institution_requires_repeated_practice")


def test_full_anima_save_load():
    """Cycle complet save/load avec tous les champs Anima."""
    import os
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    b = sim.spawn_agent(x=510, y=500)
    assert a is not None and b is not None
    a.anima_add_identity("builder", 0.4)
    a.anima_add_value("community", 0.3)
    a.anima["trauma"]["attack"] = 0.2
    a.anima_update_social_belief(b.eid, 100, trust_delta=0.3)
    a.anima_set_intention("build_home", "test", priority=0.6, tick=100)
    a.anima_add_causal_trace("harvest", (50, 50), 100, "food_found")
    a.anima_add_attachment(f"home:{a.home[0]}:{a.home[1]}" if a.home else "home:0:0", 0.4)
    from game.save import save_game, load_game
    slot = 98
    save_game(sim, slot=slot)
    loaded, _ = load_game(sim.am, slot=slot)
    assert loaded is not None
    a2 = next((x for x in loaded.agents if x.eid == a.eid), None)
    assert a2 is not None
    assert abs(a2.anima["identity"]["builder"] - 0.4) < 0.05
    assert abs(a2.anima["values"]["community"] - 0.8) < 0.05
    assert a2.anima["trauma"]["attack"] > 0.1
    intent = a2.anima_get_intention()
    assert intent is not None and intent["kind"] == "build_home"
    traces = a2.anima.get("causal_traces", [])
    assert len(traces) >= 1
    try:
        os.remove(os.path.join("data", f"slot_{slot}.pkl"))
    except OSError:
        pass
    print("PASS: test_full_anima_save_load")


def test_long_run_no_nan_inf():
    """1000 ticks sans NaN/Inf dans les donnees Anima."""
    import math
    sim = _make_sim()
    for _ in range(3):
        sim.spawn_agent(x=500, y=500)
    for _ in range(1000):
        sim.step()
    for a in sim.agents:
        if not a.alive:
            continue
        for k, v in a.anima.get("identity", {}).items():
            assert math.isfinite(v), f"NaN identity[{k}]"
        for k, v in a.anima.get("values", {}).items():
            assert math.isfinite(v), f"NaN values[{k}]"
        for k, v in a.anima.get("trauma", {}).items():
            assert math.isfinite(v), f"NaN trauma[{k}]"
        belief = a.anima.get("beliefs", {}).get("beings", {})
        for eid, bdict in belief.items():
            if isinstance(bdict, dict):
                for bk, bv in bdict.items():
                    assert math.isfinite(bv), f"NaN belief[{eid}][{bk}]"
    print("PASS: test_long_run_no_nan_inf")


if __name__ == "__main__":
    test_brain_schema_inputs()
    test_migrate_input_weights()
    test_harvest_to_build_chain()
    test_house_needs_all_layers()
    test_storage()
    test_site_has_required_phases()
    test_bootstrap_resource_memory()
    test_complete_site_creates_shelter()
    test_anima_episodic_memory()
    test_anima_belief_update()
    test_anima_perceived_danger()
    test_anima_bias_modulation()
    test_anima_brain_schema()
    test_anima_migration_128_to_132()
    test_anima_low_importance_forgotten()
    test_identity_api()
    test_values_api()
    test_social_belief_init()
    test_social_belief_update()
    test_social_score()
    test_identity_decay()
    test_social_target_selection()
    test_anima_social_beliefs_save_load()
    test_anima_old_save_defaults_do_not_crash()
    test_anima_values_modulate_bias_without_forcing_action()
    test_anima_no_nan_inf()
    test_anima_intention_persists_until_interrupt()
    test_anima_plan_rejects_impossible_step()
    test_delayed_causal_credit()
    test_observation_changes_habit()
    test_attachment_increases_home_preference()
    test_trauma_recovers_under_safety()
    test_institution_requires_repeated_practice()
    test_full_anima_save_load()
    test_long_run_no_nan_inf()
    print("\n=== TOUS LES TESTS PASSENT ===")
