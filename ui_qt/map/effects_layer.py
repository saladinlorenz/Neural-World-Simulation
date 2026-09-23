"""EffectsLayer — nuit, pluie, foudre et halo de feu sur la carte.

Contraintes de performance (document de parite, §11) :
- nuit : un seul ``fillRect`` sur le viewport, couleur prise dans une table
  de 32 ``QColor`` precalculees indexee par ``int(clock.light * 31)`` ;
- pluie : budget fixe de 120 segments, positions derivees du tick monde et
  d'un tableau NumPy d'offsets alloue une fois, un seul ``QPen`` ;
- feu : un halo ``QRadialGradient`` rendu UNE fois dans un QPixmap 64x64,
  redessine mis a l'echelle par cellule en feu ;
- foudre : flash de 3 images declenche par ``clock.lightning_tick`` pose par
  le moteur (``game/simulation.py``) — jamais de tirage rng cote peinture.
"""
from __future__ import annotations

import math

import numpy as np

from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtGui import QBrush, QColor, QPen, QRadialGradient, QPainter, QPixmap

from game.config import GRID, TILE

RAIN_BUDGET = 120
FIRE_CELL_BUDGET = 400


def _night_table():
    """32 teintes : index 0 = nuit noire, 31 = plein jour (alpha nul)."""
    colors = []
    for i in range(32):
        f = i / 31.0
        alpha = int(max(0.0, (0.62 - f) / 0.62) * 150)
        if f < 0.45:
            r, g, b = 10, 14, 40
        else:
            t = (f - 0.45) / 0.55
            r = int(10 + 70 * t)
            g = int(14 + 34 * t)
            b = int(40 + 14 * t)
        colors.append(QColor(r, g, b, alpha))
    return colors


class EffectsLayer:
    """Couche meteo/ambiance peinte apres les entites, avant la legende."""

    def __init__(self):
        self._night = _night_table()
        rng = np.random.default_rng(7)
        self._rain = np.zeros((RAIN_BUDGET, 4), dtype=np.float64)
        self._rain[:, 0] = rng.uniform(0.0, 1.0, RAIN_BUDGET)
        self._rain[:, 1] = rng.uniform(0.0, 1.0, RAIN_BUDGET)
        self._rain[:, 2] = rng.uniform(0.6, 1.4, RAIN_BUDGET)
        self._rain[:, 3] = rng.uniform(10.0, 22.0, RAIN_BUDGET)
        self._halo_pixmap: QPixmap | None = None

    # ------------------------------------------------------------------ nuit

    def paint_night(self, painter: QPainter, clock, sw: int, sh: int):
        if clock is None:
            return
        light = float(getattr(clock, "light", 1.0))
        if light >= 0.995:
            return
        idx = max(0, min(31, int(light * 31)))
        color = self._night[idx]
        if color.alpha() > 0:
            painter.fillRect(0, 0, sw, sh, color)

    # ------------------------------------------------------------------ feu

    def _halo(self) -> QPixmap:
        if self._halo_pixmap is not None:
            return self._halo_pixmap
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        gradient = QRadialGradient(32.0, 32.0, 32.0)
        gradient.setColorAt(0.0, QColor(255, 196, 96, 150))
        gradient.setColorAt(0.5, QColor(255, 120, 40, 60))
        gradient.setColorAt(1.0, QColor(255, 80, 20, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(gradient))
        painter.drawRect(0, 0, 64, 64)
        painter.end()
        self._halo_pixmap = pixmap
        return pixmap

    def paint_fire_glow(self, painter: QPainter, transform, sim, sw: int, sh: int):
        fire = getattr(sim.w, "fire", None)
        if fire is None:
            return
        x0, y0, x1, y1 = transform.visible_tiles(TILE, GRID, sw, sh)
        x0, y0 = max(0, int(x0)), max(0, int(y0))
        x1, y1 = min(int(fire.shape[1]), int(x1)), min(int(fire.shape[0]), int(y1))
        if x1 <= x0 or y1 <= y0:
            return
        ys, xs = np.nonzero(fire[y0:y1, x0:x1] > 0)
        if ys.size == 0:
            return
        halo = self._halo()
        tick = int(getattr(sim.w, "tick", 0))
        zoom = transform.zoom
        ysq = transform.ys
        for ty, tx in list(zip(y0 + ys, x0 + xs))[:FIRE_CELL_BUDGET]:
            sx, sy = transform.to_screen((int(tx) + 0.5) * TILE,
                                         (int(ty) + 0.5) * TILE)
            flicker = 1.0 + 0.12 * math.sin(tick * 0.7 + int(tx) * 1.3 + int(ty) * 2.1)
            d = 3.0 * TILE * zoom * flicker
            painter.drawPixmap(
                QRectF(sx - d / 2.0, sy - d * ysq / 2.0, d, d * ysq),
                halo, QRectF(halo.rect()))

    # ------------------------------------------------------------------ pluie

    def paint_rain(self, painter: QPainter, clock, tick: int, sw: int, sh: int,
                   zoom: float):
        if clock is None or zoom < 0.4:
            return
        rain = float(getattr(clock, "rain", 0.0))
        if rain <= 0.05:
            return
        wind = getattr(clock, "wind", (0.0, 0.0))
        wx = float(wind[0]) if wind else 0.0
        painter.setPen(QPen(QColor(170, 200, 235, int(60 + 90 * min(1.0, rain))), 1))
        for i in range(RAIN_BUDGET):
            fx = (self._rain[i, 0] + tick * 0.013 * self._rain[i, 2]) % 1.0
            fy = (self._rain[i, 1] + tick * 0.031 * self._rain[i, 2]) % 1.0
            x = fx * sw
            y = fy * sh
            length = self._rain[i, 3]
            painter.drawLine(QPointF(x, y),
                             QPointF(x + wx * length * 0.6, y + length))

    # ------------------------------------------------------------------ foudre

    def paint_lightning(self, painter: QPainter, clock, tick: int,
                        sw: int, sh: int):
        if clock is None:
            return
        last = int(getattr(clock, "lightning_tick", -10))
        if 0 <= tick - last < 3:
            painter.fillRect(0, 0, sw, sh, QColor(240, 244, 255, 90))

    # ------------------------------------------------------------------ tout

    def paint(self, painter: QPainter, transform, sim, sw: int, sh: int):
        clock = getattr(sim, "clock", None)
        tick = int(getattr(sim.w, "tick", 0))
        self.paint_night(painter, clock, sw, sh)
        self.paint_fire_glow(painter, transform, sim, sw, sh)
        self.paint_rain(painter, clock, tick, sw, sh, transform.zoom)
        self.paint_lightning(painter, clock, tick, sw, sh)
