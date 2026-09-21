"""Univers Vivant — point d'entree PyQt6.

Utilise le meme moteur que main.py, le meme SimulationController,
les memes snapshots et les memes commandes.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ["QT_QPA_PLATFORM"] = os.environ.get("QT_QPA_PLATFORM", "")


def main():
    ap = argparse.ArgumentParser(description="Univers Vivant — interface PyQt6")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--speed", type=int, default=2)
    ap.add_argument("--blank", type=int, default=0)
    ap.add_argument("--procedural", type=int, default=1)
    args = ap.parse_args()

    from ui_qt.app import create_app
    app = create_app()

    # Importer le moteur (pas de Pygame nécessaire pour le moteur lui-même)
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    from game.engine import build_world, build_world_blank
    from game.simulation_controller import SimulationController

    print("Chargement des assets...")
    am = AssetManager(headless=True)
    am.discover()
    am.ensure_procedural_blocks()
    am.ensure_procedural_tools()
    _set_asset_manager(am)

    # Construire le monde
    if args.blank:
        world, sim = build_world_blank(am, args.seed)
    else:
        world, sim = build_world(am, args.seed, procedural=bool(args.procedural))
    sim.speed = args.speed

    from game.camera import Camera
    cam = Camera()
    import numpy as np
    _ys, _xs = np.nonzero(world.land)
    if len(_xs):
        from game.config import TILE
        cam.center_on(float(_xs.mean()) * TILE, float(_ys.mean()) * TILE)

    # Créer le controller
    controller = SimulationController(sim, cam)

    # Créer la fenêtre
    from ui_qt.main_window import MainWindow
    window = MainWindow(controller, am)
    window.show()

    print("Interface PyQt6 demarree.")
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
