"""Tests d'invariants exécutables en mode debug."""
from __future__ import annotations

import math


def validate_simulation(sim):
    errors = []
    w = sim.w

    for a in sim.agents:
        if not a.alive:
            errors.append(f"agent mort encore présent : eid={a.eid}")
        # position finie d'abord : a.tx lève ValueError si x/y est NaN
        if not (math.isfinite(a.x) and math.isfinite(a.y)):
            errors.append(f"position non finie : eid={a.eid}")
        elif not (0 <= a.tx < w.g and 0 <= a.ty < w.g):
            errors.append(f"agent hors monde : eid={a.eid}")
        if not (0.0 <= a.health <= 1.0):
            errors.append(f"santé invalide : eid={a.eid}")
        if not (0.0 <= a.energy <= 1.0):
            errors.append(f"énergie invalide : eid={a.eid}")
        if not (0.0 <= a.hunger <= 1.0):
            errors.append(f"faim invalide : eid={a.eid}")
        if a.tool >= 0 and not (0 <= a.tool < len(sim.am.assets)):
            errors.append(f"outil invalide : eid={a.eid}")
        # but actif : coordonnées toujours dans le monde
        g = a.goal
        if g is not None:
            gx, gy = g.get("x"), g.get("y")
            try:
                in_bounds = w.inb(gx, gy)
            except TypeError:
                in_bounds = False
            if not in_bounds:
                errors.append(f"but hors monde : eid={a.eid} ({gx!r}, {gy!r})")

    for tx, ty, name, death_tick, color in getattr(w, "cemetery", ()):
        if not (0 <= tx < w.g and 0 <= ty < w.g):
            errors.append(f"tombe hors monde : {name}")

    for (tx, ty), storage in getattr(w, "storages", {}).items():
        if (tx, ty) != (storage.tx, storage.ty):
            errors.append("clé de stockage incohérente")
        if sum(storage.inventory.values()) > storage.capacity:
            errors.append(f"stockage dépasse capacité : {tx},{ty}")

    return errors
