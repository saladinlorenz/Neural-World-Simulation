"""Sauvegarde / chargement complet de la simulation.

Sauvegarde : world + sim + agents + cerveaux + camera → data/saves/slot_N.npz
Charge : restaure l'état exact, y compris les poids de neurones.

Politique de validation au chargement (sauvegarde corrompue / NaN-Inf) :
- jamais d'exception pour une valeur non finie : le chargement aboutit ;
- scalaires d'entités (x, y, santé, énergie, ...) : repli sûr si non fini,
  puis bornes appliquées ([0,1] pour les ratios vitaux, [0, GRID*TILE] pour
  les positions) ;
- poids de cerveau : NaN/Inf remplacés par `np.nan_to_num` (les poids sains
  sont conservés, même garde-fou que Brain.learn) ; taille historique
  128 entrées migrée AVANT la construction du Brain ; taille inconnue →
  cerveau régénéré (le chargement ne plante pas) ;
- chaque correction est comptée : compteur module `load_anomalies()`,
  recopié sur `sim.metrics["load_anomalies"]` si ce dictionnaire existe ;
- seule une absence de données exploitables reste fatale : fichier pickle
  illisible → `ValueError("Sauvegarde corrompue : <path>")`."""
import ast
import os
import pickle
import numpy as np

from .config import SAVE_DIR, GRID, TILE, AGE_MAX_NATURAL_DEATH_TICKS

#: Version courante des sauvegardes (Lot Save v3).
SAVE_VERSION = 3


def _slot_path(slot=0):
    os.makedirs(SAVE_DIR, exist_ok=True)
    return os.path.join(SAVE_DIR, f"slot_{slot}.pkl")


# ------------------------------------------------------- validation au chargement
#: Nombre d'anomalies (valeur non finie, poids corrompus, taille inconnue)
#: assainies lors du dernier chargement. Remis à zéro au début de `load_game`
#: puis reporté sur `sim.metrics["load_anomalies"]`.
_LOAD_ANOMALIES = 0

#: Bornes monde (pixels) pour recaler les positions chargées.
_WORLD_MAX_PX = float(GRID * TILE - 1)
_WORLD_CENTER_PX = float(GRID * TILE) / 2.0


def load_anomalies():
    """Nombre d'anomalies assainies lors du dernier `load_game` (0 = sain)."""
    return _LOAD_ANOMALIES


def _reset_anomalies():
    """Remet à zéro le compteur d'anomalies de chargement."""
    global _LOAD_ANOMALIES
    _LOAD_ANOMALIES = 0


def _count_anomaly(name):
    """Compte une anomalie assainie (nom conservé pour diagnostic)."""
    global _LOAD_ANOMALIES
    _LOAD_ANOMALIES += 1
    return name


def _require_finite(value, name, default=None):
    """Vérifie qu'une valeur (scalaire ou tableau) ne contient ni NaN ni Inf.

    Politique : valeur finie → renvoyée telle quelle ; sinon `default` est
    renvoyé si fourni (assainissement silencieux, compté comme anomalie),
    sinon `ValueError` — un repli doit être fourni pour toute donnée de la
    simulation, seuls les fichiers illibles restent fatals.
    """
    try:
        arr = np.asarray(value, dtype=np.float64)
    except (TypeError, ValueError):
        _count_anomaly(name)
        if default is not None:
            return default
        raise ValueError(f"{name} contient des valeurs non finies") from None
    if np.all(np.isfinite(arr)):
        return value
    _count_anomaly(name)
    if default is not None:
        return default
    raise ValueError(f"{name} contient des valeurs non finies")


def _sanitize_finite(value, name, default=None):
    """Assainit un tableau : NaN→0, ±Inf→±1, poids sains inchangés.

    `default` est renvoyé si la conversion échoue (sinon `None`).
    """
    try:
        arr = np.asarray(value, dtype=np.float64)
    except (TypeError, ValueError):
        _count_anomaly(name)
        return default
    if np.all(np.isfinite(arr)):
        return arr
    _count_anomaly(name)
    return np.nan_to_num(arr, nan=0.0, posinf=1.0, neginf=-1.0)


def _finite_scalar(value, name, default, lo=None, hi=None):
    """Assainit un scalaire d'état : non fini → `default`, hors bornes → clamp.

    Toute correction est comptée comme anomalie de chargement.
    """
    try:
        v = float(_require_finite(value, name, default=default))
    except (TypeError, ValueError):
        return float(default)
    if lo is not None and v < lo:
        _count_anomaly(name)
        v = float(lo)
    elif hi is not None and v > hi:
        _count_anomaly(name)
        v = float(hi)
    return v


def _expected_params_size(n_hid, n_in):
    """Taille des poids attendue : Wx(n_in*n)+Wd(n)+b1(n)+Wo(N_OUT*n)+b2."""
    from .brain import N_OUT
    return n_in * n_hid + 2 * n_hid + N_OUT * n_hid + N_OUT


def _prepare_brain_params(raw, n_hid, kind="agent"):
    """Valide et migre les poids de cerveau d'une sauvegarde.

    - NaN/Inf remplacés par `np.nan_to_num` (poids sains conservés) ;
    - taille historique 128 entrées migrée VERS N_IN courant **avant** la
      construction du Brain (unpack() plante sinon sur un vecteur trop court) ;
    - taille non interprétable → `None`, l'appelant régénère un cerveau neuf.

    Retourne le vecteur de poids prêt pour `Brain(params=...)`, ou `None`.
    """
    from . import brain as _brain
    n_in = int(getattr(_brain, "N_IN", 132))
    old_nin = int(getattr(_brain, "OLD_NIN", 128))
    p = _sanitize_finite(raw, f"{kind}.brain_p")
    if p is None:
        return None
    p = np.asarray(p, dtype=np.float64).ravel()
    params_size = getattr(_brain, "params_size", None)
    if callable(params_size):
        expected = int(params_size(n_hid))
    else:
        expected = _expected_params_size(n_hid, n_in)
    if p.size == expected:
        return p
    # ancien format (128 entrées) : migrer AVANT toute construction Brain
    migrate = getattr(_brain, "migrate_input_weights", None)
    if migrate is not None:
        cand, _new_n = migrate(p, old_n=old_nin, new_n=n_in)
        cand = np.asarray(cand, dtype=np.float64).ravel()
        if cand.size == expected:
            return cand
    _count_anomaly(f"{kind}.brain_p (taille {p.size} inattendue)")
    return None


def _fresh_brain(n_hid, eid=0):
    """Cerveau neuf de repli, graine déterministe dérivée de l'eid."""
    from . import brain as _brain
    rng = np.random.default_rng(int(eid) * 7919 + 13)
    return _brain.Brain(n_hid=int(n_hid), rng=rng)


def _publish_load_anomalies(sim):
    """Reporte le compteur d'anomalies sur le Sim chargé (défensif : le
    dictionnaire `metrics` peut être absent ou de type inconnu)."""
    n = _LOAD_ANOMALIES
    if not n:
        return
    try:
        m = getattr(sim, "metrics", None)
        if isinstance(m, dict):
            m["load_anomalies"] = int(m.get("load_anomalies", 0)) + n
        elif m is None:
            sim.metrics = {"load_anomalies": n}
    except (AttributeError, TypeError, ValueError):
        pass


def save_game(sim, cam=None, slot=0, ui_state=None):
    """Sauvegarde complète : monde, simulation, agents, cerveaux, camera."""
    w = sim.w
    data = {
        "version": SAVE_VERSION,
        # --- world arrays ---
        "land": w.land,
        "water": w.water,
        "mountains": w.mountains,
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
        "foundation": w.foundation,
        "roof": w.roof,
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
        "crop_plots": {
            f"{tx},{ty}": {
                "tx": cp.tx, "ty": cp.ty, "owner_eid": cp.owner_eid,
                "planted_tick": cp.planted_tick, "growth": cp.growth,
                "water_need": cp.water_need, "crop_type": cp.crop_type,
                "watered": cp.watered,
            }
            for (tx, ty), cp in w.crop_plots.items()
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
        # graine de la simulation (determinisme + affichage UI) ; absent des
        # sauvegardes antérieures → 0 au rechargement
        "seed": int(getattr(sim, "seed", 0)),
        # --- sim social/commerce ---
        "clan_knowledge": {
            "places": sim.clan_knowledge.places,
            "dangers": sim.clan_knowledge.dangers,
            "reservations": sim.clan_knowledge.reservations,
            "culture": sim.clan_knowledge.culture,
            "institutions": sim.clan_knowledge.institutions,
        },
        "trade": sim._trade,
        "dominance": dict(sim._dominance),
        "village_pts": list(sim._village_pts),
        "recent_attacks": list(sim._recent_attacks),
        "last_war_log": sim._last_war_log,
        # --- Lot Save v3 ---
        "ui_state": ui_state,
        "asset_catalog_fingerprint": sim.am.catalog_fingerprint(),
        "districts": {k: d.to_dict()
                      for k, d in getattr(sim, "districts", {}).items()},
        "predator_zones": {k: z.to_dict()
                           for k, z in getattr(sim, "predator_zones", {}).items()},        # --- universal knowledge ---
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
        "social_memory": {
            f"{obs},{tgt}": {
                "trust": r.trust, "violence": r.violence,
                "theft": r.theft, "generosity": r.generosity,
                "last_tick": r.last_tick,
            }
            for (obs, tgt), r in sim.social_memory.records.items()
        },
    }
    if w.gen is not None:
        data["gen_height_base"] = w.gen.height_base
        data["gen_height_current"] = w.gen.height_current
        data["gen_biome"] = w.gen.biome
        data["gen_shade"] = w.gen.shade
        data["gen_carved"] = w.gen.carved
        data["gen_moisture"] = w.gen.moisture
        data["gen_g"] = w.gen.g
        # métadonnées worldgen — sans elles, le WorldGen rechargé repart avec
        # des valeurs par défaut (seed/période) incohérentes avec le terrain
        data["gen_seed"] = int(w.gen.seed)
        data["gen_tile_period"] = int(w.gen.tile_period)
        data["gen_ridge_width"] = int(w.gen.ridge_width)
        data["gen_version"] = int(w.gen.version)
    # --- camera ---
    if cam is not None:
        data["cam_x"] = cam.x
        data["cam_y"] = cam.y
        data["cam_zoom"] = cam.zoom
        data["cam_tilt"] = cam.tilt

    path = _slot_path(slot)
    tmp = path + ".tmp"
    try:
        with open(tmp, "wb") as f:
            pickle.dump(data, f, protocol=5)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except Exception:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise
    size_mb = os.path.getsize(path) / (1024 * 1024)
    return path, size_mb


def load_game(am, slot=0):
    """Charge une sauvegarde. Retourne (sim, cam) ou (None, None) si pas trouvé."""
    path = _slot_path(slot)
    if not os.path.exists(path):
        return None, None
    _reset_anomalies()
    try:
        with open(path, "rb") as f:
            data = pickle.load(f)
    except (EOFError, pickle.UnpicklingError, AttributeError) as e:
        raise ValueError(f"Sauvegarde corrompue : {path}") from e
    if not isinstance(data, dict):
        raise ValueError(f"Sauvegarde corrompue : {path}")

    ver = data.get("version", 1)
    if ver > SAVE_VERSION:
        raise ValueError(
            f"Sauvegarde version {ver} incompatible "
            f"(version supportée : {SAVE_VERSION}). "
            "Mettez à jour le logiciel."
        )

    from .world import World
    from .simulation import Sim
    from .camera import Camera

    # --- reconstruire world ---
    w = World()
    g = data.get("g", GRID)
    w.g = g
    w.land = data["land"]
    w.water = data["water"]
    w.mountains = data.get("mountains", w.blocked.copy())
    w.foundation = data.get("foundation", np.zeros_like(w.blocked))
    w.roof = data.get("roof", np.zeros_like(w.blocked))
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
    w.crop_plots = {}
    from .world import CropPlot
    for raw_cp in data.get("crop_plots", {}).values():
        cp = CropPlot(
            tx=raw_cp["tx"], ty=raw_cp["ty"],
            owner_eid=raw_cp.get("owner_eid"),
            planted_tick=int(raw_cp.get("planted_tick", 0)),
            growth=float(raw_cp.get("growth", 0.0)),
            water_need=float(raw_cp.get("water_need", 0.5)),
            crop_type=raw_cp.get("crop_type", "grain"),
        )
        cp.watered = raw_cp.get("watered", False)
        w.crop_plots[(cp.tx, cp.ty)] = cp
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
            tile_period=int(data.get("gen_tile_period", 250)),
            ridge_width=int(data.get("gen_ridge_width", 55)),
            seed=int(data.get("gen_seed", 42)),
            version=int(data.get("gen_version", 0)),
        )
    else:
        w.gen = None

    # --- reconstruire sim ---
    sim = Sim(w, am, seed=int(data.get("seed", 0)))
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
        sim.clan_knowledge.culture = {_parse_key(k): v for k, v in ck.get("culture", {}).items()}
        sim.clan_knowledge.institutions = {_parse_key(k): v for k, v in ck.get("institutions", {}).items()}
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
    # social memory
    from .social_memory import SocialRecord
    sim.social_memory.records = {}
    for key, raw in data.get("social_memory", {}).items():
        observer, target = map(int, key.split(","))
        sim.social_memory.records[(observer, target)] = SocialRecord(**raw)

    # --- Lot Save v3 : zones + empreinte catalogue + état UI ---
    from .zones import District, PredatorZone
    sim.districts = {
        k: District.from_dict(v)
        for k, v in data.get("districts", {}).items()
    }
    sim.predator_zones = {
        k: PredatorZone.from_dict(v)
        for k, v in data.get("predator_zones", {}).items()
    }
    sim.loaded_catalog_fingerprint = data.get("asset_catalog_fingerprint")
    sim.loaded_ui_state = data.get("ui_state")

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

    # --- anomalies de chargement assainies (valeurs non finies, poids) ---
    _publish_load_anomalies(sim)

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
        # brain tete strategie + cible (Lot 7.2)
        "brain_Wo_strat": a.brain._Wo_strat.copy(),
        "brain_b2_strat": a.brain._b2_strat.copy(),
        "brain_Wo_targ": a.brain._Wo_targ.copy(),
        "brain_b2_targ": a.brain._b2_targ.copy(),
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
        # Anima Phase 1+
        "anima": {
            "episodic_memory": list(a.anima["episodic_memory"]),
            "beliefs": {
                "places": {f"{k[0]}|{k[1]}": v
                           for k, v in a.anima["beliefs"]["places"].items()},
                "beings": {str(k): v
                           for k, v in a.anima["beliefs"]["beings"].items()},
            },
            "identity": dict(a.anima["identity"]),
            "values": dict(a.anima["values"]),
            "trauma": dict(a.anima["trauma"]),
            "attachments": {str(k): v
                            for k, v in a.anima.get("attachments", {}).items()},
            "intention": a.anima.get("intention"),
            "plan": a.anima.get("plan"),
            "reputation": dict(a.anima.get("reputation", {})),
            "causal_traces": list(a.anima.get("causal_traces", [])),
            "observations": list(a.anima.get("observations", [])),
        },
    }


def _deserialize_agent(d):
    from collections import deque as _dq
    from . import brain as _brain
    n_hid = int(d["brain_n"])
    # --- cerveau : validation + migration 128→132 AVANT construction ------
    # (unpack() plante sur un vecteur 128 entrées : la migration doit donc
    # précéder Brain(...) ; aucune réaffectation de brain.p ensuite, donc
    # les vues _Wx/_Wo issues du constructeur restent cohérentes)
    brain_p = _prepare_brain_params(d["brain_p"], n_hid, kind="agent")
    if brain_p is None:
        brain = _fresh_brain(n_hid, d["eid"])
    else:
        try:
            brain = _brain.Brain(n_hid=n_hid, params=brain_p)
        except (ValueError, TypeError):
            _count_anomaly("agent.brain_p")
            brain = _fresh_brain(n_hid, d["eid"])
    brain.h = _sanitize_finite(d["brain_h"], "agent.brain_h", brain.h)
    brain.last_out = _sanitize_finite(d["brain_last_out"], "agent.brain_last_out",
                                      brain.last_out)
    brain.probs = _sanitize_finite(d["brain_probs"], "agent.brain_probs", brain.probs)
    brain.base = _finite_scalar(d["brain_base"], "agent.brain_base", 0.0)
    if d.get("brain_rng") is not None:
        brain.rng.bit_generator.state = d["brain_rng"]
    if d.get("brain_trace"):
        brain._trace = _dq(d["brain_trace"], maxlen=brain._trace.maxlen)
    # tete strategie + cible (fallback: aleatoire pour anciens saves)
    if d.get("brain_Wo_strat") is not None:
        brain._Wo_strat = _sanitize_finite(d["brain_Wo_strat"], "agent.brain_Wo_strat",
                                           brain._Wo_strat)
        brain._b2_strat = _sanitize_finite(d["brain_b2_strat"], "agent.brain_b2_strat",
                                           brain._b2_strat)
        brain._Wo_targ = _sanitize_finite(d["brain_Wo_targ"], "agent.brain_Wo_targ",
                                          brain._Wo_targ)
        brain._b2_targ = _sanitize_finite(d["brain_b2_targ"], "agent.brain_b2_targ",
                                          brain._b2_targ)

    # --- positions : repli au centre du monde puis bornes [0, GRID*TILE] ---
    x = _finite_scalar(d["x"], "agent.x", _WORLD_CENTER_PX, 0.0, _WORLD_MAX_PX)
    y = _finite_scalar(d["y"], "agent.y", _WORLD_CENTER_PX, 0.0, _WORLD_MAX_PX)
    a = Being(
        eid=d["eid"], x=x, y=y, color=d["color"], cls=d["cls"],
        states={}, gen=d["gen"], brain=brain, parents=d.get("parents", ()),
        personality=_sanitize_finite(d["personality"], "agent.personality"),
        rng=None, born_tick=d["born_tick"],
        n_hid=n_hid, body=_sanitize_finite(d["body"], "agent.body"),
        cog=_sanitize_finite(d["cog"], "agent.cog"),
        emotions=_sanitize_finite(d["emotions"], "agent.emotions"),
        needs=_sanitize_finite(d["needs"], "agent.needs"), sex=d["sex"],
    )
    a.name = d["name"]
    a.age = d["age"]
    a.natural_death_age = d.get("natural_death_age", AGE_MAX_NATURAL_DEATH_TICKS)
    a.vx = _finite_scalar(d["vx"], "agent.vx", 0.0)
    a.vy = _finite_scalar(d["vy"], "agent.vy", 0.0)
    a.fx = int(_finite_scalar(d["fx"], "agent.fx", 0))
    a.fy = int(_finite_scalar(d["fy"], "agent.fy", 0))
    # --- état vital : repli sûr puis bornes [0, 1] ---
    a.health = _finite_scalar(d["health"], "agent.health", 1.0, 0.0, 1.0)
    a.pain = _finite_scalar(d["pain"], "agent.pain", 0.0, 0.0, 1.0)
    a.temp = _finite_scalar(d["temp"], "agent.temp", 0.5, 0.0, 1.0)
    a.energy = _finite_scalar(d["energy"], "agent.energy", 0.5, 0.0, 1.0)
    a.hunger = _finite_scalar(d["hunger"], "agent.hunger", 0.0, 0.0, 1.0)
    a.tool = d["tool"]; a.inv = d["inv"]
    a.tool_durability = d.get("tool_durability", 0)
    a.skills = _sanitize_finite(d["skills"], "agent.skills", np.zeros(4))
    a.habits = _sanitize_finite(d["habits"], "agent.habits", np.full(15, 0.06))
    a.self_esteem = _finite_scalar(d["self_esteem"], "agent.self_esteem", 0.5, 0.0, 1.0)
    a.rep = _finite_scalar(d["rep"], "agent.rep", 0.0)
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
    # Anima Phase 1
    ad = d.get("anima")
    if ad:
        from .studio_parameters import DEFAULT_RUNTIME
        ep_cap = max(1, int(DEFAULT_RUNTIME.get("episodes_max", 32)))
        a.anima["episodic_memory"] = _dq(
            list(ad.get("episodic_memory", []))[-ep_cap:], maxlen=200)
        places_raw = ad.get("beliefs", {}).get("places", {})
        a.anima["beliefs"]["places"] = {
            (int(k.split("|")[0]), int(k.split("|")[1])): v
            for k, v in places_raw.items()
        }
        beings_raw = ad.get("beliefs", {}).get("beings", {})
        loaded_beings = {}
        for k, v in beings_raw.items():
            eid = int(k)
            if isinstance(v, dict):
                loaded_beings[eid] = v
            else:
                loaded_beings[eid] = {
                    "trust": 0.5, "danger": 0.0, "generosity": 0.5,
                    "reliability": 0.5, "confidence": 0.0,
                    "last_update": 0,
                }
        a.anima["beliefs"]["beings"] = loaded_beings
        for k in ("identity", "values", "trauma"):
            if k in ad:
                a.anima[k].update(ad[k])
        att_raw = ad.get("attachments", {})
        loaded_att = {}
        for k, v in att_raw.items():
            try:
                loaded_att[int(k)] = v
            except (ValueError, TypeError):
                loaded_att[k] = v
        a.anima["attachments"] = loaded_att
        # Lot D/F/H : champs nouveaux
        if ad.get("intention") is not None:
            a.anima["intention"] = ad["intention"]
        a.anima["plan"] = ad.get("plan")
        a.anima["reputation"] = dict(ad.get("reputation", {}))
        a.anima["causal_traces"] = list(ad.get("causal_traces", []))
        from collections import deque as _dq2
        a.anima["observations"] = _dq2(ad.get("observations", []), maxlen=24)
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
    from . import brain as _brain
    n_hid = int(d["brain_n"])
    # même politique que les agents : validation + migration 128→132 AVANT
    # la construction du Brain (sinon unpack() plante sur l'ancien format)
    brain_p = _prepare_brain_params(d["brain_p"], n_hid, kind="sheep")
    if brain_p is None:
        brain = _fresh_brain(n_hid, d["eid"])
    else:
        try:
            brain = _brain.Brain(n_hid=n_hid, params=brain_p)
        except (ValueError, TypeError):
            _count_anomaly("sheep.brain_p")
            brain = _fresh_brain(n_hid, d["eid"])
    brain.h = _sanitize_finite(d["brain_h"], "sheep.brain_h", brain.h)
    x = _finite_scalar(d["x"], "sheep.x", _WORLD_CENTER_PX, 0.0, _WORLD_MAX_PX)
    y = _finite_scalar(d["y"], "sheep.y", _WORLD_CENTER_PX, 0.0, _WORLD_MAX_PX)
    s = Sheep(d["eid"], x, y, brain=brain)
    s.vx = _finite_scalar(d["vx"], "sheep.vx", 0.0)
    s.vy = _finite_scalar(d["vy"], "sheep.vy", 0.0)
    s.energy = _finite_scalar(d["energy"], "sheep.energy", 0.6, 0.0, 1.0)
    s.health = _finite_scalar(d["health"], "sheep.health", 1.0, 0.0, 1.0)
    s.state = d["state"]; s.alive = d["alive"]
    s.fear = _finite_scalar(d.get("fear", 0.0), "sheep.fear", 0.0, 0.0, 1.0)
    return s


def _serialize_monster(m):
    return {
        "eid": m.eid, "x": m.x, "y": m.y,
        "vx": m.vx, "vy": m.vy,
        "energy": m.energy, "health": m.health,
        "kind": m.kind, "alive": m.alive,
        "zone_id": getattr(m, "zone_id", None),
    }


def _deserialize_monster(d):
    x = _finite_scalar(d["x"], "monster.x", _WORLD_CENTER_PX, 0.0, _WORLD_MAX_PX)
    y = _finite_scalar(d["y"], "monster.y", _WORLD_CENTER_PX, 0.0, _WORLD_MAX_PX)
    m = Monster(d["eid"], x, y, kind=d["kind"])
    m.vx = _finite_scalar(d["vx"], "monster.vx", 0.0)
    m.vy = _finite_scalar(d["vy"], "monster.vy", 0.0)
    m.energy = _finite_scalar(d["energy"], "monster.energy", 0.8, 0.0, 1.0)
    m.health = _finite_scalar(d["health"], "monster.health", 1.0, 0.0, 1.0)
    m.alive = d["alive"]
    m.zone_id = d.get("zone_id")
    return m


# --- import circular ---
from .entities import Being, Sheep, Monster
