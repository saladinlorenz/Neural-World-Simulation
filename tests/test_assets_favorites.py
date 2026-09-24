"""Lot G — favoris assets persistants (QSettings roundtrip)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ["QT_QPA_PLATFORM"] = "offscreen"

_SETTINGS_KEY = "assets/favorites"


_APP = None


def _app():
    global _APP
    from PyQt6.QtWidgets import QApplication
    _APP = QApplication.instance()
    if _APP is None:
        _APP = QApplication(sys.argv)
    return _APP


def _clean():
    from ui_qt.theme.theme import get_settings
    get_settings().remove(_SETTINGS_KEY)


def test_favorites_roundtrip():
    _app()
    from ui_qt.docks.assets_dock import AssetsDock
    from ui_qt.theme.theme import get_settings

    _clean()
    try:
        dock = AssetsDock(None)
        assert dock._favs == []
        dock._favs = [3, 7, 11]
        dock.save_favorites()

        dock2 = AssetsDock(None)
        assert dock2._favs == [3, 7, 11]
    finally:
        _clean()


def test_favorites_robust_to_bad_values():
    _app()
    from ui_qt.docks.assets_dock import AssetsDock
    from ui_qt.theme.theme import get_settings

    _clean()
    try:
        get_settings().setValue(_SETTINGS_KEY, ["4", "oops", 9])
        dock = AssetsDock(None)
        assert dock._favs == [4, 9]

        get_settings().setValue(_SETTINGS_KEY, 5)
        dock2 = AssetsDock(None)
        assert dock2._favs == [5]
    finally:
        _clean()


if __name__ == "__main__":
    test_favorites_roundtrip()
    test_favorites_robust_to_bad_values()
    print("ALL TESTS PASSED")
