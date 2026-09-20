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
from collections import deque

import numpy as np

from .brain_api import (ATTACK, BUILD, DRINK, DROP, EAT, EXPLORE, FLEE, GIVE,
                     HARVEST, MARK, N_IN, N_OUT, REST, SLEEP, SOCIAL, TAKE,
                     TALK, ACTION_NAMES_EXP as ACTION_NAMES, ACTION_TRAIT_EXP as ACTION_TRAIT)
from .brain import Brain
from .clock import Clock
from .config import (CLAN_COLORS, GRID, MAX_POP, MAX_SHEEP, TILE, WORLD_PX,
                     DEFAULT_SPAWN_AGE_TICKS, TICKS_PER_YEAR, AGE_ELDER_TICKS,
                     AGE_MAX_NATURAL_DEATH_TICKS, DAY_TICKS)
from .entities import Being, Sheep, Monster, ClanKnowledge
from .world import Item
from .universal_knowledge import UniversalKnowledge
from .academy import Academy
from .lab import LabRecorder
from .construction import ConstructionSite, blueprint_from_name

MAT_AIDS = {"bois": "item_wood", "pierre": "stone_res", "or": "gold_pile"}

# --- metabolisme (lois biologiques, pas des comportements)
HUNGER_RATE = 0.00012
THIRST_RATE = 0.00008
SLEEP_RATE_D = 0.00006
SLEEP_RATE_N = 0.00020
E_DRAIN = 0.00004
MOVE_DRAIN = 0.00018
REST_GAIN = 0.00180
SLEEP_GAIN = 0.00420
SHELTER_BONUS = 1.9
STARVE_HP = 0.00012
THIRST_HP = 0.00012
LOWE_HP = 0.00008
INV_CAP = 8
ATTACK_DMG = 0.16
ATTACK_DMG_TOOL = 0.30
WORK_TICKS = 6
PERCEPT_CELLS = 70          # echantillons de perception / tick / etre


class Sim:
    def __init__(self, world, am, seed=7):
        self.w = world
        self.am = am
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
        self.grid_bucket = {}
        self.item_bucket = {}
        self.food_cells = {}
        self._entity_cells = {}
        self.stats = dict(births=0, deaths=0, builds=0, villages=0, attacks=0,
                          gives=0, takes=0, talks=0, harvests=0, tool_found=0,
                          explored=0, drinks=0, sleeps=0, fires=0)
        self.journal = deque(maxlen=120)
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
        from .social_memory import SocialMemory
        self.social_memory = SocialMemory()

    # ------------------------------------------------------------------ journal
    def log(self, text, color=None, cat="monde"):
        """cat: combat|social|meteo|economie|vie|batiment|monde — groupés à l'affichage."""
        if self.journal and self.journal[-1][1] == text and self.w.tick - self.journal[-1][0] < 900:
            t0, tx, c, k, n = self.journal[-1]
            self.journal[-1] = (self.w.tick, tx, c, k, n + 1)
            return
        self.journal.append((self.w.tick, text, color, cat, 1))

    def emit_sound(self, x, y, kind, intensity=1.0):
        self.sounds.append((x, y, kind, intensity, self.w.tick))

    # ------------------------------------------------------------------ spawns
    def spawn_agent(self, x=None, y=None, color=None, gen=0, brain=None, parents=(),
                    energy=None, personality=None, n_hid=None, cls=None,
                    body=None, cog=None, emotions=None, needs=None, sex=None):
        if len(self.agents) >= MAX_POP:
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
        if parents is None:
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
        if len(self.monsters) >= 20:
            return
        kinds = ["bear", "wolf", "snake", "beatle"]
        for _ in range(30):
            if x is None:
                tx = int(self.rng.integers(6, GRID - 6))
                ty = int(self.rng.integers(6, GRID - 6))
            else:
                tx = min(GRID - 2, max(1, int(x // TILE)))
                ty = min(GRID - 2, max(1, int(y // TILE)))
            if self.w.land[ty, tx] and not self.w.blocked[ty, tx]:
                break
        k = kind or self.rng.choice(kinds)
        m = Monster(self.next_eid, tx * TILE + 8, ty * TILE + 8, kind=k)
        self.next_eid += 1
        self.monsters.append(m)
        cx, cy = int(m.x // 32), int(m.y // 32)
        self.grid_bucket.setdefault((cx, cy), []).append(m)
        self._entity_cells[m.eid] = (cx, cy)

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
        self.log(f"{a.name} a quitté le monde (retiré par {name}).", (148, 148, 208), "vie")
        self.agents[:] = [x for x in self.agents if x.alive]

    def _colidx(self, color):
        keys = self.am.unit_colors()
        return (keys.index(color) + 1) if color in keys else 1

    def _by_eid(self, eid):
        for a in self.agents:
            if a.eid == eid:
                return a
        return None

    # ------------------------------------------------------------------ step
    def step(self):
        w = self.w
        self.clock.step()
        w.step(self.am, self.clock)
        # feu : systeme physique pur (combustible + vent - pluie)
        burned = w.step_fire(self.am, self.clock.wind, self.clock.rain, self.am.flammable)
        if burned and w.tick % 30 == 0:
            self.stats["fires"] += 1
        if self.clock.lightning():
            for _ in range(3):
                tx, ty = int(self.rng.integers(GRID)), int(self.rng.integers(GRID))
                if w.land[ty, tx] and w.content_at(tx, ty) >= 0:
                    w.ignite(tx, ty)
                    self.log("La foudre a allumé un feu.", (218, 138, 58), "meteo")
                    break
        self._bucket()
        for a in self.agents:
            if a.alive:
                self._perceive(a)
                self._agent(a)
        for s in self.sheep:
            if s.alive:
                self._sheep(s)
        for m in self.monsters:
            if m.alive:
                self._monster(m)
        self.agents = [a for a in self.agents if a.alive]
        self.sheep = [s for s in self.sheep if s.alive]
        self.monsters = [m for m in self.monsters if m.alive]
        # nettoyage grid_bucket : entités mortes
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
        if w.tick % 300 == 0:
            self.universal_knowledge.sync_from_world(self.w, self.am, self.w.tick)
        if w.tick % 3600 == 0:
            self.social_memory.decay(self.w.tick)
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
            growth_rate = 0.001
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

    # ------------------------------------------------------------------ messages
    def send_fact(self, sender, receiver, category, tx, ty, confidence=0.6):
        trust = receiver.trust(sender.eid)
        if trust < -0.3:
            return False
        receiver.remember(category, tx, ty)
        receiver.episodes.append((self.w.tick, "message", {
            "from": sender.eid,
            "category": category,
            "tx": tx,
            "ty": ty,
            "confidence": confidence,
        }))
        return True
        if w.tick % 1800 == 0:
            for a in self.agents:
                if a.alive and not a.child:
                    accepted = self.academy.consider(a, self.w.tick)
                    if accepted:
                        self.log(f"Nouveau champion : {a.name} ({a.age_years:.1f} ans)",
                                 (88, 148, 228), "laboratoire")
        if w.tick % DAY_TICKS == 0:
            self.lab.snapshot(self)
        if __debug__ and w.tick % 600 == 0:
            from .invariants import validate_simulation
            for error in validate_simulation(self):
                self.log(f"INVARIANT: {error}", (214, 84, 84), "monde")
        if w.tick % 1800 == 0:
            for a in self.agents:
                expired = [k for k, (_, until) in a.failed_targets.items() if w.tick > until]
                for k in expired:
                    del a.failed_targets[k]

    def _bucket(self):
        self.item_bucket = {}
        self.food_cells = {}
        keep = []
        for it in self.w.items:
            it.life -= 1
            if it.life > 0:
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

    # ------------------------------------------------------------------ perception double : longue + courte portée
    def _perceive(self, a: Being):
        w = self.w
        light = self.clock.light
        R = a.sense_r(light)                    # longue portée (10-15 tiles)
        R_near = a.sense_r_near()               # courte portée (8 tiles = Moore)
        tx, ty = a.tx, a.ty
        w.heat[ty, tx] = min(1.0, w.heat[ty, tx] + 0.012)

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
                continue
            asd = self.am.assets[aid]
            if asd.edible > 0:
                a.remember("food", x, y)
                self.clan_knowledge.share_place("food", x, y, a.eid, w.tick)
            elif asd.harvest:
                m = asd.harvest["material"]
                cat = {"bois": "wood", "pierre": "stone",
                        "or": "stone"}.get(m, "wood")
                a.remember(cat, x, y)
                self.clan_knowledge.share_place(cat, x, y, a.eid, w.tick)
            elif asd.tool:
                a.remember("wood", x, y)
                self.clan_knowledge.share_place("wood", x, y, a.eid, w.tick)
            elif asd.shelter:
                a.remember("shelter", x, y)
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
        loc[1] = 1.0 if any(w.content_at(x, y) >= 0 and self.am.assets[w.content_at(x, y)].harvest
                            for x, y in self._ring(tx, ty)) else 0.0
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

        # ====== CONTEXTE LOCAL STRUCTURE ======
        def local_density(category):
            count = 0
            radius = 5
            for yy in range(max(0, ty - radius), min(w.g, ty + radius + 1)):
                for xx in range(max(0, tx - radius), min(w.g, tx + radius + 1)):
                    aid = w.content_at(xx, yy)
                    if aid < 0:
                        continue
                    asset = self.am.assets[aid]
                    if category == "food" and asset.edible > 0:
                        count += 1
                    elif category == "wood" and asset.harvest and asset.harvest.get("material") == "bois":
                        count += 1
                    elif category == "stone" and asset.harvest and asset.harvest.get("material") in ("pierre", "or"):
                        count += 1
            return min(1.0, count / 12.0)

        ctx = a.context
        ctx["food_density"] = local_density("food")
        ctx["wood_density"] = local_density("wood")
        ctx["stone_density"] = local_density("stone")
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
        return s

    # ------------------------------------------------------------------ arbitrage
    def _bias(self, a: Being):
        """Personnalite + emotions + besoins + croyances + risque -> bias de logits."""
        p, e, n = a.personality, a.emotions, a.needs
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
        bias[GIVE] += 0.5 * n[5] * p[0] + 0.4 * p[10]
        bias[BUILD] += 0.4 * n[6] * p[7] + 0.3 * p[9]
        bias[MARK] += 0.3 * n[6]
        bias[HARVEST] += 0.3 * a.skills[0]
        bias[BUILD] += 0.25 * a.skills[1]
        bias[TALK] += 0.2 * a.skills[3]
        bias += 0.5 * a.habits * (1.0 - 0.7 * p[6])
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
        f[HARVEST] = bool(a.recall("wood", a.tx, a.ty) or a.recall("stone", a.tx, a.ty))
        f[DRINK] = a.needs[2] > 0.32 and (a._loc[4] > 0 or bool(a.recall("water", a.tx, a.ty)))
        f[DROP] = a.carry() > 0
        f[BUILD] = ((a.inv.get("bois", 0) >= 6 and a.inv.get("pierre", 0) >= 2)
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
        f[TALK] = bool(a._near_agents) and \
            self.w.tick - a.talk_cd.get(a._near_agents[0].eid, -999) > 240
        f[SOCIAL] = bool(a.recall("agent", a.tx, a.ty)) or bool(a._near_agents)
        return f

    def _decide(self, a: Being):
        x = self._sense(a)
        bias = self._bias(a)
        temperature = 0.5 + 0.9 * a.personality[6] + 0.4 * a.emotions[4]
        act, probs = a.brain.think(
            x, temperature, bias,
            curiosity=a.personality[2],
            caution=a.personality[3],
        )
        f = self._feasible(a)
        if not f[act]:
            order = np.argsort(-probs)
            for cand in order:
                if f[cand]:
                    act = int(cand)
                    break
            else:
                act = REST
        a.habits *= 0.992
        a.habits[act] = min(1.0, a.habits[act] + 0.02)
        self._set_goal(a, act)

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
                e = a._near_agents[0] if act != ATTACK else \
                    max(a._near_agents, key=lambda t: t.health)
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
            m = self._known_or_universal(a, "shelter", tx, ty)
            if m and m[2] < 14 and self.rng.random() < 0.7:
                g["x"], g["y"] = m[0], m[1]
        if self.target_is_blocked(a, act, g["x"], g["y"]):
            a.goal = None
            return
        a.goal = g
        a.goal_t = 0
        a.stuck = 0
        a._last_px, a._last_py = a.x, a.y

    def register_goal_failure(self, a, reason="blocked"):
        goal = a.goal or {}
        key = (goal.get("act"), goal.get("x"), goal.get("y"))
        count, until = a.failed_targets.get(key, (0, 0))
        count += 1
        cooldown = min(1800, 180 * count)
        a.failed_targets[key] = (count, self.w.tick + cooldown)
        a.goal = None
        a.stuck = 0
        a.emotions[3] = min(1.0, a.emotions[3] + 0.04)
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
        return True

    def withdraw_from_storage(self, a, storage, material):
        if a.inv.get(material, 0) >= INV_CAP:
            return False
        moved = storage.withdraw(a.eid, material, min(2, INV_CAP - a.inv.get(material, 0)), self.w.tick)
        if moved <= 0:
            return False
        a.inv[material] = a.inv.get(material, 0) + moved
        return True

    # ------------------------------------------------------------------ agent
    def _agent(self, a: Being):
        w = self.w
        a.age += 1
        a.repro_cd = max(0, a.repro_cd - 1)
        a.atk_t = max(0, a.atk_t - 1)
        a.goal_t += 1
        a.pain = max(0.0, a.pain - 0.0004)

        # VOLONTE : le but persiste (engagement). On ne re-delibere que si :
        # but fini/expiré/bloque, urgence viscerale, ou mollesse (petit cerveau
        # en veille). Un grand cerveau stratege va au bout de sa tache.
        g = a.goal
        expired = g is not None and w.tick > g["until"]
        soft = g is not None and g["act"] in (REST, MARK, SOCIAL, TALK)
        urgent = (a.hunger > 0.85 or a.needs[2] > 0.85 or a.energy < 0.12
                  or a.emotions[0] > 0.7 or a.pain > 0.6)
        if g is None or expired or a.stuck > 20 + 50 * a.personality[8]:
            self._decide(a)
        elif a.goal_t % a.brain.te == 0:
            if urgent and self.rng.random() > 0.25:
                self._decide(a)
            elif soft and a.goal_t > 60 and self.rng.random() > \
                    (0.4 + 0.5 * a.personality[4] - 0.4 * a.personality[6]):
                self._decide(a)
        if a.goal is None:
            a.goal = {"act": REST, "x": a.tx, "y": a.ty, "ref": None,
                      "intensity": 1.0, "until": w.tick + 300}
            a.goal_t = 0

        self._execute(a)
        self._metabolize(a)

        after = self._wellbeing(a)
        delta = after - getattr(a, 'prev_wellbeing', after)
        if abs(delta) > 0.001:
            self._reward(a, 0.08 * delta)
        a.prev_wellbeing = after

        if a.age >= a.natural_death_age:
            self._die(a, cause="vieillesse")
        elif a.health <= 0:
            self._die(a)

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
                if step_x != 0 or step_y != 0:
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
            a.state = "run" if not a.child else "run"
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
            a.emotions[1] = min(1.0, a.emotions[1] + 0.04)
            self._reward(a, 0.12 if w.heat[gy, gx] < 0.15 else 0.03)
            done = True
        elif act == TALK:
            done = self._do_talk(a, ref)
        elif act == SOCIAL:
            done = self._do_social(a, ref)
        elif act == MARK:
            if a.energy > 0.12:
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
        for it in list(w.items):
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
        a.needs[0] = max(0.0, a.needs[0] - nutrition / 110.0)
        a.needs[2] = max(0.0, a.needs[2] - nutrition / 260.0)  # l'eau des aliments
        a.hunger = a.needs[0]
        a.needs[1] = a.energy = min(1.0, a.energy + nutrition / 150.0)
        a.emotions[1] = min(1.0, a.emotions[1] + 0.06)
        a.state = "eat"
        self._reward(a, (before - a.needs[0]) * 2.0)

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
                self.log(f"{a.name} a fabriqué {kind}.", (248, 208, 98), "economie")
                self._reward(a, 0.25)
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
            self.log("Un habitant a trouvé et équipé un outil.", (248, 208, 98), "economie")
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
            self._fx("dust", gx * TILE + 8, gy * TILE + 8)
            self.emit_sound(gx * TILE, gy * TILE, "chop", 0.7)
            a.state = "work"
            self._teach_near(a, 0)
            if w.hp[gy, gx] <= 0:
                self._deplete(gx, gy, asd)
            self._reward(a, 0.12)
            if a.tool >= 0:
                a.tool_durability -= 1
                if a.tool_durability <= 0:
                    self.log(f"L'outil de {a.name} s'est cassé à l'usage.", (218, 138, 58), "economie")
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
            r1 = a.rel.setdefault(e.eid, [0, 0])
            r1[0] = min(1.0, r1[0] + 0.2)
            r2 = e.rel.setdefault(a.eid, [0, 0])
            r2[0] = min(1.0, r2[0] + 0.25)
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
        a.rel.setdefault(e.eid, [0, 0])[0] -= 0.4
        e.rel.setdefault(a.eid, [0, 0])[0] -= 0.45
        e.emotions[2] = min(1.0, e.emotions[2] + 0.4)
        a.belief_beings[e.eid] = max(-1.0, a.belief_beings.get(e.eid, 0) - 0.2)
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
                a.goal = None
            return
        # consequences sociales
        a.rel.setdefault(target.eid, [0, 0])[0] -= 0.3
        target.rel.setdefault(a.eid, [0, 0])[0] -= 0.35
        target.emotions[0] = min(1.0, target.emotions[0] + 0.35)
        target.emotions[2] = min(1.0, target.emotions[2] + 0.45)
        target.pain = min(1.0, target.pain + 0.3)
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
        e = ref if isinstance(ref, Being) and ref.alive else (
            a._near_agents[0] if a._near_agents else None)
        if e is None:
            return True
        self.stats["talks"] += 1
        a.talk_cd[e.eid] = self.w.tick
        self.emit_sound(a.x, a.y, "voice", 0.6)
        a.state = "talk"
        msg = "chat"
        if a.emotions[1] > 0.5:
            msg = "salut"
        elif a.emotions[0] > 0.5:
            msg = "alerte"
        elif a.emotions[2] > 0.5:
            msg = "menace"
        elif a.emotions[7] > 0.38 and a.bonded != e.eid and not e.child and not a.child:
            msg = "cour"
        elif self.rng.random() < 0.15:
            msg = "fait"
        r1 = a.rel.setdefault(e.eid, [0, 0])
        r2 = e.rel.setdefault(a.eid, [0, 0])
        if msg == "salut":
            r1[0] = min(1, r1[0] + 0.08)
            r2[0] = min(1, r2[0] + 0.08)
            e.emotions[1] = min(1, e.emotions[1] + 0.06)
        elif msg == "alerte":
            r2[0] = min(1, r2[0] + 0.1)
            e.emotions[0] = min(1, e.emotions[0] + 0.2)
            e.remember("agent", a.tx, a.ty)
        elif msg == "menace":
            r2[0] = max(-1, r2[0] - 0.15)
            e.emotions[2] = min(1, e.emotions[2] + 0.2)
        elif msg == "cour":
            e.emotions[7] = min(1, e.emotions[7] + 0.15 + 0.2 * a.personality[0])
            r1[1] = min(1, r1[1] + 0.12)
            r2[1] = min(1, r2[1] + 0.12)
            # mariage : M+F obligatoire, pas d'inceste, pas déjà marié
            eligible = (
                a.sex != e.sex
                and not a.married and not e.married
                and not self._are_related(a, e)
                and not a.child and not e.child
                and r1[1] > 0.45 and r2[1] > 0.45
            )
            if eligible:
                a.bonded, e.bonded = e.eid, a.eid
                a.married, e.married = True, True
                a.partner_id, e.partner_id = e.eid, a.eid
                a.life.append(("mariage", e.name))
                e.life.append(("mariage", a.name))
                self.log(f"{a.name} et {e.name} se sont mariés.",
                         (248, 178, 218), "social")
        elif msg == "fait":
            for cat in ("food", "water", "wood"):
                memory = a.recall(cat, a.tx, a.ty)
                if memory is not None:
                    self.send_fact(a, e, cat, memory[0], memory[1])
                    break
        else:
            r1[0] = min(1, r1[0] + 0.03)
            r2[0] = min(1, r2[0] + 0.03)
            if e.child and a.skills[0] > e.skills[0]:
                e.skills[0] = min(1.0, e.skills[0] + 0.05)   # enseignement oral
        a.skills[3] = min(1.0, a.skills[3] + 0.01)
        self._reward(a, 0.1)
        return True

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
            return True
        return False

    def _teach_near(self, a, skill_idx):
        """Transmission culturelle : un enfant qui regarde apprend."""
        for e in self._near(a.x, a.y, lambda e: isinstance(e, Being) and e.child, r=2):
            if e.trust(a.eid) > -0.2:
                e.skills[skill_idx] = min(1.0, e.skills[skill_idx]
                                          + 0.02 * (1 + a.skills[skill_idx]))

    # ------------------------------------------------------------------ construction
    def _do_build(self, a, tx, ty):
        w, am = self.w, self.am

        # ── repli brique-par-brique si ressources insuffisantes ──
        if (a.inv.get("bois", 0) < 3 or a.inv.get("pierre", 0) < 1) \
                and a.inv.get("graine", 0) == 0:
            if a.inv.get("bois", 0) > 0 or a.inv.get("pierre", 0) > 0:
                return self.do_build_block(a, tx, ty)

        # ── agriculture : si l'être porte des graines et que la case est vide ──
        if a.inv.get("graine", 0) > 0 and w.land[ty, tx] and w.content_at(tx, ty) < 0 \
                and not w.water[ty, tx] and (tx, ty) not in w.crop_plots:
            from .world import CropPlot
            plot = CropPlot(tx=tx, ty=ty, owner_eid=a.eid, planted_tick=w.tick)
            w.crop_plots[(tx, ty)] = plot
            a.inv["graine"] = max(0, a.inv["graine"] - 1)
            self._reward(a, 0.12)
            self.log(f"{a.name} a plante une graine.", (108, 188, 98), "economie")
            return True

        # ── construction brique par brique ──
        return self.do_build_block(a, tx, ty)
        if a.home is None:
            a.home = (tx, ty)
            a.life.append("première maison")
        self._fx("dust", tx * TILE + 8, ty * TILE + 8)
        self._check_village(tx, ty)
        self._teach_near(a, 1)
        self._reward(a, 0.35)
        return True

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
        self.log(f"{a.name} a commence le plan d'une maison.", (178, 228, 168), "batiment")
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
        if w.content_at(task.tx, task.ty) >= 0:
            return False
        role = self.role_for_block_task(task)
        pool = self.am.pool(role)
        if not pool:
            return False
        aid = int(self.am.pick(pool, self.rng))
        w.place(task.tx, task.ty, aid, self.am, hp=6,
                solid=task.solid, shelter=False, size=1)
        a.inv[task.material] -= 1
        site.mark_placed(a.eid, task)
        a.skills[1] = min(1.0, a.skills[1] + 0.012)
        self.stats["builds"] += 1
        self._fx("dust", task.tx * TILE + TILE / 2, task.ty * TILE + TILE / 2)
        self._reward(a, 0.10)
        if site.complete():
            self.complete_site(site, a)
        return True

    def complete_site(self, site, finisher):
        w = self.w
        for ty in range(site.origin_ty + 1, site.origin_ty + 4):
            for tx in range(site.origin_tx + 1, site.origin_tx + 4):
                if 0 <= tx < w.g and 0 <= ty < w.g:
                    w.shelter[ty, tx] = 1
        storage_tx = site.origin_tx + 2
        storage_ty = site.origin_ty + 2
        if (storage_tx, storage_ty) not in w.storages:
            self.create_storage(finisher, storage_tx, storage_ty, capacity=80)
            self.log(f"Depot cree au centre de la maison.", (178, 228, 168), "batiment")
        w.remove_site(site)
        self._check_village(site.origin_tx + 2, site.origin_ty + 2)
        for eid in site.contributors:
            c = next((x for x in self.agents if x.eid == eid), None)
            if c and c.alive:
                c.skills[1] = min(1.0, c.skills[1] + 0.04)
                c.needs[6] = max(0.0, c.needs[6] - 0.12)
                self._reward(c, 0.25)
        self.log(f"Maison terminee : {len(site.contributors)} contributeur(s).",
                 (108, 208, 128), "batiment")

    def do_build_block(self, a, tx, ty):
        """BUILD : contribuer a un chantier existant ou placer un bloc."""
        site = self.nearest_site(a.tx, a.ty, max_dist=14)
        if site is not None:
            task = site.next_task_for(a.inv)
            if task is not None:
                return self.place_site_block(a, site, task)
        site = self.create_house_site(a)
        if site is not None:
            task = site.next_task_for(a.inv)
            if task is not None:
                return self.place_site_block(a, site, task)
            return True
        w, am = self.w, self.am
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
            self.log(f"Un village est né en ({tx},{ty}) — {shelters} abris !", (108, 208, 128), "batiment")

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
    def _die(self, a: Being, cause: str | None = None):
        if not a.alive:
            return
        a.alive = False
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
                 f"gén {a.gen}, {a.brain.n} neurones.", (228, 98, 98), "mort")
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

    # ------------------------------------------------------------------ reproduction
    def _reproduce(self, a: Being):
        if len(self.agents) >= MAX_POP or a.energy < 0.55 or a.repro_cd > 0 \
           or a.child or a.age > AGE_ELDER_TICKS:
            return
        #必须 marié pour avoir un enfant
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
        a.repro_cd = mate.repro_cd = 2600
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
        self.stats["births"] += 1
        if self.stats["births"] % 3 == 1:
            self.log(f"{a.name} et {mate.name} ont un enfant : {child.name} "
                     f"(cerveau {n} neurones).", (78, 168, 232), "vie")
        self.lab.event(self.w.tick, "birth", eid=child.eid, parent1=a.eid, parent2=mate.eid,
                       name=child.name, brain_size=n)

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
            for dx in range(-6, 7):
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

        homes = [a.home for a in alive if a.home]
        if len(homes) >= 6:
            self.society.append(f"Foyers : {len(set(homes))}")
        bonded = sum(1 for a in alive if a.bonded) // 2
        if bonded:
            self.society.append(f"Couples liés : {bonded}")

    # ------------------------------------------------------------------ moutons
    def export_academy_model(self, name="champion"):
        return self.academy.export_model(
            f"data/models/{name}", self.universal_knowledge, label=name
        )

    def import_academy_model(self, name="champion"):
        data = self.academy.import_model(f"data/models/{name}")
        if data is not None:
            self.universal_knowledge = UniversalKnowledge.from_dict(data)

    def _sheep(self, s: Sheep):
        w = self.w
        s.energy -= 0.00022
        near = [a for a in self._near(s.x, s.y, lambda e: isinstance(e, Being), r=2)]
        x = self._sens
        x[:] = 0.0
        x[0] = s.energy
        if near:
            t = min(near, key=lambda e: (e.x - s.x) ** 2 + (e.y - s.y) ** 2)
            ang = math.atan2(s.y - t.y, s.x - t.x)
            x[73] = 1.0
            x[74] = math.cos(ang)
            x[75] = math.sin(ang)
        o = s.brain.think(x)[1]
        if o[2] > 0.12 or not near:
            s.energy += 0.0016
            s.state = "grass" if o[2] > 0.2 else "idle"
        mvx, mvy = o[0] - 1.0 / 15.0, o[1] - 1.0 / 15.0
        sp = 0.75
        self._move(s, mvx * sp, mvy * sp, sheep=True)
        s.anim_t += 1
        if s.anim_t % 7 == 0:
            s.frame += 1
        if s.energy <= 0:
            s.health -= 0.002
        if s.health <= 0:
            self._kill_sheep(s)
        if s.energy > 0.95 and len(self.sheep) < MAX_SHEEP:
            s.energy = 0.55
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
                m.state = "attack" if hasattr(m, "state") else "idle"
            elif dist > 0:
                mvx = dx / dist
                mvy = dy / dist
                self._move(m, mvx * 0.6, mvy * 0.6, sheep=True)
        else:
            mvx = self.rng.uniform(-1, 1)
            mvy = self.rng.uniform(-1, 1)
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
    def tick(self):
        self.step()
        for a in list(self.agents):
            if a.alive:
                self._reproduce(a)
        if any(not a.alive for a in self.agents):
            self.agents = [a for a in self.agents if a.alive]

    def natural_pop(self):
        return len(self.agents), len(self.sheep), len(self.w.items)
