"""Tests Qt smoke — valide le demarrage de l'interface PyQt6.

Lance QApplication en mode offscreen, cree la fenetre,
et valide que les docks et modeles se creent correctement.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ["QT_QPA_PLATFORM"] = "offscreen"


def _make_controller():
    """Construit un Sim + SimulationController pour les tests."""
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    from game.engine import build_world
    from game.simulation_controller import SimulationController

    am = AssetManager(headless=True)
    am.discover()
    _set_asset_manager(am)
    world, sim = build_world(am, seed=42, procedural=True)
    return SimulationController(sim)


class TestQtModels(unittest.TestCase):
    """Tests des modeles Qt sans creer de QApplication."""

    @classmethod
    def setUpClass(cls):
        cls.controller = _make_controller()

    def test_population_model(self):
        from ui_qt.models.population_model import PopulationModel
        from game.ui_snapshots import population_snapshot
        model = PopulationModel()
        snap = population_snapshot(self.controller.sim)
        model.set_snapshot(snap)
        self.assertEqual(model.rowCount(), len(snap))
        self.assertEqual(model.columnCount(), 10)
        if model.rowCount() > 0:
            idx = model.index(0, 0)
            self.assertIsNotNone(model.data(idx))

    def test_journal_model(self):
        from ui_qt.models.journal_model import JournalModel
        from game.ui_snapshots import journal_snapshot
        model = JournalModel()
        self.controller.sim.log("Test entry", (255, 0, 0), "monde")
        snap = journal_snapshot(self.controller.sim)
        model.set_snapshot(snap)
        self.assertGreater(model.rowCount(), 0)

    def test_anima_model_empty(self):
        from ui_qt.models.anima_model import AnimaModel
        model = AnimaModel()
        model.set_snapshot(None)
        self.assertEqual(model.rowCount(), 0)

    def test_society_model(self):
        from ui_qt.models.society_model import SocietyModel
        from game.ui_snapshots import society_snapshot
        model = SocietyModel()
        snap = society_snapshot(self.controller.sim)
        model.set_snapshot(snap)
        self.assertGreater(model.rowCount(), 0)

    def test_assets_model(self):
        from ui_qt.models.assets_model import AssetsModel
        model = AssetsModel()
        model.set_snapshot([{"id": 1, "nom": "test", "categorie": "tree",
                             "role": "tree", "placable": True}])
        self.assertEqual(model.rowCount(), 1)


class TestQtSmoke(unittest.TestCase):
    """Tests de demarrage de QApplication et MainWindow."""

    @classmethod
    def setUpClass(cls):
        from PyQt6.QtWidgets import QApplication
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication(sys.argv)
        cls.controller = _make_controller()

    def test_app_exists(self):
        from PyQt6.QtWidgets import QApplication
        self.assertIsNotNone(QApplication.instance())

    def test_main_window_creation(self):
        from ui_qt.main_window import MainWindow
        win = MainWindow(self.controller)
        self.assertIsNotNone(win)
        self.assertEqual(win.windowTitle(), "Univers Vivant — PyQt6")
        win.close()

    def test_docks_creation(self):
        from ui_qt.main_window import MainWindow
        from ui_qt.docks.population_dock import PopulationDock
        from ui_qt.docks.inspector_dock import InspectorDock
        from ui_qt.docks.journal_dock import JournalDock
        from ui_qt.docks.society_dock import SocietyDock
        win = MainWindow(self.controller)
        self.assertIsInstance(win._pop_dock, PopulationDock)
        self.assertIsInstance(win._inspector_dock, InspectorDock)
        self.assertIsInstance(win._journal_dock, JournalDock)
        self.assertIsInstance(win._society_dock, SocietyDock)
        win.close()

    def test_map_view_creation(self):
        from ui_qt.map.map_view import MapView
        from ui_qt.main_window import MainWindow
        win = MainWindow(self.controller)
        self.assertIsInstance(win._map, MapView)
        win.close()

    def test_refresh_no_crash(self):
        from ui_qt.main_window import MainWindow
        win = MainWindow(self.controller)
        # Refresh tous les docks ne doit pas planter
        win._pop_dock.refresh()
        win._inspector_dock.refresh()
        win._journal_dock.refresh()
        win._society_dock.refresh()
        win.close()

    def test_execute_command(self):
        result = self.controller.execute({"kind": "set_speed", "speed": 4})
        self.assertTrue(result["ok"])
        self.assertEqual(self.controller.sim.speed, 4)
        self.controller.sim.speed = 2


class TestMapAPI(unittest.TestCase):
    """Tests de mapapi.py (Lot 10)."""

    @classmethod
    def setUpClass(cls):
        cls.controller = _make_controller()

    def test_map_transform(self):
        from game.mapapi import MapTransform
        t = MapTransform(x=0, y=0, zoom=0.25, tilt=55.0)
        sx, sy = t.to_screen(100, 100)
        wx, wy = t.to_world(sx, sy)
        self.assertAlmostEqual(wx, 100, delta=1)
        self.assertAlmostEqual(wy, 100, delta=1)

    def test_visible_tiles(self):
        from game.mapapi import MapTransform
        t = MapTransform(zoom=0.25)
        x0, y0, x1, y1 = t.visible_tiles(32, 128)
        self.assertGreater(x1, x0)
        self.assertGreater(y1, y0)

    def test_map_visible_data(self):
        from game.mapapi import MapTransform, map_visible_data
        t = MapTransform(zoom=0.25)
        data = map_visible_data(self.controller.sim, t, 800, 600)
        self.assertIn("terrain", data)
        self.assertIn("agents", data)
        self.assertIn("tick", data)


if __name__ == "__main__":
    unittest.main()
