"""Lot B.1 : chunks de terrain — ordre (y0, y1, x0, x1) et invalidation."""
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
