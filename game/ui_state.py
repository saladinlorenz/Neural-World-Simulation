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
    active_overlay: str = "normal"

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
    #: Gabarits du créateur (listes de floats 0..1), lus par SpawnAgentDialog.
    tpl_body: list = field(default_factory=list)
    tpl_cog: list = field(default_factory=list)
    tpl_personality: list = field(default_factory=list)
    tpl_emotions: list = field(default_factory=list)
    tpl_needs: list = field(default_factory=list)
    brain_size: int = 128
    #: Options du dialogue de création en attente d'un clic sur la carte.
    pending_spawn_agent: dict | None = None

    #: Type de monstre à poser. Vide = tirage aléatoire par le moteur.
    monster_kind: str = ""

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
            "monster_kind": self.monster_kind,
            "needs_save": self.needs_save,
            # ── Lot Save v3 : état restauré au chargement ──
            "favs": list(self.favs),
            "recents": list(self.recents),
            "template_color": self.template_color,
            "template_class": self.template_class,
            "template_sex": self.template_sex,
            "tpl_body": list(self.tpl_body),
            "tpl_cog": list(self.tpl_cog),
            "tpl_personality": list(self.tpl_personality),
            "tpl_emotions": list(self.tpl_emotions),
            "tpl_needs": list(self.tpl_needs),
            "brain_size": int(self.brain_size),
            "pending_spawn_agent": self.pending_spawn_agent,
            "open_sections": dict(self.open_sections),
            "open_cards": dict(self.open_cards),
        }

    def apply_dict(self, data: dict) -> None:
        """Restaure l'état depuis un dict de types simples (Save v3)."""
        if not isinstance(data, dict):
            return
        for key, value in data.items():
            if not hasattr(self, key):
                continue
            if key in ("selected_tile", "ghost_tile") and value is not None:
                value = tuple(value)
            if key in ("action",) and value is not None:
                value = tuple(value)
            setattr(self, key, value)
