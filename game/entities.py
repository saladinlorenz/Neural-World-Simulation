"""Being — composition d'un etre (document d'architecture §4).

Identite, Corps, Perception, Cognition, Memoire (episodique + semantique +
spatiale + sociale), Emotions, Personnalite, Besoins, Motivations (emergentes),
Volonte (inertie/persistance), Soi (estime, autobiographie), Imagination
(projection), Croyances (lieux dangereux, etres de confiance), Relations
(directionnelles), Experience, Competences, Habitudes, Inventaire, Cerveau.

Tout est reglable a la creation et pendant la vie — SAUF la taille du cerveau,
verrouillee a l'insertion pour toujours."""
import math
from collections import deque

import numpy as np

from .brain import Brain
from .config import (
    CLAN_COLORS, TILE, TICKS_PER_YEAR, AGE_CHILD_TICKS, AGE_ELDER_TICKS,
    AGE_MIN_NATURAL_DEATH_TICKS, AGE_MAX_NATURAL_DEATH_TICKS,
)

NAME_SYLL = ["Aa", "Be", "Co", "Dra", "El", "Fa", "Gi", "Ha", "I", "Jo", "Ka", "Lo",
             "Me", "Na", "O", "Pyr", "Qu", "Ro", "Sa", "Ti", "U", "Vane", "Wi", "Xo",
             "Yla", "Zo", "Mor", "Nim", "Sal", "Tor", "Ul", "Vre", "Yn", "Zeph"]

# categories de memoire spatiale
MEM_CATS = ("food", "wood", "stone", "water", "shelter", "agent")


class ClanKnowledge:
    """Mémoire commune du clan : géographie, ressources, dangers partagés."""
    def __init__(self):
        self.places = {}       # (cat, tx//8, ty//8) -> (founder_eid, tick, strength)
        self.dangers = {}      # (tx//8, ty//8) -> (reporter_eid, tick, level)
        self.reservations = {} # (tx, ty) -> eid (agent qui occupe la place)
        # Lot I : connaissances culturelles
        self.culture = {}      # (claim, tx//8, ty//8) -> {confidence, sources, confirmations, last_update}
        # Lot J : institutions émergentes
        self.institutions = {}  # (kind, tx//8, ty//8) -> {members, practices, trust, age, stability}

    def share_place(self, cat, tx, ty, eid, tick):
        key = (cat, tx // 8, ty // 8)
        old = self.places.get(key)
        if old is None or tick - old[2] > 500:
            self.places[key] = (eid, tick, min(1.0, (old[2] if old else 0) + 0.3))

    def report_danger(self, tx, ty, eid, tick, level=0.8):
        key = (tx // 8, ty // 8)
        old = self.dangers.get(key)
        if old is None or level > old[2]:
            self.dangers[key] = (eid, tick, level)

    def forget_danger(self, tx, ty, tick, decay_ticks=2000):
        key = (tx // 8, ty // 8)
        old = self.dangers.get(key)
        if old and tick - old[1] > decay_ticks:
            del self.dangers[key]

    def reserve(self, tx, ty, eid):
        self.reservations[(tx, ty)] = eid

    def release(self, tx, ty):
        self.reservations.pop((tx, ty), None)

    def is_reserved(self, tx, ty, eid):
        r = self.reservations.get((tx, ty))
        return r is not None and r != eid

    def nearby_places(self, cat, tx, ty, max_dist=60):
        """Retourne les lieux connus dans un rayon donné."""
        out = []
        for (c, cx8, cy8), (fid, t, s) in self.places.items():
            if c != cat:
                continue
            d = max(abs(cx8 * 8 - tx), abs(cy8 * 8 - ty))
            if d < max_dist:
                out.append((cx8 * 8, cy8 * 8, s, d))
        out.sort(key=lambda t: t[2] / (1 + t[3] * 0.1), reverse=True)
        return out

    # ── Lot I : culture ──

    def report_culture(self, claim, tx, ty, eid, tick):
        """Signale une connaissance culturelle."""
        key = (claim, tx // 8, ty // 8)
        entry = self.culture.get(key)
        if entry is None:
            self.culture[key] = {
                "confidence": 0.2, "sources": [eid],
                "confirmations": 1, "last_update": tick,
            }
        else:
            if eid not in entry["sources"]:
                entry["sources"].append(eid)
            entry["confirmations"] += 1
            entry["confidence"] = min(1.0, entry["confidence"] + 0.15)
            entry["last_update"] = tick

    def is_cultural(self, claim, tx, ty):
        """Une connaissance est culturelle si confirmée par plusieurs sources."""
        key = (claim, tx // 8, ty // 8)
        entry = self.culture.get(key)
        if entry is None:
            return False
        return (len(entry["sources"]) >= 2
                or entry["confirmations"] >= 3) and entry["confidence"] > 0.4

    # ── Lot J : institutions émergentes ──

    def add_institution(self, kind, tx, ty, eid, tick):
        """Ajoute un membre à une institution existante ou en crée une."""
        key = (kind, tx // 8, ty // 8)
        inst = self.institutions.get(key)
        if inst is None:
            self.institutions[key] = {
                "kind": kind, "members": [eid],
                "practices": {}, "trust": 0.3,
                "age": 0, "stability": 0.1,
                "created_tick": tick,
            }
        else:
            if eid not in inst["members"]:
                inst["members"].append(eid)
            inst["trust"] = min(1.0, inst["trust"] + 0.05)
            inst["stability"] = min(1.0, inst["stability"] + 0.03)

    def record_practice(self, kind, tx, ty, eid, action, tick):
        """Enregistre une pratique répétée dans une institution."""
        key = (kind, tx // 8, ty // 8)
        inst = self.institutions.get(key)
        if inst is None:
            return
        practices = inst.setdefault("practices", {})
        count = practices.get(action, 0)
        practices[action] = count + 1
        if count + 1 >= 3:
            inst["stability"] = min(1.0, inst["stability"] + 0.05)
        inst["age"] = tick - inst.get("created_tick", tick)
        inst["last_practice_tick"] = tick

    def decay_institutions(self, tick, rate=0.001):
        """Dégrade les institutions inactives."""
        for key in list(self.institutions.keys()):
            inst = self.institutions[key]
            if tick - inst.get("last_practice_tick", inst.get("created_tick", 0)) > 5000:
                inst["stability"] *= (1.0 - rate)
                if inst["stability"] < 0.05:
                    del self.institutions[key]


class Being:
    """Un habitant : un corps, un esprit, une histoire."""

    def __init__(self, eid, x, y, color, cls, states, gen=0, brain=None, parents=(),
                 personality=None, rng=None, born_tick=0, n_hid=128,
                 body=None, cog=None, emotions=None, needs=None, sex=None):
        rng = rng or np.random.default_rng(eid * 7919 + 13)
        # ---- Identite / Soi
        self.eid = eid
        self.name = rng.choice(NAME_SYLL) + rng.choice(NAME_SYLL)
        self.gen = gen
        self.color = color
        self.cls = cls
        self.parents = parents
        self.children = []
        self.born_tick = born_tick
        self.life = deque(maxlen=48)          # autobiographie (events marquants)
        self.self_esteem = 0.5
        # ---- Corps
        self.x, self.y = float(x), float(y)
        self.vx = self.vy = 0.0
        self.fx, self.fy = int(rng.integers(-1, 2)) or 1, int(rng.integers(-1, 2))
        self.sex = sex if sex is not None else ("F" if rng.random() < 0.5 else "M")
        self.age = 0
        self.natural_death_age = int(rng.integers(
            AGE_MIN_NATURAL_DEATH_TICKS,
            AGE_MAX_NATURAL_DEATH_TICKS + 1,
        ))
        self.body = body if body is not None else np.clip(
            rng.random(5) * 0.6 + 0.25, 0, 1)        # force endurance mobilite sens recuperation
        self.health = 1.0
        self.pain = 0.0
        self.temp = 0.5                              # temperature corporelle
        self.tool = -1
        self.tool_durability = 0
        self.inv = {"bois": 0, "pierre": 0, "or": 0, "graine": 0}
        # ---- Cognition / cerveau (TAILLE VERROUILLEE)
        self.brain = brain or Brain(n_hid=n_hid, rng=rng)
        self.cog = cog if cog is not None else np.clip(
            rng.random(4) * 0.6 + 0.25, 0, 1)        # memoire anticipation imagination attention
        # ---- Emotions (etats continus, jamais des if)
        self.emotions = emotions if emotions is not None else np.array(
            [0.0, 0.35, 0.0, 0.1, 0.1, 0.0, 0.0, 0.0])  # peur joie colere tristesse stress surprise degout affection
        # ---- Besoins
        self.needs = needs if needs is not None else np.array(
            [0.25, 0.70, 0.30, 0.30, 0.80, 0.50, 0.40])
        # faim energie soif sommeil securite appartenance estime
        self.energy = float(self.needs[1])
        self.hunger = float(self.needs[0])
        # ---- Personnalite (predispositions, pas programmations)
        self.personality = (personality if personality is not None
                            else np.clip(rng.random(12) * 0.7 + 0.15, 0, 1))
        # ---- Experience / competences / habitudes
        self.skills = np.zeros(4)                    # recolte construction combat social
        self.habits = np.full(15, 0.06)
        # ---- Memoire
        self.seen = {c: [] for c in MEM_CATS}        # spatiale: [(x,y,force)]
        self.episodes = deque(maxlen=64)             # episodique: (tick, type, data)
        self.belief_beings = {}                      # semantique sociale: eid -> trait -1..1
        self.belief_places = {}                      # croyances lieux: (cx,cy) -> danger 0..1
        self.known = {}
        self.kn_t = -99
        self._loc = np.zeros(8)
        self._near_agents = []
        self._near_sheep = []
        self._near_monsters = []
        self._last_heard = -1
        # ---- Relations (directionnelles)
        self.rel = {}                                # eid -> [confiance, affection]
        self.rep = 0.0
        self.hated = None
        self.bonded = None                           # partenaire (famille)
        self.dangers = []
        self.gave = {}
        self.talk_cd = {}
        # ---- Anima (memoire episodique emotive)
        self.anima = {
            "episodic_memory": deque(maxlen=200),
            "beliefs": {"places": {}, "beings": {}},
            "identity": {
                "builder": 0.0, "provider": 0.0, "fighter": 0.0,
                "explorer": 0.0, "caretaker": 0.0, "survivor": 0.0,
                "mediator": 0.0,
            },
            "values": {
                "survival": 0.8, "family": 0.6, "security": 0.7,
                "community": 0.5, "knowledge": 0.4,
                "wealth": 0.5, "generosity": 0.5,
            },
            "trauma": {"attack": 0.0, "hunger": 0.0, "loss": 0.0, "betrayal": 0.0, "fire": 0.0},
            "attachments": {},
            "intention": None,
            "plan": None,
            "reputation": {},
            "causal_traces": [],
            "observations": deque(maxlen=24),
        }
        # ---- Volonte
        self.goal = None                             # intention structuree (dict)
        self.goal_t = 0
        self.commitment = 0.0                        # engagement dans le but courant
        self.stuck = 0
        self.failed_targets = {}                     # {(act,tx,ty): (count, until_tick)}
        self.observed_actions = deque(maxlen=32)     # actions observees chez autrui
        self.context = {
            "food_density": 0.0,
            "wood_density": 0.0,
            "stone_density": 0.0,
            "sheep_count": 0.0,
            "monster_count": 0.0,
            "ally_count": 0.0,
            "enemy_count": 0.0,
            "storage_near": 0.0,
            "site_near": 0.0,
            "route_danger": 0.0,
        }
        self.prev_wellbeing = 0.0
        self.mood_phase = float(rng.uniform(0, math.tau))
        self.mood_freq = float(rng.uniform(0.004, 0.02))
        self.home = None
        self.work_t = 0
        self.atk_t = 0
        self.repro_cd = 400
        # ---- Mariage / reproduction / filiation
        self.married = False
        self.partner_id = None            # eid du conjoint
        self.parent_pere_id = None        # eid du père
        self.parent_mere_id = None        # eid de la mère
        self.affinity_cd = 0              # cooldown avant prochaine tentative drague
        self.state = "idle"
        self.alive = True
        self.avatar = int(rng.integers(0, 400))
        self.col_idx = 1
        self.frame = 0
        self.anim_t = 0
        self.states = states
        self._last_px, self._last_py = self.x, self.y

    # ------------------------------------------------------------------ cycle de vie
    @property
    def age_years(self) -> float:
        return self.age / float(TICKS_PER_YEAR)

    @property
    def age_label(self) -> str:
        return f"{self.age_years:.1f} ans"

    @property
    def stage(self):
        if self.age < AGE_CHILD_TICKS:
            return "enfant"
        if self.age < AGE_ELDER_TICKS:
            return "adulte"
        return "ancien"

    @property
    def child(self):
        return self.age < AGE_CHILD_TICKS

    def age_health_cap(self) -> float:
        """Fragilité progressive, sans décès biologique avant 65 ans."""
        if self.age <= AGE_ELDER_TICKS:
            return 1.0
        span = max(1, self.natural_death_age - AGE_ELDER_TICKS)
        u = min(1.0, (self.age - AGE_ELDER_TICKS) / span)
        smooth = u * u * (3.0 - 2.0 * u)
        return 1.0 - 0.65 * smooth

    @property
    def hunger(self):
        return self.needs[0]

    @hunger.setter
    def hunger(self, v):
        self.needs[0] = v

    @property
    def rgb(self):
        return CLAN_COLORS.get(self.color, (200, 200, 200))

    @property
    def tx(self):
        return int(self.x // TILE)

    @property
    def ty(self):
        return int(self.y // TILE)

    def carry(self):
        return self.inv["bois"] + self.inv["pierre"] + self.inv["or"]

    def mood(self, tick):
        return math.sin(tick * self.mood_freq + self.mood_phase)

    def speed(self, light=1.0, heat=0.0):
        if self.child:
            age_factor = 0.55
        elif self.age < AGE_ELDER_TICKS:
            age_factor = 1.0
        else:
            age_factor = max(0.40, 0.75 * self.age_health_cap())
        hurt = max(0.35, 1.0 - 0.5 * self.pain - 0.4 * max(0.0, 0.2 - self.needs[1]))
        load_weight = (self.inv.get("bois", 0) * 1.0 +
                       self.inv.get("pierre", 0) * 1.5 +
                       self.inv.get("or", 0) * 2.0 +
                       self.inv.get("graine", 0) * 0.2)
        load_factor = max(0.45, 1.0 - 0.04 * load_weight)
        road_bonus = min(0.18, heat * 0.08)
        return (2.7 * (0.6 + 0.7 * self.body[2]) * age_factor * hurt
                * (0.8 + 0.2 * light) * load_factor * (1.0 + road_bonus))

    def drain_f(self):
        return (1.35 - 0.7 * self.body[1]) * (1.25 if self.child else 1.0)

    def dmg_f(self):
        return (0.7 + 0.8 * self.body[0]) * (1 + 0.5 * self.skills[2]) * (0.5 if self.child else 1.0)

    def sense_r(self, light=1.0):
        base = 12 + 44 * self.body[3]
        return int(base * (0.45 + 0.55 * light) * (0.6 + 0.4 * self.cog[3]))

    def sense_r_near(self):
        """Vision court portée : 8 cases autour (Moore), pour actions physiques."""
        return 8

    def trust(self, other_eid):
        r = self.rel.get(other_eid)
        return r[0] if r else 0.0

    def remember(self, cat, x, y):
        """La perception d'aujourd'hui devient la memoire de demain."""
        lst = self.seen[cat]
        for i in range(len(lst) - 1, -1, -1):
            if lst[i][0] == x and lst[i][1] == y:
                lst[i] = (x, y, min(1.0, lst[i][2] + 0.5))
                return
        lst.append((x, y, 0.85))
        if len(lst) > 40:
            lst.sort(key=lambda t: -t[2])
            del lst[40:]

    def recall(self, cat, tx, ty):
        """Se souvenir : (x,y,dist) le plus proche dans ma memoire, ou None."""
        best, bd = None, 1e9
        for (x, y, f) in self.seen[cat]:
            if f < 0.18:
                continue
            d = max(abs(x - tx), abs(y - ty)) / (1.15 - 0.5 * f)   # le doute eloigne
            if d < bd:
                best, bd = (x, y), d
        return (best[0], best[1], bd) if best else None

    def forget(self, cat, x, y):
        """Un souvenir inaccessible devient une fausse croyance : on l'efface."""
        self.seen[cat] = [(sx, sy, f) for sx, sy, f in self.seen[cat]
                          if not (sx == x and sy == y)]

    def remember_event(self, kind, data=None):
        self.episodes.append((self.born_tick, kind, data))

    def remember_anima_episode(self, tick, kind, place, actors=None,
                               action="", outcome="", emotion=None,
                               importance=0.0, cap=None):
        """Enregistre un episode dans la memoire episodique Anima.

        ``cap`` = plafond runtime ``episodes_max`` (deque maxlen=200 est le
        plafond dur du paramètre) ; au-delà, le plus ancien est évicté.
        """
        if emotion is None:
            emotion = {}
        ep = {
            "tick": tick, "kind": kind, "place": place,
            "actors": actors or [], "action": action,
            "outcome": outcome, "emotion": emotion,
            "importance": importance,
        }
        if importance < 0.20:
            return ep
        mem = self.anima["episodic_memory"]
        mem.append(ep)
        if cap:
            cap = int(cap)
            while len(mem) > cap:
                mem.popleft()
        if importance >= 0.70:
            self._anima_strong_belief(kind, place, importance, emotion)
        else:
            self._anima_weak_belief(kind, place, importance)
        return ep

    def _anima_strong_belief(self, kind, place, importance, emotion):
        a = self.anima
        fear = emotion.get("fear", 0.0)
        cx, cy = place[0] // 8, place[1] // 8
        key = (cx, cy)
        old = a["beliefs"]["places"].get(key, 0.0)
        a["beliefs"]["places"][key] = min(1.0, max(old, importance * fear))
        if "attack" in kind:
            a["trauma"]["attack"] = min(1.0, a["trauma"]["attack"] + 0.15 * importance)
            a["identity"]["survivor"] = min(1.0, a["identity"]["survivor"] + 0.05)
        if "hunger" in kind:
            a["trauma"]["hunger"] = min(1.0, a["trauma"]["hunger"] + 0.10 * importance)
        if "loss" in kind:
            a["trauma"]["loss"] = min(1.0, a["trauma"]["loss"] + 0.12 * importance)

    def _anima_weak_belief(self, kind, place, importance):
        cx, cy = place[0] // 8, place[1] // 8
        key = (cx, cy)
        old = self.anima["beliefs"]["places"].get(key, 0.0)
        self.anima["beliefs"]["places"][key] = min(1.0, max(old, importance * 0.5))

    def anima_perceived_danger(self, tx, ty, base_danger):
        """Danger percu = visible + croyance + trauma - confiance allies."""
        a = self.anima
        cx, cy = tx // 8, ty // 8
        belief = a["beliefs"]["places"].get((cx, cy), 0.0)
        trauma_fear = min(1.0, a["trauma"]["attack"] * 0.4)
        ally_trust = min(0.3, len([e for e in a["attachments"].values()
                                    if e > 0.3]) * 0.1)
        perceived = base_danger + belief * 0.35 + trauma_fear - ally_trust
        return max(0.0, min(1.0, perceived))

    # ── Anima Phase 2 : API centralisee ──

    @staticmethod
    def anima_clamp(value: float) -> float:
        return max(0.0, min(1.0, float(value)))

    def anima_add_identity(self, key: str, delta: float) -> float:
        identity = self.anima.setdefault("identity", {})
        old = float(identity.get(key, 0.0))
        identity[key] = self.anima_clamp(old + float(delta))
        return identity[key]

    def anima_add_value(self, key: str, delta: float) -> float:
        values = self.anima.setdefault("values", {})
        old = float(values.get(key, 0.5))
        values[key] = self.anima_clamp(old + float(delta))
        return values[key]

    def anima_dominant_identity(self):
        identity = self.anima.get("identity", {})
        if not identity:
            return None
        key, score = max(identity.items(), key=lambda item: item[1])
        return key if score >= 0.20 else None

    def anima_decay_identity(self, amount: float = 0.001):
        for key, value in self.anima.get("identity", {}).items():
            self.anima["identity"][key] = self.anima_clamp(
                value * (1.0 - amount))

    # ── Lot C : trauma, résilience, attachement ──

    def anima_decay_trauma(self, safety: float = 1.0, support: float = 0.0):
        """Décroissance du trauma basée sur sécurité et soutien social."""
        recovery = 0.0005 + 0.0015 * self.personality[5]
        rate = recovery * max(0.35, safety) * (0.6 + 0.4 * min(1.0, support))
        for key in self.anima.get("trauma", {}):
            self.anima["trauma"][key] = self.anima_clamp(
                self.anima["trauma"][key] * (1.0 - rate))

    def anima_add_attachment(self, key, delta: float):
        """Ajoute un delta d'attachement pour une cible (eid, lieu, etc.)."""
        att = self.anima.setdefault("attachments", {})
        att[key] = self.anima_clamp(att.get(key, 0.0) + delta)

    def anima_get_attachment(self, key) -> float:
        return self.anima.get("attachments", {}).get(key, 0.0)

    def anima_home_preference(self) -> float:
        """Préférence de retour au foyer basée sur attachement."""
        if self.home is None:
            return 0.0
        key = f"home:{self.home[0]}:{self.home[1]}"
        return self.anima_get_attachment(key) * 0.3

    # ── Lot D : intention psychologique persistante ──

    def anima_set_intention(self, kind: str, reason: str = "",
                            target=None, place=None,
                            priority: float = 0.5, tick: int = 0,
                            duration: int = 500):
        """Définit ou remplace l'intention Anima courante."""
        self.anima["intention"] = {
            "kind": kind,
            "reason": reason,
            "target": target,
            "place": place,
            "priority": self.anima_clamp(priority),
            "created_tick": tick,
            "expires_tick": tick + duration,
            "progress": 0.0,
        }

    def anima_clear_intention(self):
        self.anima["intention"] = None

    def anima_get_intention(self):
        return self.anima.get("intention")

    def anima_intention_valid(self, tick: int) -> bool:
        """Vérifie si l'intention courante est encore valide."""
        intent = self.anima.get("intention")
        if intent is None:
            return False
        if tick > intent.get("expires_tick", 0):
            self.anima["intention"] = None
            return False
        return True

    def anima_update_intention_progress(self, delta: float, tick: int):
        """Met à jour la progression de l'intention."""
        intent = self.anima.get("intention")
        if intent is None:
            return
        intent["priority"] = self.anima_clamp(intent["priority"] + delta)
        intent["expires_tick"] = tick + 500

    # ── Lot F : apprentissage causal différé ──

    def anima_add_causal_trace(self, action, place, tick, expected_effect=""):
        """Enregistre une trace causale pour crédit différé."""
        traces = self.anima.setdefault("causal_traces", [])
        traces.append({
            "tick": tick, "action": action, "place": place,
            "eligibility": 1.0, "contribution": 0.0,
            "expected_effect": expected_effect,
        })
        if len(traces) > 32:
            traces.pop(0)

    def anima_decay_causal_traces(self, rate: float = 0.02):
        traces = self.anima.get("causal_traces", [])
        for t in traces:
            t["eligibility"] *= (1.0 - rate)
        self.anima["causal_traces"] = [t for t in traces if t["eligibility"] > 0.05]

    def anima_credit_for(self, effect_kind, tick, max_delay=2000):
        """Retourne et consomme le crédit causale pour un effet donné."""
        traces = self.anima.get("causal_traces", [])
        credit = 0.0
        for t in traces:
            if t.get("expected_effect") == effect_kind and t["eligibility"] > 0.1:
                delay = tick - t.get("tick", 0)
                if 0 < delay < max_delay:
                    credit += t["eligibility"] * max(0.0, 1.0 - delay / max_delay)
                    t["contribution"] = min(1.0, t["contribution"] + 0.3)
                    t["eligibility"] *= 0.5
        return min(1.0, credit)

    # ── Lot H : imitation réelle ──

    def anima_record_observation(self, action, reward, tick):
        """Enregistre l'observation d'une action réussie par autrui."""
        obs = self.anima.setdefault("observations", deque(maxlen=24))
        obs.append({"action": int(action), "reward": float(reward), "tick": tick})

    def anima_apply_observation_learning(self):
        """Modifie les habitudes basées sur les observations."""
        obs = self.anima.get("observations")
        if not obs:
            return
        for o in list(obs):
            act = o.get("action", -1)
            reward = o.get("reward", 0.0)
            if 0 <= act < len(self.habits) and reward > 0:
                self.habits[act] = self.anima_clamp(
                    self.habits[act] + 0.01 * reward)
        obs.clear()

    # ── Lot 2 : memoire sociale personnelle ──

    def anima_social_belief(self, other_eid: int, tick: int):
        beliefs = self.anima.setdefault("beliefs", {}).setdefault("beings", {})
        eid = int(other_eid)
        existing = beliefs.get(eid)
        if existing is None or not isinstance(existing, dict):
            beliefs[eid] = {
                "trust": 0.5, "danger": 0.0, "generosity": 0.5,
                "reliability": 0.5, "confidence": 0.0,
                "last_update": int(tick),
            }
        return beliefs[eid]

    def anima_update_social_belief(self, other_eid: int, tick: int,
                                   trust_delta=0.0, danger_delta=0.0,
                                   generosity_delta=0.0,
                                   reliability_delta=0.0,
                                   confidence_delta=0.0):
        belief = self.anima_social_belief(other_eid, tick)
        for key, delta in {
            "trust": trust_delta, "danger": danger_delta,
            "generosity": generosity_delta,
            "reliability": reliability_delta,
            "confidence": confidence_delta,
        }.items():
            belief[key] = self.anima_clamp(
                float(belief.get(key, 0.0)) + float(delta))
        belief["last_update"] = int(tick)
        return belief

    def anima_social_score(self, other_eid: int) -> float:
        belief = (self.anima.get("beliefs", {})
                  .get("beings", {}).get(int(other_eid)))
        if not belief or not isinstance(belief, dict):
            return 0.0
        trust = float(belief.get("trust", 0.5))
        reliability = float(belief.get("reliability", 0.5))
        danger = float(belief.get("danger", 0.0))
        return (trust - 0.5) * 0.8 + (reliability - 0.5) * 0.4 - danger * 0.9

    def set_dir(self, dx, dy):
        dx, dy = float(dx), float(dy)
        if abs(dx) + abs(dy) < 0.08:
            return
        self.vx, self.vy = dx, dy
        self.fx = int(dx > 0.18) - int(dx < -0.18)
        self.fy = int(dy > 0.18) - int(dy < -0.18)
        if self.fx == 0 and self.fy == 0:
            self.fx = 1


class Sheep:
    __slots__ = ("eid", "x", "y", "vx", "vy", "energy", "health", "brain", "state",
                 "alive", "anim_t", "frame", "fear")

    def __init__(self, eid, x, y, brain=None):
        rng = np.random.default_rng(eid * 104729 + 7)
        self.eid = eid
        self.x, self.y = x, y
        self.vx = self.vy = 0.0
        self.energy = 0.6
        self.health = 1.0
        self.brain = brain or Brain(n_hid=64, rng=rng)
        self.state = "idle"
        self.alive = True
        self.anim_t = 0
        self.frame = 0
        self.fear = 0.0

    @property
    def tx(self):
        return int(self.x // TILE)

    @property
    def ty(self):
        return int(self.y // TILE)


class Monster:
    __slots__ = ("eid", "x", "y", "vx", "vy", "energy", "health", "kind",
                 "alive", "anim_t", "frame", "hostile", "damage", "sight",
                 "state", "zone_id")

    def __init__(self, eid, x, y, kind="wolf"):
        self.eid = eid
        self.x, self.y = x, y
        self.vx = self.vy = 0.0
        self.energy = 0.8
        self.health = 1.0
        self.kind = kind
        self.alive = True
        self.anim_t = 0
        self.frame = 0
        self.state = "idle"
        #: Lot G.2 : confinement dans une PredatorZone (None = libre).
        self.zone_id = None
        stats = {"bear": {"hostile": True, "damage": 0.18, "sight": 6},
                 "wolf": {"hostile": True, "damage": 0.12, "sight": 8},
                 "snake": {"hostile": True, "damage": 0.10, "sight": 5},
                 "beatle": {"hostile": False, "damage": 0.0, "sight": 3}}
        s = stats.get(kind, stats["wolf"])
        self.hostile = s["hostile"]
        self.damage = s["damage"]
        self.sight = s["sight"]

    @property
    def tx(self):
        return int(self.x // TILE)

    @property
    def ty(self):
        return int(self.y // TILE)


# compat nom historique (dashboard/renderer)
Inhabitant = Being
