"""UI Commands — commandes neutres validatees par le moteur.

Chaque commande est un dict avec au minimum ``kind``. Le moteur valide
les parametres, effectue l'action, et retourne un resultat dict.

Aucune dependance Pygame ni Qt.
"""
from __future__ import annotations

from typing import Any

import numpy as np

from .config import TILE


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

    box = _mutator_box(command)
    hist = getattr(sim, "history", None) if box else None
    if hist is not None:
        group = command.get("group")
        if group is not None and hist.has_pending() \
                and group == hist.pending_group:
            hist.extend(sim.w, box)
        else:
            hist.begin(sim.w, box, group=group)

    try:
        result = handler(sim, command)
    except Exception as exc:
        result = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}

    if hist is not None:
        if command.get("group") is None:
            if result.get("ok"):
                hist.commit()
            else:
                hist.discard()
        elif not result.get("ok"):
            # Échec en cours de glisser : l'entrée pendante reste ouverte,
            # les cellules réellement modifiées continuent de s'agréger.
            pass
    return result


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
    for key in ("color", "cls", "sex", "n_hid", "gen", "energy",
                "body", "cog", "personality", "emotions", "needs",
                "brain", "parents"):
        if key in cmd:
            kwargs[key] = cmd[key]
    shapes = {"body": 5, "cog": 4, "personality": 12, "emotions": 8, "needs": 7}
    for key, length in shapes.items():
        if key not in kwargs:
            continue
        values = kwargs[key]
        if not isinstance(values, (list, tuple)) or len(values) != length:
            return {"ok": False,
                    "error": f"{key} attend {length} valeurs entre 0 et 1"}
        try:
            kwargs[key] = np.clip(np.array([float(v) for v in values]), 0.0, 1.0)
        except (TypeError, ValueError):
            return {"ok": False, "error": f"{key} : valeurs numeriques attendues"}
    if x is not None:
        kwargs["x"] = float(x)
    if y is not None:
        kwargs["y"] = float(y)
    created = sim.spawn_agent(**kwargs)
    if created is None:
        return {"ok": False, "error": "Impossible de creer l'habitant (place ou limite)"}
    name = cmd.get("name")
    if name:
        created.name = str(name)[:32]
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
    from .config import MONSTER_KINDS
    x = cmd.get("x")
    y = cmd.get("y")
    kwargs = {}
    if x is not None:
        kwargs["x"] = float(x)
    if y is not None:
        kwargs["y"] = float(y)
    # "kind" est le discriminant de commande : le type de monstre vit dans une
    # cle dediee, sinon chaque monstre naissait avec kind="spawn_monster".
    monster_kind = cmd.get("monster_kind")
    if monster_kind:
        monster_kind = str(monster_kind)
        if monster_kind not in MONSTER_KINDS:
            return {"ok": False,
                    "error": f"Type de monstre inconnu: {monster_kind} "
                             f"(disponibles: {', '.join(MONSTER_KINDS)})"}
        kwargs["kind"] = monster_kind
    created = sim.spawn_monster(**kwargs)
    if created is None:
        return {"ok": False, "error": "Limite de monstres atteinte"}
    return {"ok": True, "eid": int(created.eid),
            "monster_kind": str(getattr(created, "kind", kwargs.get("kind", "?")))}


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


#: Nom de stat cote UI -> emplacement reel sur Being.
#: Les besoins vivent dans ``Being.needs`` (tableau indexe), avec ``hunger`` et
#: ``energy`` comme miroirs lisibles. Les ecrire directement par nom d'attribut
#: (``agent.faim``) etait un no-op silencieux : ces attributs n'existent pas.
_STAT_NEED_INDEX = {
    "faim": 0,
    "energie": 1,
    "soif": 2,
    "sommeil": 3,
    "securite": 4,
    "appartenance": 5,
    "estime": 6,
}
_STAT_ATTR = {
    "sante": "health",
    "douleur": "pain",
    "temperature": "temp",
}
_STAT_MIRROR = {0: "hunger", 1: "energy"}


def _cmd_set_agent_stat(sim, cmd):
    eid = cmd.get("eid")
    stat = cmd.get("stat")
    value = float(cmd.get("value", 0))
    if eid is None or stat is None:
        return {"ok": False, "error": "eid ou stat manquant"}
    agent = next((a for a in sim.agents if a.eid == int(eid) and a.alive), None)
    if agent is None:
        return {"ok": False, "error": "Habitant introuvable ou mort"}

    value = max(0.0, min(1.0, value))
    key = str(stat).strip().lower()

    index = _STAT_NEED_INDEX.get(key)
    if index is not None:
        agent.needs[index] = value
        mirror = _STAT_MIRROR.get(index)
        if mirror is not None:
            setattr(agent, mirror, value)
        return {"ok": True, "stat": key, "value": value}

    attr = _STAT_ATTR.get(key)
    if attr is not None:
        setattr(agent, attr, value)
        return {"ok": True, "stat": key, "value": value}

    if hasattr(agent, key):
        setattr(agent, key, value)
        return {"ok": True, "stat": key, "value": value}

    return {"ok": False, "error": f"Stat inconnue: {stat}"}


# ══════════════════════════════════════════════════════════════════════
#  Outils monde (paint / place / erase / carve / restore)
# ══════════════════════════════════════════════════════════════════════
def can_place(world, am, tx: int, ty: int, aid: int) -> tuple[bool, str]:
    """Validation de pose partagee par la commande ET l'apercu fantome.

    Le fantome ne doit jamais pouvoir mentir : il affiche exactement ce que
    ``place_asset`` acceptera ou refusera.
    """
    if not (0 <= aid < len(am.assets)):
        return False, "Asset invalide"
    adef = am.assets[aid]
    if not getattr(adef, "placable", False):
        return False, "Asset non placable"
    g = int(world.g)
    size = max(1, int(adef.size_tiles)) if bool(adef.solid) else 1
    for dy in range(size):
        for dx in range(size):
            cx, cy = tx + dx, ty + dy
            if not (0 <= cx < g and 0 <= cy < g):
                return False, "Empreinte hors du monde"
            if not world.land[cy, cx] or world.blocked[cy, cx] \
                    or world.content_at(cx, cy) >= 0:
                return False, "Case occupee ou incompatible"
    return True, ""


def _cmd_paint_tile(sim, cmd):
    """Peint un mode sur une zone de tuiles (water, land, wall)."""
    tx = int(cmd.get("tx", 0))
    ty = int(cmd.get("ty", 0))
    mode = cmd.get("mode", "land")
    radius = max(1, min(15, int(cmd.get("radius", 1))))
    w = sim.w

    if mode not in ("water", "land", "wall"):
        return {"ok": False, "error": f"Mode de peinture inconnu: {mode}"}
    if not (0 <= tx < w.g and 0 <= ty < w.g):
        return {"ok": False, "error": "Coordonnees hors monde"}

    changed = False
    missing_pool = False
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
                    else:
                        missing_pool = True

    if not changed:
        if missing_pool:
            return {"ok": False,
                    "error": "Aucun asset pierre disponible pour batir un mur"}
        return {"ok": True, "changed": False}
    return {"ok": True, "changed": True}


def _cmd_place_asset(sim, cmd):
    """Pose un asset sur une tuile."""
    tx = int(cmd.get("tx", 0))
    ty = int(cmd.get("ty", 0))
    aid = int(cmd.get("aid", -1))
    w = sim.w

    ok, reason = can_place(w, sim.am, tx, ty, aid)
    if not ok:
        return {"ok": False, "error": reason}
    adef = sim.am.assets[aid]
    w.place(tx, ty, aid, sim.am, hp=max(1, getattr(adef, "hp", 1)),
            solid=bool(adef.solid), shelter=bool(adef.shelter),
            size=adef.size_tiles if adef.solid else 1)
    return {"ok": True}


def _cmd_erase_tile(sim, cmd):
    """Efface objet et sol sur un disque de tuiles."""
    tx = int(cmd.get("tx", 0))
    ty = int(cmd.get("ty", 0))
    radius = max(1, min(15, int(cmd.get("radius", 1))))
    w = sim.w
    if not (0 <= tx < w.g and 0 <= ty < w.g):
        return {"ok": False, "error": "Coordonnees hors monde"}
    changed = False
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if dx * dx + dy * dy > radius * radius + 1:
                continue
            cx, cy = tx + dx, ty + dy
            if not (0 <= cx < w.g and 0 <= cy < w.g):
                continue
            removed = w.remove(cx, cy, quiet=True)
            old_len = len(w.items)
            w.items = [it for it in w.items
                       if not (int(it.x // TILE) == cx and int(it.y // TILE) == cy)]
            had_floor = w.floor[cy, cx] >= 0
            w.floor[cy, cx] = -1
            if removed or len(w.items) != old_len or had_floor:
                changed = True
    w.mark_dirty(tx, ty, radius + 1)
    return {"ok": True, "changed": changed}


def _cmd_set_floor(sim, cmd):
    """Definit le sol sur un disque de tuiles."""
    tx = int(cmd.get("tx", 0))
    ty = int(cmd.get("ty", 0))
    aid = int(cmd.get("aid", 0))
    radius = max(1, min(15, int(cmd.get("radius", 1))))
    w = sim.w
    if not (0 <= tx < w.g and 0 <= ty < w.g):
        return {"ok": False, "error": "Coordonnees hors monde"}
    if aid in sim.am.floors:
        sheet_idx = sim.am.floors.index(aid)
        tile_id = sheet_idx * 216
    elif sim.am.floors:
        tile_id = 0
    else:
        return {"ok": False, "error": "Pas de tileset de sol"}
    changed = False
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if dx * dx + dy * dy > radius * radius + 1:
                continue
            cx, cy = tx + dx, ty + dy
            if 0 <= cx < w.g and 0 <= cy < w.g and w.land[cy, cx]:
                w.set_floor(cx, cy, tile_id)
                changed = True
    return {"ok": True, "changed": changed}


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
    return {"ok": True, "changed": bool(changed)}


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
    return {"ok": True, "changed": bool(changed)}


def _cmd_build_block(sim, cmd):
    """Construit un bloc. Renvoie la raison precise en cas d'echec."""
    tx = int(cmd.get("tx", 0))
    ty = int(cmd.get("ty", 0))
    material = cmd.get("material", "bois")
    radius = max(1, min(15, int(cmd.get("radius", 1))))
    w = sim.w

    if not (0 <= tx < w.g and 0 <= ty < w.g):
        return {"ok": False, "error": "Coordonnees hors monde"}

    role = "block_wood" if material == "bois" else "block_stone"
    if not sim.am.pool(role):
        return {"ok": False,
                "error": f"Aucun asset bloc disponible pour le materiau: {material}"}

    built = 0
    last_error = "Construction refusee par le moteur"
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if dx * dx + dy * dy > radius * radius + 1:
                continue
            cx, cy = tx + dx, ty + dy
            if not (0 <= cx < w.g and 0 <= cy < w.g):
                continue
            if not w.land[cy, cx]:
                last_error = "Case non terrestre"
                continue
            if w.blocked[cy, cx]:
                last_error = "Case deja bloquee"
                continue
            if w.content_at(cx, cy) >= 0:
                last_error = "Case occupee"
                continue
            if sim.do_build_block_player(cx, cy, material=material):
                built += 1
    if built == 0:
        return {"ok": False, "error": last_error}
    return {"ok": True, "changed": True, "built": built}


# ══════════════════════════════════════════════════════════════════════
#  Historique (undo/redo) et outils personnalisés
# ══════════════════════════════════════════════════════════════════════
#: Commandes mutatrices du monde : leur état avant/après passe par
#: ``WorldHistory``. La valeur est le rayon par défaut de la boîte capturée.
_MUTATOR_RADIUS = {
    "paint_tile": 15,
    "place_asset": 4,
    "erase_tile": 15,
    "set_floor": 15,
    "carve": 15,
    "restore": 15,
    "build_block": 15,
}


def _mutator_box(command) -> tuple[int, int, int, int] | None:
    kind = command.get("kind")
    if kind not in _MUTATOR_RADIUS:
        return None
    tx = int(command.get("tx", 0))
    ty = int(command.get("ty", 0))
    r = int(command.get("radius", 1)) + 2
    r = max(r, min(_MUTATOR_RADIUS[kind], r))
    return tx - r, ty - r, tx + r + 1, ty + r + 1


def _cmd_undo(sim, cmd):
    hist = getattr(sim, "history", None)
    if hist is None:
        return {"ok": False, "error": "Historique indisponible"}
    if not hist.undo(sim.w):
        return {"ok": True, "changed": False}
    return {"ok": True, "changed": True}


def _cmd_redo(sim, cmd):
    hist = getattr(sim, "history", None)
    if hist is None:
        return {"ok": False, "error": "Historique indisponible"}
    if not hist.redo(sim.w):
        return {"ok": True, "changed": False}
    return {"ok": True, "changed": True}


def _cmd_end_stroke(sim, cmd):
    """Fin d'un glisser : pousse l'entrée d'historique pendante."""
    hist = getattr(sim, "history", None)
    if hist is None or not hist.has_pending():
        return {"ok": True, "changed": False}
    hist.commit()
    return {"ok": True, "changed": True}


def _cmd_create_tool(sim, cmd):
    """Écrit un PNG 16x16 dans assets/tools_custom/ et l'enregistre."""
    import os
    import re

    from PIL import Image

    pixels = cmd.get("pixels")
    if not isinstance(pixels, (list, tuple)) or len(pixels) != 256:
        return {"ok": False, "error": "pixels attendu : 256 entrees RGBA"}
    name = str(cmd.get("name", "outil"))[:32] or "outil"
    tool_kind = str(cmd.get("tool_kind", "hache"))
    from .config import TOOL_RECIPES
    if tool_kind not in TOOL_RECIPES:
        return {"ok": False,
                "error": f"Type d'outil inconnu: {tool_kind} "
                         f"(disponibles: {', '.join(sorted(TOOL_RECIPES))})"}

    root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "assets", "tools_custom")
    os.makedirs(root, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "outil"
    path = os.path.join(root, f"{tool_kind}_{slug}.png")
    n = 2
    while os.path.exists(path):
        path = os.path.join(root, f"{tool_kind}_{slug}_{n}.png")
        n += 1

    image = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    flat = image.load()
    for i, pixel in enumerate(pixels):
        try:
            r, g, b, a = (int(v) for v in pixel)
        except (TypeError, ValueError):
            return {"ok": False, "error": f"Pixel {i} invalide"}
        flat[i % 16, i // 16] = (max(0, min(255, r)), max(0, min(255, g)),
                                 max(0, min(255, b)), max(0, min(255, a)))
    image.save(path, "PNG")

    aid = sim.am.register_custom_tool(path, tool_kind, label=name)
    return {"ok": True, "aid": int(aid), "path": str(path)}


def _cmd_equip_tool(sim, cmd):
    eid = cmd.get("eid")
    aid = cmd.get("aid")
    if eid is None or aid is None:
        return {"ok": False, "error": "eid et aid requis"}
    agent = next((a for a in sim.agents if a.eid == int(eid) and a.alive), None)
    if agent is None:
        return {"ok": False, "error": "Habitant introuvable ou mort"}
    aid = int(aid)
    if not (0 <= aid < len(sim.am.assets)):
        return {"ok": False, "error": "Asset invalide"}
    adef = sim.am.assets[aid]
    if not getattr(adef, "tool", False):
        return {"ok": False, "error": f"{adef.label or adef.name} n'est pas un outil"}
    from .config import TOOL_RECIPES
    kind = str((adef.meta or {}).get("tool_kind", "hache"))
    agent.tool = aid
    agent.tool_durability = int(TOOL_RECIPES.get(kind, {}).get("durability", 40))
    return {"ok": True, "eid": int(agent.eid), "aid": aid,
            "durability": int(agent.tool_durability)}


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
    path, sz = save_game(sim, cam, slot=slot,
                         ui_state=cmd.get("ui_state"))
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


def _cmd_reset_world(sim, cmd):
    """Reconstruit un monde neuf. Destructif : l'UI doit confirmer avant."""
    from .engine import build_world, build_world_blank, seed_life

    am = getattr(sim, "am", None)
    if am is None:
        return {"ok": False, "error": "AssetManager indisponible"}

    mode = str(cmd.get("mode", "procedural"))
    if mode not in ("procedural", "plat", "vierge"):
        return {"ok": False, "error": f"Mode de monde inconnu: {mode} "
                                      "(attendu: procedural, plat ou vierge)"}
    seed = cmd.get("seed")
    seed = int(seed) if seed is not None else int(getattr(sim, "seed", 7))
    n_agents = max(0, int(cmd.get("n_agents", 60)))
    n_sheep = max(0, int(cmd.get("n_sheep", 40)))

    if mode == "vierge":
        world, new_sim = build_world_blank(am, seed)
    else:
        world, new_sim = build_world(am, seed, procedural=(mode == "procedural"))
        seed_life(world, new_sim, new_sim.rng, n_agents=n_agents, n_sheep=n_sheep)

    new_sim.speed = int(getattr(sim, "speed", 2))
    return {"ok": True, "sim": new_sim, "seed": seed, "mode": mode}


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
    # Historique et outils personnalisés
    "undo": _cmd_undo,
    "redo": _cmd_redo,
    "end_stroke": _cmd_end_stroke,
    "create_tool": _cmd_create_tool,
    "equip_tool": _cmd_equip_tool,
    # Journal
    "log": _cmd_log,
    # Sauvegarde
    "save": _cmd_save,
    "load": _cmd_load,
    "reset_world": _cmd_reset_world,
}


# ══════════════════════════════════════════════════════════════════════
#  Etat d'interface (UIState)
#
#  Ces commandes ne touchent pas le moteur : elles rendent l'état de
#  l'interface modifiable, testable et sauvegardable au lieu d'être écrit
#  directement par les widgets.
# ══════════════════════════════════════════════════════════════════════
def execute_ui_command(ui_state, command: dict) -> dict[str, Any] | None:
    """Exécute une commande d'interface.

    Renvoie ``None`` si la commande ne concerne pas ``UIState``, afin que
    l'appelant puisse la transmettre au moteur.
    """
    kind = command.get("kind", "")
    handler = _UI_HANDLERS.get(kind)
    if handler is None:
        return None
    try:
        return handler(ui_state, command)
    except Exception as exc:
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}


def _ui_set_mode(ui_state, cmd):
    from .ui_registry import MODES
    mode = str(cmd.get("mode", ""))
    if mode not in {m for m, _ in MODES}:
        return {"ok": False, "error": f"Mode d'outil inconnu: {mode}"}
    ui_state.active_mode = mode
    return {"ok": True, "mode": mode}


def _ui_set_overlay(ui_state, cmd):
    mode = str(cmd.get("overlay", cmd.get("mode", "")))
    if not mode:
        return {"ok": False, "error": "Overlay manquant"}
    ui_state.active_overlay = mode
    return {"ok": True, "overlay": mode}


def _ui_set_brush_size(ui_state, cmd):
    size = max(1, min(15, int(cmd.get("size", cmd.get("radius", 1)))))
    ui_state.brush_size = size
    return {"ok": True, "brush_size": size}


def _ui_set_block_material(ui_state, cmd):
    from .config import BLOCK_MATERIALS
    material = str(cmd.get("material", "bois"))
    if material not in BLOCK_MATERIALS:
        return {"ok": False,
                "error": f"Matériau non constructible: {material} "
                         f"(disponibles: {', '.join(BLOCK_MATERIALS)})"}
    ui_state.block_material = material
    return {"ok": True, "material": material}


def _ui_set_monster_kind(ui_state, cmd):
    from .config import MONSTER_KINDS
    kind = str(cmd.get("monster_kind", ""))
    if kind and kind not in MONSTER_KINDS:
        return {"ok": False,
                "error": f"Type de monstre inconnu: {kind} "
                         f"(disponibles: {', '.join(MONSTER_KINDS)})"}
    ui_state.monster_kind = kind
    return {"ok": True, "monster_kind": kind}


def _ui_select_asset(ui_state, cmd):
    aid = cmd.get("aid")
    ui_state.selected_asset_id = None if aid is None else int(aid)
    return {"ok": True, "aid": ui_state.selected_asset_id}


_UI_HANDLERS = {
    "set_mode": _ui_set_mode,
    "set_overlay": _ui_set_overlay,
    "set_brush_size": _ui_set_brush_size,
    "set_block_material": _ui_set_block_material,
    "set_monster_kind": _ui_set_monster_kind,
    "select_asset": _ui_select_asset,
}
