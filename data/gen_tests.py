import io
import os

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

FILES = {}

FILES["tests/test_overlays_attributes.py"] = '''"""Regression Lot 0.9 : chaque overlay peint sans exception et dessine quelque chose.

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
    return sim


class TestOverlaysPaint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sim = _make_sim()

    def _paint(self, mode):
        from PyQt6.QtGui import QImage, QPainter, qRed
        from PyQt6.QtWidgets import QApplication

        QApplication.instance() or QApplication([])
        image = QImage(240, 180, QImage.Format.Format_RGB32)
        image.fill(0xFF000000)
        painter = QPainter(image)
        try:
            self.sim.ui_state.selected_agent_eid = self.sim.agents[0].eid
            self.sim.overlay_paint = None
            from ui_qt.studio.world_overlay import WorldOverlay
            WorldOverlay().paint(painter, MapTransform(zoom=1.0, tilt=55.0),
                                 self.sim, mode)
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
'''

FILES["tests/test_asset_cache.py"] = '''"""Lot C.1 : QtAssetCache — pixmap natif, cle sans echelle, LRU borne."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


def _make_am():
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager

    am = AssetManager(headless=True).discover()
    _set_asset_manager(am)
    return am


class TestQtAssetCache(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from PyQt6.QtWidgets import QApplication
        QApplication.instance() or QApplication([])
        cls.am = _make_am()

    def test_pixmap_not_null(self):
        from PyQt6.QtGui import QPixmap
        from ui_qt.asset_cache import QtAssetCache

        cache = QtAssetCache()
        pixmap = cache.pixmap(self.am, 0, 0)
        self.assertIsInstance(pixmap, QPixmap)
        self.assertFalse(pixmap.isNull())

    def test_key_has_no_scale(self):
        from ui_qt.asset_cache import QtAssetCache

        cache = QtAssetCache()
        first = cache.pixmap(self.am, 0, 0)
        second = cache.pixmap(self.am, 0, 0)
        self.assertIs(first, second)
        self.assertEqual(len(cache), 1)

    def test_clear(self):
        from ui_qt.asset_cache import QtAssetCache

        cache = QtAssetCache()
        cache.pixmap(self.am, 0, 0)
        cache.clear()
        self.assertEqual(len(cache), 0)

    def test_lru_cap(self):
        from ui_qt.asset_cache import QtAssetCache

        cache = QtAssetCache(max_entries=16)
        for aid in range(min(60, len(self.am.assets))):
            cache.pixmap(self.am, aid, 0)
        self.assertLessEqual(len(cache), 16)


if __name__ == "__main__":
    unittest.main()
'''

FILES["tests/test_terrain_chunks.py"] = '''"""Lot B.1 : chunks de terrain — ordre (y0, y1, x0, x1) et invalidation."""
import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _make_world():
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    from game.engine import build_world

    am = AssetManager(headless=True)
    am.discover()
    _set_asset_manager(am)
    world, sim = build_world(am, seed=3, procedural=True, populate_dense=False)
    return world


class TestTerrainChunks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.world = _make_world()

    def test_chunk_matches_render_patch_order(self):
        from game.mapcache import CHUNK, TerrainChunkCache
        from game.worldgen import render_patch_rgb

        cache = TerrainChunkCache()
        cx, cy = 2, 3
        rgb = cache.chunk_rgb(self.world, cx, cy)
        direct = render_patch_rgb(self.world.gen, cy * CHUNK, (cy + 1) * CHUNK,
                                  cx * CHUNK, (cx + 1) * CHUNK, shading=True)
        self.assertEqual(rgb.shape, (CHUNK, CHUNK, 3))
        self.assertTrue(np.array_equal(rgb, direct),
                        "le chunk ne correspond pas a render_patch_rgb(y0,y1,x0,x1)")

    def test_invalidation_on_mods(self):
        from game.mapcache import CHUNK, TerrainChunkCache

        cache = TerrainChunkCache()
        before = cache.chunk_rgb(self.world, 1, 1).copy()
        key_before = cache.key(self.world, 1, 1)

        self.world.water[CHUNK + 2, CHUNK + 2] = 1
        self.world.land[CHUNK + 2, CHUNK + 2] = 0
        self.world.mods_version += 1

        key_after = cache.key(self.world, 1, 1)
        self.assertNotEqual(key_before, key_after)
        after = cache.chunk_rgb(self.world, 1, 1)
        self.assertFalse(np.array_equal(before, after),
                         "un chunk modifie est reste dans son ancienne version")


if __name__ == "__main__":
    unittest.main()
'''

for path, content in FILES.items():
    io.open(path, "w", encoding="utf-8", newline="\n").write(content)
    print("wrote", path)
