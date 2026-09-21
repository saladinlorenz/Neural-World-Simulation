"""Courage Brain — API publique.

Fournit les fonctions que les autres couches (simulation, UI) peuvent appeler
pour interagir avec le réseau de neurones sans jamais importer pygame directement.

L'API est délibérément minimaliste : elle ne contient aucune logique de rendu,
aucun gestionnaire d'events, aucun accès aux fichiers ou à la fenêtre. Elle
ne fait que : faire "penser" un cerveau, apprendre de la récompense, et produire
une intention (action + cible + intensité) qui sera interprétée par la couche
supérieure (simulation ou UI).

Toutes les dépendances lourdes (numpy, la structure du réseau) restent dans
brain.py ; ce fichier n'expose que le contrat.
"""
from __future__ import annotations

from typing import Dict, Any, Optional, List

import numpy as np

# Constantes d'action — partagées avec simulation et UI
from game.brain import (
    REST, SLEEP, EAT, DRINK, HARVEST, DROP, BUILD, GIVE, TAKE, ATTACK,
    FLEE, EXPLORE, TALK, MARK, SOCIAL,
    ACTION_NAMES, ACTION_COLORS, N_IN, N_OUT,
    N_STRATEGIES, N_TARGETS, STRATEGY_NAMES, STRATEGY_COLORS,
    TARGET_NAMES, TARGET_COLORS, IMMEDIAT, PRUDENT, ECONOMIQUE,
    COOPERATIF, EXPLORATION, DEFENSIF,
    SOI, NOURRITURE, EAU, BOIS, PIERRE, ABRI, DEPOT_CHANTIER, ETRE_VIVANT,
)

# Import lightweight de la structure Brain (sans dépendre de pygame ou du monde)
from game.brain import Brain


class Intention:
    """Résultat simple et autonome du cerveau — aucun référence pygame/UI.

    action      : index dans 0..14 correspondant au vocabulaire d'actions.
    target_aid  : identifiant d'actif cible (asset id), ou None si pas de cible.
    intensity   : float 0.0 .. 1.0 — force/urgency de l'intention.
    raw_probs   : (optionnel) tableau numpy des probabilités brutes — utile
                   pour le debug ou l'analyse, jamais utilisé par la simulation
                   directement (celle-ci n'a que l'intention choisie).
    strategy    : index de la stratégie choisie (0..5).
    strat_probs : probabilités brutes des stratégies.
    target_type : index du type de cible choisi (0..7).
    targ_probs  : probabilités brutes des types de cible.
    """
    __slots__ = ("action", "target_aid", "intensity", "raw_probs",
                 "strategy", "strat_probs", "target_type", "targ_probs")

    def __init__(self, action: int, target_aid: Optional[int],
                 intensity: float, raw_probs: Optional[np.ndarray] = None,
                 strategy: int = 0, strat_probs: Optional[np.ndarray] = None,
                 target_type: int = 0, targ_probs: Optional[np.ndarray] = None):
        self.action = action
        self.target_aid = target_aid
        self.intensity = float(intensity)
        self.raw_probs = raw_probs
        self.strategy = strategy
        self.strat_probs = strat_probs
        self.target_type = target_type
        self.targ_probs = targ_probs

    def __repr__(self) -> str:
        tgt = f"target={self.target_aid}" if self.target_aid is not None else "pas de cible"
        return f"<Intention action={ACTION_NAMES.get(self.action, self.action)} {tgt} intensité={self.intensity:.2f}>"


def think(brain: Brain, perception: Dict[str, Any]) -> Intention:
    """Faire "penser" un cerveau à partir de sa représentation de perception.

    perception : dict contenant les informations nécessaires au cerveau :
        - corps : dict avec besoins, émotions, état physique
        - monde : dict perception locale (tuiles voisines, ressources visibles)
        - temps : dict avec heure/jour en cours

    Retourne une Intention que la couche supérieure (simulation/UI) appliquera
    au monde via les primitives connues (BUILD, HARVEST, MOVE, etc.).

    Note : brain.py conserve ses poids internes (N_IN=132, N_OUT=15) — cette
    fonction ne fait que Forward pass + échantillonnage d'action.
    """
    x = np.asarray(perception.get("input", np.zeros(N_IN, dtype=np.float64)),
                    dtype=np.float64).ravel()
    if x.shape[0] != N_IN:
        x = np.zeros(N_IN, dtype=np.float64)
    x = x.reshape(1, -1)
    act, probs = brain.think(x, temperature=1.0)

    # Mapping index -> target aid si applicable (selon l'action)
    target_aid = None
    if act == HARVEST:
        # La perception aura fourni la cible potentielle ; ici on laisse None
        # et c'est la simulation qui vérifiera les affordances avant d'agir.
        pass
    elif act == BUILD:
        pass
    elif act == EAT:
        pass

    return Intention(
        action=int(act),
        target_aid=target_aid,
        intensity=brain.probs[act],
        raw_probs=brain.last_out.copy() if hasattr(brain, "last_out") else None,
        strategy=getattr(brain, '_strategy', 0),
        strat_probs=getattr(brain, '_strat_probs', None),
        target_type=getattr(brain, '_target', 0),
        targ_probs=getattr(brain, '_targ_probs', None),
    )


def learn(brain: Brain, reward: float, lr: float = 0.0022,
          age_factor: float = 1.0) -> None:
    """Appliquer un pas d'apprentissage REINFORCE.

    reward      : récompense reçue suite à l'action précédente (peut être négative).
    lr          : taux d'apprentissage (par défaut 0.0022 tel que dans brain.py).
    age_factor  : 0..~2, multiplie le lr — un jeune (>1.0) apprend plus vite,
                  un vieux (<1.0) se fige.

    Ne fait bouger que les poids et biais du cerveau — l'architecture (N_IN,
    N_OUT, nombre de neurones cachés) reste verrouillée.
    """
    brain.learn(reward=reward, lr=lr, age_factor=age_factor)


def explain(brain: Brain, top: int = 5) -> List[Dict[str, Any]]:
    """Classement lisible de la dernière intention, pour le dashboard.

    Retourne une liste de dicts {action, nom, couleur, probabilite}
    triée par probabilité décroissante — aucune connaissance du réseau
    n'est requise côté UI.
    """
    result = brain.explain(top=top)
    # ajouter strategie et cible courantes
    strat = getattr(brain, '_strategy', 0)
    target = getattr(brain, '_target', 0)
    result.append({
        "action": -1,
        "nom": STRATEGY_NAMES.get(strat, "?"),
        "couleur": STRATEGY_COLORS.get(strat, (180, 180, 180)),
        "probabilite": float(getattr(brain, '_strat_probs', np.zeros(N_STRATEGIES))[strat]),
        "type": "strategie",
    })
    result.append({
        "action": -2,
        "nom": TARGET_NAMES.get(target, "?"),
        "couleur": TARGET_COLORS.get(target, (180, 180, 180)),
        "probabilite": float(getattr(brain, '_targ_probs', np.zeros(N_TARGETS))[target]),
        "type": "cible",
    })
    return result


def new_brain(n_hid: int = 128,
              params: Optional[np.ndarray] = None) -> Brain:
    """Créer un nouveau cerveau avec la taille donnée.

    n_hid    : nombre de neurones cachés (taille de la couche intermédiaire).
    params   : poids existants (optionnel) à copier ; si None, poids aléatoires.
    Retourne une instance Brain prête à être utilisée par think()/learn().
    """
    from game.brain import Brain as _Brain
    return _Brain(n_hid=n_hid, params=params)


# ---- Déploiement des constantes partagées ----
# Ces tuples/lists sont aussi définis dans brain.py ; on les réexporte ici
# afin que les autres couches puissent les importer sans importer brain.py
# directement (pour éviter toute dépendance circulaire potentielle).

ACTION_NAMES_EXP = {
    REST: "Repos", SLEEP: "Dormir", EAT: "Manger", DRINK: "Boire",
    HARVEST: "Récolter", DROP: "Poser", BUILD: "Construire",
    GIVE: "Offrir", TAKE: "Prendre", ATTACK: "Attaquer",
    FLEE: "Fuir", EXPLORE: "Explorer", TALK: "Parler", MARK: "Marquer",
    SOCIAL: "Rejoindre",
}

ACTION_TRAIT_EXP = {
    REST: (8, -0.28),
    SLEEP: (11, -0.20),
    EAT: (3, -0.08),
    DRINK: (3, -0.08),
    HARVEST: (8, 0.30),
    DROP: (11, 0.10),
    BUILD: (8, 0.36),
    GIVE: (10, 0.48),
    TAKE: (1, 0.30),
    ATTACK: (1, 0.42),
    FLEE: (3, 0.30),
    EXPLORE: (2, 0.44),
    TALK: (0, 0.42),
    MARK: (9, 0.22),
    SOCIAL: (0, 0.40),
}

SIZES_EXP = (25, 50, 75, 100, 128, 256, 512, 768, 1000)

ACTION_COLORS_EXP = ACTION_COLORS


def think_every(n: int) -> int:
    """Règle la fréquence de réflexion (identique à brain.think_every)."""
    if n <= 128:
        return 2
    if n <= 256:
        return 4
    if n <= 1024:
        return 8
    return 16


def params_size(n: int) -> int:
    """Taille totale des paramètres pour un cerveau de n neurones cachés."""
    return N_IN * n + n + n + N_OUT * n + N_OUT


# Export pratique : importer ces constantespuisque brain.py les a déjà
# on les réexporte ici pour que UI/simulation puissent les avoir sans
# dépendre directement de l'implémentation brain.py (bien qu'ils existent
# dedans aussi). Cela découple les imports "bas niveau".
__all__ = [
    "Intention", "think", "learn", "explain", "new_brain",
    "ACTION_NAMES_EXP", "ACTION_TRAIT_EXP", "ACTION_COLORS", "ACTION_COLORS_EXP",
    "SIZES_EXP",
    "think_every", "params_size",
]