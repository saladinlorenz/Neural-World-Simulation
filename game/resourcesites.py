"""ResourceSite — sites de ressources persistants avec capacité et repousse.

Chaque site représente une poche de ressources (nourriture, bois, pierre, etc.)
avec une capacité finie, une régénération lente, et un index régional pour
accès local efficace.

Cycle de vie: découverte → partage → expédition → vérification → récolte →
épuisement → retour → stockage → événement diagnostique véridique.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Iterator, Optional
import numpy as np


@dataclass(slots=True)
class ResourceSite:
    """Site de ressource avec capacité, stock restant et régénération."""
    id: int
    kind: str                  # "wild_food", "wood", "stone", etc.
    tx: int
    ty: int
    radius: int
    capacity: float
    remaining: float
    regrowth_per_tick: float
    biome: int
    region: tuple[int, int]
    visible_cap: int = 18
    last_update_tick: int = 0
    discovered_by: list[int] = field(default_factory=list)  # eids qui ont découvert
    last_harvest_tick: int = 0
    last_harvest_by: int = -1
    depletion_count: int = 0
    # Cache des tuiles appartenant au site (calculé une fois)
    _tiles: list[tuple[int, int]] = field(default_factory=list, repr=False)

    def tiles(self) -> list[tuple[int, int]]:
        """Retourne les tuiles du site (calculé à la demande)."""
        if not self._tiles:
            self._compute_tiles()
        return self._tiles

    def _compute_tiles(self) -> None:
        """Calcule les tuiles dans le rayon du site (Moore neighborhood)."""
        r = self.radius
        gx, gy = self.tx, self.ty
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if max(abs(dx), abs(dy)) <= r:
                    self._tiles.append((gx + dx, gy + dy))

    def harvest(self, amount: float) -> float:
        """Récolte une quantité, retourne la quantité réellement prise."""
        taken = min(amount, self.remaining)
        self.remaining -= taken
        return taken

    def regrow(self, ticks: int) -> None:
        """Régénère le stock selon le temps écoulé."""
        self.remaining = min(self.capacity, self.remaining + self.regrowth_per_tick * ticks)

    def record_discovery(self, eid: int, tick: int) -> None:
        """Enregistre la découverte par un habitant."""
        if eid not in self.discovered_by:
            self.discovered_by.append(eid)
        self.last_update_tick = tick

    def record_harvest(self, amount: float, eid: int, tick: int) -> float:
        """Enregistre la récolte et retourne la quantité prise."""
        taken = self.harvest(amount)
        self.last_harvest_tick = tick
        self.last_harvest_by = eid
        if self.remaining <= 0:
            self.depletion_count += 1
        return taken

    def is_depleted(self) -> bool:
        return self.remaining <= 0

    def get_info(self) -> dict:
        """Retourne les infos pour l'UI/diagnostics."""
        return {
            "id": self.id,
            "kind": self.kind,
            "tx": self.tx, "ty": self.ty,
            "radius": self.radius,
            "capacity": self.capacity,
            "remaining": self.remaining,
            "depletion_count": self.depletion_count,
            "discovered_by": list(self.discovered_by),
            "last_harvest_by": self.last_harvest_by,
            "last_harvest_tick": self.last_harvest_tick,
            "is_depleted": self.is_depleted(),
        }


# ──────────────────────────────────────────────────────────────────────
# Index régional pour recherche locale efficace
# ──────────────────────────────────────────────────────────────────────

REGION_SIZE = 64  # 64 tuiles = 1024 px


def region_key(tx: int, ty: int) -> tuple[int, int]:
    """Clé de région pour une tuile."""
    return tx // REGION_SIZE, ty // REGION_SIZE


def add_resource_site(world, site: ResourceSite) -> None:
    """Ajoute un site aux index du monde."""
    if not hasattr(world, "resource_sites"):
        world.resource_sites = {}
        world.sites_by_region = {}
        world.next_resource_site_id = 1
    world.resource_sites[site.id] = site
    world.sites_by_region.setdefault(site.region, []).append(site.id)


def get_resource_site(world, site_id: int) -> Optional[ResourceSite]:
    """Récupère un site par son ID."""
    if not hasattr(world, "resource_sites"):
        return None
    return world.resource_sites.get(site_id)


def nearby_resource_sites(world, tx: int, ty: int, radius_regions: int = 1) -> Iterator[ResourceSite]:
    """Itère sur les sites proches (rayon en régions)."""
    if not hasattr(world, "sites_by_region"):
        return iter(())
    rx, ry = region_key(tx, ty)
    for y in range(ry - radius_regions, ry + radius_regions + 1):
        for x in range(rx - radius_regions, rx + radius_regions + 1):
            for site_id in world.sites_by_region.get((x, y), ()):
                site = world.resource_sites.get(site_id)
                if site is not None:
                    yield site


def update_resource_sites(world, interval: int = 200) -> None:
    """Met à jour la régénération de tous les sites (tous les `interval` ticks)."""
    if not hasattr(world, "resource_sites"):
        return
    if world.tick % interval != 0:
        return
    for site in world.resource_sites.values():
        site.regrow(interval)


def discover_resource_sites_near(world, tx: int, ty: int, max_dist: int = 80) -> list[ResourceSite]:
    """Découvre les sites de ressources à proximité (utilisé par la perception)."""
    found = []
    for site in nearby_resource_sites(world, tx, ty, radius_regions=2):
        dx = site.tx - tx
        dy = site.ty - ty
        dist = max(abs(dx), abs(dy))
        if dist <= max_dist and site.remaining > 0:
            found.append(site)
    found.sort(key=lambda s: max(abs(s.tx - tx), abs(s.ty - ty)))
    return found