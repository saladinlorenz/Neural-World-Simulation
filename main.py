"""Un monde vivant observe par un scientifique : les habitants naissent sans
regles, decident avec leur reseau de neurones, et s'auto-organisent (ou se
destruisent)."""
import argparse
import atexit
import os
import sys

import numpy as np
import pygame

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game.assets_manager import AssetManager
from game.assets_api import _set_asset_manager
from game.camera import Camera, ZOOMS
from game.config import (GRID, SCREEN_H, SCREEN_W, SIM_HZ, TILE, VIEW_H, FPS)

# marge autour de tout l'écran
M = 3
from game.dashboard import Dashboard
from game.engine import build_world, build_world_blank, populate
from game.renderer import Renderer


def main():
    ap = argparse.ArgumentParser(description="Laboratoire d'émergence IA")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--headless", type=int, default=0, help="N ticks sans fenetre")
    ap.add_argument("--agents", type=int, default=0)
    ap.add_argument("--speed", type=int, default=2)
    ap.add_argument("--screenshot", type=str, default="")
    ap.add_argument("--auto", type=int, default=0, help="N ticks puis screenshot+quit")
    ap.add_argument("--blank", type=int, default=0, help="1 = monde vide tout eau, pas d'assets")
    ap.add_argument("--procedural", type=int, default=0, help="1 = génération procédurale d'îles (pas de PNG)")
    args = ap.parse_args()

    headless = args.headless > 0 or args.auto > 0
    if headless:
        os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    pygame.display.set_caption("Univers Vivant — IA émergente (laboratoire)")
    # centrer la fenêtre AVANT de la créer
    info = pygame.display.Info()
    ox = max(0, (info.current_w - SCREEN_W) // 2)
    oy = max(0, (info.current_h - SCREEN_H) // 2)
    os.environ["SDL_VIDEO_WINDOW_POS"] = f"{ox},{oy}"
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    if headless:
        screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.HIDDEN)

    print("Chargement des assets (/assets) ...")
    am = AssetManager(headless=False).discover()
    am.ensure_procedural_blocks()
    am.ensure_procedural_tools()
    _set_asset_manager(am)
    st = am.stats()
    print(f"  {st['discovered']} fichiers trouvés, {st['deduped']} uniques après "
          f"suppression des répétitions, {len(am.floors)} tilesets de sol.")

    # 1) Essayer de charger une sauvegarde
    from game.save import load_game as _auto_load
    _loaded_sim, _loaded_cam = _auto_load(am, slot=0)
    if _loaded_sim is not None:
        sim = _loaded_sim
        world = sim.w
        cam = _loaded_cam if _loaded_cam is not None else Camera()
        sim.log("Sauvegarde restaurée.", (108, 208, 128), "monde")
    else:
        # 2) Pas de sauvegarde → monde frais
        world, sim = build_world_blank(am, args.seed) if args.blank else build_world(am, args.seed, procedural=True)
        sim.speed = args.speed
        cam = Camera()
        _ys, _xs = np.nonzero(world.land)
        if len(_xs):
            cam.center_on(float(_xs.mean()) * TILE, float(_ys.mean()) * TILE)
        else:
            cam.center_on(float(GRID // 2) * TILE, float(GRID // 2) * TILE)
        if args.agents > 0 and not args.blank:
            ys, xs = np.nonzero(world.land)
            i = int(sim.rng.integers(len(xs)))
            hx, hy = int(xs[i]), int(ys[i])
            for _ in range(args.agents):
                sim.spawn_agent(x=hx * TILE + sim.rng.normal(0, 5),
                                y=hy * TILE + sim.rng.normal(0, 5))
    ren = Renderer(am)
    dash = Dashboard(am)
    try:
        if am.ui.get("cursors"):
            csurf = am.surface(am.ui["cursors"][0], 0, 1.0)
            pygame.mouse.set_cursor(pygame.cursors.Cursor((8, 8), csurf))
    except Exception as exc:
        print(f"[cursor] curseur personnalisé indisponible : {exc}", file=sys.stderr)

    # ---- mode headless
    if args.headless > 0 and args.auto == 0:
        for i in range(args.headless):
            sim.tick()
            if i % 120 == 0:
                p, sh, it = sim.natural_pop()
                print(f"tick {i:5d} pop={p:3d} sheep={sh:3d} items={it:4d} "
                      f"births={sim.stats['births']} deaths={sim.stats['deaths']} "
                      f"builds={sim.stats['builds']} villages={sim.stats['villages']} "
                      f"attacks={sim.stats['attacks']} gives={sim.stats['gives']}")
        p, sh, it = sim.natural_pop()
        print("FINAL:", dict(pop=p, sheep=sh, items=it, **{k: v for k, v in sim.stats.items()}))
        pygame.quit()
        return

    # ---- mode auto (N ticks + screenshot + quit)
    if args.auto > 0:
        for i in range(args.auto):
            sim.tick()
            if i % 120 == 0:
                p, sh, it = sim.natural_pop()
                print(f"tick {i:5d} pop={p:3d} sheep={sh:3d} items={it:4d} "
                      f"births={sim.stats['births']} deaths={sim.stats['deaths']} "
                      f"builds={sim.stats['builds']} villages={sim.stats['villages']} "
                      f"attacks={sim.stats['attacks']} gives={sim.stats['gives']}")
        sim.pop_hist.append(len(sim.agents))
        ui = {"tile": (GRID // 2, GRID // 2), "ghost": False, "asset": dash.asset,
              "mode": dash.mode, "agent": sim.selected}
        vr = dash.view_rect()
        view_surf = pygame.Surface((vr.width, vr.height))
        ren.draw(view_surf, sim, cam, ui)
        screen.fill((227, 232, 236))
        screen.blit(view_surf, (vr.x, vr.y))
        dash.draw(screen, sim, cam)
        # cadre visible — dessiné EN DERNIER par-dessus tout
        pygame.draw.rect(screen, (180, 186, 196), (0, 0, SCREEN_W, SCREEN_H), 2)
        path = args.screenshot or "screenshot.png"
        pygame.image.save(screen, path)
        p, sh, it = sim.natural_pop()
        print("FINAL:", dict(pop=p, sheep=sh, items=it,
                              **{k: v for k, v in sim.stats.items()}))
        print("screenshot:", path)
        pygame.quit()
        return

    # ---- mode visuel (fenetre interactive)
    clock = pygame.time.Clock()
    show_legend = [False]
    acc = 0.0
    running = True
    panning = None
    ldrag_tile = None
    while running:
        evs = pygame.event.get()
        for ev in evs:
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if dash.handle_event(ev, sim):
                    continue
                if dash.focus_search or dash.hab_focus:
                    continue
                if ev.key == pygame.K_ESCAPE:
                    running = False
                elif ev.key == pygame.K_SPACE:
                    sim.paused = not sim.paused
                elif ev.key == pygame.K_g:
                    ren.show_grid = not ren.show_grid
                elif ev.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    sim.speed = min(8, sim.speed + 1)
                elif ev.key == pygame.K_MINUS:
                    sim.speed = max(1, sim.speed - 1)
                elif ev.key == pygame.K_f:
                    dash.follow = not dash.follow
                elif ev.key == pygame.K_v:
                    show_legend[0] = not show_legend[0]
                elif ev.key == pygame.K_LEFTBRACKET:
                    cam.tilt = max(40.0, cam.tilt - 5)
                elif ev.key == pygame.K_RIGHTBRACKET:
                    cam.tilt = min(70.0, cam.tilt + 5)
                elif ev.key in (pygame.K_w, pygame.K_UP):
                    cam.y -= 140 / (cam.zoom * cam.ys)
                elif ev.key in (pygame.K_s, pygame.K_DOWN):
                    cam.y += 140 / (cam.zoom * cam.ys)
                elif ev.key in (pygame.K_a, pygame.K_LEFT):
                    cam.x -= 140 / cam.zoom
                elif ev.key in (pygame.K_d, pygame.K_RIGHT):
                    cam.x += 140 / cam.zoom
                elif ev.key == pygame.K_F5:
                    from game.save import save_game as _save
                    path, sz = _save(sim, cam, slot=0)
                    sim.log(f"Sauvegardé ({sz:.1f} Mo)", (108, 208, 128), "monde")
                elif ev.key == pygame.K_F9:
                    from game.save import load_game as _load
                    new_sim, new_cam = _load(am, slot=0)
                    if new_sim is not None:
                        sim = new_sim
                        if new_cam is not None:
                            cam = new_cam
                        world = sim.w
                        sim.log("Partie chargée.", (108, 208, 128), "monde")
                    else:
                        sim.log("Aucune sauvegarde.", (228, 98, 98), "monde")
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if dash.handle_event(ev, sim):
                    if getattr(dash, '_needs_save', False):
                        dash._needs_save = False
                        from game.save import save_game as _auto_save
                        _auto_save(sim, cam, slot=0)
                    continue
                vr = dash.view_rect()
                mx = ev.pos[0]
                if ev.button == 1 and vr.collidepoint((mx, ev.pos[1])):
                    dash.apply_map_tool(sim, cam, 1)
                    if getattr(dash, '_needs_save', False):
                        dash._needs_save = False
                        from game.save import save_game as _auto_save
                        _auto_save(sim, cam, slot=0)
                    ldrag_tile = dash.hover_tile
                elif ev.button == 3:
                    panning = ev.pos
                elif ev.button == 2:
                    dash.apply_map_tool(sim, cam, 2)
            elif ev.type == pygame.MOUSEBUTTONUP:
                dash.handle_event(ev, sim)
                if ev.button == 3:
                    panning = None
                if ev.button == 1:
                    ldrag_tile = None
            elif ev.type == pygame.MOUSEMOTION:
                if panning:
                    dx, dy = ev.pos[0] - panning[0], ev.pos[1] - panning[1]
                    cam.x -= dx / cam.zoom
                    cam.y -= dy / (cam.zoom * cam.ys)
                    cam.clamp()
                    panning = ev.pos
                elif ldrag_tile and dash.view_rect().collidepoint(ev.pos):
                    dash.set_ghost(cam)
                    if dash.hover_tile != ldrag_tile:
                        dash.apply_map_tool(sim, cam, 1)
                        ldrag_tile = dash.hover_tile
            elif ev.type == pygame.MOUSEWHEEL:
                if not dash.handle_event(ev, sim):
                    mx, my = pygame.mouse.get_pos()
                    vr = dash.view_rect()
                    if vr.collidepoint((mx, my)):
                        closest = min(range(len(ZOOMS)), key=lambda i: abs(ZOOMS[i] - cam.zoom))
                        idx = max(0, min(len(ZOOMS) - 1, closest + (1 if ev.y > 0 else -1)))
                        cam.set_zoom(ZOOMS[idx], anchor_screen=(mx - vr.x, my))

        # actions du dashboard
        if dash.action:
            kind, val = dash.action
            dash.action = None
            if kind == "pause":
                sim.paused = not sim.paused
            elif kind == "step":
                sim.tick()
            elif kind == "speed":
                sim.speed = min(8, max(1, sim.speed + val))
            elif kind == "speed_set":
                sim.speed = max(1, min(8, val))
            elif kind == "spawn":
                for _ in range(val):
                    sim.spawn_agent()
            elif kind == "spawn_sheep":
                for _ in range(val):
                    sim.spawn_sheep()
            elif kind == "create_tool":
                from game.config import TOOL_RECIPES
                path = dash.tool_editor.save_png("assets/tools_custom", dash.tool_editor_kind)
                aid = am.register_custom_tool(path, dash.tool_editor_kind, label=dash.tool_editor.name)
                if sim.selected and sim.selected.alive:
                    sim.selected.tool = aid
                    sim.selected.tool_durability = TOOL_RECIPES.get(dash.tool_editor_kind, {}).get("durability", 30)
                    sim.log(f"{sim.selected.name} recoit un outil fait main : {dash.tool_editor.name}.",
                            (248, 208, 98), "economie")
                dash.tool_editor.clear()
            elif kind == "grid":
                ren.show_grid = not ren.show_grid
            elif kind == "legend":
                show_legend[0] = not show_legend[0]
            elif kind == "reseed":
                populate(world, am, sim.rng, dense=False)
                sim.log("Nouvelle pluie de ressources sur la carte.", (248, 208, 98), "monde")
            elif kind == "reset":
                world, sim = build_world(am, int(sim.rng.integers(1 << 30)), procedural=True)
                sim.speed = args.speed
                dash.hover_tile = (0, 0)
            elif kind == "save_game":
                from game.save import save_game as _save
                path, sz = _save(sim, cam, slot=0)
                sim.log(f"Sauvegardé: {path} ({sz:.1f} Mo)", (108, 208, 128), "monde")
            elif kind == "load_game":
                from game.save import load_game as _load
                new_sim, new_cam = _load(am, slot=0)
                if new_sim is not None:
                    sim = new_sim
                    if new_cam is not None:
                        cam = new_cam
                    world = sim.w
                    sim.log("Partie chargée.", (108, 208, 128), "monde")
                else:
                    sim.log("Aucune sauvegarde trouvée.", (228, 98, 98), "monde")

        if not sim.paused:
            acc += sim.speed * SIM_HZ / FPS
            n = 0
            while acc >= 1.0 and n < 8:
                sim.tick()
                acc -= 1.0
                n += 1
        else:
            acc = 0.0
            if sim.selected and not sim.selected.alive:
                sim.selected = None
        if sim.selected and not sim.selected.alive:
            sim.selected = None
        if dash.follow and sim.selected and sim.selected.alive:
            cam.center_on(sim.selected.x, sim.selected.y)

        # auto-tilt : top-down (0°) en zoom arrière, 2.5D (55°) à partir de ×1.5
        _t_min, _t_max = 0.0, 55.0
        _z_lo, _z_hi = 0.25, 1.5
        _z_clamped = max(_z_lo, min(_z_hi, cam.zoom))
        _target_tilt = _t_min + (_t_max - _t_min) * (_z_clamped - _z_lo) / (_z_hi - _z_lo)
        cam.tilt = cam.tilt + (_target_tilt - cam.tilt) * 0.12

        dash.set_ghost(cam)
        mx, my = pygame.mouse.get_pos()
        vr = dash.view_rect()
        in_map = vr.collidepoint((mx, my))
        ui = {"tile": dash.hover_tile, "ghost": dash.hover_tile[0] > 0 and in_map,
              "asset": dash.asset, "mode": dash.mode, "agent": sim.selected,
              "legend": show_legend[0], "brush": dash.brush_radius(),
              "view_rect": pygame.Rect(0, 0, vr.width, vr.height)}
        view_surf = pygame.Surface((vr.width, vr.height))
        ren.draw(view_surf, sim, cam, ui)
        screen.fill((227, 232, 236))
        screen.blit(view_surf, (vr.x, vr.y))
        dash.draw(screen, sim, cam)
        # cadre visible — dessiné EN DERNIER par-dessus tout
        pygame.draw.rect(screen, (180, 186, 196), (0, 0, SCREEN_W, SCREEN_H), 2)
        pygame.display.flip()
        clock.tick(FPS)

    from game.save import save_game as _auto_save
    try:
        _auto_save(sim, cam, slot=0)
    except Exception:
        import sys
        print(f"[auto-save] {sys.exc_info()[1]}", file=sys.stderr)
    pygame.quit()


if __name__ == "__main__":
    main()
