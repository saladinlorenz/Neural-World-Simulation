"""Diagnostics purs du monde vivant.

Ce module ne modifie jamais Sim, World ou Being. Il convertit leur état
réel en dictionnaires simples que l'UI peut afficher sans dupliquer la
logique métier.
"""
from __future__ import annotations

from typing import Any
import math

from .config import (GRID, TILE, BODY_DEFS, COG_DEFS, EMOTION_DEFS,
                     PERSONALITY_DEFS, NEED_DEFS, TICKS_PER_YEAR)


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _labelled(values, defs) -> dict[str, float]:
    """Associe chaque valeur d'un tableau NumPy à son libellé métier.

    Sans cela les grilles de l'inspecteur affichaient ``{"0": 0.4, …}`` :
    les noms existent dans ``game.config`` mais n'étaient jamais utilisés.
    """
    out = {}
    for i, v in enumerate(values):
        name = defs[i] if i < len(defs) else f"#{i}"
        out[name] = float(v)
    return out


def action_name(sim, action: int | None) -> str:
    if action is None:
        return "Aucune"
    try:
        from .brain_api import ACTION_NAMES_EXP
        return ACTION_NAMES_EXP.get(int(action), f"Action {action}")
    except Exception:
        return f"Action {action}"


#: Libellés FR des activités composées (même source que la carte).
#: Clés = ``Being.activity.kind`` réels ; l'UI traduit, jamais le moteur.
ACTIVITY_FR = {
    "food_expedition": "expédition de nourriture",
    "water_search": "recherche d'eau",
    "return_home": "retour au foyer",
    "explore_region": "exploration de région",
}


def agent_narrative(snap: dict | None) -> str:
    """Lecture narrative d'un snapshot habitant (WORLD ALIVE).

    Pure et défensive : ne lit que le snapshot (jamais Being/Sim), ne
    lève jamais. Retourne 3 à 5 phrases FR construites sur des données
    réelles : besoin dominant, émotion, activité/intention en cours,
    mémoire mobilisée (confiance), dernier résultat causal.
    L'inspecteur affiche ce texte EN PREMIER, les tableaux ensuite.
    """
    if not isinstance(snap, dict):
        return ""
    name = str(snap.get("name", "L'habitant") or "L'habitant")
    lines: list[str] = []

    needs_named = snap.get("needs_named", {}) or {}
    deliberation = snap.get("deliberation", {}) or {}
    decision_trace = snap.get("decision_trace", {}) or {}
    need_name = (deliberation.get("dominant_need")
                 or (decision_trace.get("dominant_need", {}) or {}).get("name")
                 if isinstance(decision_trace.get("dominant_need"), dict)
                 else deliberation.get("dominant_need"))
    need_val = None
    if isinstance(decision_trace.get("dominant_need"), dict):
        need_val = decision_trace["dominant_need"].get("value")
    if not need_name:
        # Fallback : besoin le plus élevé du snapshot (donnée réelle).
        try:
            need_name = max(needs_named, key=lambda k: float(needs_named[k]))
            need_val = float(needs_named[need_name])
        except (TypeError, ValueError):
            need_name, need_val = None, None
    if need_name:
        if isinstance(need_val, (int, float)):
            lines.append(f"{name} ressent surtout {need_name} ({need_val:.0%}).")
        else:
            lines.append(f"{name} ressent surtout {need_name}.")

    emo_name = (deliberation.get("dominant_emotion") or "")
    if not emo_name and isinstance(decision_trace.get("dominant_emotion"), dict):
        emo_name = decision_trace["dominant_emotion"].get("name", "")
    if emo_name and emo_name != "—":
        lines.append(f"Émotion dominante : {emo_name}.")

    activity = snap.get("activity", {}) or {}
    kind = activity.get("kind")
    stage = activity.get("stage", "")
    if isinstance(kind, str) and kind in ACTIVITY_FR:
        label = ACTIVITY_FR[kind]
        tgt_tx, tgt_ty = activity.get("target_tx"), activity.get("target_ty")
        if tgt_tx is not None and tgt_ty is not None:
            try:
                lines.append(
                    f"Elle/il mène une {label} "
                    f"(étape {stage or '—'}, cible {int(tgt_tx)},{int(tgt_ty)})."
                )
            except (TypeError, ValueError):
                lines.append(f"Elle/il mène une {label} (étape {stage or '—'}).")
        else:
            lines.append(f"Elle/il mène une {label} (étape {stage or '—'}).")
        reason = activity.get("reason", "")
        if reason:
            lines.append(f"Motif : {reason}.")
    else:
        state = activity.get("state", snap.get("state", ""))
        goal_action = activity.get("goal_action")
        if goal_action is not None:
            lines.append(f"État : {state}, action en cours : {goal_action}.")
        elif state:
            lines.append(f"État : {state}.")

    memories = snap.get("relevant_memories", []) or []
    if memories:
        try:
            best = max(memories,
                       key=lambda r: float(r.get("confidence", 0.0) or 0.0))
            cat = best.get("category", "?")
            conf = float(best.get("confidence", 0.0) or 0.0)
            tx, ty = best.get("tx", "?"), best.get("ty", "?")
            lines.append(
                f"Mémoire mobilisée : {cat} en ({tx},{ty}), "
                f"confiance {conf:.0%}."
            )
        except (TypeError, ValueError):
            pass

    last = snap.get("last_activity_result", {}) or {}
    if isinstance(last, dict) and last:
        lkind = last.get("kind", "?")
        outcome = last.get("outcome", "?")
        reason_l = last.get("reason", last.get("failure_reason", ""))
        extra = f" ({reason_l})" if reason_l else ""
        lines.append(f"Dernier essai ({lkind}) : {outcome}{extra}.")

    stuck = activity.get("stuck", 0)
    try:
        if int(stuck) >= 20:
            lines.append(f"⚠ Bloqué depuis {int(stuck)} ticks.")
    except (TypeError, ValueError):
        pass
    return "\n".join(lines[:6])


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
            {"x": int(x), "y": int(y), "strength": float(force)}
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
            "name": other.name,
            "trust": float(trust),
            "affection": float(affection),
            "alive": bool(other.alive),
        })

    relatives.sort(key=lambda r: (r["trust"] + r["affection"]), reverse=True)

    # Besoins nommés : hunger/energy sont des miroirs lisibles de
    # needs[0]/needs[1] ; les cinq autres viennent directement du tableau.
    # Les libellés viennent de NEED_DEFS (source unique dans config).
    # Bornage [0, 1] avant toute conversion en pourcentage : une santé ou
    # un besoin hors bornes ne doit jamais fuiter tel quel dans l'UI.
    needs_named = {
        NEED_DEFS[0]: clamp01(agent.hunger),
        NEED_DEFS[1]: clamp01(agent.energy),
        NEED_DEFS[2]: clamp01(agent.needs[2]),
        NEED_DEFS[3]: clamp01(agent.needs[3]),
        NEED_DEFS[4]: clamp01(agent.needs[4]),
        NEED_DEFS[5]: clamp01(agent.needs[5]),
        NEED_DEFS[6]: clamp01(agent.needs[6]),
    }

    return {
        "eid": int(agent.eid),
        "name": agent.name,
        "alive": bool(agent.alive),
        "sex": agent.sex,
        "class": agent.cls,
        "clan": agent.color,
        "generation": int(agent.gen),
        "age_years": float(agent.age_years),
        "stage": agent.stage,
        "natural_death_age_years": float(
            agent.natural_death_age / TICKS_PER_YEAR),
        "avatar_idx": int(getattr(agent, "avatar", 0)),
        "position": {"x": float(agent.x), "y": float(agent.y),
                     "tx": int(agent.tx), "ty": int(agent.ty)},
        "state": getattr(agent, "state", "idle"),
        "health": clamp01(agent.health),
        "pain": float(agent.pain),
        "temperature": float(agent.temp),
        "needs_named": needs_named,
        "emotions_named": _labelled(agent.emotions, EMOTION_DEFS),
        "personality_named": _labelled(agent.personality, PERSONALITY_DEFS),
        "body_named": _labelled(agent.body, BODY_DEFS),
        "cognition_named": _labelled(agent.cog, COG_DEFS),
        "skills_named": {"harvest": float(agent.skills[0]),
                         "building": float(agent.skills[1]),
                         "combat": float(agent.skills[2]),
                         "social": float(agent.skills[3])},
        "inventory": dict(agent.inv),
        "tool": tool,
        "tool_durability": int(getattr(agent, "tool_durability", 0)),
        "goal": {
            "action": goal.get("act"),
            "action_name": action_name(sim, goal.get("act")),
            "target_x": goal_tx,
            "target_y": goal_ty,
            "distance_px": distance,
            "until_tick": goal.get("until"),
            "intensity": goal.get("intensity", 0.0),
            "stuck_ticks": int(getattr(agent, "stuck", 0)),
        },
        "brain": {
            "neurons": int(agent.brain.n),
            "think_frequency": int(agent.brain.te),
            "action_ranking": brain_rank,
        },
        "memory": memories,
        "danger_beliefs": dict(getattr(agent, "belief_places", {})),
        "relations": relatives[:12],
        "family": {
            "partner_eid": getattr(agent, "bonded", None),
            "father_eid": getattr(agent, "parent_pere_id", None),
            "mother_eid": getattr(agent, "parent_mere_id", None),
            "children": list(getattr(agent, "children", ()) or ()),
        },
        "episodes": list(getattr(agent, "episodes", ()))[-12:],
        "life": list(getattr(agent, "life", ()))[-12:],
    }


def deceased_row(sim, agent) -> dict[str, Any]:
    """Fiche allégée d'un habitant mort, au format du tableau de population."""
    return {
        "eid": int(agent.eid),
        "name": agent.name,
        "alive": False,
        "sex": getattr(agent, "sex", "?"),
        "class": getattr(agent, "cls", ""),
        "clan": getattr(agent, "color", ""),
        "generation": int(getattr(agent, "gen", 0)),
        "age_years": float(getattr(agent, "age_years", 0.0)),
        "stage": getattr(agent, "stage", ""),
        "health": 0.0,
        "needs_named": {
            NEED_DEFS[0]: clamp01(getattr(agent, "hunger", 0.0)),
            NEED_DEFS[1]: 0.0,
        },
        "death_tick": int(sim.w.tick),
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


def deliberation_snapshot(agent, tick=-1) -> dict[str, Any] | None:
    """Snapshot de la dernière délibération de l'agent.

    Construit le résumé « pensée sélectionnée » à partir de champs déjà
    présents sur l'instance ``Being`` : pressions de besoins, émotion,
    candidats évalués, et les vérités enregistrées par le moteur au moment
    du choix (``last_selection_*``) et de l'échec (``last_failure_*``).

    L'UI ne recalcule jamais les candidats ni les raisons ; elle lit ce
    dictionnaire.
    """
    if agent is None or not getattr(agent, "alive", False):
        return None

    # Pression dominante : mêmes sources que les besoins affichés ailleurs,
    # l'énergie traitée en DÉFICIT (1 - énergie) puisqu'une énergie basse est
    # la pression réelle. Le libellé reste celui du dépôt (NEED_DEFS) pour ne
    # pas changer le contrat de l'UI ; la clé et la pression sont exposées à
    # côté (l'UI qui attend une chaîne continue de fonctionner).
    needs_arr = getattr(agent, "needs", None)

    def _need_at(i: int) -> float:
        try:
            if needs_arr is None or len(needs_arr) <= i:
                return 0.0
            return float(needs_arr[i])
        except (TypeError, ValueError):
            return 0.0

    pressures = {
        "hunger": clamp01(getattr(agent, "hunger", 0.0)),
        "energy_deficit": clamp01(1.0 - float(getattr(agent, "energy", 0.0))),
        "thirst": _need_at(2),
        "sleep": _need_at(3),
        "safety": _need_at(4),
        "belonging": _need_at(5),
        "esteem": _need_at(6),
    }
    need_key = max(pressures, key=pressures.get)
    need_pressure = max(0.0, min(1.0, pressures[need_key]))
    _label_index = {"hunger": 0, "energy_deficit": 1, "thirst": 2, "sleep": 3,
                    "safety": 4, "belonging": 5, "esteem": 6}
    _idx = _label_index.get(need_key, -1)
    dominant_need = (NEED_DEFS[_idx] if 0 <= _idx < len(NEED_DEFS)
                     else str(need_key))

    # Émotion dominante
    emotions_arr = getattr(agent, "emotions", None)
    dominant_emotion = ""
    if emotions_arr is not None and len(emotions_arr) >= 8:
        idx = int(max(range(8), key=lambda i: float(emotions_arr[i])))
        dominant_emotion = EMOTION_DEFS[idx] if idx < len(EMOTION_DEFS) else f"#{idx}"

    # Candidats évalués (déjà calculés par evaluate_candidates)
    candidates = getattr(agent, "decision_trace", []) or []
    # Ne garder que les 8 meilleurs (déjà triés : selected en premier)
    top_candidates = candidates[:8]

    # Candidat sélectionné
    selected = None
    for c in top_candidates:
        if c.get("state") == "selected":
            selected = {
                "verb": c.get("verb"),
                "target_kind": c.get("target_kind"),
                "target_id": c.get("target_id"),
                "tx": c.get("tx"),
                "ty": c.get("ty"),
                "score": c.get("score"),
            }
            break

    # Raison du choix : vérité enregistrée par le moteur au moment du choix
    # (plus aucune déduction depuis un candidat « feasible »).
    reason = str(getattr(agent, "last_selection_reason", ""))
    reason_tick = int(getattr(agent, "last_selection_tick", -1))

    # Dernier échec : vérité enregistrée au moment de l'échec (plus aucune
    # recherche du point de ``failed_targets`` qui expire le plus tard).
    failure_reason = str(getattr(agent, "last_failure_reason", ""))
    failure_tick = int(getattr(agent, "last_failure_tick", -1))

    return {
        "tick": int(tick),
        "dominant_need": dominant_need,
        "dominant_need_key": str(need_key),
        "dominant_need_pressure": float(need_pressure),
        "dominant_emotion": dominant_emotion,
        "candidates": top_candidates,
        "selected": selected,
        "reason": reason,
        "reason_tick": reason_tick,
        "failure_reason": failure_reason,
        "failure_tick": failure_tick,
    }


def activity_snapshot(agent) -> dict[str, Any] | None:
    """Snapshot de l'activité courante de l'agent."""
    if agent is None or not getattr(agent, "alive", False):
        return None

    activity = getattr(agent, "activity", None)
    if activity is None:
        # Fallback sur les champs existants (state, goal, stuck)
        return {
            "state": getattr(agent, "state", "idle"),
            "goal_action": (int(agent.goal["act"]) if agent.goal and agent.goal.get("act") is not None else None),
            "goal_tile": ([int(agent.goal["x"]), int(agent.goal["y"])] if agent.goal and agent.goal.get("x") is not None and agent.goal.get("y") is not None else None),
            "position": [round(float(agent.x), 1), round(float(agent.y), 1)],
            "stuck": int(getattr(agent, "stuck", 0)),
        }

    # Si activity est un objet, sérialisation PAR LISTE BLANCHE : jamais
    # ``__dict__``, jamais ``target_ref``/``data`` (objets métier bruts).
    # Seuls des champs sûrs et primitifs sortent.
    if hasattr(activity, "kind"):
        def _opt_int(value):
            return int(value) if value is not None else None
        try:
            return {
                "kind": str(getattr(activity, "kind", "")),
                "stage": str(getattr(activity, "stage", "")),
                "target_tx": _opt_int(getattr(activity, "target_tx", None)),
                "target_ty": _opt_int(getattr(activity, "target_ty", None)),
                "target_eid": _opt_int(getattr(activity, "target_eid", None)),
                "started_tick": int(getattr(activity, "started_tick", 0)),
                "last_stage_tick": int(getattr(activity, "last_stage_tick", 0)),
                "reason": str(getattr(activity, "reason", "")),
                "failure_reason": str(getattr(activity, "failure_reason", "")),
            }
        except (TypeError, ValueError):
            return {"kind": str(getattr(activity, "kind", "")),
                    "stage": str(getattr(activity, "stage", ""))}
    if isinstance(activity, dict):
        # Dictionnaire déjà simple : on ne garde que les clés de la liste
        # blanche, et on ne laisse passer que des primitives.
        allowed = ("kind", "stage", "target_tx", "target_ty", "target_eid",
                   "started_tick", "last_stage_tick", "reason",
                   "failure_reason")
        out = {}
        for k in allowed:
            if k in activity:
                v = activity[k]
                out[k] = (v if isinstance(v, (str, int, float, bool))
                          or v is None else str(v))
        return out
    return {"state": str(activity)}
