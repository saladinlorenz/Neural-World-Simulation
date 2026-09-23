"""Regression Lot 0.9 : chaque overlay peint sans exception et dessine quelque chose.

Avant correction, six peintures lisaient des attributs inexistants
(``croyances_danger``, ``relations``, ``faim``, ``identity``,
``confirmed_knowledge``, ``institutions``) et levaient AttributeError, ou ne
dessinaient rien a cause d'un garde inverse.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from game.mapapi import MapTransform
from ui_qt.studio.world_overlay import MODES


def _make_sim():
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    from game.engine import build_world, seed_life

    am = AssetManager(headless=True)
    am.discover()
    _set_asset_manager(am)
    world, sim = build_world(am, seed=5, procedural=False, populate_dense=False)
    seed_life(world, sim, sim.rng, n_agents=12, n_sheep=0)
    for _ in range(30):
        sim.tick()
    # Fixture : un village groupe, une repousse et une odeur en son centre.
    # ``seed_life`` disperse les naissances sur 1 000 x 1 000 tuiles : sans
    # regroupement, aucune fenetre de 240 x 180 px ne contiendrait d'habitant
    # et les overlays centres sur l'agent peindraient zero pixel.
    import math

    from game.config import TILE
    agents = [a for a in sim.agents if a.alive]
    if agents:
        ax, ay = agents[0].x, agents[0].y
        for i, agent in enumerate(agents):
            t = i * 2.399963229728653
            r = 2.0 * math.sqrt(i + 0.5)
            agent.x = ax + r * math.cos(t) * TILE
            agent.y = ay + r * math.sin(t) * TILE
        cy, cx = int(ay // TILE), int(ax // TILE)
        sim.w.regrow[cy, cx] = 0.7
        sim.w.smell[cy, cx] = 0.8
        # Un monde de 30 ticks n'a encore ni liens sociaux ni culture :
        # chaque overlay doit pourtant prouver qu'il peint ses donnees.
        if len(agents) >= 2:
            agents[0].rel[agents[1].eid] = [0.7, 0.5]
            agents[1].rel[agents[0].eid] = [0.7, 0.5]
        ck = getattr(sim, "clan_knowledge", None)
        if ck is not None:
            ck.culture[("chasse", cx // 8, cy // 8)] = {"confidence": 0.8}
            ck.institutions[("foyer", cx // 8, cy // 8)] = {
                "members": [a.eid for a in agents[:4]], "trust": 0.6}
    return sim


class TestOverlaysPaint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sim = _make_sim()

    def _paint(self, mode):
        from PyQt6.QtGui import QImage, QPainter, qRed
        from PyQt6.QtWidgets import QApplication

        app = QApplication.instance() or QApplication([])
        self._app = app
        image = QImage(240, 180, QImage.Format.Format_RGB32)
        image.fill(0xFF000000)
        painter = QPainter(image)
        try:
            from ui_qt.studio.world_overlay import WorldOverlay
            transform = MapTransform(zoom=1.0, tilt=55.0)
            # Sans centrage, to_screen renvoie ~8000 px pour des habitants au
            # milieu du monde : tous les gardes de visibilite rejetteraient.
            from game.config import GRID, TILE
            xs = [a.x for a in self.sim.agents if a.alive]
            ys = [a.y for a in self.sim.agents if a.alive]
            if xs:
                transform.center_on(sum(xs) / len(xs), sum(ys) / len(ys),
                                    image.width(), image.height(),
                                    GRID * TILE)
            WorldOverlay().paint(painter, transform, self.sim, mode)
        finally:
            painter.end()
        changed = 0
        for y in range(0, image.height(), 4):
            for x in range(0, image.width(), 4):
                if image.pixel(x, y) != 0xFF000000:
                    changed += 1
        return changed

    def test_all_modes_paint_without_exception(self):
        for mode in MODES:
            if mode == "normal":
                continue
            changed = self._paint(mode)
            self.assertGreater(changed, 0,
                               "overlay %s n'a rien dessine" % mode)


if __name__ == "__main__":
    unittest.main()
