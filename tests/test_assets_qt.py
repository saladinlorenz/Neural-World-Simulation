"""Tests assets Qt — conversion PIL→QPixmap dans _load_thumbnail, avatar."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


def _make_am():
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager

    am = AssetManager(headless=True).discover()
    am.ensure_procedural_blocks()
    am.ensure_procedural_tools()
    am.ensure_kaykit_resources()
    _set_asset_manager(am)
    return am


def test_thumbnail_returns_pil():
    from PIL import Image

    am = _make_am()
    aid = 0
    if not am.assets:
        raise AssertionError("aucun asset")
    thumb = am.thumbnail(aid, size=48)
    assert thumb is not None, "thumbnail None"
    assert isinstance(thumb, Image.Image), f"type inattendu: {type(thumb)}"
    print("OK test_thumbnail_returns_pil")


def test_load_thumbnail_no_nameerror():
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtGui import QPixmap
    from ui_qt.docks.assets_dock import AssetsDock

    app = QApplication.instance() or QApplication([])

    class _FakeController:
        def __init__(self, am):
            class _S:
                pass
            self.sim = _S()
            self.sim.am = am
            self.ui_state = None

    am = _make_am()
    dock = AssetsDock.__new__(AssetsDock)
    dock.controller = _FakeController(am)

    aid = 0
    asset = am.assets[aid]
    pm = dock._load_thumbnail(aid, asset)
    assert isinstance(pm, QPixmap), f"type inattendu: {type(pm)}"
    assert not pm.isNull(), "QPixmap null (placeholder ou echec)"
    print("OK test_load_thumbnail_no_nameerror")


def test_avatar_returns_pil():
    from PIL import Image

    am = _make_am()
    av = am.avatar(0, size=24)
    assert av is not None, "avatar None"
    assert isinstance(av, Image.Image), f"type inattendu: {type(av)}"
    print("OK test_avatar_returns_pil")


if __name__ == "__main__":
    test_thumbnail_returns_pil()
    test_load_thumbnail_no_nameerror()
    test_avatar_returns_pil()
    print("ALL TESTS PASSED")
