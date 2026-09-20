"""Sauvegarde / chargement complet de la simulation.

Sauvegarde : world + sim + agents + cerveaux + camera → data/saves/slot_N.npz
Charge : restaure l'état exact, y compris les poids de neurones."""
import ast
import os
import pickle
import numpy as np

from .config import SAVE_DIR, GRID, TILE, AGE_MAX_NATURAL_DEATH_TICKS


def _slot_path(slot=0):
    os.makedirs(SAVE_DIR, exist_ok=True)
    return os.path.join(SAVE_DIR, f"slot_{slot}.pkl")


def save_game(sim, cam=None, slot=0):
    """Sauvegarde complète : monde, simulation, agents, cerveaux, camera."""
    w = sim.w
    data = {
        # --- world arrays ---
        "land": w.land,
        "water": w.water,
        "floor": w.floor,
        "content": w.content,
        "owner": w.owner,
        "blocked": w.blocked,
        "shelter": w.shelter,
        "hp": w.hp,
        "marker": w.marker,
        "marker_col": w.marker_col,
        "regrow": w.regrow,
        "fire": w.fire,
        "smell": w.smell,
        "heat": w.heat,
        "cemetery": list(w.cemetery),
        "sites": {
            f"{tx},{ty}": {
                "origin_tx": s.origin_tx,
                "origin_ty": s.origin_ty,
                "blueprint_name": s.blueprint_name,
                "tasks": [{"tx": t.tx, "ty": t.ty, "material": t.material,
                           "phase": t.phase, "layer": t.layer, "solid": t.solid}
                          for t in s.tasks],
                "placed": list(s.placed),
                "contributors": dict(s.contributors),
                "created_tick": s.created_tick,
                "owner_eid": s.owner_eid,
                "owner_clan": s.owner_clan,
            }
            for (tx, ty), s in w.sites.items()
        },
        "storages": {
            f"{tx},{ty}": {
                "tx": st.tx, "ty": st.ty, "capacity": st.capacity,
                "owner_clan": st.owner_clan,
                "inventory": dict(st.inventory),
                "contributors": dict(st.contributors),
                "withdrawals": dict(st.withdrawals),
                "last_access_tick": st.last_access_tick,
            }
            for (tx, ty), st in w.storages.items()
        },
        "items": [(it.x, it.y, it.aid, it.kind, it.life) for it in w.items],
        "w_tick": w.tick,
        "g": w.g,
        # --- worldgen ---
        "has_gen": w.gen is not None,
        # --- sim state ---
        "next_eid": sim.next_eid,
        "paused": sim.paused,
        "speed": sim.speed,
        "stats": dict(sim.stats),
        "journal": list(sim.journal)[-40:],
        "society": sim.society[:],
        "pop_hist": list(sim.pop_hist)[-60:],
        "clock_light": sim.clock.light,
        "clock_rain": sim.clock.rain,
        "clock_season": sim.clock.season,
        "clock_day": sim.clock.day,
        "clock_year": sim.clock.year,
        "clock_t": sim.clock.t,
        "clock_temp": sim.clock.temp,
        "clock_wind": sim.clock.wind,
        "clock_growth_f": sim.clock.growth_f,
        "clock_storm": sim.clock._storm,
        "rng_state": sim.rng.bit_generator.state,
        # --- sim social/commerce ---
        "clan_knowledge": {
            "places": sim.clan_knowledge.places,
            "dangers": sim.clan_knowledge.dangers,
            "reservations": sim.clan_knowledge.reservations,
        },
        "trade": sim._trade,
        "dominance": dict(sim._dominance),
        "village_pts": list(sim._village_pts),
        "recent_attacks": list(sim._recent_attacks),
        "last_war_log": sim._last_war_log,
        # --- universal knowledge ---
        "universal_knowledge": sim.universal_knowledge.to_dict(),
        # --- academy ---
        "academy": {
            "params": sim.academy.champion_params,
            "size": sim.academy.champion_size,
            "score": sim.academy.champion_score,
            "label": sim.academy.champion_label,
        },
        # --- lab ---
        "lab_daily": list(sim.lab.daily[-5000:]),
        # --- agents ---
        "n_agents": len(sim.agents),
        "agents": [_serialize_agent(a) for a in sim.agents],
        # --- sheep ---
        "n_sheep": len(sim.sheep),
        "sheep": [_serialize_sheep(s) for s in sim.sheep],
        # --- monsters ---
        "n_monsters": len(sim.monsters),
        "monsters": [_serialize_monster(m) for m in sim.monsters],
    }
    if w.gen is not None:
        data["gen_height_base"] = w.gen.height_base
        data["gen_height_current"] = w.gen.height_current
        data["gen_biome"] = w.gen.biome
        data["gen_shade"] = w.gen.shade
        data["gen_carved"] = w.gen.carved
        data["gen_moisture"] = w.gen.moisture
        data["gen_g"] = w.gen.g
    # --- camera ---
    if cam is not None:
        data["cam_x"] = cam.x
        data["cam_y"] = cam.y
        data["cam_zoom"] = cam.zoom
        data["cam_tilt"] = cam.tilt

    path = _slot_path(slot)
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        pickle.dump(data, f, protocol=5)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)
    size_mb = os.path.getsize(path) / (1024 * 1024)
    return path, size_mb


def load_game(am, slot=0):
    """Charge une sauvegarde. Retourne (sim, cam) ou (None, None) si pas trouvé."""
    path = _slot_path(slot)
    if not os.path.exists(path):
        return None, None
    with open(path, "rb") as f:
        data = pickle.load(f)

    from .world import World
    from .simulation import Sim
    from .camera import Camera

    # --- reconstruire world ---
    w = World()
    g = data.get("g", GRID)
    w.g = g
    w.land = data["land"]
    w.water = data["water"]
    w.floor = data["floor"]
    w.content = data["content"]
    w.owner = data["owner"]
    w.blocked = data["blocked"]
    w.shelter = data["shelter"]
    w.hp = data["hp"]
    w.marker = data["marker"]
    w.marker_col = data["marker_col"]
    w.regrow = data["regrow"]
    w.fire = data["fire"]
    w.smell = data["smell"]
    w.heat = data["heat"]
    w.cemetery = data.get("cemetery", [])
    w.sites = {}
    from .construction import ConstructionSite, BlockTask
    for raw in data.get("sites", {}).values():
        tasks = [BlockTask(tx=t["tx"], ty=t["ty"], material=t["material"],
                           phase=t["phase"], layer=t.get("layer", 0),
                           solid=t.get("solid", True))
                 for t in raw.get("tasks", [])]
        site = ConstructionSite(
            origin_tx=raw["origin_tx"],
            origin_ty=raw["origin_ty"],
            blueprint_name=raw.get("blueprint_name", "small_house"),
            tasks=tasks,
            placed={tuple(p) for p in raw.get("placed", [])},
            contributors={int(k): int(v) for k, v in raw.get("contributors", {}).items()},
            created_tick=int(raw.get("created_tick", 0)),
            owner_eid=raw.get("owner_eid"),
            owner_clan=raw.get("owner_clan"),
        )
        w.sites[site.key] = site
    w.storages = {}
    from .storage import SharedStorage
    for raw_s in data.get("storages", {}).values():
        st = SharedStorage(
            tx=raw_s["tx"], ty=raw_s["ty"], capacity=raw_s.get("capacity", 80),
            owner_clan=raw_s.get("owner_clan"),
            inventory=raw_s.get("inventory", {}),
            contributors={int(k): int(v) for k, v in raw_s.get("contributors", {}).items()},
            withdrawals={int(k): int(v) for k, v in raw_s.get("withdrawals", {}).items()},
            last_access_tick=int(raw_s.get("last_access_tick", 0)),
        )
        w.storages[st.tx, st.ty] = st
    w.tick = data["w_tick"]
    w.items = []
    for (ix, iy, iaid, ikind, ilife) in data.get("items", []):
        from .world import Item
        w.items.append(Item(ikind, iaid, ix, iy, life=ilife))

    # --- worldgen ---
    if data.get("has_gen", False):
        from .worldgen import WorldGen
        w.gen = WorldGen(
            g=data["gen_g"],
            height_base=data["gen_height_base"],
            height_current=data["gen_height_current"],
            biome=data["gen_biome"],
            shade=data["gen_shade"],
            carved=data["gen_carved"],
            moisture=data["gen_moisture"],
        )
    else:
        w.gen = None

    # --- reconstruire sim ---
    sim = Sim(w, am, seed=0)
    sim.next_eid = data["next_eid"]
    sim.paused = data["paused"]
    sim.speed = data["speed"]
    sim.stats = data["stats"]
    sim.journal = data["journal"]
    sim.society = data.get("society", [])
    sim.pop_hist = data.get("pop_hist", [])
    # clock
    sim.clock.light = data.get("clock_light", 0.5)
    sim.clock.rain = data.get("clock_rain", 0.0)
    sim.clock.season = data.get("clock_season", 0)
    sim.clock.day = data.get("clock_day", 0)
    sim.clock.year = data.get("clock_year", 1)
    sim.clock.t = data.get("clock_t", 0)
    sim.clock.temp = data.get("clock_temp", 0.6)
    sim.clock.wind = data.get("clock_wind", (0.0, 0.0))
    sim.clock.growth_f = data.get("clock_growth_f", 1.0)
    sim.clock._storm = data.get("clock_storm", 0)
    # rng
    if "rng_state" in data:
        sim.rng.bit_generator.state = data["rng_state"]
    # clan knowledge (compatible versions anciennes)
    ck = data.get("clan_knowledge")
    if ck:
        def _parse_key(k):
            return ast.literal_eval(k) if isinstance(k, str) else k
        sim.clan_knowledge.places = {_parse_key(k): v for k, v in ck.get("places", {}).items()}
        sim.clan_knowledge.dangers = {_parse_key(k): v for k, v in ck.get("dangers", {}).items()}
        sim.clan_knowledge.reservations = {_parse_key(k): v for k, v in ck.get("reservations", {}).items()}
    # social / commerce
    sim._trade = {ast.literal_eval(k) if isinstance(k, str) else k: v for k, v in data.get("trade", {}).items()}
    sim._dominance = data.get("dominance", {})
    sim._village_pts = [tuple(p) for p in data.get("village_pts", [])]
    from collections import deque as _dq
    sim._recent_attacks = _dq(data.get("recent_attacks", []), maxlen=400)
    sim._last_war_log = data.get("last_war_log", -9999)
    # universal knowledge (compatible anciennes saves)
    from .universal_knowledge import UniversalKnowledge
    sim.universal_knowledge = UniversalKnowledge.from_dict(
        data.get("universal_knowledge", {})
    )
    # academy
    acad = data.get("academy", {})
    sim.academy.champion_params = acad.get("params")
    sim.academy.champion_size = acad.get("size")
    sim.academy.champion_score = acad.get("score", float("-inf"))
    sim.academy.champion_label = acad.get("label", "aucun")
    # lab
    sim.lab.daily = list(data.get("lab_daily", []))

    # --- agents ---
    sim.agents = []
    for ad in data.get("agents", []):
        sim.agents.append(_deserialize_agent(ad))
    # --- sheep ---
    sim.sheep = []
    for sd in data.get("sheep", []):
        sim.sheep.append(_deserialize_sheep(sd))
    # --- monsters ---
    sim.monsters = []
    for md in data.get("monsters", []):
        sim.monsters.append(_deserialize_monster(md))

    # --- rebuild spatial hash (grid_bucket + _entity_cells) ---
    sim.grid_bucket = {}
    sim._entity_cells = {}
    for a in sim.agents:
        cx, cy = int(a.x // 32), int(a.y // 32)
        sim.grid_bucket.setdefault((cx, cy), []).append(a)
        sim._entity_cells[a.eid] = (cx, cy)
    for s in sim.sheep:
        cx, cy = int(s.x // 32), int(s.y // 32)
        sim.grid_bucket.setdefault((cx, cy), []).append(s)
        sim._entity_cells[s.eid] = (cx, cy)
    for m in sim.monsters:
        cx, cy = int(m.x // 32), int(m.y // 32)
        sim.grid_bucket.setdefault((cx, cy), []).append(m)
        sim._entity_cells[m.eid] = (cx, cy)

    # --- camera ---
    cam = Camera()
    if "cam_zoom" in data:
        cam.x = data.get("cam_x", 0)
        cam.y = data.get("cam_y", 0)
        cam.zoom = data.get("cam_zoom", 0.25)
        cam.tilt = data.get("cam_tilt", 55.0)
        cam.clamp()
    else:
        ys, xs = np.nonzero(w.land)
        if len(xs):
            cam.center_on(float(xs.mean()) * TILE, float(ys.mean()) * TILE)

    return sim, cam


# ------------------------------------------------------------------ serialisation
def _serialize_agent(a):
    return {
        "eid": a.eid, "name": a.name, "gen": a.gen, "color": a.color,
        "cls": a.cls,         "sex": a.sex, "age": a.age, "natural_death_age": a.natural_death_age,
        "born_tick": a.born_tick,
        "x": a.x, "y": a.y, "vx": a.vx, "vy": a.vy,
        "fx": a.fx, "fy": a.fy, "health": a.health, "pain": a.pain,
        "temp": a.temp, "energy": a.energy, "hunger": a.hunger,
        "tool": a.tool, "tool_durability": getattr(a, "tool_durability", 0),
        "inv": dict(a.inv),
        "body": a.body.copy(), "cog": a.cog.copy(),
        "emotions": a.emotions.copy(), "needs": a.needs.copy(),
        "personality": a.personality.copy(),
        "skills": a.skills.copy(), "habits": a.habits.copy(),
        "self_esteem": a.self_esteem, "rep": a.rep,
        "state": a.state, "alive": a.alive,
        "avatar": a.avatar, "col_idx": a.col_idx,
        "commitment": a.commitment, "stuck": a.stuck,
        "failed_targets": {f"{k[0]}|{k[1]}|{k[2]}": list(v) for k, v in a.failed_targets.items()},
        "mood_phase": a.mood_phase, "mood_freq": a.mood_freq,
        "home": a.home, "work_t": a.work_t, "atk_t": a.atk_t,
        "repro_cd": a.repro_cd,
        "goal": a.goal, "goal_t": a.goal_t,
        "bonded": a.bonded, "hated": a.hated,
        "married": a.married, "partner_id": a.partner_id,
        "parent_pere_id": a.parent_pere_id, "parent_mere_id": a.parent_mere_id,
        "parents": a.parents, "children": a.children,
        # brain
        "brain_n": a.brain.n, "brain_p": a.brain.p.copy(),
        "brain_h": a.brain.h.copy(),
        "brain_last_out": a.brain.last_out.copy(),
        "brain_probs": a.brain.probs.copy(),
        "brain_base": a.brain.base,
        "brain_rng": a.brain.rng.bit_generator.state if hasattr(a.brain, 'rng') else None,
        "brain_trace": list(a.brain._trace),
        # memory
        "seen": {k: list(v) for k, v in a.seen.items()},
        "belief_places": dict(a.belief_places),
        "belief_beings": dict(a.belief_beings),
        "rel": dict(a.rel),
        "dangers": list(a.dangers),
        "affinity_cd": a.affinity_cd,
        # episodic / autobiographique
        "life": list(a.life),
        "episodes": list(a.episodes),
        "talk_cd": dict(a.talk_cd),
    }


def _deserialize_agent(d):
    from collections import deque as _dq
    from .brain import Brain
    brain = Brain(n_hid=d["brain_n"], params=d["brain_p"])
    brain.h = d["brain_h"]
    brain.last_out = d["brain_last_out"]
    brain.probs = d["brain_probs"]
    brain.base = d["brain_base"]
    if d.get("brain_rng") is not None:
        brain.rng.bit_generator.state = d["brain_rng"]
    if d.get("brain_trace"):
        brain._trace = _dq(d["brain_trace"], maxlen=brain._trace.maxlen)

    a = Being(
        eid=d["eid"], x=d["x"], y=d["y"], color=d["color"], cls=d["cls"],
        states={}, gen=d["gen"], brain=brain, parents=d.get("parents", ()),
        personality=d["personality"], rng=None, born_tick=d["born_tick"],
        n_hid=d["brain_n"], body=d["body"], cog=d["cog"],
        emotions=d["emotions"], needs=d["needs"], sex=d["sex"],
    )
    a.name = d["name"]
    a.age = d["age"]
    a.natural_death_age = d.get("natural_death_age", AGE_MAX_NATURAL_DEATH_TICKS)
    a.vx = d["vx"]; a.vy = d["vy"]
    a.fx = d["fx"]; a.fy = d["fy"]
    a.health = d["health"]; a.pain = d["pain"]; a.temp = d["temp"]
    a.energy = d["energy"]; a.hunger = d["hunger"]
    a.tool = d["tool"]; a.inv = d["inv"]
    a.tool_durability = d.get("tool_durability", 0)
    a.skills = d["skills"]; a.habits = d["habits"]
    a.self_esteem = d["self_esteem"]; a.rep = d["rep"]
    a.state = d["state"]; a.alive = d["alive"]
    a.avatar = d["avatar"]; a.col_idx = d["col_idx"]
    a.commitment = d["commitment"]; a.stuck = d["stuck"]
    ft_raw = d.get("failed_targets", {})
    a.failed_targets = {(k.split("|")[0], int(k.split("|")[1]), int(k.split("|")[2])): tuple(v)
                        for k, v in ft_raw.items()}
    a.mood_phase = d["mood_phase"]; a.mood_freq = d["mood_freq"]
    a.home = d["home"]; a.work_t = d["work_t"]; a.atk_t = d["atk_t"]
    a.repro_cd = d["repro_cd"]
    a.goal = d["goal"]; a.goal_t = d["goal_t"]
    a.bonded = d.get("bonded"); a.hated = d.get("hated")
    a.married = d.get("married", False); a.partner_id = d.get("partner_id")
    a.parent_pere_id = d.get("parent_pere_id"); a.parent_mere_id = d.get("parent_mere_id")
    a.children = d.get("children", [])
    a.seen = d.get("seen", {c: [] for c in ("food","wood","stone","water","shelter","agent")})
    a.belief_places = d.get("belief_places", {})
    a.belief_beings = d.get("belief_beings", {})
    a.rel = d.get("rel", {})
    a.dangers = d.get("dangers", [])
    a.affinity_cd = d.get("affinity_cd", 0)
    # episodique / autobiographique
    a.life = _dq(d.get("life", []), maxlen=48)
    a.episodes = _dq(d.get("episodes", []), maxlen=64)
    a.talk_cd = d.get("talk_cd", {})
    return a


def _serialize_sheep(s):
    return {
        "eid": s.eid, "x": s.x, "y": s.y,
        "vx": s.vx, "vy": s.vy,
        "energy": s.energy, "health": s.health,
        "state": s.state, "alive": s.alive,
        "fear": s.fear,
        "brain_n": s.brain.n, "brain_p": s.brain.p.copy(),
        "brain_h": s.brain.h.copy(),
    }


def _deserialize_sheep(d):
    from .brain import Brain
    brain = Brain(n_hid=d["brain_n"], params=d["brain_p"])
    brain.h = d["brain_h"]
    s = Sheep(d["eid"], d["x"], d["y"], brain=brain)
    s.vx = d["vx"]; s.vy = d["vy"]
    s.energy = d["energy"]; s.health = d["health"]
    s.state = d["state"]; s.alive = d["alive"]
    s.fear = d.get("fear", 0.0)
    return s


def _serialize_monster(m):
    return {
        "eid": m.eid, "x": m.x, "y": m.y,
        "vx": m.vx, "vy": m.vy,
        "energy": m.energy, "health": m.health,
        "kind": m.kind, "alive": m.alive,
    }


def _deserialize_monster(d):
    m = Monster(d["eid"], d["x"], d["y"], kind=d["kind"])
    m.vx = d["vx"]; m.vy = d["vy"]
    m.energy = d["energy"]; m.health = d["health"]
    m.alive = d["alive"]
    return m


# --- import circular ---
from .entities import Being, Sheep, Monster
