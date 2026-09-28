"""Simulation — le contrat moteur.

  1. le monde ne donne JAMAIS de mission
  2. le cerveau ne modifie pas la realite : il DEMANDE une intention
  3. le monde verifie la faisabilite (affordances, capacites physiques)
  4. toute action a des consequences
  5. les consequences deviennent experience -> recompense -> apprentissage

L'etre percoit (sens limités, jour/nuit, attention), MEMORISE (et oublie),
arbitre (reseau + personnalite + emotions + croyances + habitudes + risque),
agit (14 primitives composables), apprend (REINFORCE), grandit (enfant ->
adulte -> ancien), s'allie, fonde une famille, transmet (culture), et meurt
en laissant une reputation.
"""
import math
import time
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from typing import Any, Optional

import numpy as np

from .brain_api import (ATTACK, BUILD, DRINK, DROP, EAT, EXPLORE, FLEE, GIVE,
                      HARVEST, MARK, N_IN, N_OUT, REST, SLEEP, SOCIAL, TAKE,
                      TALK, ACTION_NAMES_EXP as ACTION_NAMES, ACTION_TRAIT_EXP as ACTION_TRAIT)
from .brain import Brain
from .brain_schema import INPUT
from .brain import (IMMEDIAT, PRUDENT, ECONOMIQUE, COOPERATIF, EXPLORATION, DEFENSIF,
                      SOI, NOURRITURE, EAU, BOIS, PIERRE, ABRI, DEPOT_CHANTIER, ETRE_VIVANT)
from .clock import Clock
from .config import (CLAN_COLORS, GRID, MAX_POP, MAX_SHEEP, TILE, WORLD_PX,
                      DEFAULT_SPAWN_AGE_TICKS, TICKS_PER_YEAR, AGE_ELDER_TICKS,
                      AGE_MAX_NATURAL_DEATH_TICKS, DAY_TICKS,
                      HUNGER_RATE, THIRST_RATE, SLEEP_RATE_D, SLEEP_RATE_N,
                      E_DRAIN, MOVE_DRAIN, REST_GAIN, SLEEP_GAIN, SHELTER_BONUS,
                      STARVE_HP, THIRST_HP, LOWE_HP, INV_CAP,
                      ATTACK_DMG, ATTACK_DMG_TOOL, WORK_TICKS, PERCEPT_CELLS,
                      JOURNAL_MAXLEN, MONSTER_KINDS, MAX_MONSTERS, MAX_SHEEP,
                      THINK_INTERVAL, CANDIDATE_INTERVAL, PLAN_INTERVAL,
                      RESOURCE_UPDATE_INTERVAL, REPUTATION_INTERVAL, SOCIETY_INTERVAL)
from .entities import Being, Sheep, Monster, ClanKnowledge
from .world import Item
from .universal_knowledge import UniversalKnowledge
from .academy import Academy
from .lab import LabRecorder
from .history import WorldHistory
from .construction import ConstructionSite, blueprint_from_name
from .actioncandidate import (ActionCandidate, propose_candidates,
                               pick_best_candidate, score_candidate,
                               evaluate_candidates, propose_talk_candidates)
from .perfmetrics import PerfMetrics
from .resourcesites import discover_resource_sites_near

MAT_AIDS = {"bois": "item_wood", "pierre": "stone_res", "or": "gold_pile"}

# ── Part A: TALK VOLONTAIRE constants ──────────────────────────────
TALK_DISTANCE = 5
TALK_COOLDOWN = 60
TALK_ENERGY_COST = 0.002
KNOWLEDGE_SHARE_FACTOR = 0.65
MAX_SHARED_MEMORY_CONFIDENCE = 0.75

# ── Part F: Message templates (deterministic, English) ─────
MESSAGE_TEMPLATES = {
    "food_location": "I found food to the {direction}.",
    "water_location": "Water is {direction} of here.",
    "danger_warning": "Danger is {direction} of here.",
    "need_help": "I need help.",
    "follow_request": "Follow me.",
    "greeting": "Hello.",
    "idle_chat": "Nice weather.",
}


def relative_direction(speaker, tx, ty):
    dx, dy = int(tx) - speaker.tx, int(ty) - speaker.ty
    if abs(dx) >= abs(dy):
        return "east" if dx > 0 else "west"
    return "south" if dy > 0 else "north"


@dataclass
class ActivityState:
    """État d'une activité à plusieurs étapes (plan §5)."""
    kind: str
    stage: str
    target_tx: int | None = None
    target_ty: int | None = None
    target_eid: int | None = None
    target_ref: Any = None
    started_tick: int = 0
    last_stage_tick: int = 0
    reason: str = ""
    failure_reason: str = ""
    data: dict = field(default_factory=dict)


class Sim:
    def __init__(self, world, am, seed=7, blank_world=False):
        self.w = world
        self.am = am
        self.seed = int(seed)
        self.rng = np.random.default_rng(seed)
        self.clock = Clock(np.random.default_rng(seed + 1))
        self.agents: list[Being] = []
        self.sheep: list[Sheep] = []
        self.monsters: list[Monster] = []
        self.effects: list[dict] = []
        self.sounds: deque = deque(maxlen=40)
        self.next_eid = 1
        self.paused = True
        self.speed = 2
        self.blank_world = bool(blank_world)
        self.grid_bucket = {}
        self.item_bucket = {}
        self.food_cells = {}
        self._entity_cells = {}
        self.stats = dict(births=0, deaths=0, builds=0, villages=0, attacks=0,
                          gives=0, takes=0, talks=0, harvests=0, tool_found=0,
                          explored=0, drinks=0, sleeps=0, fires=0)
        # Lot M : diagnostics comportementaux
        self.debug_action_counts = {}
        self.debug_failure_counts = {"path": 0, "feasible": 0, "affordance": 0}
        self.debug_anima_counts = {"episodes": 0, "intentions": 0, "plans": 0}
        self.journal = deque(maxlen=JOURNAL_MAXLEN)
        #: Habitants décédés récemment. ``tick()`` purge les cadavres de
        #: ``agents`` : sans ce tampon, l'UI ne peut plus proposer « Tous ».
        self.deceased = deque(maxlen=200)
        self.society = []
        self.pop_hist = deque(maxlen=220)
        self._recent_attacks = deque(maxlen=400)
        self._village_pts = []
        self._last_war_log = -9999
        self._dominance = {}
        self._trade = {}
        self._sens = np.zeros(N_IN, dtype=np.float64)
        self.selected = None
        self.clan_knowledge = ClanKnowledge()
        self.universal_knowledge = UniversalKnowledge(omniscient=False)
        self.academy = Academy()
        self.lab = LabRecorder()
        self.history = WorldHistory()
        from .social_memory import SocialMemory
        self.social_memory = SocialMemory()
        # ── Lot F.1 : paramètres Studio actifs ──
        from .studio_parameters import DEFAULT_RUNTIME
        self.runtime = dict(DEFAULT_RUNTIME)
        self.parameters = {}
        self.parameter_store = None
        # ── Lot G.2 : quartiers et zones prédateurs ──
        self.districts = {}
        self.predator_zones = {}

        # Performance metrics (Phase 1)
        self.perf = PerfMetrics(window=120)

        # Population revision for UI caching
        self.population_revision = 0

        # Phase 1: activity reasons counter
        self.activity_reasons = Counter()

        # Phase 2: compteurs d'anomalies (erreurs avalées, récupérations
        # NaN/Inf du cerveau, perceptions invalides, replis courts)
        self.metrics = defaultdict(int)
        # Anti-passivity: relances d'exploration dediees (pression de vie)
        self.metrics["lifedrive_explore_start"] = 0

    # ── Phase 2: Fréquences différenciées ───
    THINK_INTERVAL = THINK_INTERVAL
    CANDIDATE_INTERVAL = CANDIDATE_INTERVAL
    PLAN_INTERVAL = PLAN_INTERVAL

    def agent_should_think(self, agent) -> bool:
        """Détermine si l'agent doit réfléchir ce tick (staggered par eid).

        - Les agents urgents (faim/énergie/émotions critiques) pensent immédiatement.
        - Les agents calmes ne pensent que toutes les 20 ticks (staggered par eid),
          ce qui réduit la charge CPU tout en maintenant une périodicité répartie.
        """
        period = max(20, int(getattr(agent.brain, "te", THINK_INTERVAL)))

        urgent = (
            agent.hunger > 0.90
            or agent.needs[2] > 0.90
            or agent.energy < 0.10
            or agent.emotions[0] > 0.75
            or agent.pain > 0.65
        )

        if urgent:
            return True

        return (self.w.tick + int(agent.eid)) % period == 0

    def _should_generate_candidates(self, agent) -> bool:
        """Détermine si on doit générer des candidats pour cet agent."""
        return (self.w.tick + int(agent.eid)) % self.CANDIDATE_INTERVAL == 0

    def _should_generate_plans(self, agent) -> bool:
        """Détermine si on doit générer des plans pour cet agent."""
        return (self.w.tick + int(agent.eid)) % self.PLAN_INTERVAL == 0

    def _invalidate_agent_cache(self, agent):
        """Invalide le cache de l'agent après un événement significatif."""
        agent.cached_plans = None
        agent.cached_plans_tick = -1
        agent.cached_candidates = None
        agent.cached_candidates_tick = -1

    # ------------------------------------------------------------------ journal
    def log(self, text, color=None, cat="world"):
        """cat: id du registre JOURNAL_CATEGORIES (world|life|family|…)."""
        if self.journal and self.journal[-1][1] == text and self.w.tick - self.journal[-1][0] < 900:
            t0, tx, c, k, n = self.journal[-1]
            self.journal[-1] = (self.w.tick, tx, c, k, n + 1)
            return
        self.journal.append((self.w.tick, text, color, cat, 1))

    def emit_sound(self, x, y, kind, intensity=1.0):
        self.sounds.append((x, y, kind, intensity, self.w.tick))

    # ═══════════════════════════════════════════════════════════════════════
    # PART A: TALK VOLONTAIRE (plan §3)
    # ═══════════════════════════════════════════════════════════════════════
    def can_talk(self, speaker: Being, listener: Being) -> tuple[bool, str]:
        """Vérifie si speaker peut parler à listener (plan §5.4).

        Boucle locale uniquement : appel public utilisé par les candidats
        TALK (``nearagents`` déjà borné). Raisons stables, traduites en UI.
        """
        if speaker is None or listener is None:
            return False, "missing_agent"
        if not speaker.alive or not listener.alive:
            return False, "dead_agent"
        if speaker.eid == listener.eid:
            return False, "self_target"
        dist = max(abs(speaker.tx - listener.tx), abs(speaker.ty - listener.ty))
        if dist > TALK_DISTANCE:
            return False, "too_far"
        last_talk = speaker.talk_cd.get(listener.eid, -10000)
        if self.w.tick - last_talk < TALK_COOLDOWN:
            return False, "communication_cooldown"
        if float(speaker.energy) <= TALK_ENERGY_COST:
            return False, "not_enough_energy"
        return True, ""

    def choose_talk_topic(self, speaker: Being, listener: Being) -> str | None:
        """Choisit un sujet de conversation selon le contexte (plan §3.5)."""
        # 1. listener a faim et speaker connait réellement de la nourriture
        if float(listener.hunger) > 0.65:
            if self.best_shareable_memory(speaker, "food") is not None:
                return "food_location"
        # 2. listener a soif et speaker connait réellement de l'eau
        if float(listener.needs[2]) > 0.65:
            if self.best_shareable_memory(speaker, "water") is not None:
                return "water_location"
        # 3. danger proche
        if speaker._near_monsters:
            return "danger_warning"
        # 4. listener en détresse réelle (faim, blessure, soif)
        if (float(listener.health) < 0.45 or float(listener.hunger) > 0.82
                or float(listener.needs[2]) > 0.82):
            return "need_help"
        # 5. speaker en expédition -> follow_request
        if speaker.activity and speaker.activity.kind in {"food_expedition", "explore_region"}:
            return "follow_request"
        # 6. interaction légère : sociable et pas effrayé -> greeting
        if float(speaker.personality[0]) > 0.65 and float(speaker.emotions[0]) < 0.55:
            return "greeting"
        # 7. interaction basique : proximité + pas de conflit -> idle_chat
        dist = max(abs(speaker.tx - listener.tx), abs(speaker.ty - listener.ty))
        if dist <= 5 and float(speaker.emotions[0]) < 0.7:
            return "idle_chat"
        return None

    def apply_communication(self, speaker: Being, listener: Being,
                            topic: str) -> dict | None:
        """Applique l'effet de la communication selon le sujet (plan §3.7).

        Retourne le payload RÉELLEMENT transmis (primitives seulement) après
        succès, ou ``None`` si l'effet n'a pas été appliqué. Le payload vient
        de l'effet lui-même : aucune mémoire n'est relue une deuxième fois
        après modification, et un échec ne peut jamais être présenté comme un
        message reçu.
        """
        if topic == "food_location":
            mem = self.best_shareable_memory(speaker, "food")
            if mem:
                return self.receive_shared_place(listener, mem, "food", speaker.eid)
        elif topic == "water_location":
            mem = self.best_shareable_memory(speaker, "water")
            if mem:
                return self.receive_shared_place(listener, mem, "water", speaker.eid)
        elif topic == "danger_warning":
            mem = self.best_shareable_danger(speaker)
            if mem:
                return self.receive_danger_warning(listener, mem, speaker.eid)
        elif topic == "need_help":
            return self.receive_help_request(listener, speaker)
        elif topic == "follow_request":
            return self.receive_follow_request(listener, speaker.eid, speaker.activity)
        elif topic == "greeting":
            return self.apply_greeting(speaker, listener)
        elif topic == "idle_chat":
            return self.apply_idle_chat(speaker, listener)
        return None

    def best_shareable_memory(self, agent: Being, category: str) -> tuple[int, int, float] | None:
        """Meilleur souvenir partageable pour une catégorie (plan §5.7).

        Préfère ``place_memories`` (confiance >= 0.35), repli sur ``recall``
        pour compatibilité. Retour tuple ``(tx, ty, confidence)`` ; le dict
        complet reste lisible via ``place_memories`` pour le partage.
        """
        rows = []
        for mem in getattr(agent, "place_memories", {}).values():
            if not isinstance(mem, dict):
                continue
            if mem.get("category") != category:
                continue
            if float(mem.get("confidence", 0.0)) < 0.35:
                continue
            rows.append(mem)
        if rows:
            rows.sort(key=lambda m: (
                float(m.get("confidence", 0.0))
                + 0.25 * float(m.get("estimated_amount", 0.0))
                - 0.25 * float(m.get("estimated_danger", 0.0))
            ), reverse=True)
            best = rows[0]
            return (int(best["tx"]), int(best["ty"]),
                    float(best.get("confidence", 0.5)))
        mem = agent.recall(category, agent.tx, agent.ty)
        if mem and mem[2] < 100:
            return mem
        return None

    def _shareable_memory_dict(self, agent: Being, category: str) -> dict | None:
        """Dict complet du meilleur souvenir partageable (pour le partage)."""
        rows = []
        for mem in getattr(agent, "place_memories", {}).values():
            if not isinstance(mem, dict):
                continue
            if mem.get("category") != category:
                continue
            if float(mem.get("confidence", 0.0)) < 0.35:
                continue
            rows.append(mem)
        if rows:
            rows.sort(key=lambda m: (
                float(m.get("confidence", 0.0))
                + 0.25 * float(m.get("estimated_amount", 0.0))
                - 0.25 * float(m.get("estimated_danger", 0.0))
            ), reverse=True)
            return rows[0]
        mem = agent.recall(category, agent.tx, agent.ty)
        if mem and mem[2] < 100:
            # Souvenir ancien (seen) : ni source ni date de vérification
            # connues. On ne fabrique ni « observation directe » ni tick de
            # vérification courant — la confiance reste neutre (0.50).
            return {
                "category": category,
                "tx": int(mem[0]),
                "ty": int(mem[1]),
                "confidence": 0.50,
                "estimated_amount": 0.50,
                "estimated_danger": 0.0,
                "last_verified_tick": None,
                "source": "legacy_memory",
            }
        return None

    def best_shareable_danger(self, agent: Being) -> tuple[int, int, float] | None:
        """Meilleur souvenir de danger partageable."""
        if not agent._near_monsters:
            return None
        m = min(agent._near_monsters, key=lambda x: max(abs(x.tx - agent.tx), abs(x.ty - agent.ty)))
        return (m.tx, m.ty, 0.8)

    def receive_shared_place(self, listener: Being, mem: tuple[int, int, float],
                             category: str, from_eid: int) -> dict | None:
        """Reçoit un lieu partagé (plan §6.1) : confiance réduite, source sociale.

        Retourne le payload RÉELLEMENT transmis (confiance réellement
        reçue + provenance) ou ``None`` si la transmission échoue.
        """
        tx, ty, conf = mem
        try:
            trust = listener.anima_social_score(from_eid)
        except Exception:
            trust = listener.trust(from_eid)
        trust01 = max(0.0, min(1.0, 0.5 + 0.5 * float(trust)))
        received_conf = min(
            MAX_SHARED_MEMORY_CONFIDENCE,
            float(conf) * KNOWLEDGE_SHARE_FACTOR * (0.50 + 0.50 * trust01),
        )
        if received_conf < 0.2:
            return None
        # Compat seen + mémoire typée sociale (quantité perçue à -20%).
        listener.remember(category, tx, ty)
        amount = 0.5
        danger = 0.0
        origin_source = ""
        try:
            _d = self._shareable_memory_dict(
                self._by_eid(from_eid), category) if hasattr(self, "_by_eid") else None
        except Exception:
            _d = None
        if isinstance(_d, dict):
            amount = float(_d.get("estimated_amount", 0.5))
            danger = float(_d.get("estimated_danger", 0.0))
            # Provenance d'origine : métadonnée facultative, sans lui donner
            # le statut d'observation locale (la mémoire reçue reste sociale).
            origin_source = str(_d.get("source", ""))
        try:
            listener.remember_place(
                category, tx, ty, self.w.tick,
                confidence=received_conf,
                estimated_amount=amount * 0.80,
                estimated_danger=danger,
                source="social",
            )
        except Exception:
            pass
        try:
            self.adjust_social_interaction(
                self._by_eid(from_eid), listener, trust=0.02, affection=0.02)
        except Exception:
            pass
        self.lab.event(self.w.tick, "knowledge_shared",
                       from_eid=from_eid, to_eid=listener.eid,
                       category=category, tx=tx, ty=ty, confidence=received_conf)
        # Payload réellement reçu : confiance effective (après réduction)
        # et provenance — jamais une donnée relue après modification.
        return {
            "category": str(category),
            "tx": int(tx),
            "ty": int(ty),
            "confidence_received": float(received_conf),
            "source": "social",
            "origin_source": origin_source,
            "from_eid": int(from_eid),
        }

    def receive_danger_warning(self, listener: Being, mem: tuple[int, int, float],
                               from_eid: int) -> dict | None:
        """Reçoit un avertissement de danger (plan §6.2) : croyance réelle + prudence.

        Retourne le payload transmis (niveau réellement appliqué) ou ``None``.
        """
        tx, ty, conf = mem
        trust = listener.trust(from_eid)
        effective_conf = conf * KNOWLEDGE_SHARE_FACTOR * max(0.3, 0.5 + trust * 0.5)
        if effective_conf < 0.2:
            return None
        level = max(0.0, min(1.0, float(effective_conf) * 0.65 + 0.20))
        cx, cy = int(tx) // 8, int(ty) // 8
        prev = float(listener.belief_places.get((cx, cy), 0.0))
        listener.belief_places[(cx, cy)] = max(prev, level)
        listener.emotions[0] = min(1.0, listener.emotions[0] + 0.15)
        try:
            listener.anima_update_social_belief(
                from_eid, int(self.w.tick),
                reliability_delta=0.01, confidence_delta=0.02)
        except Exception:
            pass
        self.lab.event(self.w.tick, "danger_warning_received",
                       from_eid=from_eid, to_eid=listener.eid,
                       tx=tx, ty=ty, confidence=effective_conf)
        return {
            "kind": "danger_warning",
            "tx": int(tx),
            "ty": int(ty),
            "level": float(level),
            "confidence_received": float(effective_conf),
            "source": "social",
            "from_eid": int(from_eid),
        }

    def receive_help_request(self, listener: Being,
                             speaker) -> dict | None:
        """Reçoit une demande d'aide (plan §6.3) : signal social réel, pas de mission auto.

        Retourne le payload transmis (les données réelles de la demande) ou
        ``None``. N'écrit jamais ``listener.lastheard`` : le message canonique
        est publié par ``do_talk`` après succès.
        """
        from_eid = speaker.eid if hasattr(speaker, "eid") else int(speaker)
        trust = listener.trust(from_eid)
        if trust < -0.2:
            return None
        if hasattr(speaker, "hunger"):
            request = {
                "kind": "need_help",
                "requester_eid": int(from_eid),
                "tx": int(speaker.tx),
                "ty": int(speaker.ty),
                "hunger": float(speaker.hunger),
                "thirst": float(speaker.needs[2]),
                "health": float(speaker.health),
                "danger": float(speaker.emotions[0]),
                "tick": int(self.w.tick),
            }
            # Pas d'écriture de listener.lastheard ici : le message canonique
            # est publié une seule fois par do_talk(), après succès.
            try:
                listener.observed_actions.append({
                    "action": "need_help",
                    "reward": 0.0,
                    "tick": int(self.w.tick),
                })
            except Exception:
                pass
        else:
            request = {
                "kind": "need_help",
                "requester_eid": int(from_eid),
                "tick": int(self.w.tick),
            }
        listener.emotions[5] = min(1.0, listener.emotions[5] + 0.1)  # surprise
        listener.emotions[7] = min(1.0, listener.emotions[7] + 0.05)  # affection
        self.lab.event(self.w.tick, "help_request_received",
                       from_eid=from_eid, to_eid=listener.eid, trust=trust)
        return dict(request)

    def apply_greeting(self, speaker: Being, listener: Being) -> dict:
        """Salutation faible (plan §6.4) : le cooldown évite le farm relationnel."""
        self.adjust_social_interaction(speaker, listener, trust=0.02, affection=0.03)
        try:
            speaker.emotions[1] = min(1.0, speaker.emotions[1] + 0.03)
            listener.emotions[1] = min(1.0, listener.emotions[1] + 0.02)
        except Exception:
            pass
        # Sujet sans cible : payload minimal (jamais d'objet métier brut).
        return {"kind": "greeting"}

    def apply_idle_chat(self, speaker: Being, listener: Being) -> dict:
        """Bavardage léger : interaction sociale de base sans contenu spécifique."""
        self.adjust_social_interaction(speaker, listener, trust=0.03, affection=0.03)
        try:
            speaker.emotions[1] = min(1.0, speaker.emotions[1] + 0.02)
            listener.emotions[1] = min(1.0, listener.emotions[1] + 0.01)
        except Exception:
            pass
        return {"kind": "idle_chat"}

    def receive_follow_request(self, listener: Being, from_eid: int,
                               activity: ActivityState | None) -> dict | None:
        """Reçoit une demande de suivre. Payload transmis ou ``None``."""
        trust = listener.trust(from_eid)
        if trust < 0.1:
            return None
        if activity and activity.target_tx is not None and activity.target_ty is not None:
            listener.remember("agent", activity.target_tx, activity.target_ty)
            self.lab.event(self.w.tick, "follow_request_received",
                           from_eid=from_eid, to_eid=listener.eid,
                           target_tx=activity.target_tx, target_ty=activity.target_ty)
            return {
                "kind": "follow_request",
                "target_tx": int(activity.target_tx),
                "target_ty": int(activity.target_ty),
                "from_eid": int(from_eid),
            }
        return None

    def adjust_social_interaction(self, a: Being, b: Being,
                                    trust: float = 0.0, affection: float = 0.0) -> None:
        """Ajuste la relation sociale bidirectionnelle."""
        r1 = a.rel.setdefault(b.eid, [0.0, 0.0])
        r2 = b.rel.setdefault(a.eid, [0.0, 0.0])
        r1[0] = min(1.0, r1[0] + trust)
        r2[0] = min(1.0, r2[0] + trust)
        r1[1] = min(1.0, r1[1] + affection)
        r2[1] = min(1.0, r2[1] + affection)

    def record_betrayal(self, betrayer: Being, victim: Being, betrayal_type: str, severity: float = 0.5) -> None:
        """Enregistre une trahison/vol/violence et applique les penalites relationnelles.

        Types de trahison:
        - "theft": vol
        - "violence": agression physique
        - "betrayal": trahison de confiance (promesse rompue, mensonge)
        - "abandon": abandon en danger
        """
        severity = min(1.0, max(0.0, severity))

        # Penalites de confiance/affection selon la gravite
        trust_loss = min(0.8, 0.2 + severity * 0.6)
        affection_loss = min(0.7, 0.15 + severity * 0.5)

        betrayer.rel.setdefault(victim.eid, [0.0, 0.0])[0] = max(-1.0,
            betrayer.rel.setdefault(victim.eid, [0.0, 0.0])[0] - trust_loss)
        victim.rel.setdefault(betrayer.eid, [0.0, 0.0])[0] = max(-1.0,
            victim.rel.setdefault(betrayer.eid, [0.0, 0.0])[0] - trust_loss)

        betrayer.rel.setdefault(victim.eid, [0.0, 0.0])[1] = max(0.0,
            betrayer.rel.setdefault(victim.eid, [0.0, 0.0])[1] - affection_loss)
        victim.rel.setdefault(betrayer.eid, [0.0, 0.0])[1] = max(0.0,
            victim.rel.setdefault(betrayer.eid, [0.0, 0.0])[1] - affection_loss)

        # Emotions
        victim.emotions[2] = min(1.0, victim.emotions[2] + 0.4 * severity)  # colere
        victim.emotions[0] = min(1.0, victim.emotions[0] + 0.3 * severity)  # peur

        # Trauma pour la victime
        victim.anima["trauma"]["betrayal"] = min(1.0,
            victim.anima["trauma"].get("betrayal", 0.0) + severity * 0.3)

        # Reputation
        betrayer.rep -= int(2 * severity)

        # Anima: episode de trahison
        self._record_anima(victim, f"betrayal_{betrayal_type}", (victim.tx, victim.ty),
                           actors=[betrayer.eid, victim.eid],
                           action=betrayal_type, outcome="betrayed",
                           social_impact=-0.5 * severity)
        self._record_anima(betrayer, f"betrayal_{betrayal_type}", (betrayer.tx, betrayer.ty),
                           actors=[betrayer.eid, victim.eid],
                           action=betrayal_type, outcome="betrayer",
                           social_impact=-0.3 * severity)

        # Log
        self.log(f"{victim.name} trahi par {betrayer.name} : {betrayal_type}.",
                 (228, 98, 98), "social")

    def do_talk(self, speaker: Being, listener: Being) -> bool:
        """Exécute l'action TALK (plan §5.8) : volontaire, bornée, journalisée."""
        ok, reason = self.can_talk(speaker, listener)
        if not ok:
            self.record_activity_failure(speaker, "talk", reason)
            try:
                speaker.last_activity_result = {
                    "kind": "talk", "outcome": "failed", "reason": str(reason)}
            except Exception:
                pass
            return False
        topic = self.choose_talk_topic(speaker, listener)
        if topic is None:
            self.record_activity_failure(speaker, "talk",
                                         "communication_has_no_real_payload")
            try:
                speaker.last_activity_result = {
                    "kind": "talk", "outcome": "failed",
                    "reason": "communication_has_no_real_payload"}
            except Exception:
                pass
            return False
        payload = self.apply_communication(speaker, listener, topic)
        if payload is None:
            self.record_activity_failure(speaker, "talk",
                                         "communication_has_no_real_payload")
            try:
                speaker.last_activity_result = {
                    "kind": "talk", "outcome": "failed",
                    "reason": "communication_has_no_real_payload"}
            except Exception:
                pass
            return False
        speaker.energy = max(0.0, float(speaker.energy) - TALK_ENERGY_COST)
        speaker.talk_cd[listener.eid] = self.w.tick
        listener.talk_cd[speaker.eid] = self.w.tick
        # UN seul événement canonique, construit à partir du payload
        # réellement transmis (renvoyé par apply_communication) : les deux
        # côtés publient exactement la même chose, après succès.
        event = {
            "kind": "talk",
            "topic": str(topic),
            "speaker_eid": int(speaker.eid),
            "speaker_name": str(speaker.name),
            "listener_eid": int(listener.eid),
            "listener_name": str(listener.name),
            "payload": dict(payload),
            "tick": int(self.w.tick),
            "result": "received",
            "language_source": "semantic",
            "token": None,
        }
        event["template"] = MESSAGE_TEMPLATES.get(
            topic, "{topic}").format(
                direction=relative_direction(speaker,
                    event.get("payload", {}).get("tx", speaker.tx),
                    event.get("payload", {}).get("ty", speaker.ty))
                if topic in MESSAGE_TEMPLATES else topic)
        speaker.lastsaid = dict(event)
        listener.lastheard = dict(event)
        self.emit_sound(speaker.x, speaker.y, "voice", 0.6)
        self.effects.append({"kind": "talk", "x": speaker.x, "y": speaker.y,
                             "t0": self.w.tick, "ttl": 20})
        speaker.state = "talk"
        self.stats["talks"] += 1
        self.log(f"{speaker.name} parle à {listener.name} : {topic}.",
                 (196, 100, 162), "social")
        try:
            self.social_memory.record(listener.eid, speaker.eid, "help", 0.05,
                                      int(self.w.tick))
        except Exception:
            pass
        speaker.skills[3] = min(1.0, speaker.skills[3] + 0.01)
        self._reward(speaker, 0.05)
        speaker.record_meaningful(self.w.tick, "talk")
        return True

    def record_activity_failure(self, agent: Being, activity: str, reason: str) -> None:
        """Enregistre un échec d'activité pour apprentissage.

        Point central d'enregistrement d'échec : la vérité « dernier échec »
        est écrite ici, au moment où il se produit (et non déduite au rendu
        depuis ``failed_targets``). N'efface jamais le dernier choix.
        """
        self.metrics[f"activity_fail_{activity}"] += 1
        self.activity_reasons[f"{activity}:{reason}"] += 1
        try:
            agent.last_failure_reason = str(reason)
            agent.last_failure_tick = int(self.w.tick)
        except AttributeError:
            pass
        self._reward(agent, -0.02)

    # ═══════════════════════════════════════════════════════════════════════
    # PART B: ActivityState infrastructure + FOOD_EXPEDITION (plan §5, §6)
    # ═══════════════════════════════════════════════════════════════════════

    def start_activity(self, agent: Being, kind: str, stage: str, **kwargs) -> ActivityState:
        """Démarre une nouvelle activité (plan §5)."""
        act = ActivityState(
            kind=kind,
            stage=stage,
            target_tx=kwargs.get("target_tx"),
            target_ty=kwargs.get("target_ty"),
            target_eid=kwargs.get("target_eid"),
            target_ref=kwargs.get("target_ref"),
            started_tick=self.w.tick,
            last_stage_tick=self.w.tick,
            reason=kwargs.get("reason", ""),
            data=kwargs.get("data", {}),
        )
        agent.activity = act
        agent.goal = None  # l'activité gère ses propres buts
        return act

    def fail_activity(self, agent: Being, reason: str) -> None:
        """Termine l'activité en échec (plan §5).

        Point central d'échec des activités : la vérité « dernier échec » y
        est écrite au moment où il se produit (n'efface pas le dernier
        choix de sélection).
        """
        if agent.activity:
            agent.activity.failure_reason = reason
            self.record_activity_outcome(agent, agent.activity.kind, "failed", -0.1)
            agent.last_activity_result = {"kind": agent.activity.kind, "outcome": "failed", "reason": reason}
            try:
                agent.last_failure_reason = str(reason)
                agent.last_failure_tick = int(self.w.tick)
            except AttributeError:
                pass
            agent.activity = None
            agent.goal = None

    def finish_activity(self, agent: Being, outcome: str = "success", reward: float = 0.1) -> None:
        """Termine l'activité avec succès (plan §5)."""
        if agent.activity:
            kind = agent.activity.kind
            agent.record_meaningful(self.w.tick, kind)
            self.record_activity_outcome(agent, kind, outcome, reward)
            agent.last_activity_result = {"kind": kind, "outcome": outcome, "reward": reward}
            agent.activity = None
            agent.goal = None

    def should_interrupt_activity(self, agent: Being, activity: ActivityState) -> str | None:
        """Vérifie si l'activité doit être interrompue (plan §5)."""
        if not agent.alive or agent.health <= 0:
            return "mort"
        if agent.stuck >= 20:
            return "bloque"
        if agent.energy <= 0.06:
            return "energie_critique"
        if agent.needs[2] >= 0.92:
            return "soif_critique"
        if agent._near_monsters:
            return "danger_proche"
        # timeout par type d'activité
        elapsed = self.w.tick - activity.started_tick
        timeouts = {
            "food_expedition": 1800,
            "water_search": 900,
            "return_home": 1200,
            "explore_region": 1200,
        }
        if elapsed > timeouts.get(activity.kind, 1200):
            return "timeout"
        return None

    def record_activity_outcome(self, agent: Being, kind: str, outcome: str, reward: float) -> None:
        """Enregistre le résultat d'une activité pour apprentissage (plan §5).

        Crée une mémoire causale épidémique, met à jour compétences, identité,
        intention et biais futurs.
        """
        self.activity_reasons[f"{kind}:{outcome}"] += 1
        self._reward(agent, reward)

        # Mise à jour compétences selon activité
        if kind == "food_expedition" and outcome == "success":
            agent.skills[0] = min(1.0, agent.skills[0] + 0.02)  # récolte
        elif kind == "water_search" and outcome == "success":
            agent.skills[0] = min(1.0, agent.skills[0] + 0.015)
        elif kind == "return_home" and outcome == "success":
            agent.skills[1] = min(1.0, agent.skills[1] + 0.01)  # construction/abri
        elif kind == "explore_region" and outcome == "success":
            agent.skills[3] = min(1.0, agent.skills[3] + 0.01)  # exploration

        # ─── Mémoire causale épidémique ───
        place = (getattr(agent, "tx", 0), getattr(agent, "ty", 0))
        expected = self._expected_effect_for_activity(kind)
        agent.anima_add_causal_trace(
            action=kind,
            place=place,
            tick=self.w.tick,
            expected_effect=expected,
        )

        # Crédit différé si le résultat correspond à l'attendu
        if outcome == "success":
            credit = agent.anima_credit_for(expected, self.w.tick)
            if credit > 0.2:
                # Apprentissage positif : renforce l'habitude
                self._apply_positive_credit(agent, kind, credit)

        # ─── Mise à jour identité et valeurs Anima ───
        self._update_anima_from_outcome(agent, kind, outcome, reward)

        # ─── Progression intention ───
        self._update_intention_from_outcome(agent, kind, outcome)

        # ─── Épisode autobiographique ───
        self._record_activity_episode(agent, kind, outcome, reward)

    def _expected_effect_for_activity(self, kind: str) -> str:
        mapping = {
            "food_expedition": "food_found",
            "water_search": "water_found",
            "return_home": "safety_reached",
            "explore_region": "discovery",
        }
        return mapping.get(kind, "unknown")

    def _apply_positive_credit(self, agent: Being, kind: str, credit: float):
        """Applique le crédit causal positif : renforce habitudes et valeurs."""
        # Renforce l'habitude correspondante
        habit_map = {
            "food_expedition": 0,  # récolte
            "water_search": 0,
            "return_home": 1,  # construction
            "explore_region": 3,  # exploration
        }
        habit_idx = habit_map.get(kind)
        if habit_idx is not None:
            agent.habits[habit_idx] = self.anima_clamp(
                agent.habits[habit_idx] + 0.02 * credit
            )

    def _update_anima_from_outcome(self, agent: Being, kind: str, outcome: str, reward: float):
        """Met à jour identité et valeurs Anima selon le résultat."""
        if outcome == "success":
            # Renforce l'identité correspondant à l'activité
            identity_map = {
                "food_expedition": "provider",
                "water_search": "provider",
                "return_home": "caretaker",
                "explore_region": "explorer",
                "help_ally": "mediator",
            }
            ident = identity_map.get(kind)
            if ident:
                agent.anima_add_identity(ident, 0.01)

            # Valeurs : survie et communauté
            agent.anima_add_value("survival", 0.005)
            if kind in ("help_ally", "return_home"):
                agent.anima_add_value("community", 0.005)
            agent.anima_add_value("knowledge", 0.003)

        elif outcome == "failed":
            # Apprentissage par l'échec : prudence
            agent.anima_add_value("security", 0.005)
            # Traumatisme mineur
            trauma_map = {
                "food_expedition": "hunger",
                "water_search": "hunger",  # soif = faim dans trauma
                "explore_region": "loss",
                "return_home": "loss",
            }
            trauma = trauma_map.get(kind)
            if trauma:
                agent.anima["trauma"][trauma] = min(1.0,
                    agent.anima["trauma"].get(trauma, 0.0) + 0.03)

    def _update_intention_from_outcome(self, agent: Being, kind: str, outcome: str):
        """Met à jour la progression de l'intention courante."""
        intent = agent.anima_get_intention()
        if not intent:
            return

        # Si l'activité correspond à l'intention
        intent_kind = intent.get("kind", "")
        kind_matches = {
            "food_expedition": ("secure_food", "avoid_danger"),
            "water_search": ("secure_food", "avoid_danger"),
            "return_home": ("recover_from_loss", "build_home"),
            "explore_region": ("explore_unknown",),
        }
        matching = kind_matches.get(kind, ())
        if intent_kind in matching:
            delta = 0.05 if outcome == "success" else -0.03
            agent.anima_update_intention_progress(delta, self.w.tick)

    def _record_activity_episode(self, agent: Being, kind: str, outcome: str, reward: float):
        """Enregistre un épisode autobiographique structuré."""
        place = (getattr(agent, "tx", 0), getattr(agent, "ty", 0))
        event_type = f"activity_{kind}"
        importance = 0.5 if outcome == "success" else 0.3
        agent.remember_anima_episode(
            tick=self.w.tick,
            kind=event_type,
            place=place,
            action=kind,
            outcome=outcome,
            importance=importance,
        )

    def best_memory_for(self, agent: Being, category: str) -> dict | None:
        """Meilleur souvenir pour une catégorie avec métadonnées.

        Les DEUX sources sont consultées et classées sur la même échelle :
        ``place_memories`` (lieux perçus/partagés, confiance >= 0.35) et
        ``agent.seen`` via ``recall``. Un score unique = confiance moins une
        pénalité de distance (0 à 1 tuile/100), borné à [0, 1] :

        * le plus proche et le plus confiant gagne (un souvenir lointain
          n'écrase plus un souvenir devenu fiable à côté de soi) ;
        * la valeur retournée reste comparable aux seuils des appelants
          (0.35 / 0.3) : au-delà de ~55 tuiles le score passe sous le seuil,
          ce qui conservait l'ancien garde-fou « pas d'expédition vers un
          lieu trop loin ».
        """
        def _scored(tx, ty, conf):
            d = max(abs(int(tx) - agent.tx), abs(int(ty) - agent.ty))
            s = float(conf) - min(1.0, d / 100.0)
            return max(0.0, min(1.0, s))

        best, best_s = None, -1e9

        for mem in getattr(agent, "place_memories", {}).values():
            if not isinstance(mem, dict):
                continue
            if mem.get("category") != category:
                continue
            conf = float(mem.get("confidence", 0.0))
            if conf < 0.35:
                continue
            s = _scored(mem.get("tx", agent.tx), mem.get("ty", agent.ty), conf)
            if s > best_s:
                best_s = s
                best = {"tx": int(mem["tx"]), "ty": int(mem["ty"]),
                        "confidence": s}

        for (x, y, f) in getattr(agent, "seen", {}).get(category, ()):
            if float(f) < 0.18:
                continue
            s = _scored(x, y, float(f))
            if s > best_s:
                best_s = s
                best = {"tx": int(x), "ty": int(y), "confidence": s}

        return best

    # ── water_search helpers ────────────────────────────────────────
    def verify_water_access(self, agent: Being, memory: dict) -> bool:
        """Vérifie que la mémoire d'eau est encore valide et accessible."""
        tx, ty = memory["tx"], memory["ty"]
        if not (0 <= tx < self.w.g and 0 <= ty < self.w.g):
            return False
        # Vérifier qu'il y a de l'eau à cet endroit ou adjacent
        has_water = False
        water_tx, water_ty = tx, ty
        if self.w.water[ty, tx]:
            has_water = True
        else:
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    nx, ny = tx + dx, ty + dy
                    if 0 <= nx < self.w.g and 0 <= ny < self.w.g and self.w.water[ny, nx]:
                        has_water = True
                        water_tx, water_ty = nx, ny
                        break
                if has_water:
                    break
        if not has_water:
            return False
        # Vérifier que l'agent peut accéder à l'eau (case de terre adjacente à l'eau)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                nx, ny = water_tx + dx, water_ty + dy
                if 0 <= nx < self.w.g and 0 <= ny < self.w.g:
                    if self.w.land[ny, nx] and not self.w.blocked[ny, nx]:
                        return True
        # Fallback: si l'agent est déjà adjacent à de l'eau, c'est accessible
        if self.w.near_water(agent.tx, agent.ty):
            return True
        return False

    def try_drink_at(self, agent: Being, tx: int, ty: int) -> bool:
        """Tentative de boire à la position donnée."""
        if not (0 <= tx < self.w.g and 0 <= ty < self.w.g):
            return False
        # Vérifier présence d'eau
        if not self.w.water[ty, tx]:
            # Chercher eau adjacente
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    nx, ny = tx + dx, ty + dy
                    if 0 <= nx < self.w.g and 0 <= ny < self.w.g and self.w.water[ny, nx]:
                        tx, ty = nx, ny
                        break
                else:
                    continue
                break
            else:
                return False
        # Boire
        before = agent.needs[2]
        agent.needs[2] = max(0.0, agent.needs[2] - 0.6)
        agent.temp = max(0.0, agent.temp - 0.1)
        agent.state = "drink"
        self.stats["drinks"] += 1
        self._reward(agent, (before - agent.needs[2]) * 0.8)
        # Mettre à jour la confiance de la mémoire
        agent.remember("water", tx, ty)
        agent.record_meaningful(self.w.tick, "drink")
        return True

    # ── food_expedition helpers (plan §6) ───────────────────────────
    def verify_food_memory(self, agent: Being, memory: dict) -> bool:
        """Vérifie que la mémoire de nourriture est encore valide."""
        tx, ty = memory["tx"], memory["ty"]
        if not (0 <= tx < self.w.g and 0 <= ty < self.w.g):
            return False
        aid = self.w.content_at(tx, ty)
        if aid >= 0:
            asd = self.am.assets[aid]
            return asd.edible > 0
        # Vérifier items au sol
        cell_key = (int(tx * TILE // 128), int(ty * TILE // 128))
        for it in self.food_cells.get(cell_key, ()):
            if it.kind == "food" and max(abs(it.x - tx * TILE), abs(it.y - ty * TILE)) < 32:
                return True
        return False

    def try_harvest_or_pickup_near(self, agent: Being) -> bool:
        """Tente de récolter ou ramasser de la nourriture à proximité."""
        tx, ty = agent.tx, agent.ty
        # D'abord vérifier la tuile courante
        aid = self.w.content_at(tx, ty)
        if aid >= 0:
            asd = self.am.assets[aid]
            if asd.edible > 0:
                self._do_eat(agent, tx, ty)
                return True
        # Puis items au sol proches
        cell_key = (int(agent.x // 128), int(agent.y // 128))
        for it in list(self.food_cells.get(cell_key, ())):
            if it.kind == "food" and (it.x - agent.x) ** 2 + (it.y - agent.y) ** 2 < 32 * 32:
                self.w.items.remove(it)
                self._eat(agent, it.nutrition)
                return True
        return False

    def try_eat_inventory_food(self, agent: Being) -> bool:
        """Tente de manger de la nourriture de l'inventaire."""
        # Pas d'inventaire de nourriture directe, mais on peut manger si on a récolté
        # Pour l'instant, on délègue à _do_eat sur place
        return self.try_harvest_or_pickup_near(agent)

    def choose_return_target(self, agent: Being) -> tuple[int, int, str] | None:
        """Choisit la cible de retour (maison, dépôt, ou clan)."""
        # Priorité 1: maison
        if agent.home:
            hx, hy = agent.home
            if 0 <= hx < self.w.g and 0 <= hy < self.w.g:
                return hx, hy, "home"
        # Priorité 2: dépôt le plus proche
        storage = self.nearest_storage(agent.tx, agent.ty, max_dist=30)
        if storage:
            return storage.tx, storage.ty, "storage"
        # Priorité 3: aller vers alliés
        if agent._near_agents:
            ally = max(agent._near_agents, key=lambda o: agent.trust(o.eid))
            if agent.trust(ally.eid) > 0.2:
                return ally.tx, ally.ty, "ally"
        return None

    def store_or_share_food(self, agent: Being) -> None:
        """Stocke ou partage la nourriture ramenée."""
        storage = self.nearest_storage(agent.tx, agent.ty, max_dist=2)
        if storage:
            self.deposit_to_storage(agent, storage)
            return
        # Partager avec alliés proches
        for other in agent._near_agents:
            if agent.trust(other.eid) > 0.3 and agent.carry() > 0:
                self._do_give(agent, other)
                break

    # ── maybe_start_food_expedition (plan §6) ───────────────────────
    def maybe_start_food_expedition(self, agent: Being) -> bool:
        """Tente de démarrer une expédition nourriture (plan §6).

        Priorité:
        1. Mémoire personnelle fiable
        2. Connaissance du clan
        3. Découverte directe de sites de ressources proches
        """
        if agent.activity is not None:
            return False
        if agent.hunger < 0.62:
            return False
        if agent.child:
            return False

        # 1. Mémoire personnelle
        mem = self.best_memory_for(agent, "food")
        if mem and mem["confidence"] >= 0.35:
            self.start_activity(
                agent,
                kind="food_expedition",
                stage="travel",
                target_tx=mem["tx"],
                target_ty=mem["ty"],
                reason="hungry + reliable food memory",
                data={"memory": mem, "source": "personal"},
            )
            self.activity_reasons["food_expedition:started"] += 1
            return True

        # 2. Connaissance du clan
        clan_places = self.clan_knowledge.nearby_places("food", agent.tx, agent.ty, max_dist=60)
        if clan_places:
            tx, ty, conf, _ = clan_places[0]
            self.start_activity(
                agent,
                kind="food_expedition",
                stage="travel",
                target_tx=tx,
                target_ty=ty,
                reason="hungry + clan knowledge",
                data={"tx": tx, "ty": ty, "confidence": conf, "source": "clan"},
            )
            self.activity_reasons["food_expedition:started"] += 1
            return True

        # 3. Découverte directe de sites de ressources (cachée, rafraîchie tous les 60 ticks)
        if not hasattr(self, "_cached_food_sites"):
            self._cached_food_sites = []
            self._food_sites_cache_tick = -1
        if self.w.tick - self._food_sites_cache_tick > 60:
            self._cached_food_sites = discover_resource_sites_near(self.w, agent.tx, agent.ty, max_dist=80)
            self._food_sites_cache_tick = self.w.tick
        sites = [s for s in self._cached_food_sites if s.remaining > 0]
        if sites:
            site = sites[0]
            site.record_discovery(agent.eid, self.w.tick)
            self.start_activity(
                agent,
                kind="food_expedition",
                stage="travel",
                target_tx=site.tx,
                target_ty=site.ty,
                reason=f"hungry + discovered {site.kind} site",
                data={"site_id": site.id, "source": "discovery"},
            )
            self.activity_reasons["food_expedition:started"] += 1
            return True

        return False

    def step_food_expedition(self, agent: Being) -> bool:
        """Machine à états pour food_expedition (plan §6)."""
        act = agent.activity
        if act is None or act.kind != "food_expedition":
            return False

        # Vérifier interruption
        interrupt = self.should_interrupt_activity(agent, act)
        if interrupt:
            self.fail_activity(agent, interrupt)
            return True

        act.last_stage_tick = self.w.tick

        while True:
            if act.stage == "travel":
                tx, ty = act.target_tx, act.target_ty
                if tx is not None and ty is not None:
                    self.set_goal_to_tile(agent, EXPLORE, tx, ty)
                    dist = max(abs(agent.tx - tx), abs(agent.ty - ty))
                    if dist <= 3:
                        act.stage = "verify"
                        continue
                break

            elif act.stage == "verify":
                # Verify food is still there
                if act.data.get("site_id"):
                    site = self.w.resource_sites.get(act.data["site_id"])
                    if site and site.remaining > 0:
                        site.record_discovery(agent.eid, self.w.tick)
                        act.data["verified"] = True
                        act.stage = "harvest"
                        continue
                    else:
                        self.fail_activity(agent, "food_site_depleted")
                        return True
                else:
                    # Legacy memory verification
                    mem = act.data.get("memory", {"tx": act.target_tx, "ty": act.target_ty})
                    if not self.verify_food_memory(agent, mem):
                        self.fail_activity(agent, "food_memory_invalid")
                        return True
                act.stage = "harvest"
                continue

            elif act.stage == "harvest":
                # Harvest from resource site or local food
                harvested = False
                if act.data.get("site_id"):
                    site = self.w.resource_sites.get(act.data["site_id"])
                    if site and site.remaining > 0:
                        taken = site.record_harvest(1.0, agent.eid, self.w.tick)
                        if taken > 0:
                            agent.anima_add_causal_trace(
                                "harvest", (site.tx, site.ty), self.w.tick, "food_found"
                            )
                            self.clan_knowledge.report_culture("food_location", site.tx, site.ty, agent.eid, self.w.tick)
                            harvested = True
                if not harvested:
                    if self.try_harvest_or_pickup_near(agent):
                        harvested = True

                if harvested:
                    act.stage = "consume_or_return"
                    continue
                self.fail_activity(agent, "harvest_failed")
                return True

            elif act.stage == "consume_or_return":
                if agent.hunger >= 0.86:
                    if self.try_eat_inventory_food(agent):
                        self.finish_activity(agent, "ate_on_site", 0.3)
                        return True
                act.stage = "return"
                continue

            elif act.stage == "return":
                ret = self.choose_return_target(agent)
                if ret:
                    tx, ty, kind = ret
                    self.set_goal_to_tile(agent, EXPLORE, tx, ty)
                    act.data["return_kind"] = kind
                    act.stage = "store_or_share"
                    continue
                self.fail_activity(agent, "no_return_target")
                return True

            elif act.stage == "store_or_share":
                self.store_or_share_food(agent)
                # Log successful return with food
                if act.data.get("site_id"):
                    site = self.w.resource_sites.get(act.data["site_id"])
                    if site:
                        site.record_discovery(agent.eid, self.w.tick)
                        agent.anima_add_causal_trace(
                            "return_food", (site.tx, site.ty), self.w.tick, "food_returned"
                        )
                self.finish_activity(agent, "food_returned", 0.35)
                return True

            else:
                break

        return True

    # ── water_search activity ──────────────────────────────────────
    def maybe_start_water_search(self, agent: Being) -> bool:
        """Tente de démarrer une recherche d'eau (plan §5, §6)."""
        if agent.activity is not None:
            return False
        if agent.needs[2] < 0.7:
            return False
        if agent.child:
            return False
        mem = self.best_memory_for(agent, "water")
        if not mem or mem["confidence"] < 0.3:
            return False
        self.start_activity(
            agent,
            kind="water_search",
            stage="choose",
            target_tx=mem["tx"],
            target_ty=mem["ty"],
            reason="thirsty + reliable water memory",
            data={"memory": mem},
        )
        self.activity_reasons["water_search:started"] += 1
        return True

    def step_water_search(self, agent: Being) -> bool:
        """Machine à états pour water_search : choose → travel → verify → drink → update_memory → return_or_continue."""
        act = agent.activity
        if act is None or act.kind != "water_search":
            return False

        # Vérifier interruption (soif critique = priorité absolue)
        interrupt = self.should_interrupt_activity(agent, act)
        if interrupt and interrupt != "soif_critique":
            self.fail_activity(agent, interrupt)
            return True

        act.last_stage_tick = self.w.tick

        while True:
            if act.stage == "choose":
                act.stage = "travel"
                continue  # passer à travel immédiatement

            elif act.stage == "travel":
                tx, ty = act.target_tx, act.target_ty
                if tx is not None and ty is not None:
                    self.set_goal_to_tile(agent, EXPLORE, tx, ty)
                    dist = max(abs(agent.tx - tx), abs(agent.ty - ty))
                    if dist <= 3:
                        act.stage = "verify"
                        continue  # passer à verify immédiatement
                break  # bloquant : attendre déplacement

            elif act.stage == "verify":
                mem = act.data.get("memory", {"tx": act.target_tx, "ty": act.target_ty})
                if not self.verify_water_access(agent, mem):
                    self.fail_activity(agent, "water_memory_invalid")
                    return True
                act.stage = "drink"
                continue  # passer à drink immédiatement

            elif act.stage == "drink":
                tx, ty = act.target_tx, act.target_ty
                if tx is not None and ty is not None:
                    # Trouver la position exacte de l'eau (peut être adjacente)
                    water_tx, water_ty = tx, ty
                    if not self.w.water[water_ty, water_tx]:
                        found = False
                        for dy in (-1, 0, 1):
                            for dx in (-1, 0, 1):
                                nx, ny = tx + dx, ty + dy
                                if 0 <= nx < self.w.g and 0 <= ny < self.w.g and self.w.water[ny, nx]:
                                    water_tx, water_ty = nx, ny
                                    found = True
                                    break
                            if found:
                                break
                    # Aller vers l'eau si pas adjacent
                    dist = max(abs(agent.tx - water_tx), abs(agent.ty - water_ty))
                    if dist <= 1:
                        self._set_goal(agent, DRINK)
                        if self.try_drink_at(agent, water_tx, water_ty):
                            act.stage = "update_memory"
                            continue  # passer à update_memory immédiatement
                    else:
                        self.set_goal_to_tile(agent, EXPLORE, water_tx, water_ty)
                break  # bloquant : attendre d'être adjacent et boire

            elif act.stage == "update_memory":
                # Mettre à jour la confiance de la mémoire (elle s'est avérée fiable)
                tx, ty = act.target_tx, act.target_ty
                if tx is not None and ty is not None:
                    agent.remember("water", tx, ty)
                act.stage = "return_or_continue"
                continue  # passer à return_or_continue immédiatement

            elif act.stage == "return_or_continue":
                # Si encore soif, continuer à chercher ; sinon finir
                if agent.needs[2] >= 0.6:
                    # Chercher une autre source
                    mem = self.best_memory_for(agent, "water")
                    if mem and mem["confidence"] >= 0.3:
                        act.target_tx = mem["tx"]
                        act.target_ty = mem["ty"]
                        act.data["memory"] = mem
                        act.stage = "travel"
                        continue  # boucler vers travel
                self.finish_activity(agent, "water_found", 0.3)
                return True

            else:
                break

        return True  # activité gérée ce tick

    # ── return_home activity ──────────────────────────────────────
    def maybe_start_return_home(self, agent: Being) -> bool:
        """Tente de démarrer un retour au foyer (plan §5).

        Déclencheurs explicites (OR) :
        - énergie faible
        - nuit
        - pluie forte
        - besoin de sécurité élevé
        - charge d'inventaire importante
        """
        if agent.activity is not None:
            return False

        needs_return = (
            agent.energy < 0.22
            or self.clock.is_night
            or self.clock.rain >= 0.55
            or agent.needs[4] >= 0.75
            or agent.carry() >= 0.85
        )

        if not needs_return:
            return False

        if agent.child:
            return False  # les enfants ne font pas return_home seuls
        target = self.choose_return_home_target(agent)
        if not target:
            return False
        tx, ty, kind = target
        self.start_activity(
            agent,
            kind="return_home",
            stage="choose_target",
            target_tx=tx,
            target_ty=ty,
            reason=f"return_home:{kind}",
            data={"return_kind": kind},
        )
        self.activity_reasons[f"return_home:started:{kind}"] += 1
        return True

    def choose_return_home_target(self, agent: Being) -> tuple[int, int, str] | None:
        """Choisit la cible de retour selon la priorité :
        personal home → personal shelter → clan shelter → allied storage/depot → family/ally group."""
        # Priorité 1: maison personnelle
        if agent.home:
            hx, hy = agent.home
            if 0 <= hx < self.w.g and 0 <= hy < self.w.g:
                return hx, hy, "home"
        # Priorité 2: abri personnel connu
        shelter_mem = self.best_memory_for(agent, "shelter")
        if shelter_mem:
            return shelter_mem["tx"], shelter_mem["ty"], "shelter"
        # Priorité 3: abri du clan (stockage avec shelter)
        for storage in self.w.storages.values():
            if storage.owner_clan == agent.color:
                if self.w.shelter[storage.ty, storage.tx]:
                    return storage.tx, storage.ty, "clan_shelter"
        # Priorité 4: dépôt allié / stockage
        storage = self.nearest_storage(agent.tx, agent.ty, max_dist=30)
        if storage:
            return storage.tx, storage.ty, "storage"
        # Priorité 5: groupe famille/allié
        if agent._near_agents:
            ally = max(agent._near_agents, key=lambda o: agent.trust(o.eid))
            if agent.trust(ally.eid) > 0.2:
                return ally.tx, ally.ty, "ally"
        return None

    def step_return_home(self, agent: Being) -> bool:
        """Machine à états pour return_home : choose_target → travel → at_destination."""
        act = agent.activity
        if act is None or act.kind != "return_home":
            return False

        interrupt = self.should_interrupt_activity(agent, act)
        if interrupt and interrupt != "soif_critique":
            self.fail_activity(agent, interrupt)
            return True

        act.last_stage_tick = self.w.tick

        # États bloquants
        blocking_stages = {"travel"}

        while True:
            if act.stage == "choose_target":
                act.stage = "travel"
                continue

            elif act.stage == "travel":
                tx, ty = act.target_tx, act.target_ty
                if tx is not None and ty is not None:
                    self.set_goal_to_tile(agent, EXPLORE, tx, ty)
                    dist = max(abs(agent.tx - tx), abs(agent.ty - ty))
                    if dist <= 2:
                        act.stage = "at_destination"
                        continue
                break  # bloquant : attendre arrivée

            elif act.stage == "at_destination":
                kind = act.data.get("return_kind", "")
                tx, ty = act.target_tx, act.target_ty
                # Vérifier s'il y a un abri ici
                if tx is not None and ty is not None and self.w.shelter[ty, tx]:
                    self._set_goal(agent, SLEEP)
                    self.finish_activity(agent, "returned_to_shelter", 0.25)
                # Vérifier s'il y a un stockage
                elif tx is not None and ty is not None and (tx, ty) in self.w.storages:
                    storage = self.w.storages[(tx, ty)]
                    self.deposit_appropriate_items(agent, storage)
                    self.finish_activity(agent, "returned_to_storage", 0.2)
                else:
                    # Juste se reposer sur place
                    self._set_goal(agent, REST)
                    self.finish_activity(agent, "returned_to_rest", 0.15)
                return True

            else:
                break

        return True

    # ── explore_region activity ──────────────────────────────
    REGION_SIZE = 64

    def maybe_start_explore_region(self, agent: Being) -> bool:
        """Tente de démarrer l'exploration d'une région."""
        if agent.activity is not None:
            return False
        if agent.child:
            return False
        urgency = (agent.hunger > 0.55 or agent.needs[2] > 0.55
                   or agent.personality[2] > 0.55)
        if not urgency:
            return False
        target = self.choose_exploration_region(agent)
        if not target:
            return False
        tx, ty = target
        self.start_activity(
            agent, kind="explore_region", stage="travel",
            target_tx=tx, target_ty=ty, reason="explore_unknown_region",
        )
        self.activity_reasons["explore_region:started"] += 1
        return True

    def choose_exploration_region(self, agent: Being):
        """Choisit une région peu familière et atteignable."""
        rx, ry = (agent.tx // self.REGION_SIZE,
                   agent.ty // self.REGION_SIZE)
        candidates = []
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nrx, nry = rx + dx, ry + dy
                memory = agent.region_memory.get((nrx, nry), {})
                familiarity = float(memory.get("familiarity", 0.0))
                danger = float(memory.get("danger", 0.0))
                resources = set(memory.get("resources", []))
                tx = min(max(nrx * self.REGION_SIZE + self.REGION_SIZE // 2, 2),
                         self.w.g - 3)
                ty = min(max(nry * self.REGION_SIZE + self.REGION_SIZE // 2, 2),
                         self.w.g - 3)
                if not self.w.land[ty, tx] or self.w.blocked[ty, tx]:
                    continue
                score = 0.55 * (1.0 - familiarity) - 0.45 * danger
                if agent.hunger > 0.55 and "food" in resources:
                    score += 0.25
                if agent.needs[2] > 0.55 and "water" in resources:
                    score += 0.20
                if agent.personality[2] > 0.55:
                    score += 0.15 * (1.0 - familiarity)
                if agent.personality[3] > 0.55:
                    score -= 0.15 * danger
                candidates.append((score, tx, ty))
        if not candidates:
            return None
        best = max(candidates, key=lambda row: row[0])
        tx, ty = best[1], best[2]
        if not self.w.land[ty, tx] or self.w.blocked[ty, tx]:
            for ddx, ddy in ((0, -1), (1, 0), (0, 1), (-1, 0),
                             (1, 1), (-1, 1), (1, -1), (-1, -1)):
                nx, ny = tx + ddx, ty + ddy
                if 0 <= nx < self.w.g and 0 <= ny < self.w.g:
                    if self.w.land[ny, nx] and not self.w.blocked[ny, nx]:
                        return (nx, ny)
            return None
        return (tx, ty)

    def step_explore_region(self, agent: Being) -> bool:
        """explore_region : travel → observe → record → return."""
        act = agent.activity
        if act is None or act.kind != "explore_region":
            return False
        interrupt = self.should_interrupt_activity(agent, act)
        if interrupt:
            self.fail_activity(agent, interrupt)
            return True
        act.last_stage_tick = self.w.tick
        tx, ty = act.target_tx, act.target_ty
        if tx is None or ty is None:
            self.fail_activity(agent, "no_target")
            return True
        while True:
            if act.stage == "travel":
                self.set_goal_to_tile(agent, EXPLORE, tx, ty)
                dist = max(abs(agent.tx - tx), abs(agent.ty - ty))
                if dist <= 3:
                    act.stage = "observe"
                    continue
                break
            elif act.stage == "observe":
                rx, ry = (tx // self.REGION_SIZE, ty // self.REGION_SIZE)
                agent.region_memory[(rx, ry)] = {
                    "familiarity": 0.5, "danger": 0.0,
                    "resources": [], "last_seen_tick": self.w.tick,
                }
                for dy2 in (-1, 0, 1):
                    for dx2 in (-1, 0, 1):
                        nx, ny = tx + dx2, ty + dy2
                        if 0 <= nx < self.w.g and 0 <= ny < self.w.g:
                            aid = self.w.content_at(nx, ny)
                            if aid >= 0:
                                asset = self.am.assets[aid]
                                rm = agent.region_memory[(rx, ry)]["resources"]
                                if asset.edible > 0 and "food" not in rm:
                                    rm.append("food")
                                elif hasattr(asset, 'harvest') and asset.harvest:
                                    mat = asset.harvest.get("material", "")
                                    if mat == "bois" and "wood" not in rm:
                                        rm.append("wood")
                act.stage = "record_discovery"
                continue
            elif act.stage == "record_discovery":
                agent.remember_place("explore", tx, ty, self.w.tick,
                                     confidence=0.4, source="direct")
                act.stage = "return"
                continue
            elif act.stage == "return":
                ret = self.choose_return_target(agent)
                if ret:
                    rtx, rty, kind = ret
                    self.set_goal_to_tile(agent, EXPLORE, rtx, rty)
                    act.data["return_kind"] = kind
                    act.stage = "done"
                else:
                    self.finish_activity(agent, "explored", 0.1)
                    return True
            else:
                break
        return True

    def deposit_appropriate_items(self, agent: Being, storage) -> None:
        """Dépose les items appropriés selon le besoin (nourriture si faim, matériaux si construction)."""
        # Priorité: déposer ce qui est en excès
        if agent.needs[0] < 0.4 and agent.inv.get("food", 0) > 0:
            self.deposit_to_storage(agent, storage)
        elif agent.inv.get("bois", 0) > 6:
            self.deposit_to_storage(agent, storage)
        elif agent.inv.get("pierre", 0) > 3:
            self.deposit_to_storage(agent, storage)
        elif agent.inv.get("or", 0) > 1:
            self.deposit_to_storage(agent, storage)
        else:
            # Déposer le matériau le plus abondant
            if agent.carry() > 0:
                self.deposit_to_storage(agent, storage)

    def set_goal_to_tile(self, agent: Being, act_type: int, tx: int, ty: int) -> None:
        """Définit un but de déplacement vers une tuile."""
        agent.goal = {"act": act_type, "x": tx, "y": ty, "ref": None,
                      "intensity": 1.0, "until": self.w.tick + 600}
        agent.goal_t = 0
        agent.stuck = 0
        agent._last_px, agent._last_py = agent.x, agent.y

    # ------------------------------------------------------------------ spawns
    def spawn_agent(self, x=None, y=None, color=None, gen=0, brain=None, parents=(),
                    energy=None, personality=None, n_hid=None, cls=None,
                    body=None, cog=None, emotions=None, needs=None, sex=None):
        if len(self.agents) >= int(self.runtime.get("max_population", MAX_POP)):
            return None
        colors = self.am.unit_colors() or ["blue"]
        color = color or colors[int(self.rng.integers(len(colors)))]
        classes = self.am.unit_classes(color) or ["pawn"]
        cls = cls if cls in classes else classes[int(self.rng.integers(len(classes)))]
        states = self.am.skin_states(color, cls)
        for _ in range(60):
            if x is None:
                tx = int(self.rng.integers(6, GRID - 6))
                ty = int(self.rng.integers(6, GRID - 6))
                if self.w.land[ty, tx] and not self.w.blocked[ty, tx]:
                    break
            else:
                x = min(max(x, 4), WORLD_PX - 6)
                y = min(max(y, 4), WORLD_PX - 6)
                break
        if x is None:
            x, y = tx * TILE + 8, ty * TILE + 8
        if n_hid is None:
            n_hid = int(self.rng.choice((64, 128, 128, 256)))
        if brain is None and parents is None:
            seed = self.academy.make_seed_params(n_hid, self.rng)
            if seed is not None:
                brain = Brain(n_hid=n_hid, params=seed, rng=self.rng)
        a = Being(self.next_eid, x, y, color, cls, states, gen, brain, parents,
                  personality=personality, rng=self.rng, born_tick=self.w.tick,
                  n_hid=n_hid, body=body, cog=cog, emotions=emotions, needs=needs,
                  sex=sex)
        a.col_idx = self._colidx(color)
        # Sans parents = arrivée autonome (dialogue « Créer », seed_life) :
        # l'adulte démarre à l'âge adulte. Le défaut de spawn_agent est ()
        # (tuple vide), pas None : tester `parents is None` laissait tout
        # habitant créé par l'UI à 0 an.
        if not parents:
            a.age = DEFAULT_SPAWN_AGE_TICKS
        else:
            a.age = 0
        if energy is not None:
            a.energy = a.needs[1] = energy
        self.next_eid += 1
        self.agents.append(a)
        cx, cy = int(a.x // 32), int(a.y // 32)
        self.grid_bucket.setdefault((cx, cy), []).append(a)
        self._entity_cells[a.eid] = (cx, cy)
        self.bootstrap_resource_memory(a, radius=max(40, a.sense_r(self.clock.light)))
        return a

    def spawn_sheep(self, x=None, y=None):
        if len(self.sheep) >= MAX_SHEEP:
            return
        for _ in range(30):
            if x is None:
                tx = int(self.rng.integers(6, GRID - 6))
                ty = int(self.rng.integers(6, GRID - 6))
            else:
                tx = min(GRID - 2, max(1, int(x // TILE)))
                ty = min(GRID - 2, max(1, int(y // TILE)))
            if self.w.land[ty, tx] and not self.w.blocked[ty, tx]:
                break
        s = Sheep(self.next_eid, tx * TILE + 8, ty * TILE + 8)
        self.next_eid += 1
        self.sheep.append(s)
        cx, cy = int(s.x // 32), int(s.y // 32)
        self.grid_bucket.setdefault((cx, cy), []).append(s)
        self._entity_cells[s.eid] = (cx, cy)

    def spawn_monster(self, x=None, y=None, kind=None):
        if not self.runtime.get("predators_enabled", True):
            return None
        level = self.runtime.get("predators_level", "normal")
        cap = {"faible": 5, "normal": MAX_MONSTERS, "élevé": 40}.get(
            level, MAX_MONSTERS)
        if len(self.monsters) >= cap:
            return None
        for _ in range(30):
            if x is None:
                tx = int(self.rng.integers(6, GRID - 6))
                ty = int(self.rng.integers(6, GRID - 6))
            else:
                tx = min(GRID - 2, max(1, int(x // TILE)))
                ty = min(GRID - 2, max(1, int(y // TILE)))
            if self.w.land[ty, tx] and not self.w.blocked[ty, tx]:
                break
        k = kind or self.rng.choice(MONSTER_KINDS)
        m = Monster(self.next_eid, tx * TILE + 8, ty * TILE + 8, kind=k)
        self.next_eid += 1
        # Lot G.2 : confinement si le spawn tombe dans une zone prédateur.
        for z in self.predator_zones.values():
            if z.contains(tx, ty):
                m.zone_id = z.id
                break
        self.monsters.append(m)
        cx, cy = int(m.x // 32), int(m.y // 32)
        self.grid_bucket.setdefault((cx, cy), []).append(m)
        self._entity_cells[m.eid] = (cx, cy)
        return m

    def remove_agent(self, a, name="le gardien"):
        """Retrait manuel depuis le tableau de bord : l'habitant quitte le monde
        sans laisser de cadavre. Les liens sociaux sont nettoyés."""
        if a is None or not getattr(a, "alive", False):
            return
        if self.selected is a:
            self.selected = None
        a.alive = False
        for other in self.agents:
            other.rel.pop(a.eid, None)
            if other.bonded == a.eid:
                other.bonded = None
                other.married = False
                other.partner_id = None
                other.life.append("a perdu son partenaire")
            other.children[:] = [c for c in other.children if c != a.eid]
        self.stats["deaths"] += 1
        self.log(f"{a.name} a quitté le monde (retiré par {name}).", (148, 148, 208), "life")
        self.agents[:] = [x for x in self.agents if x.alive]

    def _colidx(self, color):
        keys = self.am.unit_colors()
        return (keys.index(color) + 1) if color in keys else 1

    def bootstrap_resource_memory(self, a, radius=12):
        w = self.w
        for ty in range(max(0, a.ty - radius), min(w.g, a.ty + radius + 1)):
            for tx in range(max(0, a.tx - radius), min(w.g, a.tx + radius + 1)):
                aid = w.content_at(tx, ty)
                if aid < 0:
                    if w.water[ty, tx]:
                        a.remember("water", tx, ty)
                    continue
                asset = self.am.assets[aid]
                if asset.edible > 0:
                    a.remember("food", tx, ty)
                elif asset.harvest:
                    material = asset.harvest.get("material")
                    if material == "bois":
                        a.remember("wood", tx, ty)
                    elif material in ("pierre", "or"):
                        a.remember("stone", tx, ty)
                elif asset.shelter:
                    a.remember("shelter", tx, ty)

    def _by_eid(self, eid):
        for a in self.agents:
            if a.eid == eid:
                return a
        return None

    # ------------------------------------------------------------------ Anima
    def _record_anima(self, a, kind, place, actors=None, action="",
                      outcome="survived", health_loss=0.0, fear=0.0,
                      surprise=0.0, social_impact=0.0, achievement=0.0):
        """Calcule l'importance et enregistre un episode Anima."""
        importance = (
            0.35 * min(1.0, health_loss)
            + 0.25 * min(1.0, fear)
            + 0.15 * min(1.0, surprise)
            + 0.15 * min(1.0, social_impact)
            + 0.10 * min(1.0, achievement)
        )
        if importance < 0.05:
            return None
        emotion = {"fear": fear, "pain": min(1.0, health_loss),
                    "surprise": surprise}
        ep = a.remember_anima_episode(
            self.w.tick, kind, place, actors=actors,
            action=action, outcome=outcome, emotion=emotion,
            importance=importance,
            cap=int(self.runtime.get("episodes_max", 32)),
        )
        if importance >= 0.20:
            cx, cy = place[0] // 8, place[1] // 8
            a.anima["beliefs"]["places"][(cx, cy)] = min(1.0,
                max(a.anima["beliefs"]["places"].get((cx, cy), 0.0), importance))
            # Lot F : trace causale pour crédit différé
            a.anima_add_causal_trace(kind, place, self.w.tick,
                                     expected_effect=kind)
            self.update_anima_from_event(a, {
                "tick": self.w.tick, "kind": kind, "place": place,
                "actors": actors or [], "action": action,
                "outcome": outcome, "emotion": emotion,
                "importance": importance,
            })
        return ep

    # -- Lot 3 : mise a jour centree apres evenements --
    IDENTITY_EFFECTS = {
        "construction_complete": {"builder": 0.06},
        "construction_started": {"builder": 0.02},
        "food_given": {"provider": 0.04, "caretaker": 0.02},
        "monster_survival": {"survivor": 0.06},
        "monster_attack": {"survivor": 0.02},
        "monster_killed": {"fighter": 0.05},
        "new_area_discovered": {"explorer": 0.025},
        "help": {"caretaker": 0.03, "mediator": 0.01},
        "birth": {"caretaker": 0.03},
        "injury": {"survivor": 0.01},
    }
    VALUE_EFFECTS = {
        "food_given": {"community": 0.01, "generosity": 0.01},
        "food_received": {"community": 0.005},
        "food_found": {"wealth": 0.005},
        "theft": {"security": 0.02, "community": -0.01},
        "betrayal": {"security": 0.025, "community": -0.015},
        "monster_attack": {"survival": 0.01, "security": 0.015},
        "construction_complete": {"security": 0.01, "family": 0.005},
        "construction_started": {"knowledge": 0.005},
        "new_area_discovered": {"knowledge": 0.01},
        "help": {"community": 0.008, "generosity": 0.005},
        "birth": {"family": 0.02, "community": 0.005},
        "injury": {"survival": 0.005},
        "resource_deposited": {"community": 0.003},
        "resource_withdrawn": {"wealth": 0.003},
    }
    TRAUMA_EFFECTS = {
        "monster_attack": {"attack": 0.08},
        "injury": {"attack": 0.04},
        "theft": {"betrayal": 0.08},
        "betrayal": {"betrayal": 0.12},
        "loss": {"loss": 0.15},
        "fire": {"fire": 0.10},
    }
    # Lot D : biais d'action associés a chaque intention persistante.
    # Sorti de _bias() (ou il etait recree a chaque appel) pour rejoindre
    # les tables ci-dessus, deja definies au niveau classe.
    INTENTION_BIAS = {
        "secure_food": {HARVEST: 0.25, EAT: 0.10, EXPLORE: 0.05},
        "protect_family": {FLEE: 0.15, ATTACK: 0.10, SOCIAL: 0.10},
        "build_home": {BUILD: 0.30, HARVEST: 0.15},
        "recover_from_loss": {REST: 0.20, SOCIAL: 0.10},
        "avoid_danger": {FLEE: 0.30, EXPLORE: -0.10},
        "help_ally": {GIVE: 0.20, SOCIAL: 0.15, TALK: 0.10},
        "explore_unknown": {EXPLORE: 0.30},
    }

    def update_anima_from_event(self, agent, event):
        """Met a jour la psychologie personnelle apres un evenement reel."""
        kind = event.get("kind", "")
        actors = event.get("actors", [])
        tick = event.get("tick", self.w.tick)
        importance = event.get("importance", 0.0)
        health_loss = event.get("health_loss", 0.0)
        # --- identite ---
        identity_fx = self.IDENTITY_EFFECTS.get(kind, {})
        for id_key, delta in identity_fx.items():
            agent.anima_add_identity(id_key, delta)
        # --- valeurs ---
        value_fx = self.VALUE_EFFECTS.get(kind, {})
        for v_key, delta in value_fx.items():
            agent.anima_add_value(v_key, delta)
        # --- trauma ---
        if self.runtime.get("trauma_enabled", True):
            trauma_fx = self.TRAUMA_EFFECTS.get(kind, {})
            trauma_scale = float(self.runtime.get("trauma_scale", 1.0))
            for t_key, delta in trauma_fx.items():
                agent.anima["trauma"][t_key] = min(
                    1.0,
                    agent.anima["trauma"].get(t_key, 0.0)
                    + delta * trauma_scale)
        # --- attachement ---
        if kind == "food_received" and actors:
            for oid in [e for e in actors if e != agent.eid]:
                agent.anima["attachments"][oid] = min(
                    1.0, agent.anima["attachments"].get(oid, 0.0) + 0.05)
        elif kind == "help" and actors:
            for oid in [e for e in actors if e != agent.eid]:
                agent.anima["attachments"][oid] = min(
                    1.0, agent.anima["attachments"].get(oid, 0.0) + 0.03)
        elif kind == "birth":
            agent.anima["attachments"]["child"] = min(
                1.0, agent.anima["attachments"].get("child", 0.0) + 0.30)
        elif kind == "loss":
            agent.anima["attachments"]["lost"] = 0.0
        # --- croyances sociales ---
        other_eids = [e for e in actors if e != agent.eid]
        if kind == "food_given" and other_eids:
            for oid in other_eids:
                agent.anima_update_social_belief(
                    oid, tick, trust_delta=0.08,
                    generosity_delta=0.06, reliability_delta=0.03)
        elif kind == "food_received" and other_eids:
            for oid in other_eids:
                agent.anima_update_social_belief(
                    oid, tick, trust_delta=0.10, confidence_delta=0.04)
        elif kind in ("theft", "betrayal") and other_eids:
            for oid in other_eids:
                agent.anima_update_social_belief(
                    oid, tick, trust_delta=-0.20, danger_delta=0.15,
                    reliability_delta=-0.15)
        elif kind == "monster_attack" and other_eids:
            for oid in other_eids:
                agent.anima_update_social_belief(
                    oid, tick, trust_delta=-0.10, danger_delta=0.08)
        elif kind == "help" and other_eids:
            for oid in other_eids:
                agent.anima_update_social_belief(
                    oid, tick, trust_delta=0.06, reliability_delta=0.05)
        elif kind == "talk" and other_eids:
            for oid in other_eids:
                agent.anima_update_social_belief(
                    oid, tick, trust_delta=0.03, confidence_delta=0.02)
        elif kind == "loss" and other_eids:
            for oid in other_eids:
                agent.anima_update_social_belief(
                    oid, tick, trust_delta=-0.05, danger_delta=0.03)
        elif kind == "resource_deposited" and other_eids:
            for oid in other_eids:
                agent.anima_update_social_belief(
                    oid, tick, reliability_delta=0.02)
        elif kind == "message_received" and other_eids:
            for oid in other_eids:
                agent.anima_update_social_belief(
                    oid, tick, confidence_delta=0.01)
        # --- croyance lieu (danger percu) ---
        if kind in ("monster_attack", "injury", "fire") and event.get("place"):
            cx, cy = event["place"][0] // 8, event["place"][1] // 8
            agent.anima["beliefs"]["places"][(cx, cy)] = min(
                1.0, max(agent.anima["beliefs"]["places"].get((cx, cy), 0.0),
                         importance))

    # ------------------------------------------------------------------ step
    def step(self):
        w = self.w
        with self.perf.measure("sim"):
            self.clock.step()
            w.step(self.am, self.clock)
            # feu : systeme physique pur (combustible + vent - pluie)
            burned = w.step_fire(
                self.am, self.clock.wind, self.clock.rain, self.am.flammable,
                spread=float(self.runtime.get("fire_spread_scale", 1.0)))
            if burned and w.tick % 30 == 0:
                self.stats["fires"] += 1
            if self.clock.lightning():
                self.clock.lightning_tick = w.tick
                for _ in range(3):
                    tx, ty = int(self.rng.integers(GRID)), int(self.rng.integers(GRID))
                    if w.land[ty, tx] and w.content_at(tx, ty) >= 0:
                        w.ignite(tx, ty)
                        self.log("La foudre a allumé un feu.", (218, 138, 58), "weather")
                        break
            self._bucket()
            for a in self.agents:
                if a.alive:
                    # Light perception every tick: heat map only (cheap)
                    with self.perf.measure("perception_light"):
                        self._perceive_light(a)
                    # Full perception + decision only when agent should think
                    if self.agent_should_think(a):
                        with self.perf.measure("perception"):
                            self._perceive(a)
                        with self.perf.measure("decision"):
                            self._agent(a)
                    else:
                        # L'agent ne pense pas ce tick, mais continue son but courant
                        if a.goal is not None:
                            with self.perf.measure("execution"):
                                self._execute(a)
                            # Anti-passivity : la pression de vie suit aussi
                            # les agents qui ne deliberent pas ce tick.
                            self.update_life_drive(a)
                        elif a.activity is None:
                            # Anti-passivity : le bloc « but nul » doit tourner
                            # a chaque tick ou aucun but n'existe, meme sans
                            # deliberation (pression de vie puis repli).
                            self.update_life_drive(a)
                            ld = float(getattr(a, "life_drive", 0.0))
                            launched = False
                            if ld > 0.3:
                                if ld > 0.35 and not a.child:
                                    if self.maybe_start_food_expedition(a):
                                        launched = True
                                    elif self.maybe_start_explore_region(a):
                                        launched = True
                                if not launched:
                                    self.fallback_goal(a)
                    # Lot C : decroissance trauma + identite (tous les 100 ticks)
                    if w.tick % 100 == 0:
                        a.anima_decay_identity()
                        n_near = len([o for o in self.agents
                                      if o.alive and o.eid != a.eid
                                      and abs(o.tx - a.tx) + abs(o.ty - a.ty) < 8])
                        safety = 1.0 if a.needs[4] > 0.6 else 0.35
                        a.anima_decay_trauma(safety=safety, support=n_near / 4.0)
                    # Lot F : reputation (tous les 120 ticks)
                    if w.tick % 120 == 0:
                        self.update_reputation(a)
            for s in self.sheep:
                if s.alive:
                    self._sheep(s)
            for m in self.monsters:
                if m.alive:
                    self._monster(m)
            # Filet de sécurité : aucun habitant vivant ne peut rester
            # avec health <= 0 (dégâts de combat, faim, soif, gel...).
            for a in self.agents:
                if a.alive and float(a.health) <= 0.0:
                    self._check_vital_death(a)
            self._forget_dead_agents()
            self.sheep = [s for s in self.sheep if s.alive]
            self.monsters = [m for m in self.monsters if m.alive]
            # nettoyage grid_bucket : entites mortes
            for dead_eid in [eid for eid, cell in list(self._entity_cells.items())
                             if not any(a.eid == eid for a in self.agents)
                             and not any(s.eid == eid for s in self.sheep)
                             and not any(m.eid == eid for m in self.monsters)]:
                cell = self._entity_cells.pop(dead_eid, None)
                if cell is not None:
                    bucket = self.grid_bucket.get(cell)
                    if bucket:
                        self.grid_bucket[cell] = [e for e in bucket if getattr(e, "eid", None) != dead_eid]
                        if not self.grid_bucket[cell]:
                            del self.grid_bucket[cell]
            self.effects = [e for e in self.effects if w.tick - e["t0"] < e["ttl"]]
            # odeurs des objets
            if w.tick % 20 == 0:
                for it in w.items:
                    if it.kind == "food":
                        w.smell[int(it.y // TILE), int(it.x // TILE)] = min(1.0,
                            w.smell[int(it.y // TILE), int(it.x // TILE)] + 0.2)
            if w.tick % 240 == 0:
                for a in self.agents:
                    for c in a.seen:
                        decay = 0.995 + 0.004 * a.cog[0]
                        a.seen[c] = [(x, y, f * decay) for x, y, f in a.seen[c] if f > 0.16]
            recent = sum(1 for t in self._recent_attacks if w.tick - t < 300)
            if recent >= 14 and w.tick - self._last_war_log > 900:
                self._last_war_log = w.tick
                self.log("Des habitants s'entredéchirent pour les ressources !", (228, 98, 98), "combat")
            if w.tick % 60 == 0:
                self.pop_hist.append(len(self.agents))
            if w.tick % 900 == 0:
                self._analyze_society()
            if w.tick % 3600 == 0:
                self.social_memory.decay(self.w.tick)
            if w.tick % 1800 == 0:
                for a in self.agents:
                    if a.alive and not a.child:
                        accepted = self.academy.consider(a, self.w.tick)
                        if accepted:
                            self.log(f"Nouveau champion : {a.name} ({a.age_years:.1f} ans)",
                                     (88, 148, 228), "world")
            if w.tick % DAY_TICKS == 0:
                self.lab.snapshot(self)
            if __debug__ and w.tick % 600 == 0:
                from .invariants import validate_simulation
                for error in validate_simulation(self):
                    self.log(f"INVARIANT: {error}", (214, 84, 84), "world")
            # Lot E : décroissance des institutions (gate runtime).
            if w.tick % 600 == 0 and self.runtime.get("institutions_enabled", True):
                self.clan_knowledge.decay_institutions(w.tick)
            if w.tick % 1800 == 0:
                for a in self.agents:
                    expired = [k for k, (_, until) in a.failed_targets.items() if w.tick > until]
                    for k in expired:
                        del a.failed_targets[k]
            if w.tick % 60 == 0:
                self._grow_crops()

    def _grow_crops(self):
        w = self.w
        for (tx, ty), plot in list(w.crop_plots.items()):
            if not (0 <= tx < w.g and 0 <= ty < w.g):
                continue
            if w.water[ty, tx]:
                plot.watered = True
            elif self.clock.rain > 0.3:
                plot.watered = True
            else:
                plot.watered = False
            food_mult = {"faible": 0.5, "normal": 1.0, "élevé": 1.5}.get(
                self.runtime.get("food_level", "normal"), 1.0)
            growth_rate = (0.001
                           * float(self.runtime.get("regrowth_scale", 1.0))
                           * food_mult)
            if plot.watered:
                growth_rate *= 2.0
            if self.clock.is_night:
                growth_rate *= 0.5
            plot.growth = min(1.0, plot.growth + growth_rate)
            if plot.growth >= 1.0 and w.content_at(tx, ty) < 0:
                pool = self.am.pool("food")
                if pool:
                    aid = int(self.am.pick(pool, self.rng))
                    w.place(tx, ty, aid, self.am, hp=3, solid=False, size=1)
                    del w.crop_plots[(tx, ty)]
                    self.lab.event(self.w.tick, "crop_harvested",
                                   eid=plot.owner_eid, tx=tx, ty=ty)

    # ------------------------------------------------------------------ messages
    SEMANTIC_VOCABULARY = {
        "danger_here": {"urgency": 0.8, "decay": 0.001},
        "food_here": {"urgency": 0.3, "decay": 0.0005},
        "water_here": {"urgency": 0.3, "decay": 0.0005},
        "need_help": {"urgency": 0.7, "decay": 0.002},
        "need_resource": {"urgency": 0.5, "decay": 0.001},
        "build_site": {"urgency": 0.2, "decay": 0.0003},
        "follow_me": {"urgency": 0.4, "decay": 0.001},
        "trust_warning": {"urgency": 0.6, "decay": 0.001},
        "thanks": {"urgency": 0.1, "decay": 0.003},
        "grief": {"urgency": 0.5, "decay": 0.001},
    }

    def send_fact(self, sender, receiver, category, tx, ty, confidence=0.6):
        trust = receiver.trust(sender.eid)
        if trust < -0.3:
            return False
        # Lot G : fiabilité du message basée sur la source
        source_belief = receiver.anima_social_belief(sender.eid, self.w.tick)
        source_reliability = source_belief.get("reliability", 0.5)
        effective_confidence = confidence * (0.5 + 0.5 * source_reliability)
        receiver.remember(category, tx, ty)
        receiver.episodes.append((self.w.tick, "message", {
            "from": sender.eid,
            "category": category,
            "tx": tx,
            "ty": ty,
            "confidence": effective_confidence,
        }))
        self.lab.event(self.w.tick, "message_sent",
                       sender_eid=sender.eid, receiver_eid=receiver.eid,
                       category=category, tx=tx, ty=ty, confidence=effective_confidence)
        self.lab.event(self.w.tick, "message_received",
                       sender_eid=sender.eid, receiver_eid=receiver.eid,
                       category=category, tx=tx, ty=ty, trust=trust)
        self._record_anima(
            receiver, "message_received", (tx, ty),
            actors=[receiver.eid, sender.eid], action="receive_message",
            outcome="received", surprise=0.1)
        return True

    def _bucket(self):
        self.item_bucket = {}
        self.food_cells = {}
        keep = []
        for it in self.w.items:
            it.life -= 1
            if it.life <= 0:
                continue
            if it.kind == "food" and it.spoil_tick > 0 and self.w.tick >= it.spoil_tick:
                continue
            keep.append(it)
            self.item_bucket.setdefault((int(it.x // 32), int(it.y // 32)), []).append(it)
            if it.kind == "food":
                self.food_cells.setdefault((int(it.x // 128), int(it.y // 128)), []).append(it)
        self.w.items = keep

    def _near(self, x, y, pred, r=1):
        cx, cy = int(x // 32), int(y // 32)
        out = []
        for j in range(cy - r, cy + r + 1):
            for i in range(cx - r, cx + r + 1):
                for e in self.grid_bucket.get((i, j), ()):
                    if pred(e):
                        out.append(e)
        return out

    def _has_food_near(self, x, y, radius_px=40):
        cell = 128
        cx, cy = int(x // cell), int(y // cell)
        r = max(1, math.ceil(radius_px / cell))
        r2 = radius_px * radius_px
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                for item in self.food_cells.get((xx, yy), ()):
                    if (item.x - x) ** 2 + (item.y - y) ** 2 <= r2:
                        return True
        return False

    # ------------------------------------------------------------------ perception légère : heat map seulement (tous les ticks)
    def _perceive_light(self, a: Being):
        w = self.w
        tx, ty = a.tx, a.ty
        old_heat = float(w.heat[ty, tx])
        w.heat[ty, tx] = min(1.0, w.heat[ty, tx] + 0.012)
        if old_heat < 0.5 and w.heat[ty, tx] >= 0.5:
            self.lab.event(self.w.tick, "route_used", tx=tx, ty=ty)

    # ------------------------------------------------------------------ perception double : longue + courte portée
    def _perceive(self, a: Being):
        w = self.w
        light = self.clock.light
        R = a.sense_r(light)                    # longue portée (10-15 tiles)
        R_near = a.sense_r_near()               # courte portée (8 tiles = Moore)
        tx, ty = a.tx, a.ty
        old_heat = float(w.heat[ty, tx])
        w.heat[ty, tx] = min(1.0, w.heat[ty, tx] + 0.012)
        if old_heat < 0.5 and w.heat[ty, tx] >= 0.5:
            self.lab.event(self.w.tick, "route_used", tx=tx, ty=ty)

        # ====== VISION LONGUE PORTÉE : mémoire / navigation ======
        n = PERCEPT_CELLS + int(40 * a.cog[3])
        for _ in range(n):
            ang = self.rng.uniform(0, 6.283)
            rad = self.rng.random() ** 0.6 * R
            x = int(tx + math.cos(ang) * rad)
            y = int(ty + math.sin(ang) * rad)
            if not (0 <= x < w.g and 0 <= y < w.g):
                continue
            if w.fire[y, x] > 0:
                a.emotions[0] = min(1.0, a.emotions[0] + 0.02)
                a.emotions[5] = min(1.0, a.emotions[5] + 0.02)
                a.belief_places[(x // 8, y // 8)] = min(1.0,
                    a.belief_places.get((x // 8, y // 8), 0) + 0.1)
                self.clan_knowledge.report_danger(x, y, a.eid, w.tick, 0.6)
                continue
            aid = w.content_at(x, y)
            if aid < 0:
                if w.water[y, x]:
                    a.remember("water", x, y)
                    a.remember_place("water", x, y, self.w.tick,
                                       confidence=0.7, source="direct")
                continue
            asd = self.am.assets[aid]
            if asd.edible > 0:
                a.remember("food", x, y)
                a.remember_place("food", x, y, self.w.tick,
                                   confidence=0.75,
                                   estimated_amount=0.6,
                                   estimated_danger=0.1,
                                   source="direct")
                self.clan_knowledge.share_place("food", x, y, a.eid, w.tick)
            elif asd.harvest:
                m = asd.harvest["material"]
                cat = {"bois": "wood", "pierre": "stone",
                        "or": "stone"}.get(m, "wood")
                a.remember(cat, x, y)
                a.remember_place(cat, x, y, self.w.tick,
                                   confidence=0.7, source="direct")
                self.clan_knowledge.share_place(cat, x, y, a.eid, w.tick)
            elif asd.tool:
                a.remember("wood", x, y)
                a.remember_place("wood", x, y, self.w.tick,
                                   confidence=0.6, source="direct")
                self.clan_knowledge.share_place("wood", x, y, a.eid, w.tick)
            elif asd.shelter:
                a.remember("shelter", x, y)
                a.remember_place("shelter", x, y, self.w.tick,
                                   confidence=0.65, source="direct")
                self.clan_knowledge.share_place("shelter", x, y, a.eid, w.tick)

        # ====== VISION COURTE PORTÉE : Moore neighborhood (actions physiques) ======
        near_agents = []
        near_sheep = []
        near_monsters = []
        R_near_chunks = max(1, int(R_near * TILE / 32))
        cx_a, cy_a = int(a.x // 32), int(a.y // 32)
        R_near_px = R_near * TILE
        for j in range(cy_a - R_near_chunks, cy_a + R_near_chunks + 1):
            for i in range(cx_a - R_near_chunks, cx_a + R_near_chunks + 1):
                for e in self.grid_bucket.get((i, j), ()):
                    if isinstance(e, Being) and e.eid != a.eid and getattr(e, "alive", False):
                        d2 = (e.x - a.x) ** 2 + (e.y - a.y) ** 2
                        if d2 < R_near_px ** 2:
                            near_agents.append(e)
                    elif isinstance(e, Sheep) and getattr(e, "alive", False):
                        d2 = (e.x - a.x) ** 2 + (e.y - a.y) ** 2
                        if d2 < R_near_px ** 2:
                            near_sheep.append(e)
                    elif isinstance(e, Monster) and getattr(e, "alive", False):
                        d2 = (e.x - a.x) ** 2 + (e.y - a.y) ** 2
                        if d2 < R_near_px ** 2:
                            near_monsters.append(e)
        # mémoriser agents vus en longue portée aussi
        for e in near_agents:
            a.remember("agent", e.tx, e.ty)

        # Mémoire régionale : mise à jour de la région actuelle
        rx, ry = int(tx // 64), int(ty // 64)
        a.region_memory[(rx, ry)] = {
            "familiarity": min(1.0, float(a.region_memory.get((rx, ry), {}).get("familiarity", 0.0)) + 0.05),
            "danger": max(float(a.region_memory.get((rx, ry), {}).get("danger", 0.0)),
                         float(a.belief_places.get((rx, ry), 0.0))),
            "resources": list(set(a.region_memory.get((rx, ry), {}).get("resources", []))),
            "last_seen_tick": self.w.tick,
        }

        # sons percus
        for (sx, sy, kind, inten, st) in self.sounds:
            if st == a._last_heard:
                continue
            d = math.hypot(sx - a.x, sy - a.y)
            if d < (30 + 70 * a.body[3]) * inten:
                a._last_heard = st
                self._on_sound(a, kind, sx, sy)

        # canaux locaux (8 cases Moore — court portée)
        loc = a._loc if hasattr(a, "_loc") else np.zeros(8)
        fx, fy = tx + (a.fx or 1), ty + a.fy
        loc[0] = 1.0 if (0 <= fx < w.g and 0 <= fy < w.g and w.blocked[fy, fx]) else 0.0
        loc[1] = 1.0 if any(
            (lambda aid: aid >= 0 and self.am.assets[aid].harvest)(w.content_at(x, y))
            for x, y in self._ring(tx, ty)
        ) else 0.0
        loc[2] = 1.0 if near_agents else 0.0
        loc[3] = 1.0 if near_sheep else 0.0
        loc[4] = 1.0 if w.near_water(tx, ty) else 0.0
        loc[5] = 1.0 if w.fire[max(0, ty - 2):ty + 3, max(0, tx - 2):tx + 3].any() else 0.0
        loc[6] = float(w.smell[ty, tx])
        loc[7] = float(w.shelter[ty, tx])
        a._loc = loc
        a._near_agents = near_agents
        a._near_sheep = near_sheep
        a._near_monsters = near_monsters
        for monster in near_monsters:
            a.belief_places[(monster.tx // 8, monster.ty // 8)] = min(
                1.0,
                a.belief_places.get((monster.tx // 8, monster.ty // 8), 0.0) + 0.20,
            )

        # ====== CONTEXTE LOCAL STRUCTURE ======
        # Check perception cache (same tile + same tick)
        if (a.context_tick == w.tick and a.context_tx == tx and a.context_ty == ty):
            # Cache hit - reuse stored values
            pass
        else:
            # Single bounded scan for all local densities
            food_count = 0
            wood_count = 0
            stone_count = 0
            radius = 5
            y_min = max(0, ty - radius)
            y_max = min(w.g, ty + radius + 1)
            x_min = max(0, tx - radius)
            x_max = min(w.g, tx + radius + 1)
            am_assets = self.am.assets
            for yy in range(y_min, y_max):
                for xx in range(x_min, x_max):
                    aid = w.content_at(xx, yy)
                    if aid < 0:
                        continue
                    asset = am_assets[aid]
                    if asset.edible > 0:
                        food_count += 1
                    elif asset.harvest:
                        mat = asset.harvest.get("material")
                        if mat == "bois":
                            wood_count += 1
                        elif mat in ("pierre", "or"):
                            stone_count += 1
            # Update cache
            a.context_tick = w.tick
            a.context_tx = tx
            a.context_ty = ty
            a.context["food_density"] = min(1.0, food_count / 12.0)
            a.context["wood_density"] = min(1.0, wood_count / 12.0)
            a.context["stone_density"] = min(1.0, stone_count / 12.0)

        ctx = a.context
        ctx["sheep_count"] = min(1.0, len(near_sheep) / 5.0)
        ctx["monster_count"] = min(1.0, len(near_monsters) / 4.0)
        ctx["ally_count"] = min(1.0, sum(1 for e in near_agents if a.trust(e.eid) > 0.2) / 5.0)
        ctx["enemy_count"] = min(1.0, sum(1 for e in near_agents if a.trust(e.eid) < -0.2) / 5.0)
        stor = self.nearest_storage(tx, ty, max_dist=12)
        ctx["storage_near"] = 0.0 if stor is None else max(0.0, 1.0 - stor.total() / max(1, stor.capacity))
        ctx["site_near"] = 1.0 if any(
            abs(sx - tx) <= 8 and abs(sy - ty) <= 8
            for sx, sy in w.sites
        ) else 0.0
        ctx["route_danger"] = min(1.0, float(w.smell[ty, tx]))

    @staticmethod
    def _ring(tx, ty):
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx or dy:
                    yield tx + dx, ty + dy

    def _on_sound(self, a, kind, sx, sy):
        if kind == "chop":
            a.emotions[5] = min(1.0, a.emotions[5] + 0.08)   # curiosite
        elif kind == "scream":
            a.emotions[0] = min(1.0, a.emotions[0] + 0.3)
            a.belief_places[(int(sx // 128), int(sy // 128))] = min(
                1.0, a.belief_places.get((int(sx // 128), int(sy // 128)), 0) + 0.25)
        elif kind == "fight":
            a.emotions[0] = min(1.0, a.emotions[0] + 0.15)
        elif kind == "voice" and a.child:
            a.skills[3] = min(1.0, a.skills[3] + 0.02)       # l'enfant écoute et apprend

    # ------------------------------------------------------------------ vecteur mental
    def _sense(self, a: Being):
        s = self._sens
        n, e, p, b = a.needs, a.emotions, a.personality, a.body
        tx, ty = a.tx, a.ty
        s[0] = a.hunger
        s[1] = a.energy
        s[2] = n[2]
        s[3] = n[3]
        s[4] = 1.0 - e[0]
        s[5] = n[5]
        s[6] = n[6]
        s[7] = a.health
        s[8] = min(1.0, a.age / float(AGE_ELDER_TICKS * 2))
        s[9] = self.clock.temp
        s[10:15] = b
        s[15:27] = p
        s[27:35] = e
        s[35:39] = a.cog
        s[39] = a.self_esteem
        s[40] = max(-1.0, min(1.0, a.rep / 8.0))
        near_trust = 0.0
        if a._near_agents:
            near_trust = float(np.mean([a.trust(x.eid) for x in a._near_agents]))
        s[41] = near_trust
        s[42] = 1.0 if a.hated is not None else 0.0
        s[43] = 1.0 if a.bonded is not None else 0.0
        s[44] = 1.0 if a.child else 0.0
        s[45:49] = a.skills
        s[49:64] = a.habits
        s[64] = a.mood(self.w.tick)
        s[65:73] = a._loc
        i = 73
        for cat in ("food", "wood", "stone", "water", "shelter", "agent"):
            mem = a.recall(cat, tx, ty)
            if mem:
                ang = math.atan2(mem[1] - ty, mem[0] - tx)
                s[i] = 1.0
                s[i + 1] = math.cos(ang)
                s[i + 2] = math.sin(ang)
            else:
                s[i] = s[i + 1] = s[i + 2] = 0.0
            i += 3
        f = self.clock.day_frac
        s[91] = math.sin(f * 6.283)
        s[92] = math.cos(f * 6.283)
        s[93] = self.clock.temp
        s[94] = self.clock.rain
        # === Nouvelles entrees (95-127) ===
        INVCAP = 8.0
        s[INPUT["wood_inventory"]] = min(1.0, a.inv.get("bois", 0) / INVCAP)
        s[INPUT["stone_inventory"]] = min(1.0, a.inv.get("pierre", 0) / INVCAP)
        s[INPUT["seed_inventory"]] = min(1.0, a.inv.get("graine", 0) / INVCAP)
        s[INPUT["gold_inventory"]] = min(1.0, a.inv.get("or", 0) / INVCAP)
        s[INPUT["tool_equipped"]] = 1.0 if a.tool >= 0 else 0.0
        s[INPUT["tool_durability"]] = min(1.0, a.tool_durability / 20.0) if a.tool >= 0 else 0.0
        tool_kind = ""
        if a.tool >= 0:
            tool_kind = self.am.assets[a.tool].meta.get("tool_kind", "")
        s[INPUT["tool_axe"]] = 1.0 if tool_kind == "hache" else 0.0
        s[INPUT["tool_pickaxe"]] = 1.0 if tool_kind == "pioche" else 0.0
        s[INPUT["tool_hammer"]] = 1.0 if tool_kind == "marteau" else 0.0
        ctx = getattr(a, 'context', {})
        s[INPUT["food_density"]] = ctx.get("food_density", 0.0)
        s[INPUT["wood_density"]] = ctx.get("wood_density", 0.0)
        s[INPUT["stone_density"]] = ctx.get("stone_density", 0.0)
        s[INPUT["sheep_near"]] = ctx.get("sheep_count", 0.0)
        s[INPUT["allies_near"]] = ctx.get("ally_count", 0.0)
        s[INPUT["enemies_near"]] = ctx.get("enemy_count", 0.0)
        s[INPUT["storage_near"]] = ctx.get("storage_near", 0.0)
        stor = self.nearest_storage(tx, ty, max_dist=14)
        if stor:
            s[INPUT["storage_food"]] = min(1.0, stor.inventory.get("food", 0) / max(1, stor.capacity))
            s[INPUT["storage_wood"]] = min(1.0, stor.inventory.get("bois", 0) / max(1, stor.capacity))
        s[INPUT["site_near"]] = ctx.get("site_near", 0.0)
        site = self.nearest_site(tx, ty, max_dist=10)
        if site:
            s[INPUT["site_progress"]] = site.progress()
            missing = sum(1 for t in site.tasks if t.key not in site.placed)
            s[INPUT["site_missing"]] = min(1.0, missing / 10.0)
        food_mem = a.recall("food", tx, ty)
        s[INPUT["food_distance"]] = min(1.0, (food_mem[2] / 100.0) if food_mem else 1.0)
        water_mem = a.recall("water", tx, ty)
        s[INPUT["water_distance"]] = min(1.0, (water_mem[2] / 100.0) if water_mem else 1.0)
        shelter_mem = a.recall("shelter", tx, ty)
        s[INPUT["shelter_distance"]] = min(1.0, (shelter_mem[2] / 100.0) if shelter_mem else 1.0)
        if a.bonded is not None:
            partner = self._by_eid(a.bonded)
            if partner:
                d = max(abs(partner.tx - tx), abs(partner.ty - ty))
                s[INPUT["partner_distance"]] = min(1.0, d / 40.0)
        s[INPUT["route_danger"]] = ctx.get("route_danger", 0.0)
        s[INPUT["neighbor_need"]] = min(1.0, len(a._near_agents) / 3.0)
        s[INPUT["local_reputation"]] = max(-1.0, min(1.0, a.rep / 8.0))
        s[INPUT["winter"]] = 1.0 if self.clock.is_winter else 0.0
        if a.home:
            hx, hy = a.home
            if 0 <= hx < self.w.g and 0 <= hy < self.w.g:
                stor_home = self.w.storages.get((hx, hy))
                if stor_home:
                    s[INPUT["home_storage"]] = min(1.0, stor_home.total() / max(1, stor_home.capacity))
        s[INPUT["inventory_load"]] = min(1.0, sum(max(0, v) for v in a.inv.values()) / 32.0)
        s[INPUT["local_fear"]] = float(a.emotions[0])
        s[INPUT["life_progress"]] = min(1.0, a.age / float(AGE_ELDER_TICKS * 3))
        # Anima: mémoire épisodique émotionnelle
        anima = a.anima
        s[INPUT["trauma_attack"]] = min(1.0, anima["trauma"]["attack"])
        belief_near = 0.0
        cx, cy = tx // 8, ty // 8
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                v = anima["beliefs"]["places"].get((cx + dx, cy + dy), 0.0)
                if v > belief_near:
                    belief_near = v
        s[INPUT["belief_danger"]] = min(1.0, belief_near)
        s[INPUT["episode_count"]] = min(1.0, len(anima["episodic_memory"]) / 20.0)
        s[INPUT["anima_fighter"]] = min(1.0, anima["identity"]["fighter"])
        return s

    # ------------------------------------------------------------------ pression de vie
    def update_life_drive(self, a) -> None:
        """Pression de vie: augmente quand un habitant sain reste passif,
        baisse apres une action utile."""
        tick = int(self.w.tick)
        act = None
        if a.goal is not None:
            act = a.goal.get("act")
        meaningful = getattr(a, "last_meaningful_kind", "")
        is_passive = act in (REST, SLEEP) or (a.goal is None and not meaningful)
        able = (a.energy > 0.60 and a.hunger < 0.60
                and a.needs[2] < 0.60 and a.needs[3] < 0.60
                and a.pain < 0.30 and a.emotions[0] < 0.35
                and not a.child)
        if is_passive and able:
            a.passive_ticks = getattr(a, "passive_ticks", 0) + 1
            a.life_drive = min(1.0, a.life_drive
                               + 0.004 + 0.5 * float(a.personality[2]) * 0.002)
        else:
            a.passive_ticks = max(0, getattr(a, "passive_ticks", 0) - 2)
            a.life_drive = max(0.0, a.life_drive - 0.002)
        # decroissance lente: tout oublie au bout d'env. 4000 ticks
        if tick - getattr(a, "last_meaningful_tick", 0) > 4000:
            a.life_drive = min(1.0, a.life_drive + 0.001)

    # ------------------------------------------------------------------ arbitrage
    def _bias(self, a: Being):
        """Personnalite + emotions + besoins + croyances + risque -> bias de logits."""
        p, e, n = a.personality, a.emotions, a.needs
        ctx = getattr(a, "context", {})
        bias = np.zeros(N_OUT)
        for act in range(N_OUT):
            tr, wgt = ACTION_TRAIT[act]
            bias[act] += wgt * p[tr]
        bias[EXPLORE] -= 0.4 * p[3]
        bias[ATTACK] -= 0.4 * p[5]
        bias[ATTACK] -= 0.3 * p[3]
        bias[REST] -= 0.3 * p[8]
        bias[ATTACK] += 0.7 * e[2] - 0.8 * e[0]
        bias[FLEE] += 0.9 * e[0]
        bias[EXPLORE] -= 0.5 * e[0]
        bias[SLEEP] += 0.3 * e[3]
        bias[TALK] += 0.35 * e[1] + 0.4 * e[7]
        bias[EAT] += (n[0] - 0.70) * 2.6 * (0.4 + 0.6 * p[8]) if n[0] > 0.70 else 0
        if n[0] > 0.90:
            bias[EAT] += 1.6
            bias[SLEEP] = -1.0
        bias[DRINK] += (n[2] - 0.70) * 2.6 if n[2] > 0.70 else 0
        if n[2] > 0.85:
            bias[DRINK] += 1.6
            bias[SLEEP] = -1.0
        if a._loc[4] > 0 and n[2] > 0.45:
            bias[DRINK] += 0.9
        bias[SLEEP] += (n[3] - 0.75) * 2.4 if n[3] > 0.75 else 0
        bias[REST] += (a.energy - 0.22) * -2.8 if a.energy < 0.22 else 0
        # Anti-passivity: un habitant sain et plein d'energie ne devrait
        # presque jamais se reposer, surtout si passif depuis longtemps.
        _life = float(getattr(a, "life_drive", 0.0))
        _ptick = int(getattr(a, "passive_ticks", 0))
        if (a.energy > 0.60 and a.needs[3] < 0.45 and a.pain < 0.25
                and a.emotions[0] < 0.35):
            _pen = 0.9 + 0.8 * _life + min(0.6, _ptick / 400.0)
            bias[REST] -= _pen
            # et rend les activites reelles plus tentantes
            bias[EXPLORE] += 0.25 * _life
            bias[HARVEST] += 0.20 * _life
            bias[SOCIAL] += 0.15 * _life + (0.10 if a._near_agents else 0.0)
            bias[TALK] += 0.10 * _life if a._near_agents else 0.0
            bias[BUILD] += 0.15 * _life
        bias[GIVE] += 0.5 * n[5] * p[0] + 0.4 * p[10]
        bias[BUILD] += 0.4 * n[6] * p[7] + 0.3 * p[9]
        bias[MARK] += 0.3 * n[6]
        bias[HARVEST] += 0.3 * a.skills[0]
        bias[BUILD] += 0.25 * a.skills[1]
        bias[TALK] += 0.2 * a.skills[3]
        bias += 0.5 * a.habits * (1.0 - 0.7 * p[6])
        knows_wood = bool(a.recall("wood", a.tx, a.ty))
        knows_stone = bool(a.recall("stone", a.tx, a.ty))
        has_materials = (
            a.inv.get("bois", 0) > 0 or a.inv.get("pierre", 0) > 0
        )
        if not has_materials and (knows_wood or knows_stone):
            bias[HARVEST] += 0.18
        if ctx.get("wood_density", 0.0) > 0.20:
            bias[HARVEST] += 0.10 * ctx["wood_density"]
        if ctx.get("stone_density", 0.0) > 0.20:
            bias[HARVEST] += 0.08 * ctx["stone_density"]
        if ctx.get("storage_near", 0.0) > 0.3:
            bias[GIVE] += 0.06 * ctx["storage_near"]
        if ctx.get("site_near", 0.0) > 0.3:
            bias[BUILD] += 0.08 * ctx["site_near"]
        if a.inv.get("bois", 0) >= 3 or a.inv.get("pierre", 0) >= 1:
            bias[BUILD] += 0.10
        if a.tool >= 0 and a.tool_durability < 5:
            bias[HARVEST] -= 0.04
            bias[BUILD] += 0.03
        if a.hated is not None:
            t = self._by_eid(a.hated)
            if t is not None:
                d = max(abs(t.tx - a.tx), abs(t.ty - a.ty))
                if d < 14:
                    bias[ATTACK] += (0.6 * e[2] + 0.3 * p[1]) * (1 - d / 14)
        if a.bonded is not None:
            t = self._by_eid(a.bonded)
            if t is not None and not t.child:
                d = max(abs(t.tx - a.tx), abs(t.ty - a.ty))
                if d > 10:
                    bias[SOCIAL] += 0.4 * e[7]
        if self.clock.rain > 0.6:
            bias[SLEEP] += 0.6 * self.clock.rain
            bias[REST] += 0.5 * self.clock.rain
            bias[EXPLORE] -= 0.8 * self.clock.rain
            bias[HARVEST] -= 0.4 * self.clock.rain
        if a._near_monsters:
            nearest = min(a._near_monsters,
                          key=lambda m: (m.x - a.x)**2 + (m.y - a.y)**2)
            if nearest.hostile:
                bias[FLEE] += 1.2
                bias[ATTACK] += 0.3 * e[2]
        for event in list(getattr(a, "observed_actions", ())):
            if self.w.tick - event["tick"] > 1800:
                continue
            if event["reward"] > 0:
                bias[event["action"]] += min(0.08, 0.04 * event["reward"])

        # Territoire doux : pheromones modulent peur, securite, retour foyer
        w = self.w
        phero = float(w.marker[a.ty, a.tx])
        if phero > 0.2:
            bias[REST] += 0.3 * phero
            bias[EXPLORE] -= 0.2 * phero
            bias[SOCIAL] += 0.15 * phero
        if phero > 0.5:
            bias[FLEE] -= 0.3 * phero
            bias[ATTACK] -= 0.2 * phero

        # ── Anima : beliefs + trauma modulent les decisions ──
        anima = a.anima
        trauma_atk = anima["trauma"]["attack"]
        # danger percu local
        cx, cy = a.tx // 8, a.ty // 8
        belief_local = 0.0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                v = anima["beliefs"]["places"].get((cx + dx, cy + dy), 0.0)
                if v > belief_local:
                    belief_local = v
        # trauma → FLEE, evite zones dangereuses
        if trauma_atk > 0.2:
            bias[FLEE] += 0.4 * trauma_atk
            bias[EXPLORE] -= 0.2 * trauma_atk
        # croyance lieu dangereux → FLEE, evite zone
        if belief_local > 0.3:
            bias[FLEE] += 0.3 * belief_local
            bias[HARVEST] -= 0.15 * belief_local
        # identity.fighter → ATTACK plus tentant
        if anima["identity"]["fighter"] > 0.3:
            bias[ATTACK] += 0.2 * anima["identity"]["fighter"]
        # identity.builder → BUILD plus tentant
        if anima["identity"]["builder"] > 0.2:
            bias[BUILD] += 0.15 * anima["identity"]["builder"]
        # identity.explorer → EXPLORE plus tentant
        if anima["identity"]["explorer"] > 0.2:
            bias[EXPLORE] += 0.12 * anima["identity"]["explorer"]

        # ── Lot 4 : valeurs actives ──
        vals = anima.get("values", {})
        survival = float(vals.get("survival", 0.5))
        family = float(vals.get("family", 0.5))
        security = float(vals.get("security", 0.5))
        community = float(vals.get("community", 0.5))
        knowledge = float(vals.get("knowledge", 0.5))
        wealth = float(vals.get("wealth", 0.5))
        generosity = float(vals.get("generosity", 0.5))
        bias[FLEE] += 0.30 * (security - 0.5)
        bias[REST] += 0.12 * (survival - 0.5)
        bias[SLEEP] += 0.12 * (survival - 0.5)
        bias[EAT] += 0.16 * (survival - 0.5)
        bias[DRINK] += 0.16 * (survival - 0.5)
        bias[BUILD] += 0.18 * (security - 0.5) + 0.10 * (family - 0.5)
        bias[GIVE] += 0.22 * (community - 0.5) + 0.24 * (generosity - 0.5)
        bias[TALK] += 0.16 * (community - 0.5)
        bias[SOCIAL] += 0.16 * (family - 0.5) + 0.12 * (community - 0.5)
        bias[EXPLORE] += 0.22 * (knowledge - 0.5)
        bias[HARVEST] += 0.14 * (wealth - 0.5)
        bias[TAKE] += 0.08 * (wealth - 0.5) - 0.12 * (generosity - 0.5)

        # ── Lot D : intention persistante → biais ──
        intent = a.anima.get("intention")
        if intent and intent.get("priority", 0) > 0.3:
            ik = intent.get("kind", "")
            ip = intent["priority"]
            for act_key, bdelta in self.INTENTION_BIAS.get(ik, {}).items():
                bias[act_key] += bdelta * ip

        # ── Lot E : plans courts → biais additionnel ──
        plans = getattr(a, '_cached_plans', None)
        if plans and plans[0].get("score", 0) > 0.2:
            top = plans[0]
            for step in top.get("steps", []):
                if 0 <= step < len(bias):
                    bias[step] += 0.08 * top["score"]

        return bias

    def _feasible(self, a: Being):
        w = self.w
        f = np.zeros(N_OUT, dtype=bool)
        f[REST] = True
        f[EXPLORE] = True
        f[MARK] = a.energy > 0.12
        f[SLEEP] = (a.needs[3] > 0.55 or (self.clock.is_night and a.needs[3] > 0.3)) \
            and a.needs[2] < 0.8 and a.hunger < 0.92 and a.energy > 0.08
        f[EAT] = a.hunger > 0.28 and (bool(a.recall("food", a.tx, a.ty))
                                       or self._has_food_near(a.x, a.y))
        f[HARVEST] = bool(
            a.recall("wood", a.tx, a.ty)
            or a.recall("stone", a.tx, a.ty)
            or a.seen.get("wood")
            or a.seen.get("stone")
        )
        f[DRINK] = a.needs[2] > 0.32 and (a._loc[4] > 0 or bool(a.recall("water", a.tx, a.ty)))
        f[DROP] = a.carry() > 0
        f[BUILD] = ((a.inv.get("bois", 0) >= 3 or a.inv.get("pierre", 0) >= 1)
                     or a.inv.get("graine", 0) > 0) and not a.child
        f[GIVE] = bool(a._near_agents) and a.carry() > 1
        f[TAKE] = bool(a._near_agents) and not a.child
        f[ATTACK] = (
            (bool(a._near_agents) or bool(a._near_sheep) or bool(a._near_monsters))
            and a.energy > 0.25
            and not a.child
        )
        f[FLEE] = (
            a.emotions[0] > 0.35
            and (bool(a._near_agents) or bool(a._near_sheep) or bool(a._near_monsters))
        )
        f[TALK] = any(
            self.can_talk(a, _o)[0]
            and self.choose_talk_topic(a, _o) is not None
            for _o in (a._near_agents or ())
        )
        f[SOCIAL] = bool(a.recall("agent", a.tx, a.ty)) or bool(a._near_agents)
        return f

    def _decide(self, a: Being):
        x = self._sense(a)
        if not np.all(np.isfinite(x)):
            # Perception invalide : pas de délibération, repli REST ce tick.
            self.metrics["invalid_perceptions"] += 1
            a.goal = None
            a.last_decision = {
                "tick": int(self.w.tick), "act": None, "act_name": "—",
                "prob": 0.0, "initial_act": None, "initial_act_name": None,
                "top": [], "feasible": [],
                "reason": "perception invalide — pas de délibération",
            }
            return
        bias = self._bias(a)
        temperature = 0.5 + 0.9 * a.personality[6] + 0.4 * a.emotions[4]
        try:
            with self.perf.measure("brain"):
                act, probs = a.brain.think(
                    x, temperature, bias,
                    curiosity=a.personality[2],
                    caution=a.personality[3],
                )
        except ValueError:
            self.metrics["invalid_perceptions"] += 1
            self.log(f"Perception invalide pour {a.name} : repli REST.",
                     (232, 136, 112))
            a.goal = None
            a.last_decision = {
                "tick": int(self.w.tick), "act": None, "act_name": "—",
                "prob": 0.0, "initial_act": None, "initial_act_name": None,
                "top": [], "feasible": [],
                "reason": "cerveau a rejeté la perception — repli Repos",
            }
            return
        finally:
            self._count_numeric_recoveries()
        f = self._feasible(a)
        initial_act = int(act)
        if not f[act]:
            order = np.argsort(-probs)
            for cand in order:
                if f[cand]:
                    act = int(cand)
                    break
            else:
                act = REST
        self._record_last_decision(a, probs, f, initial_act, int(act))
        a.habits *= 0.992
        a.habits[act] = min(1.0, a.habits[act] + 0.02)
        # Lot M : comptage actions
        from .brain_api import ACTION_NAMES_EXP
        act_name = ACTION_NAMES_EXP.get(act, str(act))
        self.debug_action_counts[act_name] = self.debug_action_counts.get(act_name, 0) + 1
        self._set_goal(a, act)

    def _count_numeric_recoveries(self):
        """Compte (puis remet à zéro) les récupérations NaN/Inf du cerveau.

        Import paresseux : si ``take_numeric_recoveries`` n'existe pas
        encore dans ``game.brain``, on ignore silencieusement.
        """
        try:
            from .brain import take_numeric_recoveries
        except ImportError:
            return
        n = take_numeric_recoveries()
        if n:
            self.metrics["numeric_recoveries"] += n

    def _record_last_decision(self, a: Being, probs, feasible,
                              initial_act: int, act: int):
        """Trace l'action réellement retenue par le moteur (inspecteur).

        Observation pure : lit le vecteur de probabilités du cerveau et le
        masque de faisabilité, sans modifier le but, le cerveau ou l'état
        de l'agent. Toute erreur est avalée : le diagnostic ne casse jamais
        la délibération.
        """
        try:
            from .brain_api import ACTION_NAMES_EXP
            names = ACTION_NAMES_EXP
            p = np.asarray(probs, dtype=float)
            order = np.argsort(-p)
            top = [{
                "act": int(i),
                "name": str(names.get(int(i), f"Action {int(i)}")),
                "prob": float(p[i]),
                "feasible": bool(feasible[i]),
            } for i in order[:8]]
            feasible_names = [str(names.get(int(i), f"Action {int(i)}"))
                              for i in range(len(feasible)) if feasible[i]]
            init_name = str(names.get(initial_act,
                                      f"Action {initial_act}"))
            act_name = str(names.get(act, f"Action {act}"))
            if act == initial_act:
                reason = "choix direct du cerveau (action faisable)"
            elif act == REST:
                reason = "aucune action faisable — repli Repos"
            else:
                reason = f"« {init_name} » non faisable — repli sur la meilleure alternative"
            score = float(p[act]) if 0 <= act < len(p) else 0.0
            a.last_decision = {
                "tick": int(self.w.tick),
                "act": int(act),
                "act_name": act_name,
                "prob": score,
                "initial_act": int(initial_act),
                "initial_act_name": init_name,
                "initial_prob": (float(p[initial_act])
                                 if 0 <= initial_act < len(p) else 0.0),
                "top": top,
                "feasible": feasible_names[:8],
                "reason": reason,
            }
            # Vérité de sélection : enregistrée ici, au moment précis du
            # choix moteur (et non au rendu). Score réel du candidat retenu.
            a.last_selection_tick = int(self.w.tick)
            a.last_selection_reason = f"{reason} — score {score:.3f}"
        except Exception:
            self.metrics["unhandled_action_errors"] += 1
            a.last_decision = None

    def _capture_decision_trace(self, a: Being):
        """Enregistre les candidats réellement évalués pour l'inspecteur.

        Toute erreur est avalée : le diagnostic ne doit jamais casser la
        simulation. La trace est lue telle quelle par le snapshot, l'UI ne
        recalcule jamais les candidats.
        """
        try:
            a.decision_trace = evaluate_candidates(self, a)
        except Exception:
            self.metrics["unhandled_action_errors"] += 1
            a.decision_trace = []

    def _known_or_universal(self, a, category, tx, ty):
        personal = a.recall(category, tx, ty)
        if personal is not None:
            return personal
        clan_places = self.clan_knowledge.nearby_places(category, tx, ty, max_dist=100)
        if clan_places:
            best = clan_places[0]
            return best[0], best[1], best[3]
        fact = self.universal_knowledge.nearest(category, tx, ty, tick=self.w.tick)
        if fact is None:
            return None
        return fact.tx, fact.ty, max(abs(fact.tx - tx), abs(fact.ty - ty))

    def _set_goal(self, a, act):
        w = self.w
        tx, ty = a.tx, a.ty
        strategy = getattr(a.brain, '_strategy', IMMEDIAT)
        target = getattr(a.brain, '_target', SOI)
        g = {"act": act, "x": tx, "y": ty, "ref": None, "intensity": 1.0,
             "until": w.tick + 420}
        if act == EAT:
            m = self._known_or_universal(a, "food", tx, ty)
            if not m:
                a.goal = None
                return
            g["x"], g["y"] = m[0], m[1]
        elif act == DRINK:
            m = self._known_or_universal(a, "water", tx, ty)
            if m:
                wx, wy = m[0], m[1]
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        nx2, ny2 = wx + dx, wy + dy
                        if 0 <= nx2 < GRID and 0 <= ny2 < GRID and self.w.land[ny2, nx2] \
                           and not self.w.blocked[ny2, nx2]:
                            wx, wy = nx2, ny2
                            break
                    else:
                        continue
                    break
                g["x"], g["y"] = wx, wy
        elif act == HARVEST:
            if target == BOIS:
                mw = self._known_or_universal(a, "wood", tx, ty)
                m = mw
            elif target == PIERRE:
                ms = self._known_or_universal(a, "stone", tx, ty)
                m = ms
            else:
                mw = self._known_or_universal(a, "wood", tx, ty)
                ms = self._known_or_universal(a, "stone", tx, ty)
                m = None
                if mw and ms:
                    m = ms if (a.inv["pierre"] < 2 and ms[2] <= mw[2] * 2.2) or a.inv["bois"] >= 6 else mw
                else:
                    m = mw or ms
            if not m:
                a.goal = None
                return
            g["x"], g["y"] = m[0], m[1]
        elif act in (SOCIAL, GIVE, TAKE, TALK, ATTACK):
            if a._near_agents:
                if act == ATTACK:
                    e = max(a._near_agents, key=lambda t: t.health)
                elif act in (SOCIAL, GIVE, TALK):
                    e = max(a._near_agents,
                            key=lambda o: a.anima_social_score(o.eid))
                else:
                    e = a._near_agents[0]
                g["x"], g["y"], g["ref"] = e.tx, e.ty, e
            elif act == ATTACK and a._near_sheep:
                e = a._near_sheep[0]
                g["x"], g["y"], g["ref"] = e.tx, e.ty, e
            elif act == ATTACK and a._near_monsters:
                e = max(a._near_monsters, key=lambda m: m.health)
                g["x"], g["y"], g["ref"] = e.tx, e.ty, e
            elif act == SOCIAL and a.bonded is not None:
                t = self._by_eid(a.bonded)
                if t:
                    g["x"], g["y"], g["ref"] = t.tx, t.ty, t
                else:
                    a.bonded = None
                    a.goal = None
                    return
            else:
                m = a.recall("agent", tx, ty)
                if not m:
                    a.goal = None
                    return
                g["x"], g["y"] = m[0], m[1]
        elif act == FLEE:
            t = (a._near_agents or a._near_sheep or [None])[0]
            if t is None:
                a.goal = None
                return
            ang = math.atan2(a.y - t.y, a.x - t.x)
            g["x"] = int(np.clip(tx + math.cos(ang) * 18, 2, GRID - 3))
            g["y"] = int(np.clip(ty + math.sin(ang) * 18, 2, GRID - 3))
            if not w.land[g["y"], g["x"]]:
                g["x"], g["y"] = tx, ty
        elif act == EXPLORE:
            best, bs = None, 1e9
            for ang in np.arange(0, 6.283, 0.785):
                fx = int(np.clip(tx + math.cos(ang) * 14, 2, GRID - 3))
                fy = int(np.clip(ty + math.sin(ang) * 14, 2, GRID - 3))
                if not w.land[fy, fx]:
                    continue
                dan = a.belief_places.get((fx // 8, fy // 8), 0.0)
                sc = float(w.heat[fy, fx]) + dan * 2.0
                if sc < bs:
                    best, bs = (fx, fy), sc
            if best is None:
                a.goal = None
                return
            g["x"], g["y"] = best
            g["until"] = self.w.tick + 900
        elif act == SLEEP:
            m = self._known_or_universal(a, "shelter", tx, ty)
            if m is None and a.home:
                m = a.home
            if m:
                g["x"], g["y"] = m[0], m[1]
            else:
                g["x"], g["y"] = tx, ty
        elif act == BUILD:
            if target == DEPOT_CHANTIER:
                site = self.nearest_site(a.tx, a.ty, max_dist=20)
                if site is not None:
                    g["x"], g["y"] = site.origin_tx, site.origin_ty
                else:
                    storage = self.nearest_storage(a.tx, a.ty, max_dist=20)
                    if storage is not None:
                        g["x"], g["y"] = storage.tx, storage.ty
                    else:
                        new_site = self.create_house_site(a)
                        if new_site is None:
                            a.goal = None
                            return
                        g["x"], g["y"] = new_site.origin_tx, new_site.origin_ty
            elif target == ABRI:
                m = self._known_or_universal(a, "shelter", tx, ty)
                if m and m[2] < 14 and self.rng.random() < 0.7:
                    g["x"], g["y"] = m[0], m[1]
            else:
                m = self._known_or_universal(a, "shelter", tx, ty)
                if m and m[2] < 14 and self.rng.random() < 0.7:
                    g["x"], g["y"] = m[0], m[1]
        if self.target_is_blocked(a, act, g["x"], g["y"]):
            a.goal = None
            return
        if strategy == PRUDENT:
            danger = a.belief_places.get((g["x"] // 8, g["y"] // 8), 0.0)
            if danger > 0.45:
                a.goal = None
                return
        a.goal = g
        a.goal_t = 0
        a.stuck = 0
        a._last_px, a._last_py = a.x, a.y

    def fallback_goal(self, a, reason="aucune_cible"):
        """Repli contextuel court (Phase 2A) quand aucun but n'a pu être posé.

        Contrat : pose un but REST bref sur la case courante de l'agent
        (``until`` = tick + 60, donc expiré proprement par ``_execute``),
        ne lève jamais d'exception et est idempotent : si un but existe
        déjà, il est conservé tel quel. ``reason`` trace la cause dans les
        compteurs d'activité.
        """
        w = self.w
        if a.goal is not None:
            return a.goal
        able = (not a.child and a.energy > 0.55 and a.hunger < 0.65
                and a.needs[2] < 0.70 and a.needs[3] < 0.55
                and a.pain < 0.30 and a.emotions[0] < 0.40
                and self.clock.rain < 0.6)
        if able and float(getattr(a, "life_drive", 0.0)) > 0.3:
            # Exploration locale bornee: une tuile dans les 8 directions,
            # jamais de scan global.
            import math as _m
            tx0, ty0 = int(a.tx), int(a.ty)
            for ang_i in range(8):
                ang = ang_i * 0.785398
                gx = int(tx0 + _m.cos(ang) * 10)
                gy = int(ty0 + _m.sin(ang) * 10)
                gx = max(1, min(self.w.g - 2, gx))
                gy = max(1, min(self.w.g - 2, gy))
                danger = float(a.belief_places.get((gx // 8, gy // 8), 0.0))
                if danger > 0.4:
                    continue
                if not self.w.land[gy, gx] or self.w.blocked[gy, gx]:
                    continue
                g = {"act": EXPLORE, "x": gx, "y": gy, "ref": None,
                     "intensity": 0.6, "until": self.w.tick + 600}
                a.goal = g
                a.goal_t = 0
                a.stuck = 0
                a._last_px, a._last_py = a.x, a.y
                self.metrics["lifedrive_explore_start"] += 1
                return g
        # sinon: comportement REST d'origine
        try:
            tx, ty = int(a.tx), int(a.ty)
        except (ValueError, OverflowError):
            # position corrompue (NaN/Inf) : on se replace au centre
            tx = ty = w.g // 2
        if not w.inb(tx, ty):
            tx = min(max(tx, 0), w.g - 1)
            ty = min(max(ty, 0), w.g - 1)
        g = {"act": REST, "x": tx, "y": ty, "ref": None, "intensity": 0.6,
             "until": w.tick + 60}
        a.goal = g
        a.goal_t = 0
        a.stuck = 0
        a._last_px, a._last_py = a.x, a.y
        self.metrics["fallback_goals"] += 1
        self.activity_reasons[f"fallback:{reason}"] += 1
        return g

    def register_goal_failure(self, a, reason="blocked"):
        goal = a.goal or {}
        key = (goal.get("act"), goal.get("x"), goal.get("y"))
        count, until = a.failed_targets.get(key, (0, 0))
        count += 1
        cooldown = min(1800, 180 * count)
        a.failed_targets[key] = (count, self.w.tick + cooldown)
        # Vérité « dernier échec » au moment de l'échec (n'efface pas le
        # dernier choix de sélection).
        try:
            a.last_failure_reason = str(reason)
            a.last_failure_tick = int(self.w.tick)
        except AttributeError:
            pass
        a.goal = None
        a.stuck = 0
        a.emotions[3] = min(1.0, a.emotions[3] + 0.04)
        self.activity_reasons[reason] += 1
        self._reward(a, -0.03)

    def target_is_blocked(self, a, act, tx, ty):
        count, until = a.failed_targets.get((act, tx, ty), (0, 0))
        return self.w.tick < until

    # ------------------------------------------------------------------ depots
    def nearest_storage(self, tx, ty, max_dist=12):
        best, best_distance = None, 10**9
        for storage in self.w.storages.values():
            distance = max(abs(storage.tx - tx), abs(storage.ty - ty))
            if distance <= max_dist and distance < best_distance:
                best, best_distance = storage, distance
        return best

    def create_storage(self, a, tx, ty, capacity=80):
        from .storage import SharedStorage
        if (tx, ty) in self.w.storages:
            return self.w.storages[(tx, ty)]
        storage = SharedStorage(tx=tx, ty=ty, capacity=capacity, owner_clan=a.color)
        self.w.storages[(tx, ty)] = storage
        return storage

    def _note_institution(self, kind, tx, ty, eid, action=None):
        """Émergence d'institution (Lot E) : membre + pratique répétée.

        Gate runtime ``institutions_enabled`` ; n'émet ``lab.event`` +
        journal que lors de la création effective.
        """
        if not self.runtime.get("institutions_enabled", True):
            return
        ck = self.clan_knowledge
        tx, ty = int(tx), int(ty)
        key = (kind, tx // 8, ty // 8)
        created = key not in ck.institutions
        ck.add_institution(kind, tx, ty, eid, self.w.tick)
        if action:
            ck.record_practice(kind, tx, ty, eid, action, self.w.tick)
        if created:
            self.lab.event(self.w.tick, "institution",
                           inst_kind=kind, tx=tx, ty=ty, eid=eid)
            self.log(f"Nouvelle institution : {kind} en ({tx},{ty}).",
                     (160, 112, 198), "social")

    def deposit_to_storage(self, a, storage):
        material = max(a.inv, key=a.inv.get)
        if a.inv.get(material, 0) <= 0:
            return False
        moved = storage.deposit(a.eid, material, min(2, a.inv[material]), self.w.tick)
        if moved <= 0:
            return False
        a.inv[material] -= moved
        a.skills[3] = min(1.0, a.skills[3] + 0.01)
        a.rep += 0.05
        self._reward(a, 0.08)
        self.lab.event(self.w.tick, "storage_deposit",
                       eid=a.eid, tx=storage.tx, ty=storage.ty,
                       material=material, amount=moved)
        self._note_institution("shared_storage", storage.tx, storage.ty,
                               a.eid, action="deposit")
        self._record_anima(
            a, "resource_deposited", (storage.tx, storage.ty),
            actors=[a.eid], action="deposit", outcome="success",
            achievement=0.05)
        a.record_meaningful(self.w.tick, "deposit")
        return True

    def withdraw_from_storage(self, a, storage, material):
        if a.inv.get(material, 0) >= INV_CAP:
            return False
        moved = storage.withdraw(a.eid, material, min(2, INV_CAP - a.inv.get(material, 0)), self.w.tick)
        if moved <= 0:
            return False
        a.inv[material] = a.inv.get(material, 0) + moved
        self.lab.event(self.w.tick, "storage_withdraw",
                       eid=a.eid, tx=storage.tx, ty=storage.ty,
                       material=material, amount=moved)
        self._note_institution("shared_storage", storage.tx, storage.ty,
                               a.eid, action="withdraw")
        self._record_anima(
            a, "resource_withdrawn", (storage.tx, storage.ty),
            actors=[a.eid], action="withdraw", outcome="success")
        return True

    def update_reputation(self, agent):
        """Lot F : maj anima["reputation"] depuis a.rep + a.rel (plan §3.4)."""
        positive = 0.0
        negative = 0.0
        for relation in agent.rel.values():
            if isinstance(relation, (tuple, list)):
                positive += max(0.0, float(relation[0]))
                negative += max(0.0, -float(relation[0]))
        agent.anima["reputation"] = {
            "social": max(-1.0, min(1.0, agent.rep / 10.0)),
            "trust_balance": positive - negative,
            "updated_tick": int(self.w.tick),
        }

    # ------------------------------------------------------------------ agent
    # ------------------------------------------------------------------ instinct de survie
    def _choose_food_exploration_tile(self, agent):
        """Choisit EXACTEMENT une tuile d'exploration atteignable,
        bornée aux régions immédiates, en favorisant faible familiarité
        et nourriture connue dans ``region_memory``. Ne scanne jamais
        la carte entière et ne téléporte pas l'habitant.
        """
        rx, ry = (agent.tx // self.REGION_SIZE,
                    agent.ty // self.REGION_SIZE)
        candidates = []
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nrx, nry = rx + dx, ry + dy
                memory = agent.region_memory.get((nrx, nry), {})
                familiarity = float(memory.get("familiarity", 0.0))
                danger = float(memory.get("danger", 0.0))
                resources = set(memory.get("resources", []))
                tx = min(max(nrx * self.REGION_SIZE + self.REGION_SIZE // 2, 2),
                         self.w.g - 3)
                ty = min(max(nry * self.REGION_SIZE + self.REGION_SIZE // 2, 2),
                         self.w.g - 3)
                if not self.w.land[ty, tx] or self.w.blocked[ty, tx]:
                    continue
                score = 0.55 * (1.0 - familiarity) - 0.40 * danger
                if "food" in resources:
                    score += 0.25
                if agent.hunger > 0.82:
                    score += 0.10 * (1.0 - familiarity)
                candidates.append((score, tx, ty))
        if not candidates:
            return None
        best = max(candidates, key=lambda row: row[0])
        return (best[1], best[2])

    def _try_survival_talk(self, agent, category: str) -> bool:
        """Utilise le flux TALK existant quand un habitant proche et
        de confiance peut transmettre une information r�elle
        (nourriture ou eau). Ne cr�e aucune connaissance artificielle."""
        speaker = None
        for other in agent._near_agents:
            if not getattr(other, "alive", False):
                continue
            if agent.trust(other.eid) < 0.3:
                continue
            if self.best_shareable_memory(other, category) is not None:
                speaker = other
                break
        if speaker is None:
            return False
        try:
            return self.do_talk(speaker, agent)
        except Exception:
            return False

    def enforce_survival_priority(self, agent) -> bool:
        """Instinct de survie hi�rarchique (faim → soif → danger).

        Retourne ``True`` uniquement quand une action de survie r�elle
        a �t� pos�e ou avanc�e. Doit �tre appel� dans ``_agent`` apr�s
        la gestion des dangers imm�diats et avant le choix normal du
        cerveau.

        Ne remplace pas une exp�dition valide, ne court-circuite pas la
        soif critique et ne g�re pas la fuite (elle existe d�j�).
        """
        a = agent
        if not a.alive:
            return False
        hunger = float(a.hunger)
        thirst = float(a.needs[2])

        # 1. Pas d'urgence → on ne touche � rien.
        if hunger < 0.70 and thirst < 0.82:
            return False

        # Danger imm�diat : laisser la fuite exister.
        if a._near_monsters:
            return False

        # Activit� de survie d�j� en cours → la laisser avancer.
        if a.activity is not None and a.activity.kind in (
                "food_expedition", "water_search"):
            return False

        # Ne pas �craser un but de mouvement valide (fuite, EXPLORE
        # en cours, DRINK vers de l'eau).
        g = a.goal
        goal_valid = (g is not None and g.get("until", 0) > self.w.tick)
        if goal_valid:
            act = g.get("act")
            if act == DRINK and thirst >= hunger:
                return False
            if (
                act == EXPLORE
                and a.activity is not None
                and a.activity.kind in (
                    "food_expedition",
                    "water_search",
                    "explore_region",
                )
            ):
                return False

        # ====== FAIM ======
        if hunger >= 0.70:
            # 2. Nourriture atteignable localement → manger/récolter.
            if self._has_food_near(a.x, a.y, radius_px=40):
                try:
                    if self.try_harvest_or_pickup_near(a):
                        return True
                except Exception as exc:
                    self.metrics["survival_recovery_error"] = \
                        self.metrics.get("survival_recovery_error", 0) + 1
                    self.record_activity_failure(
                        a, "survival", f"{type(exc).__name__}")
                    return False

            # 3. M�moire fiable de nourriture → exp�dition.
            if self.maybe_start_food_expedition(a):
                self.activity_reasons["food_expedition:survival"] += 1
                return True

            # 4. faim >= 0.82 → demander une indication utile � un
            #    habitant proche de confiance (flux TALK existant).
            if hunger >= 0.82:
                if self._try_survival_talk(a, "food"):
                    return True

# 5. faim >= 0.78 et aucune expédition possible →
            #    exploration alimentaire bornée.
            if (
                hunger >= 0.78
                and (
                    a.activity is None
                    or a.activity.kind != "explore_region"
                )
            ):
                if self.maybe_start_explore_region(a):
                    return True

            # Antichute anti-bloquage : fixer exactement une tuile
            # d'exploration atteignable via la mémoire régionale.
            if (
                a.activity is None
                and (
                    a.goal is None
                    or a.stuck > 15
                )
            ):
                target = self._choose_food_exploration_tile(a)
                if target is not None:
                    self.set_goal_to_tile(a, EXPLORE, target[0], target[1])
                    a.stuck = 0
                    return True

        return False

    def _agent(self, a: Being):
        w = self.w
        a.age += 1
        a.repro_cd = max(0, a.repro_cd - 1)
        a.atk_t = max(0, a.atk_t - 1)
        a.goal_t += 1
        a.pain = max(0.0, a.pain - 0.0004)

        # Phase 2: candidats pour l'inspecteur (Phase 1 diagnostic).
        # Capturés AVANT le dispatch d'activité : les branches à retour
        # anticipé (activité en cours, priorités 1-4) sautent l'appel plus
        # bas, et la trace resterait vide pour tout agent occupé.
        if self._should_generate_candidates(a):
            self._capture_decision_trace(a)

        # PART B: ActivityState - vérifier activité en cours
        if a.activity is not None:
            handled = False
            if a.activity.kind == "food_expedition":
                handled = self.step_food_expedition(a)
            elif a.activity.kind == "water_search":
                handled = self.step_water_search(a)
            elif a.activity.kind == "return_home":
                handled = self.step_return_home(a)
            elif a.activity.kind == "explore_region":
                handled = self.step_explore_region(a)
            if handled:
                # L'activité a géré ce tick, on saute la décision normale
                self._metabolize(a)
                if self._check_vital_death(a):
                    return
                after = self._wellbeing(a)
                delta = after - getattr(a, 'prev_wellbeing', after)
                if abs(delta) > 0.001:
                    self._reward(a, 0.08 * delta)
                a.prev_wellbeing = after
                # Exécuter le but de mouvement si l'activité en a posé un
                if a.goal is not None and a.goal["act"] in (EXPLORE, DRINK, SLEEP, REST):
                    self._execute(a)
                return

        # Priorité 1: water_search si soif critique (≥ 0.85) - interrompt autres activités non-vitales
        critical_thirst = a.needs[2] >= 0.85
        if critical_thirst and self.maybe_start_water_search(a):
            self._metabolize(a)
            if self._check_vital_death(a):
                return
            after = self._wellbeing(a)
            delta = after - getattr(a, 'prev_wellbeing', after)
            if abs(delta) > 0.001:
                self._reward(a, 0.08 * delta)
            a.prev_wellbeing = after
            return

        # Priorité 2: food_expedition
        if self.maybe_start_food_expedition(a):
            self._metabolize(a)
            if self._check_vital_death(a):
                return
            after = self._wellbeing(a)
            delta = after - getattr(a, 'prev_wellbeing', after)
            if abs(delta) > 0.001:
                self._reward(a, 0.08 * delta)
            a.prev_wellbeing = after
            return

        # Priorité 3: return_home
        if self.maybe_start_return_home(a):
            self._metabolize(a)
            if self._check_vital_death(a):
                return
            after = self._wellbeing(a)
            delta = after - getattr(a, 'prev_wellbeing', after)
            if abs(delta) > 0.001:
                self._reward(a, 0.08 * delta)
            a.prev_wellbeing = after
            return

        # Priorité 4: explore_region
        if self.maybe_start_explore_region(a):
            self._metabolize(a)
            if self._check_vital_death(a):
                return
            after = self._wellbeing(a)
            delta = after - getattr(a, 'prev_wellbeing', after)
            if abs(delta) > 0.001:
                self._reward(a, 0.08 * delta)
            a.prev_wellbeing = after
            return

        # Instinct de survie (faim / soif) — avant le choix
        # normal du cerveau.
        if self.enforce_survival_priority(a):
            return

        # VOLONTE : le but persiste (engagement). On ne re-delibere que si :
        # but fini/expiré/bloque, urgence viscerale, ou mollesse (petit cerveau
        # en veille). Un grand cerveau stratege va au bout de sa tache.
        g = a.goal
        expired = g is not None and w.tick > g["until"]
        soft = g is not None and g["act"] in (REST, MARK, SOCIAL, TALK)
        urgent = (a.hunger > 0.85 or a.needs[2] > 0.85 or a.energy < 0.12
                  or a.emotions[0] > 0.7 or a.pain > 0.6)
        if self.w.tick - a.born_tick < 240:
            memories = (
                a.seen.get("food", []) + a.seen.get("wood", [])
                + a.seen.get("stone", []) + a.seen.get("water", [])
            )
            if not memories:
                self.bootstrap_resource_memory(a, radius=12)

        # Phase 2: régénération des plans selon la fréquence
        if self._should_generate_plans(a):
            a._cached_plans = self._generate_plans(a)
            a.anima["plan"] = dict(a._cached_plans[0]) if a._cached_plans else None
            a._cached_plans_tick = self.w.tick

        # Phase 2: candidats pour l'inspecteur : capturés en tête d'_agent.

        if g is None or expired or a.stuck > 20 + 50 * a.personality[8]:
            self._decide(a)
        elif a.goal_t % a.brain.te == 0:
            if urgent and self.rng.random() > 0.25:
                self._decide(a)
            elif soft and a.goal_t > 60 and self.rng.random() > \
                    (0.4 + 0.5 * a.personality[4] - 0.4 * a.personality[6]):
                self._decide(a)
        if a.goal is None:
            self.update_life_drive(a)
            # Un habitant sain sous forte pression de vie cherche une
            # opportunite reelle AVANT de se reposer.
            ld = float(getattr(a, "life_drive", 0.0))
            launched = False
            if ld > 0.35 and not a.child:
                if self.maybe_start_food_expedition(a):
                    launched = True
                elif self.maybe_start_explore_region(a):
                    launched = True
            if launched:
                # L'activité gère ses propres buts : sortie identique aux
                # autres branches d'activité (pas d'_execute sans but).
                self._metabolize(a)
                if self._check_vital_death(a):
                    return
                after = self._wellbeing(a)
                delta = after - getattr(a, 'prev_wellbeing', after)
                if abs(delta) > 0.001:
                    self._reward(a, 0.08 * delta)
                a.prev_wellbeing = after
                return
            # repli contextuel court (Phase 2A) — plus de repos de 300 ticks
            self.fallback_goal(a)

        self._execute(a)
        self._metabolize(a)

        self.update_life_drive(a)

        after = self._wellbeing(a)
        delta = after - getattr(a, 'prev_wellbeing', after)
        if abs(delta) > 0.001:
            self._reward(a, 0.08 * delta)
        a.prev_wellbeing = after

        # ── Lot D : generation d'intentions (tous les 200 ticks) ──
        if w.tick % 200 == 0 and not a.anima_intention_valid(w.tick):
            self._generate_intention(a)
        # ── Lot F+H : décroissance traces causales + observation learning ──
        if w.tick % 150 == 0:
            a.anima_decay_causal_traces()
            a.anima_apply_observation_learning()

        if a.age >= a.natural_death_age:
            self._die(a, cause="vieillesse")
        else:
            self._check_vital_death(a)

    def _generate_intention(self, a: Being):
        """Génère une intention Anima basée sur l'état courant."""
        w = self.w
        vals = a.anima.get("values", {})
        trauma = a.anima.get("trauma", {})
        # priorité par besoin
        if a.hunger > 0.7:
            a.anima_set_intention("secure_food", "faim", priority=0.7,
                                  tick=w.tick, duration=600)
        elif trauma.get("loss", 0) > 0.2:
            a.anima_set_intention("recover_from_loss", "deuil", priority=0.5,
                                  tick=w.tick, duration=800)
        elif trauma.get("attack", 0) > 0.3:
            a.anima_set_intention("avoid_danger", "peur", priority=0.6,
                                  tick=w.tick, duration=400)
        elif a.home is None and a.inv.get("bois", 0) >= 2:
            a.anima_set_intention("build_home", "sans abri", priority=0.6,
                                  tick=w.tick, duration=1000)
        elif vals.get("community", 0.5) > 0.6 and a._near_agents:
            target = max(a._near_agents,
                         key=lambda o: a.anima_social_score(o.eid))
            a.anima_set_intention("help_ally", "communauté",
                                  target=target.eid, priority=0.4,
                                  tick=w.tick, duration=500)
        elif vals.get("knowledge", 0.5) > 0.6:
            a.anima_set_intention("explore_unknown", "curiosité",
                                  priority=0.35, tick=w.tick, duration=600)

    # ── Lot E : plans courts et alternatives ──

    def _generate_plans(self, a: Being):
        """Génère 1 à 4 plans alternatifs de 1-3 étapes."""
        w = self.w
        plans = []
        f = self._feasible(a)
        vals = a.anima.get("values", {})
        ident = a.anima.get("identity", {})
        trauma_sum = sum(a.anima.get("trauma", {}).values())
        # plan 1: nourriture
        if f[HARVEST]:
            plans.append({
                "steps": [HARVEST, DROP],
                "need_gain": 0.3 * (1.0 - a.hunger),
                "value_fit": vals.get("wealth", 0.5) * 0.2,
                "identity_fit": ident.get("provider", 0) * 0.15,
                "risk": 0.05, "energy_cost": 0.1,
                "social_gain": 0.0, "confidence": 0.6,
            })
        # plan 2: construire
        if f[BUILD]:
            plans.append({
                "steps": [BUILD],
                "need_gain": 0.2 * (1.0 if a.home is None else 0.1),
                "value_fit": vals.get("security", 0.5) * 0.25,
                "identity_fit": ident.get("builder", 0) * 0.2,
                "risk": 0.02, "energy_cost": 0.15,
                "social_gain": 0.0, "confidence": 0.5,
            })
        # plan 3: aide sociale
        if f[GIVE] and a._near_agents:
            plans.append({
                "steps": [GIVE],
                "need_gain": 0.05,
                "value_fit": vals.get("community", 0.5) * 0.3 + vals.get("generosity", 0.5) * 0.2,
                "identity_fit": ident.get("provider", 0) * 0.1,
                "risk": 0.03, "energy_cost": 0.05,
                "social_gain": 0.25, "confidence": 0.4,
            })
        # plan 4: explorer
        if f[EXPLORE]:
            plans.append({
                "steps": [EXPLORE],
                "need_gain": 0.1,
                "value_fit": vals.get("knowledge", 0.5) * 0.3,
                "identity_fit": ident.get("explorer", 0) * 0.2,
                "risk": 0.15, "energy_cost": 0.12,
                "social_gain": 0.0, "confidence": 0.35,
            })
        # score et trie
        for p in plans:
            p["score"] = (
                p["need_gain"] + p["value_fit"] + p["identity_fit"]
                + p["social_gain"] + p["confidence"]
                - p["risk"] - p["energy_cost"] - 0.1 * trauma_sum
            )
        plans.sort(key=lambda p: p["score"], reverse=True)
        return plans[:4]

    def _wellbeing(self, a):
        return (
            0.30 * a.health
            + 0.25 * a.energy
            + 0.25 * (1.0 - a.hunger)
            + 0.20 * (1.0 - a.needs[2])
        )

    def _metabolize(self, a: Being):
        w = self.w
        act = a.goal["act"] if a.goal else REST
        night = self.clock.is_night
        n = a.needs
        n[0] = min(1.0, n[0] + HUNGER_RATE * (1.3 if act != REST else 1.0))
        n[2] = min(1.0, n[2] + THIRST_RATE * (0.5 + self.clock.temp))
        n[3] = min(1.0, n[3] + (SLEEP_RATE_N if night else SLEEP_RATE_D))
        a.hunger = n[0]
        if act == REST:
            a.energy += REST_GAIN * (SHELTER_BONUS if w.shelter[a.ty, a.tx] else 1.0) \
                * (0.6 + 0.8 * a.body[1])
            a.state = "rest"
        elif act == SLEEP:
            sh = w.shelter[a.ty, a.tx]
            a.energy += SLEEP_GAIN * (1.6 if sh else 1.0) * (0.5 + a.body[4])
            n[3] = max(0.0, n[3] - 0.004)
            a.health += 0.0009 * (2.0 if sh else 1.0)
            a.state = "sleep"
            if a.pain > 0.5 or a.emotions[0] > 0.6 or (not night and n[3] < 0.2):
                a.goal = None
                if self.rng.random() < 0.3:
                    a.remember_event("dream", "chasse")
        else:
            a.energy -= E_DRAIN * (1.4 if self.clock.temp < 0.3 else 1.0)
        if n[2] > 0.9:
            a.health -= THIRST_HP
        if a.hunger >= 1.0:
            a.health -= STARVE_HP
        if a.energy < 0.04:
            a.health -= LOWE_HP
        # vieillissement : fragilité progressive après 65 ans
        a.health = min(a.health, a.age_health_cap())
        a.energy = min(1.0, max(0.0, a.energy))
        a.health = min(1.0, a.health)
        a.needs[1] = a.energy
        # appartenance : la solitude ronge ; estime de soi derive de la reputation
        if a._near_agents:
            n[5] = max(0.0, n[5] - 0.00025)
        else:
            n[5] = min(1.0, n[5] + 0.00012 * (0.5 + a.personality[0]))
        a.self_esteem += 0.0002 * (np.clip(a.rep / 10.0, -1, 1) - a.self_esteem)
        # decantation emotionnelle
        e = a.emotions
        e[0] = max(0.0, e[0] * 0.996 - 0.0002)
        e[1] += (0.3 - e[1]) * 0.0008
        e[2] = max(0.0, e[2] * 0.997)
        e[3] += (0.15 + 0.4 * (1 - e[1]) - e[3]) * 0.0005
        e[4] = min(1.0, 0.4 * a.hunger + 0.3 * e[0] + 0.3 * max(0.0, 0.2 - a.energy)
                   + 0.4 * n[2] + 0.3 * n[3])
        e[5] = max(0.0, e[5] * 0.99)
        e[6] = max(0.0, e[6] * 0.99)
        e[7] = max(0.0, e[7] * 0.999)
        a.anim_t += 1

    # ------------------------------------------------------------------ execution
    def _execute(self, a: Being):
        w = self.w
        g = a.goal
        act, gx, gy = g["act"], g["x"], g["y"]
        if w.tick > g["until"]:
            a.goal = None
            return
        ref = g.get("ref")
        if isinstance(ref, Being) and not ref.alive:
            a.goal = None
            return
        dx, dy = gx * TILE + 8 - a.x, gy * TILE + 8 - a.y
        dist = max(abs(dx), abs(dy))
        adjacent = dist <= (26 if act == DRINK else 16)

        if act not in (REST, SLEEP, MARK) and not adjacent:
            moved = abs(a.x - a._last_px) + abs(a.y - a._last_py)
            a.stuck = a.stuck + 1 if moved < 1.5 else 0
            a._last_px, a._last_py = a.x, a.y
            if a.stuck > 20 + 50 * a.personality[8]:
                a.emotions[3] = min(1.0, a.emotions[3] + 0.1)
                cat = {EAT: "food", DRINK: "water", HARVEST: "wood",
                       SOCIAL: "agent", SLEEP: "shelter"}.get(act)
                if cat:
                    a.forget(cat, gx, gy)
                    if cat == "wood":
                        a.forget("stone", gx, gy)
                self.register_goal_failure(a, "path")
                return
            d = math.hypot(dx, dy) or 1
            sp = a.speed(self.clock.light, float(w.heat[a.ty, a.tx]))
            if a.stuck > 12:
                def is_goal(tx, ty):
                    return (tx, ty) == (gx, gy) or (abs(tx - gx) <= 1 and abs(ty - gy) <= 1)
                step_x, step_y = self._local_bfs(a.tx, a.ty, is_goal, max_r=20)
                if step_x == 0 and step_y == 0:
                    self.register_goal_failure(a, "local_path_failed")
                    return
                target_wx = (a.tx + step_x) * TILE + 8
                target_wy = (a.ty + step_y) * TILE + 8
                ndx, ndy = target_wx - a.x, target_wy - a.y
                nd = math.hypot(ndx, ndy) or 1
                a.set_dir(ndx / nd * sp, ndy / nd * sp)
                self._move(a, ndx / nd * sp, ndy / nd * sp)
                a.energy -= MOVE_DRAIN * a.drain_f()
                a.state = "run"
                return
            elif a.stuck > 4:
                best_d, best_move = 1e9, (0, 0)
                for ddx, ddy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)):
                    ntx, nty = a.tx + ddx, a.ty + ddy
                    if 0 <= ntx < w.g and 0 <= nty < w.g and not w.blocked[nty, ntx]:
                        d2 = (ntx - gx)**2 + (nty - gy)**2
                        if d2 < best_d:
                            best_d = d2
                            best_move = (ddx, ddy)
                if best_move != (0, 0):
                    bdx, bdy = best_move
                    target_wx = (a.tx + bdx) * TILE + 8
                    target_wy = (a.ty + bdy) * TILE + 8
                    ndx, ndy = target_wx - a.x, target_wy - a.y
                    nd = math.hypot(ndx, ndy) or 1
                    a.set_dir(ndx / nd * sp, ndy / nd * sp)
                    self._move(a, ndx / nd * sp, ndy / nd * sp)
                    a.energy -= MOVE_DRAIN * a.drain_f()
                    a.state = "run"
                    return
            a.set_dir(dx / d * sp, dy / d * sp)
            self._move(a, dx / d * sp, dy / d * sp)
            a.energy -= MOVE_DRAIN * a.drain_f()
            a.state = "run"
            return

        done = False
        if act == EAT:
            done = self._do_eat(a, gx, gy)
        elif act == DRINK:
            if w.near_water(a.tx, a.ty):
                before = a.needs[2]
                a.needs[2] = max(0.0, a.needs[2] - 0.6)
                a.temp = max(0.0, a.temp - 0.1)
                a.state = "drink"
                self.stats["drinks"] += 1
                self._reward(a, (before - a.needs[2]) * 0.8)
                done = True
            else:
                a.remember("water", gx, gy)
                a.goal = None
                return
        elif act in (REST, SLEEP):
            done = False   # persiste jusqu'a reveil (metabolisme)
        elif act == HARVEST:
            a.work_t += 1
            if a.work_t >= WORK_TICKS:
                a.work_t = 0
                done = not self._do_harvest(a, gx, gy)
                if not done:
                    a.goal["until"] = w.tick + 400
        elif act == DROP:
            self._do_drop(a)
            done = True
        elif act == BUILD:
            done = not self._do_build(a, gx, gy)
        elif act == GIVE:
            done = self._do_give(a, ref)
        elif act == TAKE:
            done = self._do_take(a, ref)
        elif act == ATTACK:
            self._do_attack(a, ref, gx, gy)
            done = a.goal is None
        elif act == FLEE:
            a.emotions[0] = max(0.0, a.emotions[0] - 0.004)
            if a.emotions[0] < 0.15 or a.goal_t > 120:
                done = True
        elif act == EXPLORE:
            self.stats["explored"] += 1
            first_visit = self.w.heat[gy, gx] < 0.15
            a.emotions[1] = min(1.0, a.emotions[1] + 0.04)
            if first_visit:
                self._reward(a, 0.12)
                a.anima_add_identity("explorer", 0.02)
                # Anima: episode new_area_discovered
                self._record_anima(
                    a, "new_area_discovered", (gx, gy),
                    action="explore", outcome="discovered",
                    surprise=0.3, achievement=0.15)
            else:
                self._reward(a, 0.01)
            done = True
        elif act == TALK:
            done = self._do_talk(a, ref)
        elif act == SOCIAL:
            done = self._do_social(a, ref)
        elif act == MARK:
            if a.energy > 0.12 and w.inb(a.tx, a.ty):
                w.marker[a.ty, a.tx] = min(1.0, w.marker[a.ty, a.tx] + 0.25)
                w.marker_col[a.ty, a.tx] = a.col_idx
                a.energy -= 0.004
                if a.home is None:
                    a.home = (a.tx, a.ty)
            done = a.goal_t > 24
        if done:
            a.goal = None
            a.commitment = max(0.0, a.commitment - 0.2)

    # ------------------------------------------------------------------ primitives
    def _reward(self, a, r):
        a.brain.learn(r, lr=self._lr(a))
        self.register_success_observation(a, (a.goal or {}).get("act", REST), r)

    def register_success_observation(self, actor, action, reward):
        if reward <= 0.05:
            return
        for observer in self._near(actor.x, actor.y,
                                   lambda e: isinstance(e, Being) and e.eid != actor.eid, r=2):
            if observer.child or observer.trust(actor.eid) > 0.2:
                observer.observed_actions.append({
                    "action": int(action),
                    "reward": float(reward),
                    "tick": self.w.tick,
                    "actor": actor.eid,
                })
                self.lab.event(self.w.tick, "imitation_recorded",
                               observer_eid=observer.eid, actor_eid=actor.eid,
                               action=int(action), reward=float(reward))

    def _lr(self, a):
        """Taux d'apprentissage cohérent avec le calendrier biologique."""
        base_lr = 0.0024
        if a.child:
            age_factor = 2.0
        else:
            death_age = max(1, getattr(a, "natural_death_age", AGE_MAX_NATURAL_DEATH_TICKS))
            life_progress = min(1.0, max(0.0, a.age / death_age))
            age_factor = max(0.15, 1.0 - 0.85 * life_progress)
        return base_lr * age_factor

    def _do_eat(self, a, gx, gy):
        w = self.w
        cx, cy = gx * TILE + 8, gy * TILE + 8
        cell_key = (int(cx // 128), int(cy // 128))
        for it in list(self.food_cells.get(cell_key, ())):
            if it.kind == "food" and (it.x - cx) ** 2 + (it.y - cy) ** 2 < 20 * 20:
                w.items.remove(it)
                self._eat(a, it.nutrition)
                return True
        aid = w.content_at(gx, gy)
        if aid >= 0:
            asd = self.am.assets[aid]
            if asd.edible > 0:
                self._eat(a, asd.edible)
                w.remove(gx, gy)
                return True
        a.forget("food", gx, gy)          # la source n'existe plus : faux souvenir
        return True

    def _eat(self, a, nutrition):
        before = a.needs[0]
        a.needs[0] = max(0.0, a.needs[0] - nutrition / 50.0)
        a.needs[2] = max(0.0, a.needs[2] - nutrition / 120.0)  # l'eau des aliments
        a.hunger = a.needs[0]
        a.needs[1] = a.energy = min(1.0, a.energy + nutrition / 60.0)
        a.emotions[1] = min(1.0, a.emotions[1] + 0.10)
        a.state = "eat"
        self._reward(a, (before - a.needs[0]) * 2.0)
        a.record_meaningful(self.w.tick, "eat")

    def try_craft_tool(self, a):
        from .config import TOOL_RECIPES
        if getattr(a, "child", False):
            return False
        for kind, recipe in TOOL_RECIPES.items():
            if a.inv.get("bois", 0) >= recipe["bois"] and a.inv.get("pierre", 0) >= recipe["pierre"]:
                pool = [aid for aid in self.am.by_role.get("tool", [])
                        if self.am.assets[aid].meta.get("tool_kind") == kind]
                if not pool:
                    continue
                aid = int(self.rng.choice(pool))
                a.inv["bois"] -= recipe["bois"]
                a.inv["pierre"] -= recipe["pierre"]
                a.tool = aid
                a.tool_durability = recipe["durability"]
                self.stats["tool_found"] += 1
                a.skills[1] = min(1.0, a.skills[1] + 0.03)
                self.log(f"{a.name} a fabriqué {kind}.", (248, 208, 98), "economy")
                self._reward(a, 0.25)
                self.lab.event(self.w.tick, "tool_crafted",
                               eid=a.eid, tool_kind=kind, durability=recipe["durability"])
                return True
        return False

    def _do_harvest(self, a, gx, gy):
        w, am = self.w, self.am
        aid = w.content_at(gx, gy)
        if aid < 0:
            a.forget("wood", gx, gy)
            a.forget("stone", gx, gy)
            return False
        asd = am.assets[aid]
        if asd.tool:
            a.tool = asd.id
            w.remove(gx, gy)
            self.stats["tool_found"] += 1
            self.log("Un habitant a trouvé et équipé un outil.", (248, 208, 98), "economy")
            self._reward(a, 0.3)
            return True
        if not asd.harvest:
            return False
        h = asd.harvest
        if w.hp[gy, gx] > 0 and a.inv[h["material"]] < INV_CAP:
            w.hp[gy, gx] -= 1
            tool_kind = ""
            if a.tool >= 0:
                tool_kind = self.am.assets[a.tool].meta.get("tool_kind", "")
            material = h["material"]
            tool_bonus = 1.0
            if material == "bois" and tool_kind == "hache":
                tool_bonus = 1.8
            elif material == "pierre" and tool_kind == "pioche":
                tool_bonus = 1.8
            elif material == "or" and tool_kind == "pioche":
                tool_bonus = 1.5
            elif a.tool >= 0:
                tool_bonus = 1.4
            base_amount = int(h.get("amount", 1))
            got = max(1, int(round(base_amount * tool_bonus * (1.0 + 0.6 * a.skills[0]))))
            a.inv[h["material"]] = min(INV_CAP, a.inv[h["material"]] + got)
            # ── graine en sous-produit (10% si récolte de bois = arbres) ──
            if h["material"] == "bois" and self.rng.random() < 0.10:
                a.inv["graine"] = min(INV_CAP, a.inv.get("graine", 0) + 1)
            a.skills[0] = min(1.0, a.skills[0] + 0.015)
            self.stats["harvests"] += 1
            a.record_meaningful(self.w.tick, "harvest")
            self._fx("dust", gx * TILE + 8, gy * TILE + 8)
            self.emit_sound(gx * TILE, gy * TILE, "chop", 0.7)
            a.state = "work"
            self._teach_near(a, 0)
            if w.hp[gy, gx] <= 0:
                self._deplete(gx, gy, asd)
            self._reward(a, 0.12)
            # Anima: episode food_found
            material = h.get("material", "")
            if material == "bois":
                self._record_anima(
                    a, "food_found", (gx, gy), action="harvest",
                    outcome="success", achievement=0.3)
            elif material in ("pierre", "or"):
                self._record_anima(
                    a, "danger_discovered", (gx, gy), action="harvest",
                    outcome="success", achievement=0.2)
            a.anima_add_identity("provider", 0.03)
            if a.tool >= 0:
                a.tool_durability -= 1
                if a.tool_durability <= 0:
                    self.log(f"L'outil de {a.name} s'est cassé à l'usage.", (218, 138, 58), "economy")
                    self.lab.event(self.w.tick, "tool_broken",
                                   eid=a.eid, tool_id=a.tool)
                    a.tool = -1
                    a.tool_durability = 0
            return True
        return False

    def _do_drop(self, a):
        mat = max(a.inv, key=a.inv.get)
        if a.inv[mat] > 0:
            a.inv[mat] -= 1
            self._drop_item(mat, a.x, a.y)
            a.state = "work"

    def suggest_place(self, a, category, tx, ty, strength=0.4):
        """Suggestion non contraignante — renforce la memoire d'un etre."""
        if hasattr(a, "remember"):
            a.remember(category, tx, ty)
        key = (tx // 8, ty // 8)
        if hasattr(a, "belief_places"):
            a.belief_places[key] = min(1.0, a.belief_places.get(key, 0) + strength * 0.3)

    def _do_give(self, a, ref):
        storage = self.nearest_storage(a.tx, a.ty, max_dist=2)
        if storage is not None:
            return self.deposit_to_storage(a, storage)
        e = ref if isinstance(ref, Being) and ref.alive else None
        if e is None:
            return True
        mat = max(a.inv, key=a.inv.get)
        if a.inv[mat] > 1:
            a.inv[mat] -= 2
            e.inv[mat] = min(INV_CAP, e.inv[mat] + 2)
            self.stats["gives"] += 1
            a.state = "give"
            # Halo de don (Lot J) : effet visuel seul, purge par TTL.
            self.effects.append({"kind": "gift", "x": a.x, "y": a.y,
                                 "target_x": e.x, "target_y": e.y,
                                 "t0": self.w.tick, "ttl": 22,
                                 "color": (98, 211, 148)})
            r1 = a.rel.setdefault(e.eid, [0, 0])
            r1[0] = min(1.0, r1[0] + 0.2)
            r2 = e.rel.setdefault(a.eid, [0, 0])
            r2[0] = min(1.0, r2[0] + 0.25)
            r1[1] = min(1.0, r1[1] + 0.15)
            r2[1] = min(1.0, r2[1] + 0.15)
            e.emotions[1] = min(1.0, e.emotions[1] + 0.15)
            a.emotions[1] = min(1.0, a.emotions[1] + 0.08)
            a.emotions[7] = min(1.0, a.emotions[7] + 0.05)
            a.needs[6] = max(0.0, a.needs[6] - 0.2)
            e.needs[5] = max(0.0, e.needs[5] - 0.2)
            a.rep += 1
            a.belief_beings[e.eid] = min(1.0, a.belief_beings.get(e.eid, 0) + 0.15)
            self._trade[(min(a.eid, e.eid), max(a.eid, e.eid))] = \
                self._trade.get((min(a.eid, e.eid), max(a.eid, e.eid)), 0) + 1
            self.emit_sound(a.x, a.y, "voice", 0.4)
            self._reward(a, 0.2)
            self.social_memory.record(e.eid, a.eid, "help", 0.20, self.w.tick)
            # Anima: episodes food_given / food_received
            self._record_anima(
                a, "food_given", (a.tx, a.ty),
                actors=[a.eid, e.eid], action="give",
                outcome="success", social_impact=0.4, achievement=0.2)
            self._record_anima(
                e, "food_received", (e.tx, e.ty),
                actors=[e.eid, a.eid], action="receive",
                outcome="success", social_impact=0.5)
            e.anima["attachments"][a.eid] = min(
                1.0, e.anima["attachments"].get(a.eid, 0.0) + 0.10)
        return True

    def _do_take(self, a, ref):
        storage = self.nearest_storage(a.tx, a.ty, max_dist=2)
        if storage is not None:
            needed = "food" if a.needs[0] > 0.65 else "bois"
            return self.withdraw_from_storage(a, storage, needed)
        e = ref if isinstance(ref, Being) and ref.alive else None
        if e is None:
            return True
        mat = max(e.inv, key=e.inv.get)
        if e.inv[mat] <= 0:
            return True
        got = min(2, e.inv[mat])
        if a.trust(e.eid) > 0.4 and self.rng.random() < 0.6:
            # une relation de confiance refuse la violence : le vol echoue
            a.emotions[6] = min(1.0, a.emotions[6] + 0.2)
            return True
        e.inv[mat] -= got
        a.inv[mat] = min(INV_CAP, a.inv[mat] + got)
        self.stats["takes"] += 1
        a.rep -= 2
        a.rel.setdefault(e.eid, [0, 0])[0] -= 0.5
        e.rel.setdefault(a.eid, [0, 0])[0] -= 0.6
        e.rel.setdefault(a.eid, [0, 0])[1] -= 0.4
        a.rel.setdefault(e.eid, [0, 0])[1] -= 0.3
        e.emotions[2] = min(1.0, e.emotions[2] + 0.5)
        a.belief_beings[e.eid] = max(-1.0, a.belief_beings.get(e.eid, 0) - 0.3)
        self._reward(a, 0.15)
        self.social_memory.record(e.eid, a.eid, "theft", 0.45, self.w.tick)
        if e.personality[1] > 0.4 or e.health > a.health:
            e.hated = a.eid
        return True

    def _blocked_los(self, x1, y1, x2, y2):
        """Vérifie si un batiment solide bloque la ligne de vue entre deux points."""
        w = self.w
        dx, dy = x2 - x1, y2 - y1
        d = max(abs(dx), abs(dy))
        if d < 1:
            return False
        steps = int(d / TILE) + 1
        for s in range(1, steps):
            t = s / steps
            cx, cy = int((x1 + dx * t) // TILE), int((y1 + dy * t) // TILE)
            if 0 <= cx < w.g and 0 <= cy < w.g and w.blocked[cy, cx]:
                return True
        return False

    def _do_attack(self, a, ref, gx, gy):
        w = self.w
        target = ref if isinstance(ref, (Being, Sheep, Monster)) and getattr(ref, "alive", False) else None
        if target is None:
            near = [e for e in self._near(a.x, a.y,
                     lambda e: isinstance(e, (Being, Sheep, Monster)) and e is not a, r=1)]
            target = max(near, key=lambda t: t.health) if near else None
        if target is None:
            a.goal = None
            return
        if a.atk_t > 0:
            return
        # ── blocage par mur / batiment solide ──
        if self._blocked_los(a.x, a.y, target.x, target.y):
            a.emotions[3] = min(1.0, a.emotions[3] + 0.05)
            return
        dmg = (ATTACK_DMG_TOOL if a.tool >= 0 else ATTACK_DMG) * a.dmg_f()
        target.health -= dmg
        a.energy -= 0.03
        a.atk_t = 45
        if a.tool >= 0:
            a.tool_durability -= 2
            if a.tool_durability <= 0:
                self.lab.event(self.w.tick, "tool_broken", eid=a.eid, tool_id=a.tool)
                a.tool = -1
                a.tool_durability = 0
        a.skills[2] = min(1.0, a.skills[2] + 0.02)
        a.emotions[2] = min(1.0, a.emotions[2] + 0.15)
        self.stats["attacks"] += 1
        self._recent_attacks.append(w.tick)
        self._fx("dust", target.x, target.y)
        self.emit_sound(target.x, target.y, "fight", 1.0)
        a.state = "attack"
        if isinstance(target, Sheep):
            if target.health <= 0:
                self._kill_sheep(target, killer=a)
                a.goal = None
            return
        if isinstance(target, Monster):
            if target.health <= 0:
                target.alive = False
                self.monsters = [x for x in self.monsters if x.alive]
                self._entity_cells.pop(target.eid, None)
                for _ in range(2):
                    self._drop_food(
                        self.am.pool("meat_res"),
                        target.x + self.rng.uniform(-6, 6),
                        target.y + self.rng.uniform(-6, 6),
                        nutrition=45,
                    )
                self.lab.event(self.w.tick, "monster_killed",
                               eid=a.eid, monster_eid=target.eid,
                               tx=int(target.x), ty=int(target.y))
                self._reward(a, 0.30)
                self._record_anima(
                    a, "monster_survival",
                    (a.tx, a.ty),
                    actors=[a.eid, target.eid], action="kill",
                    outcome="survived",
                    health_loss=0.0, fear=0.0, surprise=0.3,
                    achievement=0.5,
                )
                a.anima_add_identity("fighter", 0.08)
                a.goal = None
            return
        # consequences sociales - violence sévère
        a.rel.setdefault(target.eid, [0, 0])[0] -= 0.5
        target.rel.setdefault(a.eid, [0, 0])[0] -= 0.6
        target.rel.setdefault(a.eid, [0, 0])[1] -= 0.5
        a.rel.setdefault(target.eid, [0, 0])[1] -= 0.4
        target.emotions[0] = min(1.0, target.emotions[0] + 0.5)
        target.emotions[2] = min(1.0, target.emotions[2] + 0.6)
        target.pain = min(1.0, target.pain + 0.4)
        target.belief_places[(a.tx // 8, a.ty // 8)] = min(
            1.0, target.belief_places.get((a.tx // 8, a.ty // 8), 0) + 0.3)
        target.dangers.append((a.x, a.y, w.tick))
        self._dominance[a.eid] = self._dominance.get(a.eid, 0) + 1
        self._dominance[target.eid] = self._dominance.get(target.eid, 0) - 1
        a.rep -= 1
        self.social_memory.record(target.eid, a.eid, "violence", 0.55, self.w.tick)
        if target.child:
            # tabou emergent : frapper un enfant revolte les temoins
            a.rep -= 3
            for wit in self._near(target.x, target.y,
                                  lambda e: isinstance(e, Being) and e.eid != a.eid, r=3):
                wit.emotions[2] = min(1.0, wit.emotions[2] + 0.5)
                if wit.personality[5] > 0.4:
                    wit.hated = a.eid
            self.log(f"{a.name} a frappé un enfant !", (228, 98, 98), "combat")
        for wit in self._near(target.x, target.y,
                              lambda e: isinstance(e, Being)
                              and e.eid not in (a.eid, target.eid), r=2):
            if wit.personality[5] > 0.55 and wit.emotions[2] < 0.7:
                wit.emotions[2] = min(1.0, wit.emotions[2] + 0.3 * wit.personality[5])
                if wit.personality[1] > 0.45 and wit.hated is None:
                    wit.hated = a.eid
        self.emit_sound(target.x, target.y, "scream", 1.0)
        if target.health <= 0:
            mat = max(target.inv, key=target.inv.get)
            if target.inv[mat] > 0:
                target.inv[mat] -= 1
                a.inv[mat] = min(INV_CAP, a.inv[mat] + 1)
            self._die(target)
            a.hated = None
            a.goal = None
            self._reward(a, 0.3)
        elif target.hated is None and target.emotions[2] > 0.6 \
                and target.personality[1] > 0.5:
            target.hated = a.eid
        self._reward(a, -0.1)

    def _do_talk(self, a, ref):
        w = self.w
        e = ref if isinstance(ref, Being) and ref.alive else None
        if e is None and a._near_agents:
            e = max(a._near_agents,
                    key=lambda o: a.anima_social_score(o.eid))
        if e is None:
            return True
        return self.do_talk(a, e)

    def _do_social(self, a, ref):
        e = ref if isinstance(ref, Being) and ref.alive else None
        if e is None:
            return True
        if a.goal_t > 100:
            a.health = min(1.0, a.health + 0.01)
            a.emotions[1] = min(1.0, a.emotions[1] + 0.1)
            a.needs[5] = max(0.0, a.needs[5] - 0.3)
            r = a.rel.setdefault(e.eid, [0, 0])
            r[1] = min(1.0, r[1] + 0.05)
            a.emotions[7] = min(1.0, a.emotions[7] + 0.08)
            e.emotions[7] = min(1.0, e.emotions[7] + 0.05)
            self._reward(a, 0.15)
            self.social_memory.record(e.eid, a.eid, "help", 0.10, self.w.tick)
            return True
        return False

    def _teach_near(self, a, skill_idx):
        """Transmission culturelle : un enfant qui regarde apprend."""
        if not self.runtime.get("culture_enabled", True):
            return
        for e in self._near(a.x, a.y, lambda e: isinstance(e, Being) and e.child, r=2):
            if e.trust(a.eid) > -0.2:
                e.skills[skill_idx] = min(1.0, e.skills[skill_idx]
                                          + 0.02 * (1 + a.skills[skill_idx]))

    # ------------------------------------------------------------------ construction
    def _do_build(self, a, tx, ty):
        w, am = self.w, self.am

        # ── garde coordonnées : but hors monde = indexation négative numpy ──
        if not w.inb(tx, ty):
            tx, ty = self._free_near(tx, ty)
            if not w.inb(tx, ty):
                return False

        # ── repli brique-par-brique si ressources insuffisantes ──
        if (a.inv.get("bois", 0) < 3 or a.inv.get("pierre", 0) < 1) \
                and a.inv.get("graine", 0) == 0:
            if a.inv.get("bois", 0) > 0 or a.inv.get("pierre", 0) > 0:
                res = self.do_build_block(a, tx, ty)
                if res:
                    a.record_meaningful(self.w.tick, "build")
                return res

        # ── agriculture : si l'être porte des graines et que la case est vide ──
        if a.inv.get("graine", 0) > 0 and w.land[ty, tx] and w.content_at(tx, ty) < 0 \
                and not w.water[ty, tx] and (tx, ty) not in w.crop_plots:
            from .world import CropPlot
            plot = CropPlot(tx=tx, ty=ty, owner_eid=a.eid, planted_tick=w.tick)
            w.crop_plots[(tx, ty)] = plot
            a.inv["graine"] = max(0, a.inv["graine"] - 1)
            self._reward(a, 0.12)
            self.log(f"{a.name} a plante une graine.", (108, 188, 98), "economy")
            self.lab.event(self.w.tick, "crop_planted",
                           eid=a.eid, tx=tx, ty=ty)
            a.record_meaningful(self.w.tick, "build")
            return True

        # ── construction brique par brique ──
        result = self.do_build_block(a, tx, ty)
        if result and a.home is None:
            a.home = (tx, ty)
            a.life.append("première maison")
            self._fx("dust", tx * TILE + 8, ty * TILE + 8)
            self._check_village(tx, ty)
            self._teach_near(a, 1)
            self._reward(a, 0.35)
        if result:
            a.record_meaningful(self.w.tick, "build")
        return result

    def can_place_blueprint(self, tasks):
        w = self.w
        for task in tasks:
            if not (0 <= task.tx < w.g and 0 <= task.ty < w.g):
                return False
            if not w.land[task.ty, task.tx]:
                return False
            if w.water[task.ty, task.tx]:
                return False
            if w.content_at(task.tx, task.ty) >= 0:
                return False
        return True

    def find_build_location(self, a, radius=8):
        for r in range(2, radius + 1):
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    if abs(dx) != r and abs(dy) != r:
                        continue
                    tx, ty = a.tx + dx, a.ty + dy
                    tasks = blueprint_from_name("small_house", tx, ty)
                    if self.can_place_blueprint(tasks):
                        return tx, ty
        return None

    def create_house_site(self, a, tx=None, ty=None):
        if tx is None or ty is None:
            pos = self.find_build_location(a)
            if pos is None:
                return None
            tx, ty = pos
        tasks = blueprint_from_name("small_house", tx, ty)
        if not self.can_place_blueprint(tasks):
            return None
        site = ConstructionSite(
            origin_tx=tx, origin_ty=ty,
            blueprint_name="small_house", tasks=tasks,
            created_tick=self.w.tick,
            owner_eid=a.eid, owner_clan=a.color,
        )
        self.w.add_site(site)
        a.home = (tx + 2, ty + 2)
        self.log(f"{a.name} a commence le plan d'une maison.", (178, 228, 168), "building")
        self._record_anima(
            a, "construction_started", (tx, ty),
            actors=[a.eid], action="build", outcome="started",
            achievement=0.1)
        return site

    def _choose_blueprint(self, a):
        w = self.w
        bois = a.inv.get("bois", 0)
        pierre = a.inv.get("pierre", 0)
        has_house = a.home is not None
        nearby_storages = sum(1 for s in w.storages.values()
                              if abs(s.tx - a.tx) + abs(s.ty - a.ty) < 20)
        has_well = any(s.role == "puits" for s in w.storages.values()
                       if abs(s.tx - a.tx) + abs(s.ty - a.ty) < 20)
        if not has_house:
            return "small_house"
        if nearby_storages == 0 and bois >= 4:
            return "coffre"
        if nearby_storages >= 1 and bois >= 6 and pierre >= 2:
            return "grenier"
        if not has_well and pierre >= 3:
            return "puits"
        if a.skills[1] > 0.4 and pierre >= 6 and bois >= 4:
            return "atelier"
        return "small_house"

    def create_blueprint_site(self, a, blueprint="small_house", tx=None, ty=None):
        if tx is None or ty is None:
            pos = self.find_build_location(a)
            if pos is None:
                return None
            tx, ty = pos
        tasks = blueprint_from_name(blueprint, tx, ty)
        if not self.can_place_blueprint(tasks):
            return None
        site = ConstructionSite(
            origin_tx=tx, origin_ty=ty,
            blueprint_name=blueprint, tasks=tasks,
            created_tick=self.w.tick,
            owner_eid=a.eid, owner_clan=a.color,
        )
        self.w.add_site(site)
        self.lab.event(self.w.tick, "site_created",
                       eid=a.eid, blueprint=blueprint,
                       tx=tx, ty=ty, tasks_total=len(tasks))
        if blueprint == "small_house":
            a.home = (tx + 2, ty + 2)
        self.log(f"{a.name} a commence un chantier ({blueprint}).", (178, 228, 168), "building")
        self._record_anima(
            a, "construction_started", (tx, ty),
            actors=[a.eid], action="build", outcome="started",
            achievement=0.1)
        return site

    def nearest_site(self, tx, ty, max_dist=15):
        best, best_dist = None, 10**9
        for site in self.w.sites.values():
            d = max(abs(site.origin_tx - tx), abs(site.origin_ty - ty))
            if d <= max_dist and d < best_dist:
                best, best_dist = site, d
        return best

    def role_for_block_task(self, task):
        if task.phase == "door":
            return "block_door"
        if task.phase == "roof":
            return "block_roof"
        if task.material == "pierre":
            return "block_stone"
        return "block_wood"

    def ensure_material_for_task(self, a, task):
        if a.inv.get(task.material, 0) > 0:
            return True
        storage = self.nearest_storage(a.tx, a.ty, max_dist=14)
        if storage is None:
            return False
        return self.withdraw_from_storage(a, storage, task.material)

    def place_site_block(self, a, site, task):
        w = self.w
        if task.key in site.placed:
            return False
        if task.material not in ("bois", "pierre"):
            return False
        if not self.ensure_material_for_task(a, task):
            return False
        if task.phase == "foundation":
            if w.foundation[task.ty, task.tx] >= 0:
                return False
        elif task.phase == "roof":
            if w.roof[task.ty, task.tx] >= 0:
                return False
        elif w.content_at(task.tx, task.ty) >= 0:
            return False
        role = self.role_for_block_task(task)
        pool = self.am.pool(role)
        if not pool:
            return False
        aid = int(self.am.pick(pool, self.rng))
        if task.phase == "foundation":
            w.foundation[task.ty, task.tx] = aid
        elif task.phase == "roof":
            w.roof[task.ty, task.tx] = aid
        else:
            w.place(task.tx, task.ty, aid, self.am, hp=6,
                    solid=task.solid, shelter=False, size=1)
        a.inv[task.material] -= 1
        site.mark_placed(a.eid, task)
        a.skills[1] = min(1.0, a.skills[1] + 0.012)
        self.stats["builds"] += 1
        self.lab.event(self.w.tick, "site_block_placed",
                       eid=a.eid, blueprint=site.blueprint_name,
                       tx=task.tx, ty=task.ty, phase=task.phase,
                       material=task.material,
                       progress=site.progress())
        self._note_institution("construction", site.origin_tx, site.origin_ty,
                               a.eid, action="build")
        self._fx("dust", task.tx * TILE + TILE / 2, task.ty * TILE + TILE / 2)
        self._reward(a, 0.10)
        if site.complete():
            self.complete_site(site, a)
        return True

    def site_has_required_phases(self, site):
        phases = {
            task.phase
            for task in site.tasks
            if task.key in site.placed
        }
        return {"foundation", "wall", "door", "roof"}.issubset(phases)

    def complete_site(self, site, finisher):
        w = self.w
        bp = site.blueprint_name
        if not self.site_has_required_phases(site):
            return
        if bp in ("small_house", "storage_hut", "atelier", "grenier"):
            for ty in range(site.origin_ty + 1, site.origin_ty + 4):
                for tx in range(site.origin_tx + 1, site.origin_tx + 4):
                    if 0 <= tx < w.g and 0 <= ty < w.g:
                        w.shelter[ty, tx] = 1
        # depot pour les maisons et greniers
        if bp in ("small_house", "storage_hut", "grenier"):
            storage_tx = site.origin_tx + 2
            storage_ty = site.origin_ty + 2
            if bp == "grenier":
                storage_tx = site.origin_tx + 1
                storage_ty = site.origin_ty + 1
            if (storage_tx, storage_ty) not in w.storages:
                cap = 120 if bp == "grenier" else 80
                self.create_storage(finisher, storage_tx, storage_ty, capacity=cap)
                self.log(f"{bp} termine : depot cree.", (178, 228, 168), "building")
        elif bp == "coffre":
            storage_tx, storage_ty = site.origin_tx, site.origin_ty
            if (storage_tx, storage_ty) not in w.storages:
                self.create_storage(finisher, storage_tx, storage_ty, capacity=40)
                self.log("Coffre termine.", (178, 228, 168), "building")
        elif bp == "puits":
            w.shelter[site.origin_ty, site.origin_tx] = 1
            self.log("Puits termine.", (90, 180, 230), "building")
        elif bp == "atelier":
            self.log("Atelier termine.", (200, 160, 90), "building")
        w.remove_site(site)
        self._check_village(site.origin_tx + 2, site.origin_ty + 2)
        for eid in site.contributors:
            c = next((x for x in self.agents if x.eid == eid), None)
            if c and c.alive:
                c.skills[1] = min(1.0, c.skills[1] + 0.04)
                c.needs[6] = max(0.0, c.needs[6] - 0.12)
                self._reward(c, 0.25)
                self._note_institution("construction", site.origin_tx,
                                       site.origin_ty, eid, action="complete")
        # Anima: episode construction
        if finisher and finisher.alive:
            self._record_anima(
                finisher, "construction_complete",
                (site.origin_tx, site.origin_ty),
                actors=list(site.contributors),
                action="build", outcome="completed",
                achievement=0.6, social_impact=0.3,
            )
            finisher.anima_add_identity("builder", 0.10)
        self.log(f"{bp} termine : {len(site.contributors)} contributeur(s).",
                 (108, 208, 128), "building")
        self.lab.event(self.w.tick, "site_completed",
                       blueprint=bp, tx=site.origin_tx, ty=site.origin_ty,
                       contributors=len(site.contributors),
                       finisher_eid=finisher.eid if finisher else None)

    def do_build_block(self, a, tx, ty):
        """BUILD : contribuer a un chantier existant ou placer un bloc."""
        site = self.nearest_site(a.tx, a.ty, max_dist=14)
        if site is not None:
            task = site.next_task_for(a.inv)
            if task is not None:
                return self.place_site_block(a, site, task)
        # choisir le plan selon le contexte
        bp = self._choose_blueprint(a)
        site = self.create_blueprint_site(a, bp)
        if site is not None:
            task = site.next_task_for(a.inv)
            if task is not None:
                return self.place_site_block(a, site, task)
            return True
        w, am = self.w, self.am
        if not w.inb(tx, ty):
            tx, ty = self._free_near(tx, ty)
            if not w.inb(tx, ty):
                return False
        if w.blocked[ty, tx] or w.content_at(tx, ty) >= 0 or not w.land[ty, tx]:
            tx, ty = self._free_near(tx, ty)
            if w.blocked[ty, tx] or w.content_at(tx, ty) >= 0:
                return False
        if a.inv.get("bois", 0) > 0:
            material, role = "bois", "block_wood"
        elif a.inv.get("pierre", 0) > 0:
            material, role = "pierre", "block_stone"
        else:
            return False
        pool = am.pool(role)
        if not pool:
            return False
        aid = int(am.pick(pool, self.rng))
        w.place(tx, ty, aid, am, hp=6, solid=True, shelter=False, size=1)
        a.inv[material] = max(0, a.inv[material] - 1)
        a.skills[1] = min(1.0, a.skills[1] + 0.008)
        self.stats["builds"] += 1
        self._check_village(tx, ty)
        self._reward(a, 0.10)
        return True

    def do_build_block_player(self, tx, ty, material="bois"):
        w, am = self.w, self.am
        if not (0 <= tx < GRID and 0 <= ty < GRID):
            return False
        if w.blocked[ty, tx] or w.content_at(tx, ty) >= 0 or not w.land[ty, tx]:
            return False
        role = "block_wood" if material == "bois" else "block_stone"
        pool = am.pool(role)
        if not pool:
            return False
        aid = int(am.pick(pool, self.rng))
        w.place(tx, ty, aid, am, hp=6, solid=True, shelter=False, size=1)
        self._check_village(tx, ty)
        return True

    def _free_near(self, tx, ty):
        for r in range(4):
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    x, y = tx + dx, ty + dy
                    if 0 <= x < self.w.g and 0 <= y < self.w.g \
                       and not self.w.blocked[y, x] and self.w.content_at(x, y) < 0:
                        return x, y
        return tx, ty

    def _check_village(self, tx, ty):
        w = self.w
        y0, y1 = max(0, ty - 10), min(w.g, ty + 11)
        x0, x1 = max(0, tx - 10), min(w.g, tx + 11)
        shelters = int(w.shelter[y0:y1, x0:x1].sum())
        if shelters >= 10:
            for vx, vy in self._village_pts:
                if (vx - tx) ** 2 + (vy - ty) ** 2 < 900:
                    return
            self._village_pts.append((tx, ty))
            self.stats["villages"] += 1
            self.log(f"Un village est né en ({tx},{ty}) — {shelters} abris !", (108, 208, 128), "building")

    # ------------------------------------------------------------------ deplete / feu
    def _deplete(self, tx, ty, asd):
        w, am = self.w, self.am
        mat = asd.harvest["material"]
        role = asd.role
        if role == "tree":
            stumps = am.pool("stump")
            if stumps:
                sid = int(am.pick(stumps, self.rng))
                w.place(tx, ty, sid, am, hp=0, solid=False, size=1)
            else:
                w.remove(tx, ty)
            w.regrow[ty, tx] = 2400
            for _ in range(2):
                self._drop_item("bois", tx * TILE + 8 + self.rng.uniform(-8, 8),
                                ty * TILE + 8 + self.rng.uniform(-8, 8))
        elif role in ("stone_res", "gold_stone"):
            w.remove(tx, ty)
            for _ in range(2):
                self._drop_item(mat, tx * TILE + 8 + self.rng.uniform(-8, 8),
                                ty * TILE + 8 + self.rng.uniform(-8, 8))
        elif role == "meat_res":
            w.remove(tx, ty)
            for _ in range(3):
                self._drop_food(am.pool("meat_res"), tx * TILE + 8, ty * TILE + 8, 45)
        else:
            w.remove(tx, ty)

    # ------------------------------------------------------------------ mort / famille
    def _check_vital_death(self, a) -> bool:
        """Mort garantie quand la santé tombe à 0 (ou moins).

        Point UNIQUE d'appel après chaque ``_metabolize`` et en fin de
        tick : les retours anticipés d'``_agent`` (activité en cours,
        départ d'une activité) sautaient le test de fin de fonction, et
        un habitant pouvait donc vivre des dizaines de milliers de ticks
        avec ``health < 0``.

        ``_die`` est appelé exactement une fois (garde ``if not a.alive``).
        Retourne ``True`` si l'habitant vient de mourir.
        """
        if a is None or not getattr(a, "alive", False):
            return False
        if float(a.health) > 0.0:
            return False
        a.health = 0.0
        self._die(a)
        return True

    def _die(self, a: Being, cause: str | None = None):
        if not a.alive:
            return
        a.alive = False
        a.health = 0.0
        w, am = self.w, self.am
        self.stats["deaths"] += 1
        tx, ty = a.tx, a.ty
        graves = am.pool("grave")
        if graves and w.content_at(tx, ty) < 0 and not w.blocked[ty, tx]:
            gid = int(am.pick(graves, self.rng))
            w.place(tx, ty, gid, am, hp=0, solid=False, size=1)
        self._drop_food(am.pool("meat_res"), a.x, a.y, 40)
        self._drop_food(am.pool("meat_res"), a.x + 6, a.y - 5, 40)
        # heritage : les liens survivent a l'individu
        heirs = [self._by_eid(x) for x in (list(a.rel.keys()) + list(a.children))]
        for m, c in a.inv.items():
            for h in heirs:
                if h and h.alive and c > 0 and h.trust(a.eid) > 0.2:
                    take = min(c, 3)
                    h.inv[m] = min(INV_CAP, h.inv[m] + take)
                    c -= take
            for _ in range(c):
                self._drop_item(m, a.x + self.rng.uniform(-10, 10),
                                a.y + self.rng.uniform(-10, 10))
        self._fx("explosion", a.x, a.y)
        for other in self.agents:
            r = other.rel.get(a.eid)
            if r and r[1] > 0.2:
                other.emotions[3] = min(1.0, other.emotions[3] + 0.35 * r[1])
                if other.bonded == a.eid:
                    other.bonded = None
                    other.married = False
                    other.partner_id = None
                # Anima: episode loss for mourners
                self._record_anima(
                    other, "loss", (a.tx, a.ty),
                    actors=[other.eid, a.eid], action="witness_death",
                    outcome="lost",
                    fear=0.3, social_impact=0.5)
                other.anima["trauma"]["loss"] = min(
                    1.0, other.anima["trauma"]["loss"] + 0.08)
        if a.bonded:
            b = self._by_eid(a.bonded)
            if b and b.alive:
                self.log(f"{b.name} pleure {a.name}.", (148, 148, 198), "social")
        if cause is None:
            cause = (
                "soif" if a.needs[2] >= 0.999 else
                "faim" if a.hunger >= 0.999 else
                "blessures"
            )
        self.log(f"{a.name} ({a.stage}, {a.age_years:.1f} ans) est mort de {cause}, "
                 f"gén {a.gen}, {a.brain.n} neurones.", (228, 98, 98), "death")
        # enterre dans le cimetière commun
        grave_tx, grave_ty = self.w.find_cemetery_spot(self.rng)
        self.w.bury(grave_tx, grave_ty, a.name, self.w.tick,
                    CLAN_COLORS.get(a.color, (150, 150, 150)))
        self.lab.event(self.w.tick, "death", eid=a.eid, cause=cause, age_years=a.age_years,
                       name=a.name, gen=a.gen)

    def _kill_sheep(self, s, killer=None):
        s.alive = False
        for _ in range(int(self.rng.integers(2, 4))):
            self._drop_food(self.am.pool("meat_res"), s.x, s.y, 40)
        self._fx("dust", s.x, s.y)

    def _drop_item(self, material, x, y):
        pool = self.am.pool(MAT_AIDS.get(material, "item_wood")) or self.am.pool("item_wood")
        aid = int(self.am.pick(pool, self.rng, default=0))
        self.w.drop_item(Item("mat", aid, x, y, material=material))

    def _drop_food(self, pool, x, y, nutrition):
        aid = int(self.am.pick(pool or self.am.pool("food"), self.rng, default=0))
        it = Item("food", aid, x + self.rng.uniform(-6, 6),
                  y + self.rng.uniform(-6, 6), nutrition=nutrition,
                  life=60 * 60 * 4)
        it.created_tick = self.w.tick
        it.spoil_tick = self.w.tick + 7200
        self.w.drop_item(it)

    def _fx(self, name, x, y):
        ids = self.am.fx.get(name) or []
        if not ids:
            return
        self.effects.append(dict(aid=int(ids[0]), x=x, y=y, t0=self.w.tick, ttl=32,
                                 frames=self.am.assets[int(ids[0])].frames))

    # ------------------------------------------------------------------ relationships & marriage

    def try_bond(self, a: Being, b: Being) -> bool:
        """Tente de créer un lien d'attachement (bonded) entre deux habitants.
        
        Conditions:
        - Les deux sont vivants et adultes
        - Ni l'un ni l'autre n'est déjà bonded
        - Confiance >= 0.6, Affection >= 0.5
        - Pas de lien de parenté direct
        - SEULEMENT entre un homme et une femme (mariage hétérosexuel uniquement)
        """
        if not (a.alive and b.alive):
            return False
        if a.bonded or b.bonded:
            return False
        if a.stage != "adulte" or b.stage != "adulte":
            return False
        # Règle stricte : mariage uniquement entre un homme et une femme
        if a.sex == b.sex:
            return False
        if a.trust(b.eid) < 0.6 or b.trust(a.eid) < 0.6:
            return False
        if a.rel.get(b.eid, [0, 0])[1] < 0.5 or b.rel.get(a.eid, [0, 0])[1] < 0.5:
            return False
        if a.eid in b.children or b.eid in a.children:
            return False
        
        a.bonded = b.eid
        b.bonded = a.eid
        
        # Effet visuel
        self.effects.append({"kind": "bond", "x": a.x, "y": a.y,
                             "target_x": b.x, "target_y": b.y,
                             "t0": self.w.tick, "ttl": 30,
                             "color": (255, 100, 150)})
        
        # Anima: lien formé
        a.anima["attachments"][b.eid] = min(1.0, a.anima["attachments"].get(b.eid, 0) + 0.3)
        b.anima["attachments"][a.eid] = min(1.0, b.anima["attachments"].get(a.eid, 0) + 0.3)
        
        self._record_anima(a, "bond_formed", (a.tx, a.ty), actors=[a.eid, b.eid],
                           action="bond", outcome="success", social_impact=0.8)
        self._record_anima(b, "bond_formed", (b.tx, b.ty), actors=[b.eid, a.eid],
                           action="bond", outcome="success", social_impact=0.8)
        
        self.log(f"{a.name} et {b.name} sont liés.", (255, 100, 150), "social")
        return True

    def try_propose(self, a: Being, b: Being) -> bool:
        """Tente une proposition de mariage.
        
        Conditions:
        - Déjà bonded
        - Confiance >= 0.75, Affection >= 0.7
        - Les deux adultes
        - Ni l'un ni l'autre n'est déjà marié
        - SEULEMENT entre un homme et une femme (mariage hétérosexuel uniquement)
        """
        if not (a.alive and b.alive):
            return False
        if a.bonded != b.eid or b.bonded != a.eid:
            return False
        if a.married or b.married:
            return False
        # Règle stricte : mariage uniquement entre un homme et une femme
        if a.sex == b.sex:
            return False
        if a.trust(b.eid) < 0.75 or b.trust(a.eid) < 0.75:
            return False
        if a.rel.get(b.eid, [0, 0])[1] < 0.7 or b.rel.get(a.eid, [0, 0])[1] < 0.7:
            return False
        if a.stage != "adulte" or b.stage != "adulte":
            return False
        
        # Proposition acceptée si affinité suffisante
        accept_chance = 0.5 + 0.3 * a.trust(b.eid) + 0.2 * a.rel.get(b.eid, [0, 0])[1]
        if self.rng.random() > accept_chance:
            a.rel.setdefault(b.eid, [0, 0])[0] = max(0.0, a.trust(b.eid) - 0.3)
            a.emotions[3] = min(1.0, a.emotions[3] + 0.3)
            a.emotions[7] = min(1.0, a.emotions[7] + 0.2)
            self.log(f"{b.name} refuse la proposition de {a.name}.", (200, 100, 100), "social")
            return False
        
        # Mariage accepté
        a.married = True
        b.married = True
        a.partner_id = b.eid
        b.partner_id = a.eid
        
        # Foyer commun
        if not a.home:
            a.home = (a.tx, a.ty)
        b.home = a.home
        
        # Anima
        a.anima_add_identity("caretaker", 0.1)
        b.anima_add_identity("caretaker", 0.1)
        a.anima_add_value("family", 0.15)
        b.anima_add_value("family", 0.15)
        a.anima_add_attachment(b.eid, 0.4)
        b.anima_add_attachment(a.eid, 0.4)
        
        self._record_anima(a, "marriage", (a.tx, a.ty), actors=[a.eid, b.eid],
                           action="marry", outcome="success", social_impact=1.0)
        self._record_anima(b, "marriage", (b.tx, b.ty), actors=[b.eid, a.eid],
                           action="marry", outcome="success", social_impact=1.0)
        
        self.stats["marriages"] = self.stats.get("marriages", 0) + 1
        self.log(f"{a.name} et {b.name} se sont mariés !", (255, 100, 200), "social")
        self.emit_sound(a.x, a.y, "celebration", 0.8)
        return True

    def try_have_child(self, a: Being, b: Being) -> bool:
        """Tente d'avoir un enfant (si marié, foyer, ressources)."""
        if not (a.married and b.married and a.partner_id == b.eid and b.partner_id == a.eid):
            return False
        if not (a.home and b.home and a.home == b.home):
            return False
        if a.energy < 0.5 or b.energy < 0.5:
            return False
        if a.hunger > 0.6 or b.hunger > 0.6:
            return False
        if len(self.agents) >= int(self.runtime.get("max_population", MAX_POP)):
            return False
        
        # Chance de conception
        chance = 0.15 * (0.5 + a.energy * 0.5) * (0.5 + b.energy * 0.5)
        if self.rng.random() > chance:
            return False
        
        # Création de l'enfant
        child = self.spawn_agent(
            x=a.x + self.rng.uniform(-5, 5),
            y=a.y + self.rng.uniform(-5, 5)
        )
        if not child:
            return False
        
        child.stage = "enfant"
        child.age = 0
        child.parents = (a.eid, b.eid)
        a.children.append(child.eid)
        b.children.append(child.eid)
        
        # Hérédité partielle (gènes, valeurs, traits)
        child.cog = self._inherit_traits(a.cog, b.cog)
        child.body = self._inherit_traits(a.body, b.body)
        child.personality = self._inherit_traits(a.personality, b.personality)
        
        # Héritage culturel/valeurs
        for k, v in a.anima["values"].items():
            child.anima["values"][k] = min(1.0, v * 0.7 + b.anima["values"].get(k, 0.5) * 0.3)
        for k, v in a.anima["identity"].items():
            child.anima["identity"][k] = min(1.0, v * 0.6 + b.anima["identity"].get(k, 0.5) * 0.4)
        
        child.bonded = None
        child.married = False
        child.partner_id = None
        child.home = a.home
        
        # Anima
        a.anima_add_identity("provider", 0.05)
        b.anima_add_identity("provider", 0.05)
        a.anima_add_value("family", 0.1)
        b.anima_add_value("family", 0.1)
        
        self._record_anima(a, "birth", (a.tx, a.ty), actors=[a.eid, b.eid, child.eid],
                           action="birth", outcome="success", social_impact=1.0)
        self._record_anima(b, "birth", (b.tx, b.ty), actors=[a.eid, b.eid, child.eid],
                           action="birth", outcome="success", social_impact=1.0)
        
        self.stats["births"] += 1
        self.log(f"{a.name} et {b.name} ont un enfant : {child.name} !", (150, 255, 150), "social")
        return True

    def _advance_relationships(self, alive_agents: list):
        """Fait progresser les relations : lien -> proposition -> mariage -> enfant."""
        for a in alive_agents:
            if not a.alive:
                continue
            
            # 1. Lien d'attachement (bonded)
            if a.bonded is None:
                for b in alive_agents:
                    if a.eid >= b.eid or not b.alive or b.bonded:
                        continue
                    if (a.trust(b.eid) >= 0.6 and b.trust(a.eid) >= 0.6 and
                        a.rel.get(b.eid, [0, 0])[1] >= 0.5 and
                        b.rel.get(a.eid, [0, 0])[1] >= 0.5 and
                        a.stage == "adulte" and b.stage == "adulte"):
                        self.try_bond(a, b)
                        break
            
            # 2. Proposition de mariage
            elif a.bonded is not None and not a.married:
                b = self._by_eid(a.bonded)
                if b and b.alive and not b.married:
                    if (a.trust(b.eid) >= 0.75 and b.trust(a.eid) >= 0.75 and
                        a.rel.get(b.eid, [0, 0])[1] >= 0.7 and
                        b.rel.get(a.eid, [0, 0])[1] >= 0.7 and
                        a.stage == "adulte" and b.stage == "adulte"):
                        self.try_propose(a, b)
            
            # 3. Tentative d'enfant
            elif a.married and a.partner_id:
                b = self._by_eid(a.partner_id)
                if b and b.alive and b.married and b.partner_id == a.eid:
                    if (a.home and b.home and a.home == b.home and
                        a.energy > 0.5 and b.energy > 0.5 and
                        a.hunger < 0.6 and b.hunger < 0.6):
                        self.try_have_child(a, b)

    def _inherit_traits(self, t1: np.ndarray, t2: np.ndarray) -> np.ndarray:
        """Mélange deux tableaux de traits avec mutation."""
        child = (t1 + t2) / 2
        mutation = self.rng.normal(0, 0.05, size=child.shape)
        return np.clip(child + mutation, 0, 1)

    def _try_reproduce_with_partner(self, a: Being) -> bool:
        """Tente la reproduction avec le partenaire (méthode moderne)."""
        if (a.energy < 0.55 or a.repro_cd > 0
           or a.child or a.age > AGE_ELDER_TICKS):
            return False
        # Doit être marié pour avoir un enfant
        if not a.married or a.partner_id is None:
            return
        mate = self._by_eid(a.partner_id)
        if mate is None or not mate.alive or not mate.married:
            return
        if mate.energy < 0.45 or mate.repro_cd > 0:
            return
        if max(abs(mate.tx - a.tx), abs(mate.ty - a.ty)) > 12:
            return
        # vérifier sexe opposé
        if a.sex == mate.sex:
            return
        # vérifier pas de parenté directe (inceste)
        if self._are_related(a, mate):
            return
        # vérifier abri + nourriture à proximité du foyer
        if not self._has_shelter_and_food(a, mate):
            return
        # coût énergétique
        a.energy -= 0.28
        mate.energy -= 0.28
        # Taux de naissance : 0.01 (défaut) ↔ cooldown de base 2600 ticks.
        birth_rate = max(1e-6, float(self.runtime.get("birth_rate", 0.01)))
        cooldown = int(max(200.0, 2600.0 * (0.01 / birth_rate)))
        a.repro_cd = mate.repro_cd = cooldown
        # hérédité : héritage du champion de l'Academy + mutation
        champ = self.academy.champion_params
        n = a.brain.n
        if champ is not None and self.academy.champion_size == n:
            params = champ.copy()
            params += self.rng.normal(0, 0.05, params.shape)
        else:
            params, n = Brain.breed(a.brain, mate.brain, None, self.rng)
        pers = np.clip((a.personality + mate.personality) / 2
                       + self.rng.normal(0, 0.08, 12), 0, 1)
        body = np.clip((a.body + mate.body) / 2
                       + self.rng.normal(0, 0.06, 5), 0, 1)
        cog = np.clip((a.cog + mate.cog) / 2
                       + self.rng.normal(0, 0.06, 4), 0, 1)
        color = mate.color if self.rng.random() < 0.5 else a.color
        child = self.spawn_agent(x=(a.x + mate.x) / 2, y=(a.y + mate.y) / 2,
                                 color=color, gen=max(a.gen, mate.gen) + 1,
                                 brain=Brain(n_hid=n, params=params),
                                 parents=(a.eid, mate.eid), energy=0.5,
                                 personality=pers, n_hid=n, body=body, cog=cog)
        if child is None:
            return
        child.parent_pere_id = a.eid if a.sex == "M" else mate.eid
        child.parent_mere_id = a.eid if a.sex == "F" else mate.eid
        a.children.append(child.eid)
        mate.children.append(child.eid)
        a.emotions[1] = min(1.0, a.emotions[1] + 0.25)
        mate.emotions[1] = min(1.0, mate.emotions[1] + 0.25)
        a.life.append(("enfant", child.name))
        # ── Lot K : héritage partiel des valeurs Anima ──
        for vk in child.anima.get("values", {}):
            pa_val = a.anima.get("values", {}).get(vk, 0.5)
            pb_val = mate.anima.get("values", {}).get(vk, 0.5)
            child.anima["values"][vk] = child.anima_clamp(
                0.5 * ((pa_val + pb_val) / 2) + 0.2 * self.rng.random()
                + 0.3 * child.anima["values"][vk]
            )
        self.stats["births"] += 1
        if self.stats["births"] % 3 == 1:
            self.log(f"{a.name} et {mate.name} ont un enfant : {child.name} "
                     f"(cerveau {n} neurones).", (78, 168, 232), "life")
        self.lab.event(self.w.tick, "birth", eid=child.eid, parent1=a.eid, parent2=mate.eid,
                       name=child.name, brain_size=n)
        # Anima: episode birth
        self._record_anima(
            a, "birth", (a.tx, a.ty),
            actors=[a.eid, mate.eid, child.eid], action="birth",
            outcome="success", social_impact=0.6, achievement=0.3)
        self._record_anima(
            mate, "birth", (mate.tx, mate.ty),
            actors=[mate.eid, a.eid, child.eid], action="birth",
            outcome="success", social_impact=0.6, achievement=0.3)

    def _are_related(self, a, b):
        """Vérifie parenté directe (parent/enfant ou frères/sœurs)."""
        # parent/enfant
        if a.eid == b.parent_pere_id or a.eid == b.parent_mere_id:
            return True
        if b.eid == a.parent_pere_id or b.eid == a.parent_mere_id:
            return True
        # frères/sœurs (mêmes parents)
        if (a.parent_pere_id is not None and a.parent_pere_id == b.parent_pere_id) \
           or (a.parent_mere_id is not None and a.parent_mere_id == b.parent_mere_id):
            return True
        return False

    def _has_shelter_and_food(self, a, mate):
        """Vérifie qu'il y a un abri ET de la nourriture à proximité du couple."""
        mx, my = int((a.tx + mate.tx) / 2), int((a.ty + mate.ty) / 2)
        has_shelter = False
        has_food = False
        for dy in range(-6, 7):
            if has_shelter and has_food:
                break
            for dx in range(-6, 7):
                if has_shelter and has_food:
                    break
                x, y = mx + dx, my + dy
                if not (0 <= x < self.w.g and 0 <= y < self.w.g):
                    continue
                aid = self.w.content_at(x, y)
                if aid >= 0:
                    asd = self.am.assets[aid]
                    if asd.shelter:
                        has_shelter = True
                    if asd.edible > 0:
                        has_food = True
        # nourriture au sol (items food) via index spatial
        if not has_food:
            cell = 128
            cx, cy = int(((a.x + mate.x) / 2) // cell), int(((a.y + mate.y) / 2) // cell)
            r = max(1, math.ceil(6 * TILE / cell))
            r2 = (6 * TILE) ** 2
            mid_x, mid_y = (a.x + mate.x) / 2, (a.y + mate.y) / 2
            for yy in range(cy - r, cy + r + 1):
                for xx in range(cx - r, cx + r + 1):
                    for item in self.food_cells.get((xx, yy), ()):
                        if (item.x - mid_x) ** 2 + (item.y - mid_y) ** 2 <= r2:
                            has_food = True
                            break
                    if has_food:
                        break
                if has_food:
                    break
        return has_shelter and has_food

    # ------------------------------------------------------------------ societe detectee
    def _analyze_society(self):
        self.society = []
        alive = [a for a in self.agents if getattr(a, "alive", True)]
        self.society.append(f"Villages : {self.stats['villages']}")
        routes = [(k, v) for k, v in self._trade.items() if v >= 4]
        if routes:
            self.society.append(f"Routes d'échange : {len(routes)}")

        # ── hiérarchie + royaumes émergents ──
        dom = sorted(self._dominance.items(), key=lambda kv: -kv[1])
        if dom and dom[0][1] >= 4:
            b = self._by_eid(dom[0][0])
            if b:
                self.society.append(f"Hiérarchie : {b.name} domine ({dom[0][1]} victoires)")
                # compter les suivants (agents dont la plus haute confiance pointe vers ce dominant)
                followers = []
                for a in alive:
                    if a.eid == b.eid or not a.rel:
                        continue
                    best_eid = max(a.rel.items(), key=lambda kv: kv[1][0])[0]
                    if best_eid == b.eid and a.rel[best_eid][0] > 0.3:
                        followers.append(a)
                if len(followers) >= 6:
                    clans_suivis = set(a.color for a in followers)
                    self.society.append(
                        f"Royaume émergent : {b.name} suivi par {len(followers)} "
                        f"êtres ({', '.join(clans_suivis)})")

        # ── clans spécialisés ──
        for c in ("blue", "red", "yellow", "purple", "black"):
            grp = [a for a in alive if a.color == c]
            if len(grp) >= 4:
                sk = float(np.mean([a.skills[0] for a in grp]))
                if sk > 0.5:
                    self.society.append(f"Spécialisation : les {c} récolteurs ({sk:.0%})")

        # ── clans agricoles (ceux qui plantent) ──
        planters = [a for a in alive if a.inv.get("graine", 0) > 0]
        if len(planters) >= 3:
            planter_clans = {}
            for a in planters:
                planter_clans[a.color] = planter_clans.get(a.color, 0) + 1
            best_clan = max(planter_clans, key=planter_clans.get)
            if planter_clans[best_clan] >= 2:
                self.society.append(
                    f"Clan agricole : les {best_clan} "
                    f"({planter_clans[best_clan]} portent des graines)")

        bonded = sum(1 for a in alive if a.bonded) // 2
        if bonded:
            self.society.append(f"Couples liés : {bonded}")

        # ── Progression passive : confiance/affection entre proches ──
        if self.w.tick % 60 == 0:
            for a in alive:
                if not a.alive:
                    continue
                for b in alive:
                    if a.eid >= b.eid or not b.alive:
                        continue
                    dist = max(abs(a.tx - b.tx), abs(a.ty - b.ty))
                    if dist <= 3:
                        a.rel.setdefault(b.eid, [0.0, 0.0])[0] = min(1.0, a.rel.setdefault(b.eid, [0.0, 0.0])[0] + 0.01)
                        b.rel.setdefault(a.eid, [0.0, 0.0])[0] = min(1.0, b.rel.setdefault(a.eid, [0.0, 0.0])[0] + 0.01)
                        a.rel.setdefault(b.eid, [0.0, 0.0])[1] = min(1.0, a.rel.setdefault(b.eid, [0.0, 0.0])[1] + 0.005)
                        b.rel.setdefault(a.eid, [0.0, 0.0])[1] = min(1.0, b.rel.setdefault(a.eid, [0.0, 0.0])[1] + 0.005)
        
    def export_academy_model(self, name="champion"):
        return self.academy.export_model(
            f"data/models/{name}", self.universal_knowledge, label=name
        )
    def _sheep(self, s: Sheep):
        w = self.w
        tick = w.tick

        # --- Update cadence based on state ---
        # Flee/fear: every tick; grazing: every 8; calm: every 12
        if s.state == "flee" or s.fear >= 0.40:
            update_cadence = 1 if s.fear >= 0.40 else 1
        elif s.state == "graze":
            update_cadence = 8
        else:
            update_cadence = 12

        if tick < s.next_update_tick and s.state not in ("flee",):
            # Cheap energy/grazing only, no neighbor scans
            s.reproduction_cooldown = max(0, s.reproduction_cooldown - 1)

            # Base metabolism even when skipping full update
            s.energy -= 0.00022
            s.anim_t += 1
            if s.anim_t % 7 == 0:
                s.frame += 1

            # Continue current behavior
            if s.state == "graze" and s.graze_until_tick > w.tick:
                s.energy = min(1.0, s.energy + 0.0012)
            elif w.tick < s.next_decision_tick:
                # Wander using cached direction
                self._move(s, s.wander_dx * 0.25, s.wander_dy * 0.25, sheep=True)
                s.energy = max(0.0, s.energy - 0.00015)
            else:
                # Fallback to graze if no decision pending
                s.state = "graze"
                s.energy = min(1.0, s.energy + 0.0012)

            # Death check
            if s.energy <= 0:
                s.health -= 0.002
            if s.health <= 0:
                self._kill_sheep(s)

            # Schedule next update
            s.next_update_tick = tick + update_cadence
            return

        # --- Full update for this tick ---
        s.next_update_tick = tick + update_cadence
        s.reproduction_cooldown = max(0, s.reproduction_cooldown - 1)

        # --- Threat scan (cached between scans) ---
        scan_cadence = 1 if (s.state == "flee" or s.fear >= 0.40) else \
                       (2 if s.fear > 0 else (8 if s.state == "graze" else 12))

        if tick >= s.next_neighbor_scan_tick:
            s.next_neighbor_scan_tick = tick + scan_cadence
            # Scan for threats
            threats = self._near(s.x, s.y,
                                 lambda e: isinstance(e, Monster) and e.hostile,
                                 r=2)
            if not threats:
                threats = self._near(s.x, s.y,
                                     lambda e: isinstance(e, Being) and e.alive
                                     and e.fear > 0.7,
                                     r=2)

            if threats:
                threat = min(threats,
                             key=lambda e: (e.x - s.x) ** 2 + (e.y - s.y) ** 2)
                s.cached_threat_dx = threat.x - s.x
                s.cached_threat_dy = threat.y - s.y
            else:
                s.cached_threat_dx = 0.0
                s.cached_threat_dy = 0.0

        # --- React to cached threat ---
        if s.cached_threat_dx != 0.0 or s.cached_threat_dy != 0.0:
            dx = s.cached_threat_dx
            dy = s.cached_threat_dy
            dist = max(1.0, math.hypot(dx, dy))
            self._move(s, -dx / dist * 1.2, -dy / dist * 1.2, sheep=True)
            s.fear = min(1.0, s.fear + 0.10)
            s.energy = max(0.0, s.energy - 0.0015)
            s.state = "flee"
            # Override cadence for immediate reaction
            s.next_update_tick = tick + 1
            s.next_neighbor_scan_tick = tick + 1
            return

        # No cached threat -> fear decays
        s.fear = max(0.0, s.fear - 0.01)

        # --- Grazing continues without scans ---
        if s.graze_until_tick > w.tick:
            s.energy = min(1.0, s.energy + 0.0012)
            s.state = "graze"
            return

        # Waiting for next decision tick -> light wander
        if w.tick < s.next_decision_tick:
            self._move(s, s.wander_dx * 0.25, s.wander_dy * 0.25, sheep=True)
            s.energy = max(0.0, s.energy - 0.00015)
            s.state = "walk"
            return

        # --- Time for new decision (wander/graze) ---
        s.graze_until_tick = tick + int(self.rng.integers(15, 45))
        angle = float(self.rng.uniform(0.0, 6.283))
        s.wander_dx = math.cos(angle)
        s.wander_dy = math.sin(angle)
        s.next_decision_tick = tick + int(self.rng.integers(20, 60))

        # --- Herd scan (every 30 ticks max) ---
        if tick >= s.herd_scan_tick:
            s.herd_scan_tick = tick + 30
            near_sheep = self._near(s.x, s.y,
                                    lambda e: isinstance(e, Sheep) and e.alive,
                                    r=3)
            if near_sheep and len(near_sheep) > 1:
                cx = sum(e.x for e in near_sheep) / len(near_sheep)
                cy = sum(e.y for e in near_sheep) / len(near_sheep)
                dx = cx - s.x
                dy = cy - s.y
                dist = max(1.0, math.hypot(dx, dy))
                s.cached_herd_dx = dx / dist
                s.cached_herd_dy = dy / dist
            else:
                s.cached_herd_dx = 0.0
                s.cached_herd_dy = 0.0

        # Apply cached herd direction
        if s.cached_herd_dx != 0.0 or s.cached_herd_dy != 0.0:
            s.wander_dx = s.wander_dx * 0.5 + s.cached_herd_dx * 0.5
            s.wander_dy = s.wander_dy * 0.5 + s.cached_herd_dy * 0.5

        s.state = "graze"

        # Base metabolism
        s.energy -= 0.00022
        s.anim_t += 1
        if s.anim_t % 7 == 0:
            s.frame += 1
        if s.energy <= 0:
            s.health -= 0.002
        if s.health <= 0:
            self._kill_sheep(s)
            return

        # Reproduction
        if (s.energy > 0.95 and s.reproduction_cooldown == 0
                and len(self.sheep) < MAX_SHEEP):
            s.energy = 0.55
            s.reproduction_cooldown = 3600
            self.spawn_sheep(x=s.x + 10, y=s.y)

    def _monster(self, m: Monster):
        w = self.w
        m.energy -= 0.00018
        near_humans = self._near(m.x, m.y,
                                 lambda e: isinstance(e, Being) and e.alive,
                                 r=m.sight)
        near_sheep = self._near(m.x, m.y,
                                lambda e: isinstance(e, Sheep) and e.alive,
                                r=m.sight)
        target = None
        if near_humans:
            target = min(near_humans, key=lambda e: (e.x - m.x)**2 + (e.y - m.y)**2)
        elif near_sheep:
            target = min(near_sheep, key=lambda e: (e.x - m.x)**2 + (e.y - m.y)**2)

        if m.hostile and target and m.energy > 0.1:
            dx = target.x - m.x
            dy = target.y - m.y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < 14:
                target.health -= m.damage
                m.state = "attack"
                if isinstance(target, Being):
                    self._record_anima(
                        target, "monster_attack",
                        (target.tx, target.ty),
                        actors=[target.eid, m.eid], action="hit",
                        outcome="injured",
                        health_loss=m.damage,
                        fear=min(1.0, m.damage * 2.5),
                        surprise=0.6,
                    )
            elif dist > 0:
                mvx = dx / dist
                mvy = dy / dist
                mvx, mvy = self._zone_deflect(m, mvx, mvy, 0.6 * 8)
                self._move(m, mvx * 0.6, mvy * 0.6, sheep=True)
        else:
            mvx = self.rng.uniform(-1, 1)
            mvy = self.rng.uniform(-1, 1)
            mvx, mvy = self._zone_deflect(m, mvx, mvy, 0.3 * 8)
            self._move(m, mvx * 0.3, mvy * 0.3, sheep=True)

        m.anim_t += 1
        if m.anim_t % 7 == 0:
            m.frame += 1
        if m.energy <= 0:
            m.health -= 0.002
        if m.health <= 0:
            m.alive = False
            self.monsters = [x for x in self.monsters if x.alive]
            self._entity_cells.pop(m.eid, None)

    def _zone_deflect(self, m, mvx, mvy, probe_px):
        """Inverse la direction si la zone prédateur interdit la cible."""
        from .zones import can_monster_enter
        ntx = int((m.x + mvx * probe_px) // TILE)
        nty = int((m.y + mvy * probe_px) // TILE)
        if can_monster_enter(self, m, ntx, nty):
            return mvx, mvy
        return -mvx, -mvy

    # ------------------------------------------------------------------ pathfinding local
    def _local_bfs(self, start_tx, start_ty, goal_fn, max_r=15):
        """BFS local : cherche un chemin autour des obstacles.
        Retourne le premier pas (dx, dy) à effectuer pour suivre le gradient.
        """
        from collections import deque
        q = deque([(start_tx, start_ty)])
        came_from = {(start_tx, start_ty): None}
        w = self.w
        while q:
            cx, cy = q.popleft()
            if goal_fn(cx, cy):
                curr = (cx, cy)
                if curr == (start_tx, start_ty):
                    return 0, 0
                while came_from[curr] != (start_tx, start_ty):
                    curr = came_from[curr]
                return curr[0] - start_tx, curr[1] - start_ty
            if len(came_from) > max_r * max_r * 3:
                break
            for ddx, ddy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)):
                nx, ny = cx+ddx, cy+ddy
                if 0 <= nx < w.g and 0 <= ny < w.g and (nx, ny) not in came_from:
                    if w.land[ny, nx] and not w.blocked[ny, nx]:
                        came_from[(nx, ny)] = (cx, cy)
                        q.append((nx, ny))
        return 0, 0

    # ------------------------------------------------------------------ physique
    def _move(self, e, dx, dy, sheep=False):
        w = self.w
        r = 4.0
        nx, ny = e.x + dx, e.y + dy
        if not self._free(nx, e.y, r):
            nx = e.x
        if not self._free(nx, ny, r):
            ny = e.y
        e.x = min(max(4.0, nx), (GRID - 1) * TILE + 12)
        e.y = min(max(4.0, ny), (GRID - 1) * TILE + 12)
        if sheep and abs(dx) + abs(dy) > 0.2:
            e.vx, e.vy = dx, dy
        if hasattr(e, 'eid'):
            self._update_entity_bucket(e)

    def _update_entity_bucket(self, e):
        cx, cy = int(e.x // 32), int(e.y // 32)
        key = (cx, cy)
        old = self._entity_cells.get(e.eid)
        if old == key:
            return
        if old is not None:
            bucket = self.grid_bucket.get(old)
            if bucket and e in bucket:
                bucket.remove(e)
                if not bucket:
                    del self.grid_bucket[old]
        self.grid_bucket.setdefault(key, []).append(e)
        self._entity_cells[e.eid] = key

    def _free(self, x, y, r):
        w = self.w
        x0, y0 = int((x - r) // TILE), int((y - r) // TILE)
        x1, y1 = int((x + r) // TILE), int((y + r) // TILE)
        if x0 < 0 or y0 < 0 or x1 > w.g - 1 or y1 > w.g - 1:
            return False
        if not w.land[y0:y1 + 1, x0:x1 + 1].all():
            return False
        return not w.blocked[y0:y1 + 1, x0:x1 + 1].any()

    # ------------------------------------------------------------------ appel global
    def _forget_dead_agents(self):
        """Purge les cadavres de ``agents`` en gardant une fiche pour l'UI."""
        if any(not a.alive for a in self.agents):
            from .diagnostics import deceased_row
            for a in self.agents:
                if not a.alive:
                    self.deceased.append(deceased_row(self, a))
            self.agents = [a for a in self.agents if a.alive]

    def tick(self):
        prev_agents = len(self.agents)
        prev_sheep = len(self.sheep)

        self.step()
        for a in list(self.agents):
            if a.alive:
                self._try_reproduce_with_partner(a)
        self._forget_dead_agents()

        # Increment population revision only on structural changes
        if len(self.agents) != prev_agents or len(self.sheep) != prev_sheep:
            self.population_revision += 1

    def natural_pop(self):
        return len(self.agents), len(self.sheep), len(self.w.items)
