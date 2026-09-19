"""Camera : deplacement/zoom + INCLINAISON 2.5D.

Le sol est verticalement ecrase par cos(tilt) (vue plongeante 45-60 degres),
les sprites restent debouts (billboards) ancrs au sol : c'est la projection
conceptuelle du document d'architecture, en 2D pur.

    screen_x = (wx - cam.x) * zoom
    screen_y = (wy - cam.y) * zoom * cos(tilt)
"""
import math

from .config import GRID, TILE, VIEW_W, VIEW_H

WORLD = GRID * TILE
ZOOMS = (0.1, 0.15, 0.2, 0.25, 0.35, 0.5, 0.75, 1, 1.5, 2, 3, 4, 6)


class Camera:
    def __init__(self, tilt=55.0):
        self.zoom = 0.25
        self.tilt = max(30.0, min(70.0, float(tilt)))
        self.x = WORLD / 2 - self.view_w() / 2
        self.y = WORLD / 2 - self.view_h() / 2

    @property
    def ys(self):
        return math.cos(math.radians(self.tilt))

    def view_w(self):
        return VIEW_W / self.zoom

    def view_h(self):
        return VIEW_H / (self.zoom * self.ys)

    def clamp(self):
        vw, vh = self.view_w(), self.view_h()
        if vw >= WORLD:
            self.x = (WORLD - vw) / 2
        else:
            self.x = min(max(self.x, 0), WORLD - vw)
        if vh >= WORLD:
            self.y = (WORLD - vh) / 2
        else:
            self.y = min(max(self.y, 0), WORLD - vh)

    def center_on(self, x, y):
        self.x = x - self.view_w() / 2
        self.y = y - self.view_h() / 2
        self.clamp()

    def to_world(self, sx, sy):
        return self.x + sx / self.zoom, self.y + sy / (self.zoom * self.ys)

    def to_screen(self, wx, wy):
        return (wx - self.x) * self.zoom, (wy - self.y) * self.zoom * self.ys

    def visible_tiles(self):
        tw = self.view_w()
        th = self.view_h()
        x0 = int(self.x // TILE) - 2
        y0 = int(self.y // TILE) - 2
        x1 = int((self.x + tw) // TILE) + 4
        y1 = int((self.y + th) // TILE) + 4
        return x0, y0, x1, y1

    def set_zoom(self, nz, anchor_screen=None):
        if anchor_screen is None:
            self.zoom = nz
            self.clamp()
            return
        ax, ay = anchor_screen
        wx, wy = self.to_world(ax, ay)
        self.zoom = nz
        self.x = wx - ax / nz
        self.y = wy - ay / (nz * self.ys)
        self.clamp()
