"""Univers Vivant — point d'entree PyQt6.

Utilise le meme moteur que main.py, le meme SimulationController,
les memes snapshots et les memes commandes.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Ne pas forcer QT_QPA_PLATFORM a une valeur vide : Qt echouerait a
# charger le plugin de plateforme. Laisser l'environnement decider.


def main():
    print("[BOOT] debut main_qt")
    ap = argparse.ArgumentParser(description="Univers Vivant — interface PyQt6")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--speed", type=int, default=2)
    ap.add_argument("--blank", type=int, default=0)
    ap.add_argument("--procedural", type=int, default=1)
    ap.add_argument("--agents", type=int, default=60,
                    help="nombre d'habitants au depart (0 = monde sans vie)")
    ap.add_argument("--sheep", type=int, default=40)
    args = ap.parse_args()

    print("[BOOT] creation QApplication")
    from ui_qt.app import create_app
    app = create_app()
    print("[BOOT] QApplication creee")

    # Importer le moteur (pas de Pygame nécessaire pour le moteur lui-même)
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    from game.engine import build_world, build_world_blank, seed_life
    from game.simulation_controller import SimulationController

    print("[BOOT] chargement AssetManager")
    am = AssetManager(headless=True)
    am.discover()
    am.ensure_procedural_blocks()
    am.ensure_procedural_tools()
    _set_asset_manager(am)
    print("[BOOT] decouverte assets terminee")

    # Construire le monde
    print("[BOOT] construction du monde")
    if args.blank:
        world, sim = build_world_blank(am, args.seed)
    else:
        world, sim = build_world(am, args.seed, procedural=bool(args.procedural),
                                 start_paused=False)
        seed_life(world, sim, sim.rng, n_agents=args.agents, n_sheep=args.sheep)
    sim.speed = args.speed
    print("[BOOT] monde construit", world.g, "x", world.g,
          "habitants:", len(sim.agents), "moutons:", len(sim.sheep))

    from game.camera import Camera
    cam = Camera()
    import numpy as np
    _ys, _xs = np.nonzero(world.land)
    if len(_xs):
        from game.config import TILE
        cam.center_on(float(_xs.mean()) * TILE, float(_ys.mean()) * TILE)

    # Créer le controller
    print("[BOOT] controller cree")
    controller = SimulationController(sim, cam)

    # Créer la fenêtre
    print("[BOOT] creation MainWindow")
    from ui_qt.main_window import MainWindow
    window = MainWindow(controller, am)
    print("[BOOT] MainWindow creee")
    print("[BOOT] avant window.show()")
    window.show()
    print("[BOOT] apres window.show()")

    print("Interface PyQt6 demarree.")
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
