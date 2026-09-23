"""Lot C.1 : QtAssetCache — pixmap natif, cle sans echelle, LRU borne."""
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
        # Garder la reference : sans elle l'objet est ramasse et tout appel
        # Qt suivant fait tomber l'interpreteur sans traceback.
        cls.app = QApplication.instance() or QApplication([])
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
