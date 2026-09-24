"""Engine backend — logique pure, aucune dépendance pygame.

Extrait de main.py pour que le web (Flask-SocketIO) puisse lancer la
simulation sans importer pygame.

Corrections et améliorations par rapport à la v1
------------------------------------------------
1. BUG MAJEUR : `populate()` n'était JAMAIS appelé par `build_world()`.
   Le monde procédural naissait vide — aucun arbre, aucune nourriture,
   donc aucune famine possible, donc aucune pression de sélection.
2. BUG : `place_random(trees, …, hp=am.assets[am.pick(trees)].harvest["hp"])`
   tirait un arbre pour calculer les PV et un AUTRE arbre à l'intérieur de
   `place_random` — les PV ne correspondaient pas à l'asset posé. Le tirage
   est maintenant fait une seule fois, et les PV dérivent de l'asset réel.
3. Le décor est désormais pondéré par le BIOME et la PENTE issus de
   worldgen : forêts denses en zone humide, carrières près des montagnes,
   fruits en prairie, rien sur les pentes raides. Le monde a l'air
   « conçu à la main » alors qu'il est entièrement procédural.
4. `blob` respecte `w.blocked` et `w.water`, et son échantillonnage est
   vectorisé au lieu d'une boucle de rejet Python.
5. `build_world()` accepte `populate_dense` et `n_agents` : on peut
   désormais obtenir un monde peuplé et prêt à tourner en un seul appel.
6. Journal de départ enrichi (répartition réelle des biomes) et graine
   propagée partout — deux appels avec la même graine donnent le même monde.
"""
from __future__ import annotations

import numpy as np

from game.config import GRID, TILE
from game.world import World
from game.simulation import Sim


# ══════════════════════════════════════════════════════════════════════
#  Terrain
# ══════════════════════════════════════════════════════════════════════
#: Proportions visées par défaut — 92 % de terre émergée, 8 % d'eau.
#: `mountain_frac` fait partie de la terre : elle est simplement infranchissable.
WATER_FRAC    = 0.08
MOUNTAIN_FRAC = 0.14

#: Superficie du monde, en pixels de rendu. GRID est fixé dans game/config.py ;
#: cette constante sert aux messages et aux conversions px <-> tuiles.
WORLD_PX = GRID * TILE

#: Espacement des chaînes de montagnes, en pixels.
RIDGE_SPACING_PX = 4000


def world_pixels():
    """Côté du monde en pixels de rendu (GRID tuiles x TILE px)."""
    return GRID * TILE


def compute_land(seed=None, *, tile_period=None, ridge_width=None,
                 water_frac=WATER_FRAC, mountain_frac=MOUNTAIN_FRAC):
    """Génère le terrain procédural via worldgen. None → monde plat classique.

    `tile_period` et `ridge_width` sont exprimés en TUILES ; laissés à None,
    ils sont dérivés de RIDGE_SPACING_PX pour que l'espacement reste constant
    en pixels quelle que soit la taille de GRID.
    """
    if seed is None:
        return None
    from game import worldgen
    if tile_period is None:
        tile_period = worldgen.period_for_pixels(RIDGE_SPACING_PX, TILE)
    if ridge_width is None:
        ridge_width = max(8, int(tile_period * 0.22))
    return worldgen.generate(grid_size=GRID, tile_period=tile_period,
                             ridge_width=ridge_width, seed=int(seed),
                             water_frac=water_frac,
                             mountain_frac=mountain_frac)


# ══════════════════════════════════════════════════════════════════════
#  Outils de placement
# ══════════════════════════════════════════════════════════════════════
def _free(w, x, y):
    """La case accepte-t-elle un nouvel objet ?"""
    return (0 < x < GRID - 1 and 0 < y < GRID - 1
            and w.land[y, x] and not w.blocked[y, x]
            and w.content_at(x, y) < 0)


def blob(w, am, rng, cx, cy, radius, fn, density=2.0):
    """Applique `fn(x, y)` sur un nuage gaussien de cases libres.

    Vectorisé : un seul tirage numpy au lieu d'une boucle de rejet.
    """
    n = max(4, int(radius * radius * density))
    xs = np.clip(np.round(rng.normal(cx, radius / 2.0, n)), 1, GRID - 2).astype(int)
    ys = np.clip(np.round(rng.normal(cy, radius / 2.0, n)), 1, GRID - 2).astype(int)
    for x, y in zip(xs, ys):
        if _free(w, int(x), int(y)):
            fn(int(x), int(y))


def _biome_sites(w, rng, n, biomes, *, max_slope=None, margin=20):
    """Tire `n` centres au hasard parmi les tuiles appartenant à `biomes`.

    Sans heightmap, retombe sur un tirage uniforme. C'est ce qui donne aux
    forêts, carrières et vergers leur placement « logique » sans qu'aucune
    règle ne soit écrite à la main.
    """
    gen = getattr(w, "gen", None)
    if gen is None:
        return [(int(rng.integers(margin, GRID - margin)),
                 int(rng.integers(margin, GRID - margin))) for _ in range(n)]

    from game import worldgen as wg
    mask = np.isin(gen.biome, list(biomes))
    mask[:margin, :] = mask[-margin:, :] = False
    mask[:, :margin] = mask[:, -margin:] = False
    if max_slope is not None:
        mask &= wg.slope(gen) <= max_slope
    ys, xs = np.nonzero(mask)
    if not len(xs):
        return [(int(rng.integers(margin, GRID - margin)),
                 int(rng.integers(margin, GRID - margin))) for _ in range(n)]
    idx = rng.integers(0, len(xs), n)
    return [(int(xs[i]), int(ys[i])) for i in idx]


def populate(w, am, rng, dense=True):
    """Installe le décor naturel : forêts, carrières, sources, fruits sauvages,
    outils oubliés, ruines. Aucun ordre imposé — seulement des probabilités
    pondérées par le biome."""
    trees  = am.pool("tree")
    stones = am.pool("stone_res")
    golds  = am.pool("gold_stone")
    bushes = am.pool("bush")
    rocks  = am.pool("decor") + am.pool("waterrock")
    tools  = am.pool("tool")
    foods  = am.pool("food")
    meats  = am.pool("meat_res")
    if not trees:
        return

    from game import worldgen as wg
    gen = getattr(w, "gen", None)

    def place(pool, x, y, hp=1, solid=False, size=None):
        """Pose UN asset tiré du pool. Le tirage sert aussi aux PV : c'est la
        correction du bug de la v1, où l'asset posé et l'asset mesuré
        différaient."""
        if not pool or not _free(w, x, y):
            return
        aid = int(am.pick(pool, rng))
        a = am.assets[aid]
        if hp == "harvest":
            hp = int(a.harvest.get("hp", 1)) if getattr(a, "harvest", None) else 1
        s = size if size is not None else (a.size_tiles if a.solid else 1)
        w.place(x, y, aid, am, hp=hp, solid=solid, shelter=a.shelter, size=s)

    B = wg  # raccourci de lisibilité

    # ── forêts : là où l'humidité fait déjà pousser la forêt ──────────
    for cx, cy in _biome_sites(w, rng, 26 if dense else 6,
                               (B.BIOME_FOREST, B.BIOME_GRASS), max_slope=0.9):
        blob(w, am, rng, cx, cy, 11,
             lambda x, y: place(trees, x, y, hp="harvest", solid=True))

    # ── carrières : au pied des montagnes ─────────────────────────────
    for cx, cy in _biome_sites(w, rng, 9 if dense else 2,
                               (B.BIOME_ROCK, B.BIOME_GRASS)):
        blob(w, am, rng, cx, cy, 6,
             lambda x, y: place(stones, x, y, hp=5, solid=True))

    # ── filons d'or : plus haut, plus rares ───────────────────────────
    for cx, cy in _biome_sites(w, rng, 5 if dense else 1,
                               (B.BIOME_ROCK, B.BIOME_SNOW), margin=30):
        blob(w, am, rng, cx, cy, 4,
             lambda x, y: place(golds, x, y, hp=5, solid=True))

    # ── broussailles et rochers, partout ──────────────────────────────
    for _ in range(1200 if dense else 150):
        x, y = int(rng.integers(4, GRID - 4)), int(rng.integers(4, GRID - 4))
        place(bushes + rocks, x, y)

    # ── fruits sauvages : prairies et lisières ────────────────────────
    for x, y in _biome_sites(w, rng, 2500 if dense else 250,
                             (B.BIOME_GRASS, B.BIOME_FOREST, B.BIOME_MARSH),
                             margin=4):
        place(foods, x, y, hp=1)

    # ── carcasses ─────────────────────────────────────────────────────
    for _ in range(34 if dense else 5):
        x, y = int(rng.integers(8, GRID - 8)), int(rng.integers(8, GRID - 8))
        place(meats, x, y, hp=1)

    # ── outils oubliés ────────────────────────────────────────────────
    for _ in range(10 if dense else 2):
        x, y = int(rng.integers(6, GRID - 6)), int(rng.integers(6, GRID - 6))
        place(tools, x, y)

    _paint_floors(w, am, rng, dense)


def _paint_floors(w, am, rng, dense):
    """Clairières herbeuses et mares — peinture de sol, pas des objets."""
    if not am.floors:
        return
    n_sheets = len(am.floors)

    def paint(x, y):
        sheet = 0 if rng.random() < 0.9 else min(1, n_sheets - 1)
        cells = am.tile_cells(am.floors[sheet]) or 1
        w.set_floor(x, y, sheet * 216 + int(rng.integers(cells)))

    for cx, cy in _biome_sites(w, rng, 7 if dense else 2,
                               (3, 4), max_slope=0.8):   # prairie / forêt
        blob(w, am, rng, cx, cy, 9, paint)

    water_sheet = next((i for i, f in enumerate(am.floors)
                        if "water background" in am.assets[f].name.lower()), 5)
    water_sheet = min(water_sheet, n_sheets - 1)

    def paint_water(x, y):
        cells = am.tile_cells(am.floors[water_sheet]) or 1
        w.set_floor(x, y, water_sheet * 216 + int(rng.integers(cells)))

    cx, cy = (int(rng.integers(30, GRID - 30)), int(rng.integers(30, GRID - 30)))
    blob(w, am, rng, cx, cy, 5, paint_water)


# ══════════════════════════════════════════════════════════════════════
#  Construction du monde
# ══════════════════════════════════════════════════════════════════════
def seed_life(w, sim, rng, *, n_agents=60, n_sheep=40, n_monsters=0):
    """Peuple un monde déjà construit : habitants, moutons, prédateurs.

    Séparé de `build_world` pour que `main_qt.py` et les outils hors écran
    partagent exactement le même chemin d'apparition.
    """
    for _ in range(max(0, int(n_agents))):
        x, y = _spawn_spot(w, rng)
        sim.spawn_agent(x=x * TILE + TILE / 2, y=y * TILE + TILE / 2, parents=None)
    for _ in range(max(0, int(n_sheep))):
        sim.spawn_sheep()
    for _ in range(max(0, int(n_monsters))):
        sim.spawn_monster()
    return sim


def build_world(am, seed, procedural=False, *, populate_dense=True,
                n_agents=0, tile_period=None, ridge_width=None,
                water_frac=WATER_FRAC, mountain_frac=MOUNTAIN_FRAC):
    """Construit le monde complet : heightmap, décor, simulation prête.

    `procedural=False` conserve l'ancien comportement (terre pleine, pas de
    relief) ; `procedural=True` génère les chaînes de montagnes.
    """

    rng = np.random.default_rng(seed)
    w = World()

    gen = compute_land(seed if procedural else None,
                       tile_period=tile_period, ridge_width=ridge_width,
                       water_frac=water_frac, mountain_frac=mountain_frac)
    if gen is not None:
        from game import worldgen as _wg
        _wg.apply_to_layers(w, gen)          # pose aussi w.gen
    else:
        w.set_land(np.ones((GRID, GRID), dtype=np.uint8))
        w.gen = None
    w.save_mountains()

    sim = Sim(w, am, seed=seed)

    # ← la v1 sautait cette étape : le monde naissait stérile
    populate(w, am, rng, dense=populate_dense)

    seed_life(w, sim, rng, n_agents=n_agents)

    sim.paused = True
    if gen is not None:
        from game import worldgen as _wg
        parts = sorted(_wg.stats(gen).items(), key=lambda kv: -kv[1])[:4]
        repartition = ", ".join(f"{k} {v*100:.0f}%" for k, v in parts)
        px = world_pixels()
        sim.log(f"Monde prêt — {px}x{px} px ({GRID}x{GRID} tuiles) · "
                f"terre {(1 - water_frac) * 100:.0f}% / eau {water_frac * 100:.0f}% · "
                f"crêtes tous les {gen.tile_period * TILE} px · {repartition}. "
                f"Outil « Sculpter » pour creuser, « Restaurer » pour rétablir.",
                (108, 208, 128), "world")
    else:
        sim.log("Monde prêt — terrain plat, pas de relief.",
                (108, 208, 128), "world")
    return w, sim


def build_world_blank(am, seed):
    """Monde vierge : tout eau, aucun asset, aucun habitant.
    L'utilisateur peint ses îles avec les outils de terrain."""

    w = World()
    w.set_land(np.zeros((GRID, GRID), dtype=np.uint8))
    w.gen = None
    sim = Sim(w, am, seed=seed)
    sim.paused = True
    sim.log("Monde vide — tout est océan. Peignez des îles avec les outils "
            "de terrain.", (78, 168, 232), "world")
    return w, sim


def _spawn_spot(w, rng, tries=400):
    """Trouve une case libre et praticable pour y faire naître un être."""
    for _ in range(tries):
        x = int(rng.integers(8, GRID - 8))
        y = int(rng.integers(8, GRID - 8))
        if w.land[y, x] and not w.blocked[y, x] and w.content_at(x, y) < 0:
            return x, y
    ys, xs = np.nonzero(w.land > 0)
    if len(xs):
        i = int(rng.integers(0, len(xs)))
        return int(xs[i]), int(ys[i])
    return GRID // 2, GRID // 2
