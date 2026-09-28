"""WorldGrid : carte 312x312 tuiles de 16px (~5000x5000 px), contenu, blocage,
abris, pv de ressource, pheromones, decors, elements laches."""
import os
from dataclasses import dataclass
import numpy as np

from .config import GRID, TILE, ROOT

MODS_FILE = os.path.join(ROOT, "map", "terrain_mods.npy")


class World:
    def __init__(self):
        g = GRID
        self.g = g
        self.floor = np.full((g, g), -1, dtype=np.int16)   # sheet*216+cell
        self.content = np.full((g, g), -1, dtype=np.int16)  # asset id (anchor)
        self.owner = np.full((g, g), -1, dtype=np.int32)   # flat anchor index for footprint
        self.blocked = np.zeros((g, g), dtype=np.uint8)
        self.shelter = np.zeros((g, g), dtype=np.uint8)
        self.hp = np.zeros((g, g), dtype=np.int16)
        self.marker = np.zeros((g, g), dtype=np.float32)   # pheromones
        self.marker_col = np.zeros((g, g), dtype=np.uint8)
        self.regrow = np.zeros((g, g), dtype=np.float32)   # stump regrow timer
        self.items = []      # Item
        self.dirty_chunks = set()
        #: Compteur global de modifications terrain : toute cle de cache
        #: de chunks l'inclut, ainsi aucun cache ne peut survivre a un
        #: coup de pinceau ou a une construction.
        self.mods_version = 0
        self.tick = 0
        self.land = np.ones((g, g), dtype=np.uint8)   # masque continents (map.png)
        self.water = np.zeros((g, g), dtype=np.uint8)
        self.fire = np.zeros((g, g), dtype=np.int16)   # ticks de flamme restants
        self._burning_cells = set()  # (y, x) tuples of cells with fire > 0
        self.smell = np.zeros((g, g), dtype=np.float32)  # champ d'odeurs (feu, nourriture, mort)
        self.heat = np.zeros((g, g), dtype=np.float32)   # traces de présence (exploration)
        self.cemetery = []  # list of (tx, ty, name, death_tick, color_rgb)
        self.storages = {}  # (tx, ty) -> Storage
        self.sites = {}     # (tx, ty) -> BuildingSite
        self.crop_plots = {}  # (tx, ty) -> CropPlot
        self.mountains = np.zeros((g, g), dtype=np.uint8)  # terrain montagnes ( jamais modifie)
        self.foundation = np.full((g, g), -1, dtype=np.int16)
        self.roof = np.full((g, g), -1, dtype=np.int16)
        # index de connaissance : ou est chaque categorie de ressource
        self.kidx = {k: {} for k in ("food", "wood", "stone", "gold", "tool", "shelter")}
        self._kcell = 8
        # Sites de ressources persistants (Phase 3)
        self.resource_sites: dict[int, "ResourceSite"] = {}
        self.sites_by_region: dict[tuple[int, int], list[int]] = {}
        self.next_resource_site_id: int = 1
        self.gen = None  # WorldGen instance (worldgen.py)
        self.rng_fire = np.random.default_rng(11)
        self._rng_regrow = np.random.default_rng(42)

    def set_land(self, mask):
        self.mods_version += 1
        self.land = mask.astype(np.uint8)
        self.water = (1 - self.land).astype(np.uint8)

    # ------------------------------------------------------------------ persistence
    def save_mods(self, path=None):
        """Sauvegarde les modifications terrain (land + water) dans un .npy."""
        path = path or MODS_FILE
        os.makedirs(os.path.dirname(path), exist_ok=True)
        np.savez_compressed(path, land=self.land, water=self.water)

    def load_mods(self, path=None):
        """Charge les modifications terrain si le fichier existe et taille compatible."""
        path = path or MODS_FILE
        if not os.path.exists(path):
            return False
        try:
            data = np.load(path)
            l = data["land"]
            if l.shape[0] != self.g or l.shape[1] != self.g:
                os.remove(path)
                return False
            self.land = l.astype(np.uint8)
            self.water = data["water"].astype(np.uint8)
            return True
        except Exception:
            return False

    def is_land(self, tx, ty):
        return bool(self.land[ty, tx]) if self.inb(tx, ty) else False

    def near_water(self, tx, ty):
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                x, y = tx + dx, ty + dy
                if self.inb(x, y) and self.water[y, x]:
                    return True
        return False

    def ignite(self, tx, ty, ticks=220):
        if self.inb(tx, ty) and not self.water[ty, tx]:
            if self.fire[ty, tx] == 0:
                self._burning_cells.add((ty, tx))
            self.fire[ty, tx] = max(self.fire[ty, tx], ticks)
            self.mark_dirty(tx, ty)

    def step_fire(self, am, wind=(0.0, 0.0), rain=0.0, flammable=None,
                  spread=1.0):
        """Feu = systeme physique : temperature, combustible, vent, eau.
        Il ne sait pas ce qu'est une maison — il sait seulement bruler."""
        if not self._burning_cells:
            return 0
        spread_chance = min(0.9, 0.16 * max(0.0, float(spread)))
        wind_x = int(wind[0] * 2)
        wind_y = int(wind[1] * 2)
        rain_decay = 1 + int(rain * 6)
        new_burning = set()
        for y, x in self._burning_cells:
            self.fire[y, x] -= rain_decay
            if self.fire[y, x] <= 0:
                self.fire[y, x] = 0
                if self.content[y, x] >= 0 and flammable and int(self.content[y, x]) in flammable:
                    self.burn_out(am, y, x)
                continue
            self.smell[y, x] = min(1.0, self.smell[y, x] + 0.08)
            if self.fire[y, x] % 4 == 0:
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        nx, ny = x + dx + wind_x, y + dy + wind_y
                        if not self.inb(nx, ny) or self.water[ny, nx] or self.fire[ny, nx]:
                            continue
                        naid = self.content_at(nx, ny)
                        if flammable and naid >= 0 \
                           and naid in flammable \
                           and self.rng_fire.random() < spread_chance:
                            self.fire[ny, nx] = 200
                            new_burning.add((ny, nx))
            new_burning.add((y, x))
        self._burning_cells = new_burning
        return len(self._burning_cells)

    def _kadd(self, cat, x, y):
        cell = (x // self._kcell, y // self._kcell)
        self.kidx[cat].setdefault(cell, set()).add((x, y))

    def _kdel(self, cat, x, y):
        cell = (x // self._kcell, y // self._kcell)
        s = self.kidx[cat].get(cell)
        if s:
            s.discard((x, y))
            if not s:
                del self.kidx[cat][cell]

    def knearest(self, cat, tx, ty, maxr=40):
        """Position connue la plus proche d'une categorie (le savoir du monde)."""
        best, bd = None, 1e9
        c = self._kcell
        cx, cy = tx // c, ty // c
        r = 0
        while (cx - r) * c <= tx + maxr and (cy - r) * c <= ty + maxr:
            found_ring = False
            for j in range(cy - r, cy + r + 1):
                for i in range(cx - r, cx + r + 1):
                    if max(abs(i - cx), abs(j - cy)) != r:
                        continue
                    for (x, y) in self.kidx[cat].get((i, j), ()):
                        d = max(abs(x - tx), abs(y - ty))
                        if d < bd and d <= maxr:
                            best, bd = (x, y), d
                            found_ring = True
            if found_ring and bd <= r * c:
                break
            r += 1
            if r > 6:
                break
        return best, (bd if best else -1)

    # ------------------------------------------------------------------ utils
    def inb(self, x, y):
        return 0 <= x < self.g and 0 <= y < self.g

    @staticmethod
    def px2t(v):
        return int(v // TILE)

    def content_at(self, x, y):
        g = self.g
        if x < 0 or y < 0 or x >= g or y >= g:
            return -1
        flat = self.owner[y, x]
        if flat < 0:
            return -1
        ay = flat // g
        ax = flat - ay * g
        return int(self.content[ay, ax])

    def anchor_of(self, x, y):
        g = self.g
        if x < 0 or y < 0 or x >= g or y >= g:
            return -1
        flat = self.owner[y, x]
        if flat < 0:
            return -1
        ay = flat // g
        ax = flat - ay * g
        return int(self.content[ay, ax])

    def mark_dirty(self, tx, ty, r=2):
        self.mods_version += 1
        cx, cy = tx // TILE, ty // TILE
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                self.dirty_chunks.add((cx + dx, cy + dy))

    # ------------------------------------------------------------------ placement
    def place(self, tx, ty, aid, am, hp=1, solid=False, shelter=False, size=1):
        """Met un asset ancre (tx,ty) en occupant une empreinte size x size centree bas."""
        tx = min(max(tx, 0), self.g - size)
        ty = min(max(ty, 0), self.g - size)
        self.remove(tx, ty, quiet=True)
        flat = ty * self.g + tx
        self.content[ty, tx] = aid
        self.hp[ty, tx] = hp
        for j in range(size):
            for i in range(size):
                x, y = tx + i, ty + j
                if self.inb(x, y):
                    self.owner[y, x] = flat
                    if solid:
                        self.blocked[y, x] = 1
                    if shelter:
                        self.shelter[y, x] = 1
        self._kindex_set(tx, ty, am.assets[aid])
        self.mark_dirty(tx, ty, size + 1)

    def _kindex_set(self, tx, ty, asd):
        for cat in list(self.kidx):
            self._kdel(cat, tx, ty)
        if asd.edible > 0:
            self._kadd("food", tx, ty)
        elif asd.harvest:
            m = asd.harvest["material"]
            self._kadd({"bois": "wood", "pierre": "stone", "or": "gold"}.get(m, "wood"), tx, ty)
        elif asd.tool:
            self._kadd("tool", tx, ty)
        if asd.shelter:
            self._kadd("shelter", tx, ty)

    def _kindex_clear(self, tx, ty):
        for cat in self.kidx:
            self._kdel(cat, tx, ty)

    def remove(self, tx, ty, quiet=False):
        tx = min(max(tx, 0), self.g - 1)
        ty = min(max(ty, 0), self.g - 1)
        flat = self.owner[ty, tx]
        if flat < 0:
            return False
        ax, ay = flat % self.g, flat // self.g
        aid = int(self.content[ay, ax])
        # efface toute la zone de l'ancre (jusqu'à 6×6, couvrant tous les assets)
        size = 1
        for j in range(6):
            for i in range(6):
                x, y = ax + i, ay + j
                if self.inb(x, y) and self.owner[y, x] == flat:
                    self.owner[y, x] = -1
                    self.blocked[y, x] = 0
                    self.shelter[y, x] = 0
                    size = max(size, i + 1, j + 1)
        self.content[ay, ax] = -1
        self.hp[ay, ax] = 0
        self.regrow[ay, ax] = 0.0
        self._kindex_clear(ax, ay)
        if not quiet:
            self.mark_dirty(ax, ay, size + 1)
        return True

    def set_floor(self, tx, ty, tile_id):
        if self.inb(tx, ty):
            self.floor[ty, tx] = tile_id
            self.mark_dirty(tx, ty)

    # ------------------------------------------------------------------ items
    def drop_item(self, item):
        self.items.append(item)

    def take_items_at(self, tx, ty, radius_px=10):
        out = []
        cx, cy = tx * TILE + TILE / 2, ty * TILE + TILE / 2
        keep = []
        for it in self.items:
            if (it.x - cx) ** 2 + (it.y - cy) ** 2 <= radius_px * radius_px:
                out.append(it)
            else:
                keep.append(it)
        self.items = keep
        return out

    # ------------------------------------------------------------------ per tick
    def step(self, am, clock=None):
        self.tick += 1
        perf = self._get_perf(am)

        with perf.measure("world_items"):
            self._step_items()

        if self.tick % 3 == 0:
            with perf.measure("world_markers"):
                self._step_markers()
            with perf.measure("world_smell"):
                self._step_smell()
            with perf.measure("world_heat"):
                self._step_heat()

        if self.tick % 30 == 0:
            with perf.measure("world_regrowth"):
                self._step_regrowth(am, clock)

        with perf.measure("world_fire"):
            self._step_fire(am, clock)

    def _get_perf(self, am):
        """Get PerfMetrics from simulation or asset manager."""
        try:
            if hasattr(am, 'sim') and hasattr(am.sim, 'perf'):
                return am.sim.perf
        except Exception:
            pass
        try:
            from game.perfmetrics import PerfMetrics
            return PerfMetrics._global_instance if hasattr(PerfMetrics, '_global_instance') else PerfMetrics()
        except Exception:
            pass
        return PerfMetrics()

    def _step_items(self):
        if self.tick % 30 == 0:
            self.items = [item for item in self.items
                          if item.life > 0 and (item.kind != "food" or self.tick < item.spoil_tick)]

    def _step_markers(self):
        self.marker *= 0.992
        self.marker[self.marker < 0.01] = 0

    def _step_smell(self):
        self.smell *= 0.985
        self.smell[self.smell < 0.01] = 0

    def _step_heat(self):
        self.heat *= 0.996

    def _step_regrowth(self, am, clock):
        slow = 1.0 if clock is None else clock.growth_f
        trees = am.pool("tree")
        if trees:
            mask = self.regrow > 0
            if mask.any():
                self.regrow[mask] -= 3 * slow
                ripe = mask & (self.regrow <= 0)
                for y, x in zip(*np.nonzero(ripe)):
                    if self.is_land(x, y) and not self.blocked[y, x] and self.content_at(x, y) < 0:
                        aid = int(am.pick(trees, self._rng_regrow))
                        self.place(int(x), int(y), aid, am, hp=6, solid=True,
                                   size=am.assets[aid].size_tiles)
                        self.regrow[y, x] = 0
                    else:
                        self.regrow[y, x] = 100.0

    def _step_fire(self, am, clock):
        if not self._burning_cells:
            return 0
        spread_chance = min(0.9, 0.16 * max(0.0, 1.0))
        wind_x = 0
        wind_y = 0
        rain = 0.0
        if clock is not None:
            wind_x = int(clock.wind[0] * 2)
            wind_y = int(clock.wind[1] * 2)
            rain = clock.rain
        spread_chance = min(0.9, 0.16 * max(0.0, float(1.0)))
        rain_decay = 1 + int(rain * 6)
        new_burning = set()
        for y, x in self._burning_cells:
            self.fire[y, x] -= rain_decay
            if self.fire[y, x] <= 0:
                self.fire[y, x] = 0
                if self.content[y, x] >= 0 and hasattr(am, 'flammable') and am.flammable and int(self.content[y, x]) in am.flammable:
                    self.burn_out(am, y, x)
                continue
            self.smell[y, x] = min(1.0, self.smell[y, x] + 0.08)
            if self.fire[y, x] % 4 == 0:
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        nx, ny = x + dx + wind_x, y + dy + wind_y
                        if not self.inb(nx, ny) or self.water[ny, nx] or self.fire[ny, nx]:
                            continue
                        naid = self.content_at(nx, ny)
                        if hasattr(am, 'flammable') and am.flammable and naid >= 0 \
                           and naid in am.flammable \
                           and self.rng_fire.random() < spread_chance:
                            self.fire[ny, nx] = 200
                            new_burning.add((ny, nx))
            new_burning.add((y, x))
        self._burning_cells = new_burning
        return len(self._burning_cells)

    def find_cemetery_spot(self, rng=None):
        """Retourne une parcelle libre de cimetière dans le tiers supérieur."""
        if rng is None:
            import numpy as np
            rng = np.random.default_rng(42)

        g = self.g
        cx = g // 2
        cy = max(10, g // 10)
        occupied = {(int(tx), int(ty)) for tx, ty, *_ in self.cemetery}

        for radius in range(0, g // 3, 8):
            xmin = max(3, cx - radius)
            xmax = min(g - 9, cx + radius + 1)
            ymin = max(3, cy - radius)
            ymax = min(g - 9, cy + radius + 1)
            if xmin >= xmax or ymin >= ymax:
                continue

            for _ in range(48):
                tx = int(rng.integers(xmin, xmax))
                ty = int(rng.integers(ymin, ymax))

                if any(abs(tx - gx) < 2 and abs(ty - gy) < 2 for gx, gy in occupied):
                    continue
                if not self.is_land(tx, ty):
                    continue
                if self.blocked[ty, tx] or self.content_at(tx, ty) >= 0:
                    continue
                return tx, ty

        return max(3, cx - 3), max(8, cy)

    def bury(self, tx, ty, name, death_tick, color_rgb):
        """Enterre un habitant : enregistre la tombe (pas de bloc posé)."""
        self.cemetery.append((tx, ty, name, death_tick, color_rgb))

    def site_at(self, tx, ty):
        for site in self.sites.values():
            for task in site.tasks:
                if task.tx == tx and task.ty == ty:
                    return site
        return None

    def add_site(self, site):
        self.sites[site.key] = site

    def remove_site(self, site):
        self.sites.pop(site.key, None)

    def save_mountains(self):
        """Sauvegarde le masque de montagnes (terrain) apres worldgen."""
        self.mountains = self.blocked.copy()

    def reset_content(self):
        """Reinitialise tout le contenu place (objets, ressources, batiments)
        mais garde le terrain (land, water, mountains)."""
        g = self.g
        self.content[:] = -1
        self.owner[:] = -1
        self.blocked[:] = self.mountains.copy()
        self.shelter[:] = 0
        self.hp[:] = 0
        self.marker[:] = 0
        self.marker_col[:] = 0
        self.regrow[:] = 0
        self.fire[:] = 0
        self._burning_cells.clear()
        self.smell[:] = 0
        self.heat[:] = 0
        self.floor[:] = -1
        self.foundation[:] = -1
        self.roof[:] = -1
        self.items.clear()
        self.cemetery.clear()
        self.storages.clear()
        self.sites.clear()
        self.crop_plots.clear()
        self.kidx = {k: {} for k in ("food", "wood", "stone", "gold", "tool", "shelter")}
        self.dirty_chunks.clear()

    def burn_out(self, am, y, x):
        """Le feu a fini de bruler la tuile : ce qu'elle contenait est detruit."""
        aid = self.content_at(x, y)
        if aid >= 0:
            self.remove(x, y)
            self.regrow[y, x] = 5200          # la terre brulee repoussera, plus tard


class Item:
    __slots__ = ("kind", "aid", "x", "y", "material", "nutrition", "life",
                 "created_tick", "spoil_tick")

    def __init__(self, kind, aid, x, y, material="", nutrition=0.0, life=1e9):
        self.kind = kind          # 'mat' | 'food'
        self.aid = aid
        self.x, self.y = x, y
        self.material = material
        self.nutrition = nutrition
        self.life = life
        self.created_tick = 0
        self.spoil_tick = 0


@dataclass
class CropPlot:
    tx: int
    ty: int
    owner_eid: int | None
    planted_tick: int
    growth: float = 0.0
    water_need: float = 0.5
    crop_type: str = "grain"
    watered: bool = False
