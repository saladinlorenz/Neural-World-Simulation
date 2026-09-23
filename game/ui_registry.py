"""UI Registry — registres declaratifs de l'interface.

Extrait de dashboard.py. Ces registres ne contiennent aucune
coordonnee Pygame, aucune surface, aucun widget. Ils decrivent
uniquement la structure de l'interface.

Pour ajouter une section ou une carte, ajouter UNE entree ici.
"""
from __future__ import annotations

# ══════════════════════════════════════════════════════════════════════
#  Couleurs d'accent par famille de donnees
# ══════════════════════════════════════════════════════════════════════
C_CORPS = (67, 160, 92)
C_COG = (62, 124, 214)
C_PERSO = (222, 164, 46)
C_EMO = (34, 158, 142)
C_BESOIN = (146, 96, 186)
C_EXP = (206, 126, 60)
C_MEM = (150, 110, 200)

# ══════════════════════════════════════════════════════════════════════
#  Definitions des champs
# ══════════════════════════════════════════════════════════════════════
from .config import (
    BODY_DEFS, COG_DEFS, PERSONALITY_DEFS, EMOTION_DEFS, NEED_DEFS,
)

SKILL_DEFS = ["recolte", "construction", "combat", "social"]

# ══════════════════════════════════════════════════════════════════════
#  Section Registry — accordions de l'inspecteur
#  (cle, libelle, couleur, champs, attribut_agent, attribut_template)
# ══════════════════════════════════════════════════════════════════════
SECTION_REGISTRY = [
    ("body",   "Corps",        C_CORPS,  BODY_DEFS,        "body",        "tpl_body"),
    ("cog",    "Cognition",    C_COG,    COG_DEFS,         "cog",         "tpl_cog"),
    ("perso",  "Personnalite", C_PERSO,  PERSONALITY_DEFS, "personality", "tpl_personality"),
    ("emo",    "Emotions",     C_EMO,    EMOTION_DEFS,     "emotions",    "tpl_emotions"),
    ("needs",  "Besoins",      C_BESOIN, NEED_DEFS,        "needs",       "tpl_needs"),
    ("skills", "Experience",   C_EXP,    SKILL_DEFS,       "skills",      "tpl_skills"),
]

DEFAULT_OPEN = {
    "body": True, "cog": True, "perso": True,
    "emo": True, "needs": False, "skills": False,
}

# ══════════════════════════════════════════════════════════════════════
#  Card Registry — cartes de la colonne droite
# ══════════════════════════════════════════════════════════════════════
CARD_REGISTRY = [
    ("intention", "Intention"),
    ("memoire", "Memoire"),
    ("gabarit", "Gabarit"),
    ("events", "Evenements"),
]

# ══════════════════════════════════════════════════════════════════════
#  Onglets
# ══════════════════════════════════════════════════════════════════════
TABS = [
    ("decor",      "DECOR"),
    ("etre",       "ETRE"),
    ("habitants",  "HABITANTS"),
    ("creator",    "CREATEUR"),
    ("societe",    "SOCIETE"),
    ("journal",    "JOURNAL"),
]

READONLY_TABS = ("societe", "journal", "habitants")

# ══════════════════════════════════════════════════════════════════════
#  Modes d'interaction (outils)
# ══════════════════════════════════════════════════════════════════════
MODES = [
    ("place", "Poser"), ("erase", "Gommer"), ("floor", "Sol"),
    ("block", "Bloc"),
    ("agent", "Etre"), ("sheep", "Mouton"), ("monster", "Monstre"),
    ("inspect", "Examiner"),
    ("water", "Eau"), ("land", "Terre"), ("wall", "Mur"),
    ("carve", "Sculpter"), ("restore", "Restaurer"),
]

SEX_CLASSES = {
    "M": ("swordsman", "archer", "wizard", "pawn"),
    "F": ("knight", "enchantress", "musketeer", "pawn"),
}

TAB_MODES = {
    "decor": [
        ("place", "Poser"), ("erase", "Gommer"), ("floor", "Sol"),
        ("block", "Bloc"),
        ("water", "Eau"), ("land", "Terre"), ("wall", "Mur"),
        ("carve", "Sculpter"), ("restore", "Restaurer"),
        ("inspect", "Examiner"),
    ],
    "etre":     [("agent", "Etre"), ("inspect", "Examiner")],
    "habitants": [("agent", "Creer"), ("inspect", "Examiner")],
    "societe":  [],
    "journal":  [],
}

TAB_HINTS = {
    "place":   "clic = poser l'asset / glisser = peindre",
    "erase":   "clic = effacer les objets de la case",
    "floor":   "clic = peindre le sol selectionne",
    "block":   "clic = construire un bloc (bois ou pierre)",
    "agent":   "clic = inserer l'etre defini dans le gabarit",
    "sheep":   "clic = ajouter un mouton",
    "monster": "clic = ajouter un monstre aleatoire",
    "inspect": "clic = examiner un etre",
    "water":   "glisser = transformer terre en eau (pinceau)",
    "land":    "glisser = transformer eau en terre (pinceau)",
    "wall":    "glisser = placer des rochers solides (pinceau)",
    "carve":   "glisser = creuser les montagnes (pinceau)",
    "restore": "glisser = restaurer le terrain procedural (pinceau)",
}

# ══════════════════════════════════════════════════════════════════════
#  Categories de journal
# ══════════════════════════════════════════════════════════════════════
LOG_CATS = {
    "combat":   (214, 84, 84),
    "social":   (198, 100, 162),
    "meteo":    (62, 124, 214),
    "economie": (206, 160, 50),
    "vie":      (67, 160, 92),
    "mort":     (140, 80, 86),
    "batiment": (96, 154, 96),
    "monde":    (112, 126, 150),
}

LOG_TITLES = {
    "combat":   "Combat",
    "social":   "Social",
    "meteo":    "Meteo",
    "economie": "Economie",
    "vie":      "Vie",
    "mort":     "Mort",
    "batiment": "Batiment",
    "monde":    "Monde",
}

# ══════════════════════════════════════════════════════════════════════
#  Categories d'assets
# ══════════════════════════════════════════════════════════════════════
CAT_ALL = "__all__"
HIDDEN_CATS = {"unites", "interface", "atlas", "rendus"}

CHIP_LABELS = {
    "__all__": "Tous",
    "ressources": "Ressources",
    "nourriture": "Nourriture",
    "batiments": "Batiments",
    "outils": "Outils",
    "animaux": "Animaux",
    "props": "Props",
    "vehicules": "Vehicules",
    "tombe": "Tombes",
    "decor": "Decor",
    "sol": "Sols",
    "unites": "Unites",
    "interface": "Interface",
    "materiaux": "Materiaux",
    "meat_res": "Viande",
    "weapon": "Armes",
    "armor": "Armures",
}

# ══════════════════════════════════════════════════════════════════════
#  Panels — description des panneaux pour le découpage Pygame/Qt
# ══════════════════════════════════════════════════════════════════════
PANELS = {
    "population": {
        "title": "Habitants",
        "snapshot": "population",
        "tab": "habitants",
    },
    "inspector": {
        "title": "Inspecteur",
        "snapshot": "selected_agent",
        "tab": "etre",
    },
    "anima": {
        "title": "Anima",
        "snapshot": "selected_agent.anima",
        "tab": "etre",
    },
    "journal": {
        "title": "Journal",
        "snapshot": "journal",
        "tab": "journal",
    },
    "society": {
        "title": "Societe",
        "snapshot": "society",
        "tab": "societe",
    },
    "assets": {
        "title": "Assets",
        "snapshot": "assets",
        "tab": "decor",
    },
    "creator": {
        "title": "Createur",
        "snapshot": "template",
        "tab": "creator",
    },
    "world_tools": {
        "title": "Outils monde",
        "snapshot": "tools",
        "tab": "decor",
    },
}
