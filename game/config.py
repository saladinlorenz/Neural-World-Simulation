import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(ROOT, "assets")

TILE = 16
GRID = 1000
WORLD_PX = GRID * TILE

# detect screen size dynamically
def _detect_screen():
    try:
        import ctypes
        user32 = ctypes.windll.user32
        return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    except Exception:
        pass
    return 1600, 900

_sw, _sh = _detect_screen()
SCREEN_W = min(_sw - 40, 1600)
SCREEN_H = min(_sh - 80, 900)
LEFT_W = 320
DASH_W = 380
VIEW_W = SCREEN_W - DASH_W - LEFT_W
VIEW_H = SCREEN_H

MAX_POP = 800
MAX_SHEEP = 300
MAX_MONSTERS = 20

BG = (12, 14, 22)
PANEL = (20, 24, 36)
PANEL2 = (26, 30, 44)
INK = (232, 238, 248)
MUTED = (142, 152, 172)
ACCENT = (78, 168, 232)
GOOD = (108, 208, 128)
BAD = (228, 98, 98)
GOLD = (248, 208, 98)

CLAN_COLORS = {
    "blue": (88, 148, 228),
    "red": (218, 88, 78),
    "yellow": (238, 198, 78),
    "purple": (178, 118, 218),
    "black": (62, 68, 82),
}

# ---- temps / climat
# Objectif : 1 h réelle = 10 ans simulés à vitesse ×4
# SIM_HZ=30, ×4 = 120 ticks/s, 1 h = 432 000 ticks
# Calendrier : 20 jours/an (4 saisons × 5 jours)
SIM_HZ = 30
FPS = 20
TARGET_OBSERVATION_SPEED = 4.0
TARGET_YEARS_PER_REAL_HOUR = 10.0
TICKS_PER_REAL_HOUR_AT_TARGET = int(SIM_HZ * TARGET_OBSERVATION_SPEED * 3600)
TICKS_PER_YEAR = int(TICKS_PER_REAL_HOUR_AT_TARGET / TARGET_YEARS_PER_REAL_HOUR)
DAYS_PER_SEASON = 5
SEASONS = ("Printemps", "Été", "Automne", "Hiver")
DAYS_PER_YEAR = DAYS_PER_SEASON * len(SEASONS)
DAY_TICKS = TICKS_PER_YEAR // DAYS_PER_YEAR

# ---- âges biologiques (dérivés du calendrier)
AGE_CHILD_YEARS = 18
AGE_ELDER_YEARS = 65
AGE_MIN_NATURAL_DEATH_YEARS = 75
AGE_MAX_NATURAL_DEATH_YEARS = 95
DEFAULT_SPAWN_AGE_YEARS = 18

AGE_CHILD_TICKS = AGE_CHILD_YEARS * TICKS_PER_YEAR
AGE_ELDER_TICKS = AGE_ELDER_YEARS * TICKS_PER_YEAR
AGE_MIN_NATURAL_DEATH_TICKS = AGE_MIN_NATURAL_DEATH_YEARS * TICKS_PER_YEAR
AGE_MAX_NATURAL_DEATH_TICKS = AGE_MAX_NATURAL_DEATH_YEARS * TICKS_PER_YEAR
DEFAULT_SPAWN_AGE_TICKS = DEFAULT_SPAWN_AGE_YEARS * TICKS_PER_YEAR

SAVE_DIR = os.path.join(ROOT, "data", "saves")

# ---- besoins (couches de l'être)
NEED_DEFS = ["faim", "énergie", "soif", "sommeil", "sécurité", "appartenance", "estime"]
EMOTION_DEFS = ["peur", "joie", "colère", "tristesse", "stress", "surprise",
                "dégoût", "affection"]
BODY_DEFS = ["force", "endurance", "mobilité", "sens", "récupération"]
COG_DEFS = ["mémoire", "anticipation", "imagination", "attention"]
PERSONALITY_DEFS = ["sociabilité", "agressivité", "curiosité", "prudence", "patience",
                    "empathie", "impulsivité", "confiance", "persévérance", "ambition",
                    "générosité", "discipline"]

#: Entrées du journal conservées en mémoire. ``journal_snapshot`` plafonne
#: l'affichage à 200 ; les exports peuvent demander davantage.
JOURNAL_MAXLEN = 2000

#: Matériaux que ``Sim.do_build_block_player`` sait réellement poser : le
#: moteur ne connaît que les rôles ``block_wood`` et ``block_stone``, donc
#: proposer « or » ou « graine » produirait un bloc de bois en silence.
BLOCK_MATERIALS = ("bois", "pierre")

#: Types de monstres que ``Sim.spawn_monster`` peut produire. Source unique :
#: l'UI valide ses choix contre cette liste.
MONSTER_KINDS = ("bear", "wolf", "snake", "beatle")

TOOL_RECIPES = {
    "hache":   {"bois": 2, "pierre": 1, "durability": 40},
    "pioche":  {"bois": 1, "pierre": 3, "durability": 45},
    "marteau": {"bois": 3, "pierre": 2, "durability": 50},
}

# ---- métabolisme (lois biologiques)
HUNGER_RATE = 0.00012
THIRST_RATE = 0.00008
SLEEP_RATE_D = 0.00006
SLEEP_RATE_N = 0.00020
E_DRAIN = 0.00004
MOVE_DRAIN = 0.00018
REST_GAIN = 0.00180
SLEEP_GAIN = 0.00420
SHELTER_BONUS = 1.9
STARVE_HP = 0.00012
THIRST_HP = 0.00012
LOWE_HP = 0.00008
INV_CAP = 8
ATTACK_DMG = 0.16
ATTACK_DMG_TOOL = 0.30
WORK_TICKS = 6
PERCEPT_CELLS = 70

# ---- Fréquences de décision et planification (Phase 2 optimisation)
THINK_INTERVAL = 8
CANDIDATE_INTERVAL = 40
PLAN_INTERVAL = 100
RESOURCE_UPDATE_INTERVAL = 200
REPUTATION_INTERVAL = 120
SOCIETY_INTERVAL = 900
