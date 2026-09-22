"""MapAPI — abstraction de carte sans Pygame.

Fournit des snapshots de carte et des conversions de coordonnees
pour n'importe quel frontend (Pygame, Qt, web).
"""
from __future__ import annotations

import math
from typing import Any


class MapTransform:
    """Transformation geometrique de la carte (neutre, pas de Pygame)."""

    def __init__(self, x: float = 0.0, y: float = 0.0,
                 zoom: float = 0.25, tilt: float = 55.0):
        self.x = x
        self.y = y
        self.zoom = zoom
        self.tilt = tilt

    @property
    def ys(self) -> float:
        return math.cos(math.radians(self.tilt))

    def view_w(self, screen_w: int) -> float:
        return screen_w / self.zoom

    def view_h(self, screen_h: int) -> float:
        return screen_h / (self.zoom * self.ys)

    def to_screen(self, wx: float, wy: float) -> tuple[float, float]:
        """Coordonnees monde -> ecran."""
        return (wx - self.x) * self.zoom, (wy - self.y) * self.zoom * self.ys

    def to_world(self, sx: float, sy: float) -> tuple[float, float]:
        """Coordonnees ecran -> monde."""
        return self.x + sx / self.zoom, self.y + sy / (self.zoom * self.ys)

    def clamp(self, world_size: float, screen_w: int = 800,
              screen_h: int = 600) -> None:
        """Empeche de sortir du monde.

        `screen_w`/`screen_h` sont les dimensions REELLES de la vue : les
        passer pour la taille du monde (ancien comportement) faisait que la
        camera etait « centree » hors du monde des le premier zoom — carte
        noire.
        """
        vw = self.view_w(screen_w)
        vh = self.view_h(screen_h)
        if vw >= world_size:
            self.x = (world_size - vw) / 2
        else:
            self.x = min(max(self.x, 0), world_size - vw)
        if vh >= world_size:
            self.y = (world_size - vh) / 2
        else:
            self.y = min(max(self.y, 0), world_size - vh)

    def center_on(self, wx: float, wy: float, screen_w: int, screen_h: int,
                  world_size: float) -> None:
        """Centre la vue sur un point monde."""
        self.x = wx - self.view_w(screen_w) / 2
        self.y = wy - self.view_h(screen_h) / 2
        self.clamp(world_size, screen_w, screen_h)

    def visible_tiles(self, tile_size: int, grid_size: int,
                      screen_w: int = 800,
                      screen_h: int = 600) -> tuple[int, int, int, int]:
        """Retourne (x0, y0, x1, y1) des tuiles visibles."""
        vw = self.view_w(screen_w)
        vh = self.view_h(screen_h)
        x0 = max(0, int(self.x // tile_size) - 2)
        y0 = max(0, int(self.y // tile_size) - 2)
        x1 = min(grid_size, int((self.x + vw) // tile_size) + 3)
        y1 = min(grid_size, int((self.y + vh) // tile_size) + 3)
        return x0, y0, x1, y1

    def set_zoom(self, new_zoom: float, anchor_screen: tuple[int, int] = (0, 0),
                 screen_w: int = 800, screen_h: int = 600) -> None:
        """Change le zoom en gardant un point ecran fixe.

        L'ancienne formule soustrayait un ecart calcule APRES le changement
        de zoom : la camera derivait a chaque cran de molette.
        """
        wx, wy = self.to_world(anchor_screen[0], anchor_screen[1])
        self.zoom = max(0.05, min(6.0, new_zoom))
        self.x = wx - anchor_screen[0] / self.zoom
        self.y = wy - anchor_screen[1] / (self.zoom * self.ys)


def map_tile_data(sim, tx: int, ty: int) -> dict[str, Any] | None:
    """Donnees d'une tuile pour le rendu (pas de surface Pygame).

    Conservee pour un usage ponctuel (ex: inspection d'une tuile precise),
    mais n'est plus appelee en boucle par map_visible_data (voir plus bas) :
    l'appeler tuile par tuile sur toute la zone visible etait l'operation
    qui faisait ramer/geler l'app au demarrage.
    """
    w = sim.w
    if not (0 <= tx < w.g and 0 <= ty < w.g):
        return None

    aid = w.content_at(tx, ty)
    return {
        "tx": tx,
        "ty": ty,
        "land": bool(w.land[ty, tx]),
        "water": bool(w.water[ty, tx]),
        "blocked": bool(w.blocked[ty, tx]),
        "shelter": bool(w.shelter[ty, tx]),
        "fire": int(w.fire[ty, tx]),
        "floor": int(w.floor[ty, tx]),
        "hp": int(w.hp[ty, tx]) if aid >= 0 else 0,
        "asset_id": int(aid) if aid >= 0 else -1,
        "regrow": float(w.regrow[ty, tx]),
    }


def map_visible_data(sim, transform: MapTransform, screen_w: int, screen_h: int,
                     tile_size: int = None) -> dict[str, Any]:
    """Snapshot de la zone visible pour le rendu carte.

    Retourne des donnees simples, pas de surfaces.

    NOTE PERF / TEMPORAIRE (2026-09-22) :
    La carte fait GRID x GRID tuiles (GRID=1000 dans config.py). Au zoom
    par defaut (0.25), la zone visible couvre facilement 100 000+ tuiles.
    L'ancienne version appelait map_tile_data() (donc plusieurs lectures
    numpy scalaires + creation d'un dict) pour CHAQUE tuile visible, a
    chaque frame : c'est ce qui faisait demarrer l'app puis rester bloquee/
    saccadee (des centaines de milliers d'operations Python par frame).

    Pour l'instant le terrain n'est plus envoye tuile par tuile : on
    renvoie juste la zone visible (tile_range) et le cote UI (map_view.py)
    la dessine comme un unique aplat vert. C'est volontairement simplifie
    ("terrain completement vert pour l'instant") pour valider que le lag
    vient bien de la et debloquer le demarrage ; le detail par tuile
    (eau/mur/feu) pourra revenir plus tard via une version vectorisee
    numpy (calculee sur toute la zone en une fois, sans boucle Python).
    """
    from .config import GRID, TILE
    ts = tile_size or TILE
    grid_size = GRID

    x0, y0, x1, y1 = transform.visible_tiles(ts, grid_size, screen_w, screen_h)

    # Terrain : plus de boucle tuile par tuile ici (voir note ci-dessus).
    # Le cote UI dessine un aplat vert sur la zone (x0, y0, x1, y1).
    terrain: list[dict[str, Any]] = []

    # Agents visibles
    agents = []
    vw = transform.view_w(screen_w)
    vh = transform.view_h(screen_h)
    for a in sim.agents:
        if not a.alive:
            continue
        sx, sy = transform.to_screen(a.x, a.y)
        if -50 < sx < screen_w + 50 and -50 < sy < screen_h + 50:
            agents.append({
                "eid": int(a.eid),
                "sx": float(sx), "sy": float(sy),
                "color": str(a.color),
                "cls": str(a.cls),
                "stage": str(a.stage),
            })

    # Sheep visibles
    sheep = []
    for s in sim.sheep:
        sx, sy = transform.to_screen(s.x, s.y)
        if -50 < sx < screen_w + 50 and -50 < sy < screen_h + 50:
            sheep.append({"eid": int(s.eid), "sx": float(sx), "sy": float(sy)})

    # Monsters visibles
    monsters = []
    for m in sim.monsters:
        sx, sy = transform.to_screen(m.x, m.y)
        if -50 < sx < screen_w + 50 and -50 < sy < screen_h + 50:
            monsters.append({
                "eid": int(m.eid), "sx": float(sx), "sy": float(sy),
                "kind": str(getattr(m, "kind", "")),
            })

    # Effets visibles
    effects = []
    for e in sim.effects:
        sx, sy = transform.to_screen(e.get("x", 0), e.get("y", 0))
        if -50 < sx < screen_w + 50 and -50 < sy < screen_h + 50:
            effects.append({
                "kind": str(e.get("kind", "")),
                "sx": float(sx), "sy": float(sy),
                "color": tuple(e.get("color", (255, 255, 255))),
            })

    return {
        "tick": int(sim.w.tick),
        "tile_range": (x0, y0, x1, y1),
        "terrain": terrain,
        "agents": agents,
        "sheep": sheep,
        "monsters": monsters,
        "effects": effects,
        "zoom": float(transform.zoom),
        "tilt": float(transform.tilt),
    }
