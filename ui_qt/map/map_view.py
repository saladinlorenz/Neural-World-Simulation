from __future__ import annotations

import math
from typing import Optional

import numpy as np

from PyQt6.QtCore import QPointF, QRectF, Qt, pyqtSignal
from PyQt6.QtGui import (
    QColor,
    QBrush,
    QFont,
    QImage,
    QPainter,
    QPen,
    QPixmap,
)
from PyQt6.QtWidgets import QWidget

from game.config import CLAN_COLORS, GRID, TILE
from game.mapapi import MapTransform
from game.mapcache import CHUNK, TerrainCache, TerrainChunkCache
from game.ui_commands import can_place
from ui_qt.asset_cache import QtAssetCache
from ui_qt.map.effects_layer import EffectsLayer
from ui_qt.qtimage import pil_to_qimage, rgb_to_qimage
from ui_qt.studio.world_overlay import WorldOverlay


#: Au-dela de ce zoom, le terrain global (1 px pour ~1.6 tuile) est remplace
#: par le rendu detaille par chunks : 1 px par tuile, ombrage de pente inclus.
CHUNK_ZOOM = 0.5

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

    #: Résultat brut de chaque commande déclenchée depuis la carte. La
    #: fenêtre principale l'affiche dans la barre d'état.
    command_result = pyqtSignal(dict)

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.transform = MapTransform(zoom=0.75, tilt=55.0)
        self._sync_transform_from_controller()

        self.panstart: Optional[QPointF] = None
        self.painting: Optional[tuple[int, int]] = None
        #: Identifiant du glisser en cours : une seule entrée d'historique
        #: par coup de pinceau, pas une par tuile traversée.
        self._stroke_group = 0
        self.data = None

        self.overlay = WorldOverlay()
        self.overlaymode = "normal"

        #: Nuit, pluie, foudre, halo de feu (Lot B.4).
        self.effects = EffectsLayer()
        #: Tilt dynamique 30-70° lie au zoom (Lot B.2). Desactive pour les
        #: captures d'ecran, qui veulent une camera exacte.
        self.auto_tilt = True
        self._minimap_drag = False

        #: Sprites du monde. Indépendant de l'état du terrain : il n'est
        #: vidé qu'au chargement d'une partie (les ``aid`` sont positionnels).
        self.asset_cache = QtAssetCache()

        #: Terrain detaille par chunks de 64 tuiles, rendu a la demande.
        self.chunk_cache = TerrainChunkCache()
        self.chunk_qimages: dict[tuple, QImage] = {}

        self.terrain_cache = TerrainCache(max_size=1600)
        self.terrain_qimage: Optional[QImage] = None
        self.terrain_qkey = None
        self.minimap_qimage: Optional[QImage] = None
        self.minimap_qkey = None
        self.show_legend = True

        self.debug_no_minimap = False
        self.debug_no_overlay = False
        self.debug_show_grid = False
        #: En mode debug seulement : identifiants et anneaux de sélection.
        self.debug_show_labels = False

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

    _pil_to_qimage = staticmethod(pil_to_qimage)

    def invalidate_terrain_cache(self):
        self.terrain_cache.invalidate_all()
        self.chunk_qimages.clear()
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
            if self.auto_tilt:
                before = self.transform.tilt
                self.transform.auto_tilt()
                if abs(self.transform.tilt - before) > 1e-4:
                    self._sync_controller_from_transform()

            painter.fillRect(self.rect(), DARK)

            if self.transform.zoom >= CHUNK_ZOOM:
                self.draw_chunk_terrain(painter)
            else:
                self.ensure_terrain_qimage()
                self.draw_cached_terrain(painter)
            self.draw_entities(painter)
            self.draw_ghost(painter)
            if self.debug_show_grid:
                self.draw_grid(painter)

            if not self.debug_no_overlay and self.overlaymode != "normal":
                sim = self.controller.sim
                self.overlay.paint(
                    painter,
                    self.transform,
                    sim,
                    self.overlaymode,
                )

            self.effects.paint(painter, self.transform, self.controller.sim,
                               self.width(), self.height())

            if self.show_legend:
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

    def draw_chunk_terrain(self, painter: QPainter):
        """Terrain detaille : un chunk de CHUNK x CHUNK tuiles par QImage.

        Le terrain global reste utilise sous ``CHUNK_ZOOM`` (et pour la
        minimap) ; au-dela, chaque chunk est rendu en resolution native puis
        blite a sa place monde exacte, ecrase par ``cos(tilt)`` comme le sol.
        """
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
        """Une ligne par tuile - seulement si le zoom le rend lisible."""
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
    # Entités
    # ------------------------------------------------------------------

    #: Au-delà de ce nombre de tuiles visibles, la passe « contenus du monde »
    #: est sautée. Une boucle Python sur les 100 000+ tuiles visibles au zoom
    #: par défaut gèle l'interface — c'est le bug historique documenté dans
    #: ``game/mapapi.py``.
    CONTENT_TILE_BUDGET = 40000

    #: ``Being.state`` (moteur) → état d'animation des skins.
    _SKIN_STATE = {
        "run": "run",
        "attack": "attack",
        "work": "work",
        "build": "build",
        "heal": "heal",
    }

    def draw_entities(self, painter: QPainter):
        """Dessine le monde vivant en vrais sprites, triés par profondeur.

        Le tri est ``(world_y, layer)`` : un habitant au nord d'un arbre passe
        derrière lui, au sud il passe devant.
        """
        sim = self.controller.sim
        w = sim.w
        am = sim.am
        zoom = self.transform.zoom

        x0, y0, x1, y1 = self.transform.visible_tiles(TILE, GRID,
                                                        self.width(), self.height())
        drawables = []

        # 2 — assets posés : arbres, rochers, structures, cultures, blocs
        if (x1 - x0) * (y1 - y0) <= self.CONTENT_TILE_BUDGET:
            drawables.extend(self._collect_contents(w, am, x0, y0, x1, y1))
            drawables.extend(self._collect_stumps(w, am, x0, y0, x1, y1))
        drawables.extend(self._collect_structures(w, am, x0, y0, x1, y1))
        # 5 — feu (au-dessus de tout le reste)
        drawables.extend(self._collect_fire(w, am, x0, y0, x1, y1))

        # 1 — objets au sol
        for item in getattr(w, "items", ()):
            drawables.append((float(getattr(item, "y", 0.0)), 1, "item", item))

        # 3 — animaux
        for sheep in sim.sheep:
            if sheep.alive:
                drawables.append((float(sheep.y), 3, "sheep", sheep))
        for monster in sim.monsters:
            if monster.alive:
                drawables.append((float(monster.y), 3, "monster", monster))

        # 4 — habitants
        for agent in sim.agents:
            if agent.alive:
                drawables.append((float(agent.y), 4, "agent", agent))

        # 5 — effets d'action (liste déjà purgée par TTL côté moteur)
        for fx in getattr(sim, "effects", ()):
            try:
                drawables.append((float(fx.get("y", 0.0)), 5, "effect", fx))
            except (TypeError, ValueError):
                continue

        drawables.sort(key=lambda value: (value[0], value[1]))

        for _, _, kind, payload in drawables:
            if kind == "content":
                self.draw_content(painter, am, payload, zoom)
            elif kind == "fire":
                self.draw_fire(painter, am, payload, zoom)
            elif kind == "agent":
                self.draw_agent(painter, payload)
            elif kind == "sheep":
                self.draw_sheep(painter, payload)
            elif kind == "monster":
                self.draw_monster(painter, payload)
            elif kind == "item":
                self.draw_item(painter, payload)
            elif kind == "effect":
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

    def _visible(self, sx, sy, margin=50):
        return (
            -margin <= sx <= self.width() + margin
            and -margin <= sy <= self.height() + margin
        )

    # ------------------------------------------------------------------
    # Collecte vectorisée
    # ------------------------------------------------------------------

    def _clip_tiles(self, w, x0, y0, x1, y1):
        g = int(w.g)
        x0, y0 = max(0, int(x0)), max(0, int(y0))
        x1, y1 = min(g, int(x1)), min(g, int(y1))
        if x1 <= x0 or y1 <= y0:
            return None
        return x0, y0, x1, y1, g

    def _collect_contents(self, w, am, x0, y0, x1, y1):
        """Anchres des assets posés dans la zone visible.

        ``World.place`` écrit l'``aid`` sur la case d'ancre (coin haut-gauche)
        et l'index plat de cette ancre dans ``owner`` sur toute l'empreinte :
        le filtre ``owner == flat`` élimine donc les doublons d'empreinte.
        """
        box = self._clip_tiles(w, x0, y0, x1, y1)
        if box is None:
            return []
        x0, y0, x1, y1, g = box

        import numpy as np

        sub = w.content[y0:y1, x0:x1]
        ys, xs = np.nonzero(sub >= 0)
        if ys.size == 0:
            return []
        owner = w.owner[y0:y1, x0:x1][ys, xs]
        tys, txs = y0 + ys, x0 + xs
        anchors = owner == tys * g + txs

        out = []
        tick = int(getattr(w, "tick", 0))
        for ty, tx, aid in zip(tys[anchors], txs[anchors], sub[ys, xs][anchors]):
            tx, ty, aid = int(tx), int(ty), int(aid)
            if not (0 <= aid < len(am.assets)):
                continue
            size = max(1, int(getattr(am.assets[aid], "size_tiles", 1) or 1))
            frames = max(1, int(getattr(am.assets[aid], "frames", 1) or 1))
            frame = ((tick // 8) + tx * 7 + ty * 13) % frames if frames > 1 else 0
            out.append(((ty + size) * float(TILE), 2, "content", (tx, ty, aid, size, frame)))
        return out

    def _collect_stumps(self, w, am, x0, y0, x1, y1):
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
        out = []
        for ty, tx in zip(ys, xs):
            out.append((((y0 + int(ty)) + 1) * float(TILE), 2, "stump",
                         (int(x0 + tx), int(y0 + ty), aid)))
        return out

    def _collect_structures(self, w, am, x0, y0, x1, y1):
        """Tombes, depots, cultures et chantiers - peu nombreux, en bornes."""
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

    def _collect_fire(self, w, am, x0, y0, x1, y1):
        fire = getattr(w, "fire", None)
        if fire is None:
            return []
        pool = getattr(am, "fx", {}).get("fire") or []
        box = self._clip_tiles(w, x0, y0, x1, y1)
        if box is None or not pool:
            return []
        x0, y0, x1, y1, _g = box

        import numpy as np

        ys, xs = np.nonzero(fire[y0:y1, x0:x1] > 0)
        if ys.size == 0:
            return []
        aid = int(pool[0])
        frames = max(1, int(getattr(am.assets[aid], "frames", 1) or 1))
        tick = int(getattr(w, "tick", 0))
        return [((int(ty) + 1) * float(TILE), 5, "fire",
                 (int(tx), int(ty), aid, ((tick // 4) + int(tx)) % frames if frames > 1 else 0))
                for ty, tx in zip(y0 + ys, x0 + xs)]

    # ------------------------------------------------------------------
    # Blit de sprites
    # ------------------------------------------------------------------

    def _draw_grounded_sprite(self, painter, pixmap, wx, wy, zoom,
                              shadow=None, alpha=1.0):
        """Billboard ancré au sol.

        Le sol est écrasé verticalement par ``cos(tilt)`` ; les sprites, eux,
        restent debout. Leur hauteur ne doit donc PAS être multipliée par
        ``transform.ys``.
        """
        if pixmap is None or pixmap.isNull():
            return False
        pw = pixmap.width() * zoom
        ph = pixmap.height() * zoom
        if pw < 0.6 or ph < 0.6:
            return False

        sx, sy = self.transform.to_screen(wx, wy)
        margin = int(max(64.0, ph))
        if not self._visible(sx, sy, margin):
            return False

        if shadow is not None and not shadow.isNull():
            sw = pw * 0.85
            sh = max(2.0, sw * 0.32)
            painter.setOpacity(0.35)
            painter.drawPixmap(QRectF(sx - sw / 2.0, sy - sh / 2.0, sw, sh),
                               shadow, QRectF(shadow.rect()))
            painter.setOpacity(1.0)

        target = QRectF(sx - pw / 2.0, sy - ph, pw, ph)
        if alpha < 1.0:
            painter.setOpacity(alpha)
        painter.drawPixmap(target, pixmap, QRectF(pixmap.rect()))
        if alpha < 1.0:
            painter.setOpacity(1.0)
        return True

    def _animation_frame(self, tick, entity, frames, fast):
        if frames <= 1:
            return 0
        step = 4 if fast else 10
        return ((int(tick) // step) + int(getattr(entity, "eid", 0))) % frames

    def draw_content(self, painter, am, payload, zoom):
        tx, ty, aid, size, frame = payload
        pixmap = self.asset_cache.pixmap(am, aid, frame)
        self._draw_grounded_sprite(
            painter, pixmap,
            (tx + size / 2.0) * TILE, (ty + size) * TILE, zoom)

    def draw_fire(self, painter, am, payload, zoom):
        tx, ty, aid, frame = payload
        pixmap = self.asset_cache.pixmap(am, aid, frame)
        self._draw_grounded_sprite(
            painter, pixmap,
            (tx + 0.5) * TILE, (ty + 1.0) * TILE, zoom, alpha=0.9)

    def draw_effect(self, painter, am, fx, zoom):
        aid = fx.get("aid")
        if aid is None:
            return
        frames = max(1, int(getattr(am.assets[int(aid)], "frames", 1) or 1)) \
            if 0 <= int(aid) < len(am.assets) else 1
        tick = int(getattr(self.controller.sim.w, "tick", 0))
        age = tick - int(fx.get("t0", tick))
        frame = (age // 3) % frames if frames > 1 else 0
        pixmap = self.asset_cache.pixmap(am, int(aid), frame)
        self._draw_grounded_sprite(painter, pixmap,
                                   float(fx.get("x", 0.0)), float(fx.get("y", 0.0)),
                                   zoom, alpha=0.85)

    def draw_stump(self, painter, am, payload, zoom):
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

    def draw_agent(self, painter: QPainter, agent):
        am = self.controller.sim.am
        zoom = self.transform.zoom
        pixmap = self._agent_pixmap(am, agent)
        shadow = self.asset_cache.shadow(am)
        drawn = self._draw_grounded_sprite(painter, pixmap, agent.x, agent.y,
                                           zoom, shadow=shadow)
        if not drawn:
            # Aucun skin disponible : garder un repère plutôt qu'un habitant
            # invisible. N'arrive que si le pack d'assets est absent.
            sx, sy = self.transform.to_screen(agent.x, agent.y)
            if self._visible(sx, sy):
                rgb = CLAN_COLORS.get(str(getattr(agent, "color", "gray")),
                                      (150, 150, 150))
                painter.setPen(QPen(QColor(0, 0, 0), 1))
                painter.setBrush(QBrush(QColor(*rgb)))
                painter.drawEllipse(QPointF(sx, sy - 4), 6, 6)

        selected = getattr(self.controller.ui_state,
                           "selected_agent_eid", None) == agent.eid
        if selected:
            sx, sy = self.transform.to_screen(agent.x, agent.y)
            r = max(6.0, 8.0 * zoom)
            painter.setPen(QPen(QColor(255, 220, 80), 2))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(QPointF(sx, sy - r * 0.4), r, r * 0.45)

        if self.debug_show_labels:
            sx, sy = self.transform.to_screen(agent.x, agent.y)
            painter.setPen(QPen(QColor(255, 255, 255), 1))
            painter.setFont(QFont("Segoe UI", 8))
            painter.drawText(QPointF(sx + 8, sy - 5), str(agent.eid))

    def _agent_pixmap(self, am, agent):
        states = am.skin_states(str(getattr(agent, "color", "blue")),
                                str(getattr(agent, "cls", "pawn")))
        state = self._SKIN_STATE.get(str(getattr(agent, "state", "idle")), "idle")
        ids = states.get(state) or states.get("run") or states.get("idle") or []
        if not ids:
            return None
        aid = int(ids[int(agent.eid) % len(ids)])
        frames = max(1, int(getattr(am.assets[aid], "frames", 1) or 1))
        tick = int(getattr(self.controller.sim.w, "tick", 0))
        frame = self._animation_frame(tick, agent, frames, state != "idle")
        return self.asset_cache.pixmap(am, aid, frame)

    def draw_sheep(self, painter: QPainter, sheep):
        am = self.controller.sim.am
        zoom = self.transform.zoom
        table = getattr(am, "sheep", {}) or {}
        state = str(getattr(sheep, "state", "idle"))
        aid = table.get(state)
        if aid is None and table:
            aid = next(iter(table.values()))
        if aid is None:
            return
        frames = max(1, int(getattr(am.assets[int(aid)], "frames", 1) or 1))
        tick = int(getattr(self.controller.sim.w, "tick", 0))
        frame = self._animation_frame(tick, sheep, frames, False)
        self._draw_grounded_sprite(
            painter, self.asset_cache.pixmap(am, int(aid), frame),
            sheep.x, sheep.y, zoom, shadow=self.asset_cache.shadow(am))

    def draw_monster(self, painter: QPainter, monster):
        am = self.controller.sim.am
        zoom = self.transform.zoom
        kinds = getattr(am, "monsters", {}) or {}
        table = kinds.get(str(getattr(monster, "kind", ""))) or {}
        if not table:
            for candidate in kinds.values():
                if candidate:
                    table = candidate
                    break
        if not table:
            return
        state = str(getattr(monster, "state", "idle"))
        aid = table.get(state)
        if aid is None:
            aid = next(iter(table.values()))
        frames = max(1, int(getattr(am.assets[int(aid)], "frames", 1) or 1))
        tick = int(getattr(self.controller.sim.w, "tick", 0))
        frame = self._animation_frame(tick, monster, frames, state == "attack")
        self._draw_grounded_sprite(
            painter, self.asset_cache.pixmap(am, int(aid), frame),
            monster.x, monster.y, zoom, shadow=self.asset_cache.shadow(am))

    def draw_item(self, painter: QPainter, item):
        am = self.controller.sim.am
        zoom = self.transform.zoom
        aid = getattr(item, "aid", -1)
        wx = float(getattr(item, "x", 0.0))
        wy = float(getattr(item, "y", 0.0))
        if aid is not None and 0 <= int(aid) < len(am.assets):
            if self._draw_grounded_sprite(
                    painter, self.asset_cache.pixmap(am, int(aid), 0),
                    wx, wy, zoom * 0.8):
                return
        sx, sy = self.transform.to_screen(wx, wy)
        if not self._visible(sx, sy):
            return
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(210, 180, 80)))
        painter.drawEllipse(QPointF(sx, sy - 2), 3, 3)

    # ------------------------------------------------------------------
    # Aperçu fantôme de pose (Lot D.3)
    # ------------------------------------------------------------------

    def draw_ghost(self, painter: QPainter):
        """Sprite semi-transparent sous le curseur en mode « Poser ».

        Teinté de rouge si ``can_place`` refuse la pose : l'aperçu ne peut
        donc jamais promettre une pose que la commande refusera.
        """
        ui_state = self.controller.ui_state
        if not getattr(ui_state, "ghost_visible", False):
            return
        tile = getattr(ui_state, "ghost_tile", None)
        aid = getattr(ui_state, "selected_asset_id", None)
        if tile is None or aid is None:
            return
        tx, ty = int(tile[0]), int(tile[1])
        sim = self.controller.sim
        am = sim.am
        aid = int(aid)
        if not (0 <= aid < len(am.assets)):
            return
        ok, _reason = can_place(sim.w, am, tx, ty, aid)
        size = max(1, int(getattr(am.assets[aid], "size_tiles", 1) or 1))
        pixmap = self.asset_cache.pixmap(am, aid, 0)
        if pixmap is None or pixmap.isNull():
            return
        if not ok:
            pixmap = self._tinted_red(pixmap)
        self._draw_grounded_sprite(
            painter, pixmap,
            (tx + size / 2.0) * TILE, (ty + size) * TILE,
            self.transform.zoom, alpha=0.55)

        sx0, sy0 = self.transform.to_screen(tx * TILE, ty * TILE)
        sx1, sy1 = self.transform.to_screen((tx + size) * TILE,
                                            (ty + size) * TILE)
        painter.setPen(QPen(QColor(255, 255, 255, 150) if ok
                            else QColor(255, 80, 80, 210), 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(QRectF(sx0, sy0, sx1 - sx0, sy1 - sy0))

    def _tinted_red(self, pixmap: QPixmap) -> QPixmap:
        cache = getattr(self, "_ghost_tints", None)
        if cache is None:
            cache = self._ghost_tints = {}
        key = pixmap.cacheKey()
        tinted = cache.get(key)
        if tinted is not None:
            return tinted
        image = pixmap.toImage().convertToFormat(QImage.Format.Format_RGBA8888)
        painter = QPainter(image)
        painter.setCompositionMode(
            QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(image.rect(), QColor(220, 60, 60, 255))
        painter.end()
        tinted = QPixmap.fromImage(image)
        cache[key] = tinted
        while len(cache) > 64:
            cache.pop(next(iter(cache)))
        return tinted

    # ------------------------------------------------------------------
    # Légende et minimap
    # ------------------------------------------------------------------

    def draw_legend(self, painter: QPainter):
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

    def _minimap_rect(self) -> QRectF:
        size = 192
        return QRectF(self.width() - size - 20, self.height() - size - 20,
                      size, size)

    def _center_from_minimap(self, pos):
        rect = self._minimap_rect()
        world_size = max(1.0, self.controller.sim.w.g * TILE)
        fx = (pos.x() - rect.x()) / rect.width()
        fy = (pos.y() - rect.y()) / rect.height()
        self.transform.center_on(max(0.0, min(1.0, fx)) * world_size,
                                 max(0.0, min(1.0, fy)) * world_size,
                                 self.width(), self.height(), world_size)
        self._sync_controller_from_transform()
        self.update()

    def draw_minimap(self, painter: QPainter):
        if self.minimap_qimage is None:
            return

        rect = self._minimap_rect()
        x0, y0 = rect.x(), rect.y()
        size = rect.width()

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
        self.chunk_cache.clear()
        self.chunk_qimages.clear()
        self.asset_cache.clear()
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

        if self._minimap_rect().contains(event.position()):
            self._minimap_drag = True
            self._center_from_minimap(event.position())
            return

        wx, wy = self.transform.to_world(
            event.position().x(),
            event.position().y(),
        )
        tx, ty = int(wx // TILE), int(wy // TILE)
        mode = getattr(self.controller.ui_state, "active_mode", "inspect")

        if mode == "inspect":
            self._run({
                "kind": "select_tile",
                "tx": tx,
                "ty": ty,
            }, invalidate=False)
            self.select_nearest_agent(wx, wy)

        elif mode == "agent":
            cmd = {"kind": "spawn_agent", "x": wx, "y": wy}
            pending = getattr(self.controller.ui_state,
                              "pending_spawn_agent", None)
            if pending:
                cmd.update(pending)
                self.controller.ui_state.pending_spawn_agent = None
            self._run(cmd, invalidate=False)

        elif mode == "sheep":
            self._run({
                "kind": "spawn_sheep",
                "x": wx,
                "y": wy,
            }, invalidate=False)

        elif mode == "monster":
            cmd = {"kind": "spawn_monster", "x": wx, "y": wy}
            monster_kind = getattr(self.controller.ui_state, "monster_kind", "")
            if monster_kind:
                cmd["monster_kind"] = monster_kind
            self._run(cmd, invalidate=False)

        else:
            self._stroke_group += 1
            self.painting = (tx, ty)
            self.apply_tool(tx, ty, group=self._stroke_group)

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

    def apply_tool(self, tx, ty, group=None):
        mode = getattr(self.controller.ui_state, "active_mode", "inspect")
        radius = getattr(self.controller.ui_state, "brush_size", 3)

        if mode in {"water", "land", "wall"}:
            self._run({
                "kind": "paint_tile",
                "tx": tx,
                "ty": ty,
                "mode": mode,
                "radius": radius,
                "group": group,
            })

        elif mode in {"carve", "restore"}:
            self._run({"kind": mode, "tx": tx, "ty": ty, "radius": radius,
                       "group": group})

        elif mode == "erase":
            self._run({"kind": "erase_tile", "tx": tx, "ty": ty,
                       "radius": radius, "group": group})

        elif mode == "place":
            aid = getattr(self.controller.ui_state, "selected_asset_id", None)
            if aid is None:
                # Un retour silencieux laissait croire que la pose avait réussi.
                self.command_result.emit({
                    "ok": False,
                    "error": "Aucun asset sélectionné dans le dock Assets",
                })
                return
            self._run({
                "kind": "place_asset",
                "tx": tx,
                "ty": ty,
                "aid": int(aid),
                "group": group,
            })

        elif mode == "floor":
            cmd = {"kind": "set_floor", "tx": tx, "ty": ty,
                   "radius": radius, "group": group}
            aid = getattr(self.controller.ui_state, "selected_asset_id", None)
            if aid is not None:
                cmd["aid"] = int(aid)
            self._run(cmd)

        elif mode == "block":
            material = getattr(self.controller.ui_state, "block_material", "bois")
            self._run({
                "kind": "build_block",
                "tx": tx,
                "ty": ty,
                "material": material,
                "radius": radius,
                "group": group,
            })

    def _run(self, command, invalidate=True):
        """Exécute une commande et publie son résultat.

        Tous les retours étaient auparavant jetés : un échec (case occupée,
        asset non plaçable, matériau indisponible) restait invisible.
        """
        result = self.controller.execute(command)
        if invalidate:
            self.invalidate_all_caches()
        self.command_result.emit(result)
        return result

    def mouseMoveEvent(self, event):
        if self._minimap_drag:
            self._center_from_minimap(event.position())
            return

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
                self.apply_tool(tx, ty, group=self._stroke_group)
                self.update()
            return

        self._update_ghost(event.position())

    def _update_ghost(self, pos):
        ui_state = self.controller.ui_state
        if getattr(ui_state, "active_mode", "inspect") != "place":
            if getattr(ui_state, "ghost_visible", False):
                ui_state.ghost_visible = False
                self.update()
            return
        wx, wy = self.transform.to_world(pos.x(), pos.y())
        tile = (int(wx // TILE), int(wy // TILE))
        if tile != getattr(ui_state, "ghost_tile", None) \
                or not getattr(ui_state, "ghost_visible", False):
            ui_state.ghost_tile = tile
            ui_state.ghost_visible = True
            self.update()

    def leaveEvent(self, event):
        if getattr(self.controller.ui_state, "ghost_visible", False):
            self.controller.ui_state.ghost_visible = False
            self.update()
        super().leaveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.panstart = None
        elif event.button() == Qt.MouseButton.LeftButton:
            if self.painting is not None:
                self.painting = None
                # Clôt l'entrée d'historique du glisser : un coup de
                # pinceau = une annulation, pas une par tuile.
                self.controller.execute({"kind": "end_stroke"})
            self._minimap_drag = False

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
