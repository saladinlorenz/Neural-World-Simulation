"""MapView — QWidget de rendu carte avec QPainter."""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from game.mapapi import MapTransform, map_visible_data
from game.config import GRID, TILE, CLAN_COLORS
from ui_qt.studio.world_overlay import WorldOverlay


class MapView(QWidget):
    """Widget de carte rendue avec QPainter."""

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.transform = MapTransform(zoom=0.25, tilt=55.0)
        self.setMinimumSize(400, 300)
        self._pan_start = None
        self._painting = None
        self._data = {}
        self._overlay = WorldOverlay()
        self._overlay_mode = "normal"
        self.setMouseTracking(True)

    def set_transform(self, transform: MapTransform):
        self.transform = transform
        self.update()

    def set_overlay_mode(self, mode):
        self._overlay_mode = mode
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()

        # Fond
        painter.fillRect(0, 0, w, h, QColor(12, 14, 20))

        # Obtenir les données de carte
        sim = self.controller.sim
        self._data = map_visible_data(sim, self.transform, w, h)

        # Dessiner le terrain
        self._draw_terrain(painter, w, h)

        # Dessiner les entités
        self._draw_entities(painter)

        # Dessiner la grille (optionnel)

        # --- Legend overlay (bottom-left, drawn last) ---
        self._draw_legend(painter)

        # Overlay
        if self._overlay_mode != "normal" and self._data:
            self._overlay.paint(painter, self.transform, self._get_sim_ref(), self._overlay_mode)

        # Minimap
        if self._data:
            self._draw_minimap(painter)

        painter.end()

    def _draw_terrain(self, painter, w, h):
        """Dessine les tuiles de terrain."""
        for tile in self._data.get("terrain", []):
            tx, ty = tile["tx"], tile["ty"]
            sx, sy = self.transform.to_screen(tx * TILE, ty * TILE)

            # Taille de la tuile à l'écran
            ts = max(2, int(TILE * self.transform.zoom))

            if tile["water"]:
                color = QColor(46, 92, 158)
            elif tile["blocked"]:
                color = QColor(128, 118, 106)
            elif tile["land"]:
                color = QColor(86, 150, 62)
            else:
                color = QColor(46, 60, 80)

            painter.fillRect(int(sx), int(sy), ts, ts, color)

            # Feu
            if tile["fire"] > 0:
                alpha = min(200, int(tile["fire"] * 80))
                painter.fillRect(int(sx), int(sy), ts, ts,
                                 QColor(220, 120, 40, alpha))

    def _draw_entities(self, painter):
        """Dessine agents, moutons, monstres."""
        font = QFont("Segoe UI", 8)
        painter.setFont(font)

        # Agents
        for ag in self._data.get("agents", []):
            sx, sy = ag["sx"], ag["sy"]
            color_str = ag["color"]
            r, g, b = CLAN_COLORS.get(color_str, (150, 150, 150))
            painter.setBrush(QBrush(QColor(r, g, b)))
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.drawEllipse(QPointF(sx, sy), 6, 6)

            # Nom
            painter.setPen(QPen(QColor(255, 255, 255)))
            painter.drawText(QPointF(sx + 8, sy - 4), str(ag.get("eid", "")))

        # Sheep
        painter.setBrush(QBrush(QColor(234, 236, 240)))
        for sh in self._data.get("sheep", []):
            painter.drawEllipse(QPointF(sh["sx"], sh["sy"]), 4, 4)

        # Monsters
        painter.setBrush(QBrush(QColor(180, 60, 60)))
        for m in self._data.get("monsters", []):
            painter.drawRect(QPointF(m["sx"] - 4, m["sy"] - 4), 8, 8)

    def _draw_legend(self, painter):
        """Draw a semi-transparent legend box in the bottom-left corner."""
        items = [
            ("Eau (water)", QColor(52, 152, 219)),
            ("Terre (land)", QColor(39, 174, 96)),
            ("Mur (wall)", QColor(230, 126, 34)),
            ("Feu (fire)", QColor(231, 76, 60)),
            ("Agent", QColor(0, 0, 0), "ellipse"),
            ("Mouton", QColor(234, 236, 240), "rect"),
            ("Monstre", QColor(180, 60, 60), "rect"),
        ]

        font = QFont("Segoe UI", 9)
        painter.setFont(font)
        fm = painter.fontMetrics()

        # Measure label widths to compute box width
        max_label_w = 0
        for entry in items:
            tw = fm.horizontalAdvance(entry[0])
            if tw > max_label_w:
                max_label_w = tw

        box_w = 20 + 16 + 8 + max_label_w + 12
        box_h = 12 + len(items) * (fm.height() + 6) + 8
        margin = 20
        bx = margin
        by = self.height() - margin - box_h

        # Semi-transparent background
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.setBrush(QBrush(QColor(20, 20, 30, 180)))
        painter.drawRect(bx, by, box_w, box_h)

        y = by + 12
        for entry in items:
            label = entry[0]
            color = entry[1]
            shape = entry[2] if len(entry) > 2 else "rect"

            sw = 16
            sh = 12
            sx = bx + 10
            sy = y - sh // 2

            painter.setPen(QPen(QColor(40, 40, 40)))
            painter.setBrush(QBrush(color))
            if shape == "ellipse":
                painter.drawEllipse(QPointF(sx + sw / 2, sy + sh / 2),
                                    sw / 2, sh / 2)
            else:
                painter.drawRect(sx, sy, sw, sh)

            painter.setPen(QPen(QColor(230, 230, 230)))
            painter.drawText(QPointF(bx + 10 + 16 + 8, y + fm.ascent() / 2), label)

            y += fm.height() + 6

    def _get_sim_ref(self):
        """Get simulation reference for overlay rendering."""
        return getattr(self.controller, 'sim', None)

    def _draw_minimap(self, painter):
        """Draw a minimap in the bottom-right corner."""
        mm_w, mm_h = 120, 120
        view_w = self.width()
        view_h = self.height()
        x0 = view_w - mm_w - 20
        y0 = view_h - mm_h - 20

        # Background
        painter.setBrush(QColor(20, 20, 30, 180))
        painter.setPen(QPen(QColor(100, 100, 120), 1))
        painter.drawRect(x0, y0, mm_w, mm_h)

        world_size = GRID * TILE
        scale_x = mm_w / world_size
        scale_y = mm_h / world_size

        # Draw terrain simplified
        tiles = self._data.get("terrain", [])
        for tile in tiles:
            tx = tile.get("tx", 0)
            ty = tile.get("ty", 0)
            px = x0 + int(tx * TILE * scale_x)
            py = y0 + int(ty * TILE * scale_y)
            pw = max(1, int(TILE * scale_x))
            ph = max(1, int(TILE * scale_y))

            if tile.get("water"):
                color = QColor(52, 152, 219)
            elif tile.get("blocked"):
                color = QColor(230, 126, 34)
            elif tile.get("land"):
                color = QColor(39, 174, 96)
            else:
                color = QColor(86, 150, 62)

            painter.setBrush(color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(px, py, pw, ph)

        # Draw agents
        for a in self._data.get("agents", []):
            px = x0 + int(a.get("sx", 0) * scale_x)
            py = y0 + int(a.get("sy", 0) * scale_y)
            painter.setBrush(QColor(255, 255, 255))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(px - 1, py - 1, 3, 3)

        # Draw viewport rectangle
        vx = x0 + int(self.transform.x * scale_x)
        vy = y0 + int(self.transform.y * scale_y)
        vw = int((view_w / self.transform.zoom) * scale_x)
        vh = int((view_h / (self.transform.zoom * self.transform.ys)) * scale_y)
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(vx, vy, vw, vh)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self._pan_start = event.pos()
        elif event.button() == Qt.MouseButton.LeftButton:
            wx, wy = self.transform.to_world(event.x(), event.y())
            tx, ty = int(wx // TILE), int(wy // TILE)
            mode = self.controller.ui_state.active_mode

            if mode == "inspect":
                self.controller.execute({"kind": "select_tile", "tx": tx, "ty": ty})
                # Inspecter agent le plus proche
                best, bd = None, (TILE * 3) ** 2
                for a in self.controller.sim.agents:
                    if not a.alive:
                        continue
                    d2 = (a.x - wx) ** 2 + (a.y - wy) ** 2
                    if d2 <= bd:
                        best, bd = a, d2
                if best:
                    self.controller.execute({"kind": "select_agent", "eid": best.eid})
            elif mode == "agent":
                self.controller.execute({
                    "kind": "spawn_agent",
                    "x": wx, "y": wy,
                })
            elif mode == "sheep":
                self.controller.execute({"kind": "spawn_sheep", "x": wx, "y": wy})
            elif mode == "monster":
                self.controller.execute({"kind": "spawn_monster", "x": wx, "y": wy})
            elif mode in ("water", "land", "wall", "carve", "restore"):
                radius = self.controller.ui_state.brush_size
                self.controller.execute({
                    "kind": "paint_tile", "tx": tx, "ty": ty,
                    "mode": mode, "radius": radius,
                })
            elif mode == "erase":
                self.controller.execute({"kind": "erase_tile", "tx": tx, "ty": ty})
            elif mode == "place":
                aid = self.controller.ui_state.selected_asset_id
                if aid is not None:
                    self.controller.execute({
                        "kind": "place_asset", "tx": tx, "ty": ty, "aid": aid,
                    })
            elif mode == "floor":
                aid = self.controller.ui_state.selected_asset_id
                if aid is not None:
                    self.controller.execute({
                        "kind": "set_floor", "tx": tx, "ty": ty, "aid": aid,
                    })
            elif mode == "block":
                mat = self.controller.ui_state.block_material
                self.controller.execute({
                    "kind": "build_block", "tx": tx, "ty": ty, "material": mat,
                })

            self._painting = (tx, ty)
            self.update()

    def mouseMoveEvent(self, event):
        if self._pan_start is not None:
            dx = event.x() - self._pan_start.x()
            dy = event.y() - self._pan_start.y()
            self.transform.x -= dx / self.transform.zoom
            self.transform.y -= dy / (self.transform.zoom * self.transform.ys)
            world_size = GRID * TILE
            self.transform.clamp(world_size)
            self._pan_start = event.pos()
            self.update()
        elif self._painting is not None:
            wx, wy = self.transform.to_world(event.x(), event.y())
            tx, ty = int(wx // TILE), int(wy // TILE)
            if (tx, ty) != self._painting:
                mode = self.controller.ui_state.active_mode
                if mode in ("water", "land", "wall", "carve", "restore"):
                    radius = self.controller.ui_state.brush_size
                    self.controller.execute({
                        "kind": "paint_tile", "tx": tx, "ty": ty,
                        "mode": mode, "radius": radius,
                    })
                    self._painting = (tx, ty)
                    self.update()
                elif mode == "erase":
                    self.controller.execute({"kind": "erase_tile", "tx": tx, "ty": ty})
                    self._painting = (tx, ty)
                    self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self._pan_start = None
        if event.button() == Qt.MouseButton.LeftButton:
            self._painting = None

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        factor = 1.1 if delta > 0 else 0.9
        old_zoom = self.transform.zoom
        new_zoom = max(0.05, min(6.0, old_zoom * factor))
        self.transform.set_zoom(new_zoom, (event.x(), event.y()),
                                self.width(), self.height())
        self.update()
