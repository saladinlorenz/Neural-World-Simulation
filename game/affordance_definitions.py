"""Registre des affordances — définition structurée de chaque tag du catalogue.

Chaque définition contient :
- requires : préconditions (outil, distance, etc.)
- cost      : coût en temps / énergie
- effect    : effets monde / agent (sont des gabarits, interpolés ailleurs)
- risk      : 0.0 = sûr, >0 = danger potentiel

Le point clé : une seule définition par tag, partagée par tous les assets.
Les paramètres variables (materiau, recolte.amount, poids, enflammable, edible, etc.)
viennent du catalogue asset individuel et sont lus en même temps que la définition.
"""
from typing import Any, Dict, List


AFFORDANCE_DEFS: Dict[str, Dict[str, Any]] = {
    "observe": {
        "requires": {},
        "cost": {"time": 0.5, "energy": 0.0},
        "effect": {"world": "perception mise à jour"},
        "risk": 0.0,
    },

    "harvest": {
        "requires": {"tool": None, "distance_max": 1, "needs_hp": True},
        "cost": {"time": 2.0, "energy": 4.0},
        "effect": {"world": "object.hp -= 1",
                   "on_depletion": "spawn_material({materiau}, {recolte.amount})",
                   "on_pickup": "agent.inv[{materiau}] += gain * (2 si agent.tool)"},
        "risk": 0.0,
    },

    "eat": {
        "requires": {"edible": ">0"},
        "cost": {"time": 1.0, "energy": 0.0},
        "effect": {"world": "object consommé",
                   "agent": "faim -= {edible}/110.0, energie += {edible}/150.0, soif -= {edible}/260.0"},
        "risk": 0.0,
    },

    "carry": {
        "requires": {"poids": "<= agent.force_max"},
        "cost": {"time": 0.2, "energy": 0.5},
        "effect": {"world": "object -> agent.inv",
                   "agent": "inv[{materiau}] += {recolte.amount}"},
        "risk": 0.0,
    },

    "place": {
        "requires": {},
        "cost": {"time": 0.3, "energy": 0.5},
        "effect": {"world": "agent.inv[{materiau}] -> world.object",
                   "agent": "inv[{materiau}] -= 1"},
        "risk": 0.0,
    },

    "use": {
        "requires": {"role": "tool"},
        "cost": {"time": 1.0, "energy": 1.0},
        "effect": {"agent": "agent.tool = object.id (multiplicateur récolte ×2)",
                   "world": "outil équipé"},
        "risk": 0.0,
    },

    "shelter": {
        "requires": {},
        "cost": {"time": 0.5, "energy": 0.0},
        "effect": {"agent": "securite += 0.15, abri = true",
                   "world": "tuile marquée abri"},
        "risk": 0.0,
    },

    "sleep": {
        "requires": {"energy": "<0.2 or nuit"},
        "cost": {"time": 10.0, "energy": 0.0},
        "effect": {"agent": "energie += REST_GAIN * (SHELTER_BONUS si abri)",
                   "world": "état = sleep"},
        "risk": 0.05,
    },

    "burn": {
        "requires": {"enflammable": True},
        "cost": {"time": 1.0, "energy": 0.0},
        "effect": {"world": "allume feu (object.hp -= fire_damage), propagation possible"},
        "risk": 0.6,
    },

    "block": {
        "requires": {},
        "cost": {"time": 0.0, "energy": 0.0},
        "effect": {"world": "obstacle physique",
                   "agent": "mouvement empêché"},
        "risk": 0.0,
    },

    "hit": {
        "requires": {},
        "cost": {"time": 1.0, "energy": 2.0},
        "effect": {"agent": "cible.hp -= dmg(force)",
                   "world": "riposte possible"},
        "risk": 0.3,
    },

    "throw": {
        "requires": {},
        "cost": {"time": 0.5, "energy": 1.0},
        "effect": {"agent": "projectile lancé (dégât à distance)",
                   "world": "projectile créé"},
        "risk": 0.2,
    },

    "give": {
        "requires": {"target_proche": True},
        "cost": {"time": 0.5, "energy": 0.5},
        "effect": {"agent": "objet transféré, lien social +0.05",
                   "target": "inv[materiau] += 1"},
        "risk": 0.0,
    },

    "mourn": {
        "requires": {"role": "grave"},
        "cost": {"time": 2.0, "energy": 0.0},
        "effect": {"agent": "tristesse -0.2, mémoire deuil créée, lien social renforcé"},
        "risk": 0.0,
    },

    "mark": {
        "requires": {},
        "cost": {"time": 1.0, "energy": 0.5},
        "effect": {"world": "phéromone territoire déposée (marqueur clan)",
                   "agent": "reconnaissance territoire"},
        "risk": 0.0,
    },

    "sit": {
        "requires": {},
        "cost": {"time": 1.0, "energy": -0.5},
        "effect": {"agent": "repos léger, energie +0.02",
                   "world": "état = sit"},
        "risk": 0.0,
    },

    "climb": {
        "requires": {"obstacle_hauteur": "<= agent.mobilite"},
        "cost": {"time": 1.0, "energy": 2.0},
        "effect": {"agent": "se déplace au-dessus de l'obstacle",
                   "world": "position modifiée"},
        "risk": 0.15,
    },

    "chase": {
        "requires": {"cible_mobile": True},
        "cost": {"time": 1.0, "energy": 2.0},
        "effect": {"agent": "poursuit la cible",
                   "world": "poursuite engagée"},
        "risk": 0.2,
    },

    "shear": {
        "requires": {},
        "cost": {"time": 2.0, "energy": 1.0},
        "effect": {"agent": "laine/ressource récupérée",
                   "target": "recolte = laine"},
        "risk": 0.0,
    },

    "lean": {
        "requires": {},
        "cost": {"time": 1.0, "energy": 0.0},
        "effect": {"agent": "s'appuie, repos passif",
                   "world": "état = lean"},
        "risk": 0.0,
    },

    "decorate": {
        "requires": {"role": "prop or decor"},
        "cost": {"time": 1.0, "energy": 0.5},
        "effect": {"agent": "estime sociale +0.05, monde changé visuellement",
                   "world": "décoration posée"},
        "risk": 0.0,
    },

    "follow": {
        "requires": {"cible_sociale": True},
        "cost": {"time": 0.5, "energy": 0.2},
        "effect": {"agent": "suit la cible",
                   "world": "groupe formé"},
        "risk": 0.0,
    },
}


# ------------------------------------------------------------------ recettes de construction
# Posées par rôle (house, fort, tool). Utilisées par _do_build au lieu de
# coûts codés en dur (3 bois + 1 pierre par défaut).

BUILD_RECIPES: Dict[str, Dict[str, Any]] = {
    "house": {
        "materials": [{"materiau": "bois", "quantity": 6},
                      {"materiau": "pierre", "quantity": 2}],
        "tool_required": None,
        "primitives": ["take", "carry", "place", "assemble"],
        "duration": 12.0,
    },
    "fort": {
        "materials": [{"materiau": "bois", "quantity": 4},
                      {"materiau": "pierre", "quantity": 4}],
        "tool_required": None,
        "primitives": ["take", "carry", "place", "assemble"],
        "duration": 16.0,
    },
    "tool": {
        "materials": [{"materiau": "bois", "quantity": 1}],
        "tool_required": None,
        "primitives": ["take", "carry", "place", "assemble"],
        "duration": 3.0,
    },
}


def render_asset(asset) -> Dict[str, Dict[str, Any]]:
    """Retourne la vue des affordances pour un asset donné.

    Pour chaque tag présent dans a.afford, on renvoie la définition
    partagée AFFORDANCE_DEFS[tag]. C'est la même définition pour tous les
    assets portant ce tag ; ce sont les attributs de l'asset (a.harvest,
    a.edible, a.flammable, etc.) qui apportent la variation.
    """
    out: Dict[str, Dict[str, Any]] = {}
    for tag in getattr(asset, "afford", ["observe"]):
        defn = AFFORDANCE_DEFS.get(tag)
        if defn is not None:
            out[tag] = defn
    return out


def build_recipe_for(asset) -> Dict[str, Any] | None:
    """Retourne la recette de construction si l'asset a un rôle constructible."""
    return BUILD_RECIPES.get(asset.role)


def plans_for(am, inv: Dict[str, int]) -> List[Dict[str, Any]]:
    """Retourne la liste des assets constructibles avec l'inventaire donné.

    Pour chaque asset placable possédant une build_recipe, on vérifie que
    l'inventaire contient suffisamment de chaque matière première.
    """
    out: List[Dict[str, Any]] = []
    for a in am.assets:
        if not getattr(a, "placable", False):
            continue
        rec = BUILD_RECIPES.get(a.role)
        if rec is None:
            continue
        missing: Dict[str, int] = {}
        for m in rec["materials"]:
            have = inv.get(m["materiau"], 0)
            need = m["quantity"]
            if have < need:
                missing[m["materiau"]] = need - have
        if missing:
            continue
        out.append({
            "aid": a.id,
            "label": a.label,
            "role": a.role,
            "recipe": rec,
            "missing": missing,
            "footprint": a.size_tiles,
            "px": a.px,
        })
    return out