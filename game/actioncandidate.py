"""ActionCandidate — structure neutre pour variantes d'intention pilotées par perception.

Ne dépend d'aucun module moteur ; utilisable par Sim._set_goal et _execute.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .simulation import Sim
    from .entities import Being


@dataclass(frozen=True)
class ActionCandidate:
    """Candidat d'action issu de la perception/mémoire de l'agent."""
    verb: str                   # "pickup" | "sit" | "follow" | variante existante
    target_kind: str            # "item" | "spot" | "agent" | "terrain"
    target_id: Optional[int]    # eid / item id / None
    tx: int
    ty: int
    estimated_cost: float
    estimated_risk: float
    motive: str                 # "discover" | "social" | "rest" | "economy"


def score_candidate(agent, candidate: ActionCandidate, urgency: float,
                    learned_value: float = 0.0) -> float:
    """Score d'un candidat — formule du plan, learned_value=0.0 pour cette tranche."""
    p = agent.personality
    curiosity = float(p[2]) if len(p) > 2 else 0.0
    sociability = float(p[0]) if len(p) > 0 else 0.0
    caution = float(p[3]) if len(p) > 3 else 0.0
    return (
        float(urgency)
        + 0.25 * curiosity * (candidate.motive == "discover")
        + 0.20 * sociability * (candidate.motive == "social")
        + float(learned_value)
        - float(candidate.estimated_cost)
        - (0.25 + caution) * float(candidate.estimated_risk)
    )


MAX_CANDIDATES = 64        # budget de génération par délibération
_PERCEPT_R = 8             # rayon de perception immédiat, en tuiles
_ITEM_BUCKET_PX = 32       # pas des seaux d'objets (voir Sim._bucket)


def _add(cands: list[ActionCandidate], cand: ActionCandidate) -> bool:
    """Ajoute ``cand`` dans la limite du budget ; False = budget épuisé.

    La clé est celle de ``_dedupe`` : un doublon ne consomme aucun budget
    (il ne fait qu'upgrader un ``target_id=None`` vers la cible réelle),
    le plafond ``MAX_CANDIDATES`` ne compte que des candidats distincts.
    """
    key = (cand.verb, cand.tx, cand.ty, cand.target_kind)
    for i, c in enumerate(cands):
        if (c.verb, c.tx, c.ty, c.target_kind) == key:
            if c.target_id is None and cand.target_id is not None:
                cands[i] = cand
            return True
    if len(cands) >= MAX_CANDIDATES:
        return False
    cands.append(cand)
    return True


def _dedupe(cands: list[ActionCandidate]) -> list[ActionCandidate]:
    """Supprime les doublons sur la clé ``(verb, tx, ty, target_kind)``.

    Garde la première occurrence (ordre stable) ; un doublon pourvu d'un
    ``target_id`` concret remplace à sa place un doublon de mémoire
    (``target_id=None``), la cible réelle faisant foi. Aucune réduction :
    un souvenir sans objet visible reste proposable. Appliqué à la fin de
    ``propose_candidates``, avant tout scoring/triage (filet de sécurité
    : ``_add`` empêche déjà l'entrée des doublons).
    """
    order: list[tuple] = []
    by_key: dict[tuple, ActionCandidate] = {}
    for c in cands:
        key = (c.verb, c.tx, c.ty, c.target_kind)
        seen = by_key.get(key)
        if seen is None:
            by_key[key] = c
            order.append(key)
        elif seen.target_id is None and c.target_id is not None:
            by_key[key] = c
    return [by_key[k] for k in order]


def propose_candidates(sim, a) -> list[ActionCandidate]:
    """Génère des candidats à partir de la perception/mémoire de l'agent.

    Ne consulte QUE ce que l'agent perçoit ou a mémorisé (pas de balayage omniscient).
    Revalider le candidat au moment de l'exécution (la cible peut avoir disparu).
    Sortie dédupliquée (``_dedupe``) et bornée à ``MAX_CANDIDATES``.
    """
    w = sim.w
    cands: list[ActionCandidate] = []
    tx, ty = a.tx, a.ty

    # --- pickup : objets au sol perçus/mémorisés (rayon perception court) ---
    # Mémoire personnelle + clan + universelle
    for kind in ("food", "wood", "stone"):
        pos = a.recall(kind, tx, ty)
        if pos:
            px, py, dist = pos
            px, py = int(px), int(py)
            # w.inb obligatoire : un indice négatif serait lu silencieusement
            # par NumPy (cf. contrôle identique dans classify_candidate).
            if (dist <= a.sense_r_near() and w.inb(px, py)
                    and w.land[py, px] and not w.blocked[py, px]):
                if not _add(cands, ActionCandidate(
                    verb="pickup",
                    target_kind="item",
                    target_id=None,
                    tx=px, ty=py,
                    estimated_cost=0.5 + dist * 0.05,
                    estimated_risk=0.0,
                    motive="economy",
                )):
                    return _dedupe(cands)

    # Items visibles : requête ciblée sur ``sim.item_bucket`` (clés
    # int(coord_px // 32), objets en pixels, TILE=16) — on ne parcourt
    # que les seaux couvrant la fenêtre ±_PERCEPT_R tuiles.
    buckets = getattr(sim, "item_bucket", {}) or {}
    if buckets:
        bx0 = ((tx - _PERCEPT_R) * TILE) // _ITEM_BUCKET_PX
        bx1 = ((tx + _PERCEPT_R + 1) * TILE - 1) // _ITEM_BUCKET_PX
        by0 = ((ty - _PERCEPT_R) * TILE) // _ITEM_BUCKET_PX
        by1 = ((ty + _PERCEPT_R + 1) * TILE - 1) // _ITEM_BUCKET_PX
        items = (it for by in range(by0, by1 + 1)
                  for bx in range(bx0, bx1 + 1)
                  for it in buckets.get((bx, by), ()))
    else:
        # Seaux pas encore construits (avant le 1er Sim._bucket) :
        # retomber sur w.items, strictement équivalent à l'ancien balayage.
        items = iter(w.items)
    for it in items:
        if it.kind != "food" or it.life <= 0:
            continue
        itx, ity = int(it.x // TILE), int(it.y // TILE)
        dx, dy = itx - tx, ity - ty
        if abs(dx) > _PERCEPT_R or abs(dy) > _PERCEPT_R:
            continue
        d = max(abs(dx), abs(dy))
        if not _add(cands, ActionCandidate(
            verb="pickup",
            target_kind="item",
            target_id=id(it),
            tx=itx, ty=ity,
            estimated_cost=0.5 + d * 0.05,
            estimated_risk=0.0,
            motive="economy",
        )):
            return _dedupe(cands)

    # --- sit : spots libres/sûrs proches (rayon 4-6) ---
    if a.energy > 0.2 and a.health > 0.3 and a.emotions[0] < 0.6:
        for r in (3, 5, 7):
            for ddx, ddy in ((0, -r), (r, 0), (0, r), (-r, 0),
                             (r//2, r//2), (-r//2, r//2),
                             (r//2, -r//2), (-r//2, -r//2)):
                sx, sy = tx + ddx, ty + ddy
                if 1 <= sx < w.g - 1 and 1 <= sy < w.g - 1:
                    if w.land[sy, sx] and not w.blocked[sy, sx] and w.shelter[sy, sx] > 0.1:
                        if not _add(cands, ActionCandidate(
                            verb="sit",
                            target_kind="spot",
                            target_id=None,
                            tx=sx, ty=sy,
                            estimated_cost=0.3 + r * 0.08,
                            estimated_risk=0.05,
                            motive="rest",
                        )):
                            return _dedupe(cands)
                        break
            if cands and cands[-1].verb == "sit":
                break

    # --- follow : agent lié proche (amitié/famille) ---
    if a._near_agents:
        for other in a._near_agents:
            # Relation : amis, famille, clan
            if (other.eid == a.partner_id or
                other.eid == a.parent_pere_id or other.eid == a.parent_mere_id or
                a.trust(other.eid) > 0.4):
                d = max(abs(other.tx - tx), abs(other.ty - ty))
                if not _add(cands, ActionCandidate(
                    verb="follow",
                    target_kind="agent",
                    target_id=other.eid,
                    tx=other.tx, ty=other.ty,
                    estimated_cost=0.4 + d * 0.06,
                    estimated_risk=0.1,
                    motive="social",
                )):
                    break

    # --- talk : candidats volontaires (plan §3) ---
    talk_cands = propose_talk_candidates(sim, a)
    cands.extend(talk_cands)

    return _dedupe(cands)


def propose_talk_candidates(sim: "Sim", agent: "Being") -> list[ActionCandidate]:
    """Génère des candidats TALK volontaires (plan §3.4).

    Itère sur les agents proches, vérifie can_talk, choisit un sujet
    via choose_talk_topic, et crée un ActionCandidate avec motive=topic.
    """
    cands: list[ActionCandidate] = []
    if not agent._near_agents:
        return cands
    for other in agent._near_agents:
        if not other.alive:
            continue
        ok, _reason = sim.can_talk(agent, other)
        if not ok:
            continue
        topic = sim.choose_talk_topic(agent, other)
        if topic is None:
            continue
        d = max(abs(other.tx - agent.tx), abs(other.ty - agent.ty))
        if not _add(cands, ActionCandidate(
            verb="talk",
            target_kind="agent",
            target_id=other.eid,
            tx=other.tx, ty=other.ty,
            estimated_cost=0.3 + d * 0.04,
            estimated_risk=0.0,
            motive=topic,
        )):
            break
    return cands


def pick_best_candidate(agent, candidates: list[ActionCandidate],
                        urgency: float) -> Optional[ActionCandidate]:
    """Sélectionne le meilleur candidat selon score_candidate.

    Liste vide (ou ``None``) -> ``None`` ; l'entrée est au plus
    ``MAX_CANDIDATES`` quand elle vient de ``propose_candidates``.
    """
    if not candidates:
        return None
    scored = [(score_candidate(agent, c, urgency), c) for c in candidates]
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]


# ══════════════════════════════════════════════════════════════════════
#  Diagnostic de décision (Phase 1) — observation pure, sans effet de bord
# ══════════════════════════════════════════════════════════════════════
# Ces helpers décrivent ce que l'agent a réellement évalué lors de sa
# délibération. Ils ne modifient jamais le but choisi : le moteur reste
# seul décideur, l'inspecteur ne fait que lire la trace produite ici.

MAX_TRACE = 8                 # au maximum les 8 meilleurs candidats évalués

# États réels d'un candidat évalué.
STATE_SELECTED = "selected"   # retenu (meilleur candidat faisable)
STATE_FEASIBLE = "feasible"   # réalisable mais un autre est meilleur
STATE_REJECTED = "rejected"   # écarté par une contrainte (danger, énergie)
STATE_INVALID = "invalid"     # cible absente / inaccessible
STATE_EXPIRED = "expired"     # souvenir trop ancien

# Raisons courtes et factuelles (libellés affichés tels quels dans l'UI).
REASON_TARGET_MISSING = "cible absente"
REASON_DANGER = "danger trop élevé"
REASON_ENERGY = "énergie insuffisante"
REASON_MEMORY_OLD = "mémoire trop ancienne"
REASON_BLOCKED = "chemin bloqué"
REASON_BETTER = "autre candidat meilleur"

# Seuils de classification (volontairement alignés sur le moteur).
DANGER_REJECT = 0.45          # belief_places au-delà -> rejeté
RISK_REJECT = 0.50            # risque estimé au-delà -> rejeté
ENERGY_MIN = 0.12             # énergie en deçà -> déplacement rejeté
STALE_FORCE = 0.30            # force mnésique en deçà -> souvenir périmé

# verb -> action moteur, pour retrouver la liste noire ``failed_targets``.
_VERB_ACTION = {"pickup": "TAKE", "sit": "REST", "follow": "SOCIAL"}


def _verb_action(verb: str):
    """Action moteur correspondant à un verb (import différé, sans cycle)."""
    name = _VERB_ACTION.get(verb)
    if name is None:
        return None
    try:
        from . import brain_api
        return getattr(brain_api, name, None)
    except Exception:
        return None


def _memory_stale(agent, tx: int, ty: int) -> bool:
    """Un souvenir d'objet en (tx,ty) est-il devenu trop faible ?

    Consultation bornée à la mémoire personnelle de l'agent (jamais un
    balayage du monde) : quelques dizaines d'entrées au plus.
    """
    for cat in ("food", "wood", "stone"):
        for mx, my, force in agent.seen.get(cat, ()):
            if int(mx) == int(tx) and int(my) == int(ty):
                return float(force) < STALE_FORCE
    return False


def classify_candidate(sim, agent, cand: ActionCandidate) -> tuple[str, Optional[str]]:
    """État réel + raison courte d'un candidat, par contrôles localisés.

    N'inspecte que la tuile visée et la cible du candidat : aucun balayage
    global du monde. Retourne ``(state, reason)`` où ``reason`` est ``None``
    quand aucune raison factuelle ne s'applique.
    """
    w = sim.w
    tx, ty = int(cand.tx), int(cand.ty)

    if not (0 <= tx < w.g and 0 <= ty < w.g):
        return STATE_INVALID, REASON_TARGET_MISSING

    act = _verb_action(cand.verb)
    if act is not None and sim.target_is_blocked(agent, act, tx, ty):
        return STATE_INVALID, REASON_BLOCKED

    if bool(w.blocked[ty, tx]):
        return STATE_INVALID, REASON_BLOCKED
    if not bool(w.land[ty, tx]):
        return STATE_INVALID, REASON_TARGET_MISSING

    if cand.target_kind == "agent" and cand.target_id is not None:
        other = sim._by_eid(cand.target_id)
        if other is None or not getattr(other, "alive", False):
            return STATE_INVALID, REASON_TARGET_MISSING

    if cand.verb == "pickup" and cand.target_id is None and _memory_stale(agent, tx, ty):
        return STATE_EXPIRED, REASON_MEMORY_OLD

    danger = float(agent.belief_places.get((tx // 8, ty // 8), 0.0))
    if danger > DANGER_REJECT or float(cand.estimated_risk) > RISK_REJECT:
        return STATE_REJECTED, REASON_DANGER

    if cand.verb != "sit" and float(agent.energy) <= ENERGY_MIN:
        return STATE_REJECTED, REASON_ENERGY

    return STATE_FEASIBLE, None


def evaluate_candidates(sim, agent, urgency: float = 0.0,
                        limit: int = MAX_TRACE) -> list[dict]:
    """Trace de diagnostic : les ``limit`` meilleurs candidats évalués.

    Génère les candidats (perception/mémoire de l'agent uniquement), les
    score, détermine leur état réel, marque le meilleur faisable comme
    ``selected`` et renvoie une liste de dictionnaires simples, triée
    (``selected`` d'abord, puis score décroissant). Aucune mutation de
    l'agent ni du monde : le but choisi par le moteur reste inchangé.
    """
    candidates = propose_candidates(sim, agent)
    ax, ay = int(agent.tx), int(agent.ty)
    traced: list[dict] = []
    for cand in candidates:
        state, reason = classify_candidate(sim, agent, cand)
        traced.append({
            "verb": str(cand.verb),
            "target_kind": str(cand.target_kind),
            "target_id": (int(cand.target_id)
                          if cand.target_id is not None else None),
            "tx": int(cand.tx),
            "ty": int(cand.ty),
            "distance": int(max(abs(int(cand.tx) - ax), abs(int(cand.ty) - ay))),
            "estimated_cost": float(cand.estimated_cost),
            "estimated_risk": float(cand.estimated_risk),
            "motive": str(cand.motive),
            "score": float(score_candidate(agent, cand, urgency)),
            "state": state,
            "reason": reason,
        })

    feasible = [t for t in traced if t["state"] == STATE_FEASIBLE]
    if feasible:
        best = max(feasible, key=lambda t: t["score"])
        best["state"] = STATE_SELECTED
        best["reason"] = None
        for t in feasible:
            if t is not best and t["reason"] is None:
                t["reason"] = REASON_BETTER

    traced.sort(key=lambda t: (0 if t["state"] == STATE_SELECTED else 1,
                               -t["score"]))
    return traced[:limit]


# Import différé pour éviter cycle
from game.config import TILE