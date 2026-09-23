from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from typing import Optional

import numpy as np
from PIL import Image


#: Côté d'un chunk de terrain détaillé, en tuiles. 64 tuiles = 1024 px monde :
#: assez grand pour amortir le rendu, assez petit pour n'en avoir que quelques
#: uns à l'écran (9 au pire en 1600x900 à zoom 1.3).
CHUNK = 64


@dataclass
class TerrainImage:
    """Image RGB du terrain et sa version logique."""

    image: Image.Image
    key: tuple


class TerrainCache:
    """Cache terrain indépendant de PyQt6.

    Le moteur et le cache utilisent seulement Pillow/NumPy.
    La conversion vers QImage reste dans ui_qt.
    """

    def __init__(self, max_size: int = 1600):
        self.max_size = max(128, int(max_size))
        self._terrain: Optional[TerrainImage] = None
        self._minimap: Optional[TerrainImage] = None
        self._terrain_dirty = True
        self._minimap_dirty = True

    def invalidate_terrain(self) -> None:
        self._terrain_dirty = True

    def invalidate_minimap(self) -> None:
        self._minimap_dirty = True

    def invalidate_all(self) -> None:
        self._terrain = None
        self._minimap = None
        self._terrain_dirty = True
        self._minimap_dirty = True

    @staticmethod
    def _worldgen_version(world) -> int:
        gen = getattr(world, "gen", None)
        return int(getattr(gen, "version", 0)) if gen is not None else 0

    def _terrain_key(self, world) -> tuple:
        gen = getattr(world, "gen", None)
        return (
            "terrain",
            int(getattr(world, "g", 0)),
            self._worldgen_version(world),
            bool(gen is not None),
        )

    def _minimap_key(self, world) -> tuple:
        return (
            "minimap",
            int(getattr(world, "g", 0)),
            self._worldgen_version(world),
        )

    @staticmethod
    def _resize_rgb(image: Image.Image, maximum: int) -> Image.Image:
        image = image.convert("RGB")
        width, height = image.size
        scale = min(1.0, float(maximum) / max(width, height, 1))
        if scale >= 1.0:
            return image
        size = (
            max(1, int(round(width * scale))),
            max(1, int(round(height * scale))),
        )
        return image.resize(size, Image.Resampling.BILINEAR)

    @staticmethod
    def _flat_rgb(world) -> np.ndarray:
        g = int(getattr(world, "g", 0))
        if g <= 0:
            return np.zeros((1, 1, 3), dtype=np.uint8)

        land = np.asarray(getattr(world, "land", np.zeros((g, g))), dtype=bool)
        water = np.asarray(getattr(world, "water", np.zeros((g, g))), dtype=bool)
        blocked = np.asarray(getattr(world, "blocked", np.zeros((g, g))), dtype=bool)

        rgb = np.zeros((g, g, 3), dtype=np.uint8)
        rgb[:, :] = (46, 60, 80)
        rgb[land] = (86, 150, 62)
        rgb[blocked] = (128, 118, 106)
        rgb[water] = (46, 92, 158)
        return rgb

    @staticmethod
    def _from_rgb(rgb: np.ndarray) -> Image.Image:
        rgb = np.ascontiguousarray(rgb, dtype=np.uint8)
        if rgb.ndim != 3 or rgb.shape[2] != 3:
            raise ValueError("Le terrain RGB doit avoir la forme H,W,3")
        return Image.fromarray(rgb, mode="RGB")

    def build_terrain(self, world) -> TerrainImage:
        key = self._terrain_key(world)
        if self._terrain is not None and not self._terrain_dirty:
            if self._terrain.key == key:
                return self._terrain

        gen = getattr(world, "gen", None)
        if gen is not None:
            from .worldgen import render_patch_rgb

            rgb = render_patch_rgb(
                gen,
                0,
                int(gen.g),
                0,
                int(gen.g),
                shading=True,
            )
        else:
            rgb = self._flat_rgb(world)

        image = self._resize_rgb(self._from_rgb(rgb), self.max_size)
        self._terrain = TerrainImage(image=image, key=key)
        self._terrain_dirty = False
        return self._terrain

    def build_minimap(self, world, size: int = 192) -> TerrainImage:
        key = self._minimap_key(world)
        if self._minimap is not None and not self._minimap_dirty:
            if self._minimap.key == key:
                return self._minimap

        gen = getattr(world, "gen", None)
        if gen is not None:
            from .worldgen import render_minimap_rgb

            rgb = render_minimap_rgb(gen, int(size))
        else:
            image = self._from_rgb(self._flat_rgb(world))
            image.thumbnail((int(size), int(size)), Image.Resampling.BILINEAR)
            self._minimap = TerrainImage(image=image, key=key)
            self._minimap_dirty = False
            return self._minimap

        image = self._from_rgb(rgb)
        image = image.resize((int(size), int(size)), Image.Resampling.BILINEAR)
        self._minimap = TerrainImage(image=image, key=key)
        self._minimap_dirty = False
        return self._minimap

    @property
    def terrain_dirty(self) -> bool:
        return self._terrain_dirty

    @property
    def minimap_dirty(self) -> bool:
        return self._minimap_dirty


class TerrainChunkCache:
    """Terrain détaillé par chunks de CHUNK x CHUNK tuiles, rendu à la demande.

    L'image globale de ``TerrainCache`` est réduite à ~1600 px pour un monde de
    1000x1000 tuiles : au-delà de zoom 0.5 elle devient illisible. Ici chaque
    chunk est rendu en résolution native (1 px par tuile) par
    ``worldgen.render_patch_rgb`` — attention à l'ordre des arguments
    ``(y0, y1, x0, x1)`` — puis surchargé par les couches dynamiques du monde
    (eau, blocs, fondations, toits, sols peints).

    Clé de cache : ``(cx, cy, version_worldgen, mods_version)``. Tout coup de
    pinceau incrémente ``World.mods_version``, donc aucune tuile modifiée ne
    peut rester affichée dans sa version d'avant.
    """

    def __init__(self, max_chunks: int = 256):
        self.max_chunks = max(16, int(max_chunks))
        self._chunks: "OrderedDict[tuple, np.ndarray]" = OrderedDict()

    def clear(self) -> None:
        self._chunks.clear()

    def __len__(self) -> int:
        return len(self._chunks)

    # ------------------------------------------------------------------
    @staticmethod
    def key(world, cx: int, cy: int) -> tuple:
        gen = getattr(world, "gen", None)
        return (
            int(cx),
            int(cy),
            int(getattr(gen, "version", 0)) if gen is not None else 0,
            int(getattr(world, "mods_version", 0)),
        )

    def chunk_rgb(self, world, cx: int, cy: int) -> np.ndarray:
        """RGB uint8 (h, w, 3) du chunk (cx, cy), h/w <= CHUNK."""
        key = self.key(world, cx, cy)
        rgb = self._chunks.get(key)
        if rgb is None:
            rgb = self._render(world, cx, cy)
            self._chunks[key] = rgb
            while len(self._chunks) > self.max_chunks:
                self._chunks.popitem(last=False)
        else:
            self._chunks.move_to_end(key)
        return rgb

    # ------------------------------------------------------------------
    def _render(self, world, cx: int, cy: int) -> np.ndarray:
        g = int(getattr(world, "g", 0))
        x0 = int(cx) * CHUNK
        y0 = int(cy) * CHUNK
        x1 = min(g, x0 + CHUNK)
        y1 = min(g, y0 + CHUNK)
        if x1 <= x0 or y1 <= y0:
            return np.zeros((1, 1, 3), dtype=np.uint8)

        gen = getattr(world, "gen", None)
        if gen is not None:
            from .worldgen import render_patch_rgb

            rgb = render_patch_rgb(gen, y0, y1, x0, x1, shading=True)
            if rgb.shape[0] != (y1 - y0) or rgb.shape[1] != (x1 - x0):
                rgb = self._flat_rgb(world, x0, y0, x1, y1)
        else:
            rgb = self._flat_rgb(world, x0, y0, x1, y1)

        self._paint_dynamic(world, rgb, x0, y0, x1, y1)
        return rgb

    @staticmethod
    def _flat_rgb(world, x0, y0, x1, y1) -> np.ndarray:
        land = np.asarray(world.land[y0:y1, x0:x1], dtype=bool)
        water = np.asarray(world.water[y0:y1, x0:x1], dtype=bool)
        blocked = np.asarray(world.blocked[y0:y1, x0:x1], dtype=bool)
        rgb = np.zeros((y1 - y0, x1 - x0, 3), dtype=np.uint8)
        rgb[:, :] = (46, 60, 80)
        rgb[land] = (86, 150, 62)
        rgb[blocked] = (128, 118, 106)
        rgb[water] = (46, 92, 158)
        return rgb

    @staticmethod
    def _paint_dynamic(world, rgb: np.ndarray, x0, y0, x1, y1) -> None:
        """Surcharge le rendu worldgen par l'état réel et modifiable du monde."""
        water = np.asarray(world.water[y0:y1, x0:x1], dtype=bool)
        if water.any():
            rgb[water] = (46, 92, 158)

        blocked = np.asarray(world.blocked[y0:y1, x0:x1], dtype=bool)
        content = np.asarray(world.content[y0:y1, x0:x1])
        walls = blocked & (content < 0)
        if walls.any():
            rgb[walls] = (128, 118, 106)

        foundation = np.asarray(world.foundation[y0:y1, x0:x1])
        done = foundation >= 0
        if done.any():
            rgb[done] = (146, 122, 88)

        roof = np.asarray(world.roof[y0:y1, x0:x1])
        done = roof >= 0
        if done.any():
            rgb[done] = (122, 74, 58)

        floor = np.asarray(world.floor[y0:y1, x0:x1])
        painted = floor >= 0
        if painted.any():
            cell = (floor[painted] % 216).astype(np.int64)
            sheet = (floor[painted] // 216).astype(np.int64)
            rgb[painted] = FLOOR_COLORS[(sheet * 216 + cell) % len(FLOOR_COLORS)]


#: Palette approximative des sols peints (sheet*216+cell), indexée modulo.
#: herbe claire / herbe sombre / eau de mare / plancher / terre labourée.
FLOOR_COLORS = np.array(
    [
        (96, 168, 72),
        (78, 142, 60),
        (52, 104, 168),
        (146, 116, 78),
        (108, 84, 58),
    ],
    dtype=np.uint8,
)
