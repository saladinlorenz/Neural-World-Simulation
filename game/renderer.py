"""Rendu du monde : terrain procédural (worldgen), tuiles de sol peintes,
phéromones, assets ancrés animables, habitants, moutons, objets lâchés,
effets, nuit / pluie, fantôme de pose.

Corrections et améliorations par rapport à la v1
------------------------------------------------
1. BUG D'ANCRAGE DU TERRAIN : la v1 blittait le patch de terrain à
   `sy - sh`, où `sh` est la hauteur de TOUT le patch. `cam.to_screen()`
   renvoyant le bord bas d'une SEULE tuile, le terrain était décalé vers le
   haut de (hauteur_du_patch − une_tuile). Corrigé : `sy - th`.
2. CACHE DE TERRAIN : la v1 recalculait `render_patch_rgb` + `smoothscale`
   à chaque frame (des millions d'opérations pour rien). Le terrain est
   maintenant mis en cache, invalidé par `gen.version` (incrémenté par les
   outils de sculpture), la zone visible et le zoom.
3. `_night` reconstruisait un dégradé radial par feu et par frame. Les halos
   sont désormais mis en cache par rayon.
4. Polices : `_legend` appelait `SysFont` à chaque frame. Toutes les polices
   passent par `_font()`, mis en cache.
5. Aperçu du pinceau pour les outils de terrain (Sculpter / Restaurer / Eau /
   Terre / Mur) : un cercle de rayon réel, au lieu du carré 1×1 trompeur.
6. Bornes clampées avant usage (la v1 clampait `x1`/`y1` APRÈS s'en être
   servi), `show_grid` déclaré dans `__init__`, variables mortes retirées.
"""
from __future__ import annotations

import numpy as np
import pygame

from . import config
from .config import CLAN_COLORS, GRID, TILE
from .entities import Inhabitant, Sheep
from .world import Item

_blank_mode = False


def set_blank_mode(flag=True):
    global _blank_mode
    _blank_mode = flag


def _zq(zoom):
    """Zoom quantifié — clé de cache stable pour les surfaces mises à l'échelle."""
    return round(zoom, 2)


# --- couleurs de repli (utilisées quand le monde n'a pas de heightmap) ---
_WATER_COL = (46, 92, 158)
_LAND_COL = (86, 150, 62)
_WALL_COL = (128, 118, 106)

_FONT_STACK = "segoeui,inter,dejavusans,liberationsans,arial"

# Couleurs d'aperçu par outil de terrain
_BRUSH_COLORS = {
    "carve":   (228, 142, 78),
    "restore": (118, 198, 138),
    "water":   (78, 168, 232),
    "land":    (150, 196, 96),
    "wall":    (186, 172, 150),
    "erase":   (228, 98, 98),
}
_BRUSH_MODES = tuple(_BRUSH_COLORS)


class _CamView:
    """Caméra décalée sur la zone de carte.

    `Camera.to_screen()` renvoie des coordonnées relatives au coin haut-gauche
    du VIEWPORT, pas de la fenêtre : `dashboard.apply_map_tool` le confirme en
    faisant `cam.to_world(mx - vr.x, my)`. Le renderer blittait pourtant ces
    coordonnées telles quelles sur `screen`, donc toute la carte était décalée
    de la largeur du panneau gauche — et comme ce panneau est repliable, le
    décalage change en cours de partie.

    Ce proxy ajoute l'origine du viewport à `to_screen` et la retire de
    `to_world`. Tout le reste du renderer continue d'appeler `cam.to_screen`
    sans rien savoir de la mise en page.
    """
    __slots__ = ("_c", "ox", "oy", "w", "h")

    def __init__(self, cam, rect):
        self._c = cam
        self.ox, self.oy = rect.x, rect.y
        self.w, self.h = rect.width, rect.height

    def __getattr__(self, name):          # zoom, ys, tilt, x, y, clamp…
        return getattr(self._c, name)

    def to_screen(self, wx, wy):
        sx, sy = self._c.to_screen(wx, wy)
        return sx + self.ox, sy + self.oy

    def to_world(self, sx, sy):
        return self._c.to_world(sx - self.ox, sy - self.oy)

    def visible_tiles(self):
        return self._c.visible_tiles()


class Renderer:
    show_grid = False

    def __init__(self, am):
        self.am = am
        self.clock = 0.0
        self.show_grid = False

        # caches
        self.circle_cache = {}
        self.shadow_cache = {}
        self._ftile_cache = {}
        self._fonts = {}
        self._glow_cache = {}
        self._night_cache = None
        self._night_key = None
        self._rain_cache = None
        self._rain_key = None
        self._terrain_surf = None
        self._terrain_key = None
        self._terrain_pos = (0, 0)

    # ══════════════════════════════════════════════════════════════════
    #  Outils internes
    # ══════════════════════════════════════════════════════════════════
    def _font(self, size, bold=False):
        k = (size, bold)
        f = self._fonts.get(k)
        if f is None:
            f = pygame.font.SysFont(_FONT_STACK, size, bold=bold)
            self._fonts[k] = f
        return f

    def _clan_rgb(self, idx):
        cols = list(CLAN_COLORS.values())
        if 1 <= idx <= len(cols):
            return cols[idx - 1]
        return (180, 180, 180)

    def _circle(self, rgb, size, ys=1.0, alpha=90):
        k = (rgb, int(size), round(ys, 2), alpha)
        c = self.circle_cache.get(k)
        if c is None:
            h = max(3, int(k[1] * k[2]))
            c = pygame.Surface((k[1], h), pygame.SRCALPHA)
            pygame.draw.ellipse(c, (*rgb, alpha), (0, 0, k[1], h))
            if len(self.circle_cache) > 2000:
                self.circle_cache.clear()
            self.circle_cache[k] = c
        return c

    def _ftile(self, sheet_aid, cell, zq, ys_q):
        k = (sheet_aid, cell, zq, ys_q)
        s = self._ftile_cache.get(k)
        if s is None:
            base = self.am.floor_tile(sheet_aid, cell, zq)
            w = base.get_width()
            h = max(2, int(base.get_height() * ys_q))
            s = pygame.transform.scale(base, (w, h)) if h != base.get_height() else base
            if len(self._ftile_cache) > 3000:
                self._ftile_cache.clear()
            self._ftile_cache[k] = s
        return s

    def _ground_shadow(self, w, ys=1.0):
        k = (max(4, int(w)), round(ys, 2))
        s = self.shadow_cache.get(k)
        if s is None:
            s = pygame.Surface((k[0], max(2, int(k[0] * 0.5 * ys))), pygame.SRCALPHA)
            pygame.draw.ellipse(s, (0, 0, 0, 70), (0, 0, k[0], s.get_height()))
            self.shadow_cache[k] = s
        return s

    def _glow(self, radius, alpha):
        """Halo radial mis en cache — évite de le reconstruire par feu et par frame."""
        k = (int(radius), int(alpha) // 8)
        g = self._glow_cache.get(k)
        if g is None:
            rr = max(4, k[0])
            g = pygame.Surface((rr * 2, rr * 2), pygame.SRCALPHA)
            for r in range(rr, 0, -3):
                a = int(6 * (1.0 - r / rr) * alpha / 3)
                if a > 0:
                    pygame.draw.circle(g, (255, 180, 90, a), (rr, rr), r)
            if len(self._glow_cache) > 64:
                self._glow_cache.clear()
            self._glow_cache[k] = g
        return g

    # ══════════════════════════════════════════════════════════════════
    #  Boucle de rendu
    # ══════════════════════════════════════════════════════════════════
    def draw(self, screen, sim, cam, ui):
        self.clock = pygame.time.get_ticks() / 1000.0
        w, z = sim.w, cam.zoom
        ys = cam.ys
        ys_q = round(ys, 2)
        zq = _zq(z)

        # Zone de carte : le panneau gauche est repliable, donc elle bouge.
        # `main.py` la fournit via ui["view_rect"] (= dash.view_rect()) ;
        # sans elle on retombe sur la fenêtre entière.
        # IMPORTANT : view_rect est en coordonnées surface-local (0,0,w,h)
        # car le renderer reçoit view_surf, pas l'écran global.
        view = ui.get("view_rect")
        view = pygame.Rect(view) if view is not None else screen.get_rect()
        if view.width <= 0 or view.height <= 0:
            return
        cam = _CamView(cam, view)

        # tout le rendu de monde reste confiné à la zone de carte
        prev_clip = screen.get_clip()
        screen.set_clip(screen.get_rect())
        try:
            self._draw_world(screen, sim, cam, ui, view, z, ys, ys_q, zq)
        finally:
            screen.set_clip(prev_clip)

    def _draw_world(self, screen, sim, cam, ui, view, z, ys, ys_q, zq):
        w = sim.w

        # bornes visibles, clampées AVANT tout usage
        x0, y0, x1, y1 = self._visible_box(view, cam)

        # 1) fond
        screen.fill(_WATER_COL, view)

        # 2) terrain
        self._terrain(screen, w, cam, x0, y0, x1, y1)

        # Seuils de détail : en vue très éloignée un sprite fait moins d'un
        # pixel. Les dessiner coûte des dizaines de milliers de blits pour un
        # résultat invisible — le terrain porte déjà toute l'information.
        draw_floors = z >= 0.25
        draw_props = z >= 0.20

        # 3) sol peint (tuiles écrasées = perspective)
        floors = w.floor[y0:y1 + 1, x0:x1 + 1] if draw_floors else np.empty((0, 0), np.int32)
        fy, fx = np.nonzero(floors >= 0) if floors.size else ((), ())
        n_sheets = len(self.am.floors)
        for j, i in zip(fy, fx):
            sheet, cell = divmod(int(floors[j, i]), 216)
            if sheet >= n_sheets:
                continue
            surf = self._ftile(self.am.floors[sheet], cell, zq, ys_q)
            sx, sy = cam.to_screen((x0 + i) * TILE, (y0 + j) * TILE)
            screen.blit(surf, (sx, sy))

        # 4) phéromones (inutiles et coûteuses en vue éloignée)
        if z >= 0.75:
            msub = w.marker[y0:y1 + 1, x0:x1 + 1]
            mys, mxs = np.nonzero(msub > 0.06)
            for j, i in zip(mys, mxs):
                col = self._clan_rgb(int(w.marker_col[y0 + j, x0 + i]))
                sz = max(5, int(22 * z * float(msub[j, i])))
                sx, sy = cam.to_screen((x0 + i) * TILE + 8, (y0 + j) * TILE + 8)
                screen.blit(self._circle(col, sz, ys_q),
                            (sx - sz / 2, sy - sz * ys_q / 2))

        # 5) tout ce qui a une profondeur, trié par y
        draws = []
        for it in w.items:
            if x0 - 1 <= it.x / TILE <= x1 + 1 and y0 - 1 <= it.y / TILE <= y1 + 1:
                draws.append((it.y, 0, self._draw_item, (it,)))
        for s in sim.sheep:
            if x0 - 1 <= s.x / TILE <= x1 + 1 and y0 - 1 <= s.y / TILE <= y1 + 1:
                draws.append((s.y, 1, self._draw_sheep, (s,)))
        for a in sim.agents:
            if a.alive and x0 - 1 <= a.x / TILE <= x1 + 1 and y0 - 1 <= a.y / TILE <= y1 + 1:
                draws.append((a.y, 2, self._draw_agent, (a, ui)))
        if draw_props:
            csub = w.content[y0:y1 + 1, x0:x1 + 1]
            cys, cxs = np.nonzero(csub >= 0)
            for j, i in zip(cys, cxs):
                draws.append(((y0 + j) * TILE + 15, 3, self._draw_asset,
                              (int(i) + x0, int(j) + y0, int(csub[j, i]), w)))
        for eff in sim.effects:
            draws.append((eff["y"] + 1, 4, self._draw_fx, (eff, sim.w.tick)))
        # cimetière : pierres tombales neutres
        for tx, ty, name, dtick, col in w.cemetery:
            if x0 - 1 <= tx <= x1 + 1 and y0 - 1 <= ty <= y1 + 1:
                draws.append(((ty) * TILE + 8, 3.5, self._draw_headstone,
                              (tx, ty, name, col)))
        draws.sort(key=lambda t: (t[0], t[1]))
        for _, _, fn, arg in draws:
            fn(screen, cam, *arg)

        # 6) ligne de quête de l'habitant sélectionné
        self._goal_line(screen, cam, ui)

        # 7) atmosphère
        box = (x0, y0, x1, y1)
        self._fires(screen, cam, w, box)
        self._night(screen, sim, cam, w, box)
        self._rain(screen, sim)

        # 8) surcouches d'interface
        if ui.get("legend"):
            self._legend(screen, view)
        if ui.get("ghost"):
            self._ghost(screen, cam, ui)
        if self.show_grid:
            self._grid_lines(screen, cam, view)

    def _visible_box(self, view, cam):
        """Rectangle de tuiles réellement couvert par le viewport.

        `cam.visible_tiles()` sous-estime la zone en vue éloignée ou en forte
        inclinaison : c'est pourquoi le terrain n'occupait qu'une partie de
        l'écran. On projette donc les quatre coins de l'écran vers le monde
        via `cam.to_world`, ce qui couvre l'écran quels que soient le zoom et
        l'angle. `visible_tiles()` sert de repli si la caméra n'expose pas
        `to_world`.
        """
        to_world = getattr(cam, "to_world", None)
        if callable(to_world):
            try:
                corners = [to_world(view.left, view.top),
                           to_world(view.right, view.top),
                           to_world(view.left, view.bottom),
                           to_world(view.right, view.bottom)]
                xs = [c[0] for c in corners]
                ys = [c[1] for c in corners]
                # marge d'une tuile : un objet ancré hors champ peut déborder
                bx0 = int(np.floor(min(xs) / TILE)) - 1
                bx1 = int(np.ceil(max(xs) / TILE)) + 1
                by0 = int(np.floor(min(ys) / TILE)) - 1
                by1 = int(np.ceil(max(ys) / TILE)) + 1
            except Exception:
                bx0, by0, bx1, by1 = cam.visible_tiles()
        else:
            bx0, by0, bx1, by1 = cam.visible_tiles()

        x0 = max(0, min(GRID - 1, int(bx0)))
        y0 = max(0, min(GRID - 1, int(by0)))
        x1 = max(x0, min(GRID - 1, int(bx1)))
        y1 = max(y0, min(GRID - 1, int(by1)))
        return x0, y0, x1, y1

    # ── terrain ──────────────────────────────────────────────────────
    def _terrain(self, screen, w, cam, x0, y0, x1, y1):
        """Dessine le heightmap via worldgen, avec cache invalidé par version."""
        gen = getattr(w, "gen", None)
        if gen is None:
            self._terrain_fallback(screen, w, cam, x0, y0, x1, y1)
            return

        py0, py1 = y0, min(GRID, y1 + 2)
        px0, px1 = x0, min(GRID, x1 + 2)
        if py1 <= py0 or px1 <= px0:
            return

        z, ys = cam.zoom, cam.ys
        tw = TILE * z
        th = TILE * z * ys
        pw, ph = px1 - px0, py1 - py0
        sw = max(1, int(round(pw * tw)))
        sh = max(1, int(round(ph * th)))

        key = (gen.version, py0, py1, px0, px1, sw, sh)
        if key != self._terrain_key:
            patch = _wg().render_patch_rgb(gen, py0, py1, px0, px1)
            h, wd = patch.shape[:2]
            # frombuffer attend (largeur, hauteur) et des lignes contiguës
            surf = pygame.image.frombuffer(
                np.ascontiguousarray(patch).tobytes(), (wd, h), "RGB")
            self._terrain_surf = pygame.transform.smoothscale(surf, (sw, sh))
            self._terrain_key = key
            gen.clear_dirty()

        # `Camera.to_screen(wx, wy)` renvoie le coin HAUT-GAUCHE de la tuile
        # (cf. camera.py : (wy - cam.y) * zoom * ys). Le patch se blitte donc
        # tel quel — la v1 soustrayait toute la hauteur du patch, ce qui le
        # projetait très au-dessus de l'écran.
        sx, sy = cam.to_screen(px0 * TILE, py0 * TILE)
        screen.blit(self._terrain_surf, (int(round(sx)), int(round(sy))))

    def _terrain_fallback(self, screen, w, cam, x0, y0, x1, y1):
        """Rendu simple quand le monde n'a pas de heightmap (monde vierge)."""
        z, ys = cam.zoom, cam.ys
        tw = TILE * z
        th = TILE * z * ys
        land = w.land[y0:y1 + 1, x0:x1 + 1]
        blocked = w.blocked[y0:y1 + 1, x0:x1 + 1]
        lys, lxs = np.nonzero(land > 0)
        for j, i in zip(lys, lxs):
            sx, sy = cam.to_screen((x0 + i) * TILE, (y0 + j) * TILE)
            col = _WALL_COL if blocked[j, i] else _LAND_COL
            pygame.draw.rect(screen, col,
                             (int(sx), int(sy), int(tw) + 1, int(th) + 1))

    # ── ligne de quête ───────────────────────────────────────────────
    def _goal_line(self, screen, cam, ui):
        ag = ui.get("agent")
        if ag is None or not getattr(ag, "alive", False):
            return
        goal = getattr(ag, "goal", None)
        if not goal or goal.get("act") in (0, 1, 13):
            return
        from .brain_api import ACTION_COLORS
        sx, sy = cam.to_screen(ag.x, ag.y)
        gx, gy = cam.to_screen(goal["x"] * TILE + 8, goal["y"] * TILE + 8)
        col = ACTION_COLORS.get(goal["act"], (255, 255, 255))
        d = ((gx - sx) ** 2 + (gy - sy) ** 2) ** 0.5
        if d <= 6:
            return
        n = max(2, int(d / TILE))
        for t in range(0, n, 2):
            a0 = t / n
            a1 = min(1.0, (t + 0.55) / n)
            pygame.draw.line(screen, col,
                             (sx + (gx - sx) * a0, sy + (gy - sy) * a0),
                             (sx + (gx - sx) * a1, sy + (gy - sy) * a1), 2)
        pygame.draw.circle(screen, col, (int(gx), int(gy)), 4, 1)

    # ══════════════════════════════════════════════════════════════════
    #  Entités
    # ══════════════════════════════════════════════════════════════════
    def _draw_asset(self, screen, cam, tx, ty, aid, world):
        am = self.am
        if not (0 <= aid < len(am.assets)):
            return
        a = am.assets[aid]
        if a.role in ("cloud", "shadow"):
            return
        frame = 0
        if a.frames > 1 and a.role == "tree":
            hp = int(world.hp[ty, tx])
            frame = max(0, min(a.frames - 1, 5 - hp))
        size = a.blocked_footprint if a.solid else 1
        cx, _ = cam.to_screen(tx * TILE + size * TILE / 2, 0)
        _, by = cam.to_screen(0, ty * TILE + size * TILE)
        surf = am.surface(aid, frame, _zq(cam.zoom))
        if a.role == "mural":
            surf = surf.copy()
            surf.set_alpha(210)
        screen.blit(surf, (cx - surf.get_width() / 2, by - surf.get_height() + 2))

    def _draw_item(self, screen, cam, it: Item):
        am = self.am
        if it.aid is None or not (0 <= it.aid < len(am.assets)):
            return
        sx, sy = cam.to_screen(it.x, it.y)
        surf = am.surface(it.aid, 0, _zq(cam.zoom * 0.7))
        screen.blit(surf, (sx - surf.get_width() / 2, sy - surf.get_height() / 2))

    def _draw_sheep(self, screen, cam, s: Sheep):
        am = self.am
        moving = abs(getattr(s, "vx", 0.0)) > 0.15
        state = "move" if moving else ("grass" if s.state == "grass" else "idle")
        aid = am.sheep.get(state) or am.sheep.get("idle")
        if aid is None:
            return
        frames = max(1, am.assets[aid].frames)
        surf = am.surface(aid, (s.anim_t // 8) % frames, _zq(cam.zoom))
        sx, sy = cam.to_screen(s.x, s.y)
        if getattr(s, "vx", 0) < -0.05:
            surf = pygame.transform.flip(surf, True, False)
        screen.blit(surf, (sx - surf.get_width() / 2, sy - surf.get_height() + 3))

    def _draw_headstone(self, screen, cam, tx, ty, name, col):
        """Pierre tombale volontairement neutre : stèle grise, sans symbole religieux."""
        sx, sy = cam.to_screen(tx * TILE + TILE / 2, ty * TILE + TILE / 2)
        z = cam.zoom
        wpx = max(4, int(10 * z))
        hpx = max(6, int(14 * z))
        rect = pygame.Rect(int(sx - wpx / 2), int(sy - hpx), wpx, hpx)
        # Socle discret
        pygame.draw.ellipse(screen, (90, 94, 92),
                            (rect.x - max(1, wpx // 4), rect.bottom - 2,
                             rect.width + max(2, wpx // 2), max(2, hpx // 4)))
        # Stèle arrondie, aucun signe/croix
        pygame.draw.rect(screen, (160, 155, 148), rect, border_radius=max(2, wpx // 2))
        pygame.draw.rect(screen, (112, 108, 104), rect, 1, border_radius=max(2, wpx // 2))
        # Trait horizontal neutre d'inscription
        if hpx >= 9:
            pygame.draw.line(screen, (122, 117, 110),
                             (rect.x + 2, rect.y + hpx // 2),
                             (rect.right - 3, rect.y + hpx // 2), 1)
        if z >= 1.2 and name:
            try:
                f = pygame.font.SysFont(None, max(8, min(12, int(9 * z))))
                txt = f.render(str(name)[:10], True, (90, 86, 82))
                screen.blit(txt, (int(sx - txt.get_width() / 2), rect.bottom + 1))
            except Exception:
                pass

    def _draw_agent(self, screen, cam, a: Inhabitant, ui):
        am = self.am
        st = {"run": "run", "attack": "attack", "work": "work", "build": "build",
              "give": "work", "eat": "work", "talk": "idle", "drink": "idle",
              "rest": "idle", "sleep": "idle"}.get(a.state, "idle")
        ids = a.states.get(st) or a.states.get("work") or a.states.get("idle")
        if not ids:
            return
        aid = ids[0]
        frames = max(1, am.assets[aid].frames)
        rate = 5 if st in ("run", "attack", "work") else 16
        surf = am.surface(aid, (a.anim_t // rate) % frames, _zq(cam.zoom))
        if a.child:
            surf = pygame.transform.smoothscale(
                surf, (max(4, int(surf.get_width() * 0.72)),
                       max(4, int(surf.get_height() * 0.72))))
        sx, sy = cam.to_screen(a.x, a.y)

        # anneau de clan sous les pieds : la carte doit se lire d'un coup d'œil
        ring = self._circle(a.rgb, max(6, int(11 * cam.zoom)), cam.ys, alpha=110)
        screen.blit(ring, (sx - ring.get_width() / 2, sy - ring.get_height() / 2 - 2))

        if a.vx < -0.05:
            surf = pygame.transform.flip(surf, True, False)
        sh = surf.get_height()
        screen.blit(surf, (sx - surf.get_width() / 2, sy - sh + 3))

        if a.tool >= 0:
            ts = am.surface(a.tool, 0, _zq(cam.zoom * 0.55))
            screen.blit(ts, (sx + surf.get_width() * 0.22, sy - sh + 1))

        if cam.zoom >= 1.0:
            cols = {"bois": (168, 118, 68), "pierre": (148, 148, 156),
                    "or": (248, 208, 98), "graine": (108, 168, 78)}
            k = 0
            yy = int(sy - sh - 3 * cam.zoom)
            rad = max(1, int(2.2 * cam.zoom))
            for mm in ("bois", "pierre", "or", "graine"):
                for _ in range(min(3, a.inv.get(mm, 0))):
                    pygame.draw.circle(screen, cols[mm],
                                       (int(sx - 9 + k * 6), yy), rad)
                    k += 1

        sel = ui.get("agent") is a
        if sel or a.health < 0.35:
            col = CLAN_COLORS.get(a.color, (255, 255, 255))
            r = max(7, int(surf.get_width() * 0.62))
            pygame.draw.circle(screen, col, (int(sx), int(sy - sh * 0.45)), r,
                               2 if sel else 1)
        if sel:
            self._mini_bars(screen, sx, sy - sh - 8 * cam.zoom, a, cam.zoom)

    def _mini_bars(self, screen, sx, sy, a, z):
        vals = [(a.energy, (108, 208, 128)),
                (1 - a.hunger, (248, 208, 98)),
                (a.health, (228, 98, 98))]
        wpx = max(10, int(28 * z))
        hpx = max(2, int(3 * z))
        for i, (v, c) in enumerate(vals):
            x, y = int(sx - wpx / 2), int(sy - i * (hpx + 2))
            pygame.draw.rect(screen, (12, 14, 20), (x, y, wpx, hpx))
            pygame.draw.rect(screen, c,
                             (x, y, int(wpx * max(0.0, min(1.0, v))), hpx))

    def _draw_fx(self, screen, cam, eff, tick):
        am = self.am
        a = am.assets[eff["aid"]]
        age = tick - eff["t0"]
        if age < 0 or age > eff["ttl"]:
            return
        frame = min(a.frames - 1, int(age * a.frames / max(1, eff["ttl"])))
        surf = am.surface(eff["aid"], frame, _zq(cam.zoom))
        sx, sy = cam.to_screen(eff["x"], eff["y"])
        screen.blit(surf, (sx - surf.get_width() / 2, sy - surf.get_height() / 2))

    # ══════════════════════════════════════════════════════════════════
    #  Atmosphère
    # ══════════════════════════════════════════════════════════════════
    def _fires(self, screen, cam, w, box):
        x0, y0, x1, y1 = box
        sub = w.fire[y0:y1 + 1, x0:x1 + 1]
        ys, xs = np.nonzero(sub > 0)
        if not len(xs):
            return
        aids = self.am.fx.get("fire") or []
        if not aids:
            return
        frames = max(1, self.am.assets[aids[0]].frames)
        zq = _zq(cam.zoom * 0.8)
        for j, i in zip(ys, xs):
            sx, sy = cam.to_screen((x0 + i) * TILE + 8, (y0 + j) * TILE + 12)
            fr = int(self.clock * 10 + i * 7 + j * 3) % frames
            s = self.am.surface(aids[0], fr, zq)
            screen.blit(s, (sx - s.get_width() / 2, sy - s.get_height()),
                        special_flags=pygame.BLEND_RGB_ADD)

    def _night(self, screen, sim, cam, w, box):
        light = sim.clock.light
        if light > 0.98:
            return
        alpha = int(165 * (1.0 - light))
        size = screen.get_clip().size or screen.get_size()
        key = (size, alpha)
        if self._night_key != key:
            dark = pygame.Surface(size, pygame.SRCALPHA)
            dark.fill((8, 10, 26, alpha))
            self._night_cache = dark
            self._night_key = key
        dark = self._night_cache.copy()
        clip = screen.get_clip()

        # trous de lumière autour des feux
        x0, y0, x1, y1 = box
        sub = w.fire[y0:y1 + 1, x0:x1 + 1]
        ys, xs = np.nonzero(sub > 0)
        rr = max(8, int(60 * cam.zoom))
        glow = self._glow(rr, alpha)
        for j, i in list(zip(ys, xs))[:40]:
            sx, sy = cam.to_screen((x0 + i) * TILE + 8, (y0 + j) * TILE + 8)
            dark.blit(glow, (sx - rr - clip.x, sy - rr - clip.y),
                      special_flags=pygame.BLEND_RGBA_SUB)
        screen.blit(dark, clip.topleft)

    def _rain(self, screen, sim):
        r = sim.clock.rain
        if r <= 0.05:
            return
        n = int(80 * r)
        clip = screen.get_clip()
        key = (clip.size, n, pygame.time.get_ticks() // 50)
        if self._rain_key != key:
            col = (150, 170, 210, int(90 * r))
            rs = pygame.Surface(clip.size, pygame.SRCALPHA)
            t = pygame.time.get_ticks()
            wd, hg = clip.size
            for k in range(n):
                x = (k * 197 + t // 2) % wd
                y = (k * 251 + t) % hg
                pygame.draw.line(rs, col, (x, y), (x - 2, y + 9), 1)
            self._rain_cache = rs
            self._rain_key = key
        screen.blit(self._rain_cache, clip.topleft)

    # ══════════════════════════════════════════════════════════════════
    #  Surcouches
    # ══════════════════════════════════════════════════════════════════
    def _legend(self, screen, view=None):
        items = [
            ((60, 180, 255), "halo = territoire (phéromones de clan)"),
            (None, "anneau sous un être = son clan"),
            ((228, 108, 48), "flammes = feu actif"),
            ((198, 168, 78), "point or = abri / construction"),
            ((46, 92, 158), "bleu = eau"),
            ((128, 118, 106), "gris = montagne infranchissable"),
        ]
        wdt, hgt = 340, 16 * len(items) + 30
        area = view if view is not None else screen.get_rect()
        sh = area.bottom
        left = area.left + 8
        panel = pygame.Surface((wdt, hgt), pygame.SRCALPHA)
        panel.fill((10, 13, 20, 238))
        pygame.draw.rect(panel, (38, 42, 52), (0, 0, wdt, hgt), 1)
        screen.blit(panel, (left, sh - hgt - 8))

        title = self._font(15, True).render("Légende — V pour masquer",
                                            True, (235, 240, 248))
        screen.blit(title, (left + 10, sh - hgt - 2))
        f = self._font(11)
        for i, (col, txt) in enumerate(items):
            y = sh - hgt + 22 + i * 16
            if col:
                pygame.draw.circle(screen, col, (left + 16, y + 5), 5)
            screen.blit(f.render(txt, True, (140, 150, 170)), (left + 28, y))

    def _ghost(self, screen, cam, ui):
        """Aperçu de l'outil courant sous le curseur."""
        tx, ty = ui["tile"]
        mode = ui.get("mode")
        aid = ui.get("asset")
        sx, sy = cam.to_screen(tx * TILE, ty * TILE)
        tw = TILE * cam.zoom
        th = TILE * cam.zoom * cam.ys

        # outils à pinceau : montrer le rayon réel, pas une case 1×1
        if mode in _BRUSH_MODES:
            r = max(1, int(ui.get("brush", 1)))
            col = _BRUSH_COLORS[mode]
            rx = int(r * tw)
            ry = max(2, int(r * th))
            rect = pygame.Rect(int(sx + tw / 2 - rx), int(sy - th / 2 - ry),
                               rx * 2, ry * 2)
            pygame.draw.ellipse(screen, col, rect, 2)
            pygame.draw.ellipse(screen, col,
                                rect.inflate(-rx, -ry), 1)
            return

        if mode == "place" and aid is not None and 0 <= aid < len(self.am.assets):
            a = self.am.assets[aid]
            surf = self.am.surface(aid, 0, _zq(cam.zoom)).copy()
            if a.role == "floor" or a.kind == "tiles":
                surf.set_alpha(175)
                screen.blit(surf, (sx, sy))
                pygame.draw.rect(screen, (138, 218, 138), (sx, sy, tw, th), 2)
                return
            sz = a.blocked_footprint if a.solid else 1
            surf.set_alpha(150)
            gx = sx + sz * tw / 2 - surf.get_width() / 2
            gy = sy + sz * th - surf.get_height()
            screen.blit(surf, (gx, gy))
            pygame.draw.rect(screen, (118, 218, 138),
                             pygame.Rect(sx, sy, sz * tw, sz * th), 2)
            return

        col = (108, 208, 128) if mode == "agent" else (78, 168, 232)
        pygame.draw.rect(screen, col, (sx, sy, tw, th), 2)

    def _grid_lines(self, screen, cam, view):
        x0, y0, x1, y1 = self._visible_box(view, cam)
        col = (0, 0, 0)
        # au-delà d'une certaine densité, la grille devient un aplat noir
        if (x1 - x0) > 160 or (y1 - y0) > 160:
            return
        for x in range(max(0, int(x0)), min(GRID, int(x1) + 1)):
            sx, _ = cam.to_screen(x * TILE, 0)
            pygame.draw.line(screen, col, (sx, view.top), (sx, view.bottom), 1)
        for y in range(max(0, int(y0)), min(GRID, int(y1) + 1)):
            _, sy = cam.to_screen(0, y * TILE)
            pygame.draw.line(screen, col, (view.left, sy), (view.right, sy), 1)


def _wg():
    """Import différé de worldgen (évite un cycle d'import au chargement)."""
    from . import worldgen
    return worldgen
