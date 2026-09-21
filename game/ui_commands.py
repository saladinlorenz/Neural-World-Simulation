"""UI Commands — commandes neutres validatees par le moteur.

Chaque commande est un dict avec au minimum ``kind``. Le moteur valide
les parametres, effectue l'action, et retourne un resultat dict.

Aucune dependance Pygame ni Qt.
"""
from __future__ import annotations

from typing import Any


def execute_command(sim, command: dict) -> dict[str, Any]:
    """Execute une commande sur la simulation et retourne le resultat.

    Format de retour :
        {"ok": True, ...}  en cas de succes
        {"ok": False, "error": "message"} en cas d'erreur
    """
    kind = command.get("kind", "")

    handler = _HANDLERS.get(kind)
    if handler is None:
        return {"ok": False, "error": f"Commande inconnue: {kind}"}

    try:
        return handler(sim, command)
    except Exception as exc:
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}


# ══════════════════════════════════════════════════════════════════════
#  Controle de simulation
# ══════════════════════════════════════════════════════════════════════
def _cmd_pause_toggle(sim, cmd):
    sim.paused = not sim.paused
    return {"ok": True, "paused": bool(sim.paused)}


def _cmd_set_paused(sim, cmd):
    sim.paused = bool(cmd.get("paused", True))
    return {"ok": True, "paused": bool(sim.paused)}


def _cmd_set_speed(sim, cmd):
    speed = max(1, min(8, int(cmd.get("speed", 1))))
    sim.speed = speed
    return {"ok": True, "speed": speed}


def _cmd_speed_delta(sim, cmd):
    delta = int(cmd.get("delta", 1))
    sim.speed = max(1, min(8, sim.speed + delta))
    return {"ok": True, "speed": int(sim.speed)}


def _cmd_step(sim, cmd):
    sim.tick()
    return {"ok": True, "tick": int(sim.w.tick)}


# ══════════════════════════════════════════════════════════════════════
#  Selection
# ══════════════════════════════════════════════════════════════════════
def _cmd_select_agent(sim, cmd):
    eid = cmd.get("eid")
    if eid is not None:
        eid = int(eid)
        agent = next((a for a in sim.agents if a.eid == eid and a.alive), None)
        if agent is None:
            return {"ok": False, "error": "Habitant introuvable ou mort"}
        sim.selected = agent
        return {"ok": True, "eid": eid, "nom": agent.name}
    sim.selected = None
    return {"ok": True, "eid": None}


def _cmd_select_tile(sim, cmd):
    tx = int(cmd.get("tx", 0))
    ty = int(cmd.get("ty", 0))
    w = sim.w
    if not (0 <= tx < w.g and 0 <= ty < w.g):
        return {"ok": False, "error": "Coordonnees hors monde"}
    return {"ok": True, "tx": tx, "ty": ty}


# ══════════════════════════════════════════════════════════════════════
#  Spawns
# ══════════════════════════════════════════════════════════════════════
def _cmd_spawn_agent(sim, cmd):
    x = cmd.get("x")
    y = cmd.get("y")
    kwargs = {}
    for key in ("color", "cls", "sex", "n_hid", "gen", "energy"):
        if key in cmd:
            kwargs[key] = cmd[key]
    if x is not None:
        kwargs["x"] = float(x)
    if y is not None:
        kwargs["y"] = float(y)
    created = sim.spawn_agent(**kwargs)
    if created is None:
        return {"ok": False, "error": "Impossible de creer l'habitant (place ou limite)"}
    sim.selected = created
    return {"ok": True, "eid": int(created.eid), "nom": created.name}


def _cmd_spawn_sheep(sim, cmd):
    x = cmd.get("x")
    y = cmd.get("y")
    kwargs = {}
    if x is not None:
        kwargs["x"] = float(x)
    if y is not None:
        kwargs["y"] = float(y)
    sim.spawn_sheep(**kwargs)
    return {"ok": True}


def _cmd_spawn_monster(sim, cmd):
    x = cmd.get("x")
    y = cmd.get("y")
    kwargs = {}
    if x is not None:
        kwargs["x"] = float(x)
    if y is not None:
        kwargs["y"] = float(y)
    if "kind" in cmd:
        kwargs["kind"] = cmd["kind"]
    sim.spawn_monster(**kwargs)
    return {"ok": True}


def _cmd_remove_agent(sim, cmd):
    eid = cmd.get("eid")
    if eid is None:
        return {"ok": False, "error": "eid manquant"}
    agent = next((a for a in sim.agents if a.eid == int(eid) and a.alive), None)
    if agent is None:
        return {"ok": False, "error": "Habitant introuvable ou mort"}
    name = cmd.get("name", "le gardien")
    sim.remove_agent(agent, name)
    return {"ok": True}


def _cmd_set_agent_stat(sim, cmd):
    eid = cmd.get("eid")
    stat = cmd.get("stat")
    value = float(cmd.get("value", 0))
    if eid is None or stat is None:
        return {"ok": False, "error": "eid ou stat manquant"}
    agent = next((a for a in sim.agents if a.eid == int(eid) and a.alive), None)
    if agent is None:
        return {"ok": False, "error": "Habitant introuvable ou mort"}
    if hasattr(agent, stat):
        setattr(agent, stat, max(0.0, min(1.0, value)))
        return {"ok": True}
    return {"ok": False, "error": f"Stat inconnue: {stat}"}


# ══════════════════════════════════════════════════════════════════════
#  Outils monde (paint / place / erase / carve / restore)
# ══════════════════════════════════════════════════════════════════════
def _cmd_paint_tile(sim, cmd):
    """Peint un mode sur une zone de tuiles (water, land, wall, floor)."""
    tx = int(cmd.get("tx", 0))
    ty = int(cmd.get("ty", 0))
    mode = cmd.get("mode", "land")
    radius = max(1, min(15, int(cmd.get("radius", 1))))
    w = sim.w

    changed = False
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if dx * dx + dy * dy > radius * radius + 1:
                continue
            cx, cy = tx + dx, ty + dy
            if not (0 <= cx < w.g and 0 <= cy < w.g):
                continue

            if mode == "water":
                if w.land[cy, cx]:
                    w.remove(cx, cy, quiet=True)
                    w.land[cy, cx] = 0
                    w.water[cy, cx] = 1
                    w.blocked[cy, cx] = 0
                    w.floor[cy, cx] = -1
                    w.mark_dirty(cx, cy, 2)
                    changed = True
            elif mode == "land":
                if not w.land[cy, cx] or w.blocked[cy, cx]:
                    w.land[cy, cx] = 1
                    w.water[cy, cx] = 0
                    w.blocked[cy, cx] = 0
                    w.floor[cy, cx] = -1
                    w.mark_dirty(cx, cy, 2)
                    changed = True
            elif mode == "wall":
                if w.land[cy, cx] and not w.blocked[cy, cx] and w.content_at(cx, cy) < 0:
                    stones = sim.am.pool("stone_res") or sim.am.pool("gold_stone")
                    if stones:
                        aid = int(sim.am.pick(stones, sim.rng))
                        w.place(cx, cy, aid, sim.am, hp=8, solid=True,
                                size=sim.am.assets[aid].size_tiles)
                        changed = True
    return {"ok": changed}


def _cmd_place_asset(sim, cmd):
    """Pose un asset sur une tuile."""
    tx = int(cmd.get("tx", 0))
    ty = int(cmd.get("ty", 0))
    aid = int(cmd.get("aid", -1))
    w = sim.w

    if not (0 <= aid < len(sim.am.assets)):
        return {"ok": False, "error": "Asset invalide"}
    adef = sim.am.assets[aid]
    if not getattr(adef, "placable", False):
        return {"ok": False, "error": "Asset non placable"}
    if not w.land[ty, tx] or w.blocked[ty, tx] or w.content_at(tx, ty) >= 0:
        return {"ok": False, "error": "Case occupee ou incompatible"}
    w.place(tx, ty, aid, sim.am, hp=max(1, getattr(adef, "hp", 1)),
            solid=bool(adef.solid), shelter=bool(adef.shelter),
            size=adef.size_tiles if adef.solid else 1)
    return {"ok": True}


def _cmd_erase_tile(sim, cmd):
    """Efface un objet sur une tuile."""
    tx = int(cmd.get("tx", 0))
    ty = int(cmd.get("ty", 0))
    w = sim.w
    if not (0 <= tx < w.g and 0 <= ty < w.g):
        return {"ok": False, "error": "Coordonnees hors monde"}
    removed = w.remove(tx, ty)
    old_len = len(w.items)
    w.items = [it for it in w.items
               if not (int(it.x // 32) == tx and int(it.y // 32) == ty)]
    had_floor = w.floor[ty, tx] >= 0
    w.floor[ty, tx] = -1
    w.mark_dirty(tx, ty)
    return {"ok": removed or len(w.items) != old_len or had_floor}


def _cmd_set_floor(sim, cmd):
    """Definit le sol d'une tuile."""
    tx = int(cmd.get("tx", 0))
    ty = int(cmd.get("ty", 0))
    aid = int(cmd.get("aid", 0))
    w = sim.w
    if not (0 <= tx < w.g and 0 <= ty < w.g):
        return {"ok": False, "error": "Coordonnees hors monde"}
    if aid in sim.am.floors:
        sheet_idx = sim.am.floors.index(aid)
        w.set_floor(tx, ty, sheet_idx * 216)
    elif sim.am.floors:
        w.set_floor(tx, ty, 0)
    else:
        return {"ok": False, "error": "Pas de tileset de sol"}
    return {"ok": True}


def _cmd_carve(sim, cmd):
    """Sculpte une montagne."""
    tx = int(cmd.get("tx", 0))
    ty = int(cmd.get("ty", 0))
    radius = max(1, min(15, int(cmd.get("radius", 3))))
    w = sim.w
    gen = getattr(w, "gen", None)
    if gen is None:
        return {"ok": False, "error": "Pas de heightmap (monde plat)"}
    from game import worldgen as _wg
    changed = _wg.carve_mountain(w, gen, tx, ty, radius=radius, strength=0.12)
    return {"ok": bool(changed)}


def _cmd_restore(sim, cmd):
    """Restaure une montagne sculptee."""
    tx = int(cmd.get("tx", 0))
    ty = int(cmd.get("ty", 0))
    radius = max(1, min(15, int(cmd.get("radius", 3))))
    w = sim.w
    gen = getattr(w, "gen", None)
    if gen is None:
        return {"ok": False, "error": "Pas de heightmap (monde plat)"}
    from game import worldgen as _wg
    changed = _wg.restore_mountain(w, gen, tx, ty, radius=radius, strength=0.18)
    return {"ok": bool(changed)}


def _cmd_build_block(sim, cmd):
    """Construit un bloc."""
    tx = int(cmd.get("tx", 0))
    ty = int(cmd.get("ty", 0))
    material = cmd.get("material", "bois")
    return {"ok": bool(sim.do_build_block_player(tx, ty, material=material))}


# ══════════════════════════════════════════════════════════════════════
#  Journal
# ══════════════════════════════════════════════════════════════════════
def _cmd_log(sim, cmd):
    """Ajoute une entree au journal."""
    text = str(cmd.get("text", ""))
    color = cmd.get("color", (180, 180, 180))
    cat = cmd.get("cat", "monde")
    sim.log(text, color, cat)
    return {"ok": True}


# ══════════════════════════════════════════════════════════════════════
#  Sauvegarde / chargement
# ══════════════════════════════════════════════════════════════════════
def _cmd_save(sim, cmd):
    from .save import save_game
    slot = int(cmd.get("slot", 0))
    cam = cmd.get("cam")
    path, sz = save_game(sim, cam, slot=slot)
    return {"ok": True, "path": str(path), "size_mb": round(sz, 1)}


def _cmd_load(sim, cmd):
    from .save import load_game
    from .assets_manager import AssetManager
    slot = int(cmd.get("slot", 0))
    am = getattr(sim, "am", None)
    if am is None:
        return {"ok": False, "error": "AssetManager indisponible"}
    new_sim, new_cam = load_game(am, slot=slot)
    if new_sim is None:
        return {"ok": False, "error": "Aucune sauvegarde trouvee"}
    return {"ok": True, "sim": new_sim, "cam": new_cam}


# ══════════════════════════════════════════════════════════════════════
#  Registre des handlers
# ══════════════════════════════════════════════════════════════════════
_HANDLERS = {
    # Simulation
    "pause_toggle": _cmd_pause_toggle,
    "set_paused": _cmd_set_paused,
    "set_speed": _cmd_set_speed,
    "speed_delta": _cmd_speed_delta,
    "step": _cmd_step,
    # Selection
    "select_agent": _cmd_select_agent,
    "select_tile": _cmd_select_tile,
    # Spawns
    "spawn_agent": _cmd_spawn_agent,
    "spawn_sheep": _cmd_spawn_sheep,
    "spawn_monster": _cmd_spawn_monster,
    "remove_agent": _cmd_remove_agent,
    "set_agent_stat": _cmd_set_agent_stat,
    # Monde
    "paint_tile": _cmd_paint_tile,
    "place_asset": _cmd_place_asset,
    "erase_tile": _cmd_erase_tile,
    "set_floor": _cmd_set_floor,
    "carve": _cmd_carve,
    "restore": _cmd_restore,
    "build_block": _cmd_build_block,
    # Journal
    "log": _cmd_log,
    # Sauvegarde
    "save": _cmd_save,
    "load": _cmd_load,
}
