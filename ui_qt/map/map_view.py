from __future__ import annotations

import math
from typing import Optional

from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtGui import (
    QColor,
    QBrush,
    QFont,
    QImage,
    QPainter,
    QPen,
)
from PyQt6.QtWidgets import QWidget

from game.config import CLAN_COLORS, GRID, TILE
from game.mapapi import MapTransform
from game.mapcache import TerrainCache
from ui_qt.studio.world_overlay import WorldOverlay


TERRAINGREEN = QColor(86, 150, 62)
WATER = QColor(46, 92, 158)
BLOCKED = QColor(128, 118, 106)
DARK = QColor(12, 14, 20)
MINIMAP_BG = QColor(20, 24, 32, 220)


class MapView(QWidget):
    """Carte Qt réactive avec terrain mis en cache.

    Le terrain est statique entre deux modifications.
    Les entités mobiles restent dessinées séparément.
    """

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.transform = MapTransform(zoom=0.75, tilt=55.0)
        self._sync_transform_from_controller()

        self.panstart: Optional[QPointF] = None
        self.painting: Optional[tuple[int, int]] = None
        self.data = None

        self.overlay = WorldOverlay()
        self.overlaymode = "normal"

        self.terrain_cache = TerrainCache(max_size=1600)
        self.terrain_qimage: Optional[QImage] = None
        self.terrain_qkey = None
        self.minimap_qimage: Optional[QImage] = None
        self.minimap_qkey = None

        self.debug_no_minimap = False
        self.debug_no_overlay = False
        self.debug_show_grid = False

        self.setMouseTracking(True)
        self.setMinimumSize(400, 300)

    # ------------------------------------------------------------------
    # Caméra
    # ------------------------------------------------------------------

    def _sync_transform_from_controller(self):
        camera = getattr(self.controller, "camera", None)
        if camera is None:
            return

        for name in ("x", "y", "zoom", "tilt"):
            if hasattr(camera, name) and hasattr(self.transform, name):
                setattr(self.transform, name, float(getattr(camera, name)))

    def _sync_controller_from_transform(self):
        camera = getattr(self.controller, "camera", None)
        if camera is None:
            return

        for name in ("x", "y", "zoom", "tilt"):
            if hasattr(camera, name) and hasattr(self.transform, name):
                setattr(camera, name, float(getattr(self.transform, name)))

    # ------------------------------------------------------------------
    # Cache images
    # ------------------------------------------------------------------

    @staticmethod
    def _pil_to_qimage(image) -> QImage:
        rgba = image.convert("RGBA")
        raw = rgba.tobytes("raw", "RGBA")
        qimage = QImage(
            raw,
            rgba.width,
            rgba.height,
            rgba.width * 4,
            QImage.Format.Format_RGBA8888,
        )
        return qimage.copy()

    @staticmethod
    def _rgb_to_qimage(rgb) -> QImage:
        import numpy as np

        rgb = np.ascontiguousarray(rgb, dtype=np.uint8)
        height, width, channels = rgb.shape
        if channels != 3:
            raise ValueError("RGB attendu sous la forme H,W,3")

        qimage = QImage(
            rgb.data,
            width,
            height,
            width * 3,
            QImage.Format.Format_RGB888,
        )
        return qimage.copy()

    def invalidate_terrain_cache(self):
        self.terrain_cache.invalidate_all()
        self.terrain_qimage = None
        self.terrain_qkey = None
        self.minimap_qimage = None
        self.minimap_qkey = None
        self.update()

    def _terrain_qkey_for_world(self):
        world = self.controller.sim.w
        gen = getattr(world, "gen", None)
        return (
            int(world.g),
            int(getattr(gen, "version", 0)) if gen is not None else 0,
            bool(gen is not None),
        )

    def _minimap_qkey_for_world(self):
        world = self.controller.sim.w
        gen = getattr(world, "gen", None)
        return (
            int(world.g),
            int(getattr(gen, "version", 0)) if gen is not None else 0,
        )

    def ensure_terrain_qimage(self):
        key = self._terrain_qkey_for_world()
        if self.terrain_qimage is not None and self.terrain_qkey == key:
            return

        cached = self.terrain_cache.build_terrain(self.controller.sim.w)
        self.terrain_qimage = self._pil_to_qimage(cached.image)
        self.terrain_qkey = key

    def ensure_minimap_qimage(self):
        key = self._minimap_qkey_for_world()
        if self.minimap_qimage is not None and self.minimap_qkey == key:
            return

        cached = self.terrain_cache.build_minimap(self.controller.sim.w, 192)
        self.minimap_qimage = self._pil_to_qimage(cached.image)
        self.minimap_qkey = key

    # ------------------------------------------------------------------
    # Peinture principale
    # ------------------------------------------------------------------

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        try:
            painter.fillRect(self.rect(), DARK)

            self.ensure_terrain_qimage()
            self.draw_cached_terrain(painter)
            self.draw_entities(painter)

            if not self.debug_no_overlay and self.overlaymode != "normal":
                sim = self.controller.sim
                self.overlay.paint(
                    painter,
                    self.transform,
                    sim,
                    self.overlaymode,
                )

            self.draw_legend(painter)

            if not self.debug_no_minimap:
                self.ensure_minimap_qimage()
                self.draw_minimap(painter)

        finally:
            painter.end()

    def draw_cached_terrain(self, painter: QPainter):
        if self.terrain_qimage is None:
            return

        world_size = float(self.controller.sim.w.g * TILE)
        sx, sy = self.transform.to_screen(0.0, 0.0)

        width = max(1, int(round(world_size * self.transform.zoom)))
        height = max(
            1,
            int(round(world_size * self.transform.zoom * self.transform.ys)),
        )

        painter.drawImage(QRectF(sx, sy, width, height), self.terrain_qimage)

    # ------------------------------------------------------------------
    # Entités
    # ------------------------------------------------------------------

    def draw_entities(self, painter: QPainter):
        sim = self.controller.sim
        font = QFont("Segoe UI", 8)
        painter.setFont(font)

        drawables = []

        for agent in sim.agents:
            if agent.alive:
                drawables.append((float(agent.y), 2, "agent", agent))

        for sheep in sim.sheep:
            if sheep.alive:
                drawables.append((float(sheep.y), 1, "sheep", sheep))

        for monster in sim.monsters:
            if monster.alive:
                drawables.append((float(monster.y), 1, "monster", monster))

        for item in getattr(sim.w, "items", []):
            drawables.append((float(getattr(item, "y", 0.0)), 0, "item", item))

        drawables.sort(key=lambda value: (value[0], value[1]))

        for _, _, kind, entity in drawables:
            if kind == "agent":
                self.draw_agent(painter, entity)
            elif kind == "sheep":
                self.draw_sheep(painter, entity)
            elif kind == "monster":
                self.draw_monster(painter, entity)
            else:
                self.draw_item(painter, entity)

    def _visible(self, sx, sy, margin=50):
        return (
            -margin <= sx <= self.width() + margin
            and -margin <= sy <= self.height() + margin
        )

    def draw_agent(self, painter: QPainter, agent):
        sx, sy = self.transform.to_screen(agent.x, agent.y)
        if not self._visible(sx, sy):
            return

        color_key = str(getattr(agent, "color", "gray"))
        rgb = CLAN_COLORS.get(color_key, (150, 150, 150))
        color = QColor(*rgb)

        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.setBrush(QBrush(color))
        painter.drawEllipse(QPointF(sx, sy - 4), 6, 6)

        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.drawText(QPointF(sx + 8, sy - 5), str(agent.eid))

        selected = getattr(
            self.controller.ui_state,
            "selected_agent_eid",
            None,
        ) == agent.eid
        if selected:
            painter.setPen(QPen(QColor(255, 220, 80), 2))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(QPointF(sx, sy - 4), 10, 10)

    def draw_sheep(self, painter: QPainter, sheep):
        sx, sy = self.transform.to_screen(sheep.x, sheep.y)
        if not self._visible(sx, sy):
            return

        painter.setPen(QPen(QColor(60, 60, 60), 1))
        painter.setBrush(QBrush(QColor(234, 236, 240)))
        painter.drawEllipse(QPointF(sx, sy - 3), 5, 4)

    def draw_monster(self, painter: QPainter, monster):
        sx, sy = self.transform.to_screen(monster.x, monster.y)
        if not self._visible(sx, sy):
            return

        painter.setPen(QPen(QColor(70, 20, 20), 1))
        painter.setBrush(QBrush(QColor(180, 60, 60)))
        painter.drawRect(QRectF(sx - 5, sy - 10, 10, 10))

    def draw_item(self, painter: QPainter, item):
        sx, sy = self.transform.to_screen(
            float(getattr(item, "x", 0.0)),
            float(getattr(item, "y", 0.0)),
        )
        if not self._visible(sx, sy):
            return

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(210, 180, 80)))
        painter.drawEllipse(QPointF(sx, sy - 2), 3, 3)

    # ------------------------------------------------------------------
    # Légende et minimap
    # ------------------------------------------------------------------

    def draw_legend(self, painter: QPainter):
        painter.setFont(QFont("Segoe UI", 9))
        rect = QRectF(16, self.height() - 150, 190, 126)

        painter.setPen(QPen(QColor(0, 0, 0, 160), 1))
        painter.setBrush(QBrush(QColor(20, 20, 30, 190)))
        painter.drawRoundedRect(rect, 8, 8)

        rows = [
            ("Terrain", TERRAINGREEN),
            ("Eau", WATER),
            ("Montagne", BLOCKED),
            ("Habitant", QColor(150, 150, 150)),
            ("Mouton", QColor(234, 236, 240)),
            ("Prédateur", QColor(180, 60, 60)),
        ]

        y = rect.top() + 20
        for label, color in rows:
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(QRectF(rect.left() + 12, y - 10, 14, 14))
            painter.setPen(QPen(QColor(230, 230, 230), 1))
            painter.drawText(QPointF(rect.left() + 34, y + 2), label)
            y += 17

    def draw_minimap(self, painter: QPainter):
        if self.minimap_qimage is None:
            return

        size = 192
        x0 = self.width() - size - 20
        y0 = self.height() - size - 20
        rect = QRectF(x0, y0, size, size)

        painter.setPen(QPen(QColor(100, 100, 120), 1))
        painter.setBrush(QBrush(MINIMAP_BG))
        painter.drawRect(rect)
        painter.drawImage(rect, self.minimap_qimage)

        world_size = max(1.0, self.controller.sim.w.g * TILE)
        scale_x = size / world_size
        scale_y = size / world_size

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(255, 255, 255)))

        for agent in self.controller.sim.agents:
            if not agent.alive:
                continue
            px = x0 + float(agent.x) * scale_x
            py = y0 + float(agent.y) * scale_y
            painter.drawEllipse(QPointF(px, py), 2, 2)

        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        vx = x0 + self.transform.x * scale_x
        vy = y0 + self.transform.y * scale_y
        vw = self.width() / max(self.transform.zoom, 0.01) * scale_x
        vh = self.height() / max(
            self.transform.zoom * max(self.transform.ys, 0.01),
            0.01,
        ) * scale_y
        painter.drawRect(QRectF(vx, vy, vw, vh))

    # ------------------------------------------------------------------
    # Interactions
    # ------------------------------------------------------------------

    def set_overlay_mode(self, mode: str):
        self.overlaymode = str(mode)
        self.update()

    def invalidate_all_caches(self):
        self.terrain_cache.invalidate_all()
        self.terrain_qimage = None
        self.terrain_qkey = None
        self.minimap_qimage = None
        self.minimap_qkey = None
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.panstart = event.position()
            return

        if event.button() != Qt.MouseButton.LeftButton:
            return

        wx, wy = self.transform.to_world(
            event.position().x(),
            event.position().y(),
        )
        tx, ty = int(wx // TILE), int(wy // TILE)
        mode = getattr(self.controller.ui_state, "active_mode", "inspect")

        if mode == "inspect":
            self.controller.execute({
                "kind": "select_tile",
                "tx": tx,
                "ty": ty,
            })
            self.select_nearest_agent(wx, wy)

        elif mode == "agent":
            self.controller.execute({
                "kind": "spawn_agent",
                "x": wx,
                "y": wy,
            })

        elif mode == "sheep":
            self.controller.execute({
                "kind": "spawn_sheep",
                "x": wx,
                "y": wy,
            })

        elif mode == "monster":
            self.controller.execute({
                "kind": "spawn_monster",
                "x": wx,
                "y": wy,
            })

        else:
            self.painting = (tx, ty)
            self.apply_tool(tx, ty)

        self.update()

    def select_nearest_agent(self, wx, wy):
        best = None
        best_distance = float("inf")

        for agent in self.controller.sim.agents:
            if not agent.alive:
                continue
            distance = (agent.x - wx) ** 2 + (agent.y - wy) ** 2
            if distance < best_distance:
                best = agent
                best_distance = distance

        if best is not None and best_distance <= (TILE * 3) ** 2:
            self.controller.execute({
                "kind": "select_agent",
                "eid": best.eid,
            })

    def apply_tool(self, tx, ty):
        mode = getattr(self.controller.ui_state, "active_mode", "inspect")
        radius = getattr(self.controller.ui_state, "brush_size", 3)

        if mode in {"water", "land", "wall"}:
            self.controller.execute({
                "kind": "paint_tile",
                "tx": tx,
                "ty": ty,
                "mode": mode,
                "radius": radius,
            })
            self.invalidate_all_caches()

        elif mode in {"carve", "restore"}:
            self.controller.execute({
                "kind": mode,
                "tx": tx,
                "ty": ty,
                "radius": radius,
            })
            self.invalidate_all_caches()

        elif mode == "erase":
            self.controller.execute({
                "kind": "erase_tile",
                "tx": tx,
                "ty": ty,
            })
            self.invalidate_all_caches()

    def mouseMoveEvent(self, event):
        if self.panstart is not None:
            current = event.position()
            dx = current.x() - self.panstart.x()
            dy = current.y() - self.panstart.y()

            self.transform.x -= dx / max(self.transform.zoom, 0.01)
            self.transform.y -= dy / max(
                self.transform.zoom * max(self.transform.ys, 0.01),
                0.01,
            )
            self.transform.clamp(GRID * TILE, self.width(), self.height())
            self._sync_controller_from_transform()
            self.panstart = current
            self.update()
            return

        if self.painting is not None:
            wx, wy = self.transform.to_world(
                event.position().x(),
                event.position().y(),
            )
            tx, ty = int(wx // TILE), int(wy // TILE)
            if (tx, ty) != self.painting:
                self.painting = (tx, ty)
                self.apply_tool(tx, ty)
                self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.panstart = None
        elif event.button() == Qt.MouseButton.LeftButton:
            self.painting = None

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        factor = 1.1 if delta > 0 else 0.9
        new_zoom = max(0.08, min(4.0, self.transform.zoom * factor))
        self.transform.set_zoom(
            new_zoom,
            (int(event.position().x()), int(event.position().y())),
            self.width(),
            self.height(),
        )
        self.transform.clamp(GRID * TILE, self.width(), self.height())
        self._sync_controller_from_transform()
        self.update()
