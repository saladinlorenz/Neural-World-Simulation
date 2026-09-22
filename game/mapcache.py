from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
from PIL import Image


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
