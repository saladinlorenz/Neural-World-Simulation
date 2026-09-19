"""worldgen.py — Génération procédurale de terrain (v2).

Corrections majeures par rapport à la v1
----------------------------------------
1. BUG DE PÉRIODE : la v1 calculait `warped_x = xs_l * scale` avec
   `scale = low / g` (< 1), ce qui écrasait les coordonnées et produisait
   moins d'UNE crête sur toute la carte au lieu de `g / tile_period`.
   Tout le pipeline travaille désormais en **unités de tuiles réelles**.
2. PERFORMANCE : `_fbm` appelait `noise2()` cellule par cellule en Python
   (des centaines de milliers d'appels). On utilise `noise2array`, qui
   évalue toute la grille en C. Gain de deux ordres de grandeur.
3. NIVEAU DE LA MER : la v1 noyait ~42 % de la carte parce que le bruit de
   plaine était centré trop bas. Le relief est maintenant construit comme
   « socle continental + crêtes », avec `sea_level` explicite.
4. RENDU : `render_patch_rgb` passe par une LUT de palette (une seule
   opération numpy) au lieu d'une boucle masque par biome.
5. VERSIONNAGE : `gen.version` s'incrémente à chaque sculpture, ce qui
   permet au renderer de garder son terrain en cache au lieu de le
   recalculer chaque frame.
6. ROBUSTESSE : `apply_to_layers` respecte le dtype des couches déjà
   allouées par World, `_sync_layers` ne suppose plus l'existence des
   attributs, les bornes sont clampées partout, et le module fonctionne
   sans scipy ni opensimplex grâce à des replis internes.

API publique
------------
    generate(grid_size, tile_period, ridge_width, seed) -> WorldGen
    apply_to_layers(world, gen)
    carve_mountain / raise_terrain / flatten_terrain / restore_mountain
    render_patch_rgb(gen, y0, y1, x0, x1)   -> uint8 (h, w, 3)
    render_minimap_rgb(gen, size)           -> uint8 (size, size, 3)
    is_mountain / is_carved / biome_at / biome_name / height_at / passable
    slope(gen) / stats(gen)
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field

# ── dépendances optionnelles ──────────────────────────────────────────────────
try:
    from scipy.ndimage import zoom as _scipy_zoom
    _HAS_SCIPY = True
except ImportError:                                     # pragma: no cover
    _scipy_zoom = None
    _HAS_SCIPY = False

try:
    from opensimplex import OpenSimplex
    _HAS_SIMPLEX = True
except ImportError:                                     # pragma: no cover
    OpenSimplex = None
    _HAS_SIMPLEX = False


# ══════════════════════════════════════════════════════════════════════════════
#  Constantes
# ══════════════════════════════════════════════════════════════════════════════
BIOME_WATER  = 0
BIOME_MARSH  = 1
BIOME_SAND   = 2
BIOME_GRASS  = 3
BIOME_FOREST = 4
BIOME_ROCK   = 5
BIOME_SNOW   = 6
N_BIOMES     = 7

# Seuils d'altitude dans [0..1]
H_WATER = 0.30     # < H_WATER   → eau
H_SAND  = 0.34     # < H_SAND    → sable / berge
H_MARSH = 0.36     # < H_MARSH   → marécage
H_GRASS = 0.62     # < H_GRASS   → herbe / forêt (selon humidité)
H_ROCK  = 0.82     # < H_ROCK    → roche
#                    >= H_ROCK   → neige

# Palette indexée par BIOME_* — utilisée comme LUT numpy dans le rendu
BIOME_PALETTE = np.array([
    ( 46,  92, 158),   # WATER
    ( 74, 112,  82),   # MARSH
    (206, 194, 148),   # SAND
    ( 86, 150,  62),   # GRASS
    ( 44, 104,  50),   # FOREST
    (128, 118, 106),   # ROCK
    (234, 238, 244),   # SNOW
], dtype=np.float32)

BIOME_NAMES = {
    BIOME_WATER: "eau", BIOME_MARSH: "marécage", BIOME_SAND: "berge",
    BIOME_GRASS: "prairie", BIOME_FOREST: "forêt",
    BIOME_ROCK: "roche", BIOME_SNOW: "neige",
}

# Direction de lumière pour l'ombrage de pente
_LIGHT = np.array([0.62, -0.32, 1.0], dtype=np.float32)
_LIGHT /= np.linalg.norm(_LIGHT)

# Le heightmap vaut [0..1] sur une grille de tuiles : les pentes brutes sont
# minuscules, on les amplifie pour obtenir un relief lisible à l'écran.
_SLOPE_GAIN = 28.0


# ══════════════════════════════════════════════════════════════════════════════
#  Structure de données
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class WorldGen:
    """Couches du terrain : `height_base` procédural immuable, `height_current`
    mutable (sculpté par l'utilisateur)."""
    g: int                                  # côté de la grille, en tuiles

    height_base:    np.ndarray              # float32 [0..1] — référence procédurale
    height_current: np.ndarray              # float32 [0..1] — état courant
    moisture:       np.ndarray              # float32 [0..1]
    biome:          np.ndarray              # uint8  — BIOME_*
    shade:          np.ndarray              # float32 [0.30..1.0]
    carved:         np.ndarray              # bool   — modifié par l'outil

    tile_period: int = 250
    ridge_width: int = 55
    seed:        int = 42

    # incrémenté à chaque modification → clé de cache pour le renderer
    version: int = 0
    # union des zones modifiées depuis le dernier clear_dirty(), ou None
    last_dirty: tuple | None = field(default=None, repr=False)

    @property
    def shape(self):
        return (self.g, self.g)

    def touch(self, y0, y1, x0, x1):
        """Marque une zone comme modifiée et fait avancer la version."""
        self.version += 1
        if self.last_dirty is None:
            self.last_dirty = (y0, y1, x0, x1)
        else:
            py0, py1, px0, px1 = self.last_dirty
            self.last_dirty = (min(py0, y0), max(py1, y1),
                               min(px0, x0), max(px1, x1))

    def clear_dirty(self):
        self.last_dirty = None


# ══════════════════════════════════════════════════════════════════════════════
#  Bruit
# ══════════════════════════════════════════════════════════════════════════════
def _noise_lattice(xs_1d: np.ndarray, ys_1d: np.ndarray, seed: int) -> np.ndarray:
    """Une octave de bruit sur un treillis régulier → (len(ys), len(xs))."""
    if _HAS_SIMPLEX:
        gen = OpenSimplex(seed=int(seed) & 0x7FFFFFFF)
        # noise2array évalue toute la grille côté C
        return np.asarray(gen.noise2array(xs_1d.astype(np.float64),
                                          ys_1d.astype(np.float64)),
                          dtype=np.float32)
    return _value_noise(xs_1d, ys_1d, seed)


def _value_noise(xs_1d: np.ndarray, ys_1d: np.ndarray, seed: int) -> np.ndarray:
    """Repli sans opensimplex : value-noise interpolé en cosinus, vectorisé.

    Qualité inférieure au simplex, mais continu, sans artefact de grille
    visible, et parfaitement déterministe pour une graine donnée.
    """
    rng = np.random.default_rng(seed & 0x7FFFFFFF)
    x0i = int(np.floor(xs_1d.min())) - 1
    x1i = int(np.ceil(xs_1d.max())) + 2
    y0i = int(np.floor(ys_1d.min())) - 1
    y1i = int(np.ceil(ys_1d.max())) + 2
    lat = rng.random((y1i - y0i, x1i - x0i), dtype=np.float32) * 2.0 - 1.0

    fx = xs_1d - x0i
    fy = ys_1d - y0i
    ix = np.floor(fx).astype(np.int32)
    iy = np.floor(fy).astype(np.int32)
    tx = fx - ix
    ty = fy - iy
    tx = (1.0 - np.cos(tx * np.pi)) * 0.5     # lissage C1
    ty = (1.0 - np.cos(ty * np.pi)) * 0.5

    ix = np.clip(ix, 0, lat.shape[1] - 2)
    iy = np.clip(iy, 0, lat.shape[0] - 2)

    v00 = lat[np.ix_(iy, ix)]
    v01 = lat[np.ix_(iy, ix + 1)]
    v10 = lat[np.ix_(iy + 1, ix)]
    v11 = lat[np.ix_(iy + 1, ix + 1)]

    TX = tx[None, :]
    TY = ty[:, None]
    top = v00 + (v01 - v00) * TX
    bot = v10 + (v11 - v10) * TX
    return (top + (bot - top) * TY).astype(np.float32)


def _octave_res(span: float, freq: float, low: int) -> int:
    """Résolution d'échantillonnage suffisante pour une octave donnée.

    Une octave de fréquence `freq` (cycles par tuile) produit `span * freq`
    cycles sur toute la carte ; ~4 échantillons par cycle suffisent avant
    agrandissement. Les octaves basse fréquence coûtent donc presque rien,
    ce qui divise le temps de génération par ~5 sans perte visible.
    """
    cycles = max(1.0, span * freq)
    return int(np.clip(cycles * 4.0, 8, low))


def _fbm_field(span: float, low: int, base_freq: float, octaves: int,
               seed: int, *, lacunarity: float = 2.0, gain: float = 0.5,
               ridged: bool = False) -> np.ndarray:
    """fBm 2-D sur [0, span]², rendu à la résolution (low, low).

    Chaque octave est échantillonnée à sa propre résolution utile puis
    agrandie — c'est l'optimisation clé du module.
    Sortie dans [-1, 1] (fBm classique) ou [0, 1] (ridged).
    """
    out = np.zeros((low, low), dtype=np.float32)
    amp, freq, norm = 1.0, float(base_freq), 0.0
    for o in range(octaves):
        res = _octave_res(span, freq, low)
        c = np.linspace(0.0, span * freq, res, endpoint=False, dtype=np.float32)
        layer = _noise_lattice(c, c, seed + o * 7919)
        if ridged:
            layer = 1.0 - np.abs(layer)
            layer = layer * layer
        out += _upsample(layer, low) * amp
        norm += amp
        amp *= gain
        freq *= lacunarity
    return (out / max(norm, 1e-6)).astype(np.float32)


# ══════════════════════════════════════════════════════════════════════════════
#  Agrandissement
# ══════════════════════════════════════════════════════════════════════════════
def _upsample(low: np.ndarray, out_size: int) -> np.ndarray:
    """Agrandit une grille carrée vers (out_size, out_size), bicubique si possible."""
    if low.shape == (out_size, out_size):
        return low.astype(np.float32, copy=True)
    if _HAS_SCIPY:
        z = _scipy_zoom(low.astype(np.float64),
                        (out_size / low.shape[0], out_size / low.shape[1]),
                        order=3, mode="nearest", grid_mode=True, prefilter=True)
        return _fit(np.asarray(z, dtype=np.float32), out_size)
    return _fit(_bilinear(low, out_size), out_size)


def _bilinear(low: np.ndarray, out_size: int) -> np.ndarray:
    """Repli sans scipy : agrandissement bilinéaire vectorisé."""
    h, w = low.shape
    ys = np.linspace(0, h - 1, out_size, dtype=np.float32)
    xs = np.linspace(0, w - 1, out_size, dtype=np.float32)
    y0 = np.floor(ys).astype(np.int32); y1 = np.minimum(y0 + 1, h - 1)
    x0 = np.floor(xs).astype(np.int32); x1 = np.minimum(x0 + 1, w - 1)
    wy = (ys - y0)[:, None]
    wx = (xs - x0)[None, :]
    a = low[np.ix_(y0, x0)]; b = low[np.ix_(y0, x1)]
    c = low[np.ix_(y1, x0)]; d = low[np.ix_(y1, x1)]
    top = a + (b - a) * wx
    bot = c + (d - c) * wx
    return (top + (bot - top) * wy).astype(np.float32)


def _fit(arr: np.ndarray, size: int) -> np.ndarray:
    """Recadre / complète un tableau carré à exactement (size, size)."""
    h, w = arr.shape
    if h == size and w == size:
        return arr
    out = np.empty((size, size), dtype=np.float32)
    hh, ww = min(h, size), min(w, size)
    out[:hh, :ww] = arr[:hh, :ww]
    if hh < size:
        out[hh:, :ww] = out[hh - 1, :ww]
    if ww < size:
        out[:, ww:] = out[:, ww - 1:ww]
    return out


# ══════════════════════════════════════════════════════════════════════════════
#  Dimensionnement
# ══════════════════════════════════════════════════════════════════════════════
def grid_for_pixels(width_px: int, tile: int = 16) -> int:
    """Nombre de tuiles nécessaires pour couvrir `width_px` pixels.

    Exemple : grid_for_pixels(15000, 16) -> 938  (soit 15008 px de côté).
    Toute la simulation raisonne en tuiles ; le pixel n'existe qu'au rendu.
    """
    return int(np.ceil(float(width_px) / max(1, int(tile))))


def period_for_pixels(spacing_px: int, tile: int = 16) -> int:
    """Espacement des chaînes de montagnes, converti en tuiles."""
    return max(16, int(round(float(spacing_px) / max(1, int(tile)))))


# ══════════════════════════════════════════════════════════════════════════════
#  Génération
# ══════════════════════════════════════════════════════════════════════════════
def generate(
    grid_size:    int = 1000,
    tile_period:  int = 250,      # espacement des chaînes, en tuiles (250 = 4000px @ TILE 16)
    ridge_width:  int = 55,       # demi-largeur d'une chaîne, en tuiles
    seed:         int = 42,
    *,
    water_frac:    float = 0.08,  # fraction EXACTE de la carte sous le niveau de la mer
    mountain_frac: float = 0.14,  # fraction EXACTE de montagne infranchissable
    sea_level:    float = 0.30,   # cohérent avec H_WATER
    mountain_amp: float = 0.52,   # hauteur ajoutée au sommet d'une crête
    detail_res:   int | None = None,   # résolution interne (None = auto)
) -> WorldGen:
    """Construit le heightmap complet et toutes les couches dérivées.

    Le bruit est calculé sur une grille interne basse résolution puis agrandi
    en bicubique : le fBm est dominé par ses basses fréquences, l'agrandissement
    ne coûte donc presque rien visuellement et divise le temps de calcul par
    (grid_size / detail_res)².
    """
    g = int(grid_size)
    if g < 16:
        raise ValueError("grid_size doit valoir au moins 16 tuiles")
    tile_period = max(16, int(tile_period))
    ridge_width = int(np.clip(ridge_width, 4, max(5, tile_period // 2 - 1)))

    if detail_res is None:
        detail_res = int(np.clip(g // 6, 96, 320))
    low = int(min(detail_res, g))

    # ── coordonnées du treillis, en TUILES RÉELLES (correction centrale) ──
    coords = np.linspace(0.0, float(g), low, endpoint=False, dtype=np.float32)

    # ── 1. déformation de domaine : fait onduler l'axe des crêtes ─────────
    span = float(g)
    warp_freq = 1.0 / max(tile_period * 1.6, 1.0)
    warp_x = _fbm_field(span, low, warp_freq, 4, seed + 101) * (ridge_width * 1.35)

    xs_grid = np.broadcast_to(coords[None, :], (low, low))
    warped_x = xs_grid + warp_x

    # ── 2. distance à la crête périodique la plus proche ──────────────────
    half = tile_period * 0.5
    dist = np.abs(((warped_x + half) % tile_period) - half)
    ridge = np.clip(1.0 - dist / float(ridge_width), 0.0, 1.0) ** 1.7

    # ── 3. cols et brèches : une chaîne n'est jamais continue ─────────────
    gap_freq = 1.0 / max(tile_period * 0.55, 1.0)
    gaps = _fbm_field(span, low, gap_freq, 3, seed + 303)
    ridge = ridge * np.clip(0.74 + 0.50 * gaps, 0.22, 1.0)

    # ── 4. rugosité interne de la chaîne ─────────────────────────────────
    rough = _fbm_field(span, low, 1.0 / 26.0, 5, seed + 404, ridged=True)
    ridge_h = ridge * (0.58 + 0.42 * rough)

    # ── 5. socle continental : plaines, vallées, lacs ─────────────────────
    cont = _fbm_field(span, low, 1.0 / 210.0, 5, seed + 505)
    cont01 = np.clip((cont + 1.0) * 0.5, 0.0, 1.0)
    base = sea_level - 0.10 + cont01 * 0.36          # ≈ [0.20 .. 0.56]

    micro = _fbm_field(span, low, 1.0 / 34.0, 3, seed + 606)
    base = base + micro * 0.028                      # casse la platitude

    # ── 6. altitude finale ────────────────────────────────────────────────
    h_low = np.clip(base + ridge_h * mountain_amp, 0.0, 1.0)

    # ── 7. humidité (prairie ↔ forêt) ────────────────────────────────────
    moist = _fbm_field(span, low, 1.0 / 130.0, 4, seed + 707)
    moist_low = np.clip((moist + 1.0) * 0.5, 0.0, 1.0)

    # ── 8. agrandissement vers la grille de simulation ───────────────────
    height   = np.clip(_upsample(h_low, g), 0.0, 1.0)
    moisture = np.clip(_upsample(moist_low, g), 0.0, 1.0)

    # ── 8bis. calibration des proportions ────────────────────────────────
    height = _calibrate(height, water_frac, mountain_frac)
    # ombre pluviométrique : il pleut moins haut
    moisture = np.clip(moisture - np.clip(height - H_GRASS, 0.0, 1.0) * 0.8, 0.0, 1.0)

    return WorldGen(
        g              = g,
        height_base    = height.copy(),
        height_current = height,
        moisture       = moisture,
        biome          = _compute_biome(height, moisture),
        shade          = _compute_shade(height),
        carved         = np.zeros((g, g), dtype=bool),
        tile_period    = tile_period,
        ridge_width    = ridge_width,
        seed           = int(seed),
    )


def _calibrate(height: np.ndarray, water_frac: float,
               mountain_frac: float) -> np.ndarray:
    """Remappe l'altitude pour obtenir EXACTEMENT les proportions demandées.

    Le bruit fractal ne donne aucune garantie sur la part d'eau ou de montagne :
    elle dérive des paramètres et change avec la graine. On mesure donc les
    quantiles réels du heightmap et on l'étire par morceaux pour que :
        quantile(water_frac)              tombe pile sur H_WATER
        quantile(1 - mountain_frac)       tombe pile sur H_GRASS
    Le remappage est monotone et affine par morceaux : le relief, les vallées
    et les crêtes sont conservés, seules les altitudes-seuils sont recalées.
    """
    water_frac = float(np.clip(water_frac, 0.0, 0.60))
    mountain_frac = float(np.clip(mountain_frac, 0.0, 0.80 - water_frac))

    lo, hi = float(height.min()), float(height.max())
    if hi - lo < 1e-6:
        return np.full_like(height, (H_WATER + H_GRASS) * 0.5)

    q_w = float(np.quantile(height, water_frac)) if water_frac > 0 else lo
    q_m = float(np.quantile(height, 1.0 - mountain_frac)) if mountain_frac > 0 else hi

    # les points d'ancrage doivent rester strictement croissants
    eps = (hi - lo) * 1e-4
    q_w = min(max(q_w, lo + eps), hi - 2 * eps)
    q_m = min(max(q_m, q_w + eps), hi - eps)

    xp = [lo, q_w, q_m, hi]
    fp = [0.0, H_WATER, H_GRASS, 1.0]
    out = np.interp(height.astype(np.float64), xp, fp).astype(np.float32)
    return np.clip(out, 0.0, 1.0)


# ══════════════════════════════════════════════════════════════════════════════
#  Synchronisation avec les couches de World
# ══════════════════════════════════════════════════════════════════════════════
def _masks(h: np.ndarray):
    """Retourne (water, land, blocked) pour un bloc d'altitudes."""
    water   = h < H_WATER
    blocked = h >= H_GRASS
    land    = ~water & ~blocked
    return water, land, blocked


def apply_to_layers(world, gen: WorldGen) -> None:
    """Initialise world.land / world.blocked / world.water depuis `gen`.

    Le dtype des couches existantes est préservé (World les alloue en uint8) ;
    une couche absente est créée en uint8.
    """
    water, land, blocked = _masks(gen.height_current)
    for name, mask in (("water", water), ("land", land), ("blocked", blocked)):
        cur = getattr(world, name, None)
        if isinstance(cur, np.ndarray) and cur.shape == mask.shape:
            cur[...] = mask.astype(cur.dtype, copy=False)
        else:
            setattr(world, name, mask.astype(np.uint8))
    world.gen = gen


def _sync_layers(world, gen: WorldGen, y0: int, y1: int, x0: int, x1: int) -> None:
    """Resynchronise les couches sur le patch [y0:y1, x0:x1] uniquement.

    C'est ce qui rend l'outil de sculpture instantané : quelques centaines de
    tuiles sont retraitées, jamais le million de la carte complète.
    """
    h = gen.height_current[y0:y1, x0:x1]
    water, land, blocked = _masks(h)
    for name, mask in (("water", water), ("land", land), ("blocked", blocked)):
        cur = getattr(world, name, None)
        if isinstance(cur, np.ndarray) and cur.shape == gen.shape:
            cur[y0:y1, x0:x1] = mask.astype(cur.dtype, copy=False)

    gen.biome[y0:y1, x0:x1] = _compute_biome(h, gen.moisture[y0:y1, x0:x1])

    # l'ombrage dépend du gradient : on élargit d'une tuile puis on recadre
    py0, py1 = max(0, y0 - 1), min(gen.g, y1 + 1)
    px0, px1 = max(0, x0 - 1), min(gen.g, x1 + 1)
    sh = _compute_shade(gen.height_current[py0:py1, px0:px1])
    gen.shade[y0:y1, x0:x1] = sh[y0 - py0: y0 - py0 + (y1 - y0),
                                 x0 - px0: x0 - px0 + (x1 - x0)]

    # un objet posé sur une case devenue eau ou montagne n'a plus de sens
    _drop_orphans(world, gen, y0, y1, x0, x1, land)

    gen.touch(y0, y1, x0, x1)


def _drop_orphans(world, gen, y0, y1, x0, x1, land_mask):
    remover = getattr(world, "remove", None)
    content = getattr(world, "content", None)
    if not callable(remover) or not isinstance(content, np.ndarray):
        return
    if content.shape != gen.shape:
        return
    bad = (~land_mask) & (content[y0:y1, x0:x1] >= 0)
    if not bad.any():
        return
    for j, i in zip(*np.nonzero(bad)):
        try:
            remover(int(x0 + i), int(y0 + j), quiet=True)
        except TypeError:
            try:
                remover(int(x0 + i), int(y0 + j))
            except Exception:
                import sys
                print(f"[worldgen._drop_orphans] {sys.exc_info()[1]}", file=sys.stderr)
        except Exception:
            import sys
            print(f"[worldgen._drop_orphans] {sys.exc_info()[1]}", file=sys.stderr)


# ══════════════════════════════════════════════════════════════════════════════
#  Outils de sculpture
# ══════════════════════════════════════════════════════════════════════════════
def _brush(gen: WorldGen, tx: int, ty: int, radius: int):
    """Retourne (y0, y1, x0, x1, falloff) ou None si le pinceau est hors carte."""
    radius = max(1, int(radius))
    tx, ty = int(tx), int(ty)
    y0, y1 = max(0, ty - radius), min(gen.g, ty + radius + 1)
    x0, x1 = max(0, tx - radius), min(gen.g, tx + radius + 1)
    if y1 <= y0 or x1 <= x0:
        return None
    yy = np.arange(y0, y1, dtype=np.float32)[:, None] - ty
    xx = np.arange(x0, x1, dtype=np.float32)[None, :] - tx
    d = np.sqrt(yy * yy + xx * xx) / radius
    t = np.clip(1.0 - d, 0.0, 1.0)
    falloff = (t * t * (3.0 - 2.0 * t)).astype(np.float32)   # smoothstep
    return y0, y1, x0, x1, falloff


def carve_mountain(world, gen: WorldGen, tx: int, ty: int,
                   radius: int = 10, strength: float = 0.12) -> bool:
    """Abaisse le terrain sous le pinceau. True si quelque chose a changé."""
    br = _brush(gen, tx, ty, radius)
    if br is None:
        return False
    y0, y1, x0, x1, falloff = br
    patch = gen.height_current[y0:y1, x0:x1]
    before = patch.copy()
    np.clip(patch - float(strength) * falloff, 0.0, 1.0, out=patch)
    if np.array_equal(before, patch):
        return False

    was_high = gen.height_base[y0:y1, x0:x1] >= H_GRASS
    gen.carved[y0:y1, x0:x1] |= was_high & (patch < H_GRASS)

    _sync_layers(world, gen, y0, y1, x0, x1)
    return True


def raise_terrain(world, gen: WorldGen, tx: int, ty: int,
                  radius: int = 10, strength: float = 0.12) -> bool:
    """Élève le terrain sous le pinceau — le pendant de `carve_mountain`."""
    br = _brush(gen, tx, ty, radius)
    if br is None:
        return False
    y0, y1, x0, x1, falloff = br
    patch = gen.height_current[y0:y1, x0:x1]
    before = patch.copy()
    np.clip(patch + float(strength) * falloff, 0.0, 1.0, out=patch)
    if np.array_equal(before, patch):
        return False
    gen.carved[y0:y1, x0:x1] |= falloff > 0.02
    _sync_layers(world, gen, y0, y1, x0, x1)
    return True


def flatten_terrain(world, gen: WorldGen, tx: int, ty: int,
                    radius: int = 10, strength: float = 0.25) -> bool:
    """Aplanit vers la hauteur moyenne du pinceau — prépare un terrain de village."""
    br = _brush(gen, tx, ty, radius)
    if br is None:
        return False
    y0, y1, x0, x1, falloff = br
    patch = gen.height_current[y0:y1, x0:x1]
    core = falloff > 0.35
    target = float(patch[core].mean()) if core.any() else float(patch.mean())
    k = np.clip(float(strength) * falloff, 0.0, 1.0)
    np.clip(patch + k * (target - patch), 0.0, 1.0, out=patch)
    gen.carved[y0:y1, x0:x1] |= falloff > 0.02
    _sync_layers(world, gen, y0, y1, x0, x1)
    return True


def restore_mountain(world, gen: WorldGen, tx: int, ty: int,
                     radius: int = 10, strength: float = 0.15) -> bool:
    """Ramène progressivement le terrain vers sa forme procédurale d'origine."""
    br = _brush(gen, tx, ty, radius)
    if br is None:
        return False
    y0, y1, x0, x1, falloff = br
    base  = gen.height_base[y0:y1, x0:x1]
    patch = gen.height_current[y0:y1, x0:x1]
    if np.allclose(patch, base, atol=1e-4):
        return False
    k = np.clip(float(strength) * falloff * 4.0, 0.0, 1.0)
    np.clip(patch + k * (base - patch), 0.0, 1.0, out=patch)
    gen.carved[y0:y1, x0:x1] &= np.abs(patch - base) >= 0.02
    _sync_layers(world, gen, y0, y1, x0, x1)
    return True


# ══════════════════════════════════════════════════════════════════════════════
#  Rendu
# ══════════════════════════════════════════════════════════════════════════════
def render_patch_rgb(gen: WorldGen, y0: int, y1: int, x0: int, x1: int,
                     *, shading: bool = True) -> np.ndarray:
    """Retourne un uint8 (h, w, 3) — une couleur par tuile.

    Couleur = palette du biome, modulée par l'altitude locale puis par
    l'ombrage de pente. Une seule passe numpy, aucune boucle Python.
    """
    y0 = max(0, int(y0)); y1 = min(gen.g, int(y1))
    x0 = max(0, int(x0)); x1 = min(gen.g, int(x1))
    if y1 <= y0 or x1 <= x0:
        return np.zeros((1, 1, 3), dtype=np.uint8)

    biome  = gen.biome[y0:y1, x0:x1]
    height = gen.height_current[y0:y1, x0:x1]

    rgb = BIOME_PALETTE[biome]                       # LUT → (h, w, 3) float32
    rgb = rgb * (1.0 + (height - 0.45) * 0.30)[:, :, None]

    if shading:
        rgb = rgb * gen.shade[y0:y1, x0:x1][:, :, None]

    # les tuiles sculptées sont légèrement désaturées : le geste reste visible
    carved = gen.carved[y0:y1, x0:x1]
    if carved.any():
        grey = rgb.mean(axis=2, keepdims=True)
        rgb = np.where(carved[:, :, None], rgb * 0.82 + grey * 0.18, rgb)

    return np.clip(rgb, 0, 255).astype(np.uint8)


def render_minimap_rgb(gen: WorldGen, size: int = 128) -> np.ndarray:
    """Vignette (size, size, 3) du monde entier — sous-échantillonnage par pas."""
    size = max(8, int(size))
    step = max(1, gen.g // size)
    idx = np.arange(0, gen.g, step)[:size]
    rgb = BIOME_PALETTE[gen.biome[np.ix_(idx, idx)]]
    rgb = rgb * gen.shade[np.ix_(idx, idx)][:, :, None]
    return np.clip(rgb, 0, 255).astype(np.uint8)


# ══════════════════════════════════════════════════════════════════════════════
#  Couches dérivées
# ══════════════════════════════════════════════════════════════════════════════
def _compute_biome(height: np.ndarray, moisture: np.ndarray) -> np.ndarray:
    """Assigne un BIOME_* par tuile, depuis l'altitude et l'humidité."""
    biome = np.full(height.shape, BIOME_GRASS, dtype=np.uint8)
    biome[height >= H_ROCK] = BIOME_SNOW
    biome[(height >= H_GRASS) & (height < H_ROCK)] = BIOME_ROCK

    low = height < H_GRASS
    biome[low & (height >= H_MARSH) & (moisture > 0.56)] = BIOME_FOREST
    biome[low & (height >= H_SAND) & (height < H_MARSH)] = BIOME_MARSH
    biome[low & (height >= H_WATER) & (height < H_SAND)] = BIOME_SAND
    biome[height < H_WATER] = BIOME_WATER
    return biome


def _compute_shade(height: np.ndarray) -> np.ndarray:
    """Ombrage de pente (pseudo normal-map) depuis le gradient du heightmap."""
    if height.shape[0] < 2 or height.shape[1] < 2:
        return np.ones(height.shape, dtype=np.float32)
    gy, gx = np.gradient(height.astype(np.float32))
    gx = gx * _SLOPE_GAIN
    gy = gy * _SLOPE_GAIN
    inv = 1.0 / np.sqrt(gx * gx + gy * gy + 1.0)
    lx, ly, lz = _LIGHT
    lambert = (-gx * lx - gy * ly + lz) * inv
    return np.clip(0.42 + lambert * 0.62, 0.30, 1.0).astype(np.float32)


def slope(gen: WorldGen) -> np.ndarray:
    """Norme du gradient d'altitude — p. ex. pour interdire les arbres en pente."""
    gy, gx = np.gradient(gen.height_current.astype(np.float32))
    return np.sqrt(gx * gx + gy * gy) * _SLOPE_GAIN


# ══════════════════════════════════════════════════════════════════════════════
#  Accès ponctuel
# ══════════════════════════════════════════════════════════════════════════════
def _in_bounds(gen: WorldGen, tx: int, ty: int) -> bool:
    return 0 <= tx < gen.g and 0 <= ty < gen.g


def is_mountain(gen: WorldGen, tx: int, ty: int) -> bool:
    return _in_bounds(gen, tx, ty) and bool(gen.height_current[ty, tx] >= H_GRASS)


def is_carved(gen: WorldGen, tx: int, ty: int) -> bool:
    return _in_bounds(gen, tx, ty) and bool(gen.carved[ty, tx])


def biome_at(gen: WorldGen, tx: int, ty: int) -> int:
    return int(gen.biome[ty, tx]) if _in_bounds(gen, tx, ty) else BIOME_WATER


def biome_name(gen: WorldGen, tx: int, ty: int) -> str:
    return BIOME_NAMES.get(biome_at(gen, tx, ty), "?")


def height_at(gen: WorldGen, tx: int, ty: int) -> float:
    return float(gen.height_current[ty, tx]) if _in_bounds(gen, tx, ty) else 0.0


def passable(gen: WorldGen, tx: int, ty: int) -> bool:
    if not _in_bounds(gen, tx, ty):
        return False
    return bool(H_WATER <= gen.height_current[ty, tx] < H_GRASS)


def stats(gen: WorldGen) -> dict:
    """Répartition des biomes en fraction du total — pour le journal / debug."""
    counts = np.bincount(gen.biome.ravel(), minlength=N_BIOMES).astype(np.float64)
    total = max(1.0, counts.sum())
    return {BIOME_NAMES[i]: counts[i] / total for i in range(N_BIOMES)}


# ══════════════════════════════════════════════════════════════════════════════
#  Auto-test
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import time

    class _FakeWorld:
        def __init__(self, g):
            self.land    = np.zeros((g, g), np.uint8)
            self.blocked = np.zeros((g, g), np.uint8)
            self.water   = np.zeros((g, g), np.uint8)

    print("worldgen v2 — auto-test")
    print(f"  scipy={_HAS_SCIPY}  opensimplex={_HAS_SIMPLEX}")

    print(f"  15000px @ TILE 16 -> grille {grid_for_pixels(15000, 16)} tuiles")
    for g, period in ((500, 125), (938, 250)):
        t0 = time.perf_counter()
        gen = generate(grid_size=g, tile_period=period, ridge_width=28, seed=7,
                       water_frac=0.08, mountain_frac=0.14)
        dt = time.perf_counter() - t0
        w = _FakeWorld(g)
        apply_to_layers(w, gen)
        print(f"  {g}x{g} en {dt:.2f}s  terre={w.land.mean()*100:.0f}%  "
              f"montagne={w.blocked.mean()*100:.0f}%  eau={w.water.mean()*100:.0f}%")
        print("    biomes: " + "  ".join(f"{k}={v*100:.0f}%"
                                         for k, v in stats(gen).items()))
        row = gen.height_base[g // 2] >= H_GRASS
        crossings = int(np.count_nonzero(row[1:] & ~row[:-1]))
        print(f"    chaines traversees (ligne mediane) : {crossings} "
              f"(attendu ~ {g // period})")

    gen = generate(grid_size=400, tile_period=100, ridge_width=22, seed=3)
    w = _FakeWorld(400)
    apply_to_layers(w, gen)
    ys, xs = np.nonzero(gen.height_current >= H_GRASS)
    ty, tx = int(ys[len(ys) // 2]), int(xs[len(xs) // 2])
    h0 = height_at(gen, tx, ty)
    for _ in range(8):
        carve_mountain(w, gen, tx, ty, radius=10, strength=0.15)
    h1 = height_at(gen, tx, ty)
    assert h1 < h0 and not w.blocked[ty, tx], "la sculpture doit ouvrir un passage"
    assert gen.carved[ty, tx], "le drapeau carved doit etre pose"
    for _ in range(12):
        restore_mountain(w, gen, tx, ty, radius=10, strength=0.30)
    h2 = height_at(gen, tx, ty)
    assert abs(h2 - gen.height_base[ty, tx]) < 0.02, "la restauration doit revenir a la base"
    assert not gen.carved[ty, tx]
    print(f"  sculpture : {h0:.3f} -> {h1:.3f} -> {h2:.3f}  (version={gen.version})")

    img = render_patch_rgb(gen, 0, 120, 0, 160)
    mini = render_minimap_rgb(gen, 96)
    assert img.shape == (120, 160, 3) and img.dtype == np.uint8
    assert mini.shape == (96, 96, 3)
    print(f"  rendu {img.shape} · minimap {mini.shape}")
    print("OK")
