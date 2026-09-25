from __future__ import annotations

import math
import time
from html import escape
from typing import Optional

import numpy as np

from PyQt6.QtCore import QPointF, QRectF, Qt, pyqtSignal
from PyQt6.QtGui import (
    QColor,
    QBrush,
    QFont,
    QFontMetrics,
    QImage,
    QPainter,
    QPen,
    QPixmap,
)
from PyQt6.QtWidgets import QMenu, QWidget

from game.config import CLAN_COLORS, GRID, TILE
from game.diagnostics import action_name
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
# Seuils de rendu adaptatif (Phase 6)
LOW_DETAIL_ZOOM = 0.45      # < 0.45 : points simples
MEDIUM_DETAIL_ZOOM = 0.85   # 0.45-0.85 : simplifié
HIGH_DETAIL_ZOOM = 0.85     # >= 0.85 : détail complet

TERRAINGREEN = QColor(86, 150, 62)
WATER = QColor(46, 92, 158)
BLOCKED = QColor(128, 118, 106)
DARK = QColor(12, 14, 20)
MINIMAP_BG = QColor(20, 24, 32, 220)

#: Zoom minimal d'affichage des noms d'habitants (Lot C).
NAME_ZOOM = 0.9

#: Zoom minimal d'affichage des icones d'etat (Lot D).
STATUS_ZOOM = 0.65

#: Etat prioritaire -> glyphe texte provisoire (Lot D). Le plan UX/UI prévoit
#: des glyphes le temps de disposer de vrais sprites d'interface.
STATUS_GLYPHS = {
    "injured": "✚",
    "hungry": "●",
    "thirsty": "◈",
    "tired": "☾",
    "afraid": "!",
    "sleep": "Zz",
    "work": "⚒",
}

STATUS_COLORS = {
    "injured": QColor("#FF6B6B"),
    "hungry": QColor("#F6BD60"),
    "thirsty": QColor("#4CC9F0"),
    "tired": QColor("#A78BFA"),
    "afraid": QColor("#FF8C6B"),
    "sleep": QColor("#B8C4FF"),
    "work": QColor("#F8E16C"),
}


def agent_status_icon(agent) -> Optional[str]:
    """Etat urgent prioritaire d'un habitant — UNE seule icone (Lot D).

    Priorite exacte du plan, mais sur les vrais attributs de ``Being`` :
    ``health``, ``hunger`` (miroir de ``needs[0]``), ``needs[2]`` (soif),
    ``energy``, ``emotions[0]`` (peur) et ``state``. ``getattr`` + garde de
    longueur partout : un attribut absent rend ``None`` au lieu d'une erreur.
    """
    try:
        health = float(getattr(agent, "health", 1.0))
    except (TypeError, ValueError):
        health = 1.0
    if health < 0.35:
        return "injured"

    try:
        hunger = float(getattr(agent, "hunger", 0.0))
    except (TypeError, ValueError):
        hunger = 0.0
    if hunger > 0.80:
        return "hungry"

    needs = getattr(agent, "needs", None)
    if needs is not None:
        try:
            if len(needs) > 2 and float(needs[2]) > 0.80:
                return "thirsty"
        except (TypeError, ValueError):
            pass

    try:
        energy = float(getattr(agent, "energy", 1.0))
    except (TypeError, ValueError):
        energy = 1.0
    if energy < 0.20:
        return "tired"

    emotions = getattr(agent, "emotions", None)
    if emotions is not None:
        try:
            if len(emotions) > 0 and float(emotions[0]) > 0.65:
                return "afraid"
        except (TypeError, ValueError):
            pass

    state = str(getattr(agent, "state", ""))
    if state == "sleep":
        return "sleep"
    if state in {"work", "build"}:
        return "work"
    return None


def _percent(value, default=0.0) -> float:
    """Jauge 0..1 tolérante (infobulle, jamais de TypeError au survol)."""
    try:
        v = float(value)
    except (TypeError, ValueError):
        return default
    if v != v:  # NaN
        return default
    return max(0.0, min(1.0, v))


def construction_stage(progress: float) -> str:
    """Etape d'un chantier d'apres sa progression (Lot J)."""
    if progress <= 0.0:
        return "site"
    if progress < 0.25:
        return "foundation"
    if progress < 0.60:
        return "walls"
    if progress < 0.90:
        return "roof"
    return "complete"


#: Teinte du chantier par etape (Lot J) — meme familles que le plan.
SITE_STAGE_COLORS = {
    "site": QColor(120, 140, 120, 150),
    "foundation": QColor(110, 90, 65, 180),
    "walls": QColor(170, 130, 85, 190),
    "roof": QColor(150, 70, 55, 210),
    "complete": QColor(90, 150, 100, 180),
}


class MapView(QWidget):
    """Carte Qt réactive avec terrain mis en cache.

    Le terrain est statique entre deux modifications.
    Les entités mobiles restent dessinées séparément.
    """

    #: Résultat brut de chaque commande déclenchée depuis la carte. La
    #: fenêtre principale l'affiche dans la barre d'état.
    command_result = pyqtSignal(dict)
    #: Tuile survolée par le curseur (tx, ty) — barre d'état (Lot E.6).
    hover_changed = pyqtSignal(int, int)
    #: Clic gauche sur le monde (hors minimap) — la fenêtre principale en
    #: profite pour annuler le suivi caméra automatique.
    map_clicked = pyqtSignal()

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.transform = MapTransform(zoom=0.75, tilt=55.0)
        self._sync_transform_from_controller()

        self.panstart: Optional[QPointF] = None
        self.painting: Optional[tuple[int, int]] = None
        #: Contextuel (Lot I) : un vrai glisser du bouton droit (pan) ne
        #: doit pas ouvrir le menu à la levée.
        self._pan_dragged = False
        self._pan_travel = 0.0
        #: Eid de l'habitant dont l'infobulle est déjà affichée (Lot I).
        self._tooltip_eid: Optional[int] = None
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
        #: Mode détail faible : désactive ombres, pluie, halos, grille, noms (sauf sélection)
        #: et dessine les habitants sous forme de points au zoom faible.
        self.low_detail_mode = False

        self.setMouseTracking(True)
        # Les flèches/WASD doivent atteindre la vue quand on clique dessus.
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
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

    def _visible(self, sx: float, sy: float, margin: float = 64.0) -> bool:
        """Vérifie si un point écran est dans la zone visible (+ marge)."""
        return (-margin <= sx <= self.width() + margin and
                -margin <= sy <= self.height() + margin)

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
        # Désactiver l'antialiasing pour le terrain/sprites pixel-art (plus net, plus rapide)
        # Garder l'antialiasing uniquement pour le texte/legend si nécessaire
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, False)

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

        # 1 — objets au sol (avec culling visibilité)
        for item in getattr(w, "items", ()):
            sx, sy = self.transform.to_screen(item.x, item.y)
            if self._visible(sx, sy, margin=64):
                drawables.append((float(getattr(item, "y", 0.0)), 1, "item", item))

        # 3 — animaux (avec culling visibilité)
        for sheep in sim.sheep:
            if sheep.alive:
                sx, sy = self.transform.to_screen(sheep.x, sheep.y)
                if self._visible(sx, sy, margin=48):
                    drawables.append((float(sheep.y), 3, "sheep", sheep))
        for monster in sim.monsters:
            if monster.alive:
                sx, sy = self.transform.to_screen(monster.x, monster.y)
                if self._visible(sx, sy, margin=48):
                    drawables.append((float(monster.y), 3, "monster", monster))

        # 4 — habitants (budget de rendu : performance.max_agents) + culling visibilité
        selected_eid = getattr(self.controller.ui_state,
                               "selected_agent_eid", None)
        budget = int((sim.runtime or {}).get("max_agents_rendered", 200))
        agents_alive = [a for a in sim.agents if a.alive]
        if len(agents_alive) > budget:
            head = [a for a in agents_alive if a.eid == selected_eid]
            rest = [a for a in agents_alive if a.eid != selected_eid]
            agents_alive = head + rest[: max(0, budget - len(head))]
        for agent in agents_alive:
            sx, sy = self.transform.to_screen(agent.x, agent.y)
            if self._visible(sx, sy, margin=48):
                drawables.append((float(agent.y), 4, "agent", agent))

        # 5 — effets d'action (liste déjà purgée par TTL côté moteur)
        for fx in getattr(sim, "effects", ()):
            try:
                fx_y = float(fx.get("y", 0.0))
                sx, sy = self.transform.to_screen(fx.get("x", 0), fx_y)
                if self._visible(sx, sy, margin=64):
                    drawables.append((fx_y, 5, "effect", fx))
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
        if fx.get("kind") in ("gift", "talk"):
            # Effets sociaux sans sprite (Lot J) : peints par
            # EffectsLayer.paint(), avant la nuit, une seule fois.
            return
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
        """Chantier progressif : emprise teintée, blocs posés, barre (Lot J).

        L'étape (``construction_stage``) colore l'emprise, puis chaque tâche
        déjà placée remplit sa tuile : la construction se lit avancer sans
        rien changer au moteur. Le contour et la barre historiques restent.
        """
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

        progress = max(0.0, min(1.0, float(site.progress())))
        color = SITE_STAGE_COLORS[construction_stage(progress)]

        # Emprise : chantier fantôme teinté par étape.
        ghost = QColor(color)
        ghost.setAlpha(70)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(ghost))
        painter.drawRect(rect)

        # Blocs déjà posés : une tuile posée = une tuile colorée.
        placed = getattr(site, "placed", None) or ()
        painter.setBrush(QBrush(QColor(color)))
        for task in tasks:
            if task.key not in placed:
                continue
            tsx0, tsy0 = self.transform.to_screen(task.tx * TILE,
                                                  task.ty * TILE)
            tsx1, tsy1 = self.transform.to_screen((task.tx + 1) * TILE,
                                                  (task.ty + 1) * TILE)
            painter.drawRect(QRectF(tsx0, tsy0, tsx1 - tsx0, tsy1 - tsy0))

        # Contour et barre de progression existants, conservés à l'identique.
        painter.setPen(QPen(QColor(255, 196, 88, 190), 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(rect)
        bar = QRectF(rect.left(), rect.top() - 8, rect.width() * progress, 4)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(255, 196, 88, 220)))
        painter.drawRect(bar)

    def draw_agent(self, painter: QPainter, agent):
        am = self.controller.sim.am
        zoom = self.transform.zoom
        sx, sy = self.transform.to_screen(agent.x, agent.y)
        selected = getattr(self.controller.ui_state,
                           "selected_agent_eid", None) == agent.eid

        # Rendu adaptatif selon le zoom et le mode détail faible (Phase 6)
        if self.low_detail_mode or zoom < LOW_DETAIL_ZOOM:
            # Points simples : couleur du clan, pas de sprite
            if self._visible(sx, sy, margin=16):
                rgb = CLAN_COLORS.get(str(getattr(agent, "color", "gray")),
                                      (150, 150, 150))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(QColor(*rgb)))
                painter.drawEllipse(QPointF(sx, sy), 3.0, 3.0)
            # Sélection : halo même en mode points
            if selected and self._visible(sx, sy, 60):
                self.draw_selected_agent_marker(painter, agent, sx, sy)
            return

        # Rendu simplifié (zoom moyen) : sprite sans ombre, pas de nom/statut
        if zoom < MEDIUM_DETAIL_ZOOM:
            pixmap = self._agent_pixmap(am, agent)
            drawn = self._draw_grounded_sprite(painter, pixmap, agent.x, agent.y,
                                               zoom, shadow=None)
            if not drawn and self._visible(sx, sy):
                rgb = CLAN_COLORS.get(str(getattr(agent, "color", "gray")),
                                      (150, 150, 150))
                painter.setPen(QPen(QColor(0, 0, 0), 1))
                painter.setBrush(QBrush(QColor(*rgb)))
                painter.drawEllipse(QPointF(sx, sy - 4), 6, 6)
            if selected and self._visible(sx, sy, 60):
                self.draw_selected_agent_marker(painter, agent, sx, sy)
            return

        # Rendu détaillé (zoom élevé) - code original
        # Marqueur de sélection au sol AVANT le sprite
        if selected and self._visible(sx, sy, 60):
            self.draw_selected_agent_marker(painter, agent, sx, sy)

        # Ligne but/cible discrète, seulement pour l'habitant sélectionné
        if selected:
            self._draw_goal_line(painter, agent, sx, sy, zoom)

        pixmap = self._agent_pixmap(am, agent)
        shadow = self.asset_cache.shadow(am)
        drawn = self._draw_grounded_sprite(painter, pixmap, agent.x, agent.y,
                                           zoom, shadow=shadow)
        if not drawn:
            if self._visible(sx, sy):
                rgb = CLAN_COLORS.get(str(getattr(agent, "color", "gray")),
                                      (150, 150, 150))
                painter.setPen(QPen(QColor(0, 0, 0), 1))
                painter.setBrush(QBrush(QColor(*rgb)))
                painter.drawEllipse(QPointF(sx, sy - 4), 6, 6)

        # Ligne de base des repères flottants
        ph = 0.0
        if pixmap is not None and not pixmap.isNull():
            ph = pixmap.height() * zoom
        head_y = sy - ph - 4.0 if ph > 0.0 else sy - 28.0

        if self._visible(sx, sy, 60):
            self.draw_agent_status(painter, agent, sx, head_y, zoom)
            if zoom >= NAME_ZOOM:
                self._draw_agent_name(painter, agent, sx, head_y, zoom,
                                      selected)

        if self.debug_show_labels:
            painter.setPen(QPen(QColor(255, 255, 255), 1))
            painter.setFont(QFont("Segoe UI", 8))
            painter.drawText(QPointF(sx + 8, sy - 5), str(agent.eid))

    def draw_selected_agent_marker(self, painter, agent, sx, sy):
        """Halo pulsé jaune + anneau au sol de l'habitant sélectionné (Lot C).

        Le plan lit ``self.animation_time`` qui n'existe pas : la pulsation
        est tirée de l'horloge réelle, et comme MainWindow redessine la carte
        tous les 2 ticks, l'animation avance sans état supplémentaire.
        """
        pulse = 0.5 + 0.5 * math.sin(time.monotonic() * 4.0)
        scale = max(0.8, min(2.5, float(self.transform.zoom)))
        radius = (18.0 + pulse * 3.0) * scale

        glow = QColor(248, 225, 108, int(70 + 60 * pulse))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(glow))
        painter.drawEllipse(QPointF(sx, sy), radius, radius * 0.36)

        painter.setPen(QPen(QColor(248, 225, 108), 2.0))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QPointF(sx, sy), radius * 0.62, radius * 0.22)

    def draw_agent_status(self, painter, agent, sx, sy, zoom):
        """Une seule icône d'état au-dessus de l'habitant (Lot D).

        ``sy`` est la ligne de base : le sommet de la tête du sprite (le sol
        si le skin est absent). Invisible sous ``STATUS_ZOOM``, contour sombre
        pour rester lisible sur n'importe quel terrain.
        """
        if zoom < STATUS_ZOOM:
            return
        key = agent_status_icon(agent)
        if key is None:
            return
        glyph = STATUS_GLYPHS.get(key)
        color = STATUS_COLORS.get(key)
        if not glyph or color is None:
            return
        font = QFont("Segoe UI Symbol", max(8, int(11 * zoom)))
        painter.setFont(font)
        x = sx - QFontMetrics(font).horizontalAdvance(glyph) / 2.0
        painter.setPen(QPen(QColor(0, 0, 0, 180), 3))
        painter.drawText(QPointF(x + 1.0, sy + 1.0), glyph)
        painter.setPen(QPen(color, 1))
        painter.drawText(QPointF(x, sy), glyph)

    def _draw_agent_name(self, painter, agent, sx, head_y, zoom, selected):
        """Nom de l'habitant au-dessus de sa tête, zoom >= 0.9 (Lot C)."""
        name = str(getattr(agent, "name", "") or "")
        if not name:
            return
        size = max(8, min(16, int(10 * zoom)))
        font = QFont("Segoe UI", size)
        font.setBold(bool(selected))
        metrics = QFontMetrics(font)
        x = sx - metrics.horizontalAdvance(name) / 2.0
        y = head_y - max(14.0, 12.0 * zoom)
        painter.setFont(font)
        painter.setPen(QPen(QColor(0, 0, 0, 200), 3))
        painter.drawText(QPointF(x + 1.0, y + 1.0), name)
        painter.setPen(QPen(QColor(248, 225, 108) if selected
                            else QColor(236, 241, 248), 1))
        painter.drawText(QPointF(x, y), name)

    def _draw_goal_line(self, painter, agent, sx, sy, zoom):
        """Ligne discrète vers la cible du but courant (Lot C).

        ``Being.goal`` est un dict ``{"act", "x", "y", …}`` où ``x``/``y``
        sont des coordonnées en TUILES : la ligne n'a de sens que si la
        cible diffère de la tuile occupée par l'habitant.
        """
        if zoom < 0.45:
            return
        goal = getattr(agent, "goal", None)
        if not isinstance(goal, dict):
            return
        gx, gy = goal.get("x"), goal.get("y")
        if gx is None or gy is None:
            return
        try:
            gx, gy = int(gx), int(gy)
        except (TypeError, ValueError):
            return
        if gx == int(getattr(agent, "tx", gx)) \
                and gy == int(getattr(agent, "ty", gy)):
            return
        gxs, gys = self.transform.to_screen((gx + 0.5) * TILE,
                                            (gy + 0.5) * TILE)
        if not self._visible(gxs, gys, 40):
            return
        painter.setPen(QPen(QColor(248, 225, 108, 120), 1,
                            Qt.PenStyle.DashLine))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawLine(QPointF(sx, sy), QPointF(gxs, gys))

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
        zoom = self.transform.zoom
        sx, sy = self.transform.to_screen(sheep.x, sheep.y)

        # Rendu adaptatif (Phase 6)
        if self.low_detail_mode or zoom < LOW_DETAIL_ZOOM:
            if self._visible(sx, sy, margin=16):
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(QColor(200, 200, 180)))
                painter.drawEllipse(QPointF(sx, sy), 2.5, 2.5)
            return
        if zoom < MEDIUM_DETAIL_ZOOM:
            if not self._visible(sx, sy, margin=32):
                return

        am = self.controller.sim.am
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
        shadow = None if zoom < MEDIUM_DETAIL_ZOOM else self.asset_cache.shadow(am)
        self._draw_grounded_sprite(
            painter, self.asset_cache.pixmap(am, int(aid), frame),
            sheep.x, sheep.y, zoom, shadow=shadow)

    def draw_monster(self, painter: QPainter, monster):
        zoom = self.transform.zoom
        sx, sy = self.transform.to_screen(monster.x, monster.y)

        # Rendu adaptatif (Phase 6)
        if self.low_detail_mode or zoom < LOW_DETAIL_ZOOM:
            if self._visible(sx, sy, margin=16):
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(QColor(180, 100, 100)))
                painter.drawEllipse(QPointF(sx, sy), 3.0, 3.0)
            return
        if zoom < MEDIUM_DETAIL_ZOOM:
            if not self._visible(sx, sy, margin=32):
                return

        am = self.controller.sim.am
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
        shadow = None if zoom < MEDIUM_DETAIL_ZOOM else self.asset_cache.shadow(am)
        self._draw_grounded_sprite(
            painter, self.asset_cache.pixmap(am, int(aid), frame),
            monster.x, monster.y, zoom, shadow=shadow)

    def draw_item(self, painter: QPainter, item):
        zoom = self.transform.zoom
        aid = getattr(item, "aid", -1)
        wx = float(getattr(item, "x", 0.0))
        wy = float(getattr(item, "y", 0.0))
        sx, sy = self.transform.to_screen(wx, wy)

        # Rendu adaptatif (Phase 6)
        if self.low_detail_mode or zoom < LOW_DETAIL_ZOOM:
            if self._visible(sx, sy, margin=16):
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(QColor(210, 180, 80)))
                painter.drawEllipse(QPointF(sx, sy - 2), 2.5, 2.5)
            return
        if zoom < MEDIUM_DETAIL_ZOOM:
            if not self._visible(sx, sy, margin=32):
                return

        am = self.controller.sim.am
        if aid is not None and 0 <= int(aid) < len(am.assets):
            if self._draw_grounded_sprite(
                    painter, self.asset_cache.pixmap(am, int(aid), 0),
                    wx, wy, zoom * 0.8):
                return
        if self._visible(sx, sy):
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
            self._pan_dragged = False
            self._pan_travel = 0.0
            return

        if event.button() != Qt.MouseButton.LeftButton:
            return

        if self._minimap_rect().contains(event.position()):
            self._minimap_drag = True
            self._center_from_minimap(event.position())
            return

        self.map_clicked.emit()

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
            result = self._run(cmd, invalidate=False)
            if pending:
                # Un échec (plafond de population) ne doit pas détruire le
                # gabarit : l'utilisateur reclique ailleurs pour réessayer.
                if result.get("ok"):
                    self.controller.ui_state.pending_spawn_agent = None
                    # « Etre » pose un seul habitant par validation du dialogue :
                    # sans ce retour, les clics suivants spawnaient des
                    # habitants aléatoires sans prévenir.
                    self.controller.execute(
                        {"kind": "set_mode", "mode": "inspect"})

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
        # Pose reussie → asset ajoute en tete des recents (Lot E.4)
        if (command.get("kind") == "place_asset"
                and result.get("ok")
                and command.get("aid") is not None):
            ui_state = self.controller.ui_state
            aid = int(command["aid"])
            recent = [int(a) for a in getattr(ui_state, "recents", [])]
            if aid in recent:
                recent.remove(aid)
            recent.insert(0, aid)
            ui_state.recents = recent[:12]
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
            self._pan_travel += math.hypot(dx, dy)
            if self._pan_travel > 3.0:
                # Vrai glisser : le bouton droit navigue, il n'ouvre pas de
                # menu contextuel à la levée (Lot I).
                self._pan_dragged = True

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

        # Tuile survolée → barre d'état (Lot E.6)
        wx, wy = self.transform.to_world(
            event.position().x(), event.position().y())
        self.hover_changed.emit(int(wx // TILE), int(wy // TILE))

        self._update_ghost(event.position())
        self._update_agent_tooltip(event.position())

    def agent_at(self, pos, pad=6.0):
        """Habitant sous le curseur, ou ``None`` (Lot I).

        Filtre grossier en coordonnées monde (coûte deux multiplications par
        habitant), puis test de la boîte billboard approximative du sprite :
        ancré au sol, ~32 px de large et ~48 px de haut au zoom 1.
        """
        wx, wy = self.transform.to_world(pos.x(), pos.y())
        zoom = max(float(self.transform.zoom), 1e-6)
        ys = max(float(self.transform.ys), 1e-6)
        rx = (16.0 + pad) / zoom
        ry = 48.0 / ys + pad / (zoom * ys)

        best, best_distance = None, None
        for agent in self.controller.sim.agents:
            if not getattr(agent, "alive", False):
                continue
            dx = agent.x - wx
            if dx < -rx or dx > rx:
                continue
            dy = agent.y - wy
            if dy < -ry or dy > ry:
                continue
            sx, sy = self.transform.to_screen(agent.x, agent.y)
            if not (sx - 16.0 - pad <= pos.x() <= sx + 16.0 + pad
                    and sy - 48.0 * zoom - pad <= pos.y() <= sy + pad):
                continue
            distance = (pos.x() - sx) ** 2 + (pos.y() - sy) ** 2
            if best_distance is None or distance < best_distance:
                best, best_distance = agent, distance
        return best

    def agent_tooltip(self, agent) -> str:
        """Infobulle HTML d'un habitant : nom, classe/stade, santé, énergie, but."""
        name = escape(str(getattr(agent, "name", "?")))
        cls = escape(str(getattr(agent, "cls", "?")))
        stage = str(getattr(agent, "stage", ""))
        health = _percent(getattr(agent, "health", None))
        energy = _percent(getattr(agent, "energy", None))

        goal = getattr(agent, "goal", None)
        if isinstance(goal, dict) and goal.get("act") is not None:
            but = action_name(self.controller.sim, goal.get("act"))
            gx, gy = goal.get("x"), goal.get("y")
            if gx is not None and gy is not None:
                try:
                    but = f"{but} → {int(gx)},{int(gy)}"
                except (TypeError, ValueError):
                    pass
        else:
            but = "Repos"

        lines = [f"<b>{name}</b>"]
        lines.append(f"{cls} · {escape(stage)}" if stage else cls)
        lines.append(f"Santé : {health:.0%}")
        lines.append(f"Énergie : {energy:.0%}")
        lines.append(f"But : {escape(but)}")
        return "<br>".join(lines)

    def _update_agent_tooltip(self, pos):
        """Infobulle seulement quand le curseur est proche d'un habitant."""
        agent = self.agent_at(pos)
        raw_eid = getattr(agent, "eid", None) if agent is not None else None
        eid = None
        if raw_eid is not None:
            try:
                eid = int(raw_eid)
            except (TypeError, ValueError):
                eid = None
        if eid == self._tooltip_eid:
            return
        self._tooltip_eid = eid
        self.setToolTip(self.agent_tooltip(agent) if agent is not None else "")

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
        if self._tooltip_eid is not None:
            self._tooltip_eid = None
            self.setToolTip("")
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

    # ------------------------------------------------------------------
    # Navigation clavier : flèches + WASD/ZQSD, zoom +/- / PageUp/Down
    # ------------------------------------------------------------------

    #: Pixels écran déplacés par pression (l'auto-repeat du système
    #: permet un déplacement continu en maintenant la touche).
    KEY_PAN_STEP = 96.0

    def pan_by_screen(self, dx: float, dy: float) -> None:
        """Déplace la caméra de ``dx``/``dy`` pixels écran."""
        z = max(self.transform.zoom, 0.01)
        self.transform.x += dx / z
        self.transform.y += dy / (z * max(self.transform.ys, 0.01))
        self.transform.clamp(GRID * TILE, self.width(), self.height())
        self._sync_controller_from_transform()
        self.update()

    def zoom_step(self, factor: float) -> None:
        """Zoom au centre de la vue (molette clavier)."""
        new_zoom = max(0.08, min(4.0, self.transform.zoom * factor))
        self.transform.set_zoom(
            new_zoom,
            (self.width() // 2, self.height() // 2),
            self.width(),
            self.height(),
        )
        self.transform.clamp(GRID * TILE, self.width(), self.height())
        self._sync_controller_from_transform()
        self.update()

    def handle_nav_key(self, event) -> bool:
        """Traite une touche de navigation. Retourne True si consommée.

        Q/Z et A/Q couvrent QWERTY et AZERTY ; les flèches marchent
        partout. Si la touche est prise par un widget input (spinbox,
        liste…), celui-ci la consomme et on n'arrive jamais ici.
        """
        key = event.key()
        step = self.KEY_PAN_STEP
        dx = dy = 0.0
        if key in (Qt.Key.Key_Right, Qt.Key.Key_D):
            dx = step
        elif key in (Qt.Key.Key_Left, Qt.Key.Key_A, Qt.Key.Key_Q):
            dx = -step
        elif key in (Qt.Key.Key_Down, Qt.Key.Key_S):
            dy = step
        elif key in (Qt.Key.Key_Up, Qt.Key.Key_W, Qt.Key.Key_Z):
            dy = -step
        if dx or dy:
            self.pan_by_screen(dx, dy)
            event.accept()
            return True
        if key in (Qt.Key.Key_Plus, Qt.Key.Key_Equal, Qt.Key.Key_PageUp):
            self.zoom_step(1.2)
            event.accept()
            return True
        if key in (Qt.Key.Key_Minus, Qt.Key.Key_PageDown):
            self.zoom_step(1 / 1.2)
            event.accept()
            return True
        return False

    def keyPressEvent(self, event):
        if not self.handle_nav_key(event):
            super().keyPressEvent(event)

    # ------------------------------------------------------------------
    # Menus contextuels (Lot I)
    # ------------------------------------------------------------------

    def contextMenuEvent(self, event):
        """Clic droit : menu sur l'habitant, sinon menu terrain (en français).

        Le bouton droit sert déjà au pan ; le menu s'affiche à la levée, mais
        un glisser réel (``_pan_dragged``) le supprime pour ne pas gêner la
        navigation. ``mousePressEvent``/``mouseReleaseEvent`` restent intacts.
        """
        if self._pan_dragged:
            self._pan_dragged = False
            return
        pos = event.pos()
        agent = self.agent_at(pos)
        if agent is not None:
            self._context_menu_agent(event, agent)
        else:
            self._context_menu_terrain(event, pos)

    def _select_agent(self, agent):
        self._run({"kind": "select_agent", "eid": int(agent.eid)},
                  invalidate=False)
        self.update()

    def _context_menu_agent(self, event, agent):
        menu = QMenu(self)
        act_select = menu.addAction("Sélectionner")
        act_follow = menu.addAction("Suivre")
        act_inspect = menu.addAction("Ouvrir l'inspecteur")
        chosen = menu.exec(event.globalPos())
        if chosen is None:
            return

        if chosen == act_select:
            self._select_agent(agent)
            return

        if chosen == act_follow:
            self._select_agent(agent)
            self.controller.ui_state.follow_selected = True
            action = getattr(self.window(), "_follow_action", None)
            if action is not None and hasattr(action, "setChecked"):
                action.setChecked(True)
            return

        if chosen == act_inspect:
            self._select_agent(agent)
            self.controller.ui_state.active_tab = "etre"
            dock = getattr(self.window(), "_inspector_dock", None)
            if dock is not None and hasattr(dock, "raise_"):
                dock.raise_()

    def _context_menu_terrain(self, event, pos):
        sim = self.controller.sim
        grid = int(sim.w.g)
        wx, wy = self.transform.to_world(pos.x(), pos.y())
        tx, ty = int(wx // TILE), int(wy // TILE)
        if not (0 <= tx < grid and 0 <= ty < grid):
            return

        ui_state = self.controller.ui_state
        aid = getattr(ui_state, "selected_asset_id", None)

        menu = QMenu(self)
        act_tile = menu.addAction("Examiner la tuile")
        act_place = menu.addAction("Poser l'asset sélectionné")
        act_place.setEnabled(aid is not None)
        menu.addSeparator()
        act_agent = menu.addAction("Invoquer un habitant ici")
        act_sheep = menu.addAction("Mouton ici")
        act_monster = menu.addAction("Monstre ici")
        menu.addSeparator()
        act_center = menu.addAction("Centrer la caméra ici")

        chosen = menu.exec(event.globalPos())
        if chosen is None:
            return

        cx, cy = (tx + 0.5) * TILE, (ty + 0.5) * TILE
        if chosen == act_tile:
            self._run({"kind": "select_tile", "tx": tx, "ty": ty},
                      invalidate=False)
        elif chosen == act_place and aid is not None:
            # Arme l'outil « Poser » puis réutilise le chemin de pose classique.
            self._run({"kind": "set_mode", "mode": "place"}, invalidate=False)
            dock = getattr(self.window(), "_tools_dock", None)
            if dock is not None and hasattr(dock, "refresh"):
                dock.refresh()
            self.apply_tool(tx, ty)
        elif chosen == act_agent:
            self._run({"kind": "spawn_agent", "x": cx, "y": cy},
                      invalidate=False)
        elif chosen == act_sheep:
            self._run({"kind": "spawn_sheep", "x": cx, "y": cy},
                      invalidate=False)
        elif chosen == act_monster:
            cmd = {"kind": "spawn_monster", "x": cx, "y": cy}
            monster_kind = getattr(ui_state, "monster_kind", "")
            if monster_kind:
                cmd["monster_kind"] = monster_kind
            self._run(cmd, invalidate=False)
        elif chosen == act_center:
            self.transform.center_on(wx, wy, self.width(), self.height(),
                                     max(1.0, grid * TILE))
            self._sync_controller_from_transform()
        self.update()
