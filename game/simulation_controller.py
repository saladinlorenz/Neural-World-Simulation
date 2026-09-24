"""SimulationController — pont unique entre UI et moteur.

Toute interaction entre l'interface et la simulation passe par ce
contrôleur. Ni Pygame ni Qt ne modifient directement les objets
Sim, Being ou World.
"""
from __future__ import annotations

from typing import Any

from .ui_state import UIState
from .ui_snapshots import (
    simulation_snapshot,
    population_snapshot,
    selected_agent_snapshot,
    journal_snapshot,
    society_snapshot,
    map_snapshot,
    anima_snapshot,
    tile_snapshot,
)
from .ui_commands import execute_command, execute_ui_command


class SimulationController:
    """Pont central UI ↔ moteur.

    Utilisé par le dashboard Pygame ET par l'interface Qt.
    Fournit des snapshots immuables et exécute des commandes validées.
    """

    def __init__(self, sim, camera=None):
        self.sim = sim
        self.camera = camera
        self.ui_state = UIState()

    # ── Snapshots ──

    def snapshot(self) -> dict[str, Any]:
        """Snapshot global complet pour le rendu."""
        return {
            "simulation": simulation_snapshot(self.sim, self.ui_state),
            "population": population_snapshot(self.sim),
            "selected_agent": selected_agent_snapshot(self.sim, self.ui_state),
            "journal": journal_snapshot(
                self.sim,
                category=self.ui_state.journal_filter,
                search=self.ui_state.search_text,
            ),
        }

    def snapshot_population(self) -> list[dict]:
        return population_snapshot(self.sim)

    def snapshot_selected(self) -> dict | None:
        return selected_agent_snapshot(self.sim, self.ui_state)

    def snapshot_journal(self, category: str = "all", search: str = "") -> list[dict]:
        return journal_snapshot(self.sim, category=category, search=search)

    def snapshot_society(self) -> dict:
        return society_snapshot(self.sim)

    def snapshot_map(self) -> dict:
        return map_snapshot(self.sim, self.ui_state)

    def snapshot_anima(self) -> dict | None:
        return anima_snapshot(self.sim, self.ui_state)

    def snapshot_tile(self, tx: int, ty: int) -> dict:
        return tile_snapshot(self.sim, tx, ty)

    # ── Commandes ──

    def execute(self, command: dict) -> dict[str, Any]:
        """Exécute une commande et synchronise l'état UI.

        Les commandes d'interface (mode d'outil, pinceau, overlay, matériau)
        sont traitées ici : elles ne concernent pas le moteur, mais passer
        par ce canal les rend testables et sauvegardables.
        """
        ui_result = execute_ui_command(self.ui_state, command)
        if ui_result is not None:
            return ui_result

        kind = command.get("kind")
        # Save v3 : le contrôleur injecte l'état UI dans la sauvegarde.
        if kind == "save" and "ui_state" not in command:
            command = dict(command,
                           ui_state=self.ui_state.snapshot_dict())
        result = execute_command(self.sim, command)
        if result.get("ok") and kind in ("load", "reset_world") and "sim" in result:
            # Le chargement remplace la simulation active : sans cela,
            # la partie chargée était silencieusement ignorée.
            self.sim = result["sim"]
            if result.get("cam") is not None:
                self.camera = result["cam"]
            loaded_ui = getattr(self.sim, "loaded_ui_state", None)
            if loaded_ui:
                self.ui_state.apply_dict(loaded_ui)
        if result.get("ok") and kind == "select_tile":
            # UIState est un concept d'interface : la commande valide les
            # coordonnées, le contrôleur est seul à les mémoriser.
            self.ui_state.selected_tile = (result["tx"], result["ty"])
        self.sync_from_simulation()
        return result

    # ── Synchronisation ──

    def sync_from_simulation(self) -> None:
        """Met à jour l'UIState à partir de l'état actuel de la simulation."""
        self.ui_state.sync_from_simulation(self.sim)

    def sync_camera_from_state(self) -> None:
        """Met à jour la caméra à partir de l'UIState."""
        if self.camera is None:
            return
        self.camera.x = self.ui_state.camera_x
        self.camera.y = self.ui_state.camera_y
        self.camera.zoom = self.ui_state.camera_zoom
        self.camera.tilt = self.ui_state.camera_tilt

    def sync_state_from_camera(self) -> None:
        """Met à jour l'UIState à partir de la caméra."""
        if self.camera is None:
            return
        self.ui_state.camera_x = self.camera.x
        self.ui_state.camera_y = self.camera.y
        self.ui_state.camera_zoom = self.camera.zoom
        self.ui_state.camera_tilt = self.camera.tilt

    # ── Action tuple (compatibilité avec l'ancien dashboard) ──

    def translate_action(self, action: tuple | None) -> dict | None:
        """Convertit un ancien tuple d'action du dashboard en commande dict.

        Permet la migration progressive : le dashboard peut continuer
        à produire des tuples pendant la transition.
        """
        if action is None:
            return None
        kind, val = action
        mapping = {
            "pause": {"kind": "pause_toggle"},
            "step": {"kind": "step"},
            "speed": {"kind": "speed_delta", "delta": val},
            "speed_set": {"kind": "set_speed", "speed": val},
            "spawn": {"kind": "spawn_agent"},
            "spawn_sheep": {"kind": "spawn_sheep"},
            "save_game": {"kind": "save", "slot": 0},
            "load_game": {"kind": "load", "slot": 0},
        }
        return mapping.get(kind)

    def handle_legacy_action(self, action: tuple | None) -> dict | None:
        """Convertit et exécute un ancien tuple d'action."""
        cmd = self.translate_action(action)
        if cmd is None:
            return None
        return self.execute(cmd)
