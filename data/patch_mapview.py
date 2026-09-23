import io

p = "ui_qt/map/map_view.py"
src = io.open(p, encoding="utf-8", newline="").read()


def rep(old, new, count=1):
    global src
    assert src.count(old) == count, (src.count(old), old[:70])
    src = src.replace(old, new)


rep("""from __future__ import annotations

import math
from typing import Optional
""",
"""from __future__ import annotations

import math
from typing import Optional

import numpy as np
""")

rep("""from game.mapcache import TerrainCache
from ui_qt.asset_cache import QtAssetCache
from ui_qt.qtimage import pil_to_qimage
""",
"""from game.mapcache import CHUNK, TerrainCache, TerrainChunkCache
from ui_qt.asset_cache import QtAssetCache
from ui_qt.qtimage import pil_to_qimage, rgb_to_qimage
""")

rep("""TERRAINGREEN = QColor(86, 150, 62)""",
"""#: Au-dela de ce zoom, le terrain global (1 px pour ~1.6 tuile) est remplace
#: par le rendu detaille par chunks : 1 px par tuile, ombrage de pente inclus.
CHUNK_ZOOM = 0.5

TERRAINGREEN = QColor(86, 150, 62)""")

rep("""        self.terrain_cache = TerrainCache(max_size=1600)
        self.terrain_qimage: Optional[QImage] = None
        self.terrain_qkey = None
        self.minimap_qimage: Optional[QImage] = None
        self.minimap_qkey = None
""",
"""        #: Terrain detaille par chunks de 64 tuiles, rendu a la demande.
        self.chunk_cache = TerrainChunkCache()
        self.chunk_qimages: dict[tuple, QImage] = {}

        self.terrain_cache = TerrainCache(max_size=1600)
        self.terrain_qimage: Optional[QImage] = None
        self.terrain_qkey = None
        self.minimap_qimage: Optional[QImage] = None
        self.minimap_qkey = None
        self.show_legend = True
""")

rep("""    def invalidate_terrain_cache(self):
        self.terrain_cache.invalidate_all()
        self.terrain_qimage = None""",
"""    def invalidate_terrain_cache(self):
        self.terrain_cache.invalidate_all()
        self.chunk_qimages.clear()
        self.terrain_qimage = None""")

rep("""            self.ensure_terrain_qimage()
            self.draw_cached_terrain(painter)
            self.draw_entities(painter)
""",
"""            if self.transform.zoom >= CHUNK_ZOOM:
                self.draw_chunk_terrain(painter)
            else:
                self.ensure_terrain_qimage()
                self.draw_cached_terrain(painter)
            self.draw_entities(painter)
            if self.debug_show_grid:
                self.draw_grid(painter)
""")

rep("""            self.draw_legend(painter)
""",
"""            if self.show_legend:
                self.draw_legend(painter)
""")

rep("""        painter.drawImage(QRectF(sx, sy, width, height), self.terrain_qimage)

    # ------------------------------------------------------------------
    # Entités""",
"""        painter.drawImage(QRectF(sx, sy, width, height), self.terrain_qimage)

    def draw_chunk_terrain(self, painter: QPainter):
        \"\"\"Terrain detaille : un chunk de CHUNK x CHUNK tuiles par QImage.

        Le terrain global reste utilise sous ``CHUNK_ZOOM`` (et pour la
        minimap) ; au-dela, chaque chunk est rendu en resolution native puis
        blite a sa place monde exacte, ecrase par ``cos(tilt)`` comme le sol.
        \"\"\"
        world = self.controller.sim.w
        x0, y0, x1, y1 = self.transform.visible_tiles(
            TILE, GRID, self.width(), self.height())
        zoom = self.transform.zoom
        ys = self.transform.ys
        cx0, cy0 = x0 // CHUNK, y0 // CHUNK
        cx1 = max(cx0, (x1 - 1) // CHUNK)
        cy1 = max(cy0, (y1 - 1) // CHUNK)

        for cy in range(cy0, cy1 + 1):
            for cx in range(cx0, cx1 + 1):
                rgb = self.chunk_cache.chunk_rgb(world, cx, cy)
                if rgb.shape[0] <= 1 or rgb.shape[1] <= 1:
                    continue
                key = self.chunk_cache.key(world, cx, cy)
                qimage = self.chunk_qimages.get(key)
                if qimage is None:
                    qimage = rgb_to_qimage(rgb)
                    self.chunk_qimages[key] = qimage
                    while len(self.chunk_qimages) > 256:
                        self.chunk_qimages.pop(next(iter(self.chunk_qimages)))
                sx, sy = self.transform.to_screen(cx * CHUNK * TILE,
                                                  cy * CHUNK * TILE)
                painter.drawImage(
                    QRectF(sx, sy,
                           rgb.shape[1] * TILE * zoom,
                           rgb.shape[0] * TILE * zoom * ys),
                    qimage)

    def draw_grid(self, painter: QPainter):
        \"\"\"Une ligne par tuile - seulement si le zoom le rend lisible.\"\"\"
        if self.transform.zoom < 0.6:
            return
        x0, y0, x1, y1 = self.transform.visible_tiles(
            TILE, GRID, self.width(), self.height())
        painter.setPen(QPen(QColor(255, 255, 255, 26), 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        for tx in range(x0, x1 + 1):
            sx, sy0 = self.transform.to_screen(tx * TILE, y0 * TILE)
            _, sy1 = self.transform.to_screen(tx * TILE, y1 * TILE)
            painter.drawLine(QPointF(sx, sy0), QPointF(sx, sy1))
        for ty in range(y0, y1 + 1):
            sx0, sy = self.transform.to_screen(x0 * TILE, ty * TILE)
            sx1, _ = self.transform.to_screen(x1 * TILE, ty * TILE)
            painter.drawLine(QPointF(sx0, sy), QPointF(sx1, sy))

    # ------------------------------------------------------------------
    # Entités""")

rep("""        if (x1 - x0) * (y1 - y0) <= self.CONTENT_TILE_BUDGET:
            drawables.extend(self._collect_contents(w, am, x0, y0, x1, y1))
""",
"""        if (x1 - x0) * (y1 - y0) <= self.CONTENT_TILE_BUDGET:
            drawables.extend(self._collect_contents(w, am, x0, y0, x1, y1))
            drawables.extend(self._collect_stumps(w, am, x0, y0, x1, y1))
        drawables.extend(self._collect_structures(w, am, x0, y0, x1, y1))
""")

rep("""            elif kind == "effect":
                self.draw_effect(painter, am, payload, zoom)
""",
"""            elif kind == "effect":
                self.draw_effect(painter, am, payload, zoom)
            elif kind == "stump":
                self.draw_stump(painter, am, payload, zoom)
            elif kind == "grave":
                self.draw_grave(painter, am, payload, zoom)
            elif kind == "storage":
                self.draw_storage(painter, am, payload, zoom)
            elif kind == "crop":
                self.draw_crop(painter, payload)
            elif kind == "site":
                self.draw_site(painter, payload)
""")

rep("""    def _collect_fire(self, w, am, x0, y0, x1, y1):""",
"""    def _collect_stumps(self, w, am, x0, y0, x1, y1):
        pool = am.pool("stump")
        box = self._clip_tiles(w, x0, y0, x1, y1)
        if box is None or not pool:
            return []
        x0, y0, x1, y1, _g = box
        regrow = w.regrow[y0:y1, x0:x1]
        content = w.content[y0:y1, x0:x1]
        ys, xs = np.nonzero((regrow > 0) & (content < 0))
        if ys.size == 0:
            return []
        aid = int(pool[0])
        return [((y0 + int(ty)) + 1) * float(TILE), 2, "stump",
                (int(x0 + tx), int(y0 + ty), aid))
                for ty, tx in zip(ys, xs)]

    def _collect_structures(self, w, am, x0, y0, x1, y1):
        \"\"\"Tombes, depots, cultures et chantiers - peu nombreux, en bornes.\"\"\"
        out = []
        graves = am.pool("grave")
        grave_aid = int(graves[0]) if graves else -1
        for entry in getattr(w, "cemetery", ()):
            try:
                tx, ty = int(entry[0]), int(entry[1])
                name = entry[2]
            except (IndexError, TypeError, ValueError):
                continue
            if x0 - 2 <= tx < x1 + 2 and y0 - 2 <= ty < y1 + 2:
                out.append(((ty + 1) * float(TILE), 2, "grave",
                            (tx, ty, grave_aid, name)))

        chest = self._role_aid(am, "storage")
        for (tx, ty), storage in list(getattr(w, "storages", {}).items()):
            if x0 - 2 <= tx < x1 + 2 and y0 - 2 <= ty < y1 + 2:
                out.append(((ty + 1) * float(TILE), 2, "storage",
                            (int(tx), int(ty), chest, storage)))

        for (tx, ty), plot in list(getattr(w, "crop_plots", {}).items()):
            if x0 - 2 <= tx < x1 + 2 and y0 - 2 <= ty < y1 + 2:
                out.append(((ty + 1) * float(TILE), 2, "crop",
                            (int(tx), int(ty), plot)))

        for (tx, ty), site in list(getattr(w, "sites", {}).items()):
            if x0 - 6 <= tx < x1 + 6 and y0 - 6 <= ty < y1 + 6:
                out.append(((ty + 1) * float(TILE), 2, "site",
                            (int(tx), int(ty), site)))
        return out

    def _role_aid(self, am, kind):
        cache = getattr(self, "_role_aids", None)
        if cache is None:
            cache = self._role_aids = {}
        if kind in cache:
            return cache[kind]
        aid = -1
        if kind == "storage":
            for cand in am.pool("prop"):
                name = str(getattr(am.assets[int(cand)], "name", "")).lower()
                if any(t in name for t in ("chest", "box", "barrel", "coffre")):
                    aid = int(cand)
                    break
        cache[kind] = aid
        return aid

    def _collect_fire(self, w, am, x0, y0, x1, y1):""")

rep("""    def draw_agent(self, painter: QPainter, agent):""",
"""    def draw_stump(self, painter, am, payload, zoom):
        tx, ty, aid = payload
        self._draw_grounded_sprite(
            painter, self.asset_cache.pixmap(am, aid, 0),
            (tx + 0.5) * TILE, (ty + 1.0) * TILE, zoom * 0.85)

    def draw_grave(self, painter, am, payload, zoom):
        tx, ty, aid, _name = payload
        if aid < 0:
            return
        self._draw_grounded_sprite(
            painter, self.asset_cache.pixmap(am, aid, 0),
            (tx + 0.5) * TILE, (ty + 1.0) * TILE, zoom * 0.9)

    def draw_storage(self, painter, am, payload, zoom):
        tx, ty, aid, _storage = payload
        if aid < 0:
            return
        self._draw_grounded_sprite(
            painter, self.asset_cache.pixmap(am, aid, 0),
            (tx + 0.5) * TILE, (ty + 1.0) * TILE, zoom,
            shadow=self.asset_cache.shadow(am))

    def draw_crop(self, painter, payload):
        tx, ty, plot = payload
        sx, sy = self.transform.to_screen((tx + 0.5) * TILE, (ty + 1.0) * TILE)
        if not self._visible(sx, sy):
            return
        zw = self.transform.zoom
        ys = self.transform.ys
        wpx = TILE * zw * 0.92
        hpx = TILE * zw * ys * 0.92
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(96, 74, 52)))
        painter.drawRect(QRectF(sx - wpx / 2.0, sy - hpx, wpx, hpx))
        growth = max(0.0, min(1.0, float(getattr(plot, "growth", 0.0))))
        if growth > 0.05:
            hh = hpx * (0.25 + 0.75 * growth)
            painter.setBrush(QBrush(QColor(126, 194, 84)))
            painter.drawRect(QRectF(sx - wpx * 0.32, sy - hh, wpx * 0.64, hh))

    def draw_site(self, painter, payload):
        tx, ty, site = payload
        tasks = getattr(site, "tasks", ()) or ()
        if not tasks:
            return
        xs = [int(t.tx) for t in tasks]
        ys = [int(t.ty) for t in tasks]
        wx0, wy0 = min(xs) * TILE, min(ys) * TILE
        wx1, wy1 = (max(xs) + 1) * TILE, (max(ys) + 1) * TILE
        sx0, sy0 = self.transform.to_screen(wx0, wy0)
        sx1, sy1 = self.transform.to_screen(wx1, wy1)
        if not self._visible(sx0, sy0, 200) and not self._visible(sx1, sy1, 200):
            return
        rect = QRectF(sx0, sy0, sx1 - sx0, sy1 - sy0)
        painter.setPen(QPen(QColor(255, 196, 88, 190), 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(rect)
        progress = max(0.0, min(1.0, float(site.progress())))
        bar = QRectF(rect.left(), rect.top() - 8, rect.width() * progress, 4)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(255, 196, 88, 220)))
        painter.drawRect(bar)

    def draw_agent(self, painter: QPainter, agent):""")

rep("""    def draw_legend(self, painter: QPainter):
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
""",
"""    def draw_legend(self, painter: QPainter):
        font = QFont(self.font())
        font.setPointSize(9)
        painter.setFont(font)
        rect = QRectF(16, self.height() - 170, 200, 150)

        painter.setPen(QPen(QColor(0, 0, 0, 160), 1))
        painter.setBrush(QBrush(QColor(20, 20, 30, 190)))
        painter.drawRoundedRect(rect, 8, 8)

        rows = [
            ("Terrain", TERRAINGREEN, None),
            ("Eau", WATER, None),
            ("Montagne", BLOCKED, None),
            ("Arbre", None, "tree"),
            ("Habitant", None, "agent"),
            ("Mouton", None, "sheep"),
            ("Predateur", None, "monster"),
            ("Tombe", None, "grave"),
        ]

        y = rect.top() + 20
        for label, color, sprite in rows:
            box = QRectF(rect.left() + 12, y - 12, 16, 16)
            pixmap = None if sprite is None else self._legend_pixmap(sprite)
            if pixmap is None:
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(color if sprite is None
                                        else QColor(120, 120, 120)))
                painter.drawRect(box)
            else:
                painter.drawPixmap(box, pixmap, QRectF(pixmap.rect()))
            painter.setPen(QPen(QColor(230, 230, 230), 1))
            painter.drawText(QPointF(rect.left() + 36, y + 2), label)
            y += 17

    def _legend_pixmap(self, kind):
        am = self.controller.sim.am
        aid, frame = -1, 0
        if kind == "tree":
            pool = am.pool("tree")
            aid = int(pool[0]) if pool else -1
        elif kind == "grave":
            pool = am.pool("grave")
            aid = int(pool[0]) if pool else -1
        elif kind == "sheep":
            table = getattr(am, "sheep", {}) or {}
            aid = int(next(iter(table.values()))) if table else -1
        elif kind == "monster":
            kinds = getattr(am, "monsters", {}) or {}
            table = next(iter(kinds.values()), {}) if kinds else {}
            aid = int(next(iter(table.values()))) if table else -1
        else:
            ids = am.skin_states("blue", "pawn").get("idle") or []
            aid = int(ids[0]) if ids else -1
        if aid < 0 or aid >= len(am.assets):
            return None
        return self.asset_cache.pixmap(am, aid, frame)
""")

rep("""    def invalidate_all_caches(self):
        self.terrain_cache.invalidate_all()
        self.terrain_qimage = None""",
"""    def invalidate_all_caches(self):
        self.terrain_cache.invalidate_all()
        self.chunk_cache.clear()
        self.chunk_qimages.clear()
        self.asset_cache.clear()
        self.terrain_qimage = None""")

io.open(p, "w", encoding="utf-8", newline="").write(src)
print("patched map_view")
