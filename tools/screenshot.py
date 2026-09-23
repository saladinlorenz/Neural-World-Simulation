"""Capture d'écran hors écran de l'interface PyQt6.

Sert à produire les visuels du README sans ouvrir de fenêtre :

    python tools/screenshot.py --out docs/img/hero.png --ticks 900 --zoom 1.3
    python tools/screenshot.py --out docs/img/ui.png --window --zoom 0.9

Le monde est construit et peuplé, la simulation avance de ``--ticks`` pas,
puis la caméra est centrée sur la plus forte densité d'habitants.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


def _best_spot(sim, cell_tiles=16, window=2):
    """Centre du secteur le plus vivant : habitants d'abord, décor ensuite.

    Un simple cluster d'habitants peut tomber en pleine prairie nue ; pour la
    capture on veut aussi des arbres, des rochers et des cultures autour.
    Mais une forêt dense (256 tuiles de contenu) écrasait tout : la
    contribution du contenu est donc plafonnée par cellule, et chantiers,
    dépôts et cultures — signes d'un village — pèsent lourd.
    """
    import numpy as np

    from game.config import GRID, TILE

    w = sim.w
    step = max(1, int(cell_tiles))
    dim = GRID // step + 2
    score = np.zeros((dim, dim), dtype=np.float64)

    def _add(points, wx, wy, weight):
        cx = np.clip((np.asarray(wx) // TILE // step).astype(int), 0, dim - 1)
        cy = np.clip((np.asarray(wy) // TILE // step).astype(int), 0, dim - 1)
        np.add.at(points, (cy, cx), weight)

    agents = [a for a in sim.agents if a.alive]
    if agents:
        _add(score, [a.x for a in agents], [a.y for a in agents], 10.0)
    sheep = [s for s in sim.sheep if s.alive]
    if sheep:
        _add(score, [s.x for s in sheep], [s.y for s in sheep], 3.0)

    ys, xs = np.nonzero(w.content >= 0)
    if ys.size:
        deco = np.zeros((dim, dim), dtype=np.float64)
        _add(deco, xs * TILE, ys * TILE, 1.0)
        score += np.minimum(deco, 6.0)

    for table, weight in ((getattr(w, "sites", {}), 5.0),
                          (getattr(w, "storages", {}), 4.0),
                          (getattr(w, "crop_plots", {}), 4.0)):
        for key in table:
            try:
                tx, ty = key[0], key[1]
            except (IndexError, TypeError):
                continue
            _add(score, [tx * TILE], [ty * TILE], weight)

    box = np.zeros_like(score)
    for dy in range(-window, window + 1):
        for dx in range(-window, window + 1):
            box += np.roll(np.roll(score, dy, 0), dx, 1)
    cy, cx = np.unravel_index(int(np.argmax(box)), box.shape)

    # Recentre sur le centroide reel des entites de la fenetre gagnante :
    # la cellule argmax peut tomber au bord du village.
    half = (window + 1) * step * TILE
    wx = (cx + 0.5) * step * TILE
    wy = (cy + 0.5) * step * TILE
    pts = []
    for a in agents:
        if abs(a.x - wx) <= half and abs(a.y - wy) <= half:
            pts.append((a.x, a.y, 3.0))
    for s in sheep:
        if abs(s.x - wx) <= half and abs(s.y - wy) <= half:
            pts.append((s.x, s.y, 1.0))
    for table, weight in ((getattr(w, "sites", {}), 2.0),
                          (getattr(w, "storages", {}), 2.0),
                          (getattr(w, "crop_plots", {}), 2.0)):
        for key in table:
            try:
                tx, ty = key[0], key[1]
            except (IndexError, TypeError):
                continue
            px, py = tx * TILE, ty * TILE
            if abs(px - wx) <= half and abs(py - wy) <= half:
                pts.append((px, py, weight))
    if pts:
        total = sum(p[2] for p in pts)
        wx = sum(p[0] * p[2] for p in pts) / total
        wy = sum(p[1] * p[2] for p in pts) / total
    print(f"[shot] secteur choisi : cellule ({cx}, {cy}) score {box[cy, cx]:.0f}")
    return float(wx), float(wy)


def _spawn_cluster(sim, cx, cy, n_agents, n_sheep, radius_tiles=26):
    """Pose un village : spirale d'or autour d'un centre, sur terre ferme.

    ``seed_life`` disperse les naissances sur les 1 000 x 1 000 tuiles :
    aucune fenetre de capture ne montrerait alors de societe. La spirale
    garantit un groupe dense sans empilement exact.
    """
    import math

    from game.config import TILE

    w = sim.w
    golden = 2.399963229728653

    def _point(i, n, radius):
        r = radius * math.sqrt((i + 0.5) / max(1, n))
        t = i * golden
        return cx + r * math.cos(t), cy + r * math.sin(t)

    def _land_point(i, n, radius):
        for attempt in range(14):
            px, py = _point(i + attempt * 0.37, n, radius + attempt * 2)
            tx, ty = int(px), int(py)
            if 0 <= tx < w.g and 0 <= ty < w.g and w.land[ty, tx] \
                    and not w.blocked[ty, tx]:
                return px * TILE, py * TILE
        return None

    for i in range(max(0, n_agents)):
        pt = _land_point(i, n_agents, radius_tiles)
        if pt is not None:
            sim.spawn_agent(x=pt[0], y=pt[1])
    for i in range(max(0, n_sheep)):
        pt = _land_point(i, n_sheep, radius_tiles + 12)
        if pt is not None:
            sim.spawn_sheep(x=pt[0], y=pt[1])


def _load_fonts():
    """Le plugin offscreen n'expose aucune police : texte = carrés vides.

    On enregistre explicitement une police système pour les captures.
    """
    from PyQt6.QtGui import QFontDatabase

    if QFontDatabase.families():
        return
    for candidate in ("C:/Windows/Fonts/segoeui.ttf",
                      "C:/Windows/Fonts/arial.ttf",
                      "C:/Windows/Fonts/calibri.ttf"):
        if os.path.exists(candidate):
            QFontDatabase.addApplicationFont(candidate)
            return


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="docs/img/hero.png")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--ticks", type=int, default=900)
    parser.add_argument("--agents", type=int, default=160)
    parser.add_argument("--sheep", type=int, default=70)
    parser.add_argument("--monsters", type=int, default=8)
    parser.add_argument("--zoom", type=float, default=1.3)
    parser.add_argument("--tilt", type=float, default=62.0)
    parser.add_argument("--width", type=int, default=1600)
    parser.add_argument("--height", type=int, default=900)
    parser.add_argument("--window", action="store_true",
                        help="capturer la fenêtre entière au lieu de la carte")
    parser.add_argument("--blank", action="store_true")
    parser.add_argument("--no-hud", action="store_true",
                        help="sans legende ni minimap : visuel pur du monde")
    args = parser.parse_args()

    from PyQt6.QtWidgets import QApplication

    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    from game.camera import Camera
    from game.config import TILE
    from game.engine import build_world, build_world_blank, seed_life
    from game.simulation_controller import SimulationController

    app = QApplication.instance() or QApplication(sys.argv)
    _load_fonts()

    am = AssetManager(headless=True)
    am.discover()
    am.ensure_procedural_blocks()
    am.ensure_procedural_tools()
    _set_asset_manager(am)

    if args.blank:
        world, sim = build_world_blank(am, args.seed)
        center = None
    else:
        world, sim = build_world(am, args.seed, procedural=True)
        # Le decor d'abord (foret, cultures), puis le village groupe dessus :
        # des naissances eparpillees donneraient une carte vide au centre.
        decor = _best_spot(sim)
        center = decor
        _spawn_cluster(sim, decor[0] / TILE, decor[1] / TILE,
                       args.agents, args.sheep)
        for _ in range(max(0, args.monsters)):
            sim.spawn_monster()

    sim.paused = True
    for i in range(max(0, args.ticks)):
        sim.tick()
        if i and i % 300 == 0:
            print(f"[shot] tick {i} : habitants={len(sim.agents)}")
    w = sim.w
    print(f"[shot] tick={w.tick} habitants={len(sim.agents)} "
          f"moutons={len(sim.sheep)} monstres={len(sim.monsters)} "
          f"objets={len(w.items)} chantiers={len(w.sites)} "
          f"depots={len(w.storages)} cultures={len(w.crop_plots)} "
          f"feux={int((w.fire > 0).sum())}")

    # Le village a pu dériver pendant les ticks : on recentre sur le secteur
    # reellement peuple APRES simulation, pas sur le decor d'avant naissance.
    if not args.blank:
        center = _best_spot(sim)

    cam = Camera()
    cam.zoom = args.zoom
    cam.tilt = args.tilt
    if center is not None:
        cam.x, cam.y = center
    controller = SimulationController(sim, cam)

    from ui_qt.main_window import MainWindow

    window = MainWindow(controller, am)
    window.resize(args.width + 520, args.height + 240)
    window.show()
    app.processEvents()

    view = window._map
    view.setFixedSize(args.width, args.height)
    view.auto_tilt = False
    if args.no_hud:
        view.show_legend = False
        view.debug_no_minimap = True
    view.transform.zoom = args.zoom
    view.transform.tilt = args.tilt
    if center is not None:
        view.transform.center_on(center[0], center[1], view.width(), view.height(),
                                 float(world.g * TILE))
    app.processEvents()

    # Deux passes : la première remplit les caches (terrain, sprites).
    target = window if args.window else view
    target.grab()
    pixmap = target.grab()

    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    pixmap.save(args.out, "PNG")
    print(f"[shot] écrit {args.out} ({pixmap.width()}x{pixmap.height()})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
