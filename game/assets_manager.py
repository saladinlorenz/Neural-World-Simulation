"""Moteur d'assets : discover, dedup by content hash, classify by heuristics of path,
slice sprite sheets, expose semantic pools for the simulation + dashboard.

Every image file in /assets is catalogued (minus byte-identical repetitions) and can be
placed from the dashboard; key ones get simulation semantics (edible, harvestable, solid...).
"""
import hashlib
import os
from collections import OrderedDict

import numpy as np
from PIL import Image, ImageDraw

from .affordance_definitions import render_asset, build_recipe_for
from .config import ASSETS_DIR, CLAN_COLORS

IMG_EXT = (".png", ".jpg", ".jpeg", ".bmp", ".tga", ".gif")

# ----------------------------------------------------------------------------
# asset record
# ----------------------------------------------------------------------------
class AssetDef:
    __slots__ = ("id", "name", "label", "path", "pack", "category", "role", "kind",
                 "frames", "fw", "fh", "px", "solid", "shelter", "edible", "harvest",
                 "tool", "material", "color", "blocked_footprint", "meta", "afford",
                 "flammable", "weight", "placable", "afford_details", "build_recipe",
                 "_procedural_surface")

    def __init__(self, **kw):
        self.id = -1
        self.name = ""
        self.label = ""
        self.path = ""
        self.pack = ""
        self.category = "divers"
        self.role = ""
        self.kind = "single"      # single | strip | grid44 | tiles
        self.frames = 1
        self.fw = 16
        self.fh = 16
        self.px = 16              # display size in world px (largest side)
        self.solid = False
        self.shelter = False
        self.edible = 0.0         # nutrition (>0 = edible)
        self.harvest = None       # dict(material=..., amount=..., hp=...)
        self.tool = False
        self.material = ""
        self.color = ""
        self.blocked_footprint = 1
        self.meta = {}
        self.afford = ["observe"]           # possibilites physiques exposees au cerveau
        self.flammable = False
        self.weight = 1.0
        self.placable = True      # posable dans le monde via le panneau Decor
        self.afford_details = None
        self.build_recipe = None
        self._procedural_surface = None
        for k, v in kw.items():
            setattr(self, k, v)

    @property
    def size_tiles(self):
        return max(1, min(4, int(np.ceil(self.px / 16.0))))

    @property
    def world_rect(self):
        s = self.px
        ar = self.fw / max(1, self.fh)
        w = s * ar if ar >= 1 else s
        h = s if ar >= 1 else s / ar
        return w, h


CATEGORY_LABELS = [
    ("ressources", "Ressources"),
    ("nourriture", "Nourriture"),
    ("outils", "Outils"),
    ("animaux", "Animaux"),
    ("props", "Props"),
    ("vehicules", "Vehicules"),
    ("tombe", "Tombes"),
    ("decor", "Decors"),
    ("sol", "Sols"),
    ("unites", "Unites"),
    ("effets", "Effets"),
    ("interface", "Interface"),
    ("atlas", "Atlas"),
    ("rendus", "Rendus"),
    ("divers", "Divers"),
]

# categories d'assets NON posables dans le monde : fichiers de travail de la
# palette (feuilles de texture brutes, images promo, icones d'UI, frames de
# skel persons) — pas des objets du monde.
NON_PLACABLE = {"atlas", "rendus", "interface", "unites"}


def _tokens(rel):
    return rel.replace("\\", "/").lower()


def _classify(rel, fname):
    """Return (category, role, extra_kwargs) from path heuristics."""
    t = _tokens(rel)
    f = fname.lower()
    kw = {}
    in_tiny = "tiny swords" in t

    # ------------------------------------------------------------------ generated_assets (food / animals)
    if "generated_assets" in t:
        if f.startswith("food_"):
            FOOD_NUTRITION = {
                "tomato": 25.0, "potato": 30.0, "mushroom": 20.0,
                "meat_cooked": 55.0, "fish_raw": 40.0, "egg": 25.0,
                "cheese": 35.0, "carrot": 30.0, "bread": 40.0,
                "berry": 15.0, "banana": 25.0, "apple": 20.0,
            }
            key = f[5:-4]  # strip "food_" and ".png"
            n = FOOD_NUTRITION.get(key, 25.0)
            return "nourriture", "food", {"px": 16, "edible": n}
        if f.startswith("animal_"):
            kind = f[7:-4]  # strip "animal_" and ".png"
            px = {"bear": 26, "wolf": 22, "deer": 22, "rabbit": 16,
                  "bird": 14, "fish": 16}.get(kind, 20)
            return "animaux", "monster", {"px": px,
                                          "meta": {"kind": kind, "state": "idle"}}

    # ------------------------------------------------------------------ tiny units
    if in_tiny and "/units/" in t:
        color = next((c for c in CLAN_COLORS if f"{c} units" in t), "")
        cls = next((c for c in ("pawn", "archer", "lancer", "monk", "warrior") if f"/{c}/" in t), "")
        if "arrow" in f:
            return "effets", "projectile", {"px": 12}
        if "effect" in f or "heal_effect" in f:
            return "effets", "fx_heal", {"px": 28}
        state = ""
        for s in ("idle", "run", "attack", "shoot", "guard", "defence", "interact", "heal"):
            if s in f:
                state = "work" if s == "interact" else ("guard" if s == "defence" else s)
                break
        tool = next((x for x in ("axe", "pickaxe", "hammer", "knife", "meat", "gold", "wood") if x in f), "")
        kw = dict(meta={"cls": cls, "state": state, "tool": tool, "color": color})
        return "unites", "skin", dict(px=26, **kw)

    # ------------------------------------------------------------------ tiny terrain
    if in_tiny and "/terrain/" in t:
        if "/resources/wood/trees" in t:
            if "stump" in f:
                return "ressources", "stump", {"px": 18}
            return "ressources", "tree", {"px": 34, "solid": True,
                                          "harvest": dict(material="bois", amount=2, hp=6)}
        if "/resources/wood" in t and "wood resource" in f:
            return "ressources", "item_wood", {"px": 14, "material": "bois"}
        if "/resources/gold/gold stones" in t:
            if "_highlight" in f:
                return "ressources", "fx_highlight", {"px": 20}
            return "ressources", "gold_stone", {"px": 22, "solid": True,
                                                "harvest": dict(material="or", amount=2, hp=5)}
        if "/resources/gold" in t:
            return "ressources", "gold_pile", {"px": 14, "material": "or"}
        if "/resources/meat/meat resource" in t:
            return "nourriture", "meat_res", {"px": 14, "edible": 55.0}
        if "/resources/meat/sheep" in t:
            state = "grass" if "grass" in f else ("move" if "move" in f else "idle")
            return "animaux", "sheep", {"px": 22, "meta": {"state": state}}
        if "/resources/tools" in t:
            return "outils", "tool", {"px": 12, "tool": True}
        if "/decorations/bushes" in t:
            return "nourriture", "bush", {"px": 20, "edible": 14.0}
        if "/decorations/clouds" in t:
            return "decor", "cloud", {"px": 90}
        if "/decorations/rocks in the water" in t:
            return "decor", "waterrock", {"px": 20, "solid": True}
        if "/decorations/rocks" in t:
            return "ressources", "stone_res", {"px": 20, "solid": True,
                                               "harvest": dict(material="pierre", amount=2, hp=5)}
        if "rubber duck" in t:
            return "decor", "duck", {"px": 10}
        if "/terrain/tileset" in t:
            if "shadow" in f:
                return "effets", "shadow", {"px": 20}
            return "sol", "floor", {"kind": "tiles", "px": 16}
        return "decor", "decor", {"px": 18}

    # ignorer tiny buildings (pre-construits)
    if in_tiny and "/buildings/" in t:
        return None, None, None

    # ------------------------------------------------------------------ tiny fx
    if in_tiny and "particle fx" in t:
        fxn = "dust" if "dust" in f else ("explosion" if "explosion" in f else "fire")
        return "effets", "fx", {"px": 18, "meta": {"fx": fxn}}

    # ------------------------------------------------------------------ tiny UI
    if in_tiny and "ui element" in t:
        sub = "buttons" if "/buttons/" in t else ("bars" if "/bars/" in t else
              ("avatars" if "human avatars" in t else ("icons" if "/icons/" in t else
              ("cursors" if "/cursors/" in t else ("ribbons" if "ribbons" in t else
              ("banners" if "banners" in t or "banner" in f else ("papers" if "/papers/" in t else
              ("table" if "wood table" in t else ("swords" if "swords" in t else "misc")))))))))
        return "interface", "ui_" + sub, {"px": 32}

    # ------------------------------------------------------------------ kenney previews
    if "/previews/" in t and fname.lower().endswith(".png"):
        kit = _tokens(rel).split("/")[0]
        return _kenney(kit, f)

    # ------------------------------------------------------------------ ultimate fantasy rts (rendus PNG 1024px a decoupe alpha)
    if "ultimate fantasy rts" in t and "/png/" in t:
        return _uf_rts(f[:-4].replace("_", " ").lower())

    # ------------------------------------------------------------------ kaykit (3D : skip, pas utilisable en 2D)
    if "kaykit" in t or "resource_bits" in t:
        return None, None, None

    # ------------------------------------------------------------------ craftpix top-down trees (AVANT atlas)
    if "craftpix" in t and "top-down-trees" in t:
        if "/trees_shadow" in t or "/trees_texture_shadow" in t:
            return None, None, None
        if "source" in f or f.endswith(".psd") or "coupon" in f:
            return None, None, None
        if "palm" in f:
            return "decor", "tree", {"px": 48, "solid": True,
                                     "harvest": dict(material="bois", amount=2, hp=4)}
        return "ressources", "tree", {"px": 44, "solid": True,
                                      "harvest": dict(material="bois", amount=3, hp=6),
                                      "meta": {"trim": True}}

    # ------------------------------------------------------------------ murals / atlases / samples
    if any(x in t for x in ("/samples/", "preview", "sample", "contents_", "overview", "extra_")):
        return "rendus", "mural", {"px": 120}
    if any(x in t for x in ("/textures/", "texture", "atlas", "hexagons_medieval", "wild_animals_map")):
        return "atlas", "mural", {"px": 140}

    # ------------------------------------------------------------------ craftpix chibi sprites
    if "craftpix" in t and ("chibi" in t or "sprites" in t):
        is_female = "female" in t
        is_male = "male" in t
        if is_female or is_male:
            # extraire le nom du personnage (ex: Enchantress, Knight...)
            parts = t.replace("\\", "/").split("/")
            char_name = ""
            for p in parts:
                if p.startswith("craftpix"):
                    continue
                if "sprite" in p or "free" in p or "fantasy" in p or "chibi" in p or "pixel" in p:
                    continue
                if p and not p.endswith(".png"):
                    char_name = p.capitalize()
                    break
            CRAFTPIX_MAP = {
                "enchantress": ("purple", "enchantress"),
                "knight":      ("blue",   "knight"),
                "musketeer":   ("red",    "musketeer"),
                "archer":      ("yellow", "archer"),
                "swordsman":   ("black",  "swordsman"),
                "wizard":      ("purple", "wizard"),
            }
            # skip non-usable frames
            if any(x in f for x in ("dead.png", "hurt.png", "jump.png")):
                return None, None, None
            state = ""
            if "idle" in f:
                state = "idle"
            elif "run" in f:
                state = "run"
            elif "walk" in f:
                state = "run"
            elif "attack" in f:
                state = "attack"
            elif "contruire" in f or "build" in f:
                state = "build"
            else:
                return None, None, None
            cn = char_name.lower()
            color, cls = CRAFTPIX_MAP.get(cn, ("blue", cn))
            return "unites", "skin", dict(px=26, meta={"cls": cls, "state": state, "tool": "", "color": color})

    # ------------------------------------------------------------------ craftpix portraits
    if "portraits" in t and fname.lower().endswith(".png"):
        return "interface", "ui_portraits", {"px": 44}

    # ------------------------------------------------------------------ outils custom (tools_custom/)
    if "tools_custom" in t or "custom_tools" in t:
        kind = "hache"
        for k in ("hache", "pioche", "marteau"):
            if k in f:
                kind = k
                break
        return "outils", "tool", {"px": 14, "tool": True,
                                  "meta": {"tool_kind": kind, "custom": True}}

    # ------------------------------------------------------------------ vegetables (custom sprites extraits)
    if "vegetable" in t or "vegetables" in t:
        nutrition = 35.0
        if "carotte" in f:
            nutrition = 30.0
        elif "tomate" in f:
            nutrition = 25.0
        elif "champignon" in f:
            nutrition = 20.0
        elif "oignon" in f:
            nutrition = 22.0
        elif "courgette" in f:
            nutrition = 28.0
        return "nourriture", "food", {"px": 16, "edible": nutrition}

    # ------------------------------------------------------------------ retro rpg animals (extracted singles)
    if "animals" in t and "retro" not in t:
        if "_attack" in f:
            kind = f.split("_attack")[0]
            return "animaux", "monster_attack", {"px": 22,
                                                  "meta": {"kind": kind, "state": "attack"}}
        kind = f.replace(".png", "")
        px = {"bear": 24, "wolf": 22, "snake": 18, "beatle": 14}.get(kind, 20)
        return "animaux", "monster", {"px": px,
                                      "meta": {"kind": kind, "state": "idle"}}

    # ------------------------------------------------------------------ retro rpg animals (original sheets = ignored, use extracted singles)
    if "retro rpg" in t and "animal" in t:
        return "divers", "ignored", {}

    # ------------------------------------------------------------------ standalone environment sprites
    if fname.lower() == "sheep.png":
        return "animaux", "sheep", {"px": 22, "meta": {"state": "idle"}}

    return "divers", "decor", {"px": 20}


def _kenney(kit, f):
    name = f[:-4].replace("-", " ").replace("_", " ")
    FOOD_HI = ("meat", "fish", "chicken", "ham", "turkey", "bacon", "pork", "cheese", "bread",
               "egg", "soup", "dish", "meal", "drumstick", "boar", "steak", "ribs", "sushi",
               "pie", "cake", "cookie")
    if kit == "kenney_food-kit":
        n = 40.0 if any(x in name for x in FOOD_HI) else 22.0
        if "half" in name or "slice" in name:
            n = 16.0
        return "nourriture", "food", {"px": 13, "edible": n}
    SOLID = ("wall", "barricade", "tower", "castle", "house", "hut", "gate", "door", "roof",
             "chimney", "pillar", "column", "bridge", "coffin", "barrel", "box", "crate",
             "well", "forge", "machine", "arcade", "jukebox", "hockey", "basketball",
             "sarcophagus", "statue", "fence")
    shelter = any(x in name for x in ("house", "hut", "tent", "bed", "bedroll"))
    solid = any(x in name for x in SOLID) or shelter
    if kit == "kenney_graveyard-kit":
        return "tombe", "grave", {"px": 16, "solid": solid}
    if kit in ("kenney_castle-kit", "kenney_building-kit"):
        return None, None, None
    if kit == "kenney_car-kit":
        return "vehicules", "vehicle", {"px": 30, "solid": True}
    if kit == "kenney_survival-kit":
        ed = 0.0
        if any(x in name for x in FOOD_HI):
            ed = 34.0
        # outils
        if name.startswith("tool "):
            up = "upgraded" in name
            tool_kind = name.replace(" upgraded", "").replace("tool ", "")
            px = 14 if up else 12
            return "outils", "tool", {"px": px, "tool": True,
                                      "meta": {"tool_kind": tool_kind, "upgraded": up}}
        # ressources
        if name.startswith("resource "):
            mat = "bois" if "wood" in name or "planks" in name else "pierre"
            return "ressources", "stone_res" if mat == "pierre" else "item_wood", {
                "px": 16, "material": mat}
        # arbres
        if name.startswith("tree"):
            return "ressources", "tree", {"px": 32, "solid": True,
                                          "harvest": dict(material="bois", amount=3, hp=6)}
        # ignorer structures pre-construites
        if name.startswith("structure") or name.startswith("tent"):
            return None, None, None
        # ignorer workbench
        if name.startswith("workbench"):
            return None, None, None
        # campfeu
        if name.startswith("campfire"):
            return "props", "prop", {"px": 18, "edible": 0.0, "flammable": True}
        # caisses / stockage
        if any(name.startswith(x) for x in ("box", "chest", "barrel", "bucket")):
            return "props", "prop", {"px": 18, "solid": True}
        # clotures
        if name.startswith("fence"):
            return "props", "prop", {"px": 18, "solid": True}
        # poissons
        if name.startswith("fish"):
            return "nourriture", "food", {"px": 14, "edible": 40.0}
        # nature
        if name.startswith("rock") or name.startswith("patch") or name.startswith("grass"):
            return "decor", "decor", {"px": 16}
        # panneau
        if name.startswith("signpost"):
            return "props", "prop", {"px": 18}
        # lits (sans shelter)
        if name.startswith("bedroll"):
            return "props", "prop", {"px": 18}
        # bouteille
        if name.startswith("bottle"):
            return "props", "prop", {"px": 14}
        # panneaux metal
        if name.startswith("metal"):
            return "props", "prop", {"px": 18, "solid": True}
        # floor
        if name.startswith("floor"):
            return "props", "prop", {"px": 18}
        return "props", "prop", {"px": 18, "solid": solid, "edible": ed}
    if kit == "kenney_mini-arcade":
        return "props", "prop", {"px": 24, "solid": solid}
    return "props", "prop", {"px": 18, "solid": solid}


def _uf_rts(n):
    """Ultimate Fantasy RTS : rendus 1024x1024 avec transparence, a rogner (trim)."""
    def T(px_, **kw):
        meta = kw.pop("meta", {})
        meta["trim"] = True
        return dict(px=px_, meta=meta, **kw)
    if "_cut" in n or "group cut" in n:
        return "ressources", "stump", T(44)
    if n.startswith("resource tree") or n.startswith("resource pine") or n.startswith("resource tree group"):
        return "ressources", "tree", T(52, solid=True,
                                        harvest=dict(material="bois", amount=3, hp=7))
    if n.startswith("resource gold"):
        return "ressources", "gold_stone", T(32, solid=True,
                                             harvest=dict(material="or", amount=3, hp=6))
    if n.startswith("resource rock") or n in ("rock", "rock group"):
        return "ressources", "stone_res", T(34, solid=True,
                                            harvest=dict(material="pierre", amount=3, hp=6))
    if "mountain" in n:
        return "decor", "boulder", T(110, solid=True)
    if n == "logs":
        return "ressources", "item_wood", T(30, material="bois")
    if "wheat" in n:
        return "nourriture", "bush", T(58, edible=26.0)
    if "barrel" in n or "crate" in n:
        return "props", "prop", T(30, solid=True, material="bois")
    # Ignorer tous les batiments pre-construits
    return None, None, None


def _apply_afford(a):
    """Affordances : ce que le monde PERMET de faire avec cet objet.
    Le cerveau recoit ces possibilites, jamais une etiquette de role."""
    r = a.role
    af = ["observe"]
    if r == "tree":
        af += ["harvest", "burn", "block"]
        a.flammable = True
    elif r == "stump":
        af += ["burn"]
        a.flammable = True
    elif r in ("stone_res", "gold_stone"):
        af += ["harvest", "carry", "throw", "hit", "block"]
    elif r in ("food", "bush", "meat_res"):
        af += ["eat", "carry", "give", "burn"]
        a.flammable = True
    elif r in ("item_wood", "gold_pile"):
        af += ["carry", "place", "give", "burn"]
        a.flammable = True
    elif r == "tool":
        af += ["use", "carry", "hit"]
    elif r in ("house", "fort"):
        af += ["shelter", "sleep", "burn", "block"]
        a.flammable = True
    elif r == "grave":
        af += ["mourn", "mark"]
    elif r in ("prop", "vehicle"):
        af += ["block", "hit", "sit"]
    elif r in ("waterrock", "boulder"):
        af += ["block", "climb"]
    elif r == "sheep":
        af += ["chase", "hit", "shear"]
    elif r == "mural":
        af += ["lean", "decorate"]
    elif r == "duck":
        af += ["follow"]
    a.afford = af


# ----------------------------------------------------------------------------
# manager
# ----------------------------------------------------------------------------
class AssetManager:
    def __init__(self, headless=False):
        self.headless = headless
        self.assets: list[AssetDef] = []
        self.by_role: dict[str, list[int]] = {}
        self.by_cat: dict[str, list[int]] = {}
        self.skins: dict[tuple, list[int]] = {}     # (color, cls, state) -> [aid]
        self.sheep: dict[str, int] = {}
        self.monsters: dict[str, dict[str, int]] = {}
        self.fx: dict[str, list[int]] = {}
        self.ui: dict[str, list[int]] = {}
        self.floors: list[int] = []
        self.projectile = None
        self.shadow = None
        self.flammable = set()
        self._surf_cache = OrderedDict()
        self._thumb_cache = OrderedDict()
        self._tile_cache = {}
        self._avatar_cache = OrderedDict()
        self.discovered = 0
        self.deduped = 0

    # ------------------------------------------------------------------ scan
    def discover(self):
        seen = {}
        recs = []
        # collect craftpix attack frames for merging
        _attack_buf = {}  # (pack, char_name, color, cls) -> [(p, f), ...]
        for dp, _dn, fn in os.walk(ASSETS_DIR):
            if "__MACOSX" in dp or "_merged" in dp:
                continue
            # os.walk suit l'ordre du systeme de fichiers : sans tri des
            # sous-dossiers, les ``aid`` positionnels changeraient d'une
            # machine a l'autre et decaleraient les sauvegardes.
            _dn[:] = sorted(_dn)
            for f in sorted(fn):
                if f.startswith("._") or not f.lower().endswith(IMG_EXT):
                    continue
                p = os.path.join(dp, f)
                try:
                    with open(p, "rb") as fh:
                        head = fh.read(65536)
                        fh.seek(0, 2)
                        size = fh.tell()
                    h = hashlib.sha1(head).hexdigest() + f"|{size}"
                except OSError:
                    continue
                self.discovered += 1
                if h in seen:
                    continue
                seen[h] = p
                self.deduped += 1
                rel = os.path.relpath(p, ASSETS_DIR)
                pack = rel.replace("\\", "/").split("/")[0]
                cat, role, kw = _classify(rel, f)
                # skip files that _classify marked as unusable
                if cat is None:
                    continue
                try:
                    with Image.open(p) as im:
                        w, hh = im.size
                except Exception:
                    continue
                # collect craftpix attack frames for later merge
                if (cat == "unites" and role == "skin"
                        and kw.get("meta", {}).get("state") == "attack"
                        and "craftpix" in rel.replace("\\", "/").lower()):
                    mk = (pack, kw["meta"].get("cls", ""), kw["meta"].get("color", ""))
                    _attack_buf.setdefault(mk, []).append(p)
                    continue
                kind = kw.pop("kind", "single")
                frames = 1
                fw, fh_ = w, hh
                if kind == "strip" or (w > hh and w % hh == 0 and hh >= 48 and cat in
                                       ("unites", "ressources", "animaux", "decor", "effets")):
                    frames = max(1, w // hh)
                    fw, fh_ = hh, hh
                    kind = "strip"
                    # detect grid spritesheets (frames too large for a strip)
                    if fw > 128 and hh > 128 and w >= 48 and hh >= 48:
                        # treat as grid: assume 48x48 frames
                        fw, fh_ = 48, 48
                        cols = max(1, w // 48)
                        rows = max(1, hh // 48)
                        frames = cols * rows
                        kind = "grid"
                elif cat == "interface" and "avatars" in role:
                    frames, fw, fh_, kind = 16, w // 4, hh // 4, "grid44"
                meta = kw.get("meta") or {}
                if meta.get("trim") and kind == "single":
                    try:
                        with Image.open(p) as im:
                            bb = im.convert("RGBA").split()[3].getbbox()
                        if bb and bb[2] - bb[0] > 8 and bb[3] - bb[1] > 8:
                            meta["_bb"] = bb
                            fw, fh_ = bb[2] - bb[0], bb[3] - bb[1]
                        else:
                            meta.pop("trim")
                    except Exception:
                        meta.pop("trim")
                aid = len(self.assets)
                a = AssetDef(id=aid, name=f, label=f[:-4].replace("_", " ").replace("-", " "),
                             path=p, pack=pack, category=cat, role=role, kind=kind,
                             frames=frames, fw=fw, fh=fh_, **kw)
                a.placable = cat not in NON_PLACABLE
                a.blocked_footprint = a.size_tiles if a.solid else 1
                _apply_afford(a)
                a.afford_details = render_asset(a)
                a.build_recipe = build_recipe_for(a)
                self.assets.append(a)
                if a.flammable:
                    self.flammable.add(aid)
                self.by_role.setdefault(role, []).append(aid)
                self.by_cat.setdefault(cat, []).append(aid)

        # merge craftpix attack frames into strips
        for (pack, cls, color), paths in _attack_buf.items():
            if not paths:
                continue
            imgs = []
            for pp in sorted(paths):
                try:
                    with Image.open(pp) as im:
                        imgs.append(im.convert("RGBA"))
                except Exception:
                    continue
            if not imgs:
                continue
            fw, fh_ = imgs[0].size
            merged = Image.new("RGBA", (fw * len(imgs), fh_), (0, 0, 0, 0))
            for i, im in enumerate(imgs):
                merged.paste(im, (i * fw, 0))
            merged_path = os.path.join(ASSETS_DIR, "_merged", f"{pack}_{cls}_attack.png")
            os.makedirs(os.path.dirname(merged_path), exist_ok=True)
            merged.save(merged_path)
            aid = len(self.assets)
            a = AssetDef(id=aid, name=f"{cls}_attack.png",
                         label=f"{cls} attack", path=merged_path, pack=pack,
                         category="unites", role="skin", kind="strip",
                         frames=len(imgs), fw=fw, fh=fh_, px=26,
                         meta={"cls": cls, "state": "attack", "tool": "", "color": color})
            a.placable = False
            a.blocked_footprint = 1
            _apply_afford(a)
            a.afford_details = render_asset(a)
            a.build_recipe = build_recipe_for(a)
            self.assets.append(a)
            self.by_role.setdefault("skin", []).append(aid)
            self.by_cat.setdefault("unites", []).append(aid)

        # indices
        for a in self.assets:
            m = a.meta
            if a.role == "skin":
                st = m.get("state") or "idle"
                st = {"shoot": "attack", "guard": "idle"}.get(st, st)
                if st not in ("idle", "run", "attack", "work", "heal", "build"):
                    st = "idle"
                key = (m.get("color", "blue"), m.get("cls", "pawn"), st)
                self.skins.setdefault(key, []).append(a.id)
            elif a.role == "sheep":
                self.sheep[m["state"]] = a.id
            elif a.role in ("monster", "monster_attack"):
                kind = m.get("kind", "unknown")
                state = m.get("state", "idle")
                self.monsters.setdefault(kind, {})[state] = a.id
            elif a.role == "fx":
                self.fx.setdefault(m["fx"], []).append(a.id)
            elif a.role.startswith("ui_"):
                self.ui.setdefault(a.role[3:], []).append(a.id)
            elif a.role == "floor":
                self.floors.append(a.id)
            elif a.role == "projectile":
                self.projectile = a.id
            elif a.role == "shadow":
                self.shadow = a.id

        # copy build sprites to all characters (they share the same animation)
        build_ids = [a.id for a in self.assets if a.role == "skin"
                     and a.meta.get("state") == "build"]
        if build_ids:
            all_chars = {(k[0], k[1]) for k in self.skins
                         if k[2] == "idle"}
            for color, cls in all_chars:
                key = (color, cls, "build")
                if key not in self.skins:
                    self.skins[key] = list(build_ids)
        for k in self.skins:
            self.skins[k].sort()
        return self

    # ------------------------------------------------------------------ pixel io
    def _pil_frame(self, a: AssetDef, frame=0):
        with Image.open(a.path) as im:
            im = im.convert("RGBA")
            if a.kind == "strip":
                x = frame * a.fw
                im = im.crop((x, 0, x + a.fw, a.fh))
            elif a.kind == "grid" or a.kind == "grid44":
                cols = max(1, im.width // a.fw)
                i, j = frame % cols, frame // cols
                im = im.crop((i * a.fw, j * a.fh, (i + 1) * a.fw, (j + 1) * a.fh))
            elif a.kind == "tiles":
                raise ValueError("use tile_cells")
            else:
                if a.meta.get("_bb"):
                    im = im.crop(a.meta["_bb"])
                else:
                    im = im.copy()
            return im

    def _to_surf(self, pil, w, h):
        if (pil.width, pil.height) != (w, h):
            pil = pil.resize((max(1, int(w)), max(1, int(h))), Image.LANCZOS)
        return pil

    def surface(self, aid, frame=0, scale=1.0):
        a = self.assets[aid]
        if getattr(a, "_procedural_surface", None) is not None:
            base = a._procedural_surface
            if abs(scale - 1.0) < 1e-6:
                return base
            w = max(1, int(base.width * scale))
            h = max(1, int(base.height * scale))
            return base.resize((w, h), Image.LANCZOS)
        k = (aid, frame, round(scale, 2))
        hit = self._surf_cache.get(k)
        if hit is not None:
            self._surf_cache.move_to_end(k)
            return hit
        try:
            if a.kind == "tiles":
                pil = self._tile_pil(aid, (aid * 7 + 3) % 216)   # carreau representatif
            else:
                pil = self._pil_frame(a, frame)
        except Exception:
            pil = Image.new("RGBA", (8, 8), (255, 0, 255, 255))
        ar = a.fw / max(1, a.fh)
        if ar >= 1:
            ww, hh = a.px, a.px / ar
        else:
            ww, hh = a.px * ar, a.px
        surf = self._to_surf(pil, ww * scale, hh * scale)
        self._surf_cache[k] = surf
        if len(self._surf_cache) > 2600:
            self._surf_cache.popitem(last=False)
        return surf

    def display_size(self, aid, scale=1.0):
        a = self.assets[aid]
        ar = a.fw / max(1, a.fh)
        if ar >= 1:
            return int(a.px * scale), int(a.px / ar * scale) or 2
        return int(a.px * ar * scale) or 2, int(a.px * scale)

    def thumbnail(self, aid, size=54):
        # Un appel avec un tuple (largeur, hauteur) cassait a la fois le
        # redimensionnement et le repli : normaliser pour rester robuste.
        if isinstance(size, (tuple, list)):
            size = int(size[0])
        size = max(1, int(size))
        k = (aid, size)
        hit = self._thumb_cache.get(k)
        if hit is not None:
            self._thumb_cache.move_to_end(k)
            return hit
        a = self.assets[aid]
        try:
            if a.kind == "tiles":
                pil = self._tile_pil(aid, (aid * 7 + 3) % 216)
            else:
                pil = self._pil_frame(a, 0)
            pil.thumbnail((size, size), Image.LANCZOS)
            surf = self._to_surf(pil, pil.width, pil.height)
        except Exception:
            surf = Image.new("RGBA", (size, size), (60, 40, 70, 255))
        self._thumb_cache[k] = surf
        if len(self._thumb_cache) > 1400:
            self._thumb_cache.popitem(last=False)
        return surf

    # ------------------------------------------------------------------ tileset floors
    def _tile_pil(self, sheet_aid, cell):
        a = self.assets[sheet_aid]
        with Image.open(a.path) as im:
            im = im.convert("RGBA")
            cols = im.width // 32
            i, j = cell % cols, cell // cols
            i %= max(1, cols)
            j = min(j, max(0, im.height // 32 - 1))
            return im.crop((i * 32, j * 32, i * 32 + 32, j * 32 + 32))

    def tile_cells(self, sheet_aid):
        a = self.assets[sheet_aid]
        return (a.fw // 32) * (a.fh // 32) if a.kind == "tiles" else 0

    def floor_tile(self, sheet_aid, cell, scale=1.0):
        k = (sheet_aid, cell, round(scale, 2))
        hit = self._tile_cache.get(k)
        if hit is not None:
            return hit
        pil = self._tile_pil(sheet_aid, cell).resize((int(16 * scale), int(16 * scale)), Image.LANCZOS)
        surf = self._to_surf(pil, pil.width, pil.height)
        self._tile_cache[k] = surf
        return surf

    def random_floor_tile(self, sheet_aid, rng):
        return self.floor_tile(sheet_aid, int(rng.integers(self.tile_cells(sheet_aid) or 1)))

    # ------------------------------------------------------------------ avatars (UI)
    def avatar(self, idx, size=44):
        sheets = self.ui.get("avatars", [])
        if not sheets:
            return Image.new("RGBA", (size, size), (60, 40, 70, 255))
        k = (idx % (len(sheets) * 16), size)
        hit = self._avatar_cache.get(k)
        if hit is not None:
            self._avatar_cache.move_to_end(k)
            return hit
        sheet = sheets[(idx // 16) % len(sheets)]
        frame = idx % 16
        a = self.assets[sheet]
        i, j = frame % 4, frame // 4
        with Image.open(a.path) as im:
            im = im.convert("RGBA")
            cw, ch = im.width // 4, im.height // 4
            pil = im.crop((i * cw, j * ch, i * cw + cw, j * ch + ch))
        pil.thumbnail((size, size), Image.LANCZOS)
        surf = self._to_surf(pil, pil.width, pil.height)
        self._avatar_cache[k] = surf
        if len(self._avatar_cache) > 500:
            self._avatar_cache.popitem(last=False)
        return surf

    # ------------------------------------------------------------------ helpers
    def pool(self, role):
        return self.by_role.get(role, [])

    def pick(self, pool_ids, rng, default=None):
        if not pool_ids:
            return default
        return int(rng.choice(pool_ids))

    def skin_states(self, color, cls):
        out = {}
        for st in ("idle", "run", "attack", "work", "heal", "build"):
            ids = self.skins.get((color, cls, st))
            if ids:
                out[st] = ids
        if not out.get("idle"):
            pawn_ids = self.skins.get((color, "pawn", "idle"))
            if not pawn_ids:
                for c in CLAN_COLORS:
                    pawn_ids = self.skins.get((c, "pawn", "idle"))
                    if pawn_ids:
                        break
            out["idle"] = pawn_ids or []
        out.setdefault("run", out["idle"])
        return out

    def unit_colors(self):
        if getattr(self, "_colors", None) is None:
            self._colors = [c for c in CLAN_COLORS if any(k[0] == c for k in self.skins)]
        return self._colors

    def unit_classes(self, color):
        if getattr(self, "_classes", None) is None:
            self._classes = {}
        if color not in self._classes:
            self._classes[color] = sorted({k[1] for k in self.skins if k[0] == color})
        return self._classes[color]

    def stats(self):
        return dict(discovered=self.discovered, deduped=self.deduped,
                    per_cat={lbl: len(self.by_cat.get(c, [])) for c, lbl in CATEGORY_LABELS})

    def catalog_fingerprint(self) -> str:
        """Empreinte stable du catalogue (Save v3 : détection de drift)."""
        import hashlib
        digest = hashlib.sha256()
        for asset in self.assets:
            digest.update(str(getattr(asset, "path", "")).encode("utf-8",
                                                                "replace"))
            digest.update(b"\0")
        return digest.hexdigest()

    def plans_for(self, inv):
        """Retourne la liste des assets constructibles avec l'inventaire donné."""
        from .affordance_definitions import plans_for as _plans_for
        return _plans_for(self, inv)

    def ensure_procedural_blocks(self):
        specs = [
            ("block_wood", "Bloc bois", (150, 108, 62), (110, 78, 44), True),
            ("block_stone", "Bloc pierre", (150, 150, 156), (108, 108, 114), True),
            ("block_roof", "Tuile toit", (125, 70, 55), (86, 45, 38), False),
            ("block_door", "Porte", (108, 70, 38), (65, 42, 25), False),
        ]
        for role, label, fill, edge, solid in specs:
            if self.by_role.get(role):
                continue
            img = Image.new("RGBA", (16, 16), (*fill, 255))
            draw = ImageDraw.Draw(img)
            draw.rectangle([0, 0, 15, 15], outline=(*edge, 255), width=2)
            if role == "block_door":
                draw.ellipse([10, 6, 14, 10], fill=(220, 190, 80, 255))
            elif role == "block_roof":
                draw.line([1, 5, 15, 5], fill=(*edge, 255), width=1)
                draw.line([1, 10, 15, 10], fill=(*edge, 255), width=1)
            aid = len(self.assets)
            a = AssetDef(
                id=aid, name=f"{role}.png",
                label=label,
                path="", pack="procedural", category="batiments", role=role,
                kind="single", frames=1, fw=16, fh=16, px=16,
                solid=solid, blocked_footprint=1, placable=False,
                meta={"procedural": True},
            )
            a.afford = ("block", "hit")
            a._procedural_surface = img
            self.assets.append(a)
            self.by_role.setdefault(role, []).append(aid)
            self.by_cat.setdefault("batiments", []).append(aid)

    def ensure_procedural_tools(self):
        shapes = {
            "hache": (168, 118, 68),
            "pioche": (148, 148, 156),
            "marteau": (120, 120, 130),
        }
        for kind, color in shapes.items():
            role_key = f"tool_{kind}"
            if self.by_role.get(role_key):
                continue
            img = Image.new("RGBA", (14, 14), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.polygon([(2, 12), (10, 2), (12, 4), (4, 14)], fill=(*color, 255))
            draw.polygon([(2, 12), (10, 2), (12, 4), (4, 14)], outline=(40, 40, 44, 255))
            aid = len(self.assets)
            a = AssetDef(
                id=aid, name=f"{kind}.png", label=kind.capitalize(), path="",
                pack="procedural", category="outils", role="tool",
                kind="single", frames=1, fw=14, fh=14, px=14, tool=True,
                placable=True, meta={"tool_kind": kind, "procedural": True},
            )
            a.afford = ("use", "carry", "hit")
            a._procedural_surface = img
            self.assets.append(a)
            self.by_role.setdefault("tool", []).append(aid)
            self.by_role.setdefault(role_key, []).append(aid)
            self.by_cat.setdefault("outils", []).append(aid)

    def register_custom_tool(self, path, tool_kind, label=None):
        with Image.open(path) as img:
            img = img.convert("RGBA")
            w, h = img.size
        aid = len(self.assets)
        a = AssetDef(
            id=aid, name=os.path.basename(path), label=label or tool_kind,
            path=path, pack="custom_tools", category="outils", role="tool",
            kind="single", frames=1, fw=w, fh=h,
            px=20, tool=True, meta={"tool_kind": tool_kind}, placable=True,
        )
        a.afford = ("use", "carry", "hit")
        self.assets.append(a)
        self.by_role.setdefault("tool", []).append(aid)
        self.by_role.setdefault(f"tool_{tool_kind}", []).append(aid)
        self.by_cat.setdefault("outils", []).append(aid)
        return aid

    def ensure_kaykit_resources(self):
        """KayKit Resource Bits : sprites extraits de la texture atlas."""
        import os as _os
        from .config import ASSETS_DIR
        res_dir = _os.path.join(_os.path.dirname(ASSETS_DIR), "assets", "kaykit_resources")
        if not _os.path.isdir(res_dir):
            return
        specs = [
            ("wood_log",          "Bois (tronc)",     "ressources", "item_wood",
             {"material": "bois", "px": 16}),
            ("wood_plank",        "Planche",          "ressources", "item_wood",
             {"material": "bois", "px": 16}),
            ("wood_planks_stack", "Pile planches",    "ressources", "item_wood",
             {"material": "bois", "px": 20}),
            ("stone_brick",       "Brique pierre",    "ressources", "stone_res",
             {"material": "pierre", "px": 16}),
            ("stone_chunks",      "Cailloux",         "ressources", "stone_res",
             {"material": "pierre", "px": 16}),
            ("stone_stack",       "Pile pierres",     "ressources", "stone_res",
             {"material": "pierre", "px": 20}),
            ("gold_bar",          "Lingot or",        "ressources", "gold_pile",
             {"material": "or", "px": 16}),
            ("gold_nuggets",      "Pepites or",       "ressources", "gold_pile",
             {"material": "or", "px": 16}),
            ("gold_bars_stack",   "Pile lingots or",  "ressources", "gold_pile",
             {"material": "or", "px": 20}),
            ("iron_bar",          "Lingot fer",       "props", "prop",
             {"px": 16, "solid": True}),
            ("iron_nuggets",      "Pepites fer",      "props", "prop",
             {"px": 16}),
            ("iron_bars_stack",   "Pile lingots fer", "props", "prop",
             {"px": 20, "solid": True}),
            ("copper_bar",        "Lingot cuivre",    "props", "prop",
             {"px": 16, "solid": True}),
            ("copper_nuggets",    "Pepites cuivre",   "props", "prop",
             {"px": 16}),
            ("copper_bars",       "Barres cuivre",    "props", "prop",
             {"px": 20, "solid": True}),
        ]
        for fname, label, cat, role, kw in specs:
            path = _os.path.join(res_dir, f"{fname}.png")
            if not _os.path.exists(path):
                continue
            if self.by_role.get(role) and any(
                self.assets[i].name == f"{fname}.png" for i in self.by_role.get(role, [])
            ):
                continue
            try:
                with Image.open(path) as img:
                    img = img.convert("RGBA")
                    w, h = img.size
            except Exception:
                continue
            aid = len(self.assets)
            a = AssetDef(
                id=aid, name=f"{fname}.png", label=label,
                path=path, pack="kaykit", category=cat, role=role,
                kind="single", frames=1,
                fw=w, fh=h,
                px=kw.pop("px", 16),
                solid=kw.pop("solid", False),
                blocked_footprint=1, placable=True,
                material=kw.pop("material", ""),
                meta={"procedural": True},
            )
            for k, v in kw.items():
                setattr(a, k, v)
            a.afford = ("block", "carry", "hit") if a.solid else ("carry", "hit")
            a._procedural_surface = img
            self.assets.append(a)
            self.by_role.setdefault(role, []).append(aid)
            self.by_cat.setdefault(cat, []).append(aid)

    def register_grid_items(self, path, category, role, cell_w, cell_h,
                            labels=None, edible=0.0, tool_item=False,
                            solid=False, harvest=None):
        from PIL import Image as _Img
        with _Img.open(path) as source:
            image = source.convert("RGBA")
        columns = max(1, image.width // cell_w)
        rows = max(1, image.height // cell_h)
        gen_dir = os.path.join(ASSETS_DIR, "generated")
        os.makedirs(gen_dir, exist_ok=True)
        base = os.path.splitext(os.path.basename(path))[0]
        created = []
        for row in range(rows):
            for col in range(columns):
                index = row * columns + col
                x0, y0 = col * cell_w, row * cell_h
                tile = image.crop((x0, y0, x0 + cell_w, y0 + cell_h))
                alpha = tile.split()[3]
                if alpha.getbbox() is None:
                    continue
                tile_path = os.path.join(gen_dir, f"{base}_{index}.png")
                tile.save(tile_path)
                aid = len(self.assets)
                label = (labels[index] if labels and index < len(labels)
                         else f"{role} {index + 1}")
                asset = AssetDef(
                    id=aid, name=os.path.basename(tile_path), label=label,
                    path=tile_path, pack="generated_grid", category=category,
                    role=role, kind="single", frames=1,
                    fw=cell_w, fh=cell_h,
                    px=max(cell_w, cell_h),
                    solid=solid, edible=edible, tool=tool_item,
                    blocked_footprint=1, placable=True,
                    meta={"source_sheet": os.path.basename(path),
                           "grid_index": index},
                )
                if harvest:
                    asset.harvest = harvest
                if edible > 0:
                    asset.afford = ("eat", "carry", "give", "burn")
                else:
                    asset.afford = ("carry", "hit") if solid else ("carry",)
                self.assets.append(asset)
                self.by_role.setdefault(role, []).append(aid)
                self.by_cat.setdefault(category, []).append(aid)
                created.append(aid)
        return created
