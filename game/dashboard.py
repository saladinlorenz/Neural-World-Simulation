"""Dashboard — Univers Vivant (style « atelier clair »).

Structure :
    [rail] [ panneau gauche repliable ] [ carte ] [ panneau droit 2 colonnes ]

Tout est piloté par des REGISTRES en haut de fichier :
    · SECTION_REGISTRY  → les accordéons de l'inspecteur (Corps, Cognition…)
    · CARD_REGISTRY     → les cartes de la colonne droite (Intention, Gabarit…)
    · TABS / MODES      → navigation et outils
Ajouter une section ou une carte = ajouter UNE entrée, rien d'autre.

Aucune coordonnée en dur : tout dérive de SCREEN_W / SCREEN_H, et chaque
bloc est rogné à sa zone visible — rien ne peut sortir de l'écran.

API publique inchangée : Dashboard(am), .draw(screen, sim, cam),
.handle_event(ev, sim), .set_ghost(cam), .apply_map_tool(sim, cam, button),
.action, .mode, .tab, .follow, .focus_search, .hover_tile.

⚠ Le panneau gauche étant repliable, la carte n'a plus une largeur fixe :
le moteur de rendu doit lire dash.view_rect() (ou .view_x / .view_w) au
lieu des constantes LEFT_W / VIEW_W de config.

--------------------------------------------------------------------------
AMELIORATIONS (integration inchangee — memes methodes publiques, memes
registres, memes signatures) :

1. Bug corrige dans _identity() : `ag.bonded` est un eid (int) fourni par
   simulation.py (`a.bonded, e.bonded = e.eid, a.eid`), jamais un objet
   Being — l'ancien code faisait `ag.bonded.name` et plantait a la
   selection de tout etre en couple. Resolu via recherche dans sim.agents.
2. Stats "Societe" fiabilisees : `max_gen` et `bonded` n'existent pas dans
   sim.stats (qui ne contient que des compteurs d'evenements) — l'ancien
   affichage montrait donc toujours 0. Calcules en direct.
3. Nouvelle carte INTENTION (CARD_REGISTRY) : classement en direct des
   intentions du cerveau via brain.explain(), avec marquage de celle
   reellement engagee comme but (utile pour voir quand la faisabilite
   du monde ecarte le choix prefere du reseau).
4. Nouvelle carte MEMOIRE : autobiographie de l'etre (a.life) + nombre
   de lieux crus dangereux (belief_places) — fenetre sur le vecu
   subjectif, pas seulement les stats brutes.
5. Presets de vitesse ×1/×2/×4/×8 en plus des +/- existants.
--------------------------------------------------------------------------
"""
import os
import numpy as np
import pygame

from . import config
from .assets_api import CATEGORY_LABELS
from .brain_api import ACTION_NAMES_EXP as ACTION_NAMES, ACTION_COLORS_EXP as ACTION_COLORS, \
    SIZES_EXP as SIZES, think_every
from .config import (BODY_DEFS, CLAN_COLORS, COG_DEFS, DASH_W, EMOTION_DEFS,
                     GRID, LEFT_W, NEED_DEFS, PERSONALITY_DEFS, SCREEN_H,
                     SCREEN_W, TILE)


from dataclasses import dataclass


@dataclass
class ScrollState:
    offset: int = 0
    drag_grab_y: int | None = None


class ScrollController:
    """Scrollbar déterministe : molette douce, drag précis, clic piste = page."""
    MIN_HANDLE = 32
    WHEEL_STEP = 28

    @staticmethod
    def clamp(offset, content_h, view_h):
        return max(0, min(int(offset), max(0, int(content_h) - int(view_h))))

    @classmethod
    def handle_rect(cls, track, content_h, offset):
        track = pygame.Rect(track)
        if content_h <= track.height:
            return None
        max_offset = max(1, content_h - track.height)
        handle_h = max(cls.MIN_HANDLE, int(track.height * track.height / content_h))
        handle_h = min(track.height, handle_h)
        travel = max(1, track.height - handle_h)
        y = track.y + int((offset / max_offset) * travel)
        return pygame.Rect(track.x + 2, y, max(6, track.width - 4), handle_h)

    @classmethod
    def wheel(cls, state, wheel_y, content_h, view_h):
        state.offset = cls.clamp(
            state.offset - int(wheel_y) * cls.WHEEL_STEP, content_h, view_h)
        return state.offset

    @classmethod
    def press(cls, state, pos, track, content_h, view_h):
        track = pygame.Rect(track)
        handle = cls.handle_rect(track, content_h, state.offset)
        if handle is None or not track.collidepoint(pos):
            return False
        if handle.collidepoint(pos):
            state.drag_grab_y = pos[1] - handle.y
            return True
        if pos[1] < handle.y:
            state.offset -= int(view_h * 0.85)
        else:
            state.offset += int(view_h * 0.85)
        state.offset = cls.clamp(state.offset, content_h, view_h)
        return True

    @classmethod
    def drag(cls, state, pos, track, content_h, view_h):
        if state.drag_grab_y is None:
            return False
        track = pygame.Rect(track)
        handle = cls.handle_rect(track, content_h, state.offset)
        if handle is None:
            state.drag_grab_y = None
            return False
        max_offset = max(1, content_h - track.height)
        travel = max(1, track.height - handle.height)
        target_y = pos[1] - state.drag_grab_y
        ratio = max(0.0, min(1.0, (target_y - track.y) / travel))
        state.offset = cls.clamp(int(ratio * max_offset), content_h, view_h)
        return True

    @staticmethod
    def release(state):
        state.drag_grab_y = None


# ══════════════════════════════════════════════════════════════════════
#  1. DESIGN TOKENS
# ══════════════════════════════════════════════════════════════════════
class T:
    APP = (238, 240, 244)          # fond application
    RAIL = (246, 247, 249)         # rail d'icônes
    SURFACE = (255, 255, 255)
    SURFACE_2 = (250, 251, 253)
    HOVER = (241, 244, 249)
    SELECT = (232, 240, 253)
    TRACK = (237, 239, 244)   # plus discret
    BORDER = (226, 229, 235)
    BORDER_2 = (205, 210, 219)
    TEXT = (31, 36, 48)
    MUTED = (105, 114, 129)
    FAINT = (156, 163, 176)
    ON_DARK = (255, 255, 255)
    ACCENT = (59, 118, 214)
    DARK = (32, 38, 50)            # badge neurones
    DANGER = (214, 84, 84)
    WARN = (222, 160, 50)
    OK = (72, 158, 104)
    TIP_BG = (34, 40, 52)
    TIP_FG = (232, 236, 243)
    TIP_MUTED = (150, 159, 174)
    S1, S2, S3, S4, S5 = 4, 8, 12, 16, 24
    R1, R2, R3 = 6, 9, 13
    F_MICRO, F_SMALL, F_BODY, F_SUB, F_TITLE = 11, 12, 13, 15, 18
    H_ROW = 22                # la pilule respire mieux
    H_HEAD = 27
    H_BTN = 25
    H_TAB = 28
    H_FIELD = 27
    CELL = 68
    RAIL_W = 46


# — accents par famille de donnée, réutilisés partout —
C_CORPS = (67, 160, 92)
C_COG = (62, 124, 214)
C_PERSO = (222, 164, 46)
C_EMO = (34, 158, 142)
C_BESOIN = (146, 96, 186)
C_EXP = (206, 126, 60)
C_MEM = (150, 110, 200)

FONT_STACK = "segoeui,seguisb,inter,dejavusans,liberationsans,arial"


# ══════════════════════════════════════════════════════════════════════
#  2. REGISTRES — le seul endroit à toucher pour étendre l'interface
# ══════════════════════════════════════════════════════════════════════
SKILL_DEFS = ["récolte", "construction", "combat", "social"]

#  (clé, libellé, couleur, libellés des champs, attribut agent, attribut gabarit)
SECTION_REGISTRY = [
    ("body",   "Corps",        C_CORPS,  BODY_DEFS,        "body",        "tpl_body"),
    ("cog",    "Cognition",    C_COG,    COG_DEFS,         "cog",         "tpl_cog"),
    ("perso",  "Personnalité", C_PERSO,  PERSONALITY_DEFS, "personality", "tpl_personality"),
    ("emo",    "Émotions",     C_EMO,    EMOTION_DEFS,     "emotions",    "tpl_emotions"),
    ("needs",  "Besoins",      C_BESOIN, NEED_DEFS,        "needs",       "tpl_needs"),
    ("skills", "Expérience",   C_EXP,    SKILL_DEFS,       "skills",      "tpl_skills"),
]
DEFAULT_OPEN = {"body": True, "cog": True, "perso": True,
                "emo": True, "needs": False, "skills": False}

#  Cartes de la colonne de droite : (clé, nom de la méthode de rendu)
#  Chaque méthode a la signature (self, screen, rect, sim) -> hauteur utilisée.
CARD_REGISTRY = [
    ("intention", "_card_intention"),
    ("memoire", "_card_memoire"),
    ("gabarit", "_card_gabarit"),
    ("events", "_card_events"),
]

MODES = [("place", "Poser"), ("erase", "Gommer"), ("floor", "Sol"),
         ("block", "Bloc"),
         ("agent", "Être"), ("sheep", "Mouton"), ("monster", "Monstre"),
         ("inspect", "Examiner"),
         ("water", "Eau"), ("land", "Terre"), ("wall", "Mur"),
         ("carve", "Sculpter"), ("restore", "Restaurer")]

SEX_CLASSES = {
    "M": ("swordsman", "archer", "wizard", "pawn"),
    "F": ("knight", "enchantress", "musketeer", "pawn"),
}
TAB_MODES = {
    "decor":    [("place", "Poser"), ("erase", "Gommer"), ("floor", "Sol"),
                 ("block", "Bloc"),
                 ("water", "Eau"), ("land", "Terre"), ("wall", "Mur"),
                 ("carve", "Sculpter"), ("restore", "Restaurer"),
                 ("inspect", "Examiner")],
    "etre":     [("agent", "Être"), ("inspect", "Examiner")],
    "habitants": [("agent", "Créer"), ("inspect", "Examiner")],
    "societe":  [],
    "journal":  [],
}
TAB_HINTS = {
    "place": "clic = poser l'asset · glisser = peindre",
    "erase": "clic = effacer les objets de la case",
    "floor": "clic = peindre le sol sélectionné",
    "agent": "clic = insérer l'être défini dans le gabarit",
    "sheep": "clic = ajouter un mouton",
    "monster": "clic = ajouter un monstre aléatoire",
    "inspect": "clic = examiner un être",
    "water": "glisser = transformer terre en eau (pinceau)",
    "land": "glisser = transformer eau en terre (pinceau)",
    "wall": "glisser = placer des rochers solides (pinceau)",
    "carve": "glisser = creuser les montagnes (pinceau)",
    "restore": "glisser = restaurer le terrain procédural (pinceau)",
}
TABS = [("decor", "DÉCOR"), ("etre", "ÊTRE"), ("habitants", "HABITANTS"),
        ("creator", "CRÉATEUR"),
        ("societe", "SOCIÉTÉ"), ("journal", "JOURNAL")]
READONLY_TABS = ("societe", "journal", "habitants")
CAT_ALL = "__all__"
HIDDEN_CATS = {"unites", "interface", "atlas", "rendus"}

LOG_CATS = {"combat": (214, 84, 84), "social": (198, 100, 162),
            "meteo": (62, 124, 214), "economie": (206, 160, 50),
            "vie": (67, 160, 92), "mort": (140, 80, 86),
            "batiment": (96, 154, 96), "monde": (112, 126, 150)}
LOG_TITLES = {"combat": "Combat", "social": "Social", "meteo": "Météo",
              "economie": "Économie", "vie": "Vie", "mort": "Mort",
              "batiment": "Bâtiment", "monde": "Monde"}

CHIP_LABELS = {"__all__": "Tous", "ressources": "Ressources", "nourriture": "Nourriture",
               "batiments": "Bâtiments", "outils": "Outils", "animaux": "Animaux",
               "props": "Props", "vehicules": "Véhicules", "tombe": "Tombes",
               "decor": "Décor", "sol": "Sols", "unites": "Unités",
               "effets": "Effets", "interface": "Interface", "atlas": "Atlas",
               "rendus": "Rendus", "divers": "Divers"}

#  Légende de la carte (overlay coin haut-droit du viewport)
MAP_LEGEND = [("Fertilité", (126, 196, 122)), ("Ressource", (226, 186, 78)),
              ("Danger", (218, 108, 100))]

SPEED_PRESETS = (1, 2, 4, 8)


def _mix(a, b, t):
    return (int(a[0] + (b[0] - a[0]) * t), int(a[1] + (b[1] - a[1]) * t),
            int(a[2] + (b[2] - a[2]) * t))


def _tint(c, t=0.12):
    return _mix(T.SURFACE, c, t)


def _goal_txt(a):
    if a is not None and getattr(a, "goal", None):
        return f"{ACTION_NAMES.get(a.goal['act'], '?')} → ({a.goal['x']},{a.goal['y']})"
    return "—"


# ══════════════════════════════════════════════════════════════════════
#  3. DASHBOARD
# ══════════════════════════════════════════════════════════════════════
class Dashboard:
    def __init__(self, am):
        self.am = am
        # — largeurs : bornées pour ne jamais écraser la carte —
        self.panel_l = min(LEFT_W, 320)
        self.panel_r = min(DASH_W, 420)
        self.left_open = True
        self.x0 = SCREEN_W - self.panel_r          # recalculé à chaque frame
        self.view_x, self.view_w = 0, 0

        self.mode = "agent"
        trees = am.pool("tree")
        self.asset = trees[0] if trees else 0
        self.category = CAT_ALL
        self.tab = "etre"
        self.search = ""
        self.hab_search = ""
        self.focus_search = False
        self.hab_focus = False
        self.scroll = 0
        self.filtered = [a.id for a in am.assets]
        self._filter_sig = None
        self.hover_asset = None
        self.hover_tile = (0, 0)
        self.recents, self.favs = [], []
        self.only_favs = False
        self.jfilter = "tous"
        self.sections = dict(DEFAULT_OPEN)
        self.cards_open = {k: True for k, _ in CARD_REGISTRY}

        # — portraits (portraits 64x64)
        self.portraits = {}
        self._load_portraits()

        self.brain_size = 128
        self._init_state()

    def _load_portraits(self):
        # La v1 pointait vers un chemin absolu Windows ("E:\\my world2\\...") :
        # aucun portrait ne se chargeait ailleurs que sur la machine d'origine.
        # On cherche maintenant à côté du paquet, puis à côté du script.
        here = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.environ.get("UNIVERS_PORTRAITS", ""),
            os.path.join(here, "assets", "portraits"),
            os.path.join(here, "..", "assets", "portraits"),
            os.path.join(os.getcwd(), "assets", "portraits"),
        ]
        base = next((os.path.normpath(c) for c in candidates
                     if c and os.path.isdir(c)), None)
        if base is None:
            return
        mapping = {
            # (sex, cls) -> filename
            ("M", "swordsman"): "male_swordsman",
            ("M", "archer"): "male_archer",
            ("M", "wizard"): "male_wizard",
            ("M", "pawn"): "male_swordsman",
            ("F", "knight"): "female_knight",
            ("F", "enchantress"): "female_enchantress",
            ("F", "musketeer"): "female_musketeer",
            ("F", "pawn"): "female_knight",
        }
        for key, fname in mapping.items():
            path = os.path.join(base, f"{fname}.png")
            if not os.path.exists(path):
                continue
            try:
                self.portraits[key] = pygame.image.load(path).convert_alpha()
            except pygame.error:
                pass   # un fichier illisible ne doit pas empêcher le démarrage

    def _get_portrait(self, sex, cls):
        key = (sex, cls.lower())
        if key in self.portraits:
            return self.portraits[key]
        # fallback par sexe
        fallback = ("M", "pawn") if sex == "M" else ("F", "pawn")
        return self.portraits.get(fallback)

    def _get_cached_portrait(self, sex, cls, size=24):
        if not hasattr(self, '_portrait_cache'):
            self._portrait_cache = {}
        ckey = (sex, cls.lower(), size)
        if ckey not in self._portrait_cache:
            p = self._get_portrait(sex, cls)
            if p:
                self._portrait_cache[ckey] = pygame.transform.smoothscale(p, (size, size))
            else:
                self._portrait_cache[ckey] = None
        return self._portrait_cache[ckey]

    def template_classes(self):
        candidates = SEX_CLASSES.get(self.tpl_sex, ("pawn",))
        available = []
        for cls in candidates:
            states = self.am.skin_states(self.tpl_color, cls)
            if states.get("idle"):
                available.append(cls)
        if not available:
            available = self.am.unit_classes(self.tpl_color) or ["pawn"]
        return available

    def normalize_template_class(self):
        choices = self.template_classes()
        if self.tpl_cls not in choices:
            self.tpl_cls = choices[0]

    def report_ui_error(self, context, exc):
        """Erreur non bloquante mais visible dans stderr et journal si disponible."""
        import traceback
        print(f"[Dashboard:{context}] {exc}")
        traceback.print_exc(limit=2)
        if self._sim_ref is not None:
            self._sim_ref.log(f"Erreur UI ({context}) : {type(exc).__name__}",
                              (214, 84, 84), "monde")

    def brain_memory_estimate_mb(self, n=None):
        """Poids Elman float64 : Wx(95*n)+Wd(n*n)+Wo(15*n)+biais."""
        n = int(n if n is not None else self.brain_size)
        params = 95 * n + n * n + n + 15 * n + 15
        return params * 8 / (1024 * 1024)

    def _init_state(self):
        self.tpl_color, self.tpl_cls, self.tpl_sex = "blue", "pawn", "M"
        self.tpl_body = np.full(len(BODY_DEFS), 0.5)
        self.tpl_cog = np.full(len(COG_DEFS), 0.5)
        self.tpl_personality = np.full(len(PERSONALITY_DEFS), 0.5)
        self.tpl_emotions = np.full(len(EMOTION_DEFS), 0.2)
        self.tpl_needs = np.full(len(NEED_DEFS), 0.5)
        self.tpl_skills = np.zeros(len(SKILL_DEFS))
        self.brush_size = 3          # rayon en tiles (3 = 5×5)
        self.hdel_pending = None     # eid en attente de confirmation de suppression
        self._needs_save = False     # vrai après spawn → déclenche auto-save
        self.spawn_modal = False     # True = fenêtre modale de spawn ouverte
        self.block_material = "bois" # matériau pour le mode Bloc
        self.drag = None
        self.follow = False
        self.action = None
        self.painting = None
        self.creator_focus = False
        self.selected_tile = None    # (tx, ty) de la dernière tuile examinée
        self.last_tile_snapshot = None
        self.active_overlay = "none"
        from .tool_editor import ToolEditor
        self.tool_editor = ToolEditor()
        self.tool_editor_kind = "hache"
        self._cam = None
        self._sim_ref = None
        self._over_map = False
        self._scroll = {t: 0 for t, _ in TABS}
        self._scroll["_left"] = 0
        self._scroll["_right"] = 0
        self._content_h = dict(self._scroll)
        self.buttons, self._cells, self._slider_geo = [], [], {}
        self._scroll_geo = {}
        self._hit_clip = None
        self._minimap_surf, self._minimap_ver = None, -1
        self._fonts = {}
        self.scroll_state = {k: ScrollState() for k in
                             ("decor", "etre", "habitants", "societe", "journal", "creator", "_left")}
        self.scroll_tracks = {}
        # Modal scroll state
        self.modal_scroll = ScrollState()
        self.modal_view = None
        self.modal_content_h = 0
        self.modal_track = None
        self.modal_handle = None

    # compat ascendante
    @property
    def pscroll(self):
        return self._scroll.get(self.tab, 0)

    @property
    def hscroll(self):
        return self._scroll.get("habitants", 0)

    # ── 3.1 primitives ──────────────────────────────────────────────
    def _font(self, size, bold=False):
        k = (size, bold)
        if k not in self._fonts:
            self._fonts[k] = pygame.font.SysFont(FONT_STACK, size, bold=bold)
        return self._fonts[k]

    def _clip_text(self, size, txt, max_w, bold=False):
        f = self._font(size, bold)
        if max_w is None or f.size(txt)[0] <= max_w:
            return txt
        ew = f.size("…")[0]
        out = ""
        for ch in txt:
            if f.size(out + ch)[0] + ew > max_w:
                break
            out += ch
        return out + "…"

    def _t(self, s, size, txt, col, x, y, cx=False, cy=False, bold=False,
           right=False, max_w=None, maxw=None):
        if max_w is None:
            max_w = maxw
        txt = self._clip_text(size, str(txt), max_w, bold)
        img = self._font(size, bold).render(txt, True, col)
        if cx:
            x -= img.get_width() // 2
        if right:
            x -= img.get_width()
        if cy:
            y -= img.get_height() // 2
        s.blit(img, (x, y))
        return img.get_width()

    def _tw(self, size, txt, bold=False):
        return self._font(size, bold).size(str(txt))[0]

    def _push(self, rect, fid):
        """Zone cliquable, rognée à la région visible courante."""
        if fid is None:
            return
        r = pygame.Rect(rect)
        if self._hit_clip is not None:
            r = r.clip(self._hit_clip)
            if r.width <= 0 or r.height <= 0:
                return
        self.buttons.append((r, fid))

    def _card(self, s, rect, radius=T.R2, fill=T.SURFACE, border=T.BORDER):
        r = pygame.Rect(rect)
        pygame.draw.rect(s, fill, r, border_radius=radius)
        if border:
            pygame.draw.rect(s, border, r, 1, border_radius=radius)
        return r

    def _btn(self, s, rect, label, fid, primary=False, disabled=False,
             size=T.F_SMALL, radius=T.R1, icon=None):
        r = pygame.Rect(rect)
        hov = (not disabled) and r.collidepoint(pygame.mouse.get_pos())
        if disabled:
            bg, fg, bd = T.SURFACE_2, T.FAINT, T.BORDER
        elif primary:
            bg, fg, bd = (_mix(T.ACCENT, (0, 0, 0), .12) if hov else T.ACCENT), T.ON_DARK, None
        else:
            bg, fg, bd = (T.HOVER if hov else T.SURFACE), T.TEXT, (T.BORDER_2 if hov else T.BORDER)
        pygame.draw.rect(s, bg, r, border_radius=radius)
        if bd:
            pygame.draw.rect(s, bd, r, 1, border_radius=radius)
        tx = r.centerx + (6 if icon else 0)
        if icon:
            icon(s, r.x + 12, r.centery, fg)
        self._t(s, size, label, fg, tx, r.centery, cx=True, cy=True,
                max_w=r.width - (24 if icon else 10))
        if not disabled:
            self._push(r, fid)
        return r

    def _chip(self, s, rect, label, fid, sel=False, color=None, size=T.F_MICRO):
        r = pygame.Rect(rect)
        col = color or T.ACCENT
        hov = r.collidepoint(pygame.mouse.get_pos())
        if sel:
            bg, fg, bd = col, T.ON_DARK, col
        else:
            bg, fg, bd = (T.HOVER if hov else T.SURFACE), (T.TEXT if hov else T.MUTED), T.BORDER
        rad = r.height // 2
        pygame.draw.rect(s, bg, r, border_radius=rad)
        pygame.draw.rect(s, bd, r, 1, border_radius=rad)
        self._t(s, size, label, fg, r.centerx, r.centery, cx=True, cy=True,
                max_w=r.width - 10)
        self._push(r, fid)
        return r

    def _bar(self, s, rect, v, col, radius=None):
        r = pygame.Rect(rect)
        rad = r.height // 2 if radius is None else radius
        pygame.draw.rect(s, T.TRACK, r, border_radius=rad)
        w = int(r.width * max(0.0, min(1.0, float(v))))
        if w >= 2:
            pygame.draw.rect(s, col, (r.x, r.y, max(w, r.height), r.height),
                             border_radius=rad)
        return r

    # — petites icônes vectorielles (pas d'emoji : rendu non garanti) —
    def _i_search(self, s, x, y, c):
        pygame.draw.circle(s, c, (x, y - 1), 4, 1)
        pygame.draw.line(s, c, (x + 3, y + 2), (x + 6, y + 5), 1)

    def _i_lock(self, s, x, y, c):
        pygame.draw.rect(s, c, (x - 4, y - 1, 9, 7), border_radius=2)
        pygame.draw.arc(s, c, (x - 3, y - 7, 7, 9), 0, 3.15, 1)

    def _i_home(self, s, x, y, c):
        pygame.draw.polygon(s, c, [(x, y - 7), (x + 8, y), (x - 8, y)])
        pygame.draw.rect(s, c, (x - 5, y, 10, 7), border_radius=1)

    def _i_layers(self, s, x, y, c):
        for i, dy in enumerate((-5, 0, 5)):
            pygame.draw.polygon(s, c if i == 0 else _mix(c, T.SURFACE, .45),
                                [(x, y + dy - 3), (x + 7, y + dy),
                                 (x, y + dy + 3), (x - 7, y + dy)], 0 if i == 0 else 1)

    def _i_star(self, s, x, y, c, filled=True, rad=7):
        pts = []
        for i in range(10):
            a = -np.pi / 2 + i * np.pi / 5
            rr = rad if i % 2 == 0 else rad * .45
            pts.append((x + rr * np.cos(a), y + rr * np.sin(a)))
        pygame.draw.polygon(s, c, pts, 0 if filled else 1)

    def _chevron(self, s, x, y, c, open_):
        pts = ([(x - 4, y - 2), (x + 4, y - 2), (x, y + 3)] if open_
               else [(x - 2, y - 4), (x + 3, y), (x - 2, y + 4)])
        pygame.draw.polygon(s, c, pts)

    def _scrollbar(self, s, region, total, off, scroll_key=None):
        """Scrollbar avec ScrollController : molette douce, drag précis."""
        if total <= region.height:
            return
        bar_w = 14
        x = region.right - bar_w
        track = pygame.Rect(x, region.y, bar_w, region.height)
        if scroll_key is not None:
            self.scroll_tracks[scroll_key] = (track, int(total))
            state = self.scroll_state_for(scroll_key)
            state.offset = ScrollController.clamp(off, total, region.height)
            self._scroll[scroll_key] = state.offset
        handle = ScrollController.handle_rect(track, total, off)
        if handle is None:
            return

        # Draw track background
        pygame.draw.rect(s, (235, 238, 244), track, border_radius=7)
        pygame.draw.rect(s, (207, 213, 223), track, 1, border_radius=7)

        # Draw handle with hover effect
        hovering = handle.collidepoint(pygame.mouse.get_pos())
        state = self.scroll_state_for(scroll_key) if scroll_key else None
        is_dragging = state is not None and state.drag_grab_y is not None
        color = (77, 104, 140) if hovering or is_dragging else (125, 136, 152)
        pygame.draw.rect(s, color, handle, border_radius=6)

        # Register handle and track for interaction
        self._push(handle, f"scrollthumb:{scroll_key}")
        self._push(track, f"scrolltrack:{scroll_key}")

    def current_scroll_key(self):
        return self.tab

    def scroll_state_for(self, key=None):
        k = key or self.current_scroll_key()
        if k not in self.scroll_state:
            self.scroll_state[k] = ScrollState()
        return self.scroll_state[k]

    # ── 3.2 layout ──────────────────────────────────────────────────
    def _mm(self):
        return max(92, min(126, SCREEN_H // 9))

    def footer_h(self):
        return self._mm() + T.S2 + T.H_BTN + T.S2 + T.H_BTN + T.S3

    def footer_top(self):
        return SCREEN_H - self.footer_h()

    def content_top(self):
        return 150

    def content_bottom(self):
        return self.footer_top() - T.S2

    def left_w(self):
        return self.panel_l if self.left_open else 0

    def view_rect(self):
        """Zone de la carte — à utiliser par le moteur de rendu."""
        x = T.RAIL_W + self.left_w()
        return pygame.Rect(x, 0, self.x0 - x, SCREEN_H)

    def minimap_rect(self):
        s = self._mm()
        return pygame.Rect(self.x0 + T.S3, self.footer_top(), s, s)

    def _cols(self, w):
        return max(1, (w - T.S2) // T.CELL)

    @staticmethod
    def _clamp(v, total, view_h):
        return max(0, min(int(v), max(0, total - view_h)))

    # ── 3.3 filtres ─────────────────────────────────────────────────
    def _refilter(self):
        sig = (self.category, self.search.lower(), self.only_favs, len(self.favs))
        if sig == self._filter_sig:
            return
        self._filter_sig = sig
        pool = self.am.assets
        if self.only_favs:
            pool = [a for a in pool if a.id in self.favs]
        if self.category == CAT_ALL:
            pool = [a for a in pool if a.category not in HIDDEN_CATS]
        elif self.category:
            pool = [a for a in pool if a.category == self.category]
        if self.search:
            q = self.search.lower()
            pool = [a for a in pool if q in a.name.lower()]
        self.filtered = [a.id for a in pool]
        self._scroll["_left"] = 0
        self._scroll["decor"] = 0

    def _habitants(self, sim):
        alive = [a for a in sim.agents if getattr(a, "alive", True)]
        q = self.hab_search.lower().strip()
        if not q:
            return alive
        return [a for a in alive
                if q in f"{a.name} {a.color} {getattr(a,'cls','')} "
                        f"{getattr(a,'stage','')}".lower()]

    def _array(self, ag, key):
        for k, _l, _c, _n, attr_ag, attr_tpl in SECTION_REGISTRY:
            if k == key:
                return getattr(ag, attr_ag, None) if ag is not None \
                    else getattr(self, attr_tpl, None)
        return None

    def _measure_content(self, key, sim):
        """Pré-mesure la hauteur d'un onglet pour que le scroll fonctionne
        avant le premier rendu."""
        rh = 38
        if key == "habitants":
            people = self._habitants(sim)
            self._content_h["habitants"] = len(people) * rh + T.S2
        elif key == "etre":
            self._content_h["etre"] = 800
        elif key == "_right":
            self._content_h["_right"] = 800
        elif key == "decor":
            self._content_h["decor"] = 600
        elif key == "societe":
            self._content_h["societe"] = 600
        elif key == "journal":
            self._content_h["journal"] = 600

    # ══════════════════════════════════════════════════════════════════
    #  4. RENDU
    # ══════════════════════════════════════════════════════════════════
    def draw(self, screen, sim, cam):
        self.buttons.clear()
        self._cells.clear()
        self._slider_geo.clear()
        self._hit_clip = None
        self._cam, self._sim_ref = cam, sim
        self.x0 = SCREEN_W - self.panel_r
        vr = self.view_rect()
        self.view_x, self.view_w = vr.x, vr.width
        self._refilter()

        self._rail(screen)
        if self.left_open:
            self._left_panel(screen)
        self._map_overlay(screen, vr)

        pygame.draw.rect(screen, T.APP, (self.x0, 0, self.panel_r, SCREEN_H))
        pygame.draw.line(screen, T.BORDER_2, (self.x0, 0), (self.x0, SCREEN_H))
        self._header(screen, sim)
        self._toolbar(screen)
        self._tabs(screen)

        y = self.content_top()
        {"decor": self._tab_decor, "etre": self._tab_etre,
         "habitants": self._tab_habitants, "societe": self._tab_societe,
         "journal": self._tab_journal,
         "creator": self._tab_creator}[self.tab](screen, sim, y)

        self._footer(screen, sim, cam)
        self._tooltip(screen)
        self._draw_spawn_modal(screen, sim)

    # ── 4.1 rail d'icônes ───────────────────────────────────────────
    def _rail(self, screen):
        if not self.left_open:
            # mini-bouton pour réouvrir le catalogue
            r = pygame.Rect(4, T.S3, T.RAIL_W - 8, 34)
            hov = r.collidepoint(pygame.mouse.get_pos())
            pygame.draw.rect(screen, T.HOVER if hov else T.RAIL, r, border_radius=T.R1)
            pygame.draw.rect(screen, T.BORDER, r, 1, border_radius=T.R1)
            self._i_layers(screen, r.centerx, r.centery, T.ACCENT)
            self._push(r, "toggle_left")
            return
        pygame.draw.rect(screen, T.RAIL, (0, 0, T.RAIL_W, SCREEN_H))
        pygame.draw.line(screen, T.BORDER_2, (T.RAIL_W - 1, 0), (T.RAIL_W - 1, SCREEN_H))
        items = [("home", self._i_home, False),
                 ("toggle_left", self._i_layers, self.left_open),
                 ("only_favs", lambda s, x, y, c: self._i_star(s, x, y, c, self.only_favs),
                  self.only_favs)]
        for i, (fid, icon, active) in enumerate(items):
            r = pygame.Rect(7, T.S3 + i * 42, T.RAIL_W - 14, 34)
            hov = r.collidepoint(pygame.mouse.get_pos())
            if active:
                pygame.draw.rect(screen, T.SELECT, r, border_radius=T.R1)
            elif hov:
                pygame.draw.rect(screen, T.HOVER, r, border_radius=T.R1)
            icon(screen, r.centerx, r.centery, T.ACCENT if active else T.MUTED)
            self._push(r, fid)

    # ── 4.2 panneau gauche — catalogue ──────────────────────────────
    def _left_panel(self, screen):
        w = self.panel_l
        x = T.RAIL_W
        pygame.draw.rect(screen, T.APP, (x, 0, w, SCREEN_H))
        # pas de bordure droite ici — le rail gère la séparation
        mouse = pygame.mouse.get_pos()
        y = T.S3

        self._t(screen, T.F_SUB, "CATALOGUE", T.TEXT, x + T.S3, y, bold=True)
        cl = pygame.Rect(x + w - T.S3 - 22, y - 2, 22, 20)
        self._t(screen, T.F_BODY, "‹", T.MUTED, cl.centerx, cl.centery, cx=True, cy=True)
        self._push(cl, "toggle_left")
        y += 26

        # recherche
        sr = pygame.Rect(x + T.S3, y, w - 2 * T.S3, T.H_FIELD)
        self._card(screen, sr, T.R1, T.SURFACE, T.ACCENT if self.focus_search else T.BORDER_2)
        self._i_search(screen, sr.x + 14, sr.centery, T.MUTED)
        if self.search:
            self._t(screen, T.F_BODY, self.search, T.TEXT, sr.x + 26, sr.centery,
                    cy=True, max_w=sr.width - 50)
            cr = pygame.Rect(sr.right - 22, sr.centery - 8, 16, 16)
            self._t(screen, T.F_BODY, "×", T.MUTED, cr.centerx, cr.centery, cx=True, cy=True)
            self._push(cr, "search_clear")
        else:
            self._t(screen, T.F_BODY, "Rechercher un asset…", T.FAINT,
                    sr.x + 26, sr.centery, cy=True)
        self._push(sr, "search")
        y = sr.bottom + T.S2

        # chips catégories (repliées sur 2 lignes max)
        cats = [CAT_ALL] + list(dict(CATEGORY_LABELS).keys())
        fx, fy, lines = x + T.S3, y, 0
        for cat in cats:
            lbl = CHIP_LABELS.get(cat, cat.capitalize())
            cw = self._tw(T.F_MICRO, lbl) + 16
            if fx + cw > x + w - T.S3:
                fx, fy, lines = x + T.S3, fy + 23, lines + 1
                if lines >= 3:
                    break
            self._chip(screen, (fx, fy, cw, 19), lbl, f"cat:{cat}", self.category == cat)
            fx += cw + T.S1
        y = fy + 26

        self._t(screen, T.F_MICRO, f"{len(self.filtered)} assets", T.FAINT, x + T.S3 + 2, y)
        if self.favs:
            self._t(screen, T.F_MICRO, f"{len(self.favs)} favoris", T.FAINT,
                    x + w - T.S3, y, right=True)
        y += 17

        # favoris / récents
        items = (self.favs + [r for r in self.recents if r not in self.favs])[:self._cols(w)]
        if items:
            self._t(screen, T.F_SMALL, "FAVORIS / RÉCENTS", T.MUTED, x + T.S3, y, bold=True)
            y += 17
            for i, aid in enumerate(items):
                r = pygame.Rect(x + T.S3 + i * (T.CELL - 10), y, T.CELL - 16, T.CELL - 16)
                if r.right > x + w - T.S2:
                    break
                sel = aid == self.asset
                self._card(screen, r, T.R1,
                           T.SELECT if sel else (T.HOVER if r.collidepoint(mouse) else T.SURFACE),
                           T.ACCENT if sel else T.BORDER)
                if aid < len(self.am.assets):
                    tile = self.am.thumbnail(aid, T.CELL - 30)
                    if tile:
                        screen.blit(tile, (r.centerx - tile.get_width() // 2,
                                           r.centery - tile.get_height() // 2))
                if aid in self.favs:
                    self._i_star(screen, r.right - 8, r.y + 8, T.WARN, True, 5)
                self._push(r, f"asset:{aid}")
            y += T.CELL - 16 + T.S3

        region = pygame.Rect(x, y, w, SCREEN_H - y - T.S2)
        self._left_region_h = region.height
        self._content_h["_left"] = self._grid(screen, region, self._scroll["_left"], scroll_key="_left")

    # ── 4.3 grille d'assets (mutualisée) ────────────────────────────
    def _grid(self, screen, region, off, scroll_key=None):
        cols = self._cols(region.width)
        row_h = T.CELL + 14
        rows = (len(self.filtered) + cols - 1) // cols
        total = rows * row_h + T.S2
        old, oldhit = screen.get_clip(), self._hit_clip
        screen.set_clip(region)
        self._hit_clip = region
        mouse = pygame.mouse.get_pos()
        first = max(0, off // row_h)
        last = min(rows, first + region.height // row_h + 2)

        for row in range(first, last):
            for col in range(cols):
                k = row * cols + col
                if k >= len(self.filtered):
                    break
                r = pygame.Rect(region.x + T.S2 + col * T.CELL,
                                region.y + T.S2 + row * row_h - off,
                                T.CELL - T.S2, T.CELL - T.S2)
                aid = self.filtered[k]
                sel, hov = aid == self.asset, r.collidepoint(mouse)
                pygame.draw.rect(screen, T.SELECT if sel else (T.HOVER if hov else T.SURFACE),
                                 r, border_radius=T.R1)
                pygame.draw.rect(screen, T.ACCENT if sel else T.BORDER, r,
                                 2 if sel else 1, border_radius=T.R1)
                if aid < len(self.am.assets):
                    a = self.am.assets[aid]
                    tile = self.am.thumbnail(aid, T.CELL - 28)
                    if tile:
                        screen.blit(tile, (r.centerx - tile.get_width() // 2, r.y + 5))
                    self._t(screen, T.F_MICRO, a.name, T.TEXT if sel else T.MUTED,
                            r.centerx, r.bottom - 13, cx=True, max_w=r.width - 6)
                fav = aid in self.favs
                if fav or hov:
                    sx, sy = r.right - 11, r.y + 10
                    self._i_star(screen, sx, sy, T.WARN if fav else T.FAINT, fav, 6)
                    self._push(pygame.Rect(sx - 9, sy - 9, 18, 18), f"fav:{aid}")
                self._push(r, f"asset:{aid}")
                self._cells.append((pygame.Rect(r), aid))
        screen.set_clip(old)
        self._hit_clip = oldhit
        self._scrollbar(screen, region, total, off, scroll_key=scroll_key)
        return total

    # ── 4.4 overlay légende sur la carte ────────────────────────────
    def _map_overlay(self, screen, vr):
        if vr.width < 220:
            return
        w, h = 116, 18 + len(MAP_LEGEND) * 18
        r = pygame.Rect(vr.right - w - T.S4, T.S4, w, h)
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(s, (255, 255, 255, 232), (0, 0, w, h), border_radius=T.R2)
        screen.blit(s, r)
        pygame.draw.rect(screen, T.BORDER, r, 1, border_radius=T.R2)
        for i, (lbl, col) in enumerate(MAP_LEGEND):
            cy = r.y + 17 + i * 18
            pygame.draw.circle(screen, col, (r.x + 15, cy), 5)
            self._t(screen, T.F_SMALL, lbl, T.TEXT, r.x + 27, cy, cy=True,
                    max_w=w - 36)

    # ── 4.5 en-tête / outils / onglets ──────────────────────────────
    def _header(self, screen, sim):
        x0, c = self.x0, sim.clock
        self._t(screen, T.F_TITLE, "UNIVERS VIVANT", T.TEXT, x0 + T.S4, T.S3, bold=True)
        tw = self._tw(T.F_TITLE, "UNIVERS VIVANT", True)
        self._t(screen, T.F_MICRO, c.label(), T.MUTED, x0 + T.S4 + tw + T.S3, T.S3 + 5,
                max_w=self.panel_r - tw - 3 * T.S4)
        self._t(screen, T.F_MICRO,
                f"pop {len([a for a in sim.agents if a.alive])} · tick {sim.w.tick}", T.FAINT,
                x0 + self.panel_r - T.S4, T.S3 + 22, right=True)
        create_rect = pygame.Rect(x0 + self.panel_r - 158, 31, 146, 25)
        self._btn(screen, create_rect, "+ Nouvel habitant", "spawn_agent", radius=T.R1)

    def _toolbar(self, screen):
        x0, y = self.x0, 62
        modes = TAB_MODES.get(self.tab, MODES)
        if not modes:
            return
        avail = self.panel_r - 2 * T.S3
        min_btn_w = 72
        per_row = max(1, avail // min_btn_w)
        rows = [modes[i:i + per_row] for i in range(0, len(modes), per_row)]
        cy = y
        for row in rows:
            w = avail // len(row)
            for i, (mid, lbl) in enumerate(row):
                r = pygame.Rect(x0 + T.S3 + i * w, cy, w - T.S1, T.H_BTN)
                self._btn(screen, r, lbl, f"mode:{mid}",
                          primary=(self.mode == mid))
            cy += T.H_BTN + T.S1
        hint = TAB_HINTS.get(self.mode, "")
        if hint:
            self._t(screen, T.F_MICRO, hint, T.FAINT, x0 + T.S4, cy + 1,
                    max_w=self.panel_r - 2 * T.S4)

    def _tabs(self, screen):
        x0, y = self.x0, 110
        w = (self.panel_r - 2 * T.S3) // len(TABS)
        pygame.draw.line(screen, T.BORDER, (x0 + T.S3, y + T.H_TAB),
                         (x0 + self.panel_r - T.S3, y + T.H_TAB))
        for i, (tid, lbl) in enumerate(TABS):
            r = pygame.Rect(x0 + T.S3 + i * w, y, w, T.H_TAB)
            sel = self.tab == tid
            hov = r.collidepoint(pygame.mouse.get_pos())
            if sel:
                pygame.draw.rect(screen, _tint(T.ACCENT, .10), r, border_radius=T.R1)
            elif hov:
                pygame.draw.rect(screen, T.HOVER, r, border_radius=T.R1)
            self._t(screen, T.F_SMALL, lbl,
                    T.ACCENT if sel else (T.TEXT if hov else T.MUTED),
                    r.centerx, r.centery, cx=True, cy=True, bold=sel, max_w=r.width - 6)
            if sel:
                pygame.draw.rect(screen, T.ACCENT, (r.x + 6, r.bottom - 2, r.width - 12, 2))
            self._push(r, f"tab:{tid}")

    # ══════════════════════════════════════════════════════════════════
    #  5. ONGLET ÊTRE — deux colonnes
    # ══════════════════════════════════════════════════════════════════
    def _tab_etre(self, screen, sim, y):
        x0, ag = self.x0, sim.selected
        bottom = self.content_bottom()

        band = self._identity(screen, sim, pygame.Rect(
            x0 + T.S3, y, self.panel_r - 2 * T.S3, 0))
        y = band + T.S2

        two = self.panel_r >= 400
        gap = T.S2
        lw = int((self.panel_r - 2 * T.S3 - gap) * 0.54) if two else self.panel_r - 2 * T.S3
        left = pygame.Rect(x0 + T.S3, y, lw, bottom - y)
        right = pygame.Rect(left.right + gap, y,
                            self.panel_r - 2 * T.S3 - lw - gap, bottom - y)

        # — colonne 1 : générateur (si aucun être sélectionné) + accordéons —
        off = self._scroll["etre"]
        old = screen.get_clip()
        screen.set_clip(left)
        self._hit_clip = left
        cy = left.y - off
        if ag is None:
            self._card(screen, pygame.Rect(left.x, cy, left.width, 100), T.R2, T.SURFACE, T.BORDER)
            self._t(screen, T.F_SUB, "AUCUN ÊTRE SÉLECTIONNÉ", T.ACCENT,
                    left.centerx, cy + 22, cx=True)
            self._t(screen, T.F_SMALL,
                    "Utilise Examiner sur la carte ou choisis une ligne dans le Registre.",
                    T.MUTED, left.centerx, cy + 46, cx=True, max_w=left.width - 28)
            cr = pygame.Rect(left.x + 18, cy + 68, left.width - 36, 30)
            self._btn(screen, cr, "+ Nouvel habitant", "spawn_agent", radius=T.R2)
            cy += 108
        for key, label, color, names, _a, _t in SECTION_REGISTRY:
            cy = self._accordion(screen, ag, left, cy, key, label, color, names)
        total = (cy + off) - left.y
        screen.set_clip(old)
        self._hit_clip = None
        self._content_h["etre"] = total
        self._scrollbar(screen, left, total, off, scroll_key="etre")

        # — colonne 2 : cartes du registre —
        if not two:
            return
        off2 = self._scroll["_right"]
        screen.set_clip(right)
        self._hit_clip = right
        cy = right.y - off2
        for key, meth in CARD_REGISTRY:
            cy = getattr(self, meth)(screen, pygame.Rect(right.x, cy, right.width, 0), sim)
            cy += T.S2
        total2 = (cy + off2) - right.y
        screen.set_clip(old)
        self._hit_clip = None
        self._content_h["_right"] = total2
        self._scrollbar(screen, right, total2, off2, scroll_key="_right")

    def _identity(self, screen, sim, rect):
        """Bandeau identité — hauteur variable, rien ne peut en déborder."""
        ag = sim.selected
        if ag is None:
            r = pygame.Rect(rect.x, rect.y, rect.width, 46)
            self._card(screen, r, T.R2, _tint(T.ACCENT, .06), _tint(T.ACCENT, .30))
            self._t(screen, T.F_BODY, "Aucun être sélectionné", T.ACCENT,
                    r.x + T.S3, r.centery - 8, bold=True, max_w=r.width - 2 * T.S3)
            self._t(screen, T.F_MICRO,
                    "Outil « Examiner » ou onglet HABITANTS pour en choisir un.",
                    T.MUTED, r.x + T.S3, r.centery + 4, max_w=r.width - 2 * T.S3)
            return r.bottom

        fam = []
        bonded_eid = getattr(ag, "bonded", None)
        if bonded_eid is not None:
            # bonded est un eid (int), jamais un objet Being — on le resout
            partner = next((x for x in sim.agents if x.eid == bonded_eid), None)
            if partner is not None:
                fam.append(f"en couple avec {partner.name}")
        if getattr(ag, "children", None):
            fam.append(f"{len(ag.children)} enfant(s)")
        h = 88 + (14 if fam else 0)
        r = self._card(screen, pygame.Rect(rect.x, rect.y, rect.width, h), T.R2)
        clan = CLAN_COLORS.get(ag.color, (150, 150, 150))

        # — portrait (64x64) si disponible —
        av = pygame.Rect(r.x + T.S3, r.y + T.S3, 56, 56)
        portrait = self._get_portrait(ag.sex, getattr(ag, "cls", "pawn"))
        if portrait:
            # arrondir le coin
            mask = pygame.Surface((56, 56), pygame.SRCALPHA)
            pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, 56, 56), border_radius=20)
            frame = portrait.copy()
            frame.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            screen.blit(frame, av)
            pygame.draw.rect(screen, clan, av, 2, border_radius=20)
        else:
            # fallback : cercle coloré + initiales
            pygame.draw.rect(screen, _tint(clan, .30), av, border_radius=28)
            pygame.draw.rect(screen, clan, av, 2, border_radius=28)
            self._t(screen, T.F_BODY, ag.name[:2].upper(), _mix(clan, (0, 0, 0), .4),
                    av.centerx, av.centery, cx=True, cy=True, bold=True)

        # badge neurones, ancré à droite — largeur mesurée, jamais coupé
        btxt = f"{ag.brain.n} NEURONES"
        bw = self._tw(T.F_SMALL, btxt, True) + 40
        bdg = pygame.Rect(r.right - T.S3 - bw, r.y + T.S3, bw, 28)
        pygame.draw.rect(screen, T.DARK, bdg, border_radius=T.R2)
        self._i_lock(screen, bdg.x + 16, bdg.centery, T.ON_DARK)
        self._t(screen, T.F_SMALL, btxt, T.ON_DARK, bdg.x + 28, bdg.centery,
                cy=True, bold=True)

        tx, tw_max = av.right + T.S3, bdg.x - av.right - 2 * T.S3
        self._t(screen, T.F_SUB, f"{ag.name} ({ag.sex})", T.TEXT, tx, r.y + T.S3,
                bold=True, max_w=tw_max)
        self._t(screen, T.F_MICRO, f"{ag.stage} · {ag.age_years:.1f} ans · gén {ag.gen} · clan {ag.color}",
                T.MUTED, tx, r.y + T.S3 + 19, max_w=tw_max)
        self._t(screen, T.F_MICRO, f"but : {_goal_txt(ag)}", T.MUTED,
                tx, r.y + T.S3 + 33, max_w=tw_max)
        if fam:
            self._t(screen, T.F_MICRO, " · ".join(fam), T.FAINT, r.x + T.S3,
                    r.y + 60, max_w=r.width - 2 * T.S3)

        vy = r.bottom - 16
        vw = (r.width - 2 * T.S3 - 2 * T.S2) // 3
        for i, (lbl, val, col) in enumerate([
                ("santé", getattr(ag, "health", 0), C_CORPS),
                ("énergie", getattr(ag, "energy", 0), T.WARN),
                ("satiété", 1 - getattr(ag, "hunger", 0), C_EMO)]):
            vx = r.x + T.S3 + i * (vw + T.S2)
            self._t(screen, 10, lbl, T.FAINT, vx, vy - 12)
            self._bar(screen, (vx, vy, vw, 6), val, col)
        return r.bottom

    def _accordion(self, screen, ag, region, y, key, label, color, names):
        arr = self._array(ag, key)
        open_ = self.sections.get(key, False)
        hr = pygame.Rect(region.x, y, region.width, T.H_HEAD)
        hov = hr.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, _tint(color, .15) if open_ else (T.HOVER if hov else T.SURFACE),
                         hr, border_radius=T.R1)
        pygame.draw.rect(screen, _tint(color, .45) if open_ else T.BORDER, hr, 1,
                         border_radius=T.R1)
        self._chevron(screen, hr.x + 14, hr.centery,
                      _mix(color, (0, 0, 0), .2) if open_ else T.MUTED, open_)
        self._t(screen, T.F_BODY, label, _mix(color, (0, 0, 0), .35) if open_ else T.TEXT,
                hr.x + 26, hr.centery, cy=True, bold=True, max_w=hr.width - 80)
        if not open_ and arr is not None:
            self._t(screen, T.F_MICRO, f"{len(names)}", T.FAINT,
                    hr.right - T.S3, hr.centery, cy=True, right=True)
        self._push(hr, f"sec:{key}")
        y = hr.bottom + 2

        if open_ and arr is not None:
            lab_w = min(108, int(region.width * 0.40))
            val_w = 38
            mouse = pygame.mouse.get_pos()
            for pi, pname in enumerate(names):
                if pi >= len(arr):
                    break
                row = pygame.Rect(region.x + T.S2, y, region.width - 2 * T.S2, T.H_ROW)
                fid = f"ps:{key}:{pi}"
                active = row.collidepoint(mouse) or self.drag == fid
                self._t(screen, T.F_SMALL, pname,
                        T.TEXT if active else T.MUTED, row.x, row.centery,
                        cy=True, max_w=lab_w - 6)
                bx = row.x + lab_w
                bw = max(24, row.width - lab_w - val_w)
                v = float(arr[pi])
                self._bar(screen, (bx, row.centery - 4, bw, 7), v, color)
                # poignée seulement sur la ligne survolée ou en cours de glissement
                if active:
                    hx = bx + int(bw * max(0.0, min(1.0, v)))
                    hx = max(bx + 3, min(bx + bw - 3, hx))
                    pygame.draw.circle(screen, T.SURFACE, (hx, row.centery), 6)
                    pygame.draw.circle(screen, color, (hx, row.centery), 6, 2)
                self._t(screen, T.F_SMALL, f"{v:.2f}",
                        T.TEXT if active else T.MUTED, row.right, row.centery,
                        cy=True, right=True, bold=active)
                self._slider_geo[fid] = (bx, bw)
                self._push(row, fid)
                y += T.H_ROW
            y += T.S1
        return y + T.S1

    # ── 5.1 cartes de la colonne droite (CARD_REGISTRY) ─────────────
    def _card_head(self, screen, rect, title, color, fid, count=None):
        hr = pygame.Rect(rect.x, rect.y, rect.width, T.H_HEAD)
        open_ = self.cards_open.get(fid, True)
        pygame.draw.rect(screen, _tint(color, .14), hr, border_radius=T.R1)
        pygame.draw.rect(screen, _tint(color, .40), hr, 1, border_radius=T.R1)
        self._chevron(screen, hr.x + 14, hr.centery, _mix(color, (0, 0, 0), .2), open_)
        self._t(screen, T.F_BODY, title, _mix(color, (0, 0, 0), .35), hr.x + 26,
                hr.centery, cy=True, bold=True, max_w=hr.width - 60)
        if count is not None:
            self._t(screen, T.F_MICRO, f"({count})", T.MUTED, hr.right - T.S3,
                    hr.centery, cy=True, right=True)
        self._push(hr, f"card:{fid}")
        return hr.bottom, open_

    def _card_intention(self, screen, rect, sim):
        """Ce que l'être va faire, et pourquoi — lecture directe de
        brain.explain(). Purement une fenêtre d'observation : n'affecte
        jamais la simulation."""
        y, open_ = self._card_head(screen, rect, "INTENTION", T.ACCENT, "intention")
        if not open_:
            return y
        ag = sim.selected
        if ag is None or not getattr(ag, "alive", True):
            self._t(screen, T.F_SMALL, "Sélectionne un être pour voir ses intentions.",
                    T.FAINT, rect.centerx, y + 14, cx=True, max_w=rect.width - 2 * T.S3)
            return y + 30

        explain = getattr(ag.brain, "explain", None)
        ranking = explain(top=5) if callable(explain) else []
        if not ranking:
            self._t(screen, T.F_SMALL, "Cerveau sans explain() disponible.",
                    T.FAINT, rect.centerx, y + 14, cx=True, max_w=rect.width - 2 * T.S3)
            return y + 30

        rh = 24
        yy = y + T.S2
        engaged_act = ag.goal.get("act") if getattr(ag, "goal", None) else None
        for i, rk in enumerate(ranking):
            row = pygame.Rect(rect.x + T.S2, yy, rect.width - 2 * T.S2, rh - 4)
            col = rk.get("couleur", ACTION_COLORS.get(rk["action"], (150, 150, 150)))
            chosen = engaged_act == rk["action"]
            self._bar(screen, (row.x + 60, row.centery - 4, row.width - 60 - 48, 8),
                      rk["probabilite"], col)
            self._t(screen, T.F_SMALL, rk["nom"], T.TEXT if i == 0 else T.MUTED,
                    row.x, row.centery, cy=True, bold=(i == 0), max_w=56)
            self._t(screen, T.F_MICRO, f"{rk['probabilite']:.0%}", T.MUTED,
                    row.right, row.centery, cy=True, right=True, max_w=44)
            if chosen:
                pygame.draw.circle(screen, T.OK, (row.right - 46, row.centery), 3)
            yy += rh
        yy += T.S1
        self._t(screen, T.F_MICRO, f"engagé : {_goal_txt(ag)}", T.FAINT,
                rect.x + T.S3, yy, max_w=rect.width - 2 * T.S3)
        yy += 16
        pygame.draw.rect(screen, T.BORDER, (rect.x, y + 2, rect.width, yy - y - 2), 1,
                         border_radius=T.R1)
        return yy

    def _card_memoire(self, screen, rect, sim):
        """Vécu subjectif de l'être : autobiographie (a.life) et lieux
        qu'il croit dangereux (belief_places) — pas des stats globales,
        mais ce que CET être, en particulier, a retenu de sa vie."""
        y, open_ = self._card_head(screen, rect, "MÉMOIRE", C_MEM, "memoire")
        if not open_:
            return y
        ag = sim.selected
        if ag is None or not getattr(ag, "alive", True):
            self._t(screen, T.F_SMALL, "Sélectionne un être pour voir son vécu.",
                    T.FAINT, rect.centerx, y + 14, cx=True, max_w=rect.width - 2 * T.S3)
            return y + 30

        yy = y + T.S2
        n_danger = len(getattr(ag, "belief_places", {}) or {})
        n_beings = len(getattr(ag, "belief_beings", {}) or {})
        self._t(screen, T.F_SMALL,
                f"{n_danger} lieu(x) craint(s) · {n_beings} être(s) jugé(s)",
                T.MUTED, rect.x + T.S3, yy, max_w=rect.width - 2 * T.S3)
        yy += 20

        life = list(getattr(ag, "life", []) or [])[-5:]
        if not life:
            self._t(screen, T.F_SMALL, "Aucun événement marquant encore.",
                    T.FAINT, rect.x + T.S3, yy, max_w=rect.width - 2 * T.S3)
            yy += 18
        else:
            for entry in reversed(life):
                if isinstance(entry, tuple) and len(entry) >= 2:
                    txt = f"{entry[0]} : {entry[1]}"
                else:
                    txt = str(entry)
                pygame.draw.circle(screen, C_MEM, (rect.x + T.S4, yy + 7), 3)
                self._t(screen, T.F_MICRO, txt, T.TEXT, rect.x + 26, yy,
                        max_w=rect.width - 34)
                yy += 17
        yy += T.S1
        pygame.draw.rect(screen, T.BORDER, (rect.x, y + 2, rect.width, yy - y - 2), 1,
                         border_radius=T.R1)
        return yy

    def _card_gabarit(self, screen, rect, sim):
        """Générateur complet d'habitant — tous les paramètres modifiables."""
        y, open_ = self._card_head(screen, rect, "GENERATEUR D'HABITANT",
                                   T.ACCENT, "gabarit")
        if not open_:
            return y

        # ── prévisualisation skin idle réel ──
        ids = self.am.skin_states(self.tpl_color, self.tpl_cls).get("idle", [])
        if ids:
            try:
                skin = self.am.surface(ids[0], 0, 1.5)
                if skin:
                    pv = pygame.Rect(rect.x + T.S2, y + 2, rect.width - 2 * T.S2,
                                     max(skin.get_height() + 16, 40))
                    self._card(screen, pv, T.R1, T.SURFACE_2, T.BORDER)
                    sx = pv.centerx - skin.get_width() // 2
                    sy = pv.bottom - skin.get_height() - 3
                    screen.blit(skin, (sx, sy))
                    clan = CLAN_COLORS.get(self.tpl_color, (150, 150, 150))
                    self._t(screen, T.F_MICRO,
                            f"{self.tpl_cls} · {self.tpl_sex} · {self.tpl_color} · {self.brain_size}N",
                            T.TEXT, pv.x + T.S3, pv.y + T.S2, maxw=pv.width - 2 * T.S3)
                    pygame.draw.rect(screen, clan, pv, 1, border_radius=T.R1)
                    y = pv.bottom + T.S2
            except Exception as exc:
                self.report_ui_error("preview_skin_gabarit", exc)

        body = pygame.Rect(rect.x, y + 2, rect.width, 0)
        yy = body.y + T.S2

        # ── 1. Clan ──
        self._t(screen, 10, "CLAN", T.FAINT, body.x + T.S2, yy)
        yy += 13
        for i, cc in enumerate(CLAN_COLORS):
            r = pygame.Rect(body.x + T.S2 + i * 27, yy, 22, 18)
            if r.right > body.right - T.S2:
                break
            pygame.draw.rect(screen, CLAN_COLORS[cc], r, border_radius=T.R1)
            if self.tpl_color == cc:
                pygame.draw.rect(screen, T.TEXT, r.inflate(4, 4), 2, border_radius=T.R1 + 2)
            self._push(r, f"tcolor:{cc}")
        yy += 24

        # ── 2. Sexe ──
        self._t(screen, 10, "SEXE", T.FAINT, body.x + T.S2, yy)
        yy += 13
        for i, s in enumerate(["M", "F"]):
            self._chip(screen, (body.x + T.S2 + i * 30, yy, 27, 19), s,
                       f"tsex:{s}", self.tpl_sex == s, size=T.F_SMALL)
        yy += 25

        # ── 3. Classe ──
        self._t(screen, 10, "CLASSE", T.FAINT, body.x + T.S2, yy)
        yy += 13
        fx = body.x + T.S2
        for cls in self.template_classes():
            cw = self._tw(T.F_MICRO, cls) + 16
            if fx + cw > body.right - T.S2:
                fx, yy = body.x + T.S2, yy + 23
            self._chip(screen, (fx, yy, cw, 19), cls, f"tcls:{cls}", self.tpl_cls == cls)
            fx += cw + T.S1
        yy += 25

        # ── 4. Cerveau (slider 25–1000) ──
        br = pygame.Rect(body.x + T.S2, yy, body.width - 2 * T.S2, 32)
        self._card(screen, br, T.R1, T.SURFACE_2, T.BORDER)
        self._btn(screen, (br.x + 2, br.y + 2, 24, 24), "−", "bsize-", radius=T.R1 - 2)
        self._btn(screen, (br.right - 26, br.y + 2, 24, 24), "+", "bsize+", radius=T.R1 - 2)
        self._t(screen, T.F_SMALL, f"{self.brain_size} N · ×{think_every(self.brain_size)}",
                T.TEXT, br.centerx, br.centery, cx=True, cy=True, bold=True,
                max_w=br.width - 56)
        yy += 38
        # slider continu 25–1000 (élargi x4)
        sbr = pygame.Rect(body.x + T.S2, yy, body.width - 2 * T.S2, 28)
        sl_x, sl_w = sbr.x, sbr.width
        pygame.draw.rect(screen, T.TRACK, sbr, border_radius=14)
        t = (self.brain_size - 25) / max(1, 1000 - 25)
        hx = sl_x + int(sl_w * max(0.0, min(1.0, t)))
        pygame.draw.rect(screen, T.ACCENT, (sl_x, sbr.y, max(14, hx - sl_x), 28), border_radius=14)
        pygame.draw.circle(screen, T.SURFACE, (hx, sbr.centery), 14)
        pygame.draw.circle(screen, T.ACCENT, (hx, sbr.centery), 14, 2)
        self._slider_geo["bsize_slider"] = (sl_x, sl_w)
        self._push(sbr, "bsize_slider")
        yy += 32
        if self.brain_size >= 512:
            self._t(screen, T.F_MICRO, "⚠ mémoire élevée — risque de ralenti",
                    (228, 158, 58), body.x + T.S2, yy, max_w=body.width - 2 * T.S2)
            yy += 14
        mem = self.brain_memory_estimate_mb()
        self._t(screen, T.F_MICRO,
                f"≈ {mem:.2f} Mo de poids · réflexion toutes les {think_every(self.brain_size)} ticks",
                T.WARN if self.brain_size >= 512 else T.FAINT,
                body.x + T.S2, yy, max_w=body.width - 2 * T.S2)
        yy += 16

        # ── sections paramétrables ──
        GEN_SECTIONS = [
            ("body",   "CORPS",         C_CORPS,  BODY_DEFS,        "tpl_body"),
            ("cog",    "COGNITION",     C_COG,    COG_DEFS,         "tpl_cog"),
            ("perso",  "PERSONNALITÉ",  C_PERSO,  PERSONALITY_DEFS, "tpl_personality"),
            ("emo",    "ÉMOTIONS",      C_EMO,    EMOTION_DEFS,     "tpl_emotions"),
            ("needs",  "BESOINS",       C_BESOIN, NEED_DEFS,        "tpl_needs"),
            ("skills", "EXPÉRIENCE",    C_EXP,    SKILL_DEFS,       "tpl_skills"),
        ]
        for key, label, color, names, tpl_attr in GEN_SECTIONS:
            sec_key = f"gen_{key}"
            open_sec = self.cards_open.get(sec_key, False)
            hr = pygame.Rect(body.x, yy, body.width, T.H_HEAD)
            hov = hr.collidepoint(pygame.mouse.get_pos())
            pygame.draw.rect(screen, _tint(color, .15) if open_sec else (T.HOVER if hov else T.SURFACE),
                             hr, border_radius=T.R1)
            pygame.draw.rect(screen, _tint(color, .45) if open_sec else T.BORDER, hr, 1,
                             border_radius=T.R1)
            self._chevron(screen, hr.x + 14, hr.centery,
                          _mix(color, (0, 0, 0), .2) if open_sec else T.MUTED, open_sec)
            self._t(screen, T.F_BODY, label,
                    _mix(color, (0, 0, 0), .35) if open_sec else T.TEXT,
                    hr.x + 26, hr.centery, cy=True, bold=True, max_w=hr.width - 60)
            if not open_sec:
                arr = getattr(self, tpl_attr, None)
                if arr is not None:
                    self._t(screen, T.F_MICRO, f"{len(names)} champs", T.FAINT,
                            hr.right - T.S3, hr.centery, cy=True, right=True)
            self._push(hr, f"card:{sec_key}")
            yy = hr.bottom + 2

            if open_sec:
                arr = getattr(self, tpl_attr, None)
                if arr is not None:
                    lab_w = min(108, int(body.width * 0.40))
                    val_w = 38
                    mouse = pygame.mouse.get_pos()
                    for pi, pname in enumerate(names):
                        if pi >= len(arr):
                            break
                        row = pygame.Rect(body.x + T.S2, yy, body.width - 2 * T.S2, T.H_ROW)
                        fid = f"ps:{key}:{pi}"
                        active = row.collidepoint(mouse) or self.drag == fid
                        self._t(screen, T.F_SMALL, pname,
                                T.TEXT if active else T.MUTED, row.x, row.centery,
                                cy=True, max_w=lab_w - 6)
                        bx = row.x + lab_w
                        bw = max(24, row.width - lab_w - val_w)
                        v = float(arr[pi])
                        self._bar(screen, (bx, row.centery - 6, bw, 14), v, color)
                        if active:
                            hx = bx + int(bw * max(0.0, min(1.0, v)))
                            hx = max(bx + 6, min(bx + bw - 6, hx))
                            pygame.draw.circle(screen, T.SURFACE, (hx, row.centery), 10)
                            pygame.draw.circle(screen, color, (hx, row.centery), 10, 2)
                        self._t(screen, T.F_SMALL, f"{v:.2f}",
                                T.TEXT if active else T.MUTED, row.right, row.centery,
                                cy=True, right=True, bold=active)
                        self._slider_geo[fid] = (bx, bw)
                        self._push(row, fid)
                        yy += T.H_ROW
                    yy += T.S1
            yy += T.S1

        # ── bouton Créer ──
        btn = pygame.Rect(body.x + T.S2, yy, body.width - 2 * T.S2, 36)
        self._btn(screen, btn, "Créer un habitant", "spawn_modal", radius=T.R2)
        yy = btn.bottom + T.S2

        # ── bouton Cimetière ──
        cemetery_count = len(self._sim_ref.w.cemetery) if self._sim_ref else 0
        if cemetery_count > 0:
            cbtn = pygame.Rect(body.x + T.S2, yy, body.width - 2 * T.S2, 28)
            self._btn(screen, cbtn,
                      f"Aller au cimetière ({cemetery_count})",
                      "goto_cemetery", radius=T.R2)
            yy = cbtn.bottom + T.S2

        pygame.draw.rect(screen, T.BORDER,
                         (rect.x, y + 2, rect.width, yy - y - 2), 1,
                         border_radius=T.R1)
        return yy

    def _draw_spawn_modal(self, screen, sim):
        if not self.spawn_modal:
            self.modal_view = None
            self.modal_track = None
            self.modal_handle = None
            return

        sw, sh = screen.get_size()
        overlay = pygame.Surface((sw, sh), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        pw = min(760, max(560, int(sw * 0.46)))
        ph = min(sh - 34, 820)
        panel = pygame.Rect((sw - pw) // 2, (sh - ph) // 2, pw, ph)
        pygame.draw.rect(screen, T.SURFACE, panel, border_radius=14)
        pygame.draw.rect(screen, T.BORDER_2, panel, 2, border_radius=14)

        # ── Entête fixe ──
        header_h = 48
        header = pygame.Rect(panel.x, panel.y, panel.width, header_h)
        pygame.draw.rect(screen, T.SURFACE_2, header,
                         border_top_left_radius=14, border_top_right_radius=14)
        pygame.draw.line(screen, T.BORDER, (header.x + 12, header.bottom - 1),
                         (header.right - 12, header.bottom - 1), 1)

        self._t(screen, T.F_TITLE, "CREER UN HABITANT", T.ACCENT,
                header.centerx, header.centery, cx=True, cy=True)

        xbtn = pygame.Rect(header.right - 34, header.y + 9, 25, 25)
        hov_x = xbtn.collidepoint(pygame.mouse.get_pos())
        self._t(screen, T.F_BODY, chr(0x00d7),
                (214, 84, 84) if hov_x else T.MUTED,
                xbtn.centerx, xbtn.centery, cx=True, cy=True)
        self._push(xbtn, "spawn_modal")

        # ── Actions fixes (bas) ──
        footer_h = 54
        footer = pygame.Rect(panel.x, panel.bottom - footer_h, panel.width, footer_h)
        pygame.draw.rect(screen, T.SURFACE_2, footer,
                         border_bottom_left_radius=14, border_bottom_right_radius=14)
        pygame.draw.line(screen, T.BORDER, (footer.x + 12, footer.y),
                         (footer.right - 12, footer.y), 1)

        cancel = pygame.Rect(footer.x + 14, footer.y + 11, 130, 31)
        confirm = pygame.Rect(footer.right - 214, footer.y + 11, 200, 31)
        self._btn(screen, cancel, "Annuler", "spawn_modal", radius=T.R2)
        self._btn(screen, confirm, "Creer et placer", "spawn_confirm",
                  primary=True, radius=T.R2)

        # ── Zone scrollable ──
        view = pygame.Rect(panel.x + 18, header.bottom + 8,
                           panel.width - 18 - 28 - 18,
                           footer.y - header.bottom - 16)
        self.modal_view = view

        info = self.modal_scroll
        modal_offset = info.offset

        old_clip = screen.get_clip()
        old_hitclip = self._hit_clip
        screen.set_clip(view)
        self._hit_clip = view

        try:
            yy = view.y + 8 - modal_offset
            body = pygame.Rect(view.x, yy, view.width, 0)

            # ── PREVIEW SKIN ──
            ids = self.am.skin_states(self.tpl_color, self.tpl_cls).get("idle", [])
            preview_h = 106
            preview = pygame.Rect(view.x, yy, view.width, preview_h)
            self._card(screen, preview, T.R2, T.SURFACE_2, T.BORDER)
            if ids:
                try:
                    frames = max(1, self.am.assets[ids[0]].frames)
                    frame = (pygame.time.get_ticks() // 180) % frames
                    skin = self.am.surface(ids[0], frame, 2.6)
                    screen.blit(skin, (preview.centerx - skin.get_width() // 2,
                                       preview.bottom - skin.get_height() - 7))
                except Exception as exc:
                    self.report_ui_error("preview_skin_modal", exc)

            self._t(screen, T.F_BODY,
                    f"{self.tpl_cls}  {self.tpl_sex}  clan {self.tpl_color}  {self.brain_size}N",
                    T.TEXT, preview.x + 10, preview.y + 9, max_w=preview.width - 20)
            clan_color = CLAN_COLORS.get(self.tpl_color, (150, 150, 150))
            pygame.draw.rect(screen, clan_color, preview, 2, border_radius=T.R2)
            yy = preview.bottom + 10

            # ── CLAN ──
            self._t(screen, T.F_BODY, "CLAN", T.MUTED, view.x, yy, bold=True)
            yy += 21
            for i, cc in enumerate(CLAN_COLORS):
                r = pygame.Rect(view.x + i * 40, yy, 33, 25)
                pygame.draw.rect(screen, CLAN_COLORS[cc], r, border_radius=T.R1)
                if self.tpl_color == cc:
                    pygame.draw.rect(screen, T.TEXT, r.inflate(5, 5), 2, border_radius=T.R1)
                self._push(r, f"tcolor:{cc}")
            yy += 40

            # ── SEXE ──
            self._t(screen, T.F_BODY, "SEXE", T.MUTED, view.x, yy, bold=True)
            yy += 21
            for i, s in enumerate(["M", "F"]):
                r = pygame.Rect(view.x + i * 50, yy, 43, 26)
                self._chip(screen, r, s, f"tsex:{s}", self.tpl_sex == s,
                           size=T.F_BODY)
            yy += 42

            # ── CLASSE ──
            self._t(screen, T.F_BODY, "CLASSE", T.MUTED, view.x, yy, bold=True)
            yy += 21
            cx2 = view.x
            for c in self.template_classes():
                cw = max(56, self._tw(T.F_BODY, c) + 22)
                if cx2 + cw > view.right:
                    cx2 = view.x
                    yy += 31
                r = pygame.Rect(cx2, yy, cw, 26)
                self._chip(screen, r, c, f"tcls:{c}", self.tpl_cls == c,
                           size=T.F_SMALL)
                cx2 += cw + 5
            yy += 42

            # ── CERVEAU ──
            self._t(screen, T.F_BODY, f"CERVEAU  {self.brain_size}N", T.MUTED,
                    view.x, yy, bold=True)
            yy += 23
            slider = pygame.Rect(view.x, yy, view.width, 28)
            pygame.draw.rect(screen, T.TRACK, slider, border_radius=14)
            ratio = max(0.0, min(1.0, (self.brain_size - 25) / (1000 - 25)))
            hx = slider.x + int(slider.width * ratio)
            pygame.draw.rect(screen, T.ACCENT,
                             pygame.Rect(slider.x, slider.y, max(14, hx - slider.x), slider.height),
                             border_radius=14)
            pygame.draw.circle(screen, T.SURFACE, (hx, slider.centery), 14)
            pygame.draw.circle(screen, T.ACCENT, (hx, slider.centery), 14, 2)
            self._slider_geo["bsize_slider_modal"] = (slider.x, slider.width)
            self._push(slider, "bsize_slider_modal")
            yy += 34
            mem = self.brain_memory_estimate_mb()
            self._t(screen, T.F_MICRO,
                    f"≈ {mem:.2f} Mo / habitant · réflexion toutes les {think_every(self.brain_size)} ticks",
                    T.WARN if self.brain_size >= 512 else T.FAINT,
                    view.x, yy, max_w=view.width)
            yy += 24

            # ── GROUPES DE PARAMÈTRES ──
            GEN_SECTIONS = [
                ("body",   "CORPS",        C_CORPS,  BODY_DEFS,        "tpl_body"),
                ("cog",    "COGNITION",    C_COG,    COG_DEFS,         "tpl_cog"),
                ("perso",  "PERSONNALITE", C_PERSO,  PERSONALITY_DEFS, "tpl_personality"),
                ("emo",    "EMOTIONS",     C_EMO,    EMOTION_DEFS,     "tpl_emotions"),
                ("needs",  "BESOINS",      C_BESOIN, NEED_DEFS,        "tpl_needs"),
                ("skills", "EXPERIENCE",   C_EXP,    SKILL_DEFS,       "tpl_skills"),
            ]
            mouse = pygame.mouse.get_pos()
            for key, label, color, names, tpl_attr in GEN_SECTIONS:
                arr = getattr(self, tpl_attr, None)
                if arr is None:
                    continue
                hr = pygame.Rect(view.x, yy, view.width, 27)
                open_sec = True
                pygame.draw.rect(screen, _tint(color, .14), hr, border_radius=T.R1)
                pygame.draw.rect(screen, _tint(color, .42), hr, 1, border_radius=T.R1)
                self._t(screen, T.F_BODY, label, _mix(color, (0, 0, 0), .55),
                        hr.x + 10, hr.centery, cy=True, bold=True, max_w=hr.width - 80)
                self._t(screen, T.F_MICRO, f"{len(names)} champs", T.FAINT,
                        hr.right - T.S3, hr.centery, cy=True, right=True)
                yy = hr.bottom + 3

                lab_w = min(116, int(view.width * 0.36))
                val_w = 40
                for pi, pname in enumerate(names):
                    if pi >= len(arr):
                        break
                    row = pygame.Rect(view.x, yy, view.width, 25)
                    fid = f"ps:{key}:{pi}"
                    active = row.collidepoint(mouse) or self.drag == fid
                    self._t(screen, T.F_SMALL, pname,
                            T.TEXT if active else T.MUTED, row.x + 4, row.centery,
                            cy=True, max_w=lab_w - 8)
                    bx = row.x + lab_w
                    bw = max(48, row.width - lab_w - val_w)
                    v = float(arr[pi])
                    self._bar(screen, (bx, row.centery - 5, bw, 10), v, color)
                    if active:
                        hx = bx + int(bw * max(0.0, min(1.0, v)))
                        hx = max(bx + 3, min(bx + bw - 3, hx))
                        pygame.draw.circle(screen, T.SURFACE, (hx, row.centery), 7)
                        pygame.draw.circle(screen, color, (hx, row.centery), 7, 2)
                    self._t(screen, T.F_SMALL, f"{v:.2f}",
                            T.TEXT if active else T.MUTED,
                            row.right - 3, row.centery, cy=True, right=True)
                    self._slider_geo[fid] = (bx, bw)
                    self._push(row, fid)
                    yy += 27
                yy += 9

            # Marge finale
            content_h = yy - (view.y - modal_offset) + 18

        finally:
            screen.set_clip(old_clip)
            self._hit_clip = old_hitclip

        # Update scroll geometry
        self.modal_content_h = max(view.height, int(content_h))
        info.offset = ScrollController.clamp(info.offset, self.modal_content_h, view.height)

        # Draw scrollbar if needed
        if self.modal_content_h > view.height:
            bar_w = 12
            track_x = view.right + 5
            self.modal_track = pygame.Rect(track_x, view.y, bar_w, view.height)
            self.modal_handle = ScrollController.handle_rect(
                self.modal_track, self.modal_content_h, info.offset)
            if self.modal_handle:
                pygame.draw.rect(screen, (232, 235, 241), self.modal_track, border_radius=6)
                pygame.draw.rect(screen, (207, 212, 221), self.modal_track, 1, border_radius=6)
                hovering = self.modal_handle.collidepoint(pygame.mouse.get_pos())
                color = (77, 104, 140) if hovering or info.drag_grab_y is not None else (125, 136, 152)
                pygame.draw.rect(screen, color, self.modal_handle, border_radius=6)
                # Register handle and track for interaction
                self._push(self.modal_handle, "modal_scrollthumb")
                self._push(self.modal_track, "modal_scrolltrack")
        else:
            self.modal_track = None
            self.modal_handle = None

    def _card_events(self, screen, rect, sim):
        """Événements récents groupés par catégorie — issus de LOG_CATS."""
        groups = {}
        for e in list(sim.journal)[-80:]:
            cat = e[3] if len(e) > 3 else "monde"
            groups.setdefault(cat, []).append(e)
        y = rect.y
        for cat, entries in sorted(groups.items(), key=lambda kv: -len(kv[1]))[:5]:
            col = LOG_CATS.get(cat, T.MUTED)
            key = f"ev_{cat}"
            self.cards_open.setdefault(key, True)
            y, open_ = self._card_head(screen,
                                       pygame.Rect(rect.x, y, rect.width, 0),
                                       LOG_TITLES.get(cat, cat.capitalize()),
                                       col, key, len(entries))
            if open_:
                for e in entries[-3:]:
                    txt = e[1] if len(e) > 1 else ""
                    cnt = e[4] if len(e) > 4 else 1
                    pygame.draw.circle(screen, col, (rect.x + T.S4, y + 11), 4)
                    self._t(screen, T.F_SMALL,
                            txt + (f"  ×{cnt}" if cnt and cnt > 1 else ""),
                            T.TEXT, rect.x + 28, y + 4, max_w=rect.width - 36)
                    y += 21
            y += T.S2
        if not groups:
            self._t(screen, T.F_SMALL, "Aucun événement.", T.FAINT,
                    rect.centerx, rect.y + 6, cx=True)
            y = rect.y + 26
        return y

    # ══════════════════════════════════════════════════════════════════
    #  6. AUTRES ONGLETS
    # ══════════════════════════════════════════════════════════════════
    def _draw_tile_inspector(self, screen, sim, rect):
        from .diagnostics import tile_snapshot
        if self.selected_tile is None:
            return rect.y
        tx, ty = self.selected_tile
        data = tile_snapshot(sim, tx, ty)
        y = rect.y
        x0 = rect.x
        w = rect.width

        self._card(screen, pygame.Rect(x0, y, w, 0), T.R2, T.SURFACE, T.BORDER)
        self._t(screen, T.F_SUB, f"TUILE {tx}, {ty}", T.TEXT, x0 + T.S3, y + T.S2, bold=True)
        y += 28

        rows = [
            ("Terrain", "eau" if data["eau"] else "terre" if data["terre"] else "hors sol"),
            ("Bloquée", "oui" if data["bloque"] else "non"),
            ("Abri", "oui" if data["abri"] else "non"),
            ("Feu", str(data["feu"])),
            ("Odeur", f"{data['odeur']:.2f}"),
            ("Exploration", f"{data['exploration']:.2f}"),
            ("Phéromones", f"{data['pheromone']:.2f}"),
        ]

        if "biome" in data:
            rows.extend([
                ("Biome", str(data["biome"])),
                ("Altitude", f"{data['altitude']:.2f}"),
                ("Pente", f"{data['pente']:.2f}"),
            ])

        obj = data.get("objet")
        if obj:
            rows.extend([
                ("Objet", obj["nom"]),
                ("Rôle", obj["role"]),
                ("PV", str(data["pv_objet"])),
                ("Affordances", ", ".join(obj["affordances"][:4]) or "—"),
            ])

        if data.get("tombe"):
            grave = data["tombe"]
            rows.extend([
                ("Tombe", grave["nom"]),
                ("Décès tick", str(grave["tick_deces"])),
            ])

        storage = data.get("stockage")
        if storage:
            rows.extend([
                ("Dépôt", storage.get("clan") or "commun"),
                ("Remplissage", f"{storage['remplissage']:.0%}"),
                ("Inventaire", str(storage["inventaire"])),
            ])

        site = data.get("chantier")
        if site:
            rows.extend([
                ("Chantier", site.get("nom", "?")),
                ("Progression", f"{site.get('progression', 0):.0%}"),
                ("Blocs", f"{site.get('blocs_poses', 0)} / {site.get('blocs_total', 0)}"),
                ("Contributeurs", str(len(site.get("contributeurs", [])))),
            ])

        for label, value in rows:
            self._t(screen, T.F_MICRO, label, T.MUTED, x0 + T.S3, y, max_w=w * 0.38)
            self._t(screen, T.F_MICRO, value, T.TEXT,
                    x0 + w - T.S3, y, right=True, max_w=w * 0.56)
            y += 20

        return y + T.S2

    def _draw_agent_diagnostics(self, screen, sim, rect):
        from .diagnostics import agent_snapshot
        agent = sim.selected
        data = agent_snapshot(sim, agent)
        if data is None:
            return rect.y
        y = rect.y
        x0 = rect.x
        w = rect.width

        self._card(screen, pygame.Rect(x0, y, w, 0), T.R2, T.SURFACE, T.BORDER)
        self._t(screen, T.F_SUB, data["nom"], T.TEXT, x0 + T.S3, y + T.S2, bold=True)
        self._t(screen,
                T.F_MICRO,
                f"{data['sexe']} · {data['classe']} · {data['age_ans']:.1f} ans · "
                f"gén. {data['generation']} · {data['cerveau']['neurones']} N",
                T.MUTED,
                x0 + T.S3, y + 23, max_w=w - 2 * T.S3)
        y += 45

        vital = (
            ("Santé", data["sante"], C_CORPS),
            ("Énergie", data["energie"], T.WARN),
            ("Satiété", 1.0 - data["faim"], C_EMO),
            ("Soif", 1.0 - data["soif"], T.ACCENT),
        )
        for label, value, color in vital:
            self._t(screen, T.F_MICRO, label, T.MUTED, x0 + T.S3, y)
            bar = pygame.Rect(x0 + 74, y - 2, w - 124, 9)
            self._bar(screen, bar, value, color)
            self._t(screen, T.F_MICRO, f"{value:.2f}", T.TEXT,
                    x0 + w - T.S3, y, right=True)
            y += 17
        y += 6

        goal = data["but"]
        self._t(screen, T.F_BODY, "INTENTION ACTUELLE", T.ACCENT, x0 + T.S3, y, bold=True)
        y += 19
        self._t(screen, T.F_SMALL, goal["action_nom"], T.TEXT, x0 + T.S3, y)
        target = "—"
        if goal["cible_x"] is not None:
            target = f"tuile {goal['cible_x']}, {goal['cible_y']}"
        self._t(screen, T.F_SMALL, target, T.MUTED, x0 + w - T.S3, y, right=True)
        y += 18
        if goal["distance_px"] is not None:
            self._t(screen, T.F_MICRO,
                    f"distance {goal['distance_px'] / TILE:.1f} tuiles · "
                    f"bloqué {goal['bloque_ticks']} ticks",
                    T.FAINT, x0 + T.S3, y, max_w=w - 2 * T.S3)
            y += 18

        self._t(screen, T.F_BODY, "INVENTAIRE", C_EXP, x0 + T.S3, y, bold=True)
        y += 19
        inv = data["inventaire"]
        self._t(screen, T.F_SMALL,
                f"bois {inv.get('bois', 0)} · pierre {inv.get('pierre', 0)} · "
                f"or {inv.get('or', 0)} · graines {inv.get('graine', 0)}",
                T.TEXT, x0 + T.S3, y, max_w=w - 2 * T.S3)
        y += 19

        tool = data["outil"]
        tool_label = "aucun"
        if tool:
            tool_label = f"{tool['nom']} · durabilité {data['durabilite_outil']}"
        self._t(screen, T.F_SMALL, f"Outil : {tool_label}", T.MUTED,
                x0 + T.S3, y, max_w=w - 2 * T.S3)
        y += 23

        self._t(screen, T.F_BODY, "CERVEAU", C_COG, x0 + T.S3, y, bold=True)
        y += 19
        for item in data["cerveau"]["classement_actions"]:
            self._t(screen, T.F_SMALL, item.get("nom", "?"), T.TEXT, x0 + T.S3, y)
            self._t(screen, T.F_SMALL, f"{item.get('probabilite', 0):.1%}", T.MUTED,
                    x0 + w - T.S3, y, right=True)
            y += 18

        self._t(screen, T.F_BODY, "RELATIONS", C_MEM, x0 + T.S3, y + 4, bold=True)
        y += 24
        for relation in data["relations"][:5]:
            self._t(screen, T.F_SMALL, relation["nom"], T.TEXT, x0 + T.S3, y)
            self._t(screen, T.F_MICRO,
                    f"confiance {relation['confiance']:+.2f} · "
                    f"affection {relation['affection']:+.2f}",
                    T.MUTED, x0 + w - T.S3, y, right=True, max_w=150)
            y += 18

        return y + T.S2

    def _tab_decor(self, screen, sim, y):
        x0 = self.x0
        r = pygame.Rect(x0 + T.S3, y, self.panel_r - 2 * T.S3, 0)
        cy = r.y

        if self.selected_tile is not None:
            cy = self._draw_tile_inspector(
                screen, sim,
                pygame.Rect(x0 + T.S3, cy, self.panel_r - 2 * T.S3, 0),
            )
            cy += T.S2

        # asset sélectionné — infos détaillées
        if self.asset >= 0 and self.asset < len(self.am.assets):
            a = self.am.assets[self.asset]
            # carte info
            ir = pygame.Rect(r.x, cy, r.width, 72)
            self._card(screen, ir, T.R1, T.SELECT, T.ACCENT)
            tile = self.am.thumbnail(self.asset, 48)
            if tile:
                screen.blit(tile, (ir.x + 8, ir.y + 12))
            tx = ir.x + 60
            self._t(screen, T.F_BODY, a.name, T.TEXT, tx, ir.y + 6, bold=True,
                    max_w=ir.width - 68)
            self._t(screen, T.F_MICRO, f"catégorie: {a.category}", T.MUTED,
                    tx, ir.y + 22, max_w=ir.width - 68)
            props = []
            if a.solid:
                props.append("solide")
            if a.flammable:
                props.append("flammable")
            props.append(f"taille: {a.size_tiles}×{a.size_tiles}")
            hp_val = a.harvest.get("hp", "?") if a.harvest else "?"
            props.append(f"pv: {hp_val}")
            self._t(screen, T.F_MICRO, " · ".join(props), T.MUTED,
                    tx, ir.y + 36, max_w=ir.width - 68)
            if a.build_recipe:
                mats = ", ".join(f"{m['materiau']}×{m['quantity']}" for m in a.build_recipe["materials"])
                self._t(screen, T.F_MICRO, f"recette: {mats}", T.MUTED,
                        tx, ir.y + 50, max_w=ir.width - 68)
            cy = ir.bottom + T.S2
        else:
            self._card(screen, pygame.Rect(r.x, cy, r.width, 40), T.R1, T.SURFACE, T.BORDER)
            self._t(screen, T.F_SMALL, "Cliquez sur un asset dans le catalogue pour le sélectionner",
                    T.FAINT, r.x + T.S4, cy + 14)
            cy += 44

        # favoris / récents
        items = (self.favs + [x for x in self.recents if x not in self.favs])[:8]
        if items:
            self._t(screen, T.F_SMALL, "ACCÈS RAPIDE", T.MUTED, r.x + T.S4, cy, bold=True)
            cy += 18
            cols = max(1, r.width // 52)
            for i, aid in enumerate(items):
                col, row = i % cols, i // cols
                tr = pygame.Rect(r.x + T.S4 + col * 52, cy + row * 52, 46, 46)
                sel = aid == self.asset
                self._card(screen, tr, T.R1,
                           T.SELECT if sel else (T.HOVER if tr.collidepoint(pygame.mouse.get_pos()) else T.SURFACE),
                           T.ACCENT if sel else T.BORDER)
                if aid < len(self.am.assets):
                    tile = self.am.thumbnail(aid, 34)
                    if tile:
                        screen.blit(tile, (tr.centerx - tile.get_width() // 2,
                                           tr.centery - tile.get_height() // 2))
                self._push(tr, f"asset:{aid}")
            cy += ((len(items) - 1) // cols + 1) * 52 + T.S2

        # taille pinceau (modes eau/terre/mur)
        if self.mode in ("water", "land", "wall"):
            self._t(screen, T.F_SMALL, "TAILLE PINCEAU", T.MUTED, r.x + T.S4, cy, bold=True)
            cy += 18
            bs = self.brush_size
            diam = bs * 2 + 1
            self._t(screen, T.F_MICRO, f"{diam}×{diam} tiles ({diam * config.TILE}px)",
                    T.TEXT, r.x + T.S4, cy)
            cy += 15
            sl = pygame.Rect(r.x + T.S4, cy, r.width - 2 * T.S4, 28)
            pygame.draw.rect(screen, T.TRACK, sl, border_radius=14)
            t = max(0.0, min(1.0, (bs - 1) / 14))
            hx = sl.x + int(sl.width * t)
            pygame.draw.rect(screen, T.ACCENT, (sl.x, sl.y, max(14, hx - sl.x), 28), border_radius=14)
            pygame.draw.circle(screen, T.SURFACE, (hx, sl.centery), 14)
            pygame.draw.circle(screen, T.ACCENT, (hx, sl.centery), 14, 2)
            self._slider_geo["brush_slider"] = (sl.x, sl.width)
            self._push(sl, "brush_slider")
            cy += 34
            # boutons +/-
            bw = 36
            self._btn(screen, (r.x + T.S4, cy, bw, 26), "−", "brush-",
                      radius=T.R1 - 2, size=T.F_SMALL)
            self._btn(screen, (r.right - T.S4 - bw, cy, bw, 26), "+", "brush+",
                      radius=T.R1 - 2, size=T.F_SMALL)
            cy += 26

        # selecteur materiau (mode bloc)
        if self.mode == "block":
            self._t(screen, T.F_SMALL, "MATERIAU", T.MUTED, r.x + T.S4, cy, bold=True)
            cy += 18
            for i, mat in enumerate(("bois", "pierre")):
                rr = pygame.Rect(r.x + T.S4 + i * 70, cy, 64, 24)
                sel = self.block_material == mat
                pygame.draw.rect(screen, T.SELECT if sel else T.SURFACE, rr, border_radius=T.R1)
                if sel:
                    pygame.draw.rect(screen, T.ACCENT, rr, 1, border_radius=T.R1)
                self._t(screen, T.F_SMALL, mat, T.TEXT if sel else T.MUTED,
                        rr.centerx, rr.centery, cx=True, cy=True)
                self._push(rr, f"blockmat:{mat}")
            cy += 30

        # stats carte
        self._t(screen, T.F_SMALL, "CARTE", T.MUTED, r.x + T.S4, cy, bold=True)
        cy += 18
        st = sim.stats
        stats = [
            f"population: {len([a for a in sim.agents if a.alive])}",
            f"moutons: {len(sim.sheep)}",
            f"naissances: {st.get('births', 0)}  morts: {st.get('deaths', 0)}",
            f"constructions: {st.get('builds', 0)}  combats: {st.get('attacks', 0)}",
        ]
        for s in stats:
            self._t(screen, T.F_MICRO, s, T.MUTED, r.x + T.S4, cy)
            cy += 15
        cy += T.S2

        OVERLAY_LABELS = (
            ("none", "Normal"),
            ("resources", "Ressources"),
            ("memory", "Mémoire"),
            ("goal", "But"),
            ("danger", "Danger"),
            ("exploration", "Exploration"),
            ("territory", "Territoire"),
            ("storage", "Dépôts"),
            ("sites", "Chantiers"),
            ("cemetery", "Cimetière"),
        )
        self._t(screen, T.F_SMALL, "COUCHE DE DIAGNOSTIC", T.MUTED, r.x + T.S4, cy, bold=True)
        cy += 19
        fx = r.x + T.S4
        for key, label in OVERLAY_LABELS:
            chip_w = self._tw(T.F_MICRO, label) + 16
            if fx + chip_w > r.right - T.S4:
                fx = r.x + T.S4
                cy += 24
            chip = pygame.Rect(fx, cy, chip_w, 20)
            sel = self.active_overlay == key
            pygame.draw.rect(screen, T.SELECT if sel else T.SURFACE, chip, border_radius=T.R1)
            if sel:
                pygame.draw.rect(screen, T.ACCENT, chip, 1, border_radius=T.R1)
            self._t(screen, T.F_MICRO, label,
                    T.ACCENT if sel else T.MUTED,
                    chip.centerx, chip.centery, cx=True, cy=True)
            self._push(chip, f"overlay:{key}")
            fx += chip_w + 4
        cy += 28

        self._content_h["decor"] = cy - r.y

    def _tab_habitants(self, screen, sim, y):
        x0 = self.x0
        people = self._habitants(sim)
        alive = len([a for a in sim.agents if getattr(a, "alive", True)])
        self._t(screen, T.F_SUB, "HABITANTS", T.TEXT, x0 + T.S4, y, bold=True)
        self._t(screen, T.F_SMALL, f"{len(people)} / {alive}", T.MUTED,
                x0 + self.panel_r - T.S4, y + 2, right=True)
        y += 24

        sr = pygame.Rect(x0 + T.S3, y, self.panel_r - 2 * T.S3, T.H_FIELD)
        self._card(screen, sr, T.R1, T.SURFACE, T.ACCENT if self.hab_focus else T.BORDER_2)
        self._i_search(screen, sr.x + 14, sr.centery, T.MUTED)
        self._t(screen, T.F_BODY, self.hab_search or "filtrer par nom, clan, classe…",
                T.TEXT if self.hab_search else T.FAINT, sr.x + 26, sr.centery,
                cy=True, max_w=sr.width - 50)
        if self.hab_search:
            cr = pygame.Rect(sr.right - 22, sr.centery - 8, 16, 16)
            self._t(screen, T.F_BODY, "×", T.MUTED, cr.centerx, cr.centery, cx=True, cy=True)
            self._push(cr, "hab_clear")
        self._push(sr, "hab_focus")
        y = sr.bottom + T.S2

        region = pygame.Rect(x0 + T.S3, y, self.panel_r - 2 * T.S3,
                             self.content_bottom() - y)
        self._card(screen, region, T.R2)
        off, rh = self._scroll["habitants"], 38
        old = screen.get_clip()
        screen.set_clip(region)
        self._hit_clip = region
        mouse = pygame.mouse.get_pos()
        first = max(0, off // rh)
        for i in range(first, min(len(people), first + region.height // rh + 2)):
            ag = people[i]
            rr = pygame.Rect(region.x + T.S1, region.y + T.S1 + i * rh - off,
                             region.width - 2 * T.S1, rh - 2)
            if sim.selected is ag:
                pygame.draw.rect(screen, T.SELECT, rr, border_radius=T.R1)
            elif rr.collidepoint(mouse):
                pygame.draw.rect(screen, T.HOVER, rr, border_radius=T.R1)
            # petit portrait 24x24 (cache)
            pm = self._get_cached_portrait(ag.sex, getattr(ag, "cls", "pawn"), 24)
            if pm:
                pmx, pmy = rr.x + 7, rr.centery - 12
                screen.blit(pm, (pmx, pmy))
                clan = CLAN_COLORS.get(ag.color, (150, 150, 150))
                pygame.draw.rect(screen, clan, (pmx, pmy, 24, 24), 1, border_radius=12)
            else:
                pygame.draw.circle(screen, CLAN_COLORS.get(ag.color, (150, 150, 150)),
                                   (rr.x + 14, rr.centery), 6)
            self._t(screen, T.F_BODY, f"{ag.name} ({ag.sex})", T.TEXT,
                    rr.x + 28, rr.y + 5, max_w=rr.width - 170)
            self._t(screen, T.F_MICRO,
                    f"{ag.stage} · {ag.age_years:.1f} ans · {getattr(ag,'cls','—')} · {ag.brain.n} N",
                    T.MUTED, rr.x + 28, rr.y + 21, max_w=rr.width - 170)
            gx = rr.right - 130
            for j, (v, c) in enumerate([(getattr(ag, "health", 0), C_CORPS),
                                         (getattr(ag, "energy", 0), T.WARN),
                                         (1 - getattr(ag, "hunger", 0), C_EMO)]):
                self._bar(screen, (gx + j * 34, rr.centery - 3, 30, 6), v, c)
            dr = pygame.Rect(rr.right - 52, rr.centery - 10, 36, 20)
            hov_d = dr.collidepoint(mouse)
            if self.hdel_pending == ag.eid:
                pygame.draw.rect(screen, (214, 84, 84), dr, border_radius=4)
                self._t(screen, T.F_MICRO, "Confirmer", T.ON_DARK,
                        dr.centerx, dr.centery, cx=True, cy=True, bold=True)
            else:
                bg = (235, 100, 100) if hov_d else (214, 84, 84)
                pygame.draw.rect(screen, bg, dr, border_radius=4)
                self._t(screen, T.F_MICRO, "Supprimer", T.ON_DARK,
                        dr.centerx, dr.centery, cx=True, cy=True, bold=True)
            self._push(rr, f"hsel:{ag.eid}")
            self._push(dr, f"hdel:{ag.eid}")
        if not people:
            self._t(screen, T.F_BODY, "Aucun habitant ne correspond.", T.FAINT,
                    region.centerx, region.y + 36, cx=True)
        screen.set_clip(old)
        self._hit_clip = None
        self._content_h["habitants"] = len(people) * rh + T.S2
        self._scrollbar(screen, region, self._content_h["habitants"], off, scroll_key="habitants")

    def _tab_societe(self, screen, sim, y):
        x0, st = self.x0, sim.stats
        # max_gen et bonded ne sont pas suivis dans sim.stats (compteurs
        # d'evenements uniquement) — calcules ici en direct pour ne plus
        # afficher un 0 fige quelle que soit la population.
        alive = [a for a in sim.agents if getattr(a, "alive", True)]
        max_gen = max((a.gen for a in alive), default=0)
        bonded_count = sum(1 for a in alive if getattr(a, "bonded", None)) // 2
        n_children = sum(1 for a in alive if getattr(a, "child", False))
        groups = [
            ("Démographie", C_CORPS, [("Population", len(alive)),
                                      ("Naissances", st.get("births", 0)),
                                      ("Décès", st.get("deaths", 0)),
                                      ("Génération max", max_gen),
                                      ("Couples", bonded_count),
                                      ("Enfants", n_children)]),
            ("Activité", C_PERSO, [("Constructions", st.get("builds", 0)),
                                   ("Villages", st.get("villages", 0)),
                                   ("Récoltes", st.get("harvests", 0)),
                                   ("Outils trouvés", st.get("tool_found", 0))]),
            ("Social", C_BESOIN, [("Dons", st.get("gives", 0)),
                                  ("Vols", st.get("takes", 0)),
                                  ("Paroles", st.get("talks", 0)),
                                  ("Attaques", st.get("attacks", 0))]),
            ("Monde", C_COG, [("Feux", st.get("fires", 0)),
                              ("Moutons", len(getattr(sim, "sheep", []))),
                              ("Monstres", len(getattr(sim, "monsters", [])))]),
        ]
        self._t(screen, T.F_SUB, "SOCIÉTÉ", T.TEXT, x0 + T.S4, y, bold=True)
        self._t(screen, T.F_SMALL, "motifs observés, jamais imposés", T.MUTED,
                x0 + T.S4 + self._tw(T.F_SUB, "SOCIÉTÉ", True) + T.S3, y + 3,
                max_w=self.panel_r - 180)
        y += 26
        region = pygame.Rect(x0 + T.S3, y, self.panel_r - 2 * T.S3,
                             self.content_bottom() - y)
        off = self._scroll["societe"]
        old = screen.get_clip()
        screen.set_clip(region)
        self._hit_clip = region
        cy = region.y - off
        for title, color, rows in groups:
            h = 28 + ((len(rows) + 1) // 2) * 21 + T.S2
            card = self._card(screen, pygame.Rect(region.x, cy, region.width, h), T.R2)
            pygame.draw.rect(screen, color, (card.x, card.y + T.S2, 3, 15), border_radius=2)
            self._t(screen, T.F_SMALL, title.upper(), _mix(color, (0, 0, 0), .3),
                    card.x + T.S3, card.y + T.S2, bold=True)
            colw = (card.width - 2 * T.S3) // 2
            for i, (lbl, val) in enumerate(rows):
                lx = card.x + T.S3 + (i % 2) * colw
                ly = card.y + 30 + (i // 2) * 21
                self._t(screen, T.F_SMALL, lbl, T.MUTED, lx, ly, max_w=colw - 54)
                self._t(screen, T.F_BODY, val, T.TEXT, lx + colw - T.S3, ly - 1,
                        right=True, bold=True)
            cy = card.bottom + T.S2
        screen.set_clip(old)
        self._hit_clip = None
        self._content_h["societe"] = (cy + off) - region.y
        self._scrollbar(screen, region, self._content_h["societe"], off, scroll_key="societe")

    def _tab_journal(self, screen, sim, y):
        x0 = self.x0
        self._t(screen, T.F_SUB, "JOURNAL", T.TEXT, x0 + T.S4, y, bold=True)
        y += 26
        fx, fy = x0 + T.S3, y
        for cid in ["tous"] + list(LOG_CATS.keys()):
            col = T.MUTED if cid == "tous" else LOG_CATS[cid]
            lbl = "tous" if cid == "tous" else LOG_TITLES.get(cid, cid)
            cw = self._tw(T.F_MICRO, lbl) + 16
            if fx + cw > x0 + self.panel_r - T.S3:
                fx, fy = x0 + T.S3, fy + 23
            self._chip(screen, (fx, fy, cw, 19), lbl, f"jfil:{cid}",
                       self.jfilter == cid, color=col)
            fx += cw + T.S1
        y = fy + 27

        region = pygame.Rect(x0 + T.S3, y, self.panel_r - 2 * T.S3,
                             self.content_bottom() - y)
        self._card(screen, region, T.R2)
        entries = [e for e in sim.journal
                   if self.jfilter == "tous" or (len(e) > 3 and e[3] == self.jfilter)]
        rh = 23
        shown = entries[-max(1, (region.height - T.S2) // rh):]
        old = screen.get_clip()
        screen.set_clip(region)
        for i, e in enumerate(shown):
            t = e[0] if len(e) > 0 else 0
            txt = e[1] if len(e) > 1 else ""
            cat = e[3] if len(e) > 3 else "monde"
            cnt = e[4] if len(e) > 4 else 1
            ry = region.y + T.S2 + i * rh
            pygame.draw.circle(screen, LOG_CATS.get(cat, T.MUTED),
                               (region.x + T.S4, ry + 8), 4)
            mm, ss = divmod(int(t / config.SIM_HZ), 60)
            self._t(screen, T.F_MICRO, f"{mm:02}:{ss:02}", T.FAINT, region.x + 27, ry + 2)
            self._t(screen, T.F_SMALL, txt + (f"  ×{cnt}" if cnt and cnt > 1 else ""),
                    T.TEXT, region.x + 68, ry + 1, max_w=region.width - 80)
        if not shown:
            self._t(screen, T.F_BODY, "Rien à signaler pour ce filtre.", T.FAINT,
                    region.centerx, region.y + 36, cx=True)
        screen.set_clip(old)

    def _tab_creator(self, screen, sim, y):
        x0 = self.x0
        self._t(screen, T.F_SUB, "CREER UN OUTIL", T.TEXT, x0 + T.S4, y, bold=True)
        self._t(screen, T.F_SMALL, "dessine, nomme, choisis un type, puis equipe l'etre selectionne",
                T.MUTED, x0 + T.S4, y + 18)
        y += 40
        ed = self.tool_editor
        ed.draw(screen, x0 + T.S4, y)
        base_y = ed.palette_y + 34

        name_r = pygame.Rect(x0 + T.S4, base_y, self.panel_r - 2 * T.S4, 28)
        self._card(screen, name_r, T.R1, T.SURFACE, T.BORDER_2)
        self._t(screen, T.F_BODY, ed.name, T.TEXT, name_r.x + 8, name_r.centery, cy=True)
        self._push(name_r, "creator_name")
        y2 = name_r.bottom + T.S2

        self._t(screen, T.F_SMALL, "TYPE", T.MUTED, x0 + T.S4, y2, bold=True)
        y2 += 18
        for i, kind in enumerate(("hache", "pioche", "marteau")):
            r = pygame.Rect(x0 + T.S4 + i * 74, y2, 68, 22)
            sel = self.tool_editor_kind == kind
            pygame.draw.rect(screen, T.SELECT if sel else T.SURFACE, r, border_radius=T.R1)
            if sel:
                pygame.draw.rect(screen, T.ACCENT, r, 1, border_radius=T.R1)
            self._t(screen, T.F_SMALL, kind, T.TEXT if sel else T.MUTED,
                    r.centerx, r.centery, cx=True, cy=True)
            self._push(r, f"creator_kind:{kind}")
        y2 += 30

        disabled = sim.selected is None or not getattr(sim.selected, "alive", False)
        save_r = pygame.Rect(x0 + T.S4, y2, self.panel_r - 2 * T.S4, 32)
        self._btn(screen, save_r,
                  "Creer et equiper" if not disabled else "Selectionne un etre d'abord",
                  "creator_save", radius=T.R2)
        clear_r = pygame.Rect(x0 + T.S4, save_r.bottom + T.S1, self.panel_r - 2 * T.S4, 28)
        self._btn(screen, clear_r, "Effacer le dessin", "creator_clear", radius=T.R1)
        return clear_r.bottom + T.S2

    # ══════════════════════════════════════════════════════════════════
    #  7. PIED DE PAGE
    # ══════════════════════════════════════════════════════════════════
    def _footer(self, screen, sim, cam):
        x0, mm = self.x0, self.minimap_rect()
        pygame.draw.line(screen, T.BORDER, (x0 + T.S3, mm.y - T.S2),
                         (x0 + self.panel_r - T.S3, mm.y - T.S2))
        ver = sim.w.tick // 30
        gen = getattr(sim.w, "gen", None)
        if gen is not None:
            ver = (ver, gen.version)
        if (self._minimap_surf is None or self._minimap_ver != ver
                or self._minimap_surf.get_width() != mm.width):
            self._minimap_surf = self._build_minimap(sim, mm, gen)
            self._minimap_ver = ver
        screen.blit(self._minimap_surf, mm)
        pygame.draw.rect(screen, T.BORDER_2, mm, 1, border_radius=T.R1)
        sc = mm.width / (GRID * TILE)
        for sh in getattr(sim, "sheep", [])[::4]:
            pygame.draw.circle(screen, (234, 236, 240),
                               (int(mm.x + sh.x * sc), int(mm.y + sh.y * sc)), 1)
        for ag in sim.agents:
            pygame.draw.circle(screen, CLAN_COLORS.get(ag.color, (150, 150, 150)),
                               (int(mm.x + ag.x * sc), int(mm.y + ag.y * sc)), 2)
        vr = pygame.Rect(int(mm.x + cam.x * sc), int(mm.y + cam.y * sc),
                         max(6, int(cam.view_w() * sc)), max(6, int(cam.view_h() * sc)))
        vr.clamp_ip(mm)
        pygame.draw.rect(screen, T.ACCENT, vr, 1)
        self._push(mm, "minimap")

        info = pygame.Rect(mm.right + T.S2, mm.y,
                           self.panel_r - mm.width - 3 * T.S3, mm.height)
        self._card(screen, info, T.R2)
        self._t(screen, T.F_BODY, f"zoom ×{cam.zoom}  ·  {int(cam.tilt)}°",
                T.TEXT, info.x + T.S3, info.y + T.S2, bold=True, max_w=info.width - 2 * T.S3)
        for i, ln in enumerate(["molette = zoom · [ / ] = incliner",
                                 "clic molette = examiner · F = suivre"]):
            self._t(screen, T.F_MICRO, ln, T.MUTED, info.x + T.S3,
                    info.y + 22 + i * 13, max_w=info.width - 2 * T.S3)
        name = sim.selected.name if sim.selected else "—"
        self._btn(screen, (info.x + T.S3, info.bottom - 24, info.width - 2 * T.S3, 20),
                  f"Suivi · {name}" if self.follow else f"Suivre {name}",
                  "follow", primary=self.follow)

        cy = mm.bottom + T.S2
        bx = x0 + T.S3
        u = (self.panel_r - 2 * T.S3) // 8
        self._btn(screen, (bx, cy, u * 2 - T.S1, T.H_BTN),
                  "Pause" if not sim.paused else "Lancer", "pause", primary=sim.paused)
        self._btn(screen, (bx + u * 2, cy, u - T.S1, T.H_BTN), "Pas", "step")
        sp = self._card(screen, (bx + u * 3, cy, u - T.S1, T.H_BTN), T.R1, T.SURFACE_2)
        self._t(screen, T.F_SMALL, f"×{sim.speed}", T.TEXT, sp.centerx, sp.centery,
                cx=True, cy=True, bold=True)
        self._btn(screen, (bx + u * 4, cy, u - T.S1, T.H_BTN), "−", "speed-1")
        self._btn(screen, (bx + u * 5, cy, u - T.S1, T.H_BTN), "+", "speed+1")
        self._btn(screen, (bx + u * 6, cy, u * 2 - T.S1, T.H_BTN), "Sauver", "save_game")
        self._btn(screen, (bx + u * 7, cy, u * 2 - T.S1, T.H_BTN), "Charger", "load_game")

    def _build_minimap(self, sim, mm, gen):
        """Vignette du monde.

        Bug corrigé : la v1 allouait `a` en (largeur, hauteur, 3) — la forme
        attendue par `blit_array` — puis l'indexait avec des masques en
        (hauteur, largeur). La grille étant carrée, numpy ne levait aucune
        erreur : la minimap était simplement TRANSPOSÉE, sans que rien ne le
        signale. On construit désormais en (y, x) puis on transpose une fois.
        """
        land = sim.w.land
        h, w = land.shape
        if gen is not None:
            from game import worldgen as _wg
            rgb = _wg.render_minimap_rgb(gen, max(mm.width, 128))
            rgb = rgb.astype(np.uint8)
            step_h, step_w = rgb.shape[0], rgb.shape[1]
            # surcouches (abri / feu) rééchantillonnées sur la même grille
            iy = (np.arange(step_h) * (h / step_h)).astype(int).clip(0, h - 1)
            ix = (np.arange(step_w) * (w / step_w)).astype(int).clip(0, w - 1)
            shelter = sim.w.shelter[np.ix_(iy, ix)] > 0
            fire = sim.w.fire[np.ix_(iy, ix)] > 0
            rgb[shelter] = (226, 180, 98)
            rgb[fire] = (224, 122, 74)
            a = rgb
        else:
            a = np.empty((h, w, 3), dtype=np.uint8)
            a[:] = (208, 216, 226)
            a[land > 0] = (170, 202, 174)
            a[sim.w.blocked > 0] = (128, 118, 106)
            a[sim.w.shelter > 0] = (226, 180, 98)
            a[sim.w.fire > 0] = (224, 122, 74)
        surf = pygame.Surface((a.shape[1], a.shape[0]))
        pygame.surfarray.blit_array(surf, np.ascontiguousarray(a.transpose(1, 0, 2)))
        return pygame.transform.smoothscale(surf, (mm.width, mm.height))

    # ── infobulle ───────────────────────────────────────────────────
    def _tooltip(self, screen):
        if self.hover_asset is None or self.hover_asset >= len(self.am.assets):
            return
        a = self.am.assets[self.hover_asset]
        lines = [CHIP_LABELS.get(a.category, a.category)]
        aff = " · ".join(list(getattr(a, "affordances", []))[:6])
        if aff:
            lines.append(aff)
        w = min(280, max([self._tw(T.F_SMALL, a.name, True)] +
                         [self._tw(T.F_MICRO, l) for l in lines]) + 2 * T.S3)
        h = 20 + len(lines) * 15 + T.S2
        mx, my = pygame.mouse.get_pos()
        tx = max(0, min(mx + 14, SCREEN_W - w - T.S2))
        ty = max(0, min(my + 14, SCREEN_H - h - T.S2))
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(s, (*T.TIP_BG, 244), (0, 0, w, h), border_radius=T.R1)
        screen.blit(s, (tx, ty))
        self._t(screen, T.F_SMALL, a.name, T.TIP_FG, tx + T.S3, ty + T.S2,
                bold=True, max_w=w - 2 * T.S3)
        for i, ln in enumerate(lines):
            self._t(screen, T.F_MICRO, ln, T.TIP_MUTED, tx + T.S3,
                    ty + 24 + i * 15, max_w=w - 2 * T.S3)

    # ══════════════════════════════════════════════════════════════════
    #  8. INTERACTION CARTE
    # ══════════════════════════════════════════════════════════════════
    def brush_radius(self):
        """Rayon courant du pinceau, en tuiles — lu par le renderer pour
        dessiner l'aperçu circulaire des outils de terrain."""
        return self.brush_size if self.mode in (
            "water", "land", "wall", "carve", "restore", "erase") else 0

    def set_ghost(self, cam):
        self._cam = cam
        mx, my = pygame.mouse.get_pos()
        vr = self.view_rect()
        self._over_map = vr.collidepoint((mx, my))
        if self._over_map:
            wx, wy = cam.to_world(mx - vr.x, my)
            self.hover_tile = (int(wx // TILE), int(wy // TILE))
        self.hover_asset = None
        for rect, aid in self._cells:
            if rect.collidepoint((mx, my)):
                self.hover_asset = aid
                break

    def apply_map_tool(self, sim, cam, button):
        mx, my = pygame.mouse.get_pos()
        vr = self.view_rect()
        if not vr.collidepoint((mx, my)):
            return
        wx, wy = cam.to_world(mx - vr.x, my)
        tx, ty = int(wx // TILE), int(wy // TILE)

        if button == 2 or self.mode == "inspect":
            pick_radius_world = max(TILE * 2.0, 60.0 / max(0.10, cam.zoom))
            best, bd = None, pick_radius_world * pick_radius_world
            for ag in sim.agents:
                if not getattr(ag, "alive", False):
                    continue
                d2 = (ag.x - wx) ** 2 + (ag.y - wy) ** 2
                if d2 <= bd:
                    best, bd = ag, d2
            if best is None:
                for sh in sim.sheep:
                    if not getattr(sh, "alive", False):
                        continue
                    d2 = (sh.x - wx) ** 2 + (sh.y - wy) ** 2
                    if d2 <= bd:
                        best, bd = sh, d2
            if best is not None:
                from .entities import Being, Sheep
                if isinstance(best, Being):
                    sim.selected = best
                    self.tab = "etre"
                    self._scroll["etre"] = 0
                    self.follow = True
                    sim.log(f"Examen : {best.name}, {best.age_years:.1f} ans.",
                            (59, 118, 214), "monde")
                elif isinstance(best, Sheep):
                    self.tab = "etre"
                    sim.log(f"Mouton en ({best.tx}, {best.ty}). "
                            f"Energie : {best.energy:.0%}",
                            (108, 208, 128), "monde")
                return True
            from .diagnostics import tile_snapshot
            self.selected_tile = (tx, ty)
            self.last_tile_snapshot = tile_snapshot(sim, tx, ty)
            self.tab = "decor"
            self._scroll["decor"] = 0
            return True

        if button != 1:
            return False

        if not (0 <= tx < GRID and 0 <= ty < GRID):
            return False

        w = sim.w
        changed = False

        if self.mode in ("water", "land", "wall"):
            r = self.brush_size
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    if dx * dx + dy * dy > r * r + 1:
                        continue
                    cx, cy = tx + dx, ty + dy
                    if not (0 <= cx < GRID and 0 <= cy < GRID):
                        continue
                    if self.mode == "water":
                        if w.land[cy, cx]:
                            w.remove(cx, cy, quiet=True)
                            w.land[cy, cx] = 0
                            w.water[cy, cx] = 1
                            w.blocked[cy, cx] = 0
                            w.floor[cy, cx] = -1
                            w.mark_dirty(cx, cy, 2)
                            changed = True
                    elif self.mode == "land":
                        if not w.land[cy, cx] or w.blocked[cy, cx]:
                            w.land[cy, cx] = 1
                            w.water[cy, cx] = 0
                            w.blocked[cy, cx] = 0
                            w.floor[cy, cx] = -1
                            w.mark_dirty(cx, cy, 2)
                            changed = True
                    elif self.mode == "wall":
                        if w.land[cy, cx] and not w.blocked[cy, cx] and w.content_at(cx, cy) < 0:
                            stones = self.am.pool("stone_res") or self.am.pool("gold_stone")
                            if stones:
                                aid = int(self.am.pick(stones, sim.rng))
                                w.place(cx, cy, aid, self.am, hp=8, solid=True,
                                        size=self.am.assets[aid].size_tiles)
                                changed = True
            if changed:
                self._minimap_ver = -1
            return changed

        gen = getattr(w, "gen", None)
        if self.mode in ("carve", "restore"):
            if gen is None:
                return False
            from game import worldgen as _wg
            fn = _wg.carve_mountain if self.mode == "carve" else _wg.restore_mountain
            changed = fn(w, gen, tx, ty, radius=self.brush_size,
                         strength=0.12 if self.mode == "carve" else 0.18)
            if changed:
                self._minimap_ver = -1
            return bool(changed)

        if self.mode == "erase":
            removed = w.remove(tx, ty)
            old_len = len(w.items)
            w.items = [it for it in w.items
                       if not (int(it.x // TILE) == tx and int(it.y // TILE) == ty)]
            had_floor = w.floor[ty, tx] >= 0
            w.floor[ty, tx] = -1
            w.mark_dirty(tx, ty)
            self._minimap_ver = -1
            return removed or len(w.items) != old_len or had_floor

        if self.mode == "floor":
            aid = self.asset
            if aid in self.am.floors:
                sheet_idx = self.am.floors.index(aid)
                w.set_floor(tx, ty, sheet_idx * 216)
                return True
            if self.am.floors:
                w.set_floor(tx, ty, 0)
                return True
            return False

        if self.mode == "block":
            return sim.do_build_block_player(tx, ty, material=self.block_material)

        if self.mode == "place":
            aid = self.asset
            if not (0 <= aid < len(self.am.assets)):
                return False
            adef = self.am.assets[aid]
            if not getattr(adef, "placable", False):
                return False
            if not w.land[ty, tx] or w.blocked[ty, tx] or w.content_at(tx, ty) >= 0:
                return False
            w.place(tx, ty, aid, self.am, hp=max(1, getattr(adef, "hp", 1)),
                    solid=bool(adef.solid), shelter=bool(adef.shelter),
                    size=adef.size_tiles if adef.solid else 1)
            return True

        if self.mode == "agent":
            created = sim.spawn_agent(
                x=wx, y=wy, color=self.tpl_color, cls=self.tpl_cls,
                n_hid=self.brain_size, sex=self.tpl_sex,
                body=self.tpl_body.copy(), cog=self.tpl_cog.copy(),
                personality=self.tpl_personality.copy(),
                emotions=self.tpl_emotions.copy(), needs=self.tpl_needs.copy(),
            )
            if created is not None:
                sim.selected = created
                self._needs_save = True
                self.follow = True
                return True
            return False

        if self.mode == "sheep":
            sim.spawn_sheep(x=wx, y=wy)
            return True

        if self.mode == "monster":
            sim.spawn_monster(x=wx, y=wy)
            return True

        return False

    # ══════════════════════════════════════════════════════════════════
    #  9. ÉVÉNEMENTS
    # ══════════════════════════════════════════════════════════════════
    def handle_event(self, ev, sim):
        self._sim_ref = sim
        pos = getattr(ev, "pos", None)

        # 1. Modale : reçoit tous les événements tant qu'elle est ouverte
        if self.spawn_modal:
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                self.spawn_modal = False
                self.drag = None
                self.modal_scroll.drag_grab_y = None
                return True

            if ev.type == pygame.MOUSEWHEEL:
                if self.modal_view is not None:
                    self.modal_scroll.offset = ScrollController.clamp(
                        self.modal_scroll.offset - int(ev.y) * ScrollController.WHEEL_STEP,
                        self.modal_content_h, self.modal_view.height)
                return True

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = pos or pygame.mouse.get_pos()

                # Check modal scrollbar handle
                if self.modal_handle and self.modal_handle.collidepoint((mx, my)):
                    self.modal_scroll.drag_grab_y = my - self.modal_handle.y
                    self.drag = "scrollbar:modal"
                    return True

                # Check modal scrollbar track (page scroll)
                if self.modal_track and self.modal_track.collidepoint((mx, my)):
                    page = int(self.modal_view.height * 0.85)
                    if my < self.modal_handle.y if self.modal_handle else my < self.modal_track.centery:
                        self.modal_scroll.offset -= page
                    else:
                        self.modal_scroll.offset += page
                    self.modal_scroll.offset = ScrollController.clamp(
                        self.modal_scroll.offset, self.modal_content_h, self.modal_view.height)
                    return True

                # Check buttons
                for r, fid in reversed(self.buttons):
                    if r.collidepoint((mx, my)):
                        if fid.startswith("ps:"):
                            self.drag = fid
                            self._drag_set(sim, mx, my)
                            return True
                        self._click(fid)
                        return True
                return True  # Click outside: keep modal open

            if ev.type == pygame.MOUSEMOTION:
                mx, my = pos or pygame.mouse.get_pos()
                if self.drag == "scrollbar:modal":
                    if self.modal_track and self.modal_handle:
                        handle_h = self.modal_handle.height
                        max_offset = max(1, self.modal_content_h - self.modal_track.height)
                        travel = max(1, self.modal_track.height - handle_h)
                        target_y = my - self.modal_scroll.drag_grab_y
                        ratio = max(0.0, min(1.0, (target_y - self.modal_track.y) / travel))
                        self.modal_scroll.offset = ScrollController.clamp(
                            int(ratio * max_offset), self.modal_content_h, self.modal_view.height)
                    return True
                # Normal drag for sliders
                if self.drag:
                    self._drag_set(sim, mx, my)
                    return True

            if ev.type == pygame.MOUSEBUTTONUP:
                if self.drag == "scrollbar:modal":
                    self.modal_scroll.drag_grab_y = None
                self.drag = None
                return True

            return True

        # 2. Gestion normale (pas de modale)
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            if self.creator_focus:
                self.creator_focus = False
                return True
            return False

        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            mx, my = pos or pygame.mouse.get_pos()
            for r, fid in reversed(self.buttons):
                if not r.collidepoint((mx, my)):
                    continue
                if fid.startswith("ps:"):
                    self.drag = fid
                    self._drag_set(sim, mx, my)
                    return True
                if fid == "minimap":
                    self._minimap_jump((mx, my))
                    return True
                if fid.startswith("sec:"):
                    k = fid[4:]
                    self.sections[k] = not self.sections.get(k, False)
                    return True
                if fid.startswith("card:"):
                    k = fid[5:]
                    self.cards_open[k] = not self.cards_open.get(k, True)
                    return True
                if fid.startswith("fav:"):
                    self._toggle_fav(int(fid[4:]))
                    return True
                self._click(fid)
                return True
            if not self.view_rect().collidepoint((mx, my)):
                self.focus_search = self.hab_focus = False
            return False

        if ev.type == pygame.MOUSEBUTTONDOWN and self.tab == "creator" and ev.button in (1, 3):
            mx, my = pos or pygame.mouse.get_pos()
            picked = self.tool_editor.palette_hit(mx, my)
            if picked is not None:
                self.tool_editor.current_color = picked
                return True
            if self.tool_editor.paint_at(mx, my, erase=(ev.button == 3)):
                self.painting = ev.button
                return True

        if ev.type == pygame.MOUSEMOTION and self.drag:
            if isinstance(self.drag, str) and self.drag.startswith("scrollbar:"):
                key = self.drag.split(":", 1)[1]
                if key in self.scroll_tracks:
                    track, ch = self.scroll_tracks[key]
                    state = self.scroll_state_for(key)
                    ScrollController.drag(state, ev.pos, track, ch, track.height)
                    self._scroll[key] = state.offset
                return True
            mx, my = pos or pygame.mouse.get_pos()
            self._drag_set(sim, mx, my)
            return True

        if ev.type == pygame.MOUSEMOTION and getattr(self, "painting", None) and self.tab == "creator":
            mx, my = pos or pygame.mouse.get_pos()
            self.tool_editor.paint_at(mx, my, erase=(self.painting == 3))
            return True

        if ev.type == pygame.MOUSEBUTTONUP and self.drag:
            if isinstance(self.drag, str) and self.drag.startswith("scrollbar:"):
                key = self.drag.split(":", 1)[1]
                ScrollController.release(self.scroll_state_for(key))
            self.drag = None
            return True
        if ev.type == pygame.MOUSEBUTTONUP:
            self.painting = None

        if ev.type == pygame.MOUSEWHEEL:
            mx, my = pygame.mouse.get_pos()
            if self.left_open and T.RAIL_W <= mx < T.RAIL_W + self.panel_l:
                lh = getattr(self, '_left_region_h', SCREEN_H - 200)
                state = self.scroll_state_for("_left")
                state.offset = ScrollController.clamp(
                    state.offset - ev.y * ScrollController.WHEEL_STEP,
                    self._content_h.get("_left", 0), lh)
                self._scroll["_left"] = state.offset
                return True
            if mx >= self.x0:
                key = self.current_scroll_key()
                track_info = self.scroll_tracks.get(key)
                if track_info is not None:
                    region, ch = track_info
                    content_region = pygame.Rect(
                        self.x0 + T.S3, self.content_top(),
                        self.panel_r - 2 * T.S3 - 18,
                        self.content_bottom() - self.content_top())
                    if content_region.collidepoint((mx, my)) or region.collidepoint((mx, my)):
                        state = self.scroll_state_for(key)
                        state.offset = ScrollController.clamp(
                            state.offset - ev.y * ScrollController.WHEEL_STEP,
                            ch, region.height)
                        self._scroll[key] = state.offset
                        return True
                h = self.content_bottom() - self.content_top()
                if self._content_h.get(self.tab, 0) == 0:
                    self._measure_content(self.tab, sim)
                state = self.scroll_state_for(key)
                state.offset = ScrollController.clamp(
                    state.offset - ev.y * ScrollController.WHEEL_STEP,
                    self._content_h.get(self.tab, 0), h)
                self._scroll[key] = state.offset
                return True
            return False

        if ev.type == pygame.KEYDOWN and (self.focus_search or self.hab_focus or self.creator_focus):
            if self.creator_focus:
                cur = self.tool_editor.name
                if ev.key == pygame.K_BACKSPACE:
                    self.tool_editor.name = cur[:-1]
                elif ev.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    self.creator_focus = False
                elif ev.unicode and ev.unicode.isprintable() and len(cur) < 20:
                    self.tool_editor.name = cur + ev.unicode
            else:
                field = "search" if self.focus_search else "hab_search"
                cur = getattr(self, field)
                if ev.key == pygame.K_BACKSPACE:
                    setattr(self, field, cur[:-1])
                elif ev.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    self.focus_search = self.hab_focus = False
                elif ev.unicode and ev.unicode.isprintable() and len(cur) < 24:
                    setattr(self, field, cur + ev.unicode)
            return True

        return False

    def _click(self, fid):
        if not fid.startswith("hdel:"):
            self.hdel_pending = None
        if fid.startswith("mode:"):
            new_mode = fid[5:]
            if new_mode == "agent":
                self.spawn_modal = True
                self.focus_search = False
                self.hab_focus = False
                self.creator_focus = False
                self.drag = None
                return
            self.mode = new_mode
        elif fid.startswith("tab:"):
            self.tab = fid[4:]
            self.focus_search = self.hab_focus = False
        elif fid.startswith("cat:"):
            self.category = fid[4:]
        elif fid.startswith("asset:"):
            aid = int(fid[6:])
            self.asset = aid
            if aid not in self.recents:
                self.recents.insert(0, aid)
                self.recents = self.recents[:12]
            if self.mode == "inspect":
                self.mode = "place"
        elif fid.startswith("jfil:"):
            self.jfilter = fid[5:]
        elif fid == "toggle_left":
            self.left_open = not self.left_open
        elif fid == "only_favs":
            self.only_favs = not self.only_favs
            self._filter_sig = None
        elif fid == "home":
            self.tab = "etre"
        elif fid == "search":
            self.focus_search, self.hab_focus = True, False
        elif fid == "search_clear":
            self.search = ""
        elif fid == "hab_focus":
            self.hab_focus, self.focus_search = True, False
        elif fid == "hab_clear":
            self.hab_search = ""
        elif fid in ("pause", "step", "reset", "reseed", "grid", "save_game", "load_game"):
            self.action = (fid, None)
        elif fid == "follow":
            self.follow = not self.follow
        elif fid.startswith("spawn_sheep:"):
            self.action = ("spawn_sheep", int(fid.split(":")[1]))
        elif fid == "spawn_agent":
            self.spawn_modal = True
            self.focus_search = False
            self.hab_focus = False
            self.creator_focus = False
            self.drag = None
        elif fid == "spawn_modal":
            self.spawn_modal = not self.spawn_modal
        elif fid == "spawn_confirm":
            self.spawn_modal = False
            self.mode = "agent"
        elif fid == "goto_cemetery":
            graves = getattr(self._sim_ref.w, "cemetery", ()) if self._sim_ref else ()
            if graves and self._cam:
                cx = sum(g[0] for g in graves) / len(graves)
                cy = sum(g[1] for g in graves) / len(graves)
                self._cam.center_on(cx * TILE, cy * TILE)
        elif fid == "creator_clear":
            self.tool_editor.clear()
        elif fid.startswith("creator_kind:"):
            self.tool_editor_kind = fid[13:]
        elif fid == "creator_name":
            self.focus_search = self.hab_focus = False
            self.creator_focus = True
        elif fid == "creator_save":
            self.action = ("create_tool", None)
        elif fid == "speed+1":
            self.action = ("speed", 1)
        elif fid == "speed-1":
            self.action = ("speed", -1)
        elif fid.startswith("speed_set:"):
            self.action = ("speed_set", int(fid.split(":")[1]))
        elif fid in ("bsize-", "bsize+"):
            sizes = list(SIZES)
            i = sizes.index(self.brain_size) if self.brain_size in SIZES else 1
            i = max(0, i - 1) if fid == "bsize-" else min(len(sizes) - 1, i + 1)
            self.brain_size = sizes[i]
        elif fid == "bsize_slider":
            geo = self._slider_geo.get("bsize_slider")
            if geo:
                mx = pygame.mouse.get_pos()[0]
                sl_x, sl_w = geo
                t = max(0.0, min(1.0, (mx - sl_x) / max(1, sl_w)))
                raw = 25 + t * (1000 - 25)
                sizes = list(SIZES)
                closest = min(sizes, key=lambda s: abs(s - raw))
                self.brain_size = closest
            self.drag = "bsize_slider"
        elif fid == "bsize_slider_modal":
            geo = self._slider_geo.get("bsize_slider_modal")
            if geo:
                mx = pygame.mouse.get_pos()[0]
                sl_x, sl_w = geo
                t = max(0.0, min(1.0, (mx - sl_x) / max(1, sl_w)))
                raw = 25 + t * (1000 - 25)
                sizes = list(SIZES)
                closest = min(sizes, key=lambda s: abs(s - raw))
                self.brain_size = closest
            self.drag = "bsize_slider_modal"
        elif fid in ("brush-", "brush+"):
            self.brush_size = max(1, min(15, self.brush_size + (1 if fid == "brush+" else -1)))
        elif fid == "brush_slider":
            geo = self._slider_geo.get("brush_slider")
            if geo:
                mx = pygame.mouse.get_pos()[0]
                sl_x, sl_w = geo
                t = max(0.0, min(1.0, (mx - sl_x) / max(1, sl_w)))
                self.brush_size = max(1, min(15, int(1 + t * 14)))
            self.drag = "brush_slider"
        elif fid.startswith("scrollthumb:"):
            key = fid[12:]
            mx, my = pygame.mouse.get_pos()
            state = self.scroll_state.get(key)
            if state:
                track_info = self.scroll_tracks.get(key)
                if track_info:
                    track, ch = track_info
                    handle = ScrollController.handle_rect(track, ch, state.offset)
                    if handle and handle.collidepoint((mx, my)):
                        state.drag_grab_y = my - handle.y
                        self.drag = f"scrollbar:{key}"
        elif fid.startswith("scrolltrack:"):
            key = fid[12:]
            mx, my = pygame.mouse.get_pos()
            state = self.scroll_state.get(key)
            if state:
                track_info = self.scroll_tracks.get(key)
                if track_info:
                    track, ch = track_info
                    handle = ScrollController.handle_rect(track, ch, state.offset)
                    # Page scroll: click above handle = scroll up, below = scroll down
                    page = int(track.height * 0.85)
                    if handle is None or my < handle.y:
                        state.offset -= page
                    else:
                        state.offset += page
                    state.offset = ScrollController.clamp(state.offset, ch, track.height)
                    self._scroll[key] = state.offset
        elif fid.startswith("scroll:"):
            key = fid[7:]
            geo = self._scroll_geo.get(key)
            if geo:
                region, total = geo
                mx, my = pygame.mouse.get_pos()
                if total > region.height:
                    t = max(0.0, min(1.0, (my - region.y) / region.height))
                    self._scroll[key] = int(t * (total - region.height))
                    self.drag = fid
        elif fid.startswith("blockmat:"):
            self.block_material = fid[9:]
        elif fid.startswith("overlay:"):
            self.active_overlay = fid[8:]
        elif fid.startswith("tcolor:"):
            self.tpl_color = fid[7:]
            self.normalize_template_class()
        elif fid.startswith("tcls:"):
            candidate = fid[5:]
            if candidate in self.template_classes():
                self.tpl_cls = candidate
        elif fid.startswith("tsex:"):
            self.tpl_sex = fid[5:]
            self.normalize_template_class()
        elif fid.startswith("hsel:"):
            eid = int(fid[5:])
            for a in self._sim_ref.agents:
                if a.eid == eid:
                    self._sim_ref.selected = a
                    self.follow = True
                    self.tab = "etre"
                    self._scroll["etre"] = 0
                    break
        elif fid.startswith("hdel:"):
            eid = int(fid[5:])
            if self.hdel_pending == eid:
                # 2e clic : confirmer suppression
                for a in self._sim_ref.agents:
                    if a.eid == eid:
                        self._sim_ref.remove_agent(a, a.name)
                        if self._sim_ref.selected is a:
                            self._sim_ref.selected = None
                        self.hdel_pending = None
                        self._needs_save = True
                        break
            else:
                # 1er clic : armer la confirmation
                self.hdel_pending = eid

    def _toggle_fav(self, aid):
        if aid in self.favs:
            self.favs.remove(aid)
        else:
            self.favs.insert(0, aid)
            self.favs = self.favs[:12]
        self._filter_sig = None

    def _minimap_jump(self, pos):
        if not self._cam:
            return
        mm = self.minimap_rect()
        sc = mm.width / (GRID * TILE)
        self._cam.center_on((pos[0] - mm.x) / sc, (pos[1] - mm.y) / sc)

    def _drag_set(self, sim, mx, my=None):
        if not self.drag:
            return
        if self.drag == "scrollbar:modal":
            # Already handled in handle_event
            return
        if self.drag.startswith("scroll:"):
            key = self.drag[7:]
            geo = self._scroll_geo.get(key)
            if geo and my is not None:
                region, total = geo
                if total > region.height:
                    t = max(0.0, min(1.0, (my - region.y) / region.height))
                    self._scroll[key] = int(t * (total - region.height))
            return
        if self.drag == "bsize_slider":
            geo = self._slider_geo.get("bsize_slider")
            if geo:
                sl_x, sl_w = geo
                t = max(0.0, min(1.0, (mx - sl_x) / max(1, sl_w)))
                raw = 25 + t * (1000 - 25)
                sizes = list(SIZES)
                closest = min(sizes, key=lambda s: abs(s - raw))
                self.brain_size = closest
            return
        if self.drag == "bsize_slider_modal":
            geo = self._slider_geo.get("bsize_slider_modal")
            if geo:
                sl_x, sl_w = geo
                t = max(0.0, min(1.0, (mx - sl_x) / max(1, sl_w)))
                raw = 25 + t * (1000 - 25)
                sizes = list(SIZES)
                closest = min(sizes, key=lambda s: abs(s - raw))
                self.brain_size = closest
            return
        if self.drag == "brush_slider":
            geo = self._slider_geo.get("brush_slider")
            if geo:
                sl_x, sl_w = geo
                t = max(0.0, min(1.0, (mx - sl_x) / max(1, sl_w)))
                self.brush_size = max(1, min(15, int(1 + t * 14)))
            return
        p = self.drag.split(":")
        if len(p) != 3:
            return
        key, pi = p[1], int(p[2])
        arr = self._array(sim.selected, key)
        geo = self._slider_geo.get(self.drag)
        if arr is None or geo is None or pi >= len(arr):
            return
        bx, bw = geo
        t = max(0.0, min(1.0, (mx - bx) / max(1, bw)))
        arr[pi] = t
        ag = sim.selected
        if ag is not None and key == "needs":
            if pi == 0:
                ag.hunger = t
            elif pi == 1:
                ag.energy = t
