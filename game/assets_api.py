"""Couche Assets — API publique en lecture seule.

Fournit des accès typés aux assets du catalogue, sans exposer les détails
internes d'AssetDef. Toutes les fonctions retournent des dataclasses
immutables (AssetData) contenant seulement les champs nécessaires aux autres
couches (UI, Cerveau, Simulation).

Aucun module pygame n'est importé ici — cette couche est entièrement
déterministe et peut être utilisée en mode headless.

Chaque fonction accepte un paramètre optionnel `asset_manager` ; si non
fourni, le module tente de l'importer de façon paresseuse (utile pour les
tests unitaires). En production, main.py fournit l'instance via
`from game import assets_manager as am`.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

# Cache paresseux — sera remplacé par main.py si disponible
_AM: Optional["AssetManager"] = None


def _set_asset_manager(am):  # pragma: no cover
    """Appelé par main.py pour injecter l'instance AssetManager."""
    global _AM
    _AM = am


def _get_am() -> "AssetManager":
    """Retourne l'instance AssetManager en cache, ou l'importe paresseusement."""
    global _AM
    if _AM is not None:
        return _AM
    from game import assets_manager as _mod
    _AM = _mod.AssetManager(headless=True).discover()
    return _AM


from game.assets_manager import AssetDef, CATEGORY_LABELS, NON_PLACABLE


class AssetData:
    """Snapshot immuable d'un asset — les couches supérieures ne doivent
    jamais accéder AssetDef.__dict__ directement, seulement par ce type."""
    __slots__ = (
        "id", "label", "role", "category", "placable", "affordances",
        "build_recipe", "solid", "edible", "harvest", "material", "color",
        "blocked_footprint", "size_tiles", "px", "kind", "frames",
    )

    def __init__(self, def_: AssetDef):
        self.id = def_.id
        self.label = def_.label
        self.role = def_.role
        self.category = def_.category
        self.placable = def_.placable
        self.affordances = list(def_.afford)
        self.build_recipe = getattr(def_, "build_recipe", None)
        self.solid = def_.solid
        self.edible = def_.edible
        self.harvest = getattr(def_, "harvest", None)
        self.material = getattr(def_, "material", "")
        self.color = getattr(def_, "color", "")
        self.blocked_footprint = def_.blocked_footprint
        self.size_tiles = def_.size_tiles
        self.px = def_.px
        self.kind = def_.kind
        self.frames = def_.frames

    def __repr__(self) -> str:
        return f"<AssetData id={self.id} label={self.label!r} role={self.role!r} cat={self.category!r}>"


# ---- Accès catalogue ----

def get_asset(asset_id: int, asset_manager: Optional["AssetManager"] = None) -> AssetData:
    """Retourne un AssetData par son identifiant global (0..N-1).

    Si `asset_manager` n'est pas fourni, utilise le cache paresseux.
    """
    am = asset_manager or _get_am()
    if 0 <= asset_id < len(am.assets):
        return AssetData(am.assets[asset_id])
    raise IndexError(f"asset_id {asset_id} hors gamme [0..{len(am.assets)-1}]")


def list_assets(
    category: Optional[str] = None,
    placable_only: bool = True,
    asset_manager: Optional["AssetManager"] = None,
) -> List[AssetData]:
    """Retourne tous les assets, optionnellement filtrés par catégorie
    et par placable (panneau Décor).
    """
    am = asset_manager or _get_am()
    result: List[AssetData] = []
    for a in am.assets:
        if placable_only and a.placable is False:
            continue
        if category is not None and a.category != category:
            continue
        result.append(AssetData(a))
    return result


def list_by_role(role: str, asset_manager: Optional["AssetManager"] = None) -> List[AssetData]:
    """Retourne tous les assets d'un rôle donné (ex. 'house', 'tool', 'fort')."""
    am = asset_manager or _get_am()
    return [AssetData(a) for a in am.assets if a.role == role]


def get_placable_assets(asset_manager: Optional["AssetManager"] = None) -> List[AssetData]:
    """Retourne uniquement les assets posables dans le monde (panneau Décor)."""
    am = asset_manager or _get_am()
    return [AssetData(a) for a in am.assets if a.placable]


def get_non_placable_assets(asset_manager: Optional["AssetManager"] = None) -> List[AssetData]:
    """Retourne les assets de travail (atlas, rendus, interface, unites)."""
    am = asset_manager or _get_am()
    return [AssetData(a) for a in am.assets if not a.placable]


def get_category_labels() -> Dict[str, str]:
    """Retourne le dictionnaire {code_courtois: label_affichage}."""
    from game.assets_manager import CATEGORY_LABELS
    return dict(CATEGORY_LABELS)


# ---- Affordances ----

def get_affordance_definition(name: str, asset_manager: Optional["AssetManager"] = None) -> Optional[Dict[str, Any]]:
    """Retourne la définition structurée d'une affordance par nom."""
    from game import affordance_definitions as af
    am = asset_manager or _get_am()
    # Les definitions sont globales, pas besoin de l'asset manager pour ça
    return af.AFFORDANCE_DEFS.get(name)


def get_affordance_definitions(asset_manager: Optional["AssetManager"] = None) -> Dict[str, Dict[str, Any]]:
    """Retourne le dictionnaire complet des définitions d'affordances."""
    from game import affordance_definitions as af
    return af.AFFORDANCE_DEFS


def can_build(materials_carried: Dict[str, int], asset_manager: Optional["AssetManager"] = None) -> List[AssetData]:
    """Retourne la liste des assets constructibles avec l'inventaire donné.

    materials_carried : dict {materiau: quantite} tel que l'être le transporte
    actuellement (ex. {'bois': 6, 'pierre': 2}).

    Ne considère que les assets ayant une build_recipe (house, fort, tool).
    """
    am = asset_manager or _get_am()
    from game.affordance_definitions import BUILD_RECIPES

    out: List[AssetData] = []
    for a in am.assets:
        if not a.placable:
            continue
        recipe = BUILD_RECIPES.get(a.role)
        if recipe is None:
            continue

        ok = True
        for m in recipe["materials"]:
            have = materials_carried.get(m["materiau"], 0)
            need = m["quantity"]
            if have < need:
                ok = False
                break
        if ok:
            out.append(AssetData(a))
    return out


# ---- Utilitaires internes ----

def _asset_to_data(a: AssetDef) -> AssetData:
    return AssetData(a)