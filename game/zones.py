"""Zones spatiales : quartiers (District) et confinements prédateurs.

Lot G.2 — les quartiers sont décoratifs/organisationnels (ils ne
contraignent pas le déplacement), les zones prédateurs confinent
discrètement les monstres qui portent un ``zone_id``.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class District:
    """Quartier libre d'un village (aucune contrainte de déplacement)."""

    id: str
    name: str
    x0: int
    y0: int
    x1: int
    y1: int
    color: tuple[int, int, int] = (80, 150, 230)
    residents: set = field(default_factory=set)
    created_tick: int = 0

    def contains(self, tx, ty):
        return self.x0 <= tx <= self.x1 and self.y0 <= ty <= self.y1

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "x0": self.x0, "y0": self.y0,
            "x1": self.x1, "y1": self.y1,
            "color": list(self.color),
            "residents": sorted(int(e) for e in self.residents),
            "created_tick": int(self.created_tick),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=str(data.get("id", "")),
            name=str(data.get("name", "")),
            x0=int(data.get("x0", 0)),
            y0=int(data.get("y0", 0)),
            x1=int(data.get("x1", 0)),
            y1=int(data.get("y1", 0)),
            color=tuple(int(c) for c in data.get("color", (80, 150, 230))),
            residents={int(e) for e in data.get("residents", [])},
            created_tick=int(data.get("created_tick", 0)),
        )


@dataclass
class PredatorZone:
    """Zone qui confine certains monstres (invisiblement)."""

    id: str
    name: str
    x0: int
    y0: int
    x1: int
    y1: int
    allowed_kinds: set = field(default_factory=set)
    hard_boundary: bool = True
    visible: bool = False

    def contains(self, tx, ty):
        return self.x0 <= tx <= self.x1 and self.y0 <= ty <= self.y1

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "x0": self.x0, "y0": self.y0,
            "x1": self.x1, "y1": self.y1,
            "allowed_kinds": sorted(str(k) for k in self.allowed_kinds),
            "hard_boundary": bool(self.hard_boundary),
            "visible": bool(self.visible),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=str(data.get("id", "")),
            name=str(data.get("name", "")),
            x0=int(data.get("x0", 0)),
            y0=int(data.get("y0", 0)),
            x1=int(data.get("x1", 0)),
            y1=int(data.get("y1", 0)),
            allowed_kinds={str(k) for k in data.get("allowed_kinds", [])},
            hard_boundary=bool(data.get("hard_boundary", True)),
            visible=bool(data.get("visible", False)),
        )


def can_monster_enter(sim, monster, tx, ty):
    """Un monstre sans zone est libre ; avec une zone, il reste dedans."""
    zone_id = getattr(monster, "zone_id", None)
    if zone_id is None:
        return True
    zone = getattr(sim, "predator_zones", {}).get(zone_id)
    return zone is None or zone.contains(tx, ty)
