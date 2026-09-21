"""Diagnostics purs du monde vivant.

Ce module ne modifie jamais Sim, World ou Being. Il convertit leur état
réel en dictionnaires simples que l'UI peut afficher sans dupliquer la
logique métier.
"""
from __future__ import annotations

from typing import Any
import math

from .config import GRID, TILE


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def action_name(sim, action: int | None) -> str:
    if action is None:
        return "Aucune"
    try:
        from .brain_api import ACTION_NAMES_EXP
        return ACTION_NAMES_EXP.get(int(action), f"Action {action}")
    except Exception:
        return f"Action {action}"


def asset_info(am, aid: int | None) -> dict | None:
    if aid is None or not (0 <= int(aid) < len(am.assets)):
        return None
    a = am.assets[int(aid)]
    return {
        "id": int(aid),
        "nom": getattr(a, "label", getattr(a, "name", "asset")),
        "role": getattr(a, "role", ""),
        "categorie": getattr(a, "category", ""),
        "solid": bool(getattr(a, "solid", False)),
        "abri": bool(getattr(a, "shelter", False)),
        "comestible": float(getattr(a, "edible", 0.0)),
        "outil": bool(getattr(a, "tool", False)),
        "recolte": dict(getattr(a, "harvest", None) or {}),
        "affordances": list(getattr(a, "afford", ()) or ()),
        "inflammable": bool(getattr(a, "flammable", False)),
    }


def agent_snapshot(sim, agent) -> dict[str, Any] | None:
    """Instantané complet d'un habitant vivant.

    Toutes les valeurs proviennent directement de l'instance Being.
    """
    if agent is None or not getattr(agent, "alive", False):
        return None

    goal = getattr(agent, "goal", None) or {}
    goal_tx = goal.get("x")
    goal_ty = goal.get("y")
    distance = None
    if goal_tx is not None and goal_ty is not None:
        distance = math.hypot(goal_tx * TILE + TILE / 2 - agent.x,
                              goal_ty * TILE + TILE / 2 - agent.y)

    tool_aid = getattr(agent, "tool", -1)
    tool = asset_info(sim.am, tool_aid) if tool_aid >= 0 else None

    brain_rank = []
    explain = getattr(getattr(agent, "brain", None), "explain", None)
    if callable(explain):
        try:
            brain_rank = explain(top=5)
        except Exception:
            brain_rank = []

    memories = {}
    for category, entries in getattr(agent, "seen", {}).items():
        memories[category] = [
            {"x": int(x), "y": int(y), "force": float(force)}
            for x, y, force in entries
        ]

    relatives = []
    for other in sim.agents:
        if other.eid == agent.eid:
            continue
        relation = getattr(agent, "rel", {}).get(other.eid)
        if relation is None:
            continue
        trust = relation[0] if isinstance(relation, (tuple, list)) else float(relation)
        affection = relation[1] if isinstance(relation, (tuple, list)) and len(relation) > 1 else 0.0
        relatives.append({
            "eid": other.eid,
            "nom": other.name,
            "confiance": float(trust),
            "affection": float(affection),
            "vivant": bool(other.alive),
        })

    relatives.sort(key=lambda r: (r["confiance"] + r["affection"]), reverse=True)

    return {
        "eid": int(agent.eid),
        "nom": agent.name,
        "vivant": bool(agent.alive),
        "sexe": agent.sex,
        "classe": agent.cls,
        "clan": agent.color,
        "generation": int(agent.gen),
        "age_ans": float(agent.age_years),
        "stage": agent.stage,
        "mort_naturelle_ans": float(agent.natural_death_age / 43200.0),
        "position": {"x": float(agent.x), "y": float(agent.y),
                     "tx": int(agent.tx), "ty": int(agent.ty)},
        "etat": getattr(agent, "state", "idle"),
        "sante": float(agent.health),
        "douleur": float(agent.pain),
        "temperature": float(agent.temp),
        "energie": float(agent.energy),
        "faim": float(agent.hunger),
        "soif": float(agent.needs[2]),
        "sommeil": float(agent.needs[3]),
        "securite": float(agent.needs[4]),
        "appartenance": float(agent.needs[5]),
        "estime": float(agent.needs[6]),
        "emotions": {str(i): float(v) for i, v in enumerate(agent.emotions)},
        "personnalite": {str(i): float(v) for i, v in enumerate(agent.personality)},
        "corps": {str(i): float(v) for i, v in enumerate(agent.body)},
        "cognition": {str(i): float(v) for i, v in enumerate(agent.cog)},
        "competences": {"recolte": float(agent.skills[0]),
                        "construction": float(agent.skills[1]),
                        "combat": float(agent.skills[2]),
                        "social": float(agent.skills[3])},
        "inventaire": dict(agent.inv),
        "outil": tool,
        "durabilite_outil": int(getattr(agent, "tool_durability", 0)),
        "but": {
            "action": goal.get("act"),
            "action_nom": action_name(sim, goal.get("act")),
            "cible_x": goal_tx,
            "cible_y": goal_ty,
            "distance_px": distance,
            "expiration_tick": goal.get("until"),
            "intensite": goal.get("intensity", 0.0),
            "bloque_ticks": int(getattr(agent, "stuck", 0)),
        },
        "cerveau": {
            "neurones": int(agent.brain.n),
            "frequence_reflexion": int(agent.brain.te),
            "classement_actions": brain_rank,
        },
        "memoire": memories,
        "croyances_danger": dict(getattr(agent, "belief_places", {})),
        "relations": relatives[:12],
        "partenaire_eid": getattr(agent, "bonded", None),
        "parents": list(getattr(agent, "parents", ()) or ()),
        "enfants": list(getattr(agent, "children", ()) or ()),
        "episodes": list(getattr(agent, "episodes", ()))[-12:],
        "vie": list(getattr(agent, "life", ()))[-12:],
    }


def tile_snapshot(sim, tx: int, ty: int) -> dict[str, Any]:
    """Instantané exact d'une tuile ou d'une cellule du monde."""
    w = sim.w
    tx, ty = int(tx), int(ty)
    if not (0 <= tx < w.g and 0 <= ty < w.g):
        return {"dans_monde": False, "tx": tx, "ty": ty}

    aid = w.content_at(tx, ty)
    ainfo = asset_info(sim.am, aid)
    result = {
        "dans_monde": True,
        "tx": tx,
        "ty": ty,
        "terre": bool(w.land[ty, tx]),
        "eau": bool(w.water[ty, tx]),
        "bloque": bool(w.blocked[ty, tx]),
        "abri": bool(w.shelter[ty, tx]),
        "feu": int(w.fire[ty, tx]),
        "odeur": float(w.smell[ty, tx]),
        "exploration": float(w.heat[ty, tx]),
        "pheromone": float(w.marker[ty, tx]),
        "couleur_pheromone": int(w.marker_col[ty, tx]),
        "sol": int(w.floor[ty, tx]),
        "objet": ainfo,
        "pv_objet": int(w.hp[ty, tx]) if aid >= 0 else 0,
        "repousse": float(w.regrow[ty, tx]),
        "cimetiere": False,
        "tombe": None,
        "stockage": None,
        "chantier": None,
    }

    for grave in getattr(w, "cemetery", ()):
        gx, gy, name, death_tick, color = grave
        if int(gx) == tx and int(gy) == ty:
            result["cimetiere"] = True
            result["tombe"] = {
                "nom": name,
                "tick_deces": int(death_tick),
                "couleur": tuple(color),
            }
            break

    storage = getattr(w, "storages", {}).get((tx, ty))
    if storage is not None:
        result["stockage"] = {
            "capacite": int(storage.capacity),
            "inventaire": dict(storage.inventory),
            "clan": getattr(storage, "owner_clan", None),
            "remplissage": float(sum(storage.inventory.values()) / max(1, storage.capacity)),
        }

    site = getattr(w, "sites", {}).get((tx, ty))
    if site is None:
        site = w.site_at(tx, ty)
    if site is not None:
        result["chantier"] = {
            "nom": site.blueprint_name,
            "progression": site.progress(),
            "manquant": site.missing_materials(),
            "contributeurs": list(site.contributors),
            "blocs_poses": len(site.placed),
            "blocs_total": len(site.tasks),
        }

    gen = getattr(w, "gen", None)
    if gen is not None:
        try:
            from . import worldgen as wg
            result["biome"] = wg.biome_name(gen, tx, ty)
            result["altitude"] = float(wg.height_at(gen, tx, ty))
            result["pente"] = float(wg.slope(gen)[ty, tx])
        except Exception as exc:
            result["diagnostic_error"] = f"{type(exc).__name__}: {exc}"

    return result


def world_snapshot(sim) -> dict[str, Any]:
    """Résumé global léger, utile au panneau laboratoire."""
    alive = [a for a in sim.agents if a.alive]
    w = sim.w
    return {
        "tick": int(w.tick),
        "annee": int(sim.clock.year + 1),
        "saison": sim.clock.season,
        "jour": int(sim.clock.day + 1),
        "heure": sim.clock.label,
        "population": len(alive),
        "moutons": len(sim.sheep),
        "items": len(w.items),
        "feux": int((w.fire > 0).sum()),
        "tombes": len(getattr(w, "cemetery", ())),
        "naissances": int(sim.stats.get("births", 0)),
        "deces": int(sim.stats.get("deaths", 0)),
        "recoltes": int(sim.stats.get("harvests", 0)),
        "constructions": int(sim.stats.get("builds", 0)),
        "attaques": int(sim.stats.get("attacks", 0)),
        "dons": int(sim.stats.get("gives", 0)),
        "vols": int(sim.stats.get("takes", 0)),
        "paroles": int(sim.stats.get("talks", 0)),
        "temperature": float(sim.clock.temp),
        "pluie": float(sim.clock.rain),
        "lumiere": float(sim.clock.light),
        "champion": getattr(sim.academy, "champion_label", "aucun"),
        "score_champion": float(getattr(sim.academy, "champion_score", float("-inf"))),
    }
