"""UI Snapshots — vues immuables du moteur pour l'interface.

Chaque snapshot ne contient que des types simples (None, bool, int, float,
str, list, dict, tuples). Aucune surface Pygame, aucun widget Qt.

Réutilise les fonctions de diagnostics.py qui sont déjà validées.
"""
from __future__ import annotations

from typing import Any


def _safe_list(value) -> list:
    """Convertit un array numpy ou autre en liste Python."""
    if hasattr(value, "tolist"):
        return value.tolist()
    return list(value or [])


# ══════════════════════════════════════════════════════════════════════
#  Snapshot simulation globale
# ══════════════════════════════════════════════════════════════════════
def simulation_snapshot(sim, ui_state=None) -> dict[str, Any]:
    """État global de la simulation, pour le header / footer."""
    clock = getattr(sim, "clock", None)
    return {
        "tick": int(sim.w.tick),
        "paused": bool(sim.paused),
        "speed": int(sim.speed),
        "population": sum(1 for a in sim.agents if a.alive),
        "sheep": len(sim.sheep),
        "monsters": len(sim.monsters),
        "stats": {
            key: int(value) if isinstance(value, (int, float)) else value
            for key, value in sim.stats.items()
        },
        "clock": {
            "year": int(clock.year) if clock else 0,
            "day": int(clock.day) if clock else 0,
            "season": str(clock.season) if clock else "",
            "light": float(clock.light) if clock else 1.0,
            "temperature": float(clock.temp) if clock else 20.0,
            "rain": float(clock.rain) if clock else 0.0,
            "label": clock.label() if clock else "",
        },
        "selection": {
            "agent_eid": getattr(ui_state, "selected_agent_eid", None),
            "tile": getattr(ui_state, "selected_tile", None),
        },
    }


# ══════════════════════════════════════════════════════════════════════
#  Snapshot population
# ══════════════════════════════════════════════════════════════════════
def population_snapshot(sim, include_dead: bool = False) -> list[dict[str, Any]]:
    """Liste d'habitants, pour le tableau de population.

    ``include_dead`` ajoute les fiches allégées des décédés récents
    (``Sim.deceased``) : le moteur purge les cadavres à chaque tick, donc
    sans ce tampon l'option « Tous » du dock serait identique à « Vivants ».
    """
    from .diagnostics import agent_snapshot

    rows = []
    for agent in sim.agents:
        if not agent.alive:
            continue
        snap = agent_snapshot(sim, agent)
        if snap is not None:
            rows.append(snap)
    if include_dead:
        rows.extend(dict(r) for r in getattr(sim, "deceased", ()))
    return rows


# ══════════════════════════════════════════════════════════════════════
#  Snapshot agent sélectionné
# ══════════════════════════════════════════════════════════════════════
def selected_agent_snapshot(sim, ui_state=None,
                            include_activity: bool = False) -> dict[str, Any] | None:
    """Snapshot détaillé de l'habitant sélectionné.

    ``include_activity`` fusionne le bloc de diagnostic ``activity``
    (Phase 3) : état, but, position et compteur « bloqué », lus sur
    l'instance ``Being`` réelle. Opt-in car le contrat de clés du
    snapshot de base est vérifié à l'identique par les tests (Lot A) ;
    l'inspecteur demande explicitement le bloc enrichi.
    """
    eid = getattr(ui_state, "selected_agent_eid", None)
    if eid is None:
        agent = getattr(sim, "selected", None)
        if agent is not None and agent.alive:
            eid = agent.eid
        else:
            return None
    agent = next((a for a in sim.agents if a.eid == eid and a.alive), None)
    if agent is None:
        return None
    from .diagnostics import agent_snapshot, deliberation_snapshot, activity_snapshot
    snap = agent_snapshot(sim, agent)
    if snap is None:
        return None

    # Délibération (pensée sélectionnée visible) — toujours incluse
    deliberation = deliberation_snapshot(agent)
    if deliberation:
        snap["deliberation"] = deliberation

    # Contexte local (perception immédiate) — lu sur agent.context
    # qui est mis à jour par Sim._perceive à chaque tick.
    local_ctx = getattr(agent, "context", {}) or {}
    if local_ctx:
        snap["local_context"] = dict(local_ctx)

    if include_activity:
        # Bloc activité enrichi (Phase 3)
        act_snap = activity_snapshot(agent)
        if act_snap:
            snap["activity"] = act_snap

        # Diagnostic de décision (Phase 1) : la trace capturée par le moteur
        # lors de la dernière délibération. L'UI ne recalcule jamais les
        # candidats ; on recopie des dictionnaires déjà simples.
        snap["possibilities"] = [
            dict(row) for row in (getattr(agent, "decision_trace", []) or [])
        ]

    return snap


# ══════════════════════════════════════════════════════════════════════
#  Snapshot journal
# ══════════════════════════════════════════════════════════════════════
def journal_snapshot(sim, category: str = "all", search: str = "",
                     max_entries: int = 200) -> list[dict[str, Any]]:
    """Journal filtré, pour le panneau journal."""
    from .ui_registry import ALL_CATEGORIES

    entries = list(sim.journal)
    if category and category != ALL_CATEGORIES:
        entries = [e for e in entries if e[3] == category]
    if search:
        search_lower = search.lower()
        entries = [e for e in entries if search_lower in str(e[1]).lower()]
    result = []
    for tick, text, color, cat, count in entries[-max_entries:]:
        result.append({
            "tick": int(tick),
            "text": str(text),
            "color": tuple(color) if color else (180, 180, 180),
            "category": str(cat),
            "count": int(count),
        })
    return result


# ══════════════════════════════════════════════════════════════════════
#  Snapshot tiles (pour l'inspecteur de carte)
# ══════════════════════════════════════════════════════════════════════
def tile_snapshot(sim, tx: int, ty: int) -> dict[str, Any]:
    """Wrapper vers diagnostics.tile_snapshot."""
    from .diagnostics import tile_snapshot as _ts
    return _ts(sim, tx, ty)


# ══════════════════════════════════════════════════════════════════════
#  Snapshot carte (pour le rendu Qt)
# ══════════════════════════════════════════════════════════════════════
def map_snapshot(sim, ui_state=None) -> dict[str, Any]:
    """Données de carte pour le rendu : terrain, objets, agents, effets.

    Aucune surface ni rendu. Juste des coordonnées et des métadonnées.
    """
    w = sim.w
    alive_agents = []
    for a in sim.agents:
        if a.alive:
            alive_agents.append({
                "eid": int(a.eid),
                "x": float(a.x),
                "y": float(a.y),
                "tx": int(a.tx),
                "ty": int(a.ty),
                "color": str(a.color),
                "cls": str(a.cls),
                "stage": str(a.stage),
                "alive": True,
            })

    sheep_list = []
    for s in sim.sheep:
        sheep_list.append({
            "eid": int(s.eid),
            "x": float(s.x),
            "y": float(s.y),
            "tx": int(s.tx),
            "ty": int(s.ty),
        })

    monsters_list = []
    for m in sim.monsters:
        monsters_list.append({
            "eid": int(m.eid),
            "x": float(m.x),
            "y": float(m.y),
            "tx": int(m.tx),
            "ty": int(m.ty),
            "kind": str(getattr(m, "kind", "unknown")),
        })

    effects_list = []
    for e in sim.effects:
        effects_list.append({
            "kind": str(e.get("kind", "")),
            "x": float(e.get("x", 0)),
            "y": float(e.get("y", 0)),
            "color": tuple(e.get("color", (255, 255, 255))),
        })

    selected_eid = None
    if ui_state and getattr(ui_state, "selected_agent_eid", None) is not None:
        selected_eid = ui_state.selected_agent_eid

    return {
        "tick": int(w.tick),
        "grid": int(w.g),
        "fire_cells": int((w.fire > 0).sum()),
        "agents": alive_agents,
        "sheep": sheep_list,
        "monsters": monsters_list,
        "effects": effects_list,
        "selected_eid": selected_eid,
        "ghost_tile": getattr(ui_state, "ghost_tile", None) if ui_state else None,
        "ghost_visible": getattr(ui_state, "ghost_visible", False) if ui_state else False,
        "cemetery": [
            {"x": int(gx), "y": int(gy), "name": str(name)}
            for gx, gy, name, *_ in getattr(w, "cemetery", ())
        ],
    }


# ══════════════════════════════════════════════════════════════════════
#  Snapshot société
# ══════════════════════════════════════════════════════════════════════
def society_snapshot(sim) -> dict[str, Any]:
    """Données pour le panneau société."""
    alive = [a for a in sim.agents if a.alive]
    max_gen = max((a.gen for a in alive), default=0) if alive else 0
    bonded_count = sum(1 for a in alive if getattr(a, "bonded", None) is not None)

    alive_eids = {a.eid for a in alive}
    relations = []
    seen = set()
    for a in alive:
        for other_eid, rel_data in getattr(a, "rel", {}).items():
            if other_eid not in alive_eids:
                continue
            pair = (min(a.eid, other_eid), max(a.eid, other_eid))
            if pair in seen:
                continue
            seen.add(pair)
            trust = rel_data[0] if isinstance(rel_data, (tuple, list)) else float(rel_data)
            affection = rel_data[1] if isinstance(rel_data, (tuple, list)) and len(rel_data) > 1 else 0.0
            other = next((x for x in alive if x.eid == other_eid), None)
            if other is None:
                continue
            if a.bonded == other_eid:
                rel_type = "bonded"
            else:
                rel_type = "allied"
            relations.append({
                "eid1": a.eid,
                "name1": a.name,
                "eid2": other_eid,
                "name2": other.name,
                "type": rel_type,
                "confiance": float(trust),
                "affinite": float(affection),
            })

    institutions = []
    for key, value in getattr(sim.clan_knowledge, "institutions", {}).items():
        if not isinstance(value, dict):
            continue
        institutions.append({
            "key": str(key),
            "kind": value.get("kind", "unknown"),
            "members": list(value.get("members", [])),
            "stability": float(value.get("stability", 0.0)),
            "trust": float(value.get("trust", 0.0)),
            "age": int(value.get("age", 0)),
            "practices": {str(pk): int(pv)
                          for pk, pv in value.get("practices", {}).items()},
        })

    trade = []
    for key, value in getattr(sim, "_trade", {}).items():
        if isinstance(key, tuple) and len(key) >= 2:
            trade.append({
                "eid1": int(key[0]),
                "eid2": int(key[1]),
                "count": int(value),
            })

    return {
        "population": len(alive),
        "population_history": [int(v) for v in getattr(sim, "pop_hist", [])],
        "max_generation": int(max_gen),
        "bonded": bonded_count,
        "sheep": len(sim.sheep),
        "monsters": len(sim.monsters),
        "stats": {
            key: int(value)
            for key, value in sim.stats.items()
        },
        "institutions": institutions,
        "villages": [list(v) for v in getattr(sim, "_village_pts", [])],
        "dominance": {str(k): int(v)
                      for k, v in getattr(sim, "_dominance", {}).items()},
        "trade": trade,
        "relations": relations,
    }


# ══════════════════════════════════════════════════════════════════════
#  Snapshot Anima enrichi (pour l'inspecteur Anima)
# ══════════════════════════════════════════════════════════════════════
def anima_snapshot(sim, ui_state=None) -> dict[str, Any] | None:
    """Snapshot étendu pour l'inspecteur Anima complet."""
    base = selected_agent_snapshot(sim, ui_state)
    if base is None:
        return None

    agent = None
    eid = base.get("eid")
    if eid is not None:
        agent = next((a for a in sim.agents if a.eid == eid and a.alive), None)

    if agent is None:
        return base

    anima = getattr(agent, "anima", {}) or {}
    identity = dict(anima.get("identity", {}))
    values = dict(anima.get("values", {}))
    trauma = dict(anima.get("trauma", {}))
    intention = anima.get("intention")
    plan = anima.get("plan")
    beliefs = anima.get("beliefs", {})
    social_beliefs = beliefs.get("beings", {})

    base["anima"] = {
        "identity": identity,
        "values": values,
        "trauma": trauma,
        "intention": dict(intention) if isinstance(intention, dict) else None,
        "plan": dict(plan) if isinstance(plan, dict) else None,
        "attachments": dict(anima.get("attachments", {})),
        "reputation": dict(anima.get("reputation", {})),
        "social_beliefs": {
            str(key): dict(value) if isinstance(value, dict) else value
            for key, value in social_beliefs.items()
        },
        "episodes": list(anima.get("episodic_memory", []))[-50:],
        "causal_traces": list(anima.get("causal_traces", []))[-50:],
        "observations": list(anima.get("observations", []))[-50:],
        "habits": [float(value) for value in getattr(agent, "habits", [])],
    }

    return base
