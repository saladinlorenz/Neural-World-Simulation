"""Vues enrichies de l'etat reel avec labels lisibles. Pas de Qt/Pygame."""
from .ui_snapshots import (
    simulation_snapshot,
    population_snapshot,
    selected_agent_snapshot,
    journal_snapshot,
    map_snapshot,
    tile_snapshot,
    society_snapshot,
    anima_snapshot,
)
from .diagnostics import agent_snapshot as _raw_agent_snapshot
from .studio_text import level_label, level_color


def readable_agent(sim, agent):
    """Agent snapshot enriched with readable labels."""
    snap = _raw_agent_snapshot(sim, agent)
    if snap is None:
        return None
    snap["sante_label"] = level_label(snap.get("sante", 0))
    snap["sante_color"] = level_color(snap.get("sante", 0))
    snap["faim_label"] = level_label(snap.get("faim", 0))
    snap["energie_label"] = level_label(snap.get("energie", 0))
    identity = snap.get("identity", {})
    if identity:
        snap["identity_dominant"] = max(identity, key=identity.get)
    else:
        snap["identity_dominant"] = None
    return snap


def readable_population(sim):
    """Population with readable fields for each agent."""
    pop = population_snapshot(sim)
    for agent in pop:
        agent["sante_label"] = level_label(agent.get("sante", 0))
        agent["faim_label"] = level_label(agent.get("faim", 0))
        identity = agent.get("identity", {})
        agent["identity_dominant"] = max(identity, key=identity.get) if identity else None
    return pop


def readable_selected(sim, ui_state=None):
    """Selected agent snapshot enriched with labels."""
    snap = selected_agent_snapshot(sim, ui_state)
    if snap is None:
        return None
    snap["sante_label"] = level_label(snap.get("sante", 0))
    snap["sante_color"] = level_color(snap.get("sante", 0))
    snap["faim_label"] = level_label(snap.get("faim", 0))
    snap["energie_label"] = level_label(snap.get("energie", 0))
    identity = snap.get("identity", {})
    if identity:
        snap["identity_dominant"] = max(identity, key=identity.get)
    else:
        snap["identity_dominant"] = None
    return snap


def readable_tile(sim, tx, ty):
    """Tile snapshot enriched with labels."""
    snap = tile_snapshot(sim, tx, ty)
    if snap is None:
        return None
    snap["danger_label"] = level_label(snap.get("danger", 0))
    snap["danger_color"] = level_color(snap.get("danger", 0))
    snap["fertilite_label"] = level_label(snap.get("fertilite", 0))
    snap["ressource_label"] = level_label(snap.get("ressource", 0))
    return snap


def readable_map(sim, ui_state=None):
    """Map snapshot enriched with danger/fertility labels."""
    snap = map_snapshot(sim, ui_state)
    for tile in snap.get("tiles", []):
        tile["danger_label"] = level_label(tile.get("danger", 0))
        tile["fertilite_label"] = level_label(tile.get("fertilite", 0))
    return snap


def readable_society(sim):
    """Society snapshot with readable summary."""
    snap = society_snapshot(sim)
    pop = snap.get("population", 0)
    bonded = snap.get("bonded", 0)
    snap["summary"] = f"Le groupe compte {pop} habitant(s)"
    if bonded:
        snap["summary"] += f", {bonded} couple(s)"
    snap["summary"] += "."
    return snap
