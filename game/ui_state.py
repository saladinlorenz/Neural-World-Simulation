"""UIState — état d'interface neutre, sans dépendance Pygame ni Qt.

Cet état est partagé entre le moteur de simulation et n'importe quel
frontend (Pygame, PyQt6, futur web). Il ne contient que des types simples.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class UIState:
    """État central de l'interface, indépendant du backend de rendu."""

    # ── Navigation ──
    active_tab: str = "etre"
    active_mode: str = "agent"
    active_overlay: str = "none"

    # ── Sélection ──
    selected_agent_eid: int | None = None
    selected_asset_id: int | None = None
    selected_tile: tuple[int, int] | None = None

    # ── Filtres et recherche ──
    selected_category: str = "all"
    search_text: str = ""
    journal_filter: str = "tous"
    only_favs: bool = False

    # ── Simulation ──
    speed: int = 1
    paused: bool = True

    # ── Caméra ──
    follow_selected: bool = False
    camera_x: float = 0.0
    camera_y: float = 0.0
    camera_zoom: float = 0.25
    camera_tilt: float = 55.0

    # ── Panneaux ──
    left_panel_open: bool = True
    right_panel_open: bool = True

    # ── Pinceau / Outils ──
    brush_size: int = 3
    block_material: str = "bois"

    # ── Sections accordéon (inspecteur) ──
    open_sections: dict = field(default_factory=dict)
    open_cards: dict = field(default_factory=dict)

    # ── favoris / récents assets ──
    favs: list = field(default_factory=list)
    recents: list = field(default_factory=list)

    # ── Ghost / placement ──
    ghost_visible: bool = False
    ghost_tile: tuple[int, int] | None = None

    # ── Créateur d'habitant ──
    creator_open: bool = False
    template_color: str = "blue"
    template_class: str = "pawn"
    template_sex: str = "M"

    # ── UI state signaux ──
    needs_save: bool = False
    action: tuple | None = None

    def sync_from_simulation(self, sim) -> None:
        """Synchronise les champs dérivés de l'état de simulation."""
        self.paused = bool(sim.paused)
        self.speed = int(sim.speed)
        if getattr(sim, "selected", None) is not None and sim.selected.alive:
            self.selected_agent_eid = int(sim.selected.eid)
        else:
            self.selected_agent_eid = None

    def snapshot_dict(self) -> dict:
        """Retourne un dictionnaire de types simples, sérialisable JSON."""
        return {
            "active_tab": self.active_tab,
            "active_mode": self.active_mode,
            "active_overlay": self.active_overlay,
            "selected_agent_eid": self.selected_agent_eid,
            "selected_asset_id": self.selected_asset_id,
            "selected_tile": self.selected_tile,
            "selected_category": self.selected_category,
            "search_text": self.search_text,
            "journal_filter": self.journal_filter,
            "only_favs": self.only_favs,
            "speed": self.speed,
            "paused": self.paused,
            "follow_selected": self.follow_selected,
            "camera_x": self.camera_x,
            "camera_y": self.camera_y,
            "camera_zoom": self.camera_zoom,
            "camera_tilt": self.camera_tilt,
            "left_panel_open": self.left_panel_open,
            "right_panel_open": self.right_panel_open,
            "brush_size": self.brush_size,
            "block_material": self.block_material,
            "ghost_visible": self.ghost_visible,
            "ghost_tile": self.ghost_tile,
            "creator_open": self.creator_open,
            "needs_save": self.needs_save,
        }
