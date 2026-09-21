"""Registre officiel des 132 entrées du vecteur de perception.

Ce fichier est LA source de vérité pour les indices du vecteur sense().
Toute modification d'entrées doit passer par ici.
"""

NIN_VERSION = 3
NIN = 132

INPUT = {
    # Besoins vitaux (0-9)
    "hunger": 0,
    "energy": 1,
    "thirst": 2,
    "sleep": 3,
    "fear_inverse": 4,
    "belonging": 5,
    "esteem_need": 6,
    "health": 7,
    "age": 8,
    "temperature": 9,

    # Corps (10-14)
    "body_start": 10,       # body[0..4]

    # Personnalité (15-26)
    "personality_start": 15, # personality[0..11]

    # Émotions (27-34)
    "emotion_start": 27,     # emotions[0..7]

    # Cognition (35-38)
    "cognition_start": 35,   # cog[0..3]

    # Estime de soi / réputation (39-40)
    "self_esteem": 39,
    "reputation": 40,

    # Social (41-44)
    "near_trust": 41,
    "has_hated": 42,
    "has_partner": 43,
    "is_child": 44,

    # Compétences (45-48)
    "skills_start": 45,      # skills[0..3]

    # Habitudes (49-63)
    "habits_start": 49,      # habits[0..14]

    # Humeur (64)
    "mood": 64,

    # Perception locale 8 canaux (65-72)
    "local_start": 65,       # _loc[0..7]

    # Mémoire spatiale 6 catégories × 3 (73-90)
    "memory_start": 73,

    # Temps (91-94)
    "day_sin": 91,
    "day_cos": 92,
    "weather_temp": 93,
    "rain": 94,

    # Inventaire (95-98)
    "wood_inventory": 95,
    "stone_inventory": 96,
    "seed_inventory": 97,
    "gold_inventory": 98,

    # Outil (99-103)
    "tool_equipped": 99,
    "tool_durability": 100,
    "tool_axe": 101,
    "tool_pickaxe": 102,
    "tool_hammer": 103,

    # Contexte spatial (104-115)
    "food_density": 104,
    "wood_density": 105,
    "stone_density": 106,
    "sheep_near": 107,
    "allies_near": 108,
    "enemies_near": 109,
    "storage_near": 110,
    "storage_food": 111,
    "storage_wood": 112,
    "site_near": 113,
    "site_progress": 114,
    "site_missing": 115,

    # Mémoire de distance (116-119)
    "food_distance": 116,
    "water_distance": 117,
    "shelter_distance": 118,
    "partner_distance": 119,

    # État avancé (120-127)
    "route_danger": 120,
    "neighbor_need": 121,
    "local_reputation": 122,
    "winter": 123,
    "home_storage": 124,
    "inventory_load": 125,
    "local_fear": 126,
    "life_progress": 127,

    # Anima — mémoire épisodique émotionnelle (128-131)
    "trauma_attack": 128,
    "belief_danger": 129,
    "episode_count": 130,
    "anima_fighter": 131,
}

N_ACTIONS = 15
