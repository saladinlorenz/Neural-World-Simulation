#!/usr/bin/env python3
"""LIVE GUI PERFORMANCE DIAGNOSIS TOOL

Profiles the real PyQt6 application with actual rendering, UI, and simulation.
Runs cProfile on the main thread while Qt event loop executes.
Outputs detailed diagnostic reports.

Usage:
    python tools/diagnose_live_app.py --seconds 15 --agents 4 --sheep 0 --seed 7
"""
from __future__ import annotations

import argparse
import cProfile
import json
import os
import pstats
import sys
import time
import traceback
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Live GUI Performance Diagnosis")
    parser.add_argument("--seconds", type=int, default=15,
                        help="Real-time seconds to profile")
    parser.add_argument("--agents", type=int, default=4,
                        help="Initial agent count")
    parser.add_argument("--sheep", type=int, default=0,
                        help="Initial sheep count")
    parser.add_argument("--monsters", type=int, default=0,
                        help="Initial monster count")
    parser.add_argument("--seed", type=int, default=7,
                        help="World seed")
    parser.add_argument("--speed", type=int, default=1,
                        help="Simulation speed multiplier")
    parser.add_argument("--blank", action="store_true",
                        help="Use flat blank world instead of procedural")
    parser.add_argument("--headless", action="store_true",
                        help="Run in headless mode (offscreen rendering)")
    return parser.parse_args()


def classify_function(file_path: str, func_name: str) -> str:
    """Classify a function into a diagnosis group."""
    fp = file_path.lower()
    fn = func_name.lower()

    # Exclude shutdown/process functions from runtime bottleneck analysis
    if any(k in fn for k in ("exec", "closeEvent", "_autosave", "autosave", "save_game", "fsync", "pickle")):
        return "excluded_shutdown"

    if "simulation" in fp:
        if any(k in fn for k in ("perceive", "local_density", "sense", "vision")):
            return "agent perception"
        if any(k in fn for k in ("local_bfs", "path", "bfs", "find_path")):
            return "pathfinding"
        if any(k in fn for k in ("step_fire", "step", "regrow", "fire")):
            return "world simulation"
        return "simulation"

    if "world" in fp and ("step" in fn or "fire" in fn or "regrow" in fn):
        return "world simulation"

    if "worldgen" in fp or "mapcache" in fp:
        return "terrain/cache"

    if "mapview" in fp or "effectslayer" in fp:
        if "effect" in fn:
            return "effects rendering"
        return "map rendering"

    if "docks" in fp or "models" in fp:
        return "UI docks/models"

    if "mainwindow" in fp or "main_window" in fp:
        return "main UI loop"

    if "brain" in fp:
        return "neural decision"

    if "diagnose_live_app" in fp:
        return "diagnostic overhead"

    return "unknown"


def run_live_profile(args: argparse.Namespace) -> Tuple[Dict[str, Any], str]:
    """Run the live GUI profile and return metrics + profile data."""

    # Setup output directory
    out_dir = ROOT / "data" / "profiling"
    out_dir.mkdir(parents=True, exist_ok=True)

    prof_file = out_dir / "live_gui_profile.prof"
    json_file = out_dir / "live_gui_diagnosis.json"
    txt_file = out_dir / "live_gui_diagnosis.txt"

    # Import Qt and app components
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import QTimer, Qt
    from PyQt6.QtGui import QOffscreenSurface, QSurfaceFormat
    from ui_qt.app import create_app
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    from game.engine import build_world, build_world_blank, seed_life
    from game.simulation_controller import SimulationController
    from game.camera import Camera
    from game.config import TILE
    import numpy as np

    # Create QApplication
    app = create_app()
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

    # Setup offscreen surface for headless mode
    offscreen_surface = None
    if args.headless:
        fmt = QSurfaceFormat()
        fmt.setRenderableType(QSurfaceFormat.RenderableType.OpenGL)
        offscreen_surface = QOffscreenSurface()
        offscreen_surface.setFormat(fmt)
        offscreen_surface.create()
        if not offscreen_surface.isValid():
            print("Warning: Offscreen surface not valid, falling back to visible mode")
            args.headless = False

    # Load assets
    am = AssetManager(headless=args.headless)
    am.discover()
    am.ensure_procedural_blocks()
    am.ensure_procedural_tools()
    _set_asset_manager(am)

    # Build world
    if args.blank:
        world, sim = build_world_blank(am, args.seed)
    else:
        world, sim = build_world(am, args.seed,
                                 procedural=True,
                                 start_paused=False)
        seed_life(world, sim, sim.rng, n_agents=args.agents,
                  n_sheep=args.sheep)

    # Add monsters if requested
    for _ in range(args.monsters):
        sim.spawn_monster()

    # Create camera centered on land
    cam = Camera()
    _ys, _xs = np.nonzero(world.land)
    if len(_xs):
        cam.center_on(float(_xs.mean()) * TILE, float(_ys.mean()) * TILE)

    sim.speed = args.speed

    # Create controller and window
    controller = SimulationController(sim, cam)
    from ui_qt.main_window import MainWindow
    window = MainWindow(controller, am)

    if not args.headless:
        window.show()
    else:
        # In headless mode, we still need the widget to be "realized"
        # but we don't call show(). We'll trigger paint manually.
        window._map.resize(1280, 720)

    # Wait for window to be fully shown and first paint
    QApplication.processEvents()
    time.sleep(0.5)

    # Capture initial counters for fallback calculation
    initial_tick = sim.w.tick if hasattr(sim, 'w') else 0
    initial_rendered_frames = 0
    if hasattr(window, '_map') and hasattr(window._map, 'rendered_frames'):
        initial_rendered_frames = window._map.rendered_frames

    # Metrics collection from real MainWindow counters
    metrics = {
        "fps_map": [],
        "tps_sim": [],
        "sim_ms": [],
        "ui_ms": [],
        "render_ms": [],
    }

    def collect_metrics():
        # Use real MainWindow.perf and map counters
        if hasattr(window, '_map'):
            map_view = window._map
            perf = getattr(getattr(controller, 'sim', None), 'perf', None)
            if perf:
                sim_avg = perf.average("sim")
                ui_avg = perf.average("ui")
                render_avg = perf.average("render")
                if sim_avg is not None:
                    metrics["sim_ms"].append(sim_avg)
                if ui_avg is not None:
                    metrics["ui_ms"].append(ui_avg)
                if render_avg is not None:
                    metrics["render_ms"].append(render_avg)
            # FPS from rendered_frames (cumulative delta)
            if hasattr(map_view, 'rendered_frames'):
                metrics["fps_map"].append(map_view.rendered_frames)
                # DON'T reset - we want cumulative for final calc
        # TPS from MainWindow's tracked tps
        if hasattr(window, 'actual_tps') and window.actual_tps:
            metrics["tps_sim"].append(window.actual_tps)
        elif hasattr(window, 'actual_fps') and window.actual_fps:
            # MainWindow may track fps instead
            pass

    # Timer for metrics collection (1 Hz)
    metric_timer = QTimer()
    metric_timer.timeout.connect(collect_metrics)
    metric_timer.start(1000)

    # In headless mode, still let the real MainWindow QTimer drive everything.
    # MainWindow already has a QTimer for ticks and map updates.
    # We just need to keep the event loop alive.
    # No artificial trigger_paint, no manual processEvents loops.

    # Auto-close timer
    close_timer = QTimer()
    close_timer.setSingleShot(True)
    close_timer.timeout.connect(app.quit)
    close_timer.start(args.seconds * 1000)

    # Profile the event loop
    pr = cProfile.Profile()
    pr.enable()

    # Run the event loop
    exit_code = app.exec()

    pr.disable()

    # Cleanup headless
    if offscreen_surface:
        offscreen_surface.destroy()

    # Compute REAL final metrics from actual counters (after the run)
    elapsed_real = args.seconds  # actual elapsed seconds (close_timer is exact)

    # Real tick delta
    final_tick = sim.w.tick if hasattr(sim, 'w') else 0
    real_tps = (final_tick - initial_tick) / elapsed_real if elapsed_real > 0 else 0

    # Real rendered frames delta
    final_rendered_frames = 0
    if hasattr(window, '_map') and hasattr(window._map, 'rendered_frames'):
        final_rendered_frames = window._map.rendered_frames
    real_fps = (final_rendered_frames - initial_rendered_frames) / elapsed_real if elapsed_real > 0 else 0

    # Real render ms from perf
    perf = getattr(getattr(controller, 'sim', None), 'perf', None)
    real_render_ms = perf.average("render") if perf else 0
    real_sim_ms = perf.average("sim") if perf else 0
    real_ui_ms = perf.average("ui") if perf else 0

    # Also use MainWindow's tracked values if available
    if hasattr(window, 'actual_fps') and window.actual_fps:
        real_fps = window.actual_fps
    if hasattr(window, 'actual_tps') and window.actual_tps:
        real_tps = window.actual_tps

    # Build metrics dict for report using REAL values
    metrics_results = {
        "fps_map_avg": real_fps,
        "fps_map_min": real_fps,
        "fps_map_max": real_fps,
        "tps_sim_avg": real_tps,
        "sim_ms_avg": real_sim_ms,
        "ui_ms_avg": real_ui_ms,
        "render_ms_avg": real_render_ms,
        # Also include raw deltas for verification
        "rendered_frames_delta": final_rendered_frames - initial_rendered_frames,
        "world_tick_delta": final_tick - initial_tick,
        "elapsed_real_seconds": elapsed_real,
    }
    stats = pstats.Stats(pr)
    stats.sort_stats('cumulative')

    # Extract top functions
    top_functions = []
    for func, (cc, nc, tt, ct, callers) in stats.stats.items():
        file_path, line_no, func_name = func
        if file_path.startswith("<"):
            continue
        top_functions.append({
            "file": file_path,
            "line": line_no,
            "function": func_name,
            "cumulative_time": ct,
            "self_time": tt,
            "calls": nc,
            "group": classify_function(file_path, func_name)
        })

    top_functions.sort(key=lambda x: x["cumulative_time"], reverse=True)
    top_20 = top_functions[:20]

    # Group by diagnosis
    groups = {}
    for f in top_functions:
        g = f["group"]
        if g not in groups:
            groups[g] = {"cumulative": 0.0, "self": 0.0, "calls": 0, "functions": []}
        groups[g]["cumulative"] += f["cumulative_time"]
        groups[g]["self"] += f["self_time"]
        groups[g]["calls"] += f["calls"]
        groups[g]["functions"].append(f)

    # Separate excluded groups from runtime groups
    excluded_groups = {}
    runtime_groups = {}
    for group, data in groups.items():
        if group == "excluded_shutdown":
            excluded_groups[group] = data
        else:
            runtime_groups[group] = data

    # Sort runtime groups by cumulative time
    sorted_runtime_groups = sorted(runtime_groups.items(), key=lambda x: x[1]["cumulative"], reverse=True)

    # Determine primary bottleneck from RUNTIME groups only
    primary = sorted_runtime_groups[0][0] if sorted_runtime_groups else "unknown"
    bottleneck_map = {
        "simulation": "world simulation",
        "agent perception": "agent perception",
        "pathfinding": "pathfinding",
        "map rendering": "map terrain rendering",
        "effects": "effects rendering",
        "world simulation": "world simulation",
        "terrain/cache": "terrain/cache",
        "UI docks/models": "Qt dock/model refresh",
        "main UI loop": "main UI loop",
        "neural decision": "neural decision",
        "diagnostic overhead": "diagnostic overhead",
        "unknown": "unknown"
    }
    primary_diagnosis = bottleneck_map.get(primary, primary)

    # Build results
    results = {
        "config": {
            "real_seconds": args.seconds,
            "world_seed": args.seed,
            "agents": args.agents,
            "sheep": args.sheep,
            "monsters": args.monsters,
            "speed": args.speed,
            "blank_world": args.blank,
            "procedural": not args.blank,
        },
        "observed": {
            "population_alive": sum(1 for a in sim.agents if a.alive),
            "sheep_alive": sum(1 for s in sim.sheep if s.alive),
            "monsters_alive": sum(1 for m in sim.monsters if m.alive),
            "map_zoom": getattr(window._map, 'transform', None).zoom if hasattr(window, '_map') and hasattr(window._map, 'transform') else 1.0,
            "app_speed": args.speed,
        },
        "metrics": metrics_results,
        "top_functions": top_20,
        "groups": {k: v for k, v in sorted_runtime_groups},
        "excluded_groups": {k: v for k, v in excluded_groups.items()},
        "primary_bottleneck": primary_diagnosis,
    }

    # Write profile file
    stats.dump_stats(str(prof_file))

    # Write JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Write TXT report
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("LIVE GUI PERFORMANCE DIAGNOSIS\n")
        f.write("=" * 50 + "\n\n")

        f.write("Configuration:\n")
        for k, v in results["config"].items():
            f.write(f"  - {k}: {v}\n")
        f.write("\n")

        f.write("Observed live metrics:\n")
        for k, v in results["observed"].items():
            f.write(f"  - {k}: {v}\n")
        f.write("\n")

        f.write("Observed metrics (REAL measured values):\n")
        m = results["metrics"]
        # Primary metrics
        f.write(f"  - fps_map_avg: {m.get('fps_map_avg', 0):.2f}\n")
        f.write(f"  - tps_sim_avg: {m.get('tps_sim_avg', 0):.2f}\n")
        f.write(f"  - sim_ms_avg: {m.get('sim_ms_avg', 0):.2f}\n")
        f.write(f"  - ui_ms_avg: {m.get('ui_ms_avg', 0):.2f}\n")
        f.write(f"  - render_ms_avg: {m.get('render_ms_avg', 0):.2f}\n")
        # Verification deltas
        if 'rendered_frames_delta' in m:
            f.write(f"  - rendered_frames_delta: {m['rendered_frames_delta']}\n")
        if 'world_tick_delta' in m:
            f.write(f"  - world_tick_delta: {m['world_tick_delta']}\n")
        if 'elapsed_real_seconds' in m:
            f.write(f"  - elapsed_real_seconds: {m['elapsed_real_seconds']:.2f}\n")
        f.write("\n")

        f.write("TOP SLOWEST FUNCTIONS:\n")
        f.write(f"{'rank':>4} | {'cum(s)':>10} | {'self(s)':>10} | {'calls':>8} | {'file:line':>40} | function\n")
        f.write("-" * 110 + "\n")
        for i, fn in enumerate(top_20, 1):
            fname = f"{fn['file'].split('/')[-1]}:{fn['line']}"
            f.write(f"{i:>4} | {fn['cumulative_time']:>10.4f} | {fn['self_time']:>10.4f} | "
                    f"{fn['calls']:>8} | {fname:>40} | {fn['function']}\n")
        f.write("\n")

        f.write("GROUPED DIAGNOSIS (runtime):\n")
        for group, data in sorted_runtime_groups:
            f.write(f"  - {group}: cum={data['cumulative']:.4f}s, self={data['self']:.4f}s, "
                    f"calls={data['calls']}, functions={len(data['functions'])}\n")
        if excluded_groups:
            f.write("\nEXCLUDED SHUTDOWN / PROCESS TIME:\n")
            for group, data in excluded_groups.items():
                f.write(f"  - {group}: cum={data['cumulative']:.4f}s, self={data['self']:.4f}s, "
                        f"calls={data['calls']}, functions={len(data['functions'])}\n")
        f.write("\n")

        f.write("AUTOMATIC CONCLUSION:\n")
        f.write(f"PRIMARY BOTTLENECK: {primary_diagnosis}\n\n")

        # Recommended files/functions
        if primary in runtime_groups and runtime_groups[primary]["functions"]:
            top_funcs = runtime_groups[primary]["functions"][:3]
            files = list(set(f["file"] for f in top_funcs))
            funcs = list(set(f["function"] for f in top_funcs))
            f.write(f"Recommended next file(s): {', '.join(files[:3])}\n")
            f.write(f"Recommended next function(s): {', '.join(funcs[:3])}\n")
        f.write("Do not optimize unrelated systems.\n")

    return results, txt_file


def main():
    args = parse_args()
    print(f"Starting live GUI diagnosis for {args.seconds}s...")
    print(f"Agents: {args.agents}, Sheep: {args.sheep}, Monsters: {args.monsters}")
    print(f"Seed: {args.seed}, Speed: {args.speed}, Blank: {args.blank}")

    try:
        results, txt_file = run_live_profile(args)
        print(f"\nDiagnosis complete!")
        print(f"Primary bottleneck: {results['primary_bottleneck']}")
        print(f"Report written to: {txt_file}")
        print(f"Profile data: data/profiling/live_gui_profile.prof")
        print(f"JSON: data/profiling/live_gui_diagnosis.json")
    except Exception as e:
        print(f"ERROR: {e}")
        traceback.print_exc()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())