"""ui_kit — fondations graphiques du laboratoire.

Kit 100% pygame pur, aucune dépendance externe.
  * polices Segoe UI / pygame default
  * tokens de palette PAR FAMILLE DE DONNEES
  * gestionnaire de tooltips
  * widgets : boutons, glass panels, gauges, sliders, accordion

Tout est pre-rendu / cache : la boucle 60 FPS ne fait que des blits."""
import pygame

# ---------------------------------------------------------------- tokens
C = {
    # familles de donnees
    "corps":       (235, 145, 100),
    "cognition":   (80, 200, 255),
    "personnalite": (195, 110, 255),
    "emotions":    (255, 175, 80),
    "besoins":     (80, 230, 180),
    "experience":  (255, 215, 60),
    "social":      (255, 160, 210),
    "combat":      (255, 80, 80),
    "meteo":       (120, 195, 255),
    "economie":    (255, 215, 60),
    "vie":         (80, 225, 110),
    "mort":        (200, 80, 80),
    "batiment":    (160, 240, 150),
    "monde":       (190, 210, 240),
    # chrome — warm dark palette
    "bg":     (18, 20, 26),
    "bg2":    (24, 28, 38),
    "bg3":    (12, 14, 20),
    "line":   (38, 42, 52),
    "ink":    (235, 240, 248),
    "muted":  (140, 150, 170),
    "faded":  (88, 96, 112),
    "accent": (60, 180, 255),
    "good":   (80, 220, 110),
    "bad":    (240, 80, 80),
    "gold":   (255, 210, 60),
    "darkink": (10, 12, 18),
}

SECTION_COLOR = {
    "body": C["corps"], "cog": C["cognition"], "perso": C["personnalite"],
    "emo": C["emotions"], "needs": C["besoins"], "skills": C["experience"],
}


class UiKit:
    def __init__(self):
        self._scaled = {}
        self._texts = {}
        self._glass = {}
        self._knobs = {}
        self.fonts = {}
        self._fsize = {}
        self._tips = []
        self._init_fonts()

    # ---------------------------------------------------------------- fonts
    def _init_fonts(self):
        def vec(size, bold=False):
            for fam in ("segoeui", "Segoe UI", "arial", "helvetica"):
                try:
                    f = pygame.font.SysFont(fam, size, bold=bold)
                    if f:
                        return f
                except Exception:
                    pass
            return pygame.font.Font(None, size)

        self.fonts["title"] = vec(22, bold=True)
        self.fonts["h2"] = vec(15, bold=True)
        self.fonts["h3"] = vec(13, bold=True)
        self.fonts["body"] = vec(13)
        self.fonts["small"] = vec(11)
        self.fonts["tiny"] = vec(10)
        self._ksize = {"title": 22, "h2": 15, "h3": 13, "body": 13, "small": 11, "tiny": 10}

    def font(self, kind, size=None):
        if size is None or size == self.fonts[kind].get_height():
            return self.fonts[kind]
        k = (kind, size)
        f = self._fsize.get(k)
        if f is None:
            bold = kind in ("title", "h2", "h3")
            try:
                f = pygame.font.SysFont("segoeui", size, bold=bold)
            except Exception:
                f = pygame.font.Font(None, size)
            self._fsize[k] = f
        return f

    def text(self, kind, s, color):
        k = (kind, s, color)
        v = self._texts.get(k)
        if v is None:
            v = self.fonts[kind].render(s, True, color)
            self._texts[k] = v
            if len(self._texts) > 2200:
                self._texts.clear()
                self._texts[k] = v
        return v

    def text_fit(self, kind, s, color, maxw):
        f = self.fonts[kind]
        if f.size(s)[0] <= maxw:
            return self.text(kind, s, color)
        base = self._ksize.get(kind, 13)
        for size in (base - 1, base - 2, base - 3):
            if size < 8:
                break
            bold = kind in ("title", "h2", "h3")
            try:
                f2 = pygame.font.SysFont("segoeui", size, bold=bold)
            except Exception:
                f2 = pygame.font.Font(None, size)
            if f2.size(s)[0] <= maxw:
                k = (f"{kind}@{size}", s, color)
                v = self._texts.get(k)
                if v is None:
                    v = f2.render(s, True, color)
                    self._texts[k] = v
                return v
        while s and f.size(s + "…")[0] > maxw:
            s = s[:-1]
        return self.text(kind, s + "…", color)

    def draw_fit(self, screen, kind, s, color, x, y, maxw, cy=False):
        t = self.text_fit(kind, s, color, maxw)
        yy = y - t.get_height() // 2 if cy else y
        screen.blit(t, (x, yy))
        return t.get_width()

    def draw_text(self, screen, kind, s, color, x, y, cx=False, cy=False):
        t = self.text(kind, s, color)
        if cx:
            x -= t.get_width() // 2
        if cy:
            y -= t.get_height() // 2
        screen.blit(t, (x, y))
        return t.get_rect()

    # ---------------------------------------------------------------- widgets
    BTN_PAL = {"Blue": (42, 88, 148), "Green": (42, 118, 72), "Red": (148, 48, 48),
               "Yellow": (158, 118, 38), "Grey": (38, 44, 58)}

    @staticmethod
    def _shade(col, d):
        return tuple(max(0, min(255, c + d)) for c in col)

    def _sheen(self, size):
        s = self._scaled.get(("__sheen__", size))
        if s is None:
            w, h = size
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            n = max(2, h // 2)
            for i in range(n):
                pygame.draw.line(s, (255, 255, 255, int(24 * (1 - i / n))), (0, i), (w, i))
            m = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.rect(m, (255, 255, 255, 255), (0, 0, w, h), border_radius=7)
            s.blit(m, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            self._scaled[("__sheen__", size)] = s
        return s

    def _rbtn(self, screen, rect, base, state="normal"):
        r = pygame.Rect(rect)
        if state == "disabled":
            fill, edge = (20, 24, 34), (38, 44, 58)
        elif state == "selected":
            fill, edge = self._shade(base, 28), self._shade(base, 98)
        elif state == "hover":
            fill, edge = self._shade(base, 22), self._shade(base, 72)
        elif state == "pressed":
            fill, edge = self._shade(base, -16), self._shade(base, 44)
            r.y += 1
        else:
            fill, edge = base, self._shade(base, 48)
        pygame.draw.rect(screen, fill, r, border_radius=7)
        if state != "disabled":
            screen.blit(self._sheen(r.size), r)
        pygame.draw.rect(screen, edge, r, 1, border_radius=7)
        if state == "selected":
            pygame.draw.line(screen, self._shade(edge, 44), (r.x + 6, r.y + 1),
                             (r.right - 7, r.y + 1))

    def button(self, screen, rect, state="normal"):
        self._rbtn(screen, rect, self.BTN_PAL["Grey"], state)

    def button_color(self, screen, rect, color_name, state="normal"):
        self._rbtn(screen, rect, self.BTN_PAL.get(color_name, self.BTN_PAL["Grey"]), state)

    def chip(self, screen, rect, color_name="Grey", state="normal"):
        base = self.BTN_PAL.get(color_name, self.BTN_PAL["Grey"])
        r = pygame.Rect(rect)
        fill = self._shade(base, 18) if state in ("selected", "hover") else base
        pygame.draw.rect(screen, fill, r, border_radius=r.height // 2)
        pygame.draw.rect(screen, self._shade(base, 52), r, 1, border_radius=r.height // 2)

    def input_bg(self, screen, rect, focus=False):
        r = pygame.Rect(rect)
        pygame.draw.rect(screen, (11, 14, 22), r, border_radius=8)
        pygame.draw.rect(screen, C["accent"] if focus else (44, 52, 72), r, 1, border_radius=8)
        if focus:
            ov = pygame.Surface(r.inflate(6, 6).size, pygame.SRCALPHA)
            pygame.draw.rect(ov, (*C["accent"], 42), ov.get_rect(), 2, border_radius=10)
            screen.blit(ov, r.inflate(6, 6))

    def divider(self, screen, x, y, w):
        pygame.draw.line(screen, C["line"], (x, y), (x + w, y))

    # ---------------------------------------------------------------- glass panel
    def glass(self, screen, rect, alpha=170, tint=(18, 22, 36), edge=(62, 74, 108),
              radius=10, glow=False):
        w, h = rect.size
        if w <= 0 or h <= 0:
            return
        key = (w, h, alpha, tint, edge, radius, glow)
        surf = self._glass.get(key)
        if surf is None:
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            surf.fill((*tint, alpha))
            band = pygame.Surface((w, min(h, 28)), pygame.SRCALPHA)
            for i in range(band.get_height()):
                a = int(18 * (1 - i / band.get_height()))
                pygame.draw.line(band, (190, 210, 245, a), (0, i), (w, i))
            surf.blit(band, (0, 0))
            r = pygame.Rect(0, 0, w, h)
            pygame.draw.rect(surf, (*edge, min(255, alpha + 55)), r, 1, border_radius=radius)
            if glow:
                pygame.draw.rect(surf, (*edge, 50), r.inflate(2, 2), 1, border_radius=radius + 1)
            self._glass[key] = surf
            if len(self._glass) > 90:
                self._glass.pop(next(iter(self._glass)))
        screen.blit(surf, rect)

    # ---------------------------------------------------------------- gauge bar
    def gauge(self, screen, rect, value, color, bg=(24, 28, 42), seg=None):
        v = max(0.0, min(1.0, value))
        r = pygame.Rect(rect)
        rad = r.height // 2
        pygame.draw.rect(screen, bg, r, border_radius=rad)
        fw = int(r.width * v)
        if fw >= 2:
            fill = pygame.Rect(r.x, r.y, fw, r.height)
            pygame.draw.rect(screen, color, fill, border_radius=rad)
        pygame.draw.rect(screen, tuple(min(255, c + 16) for c in bg), r, 1, border_radius=rad)

    def knob(self, screen, rect, color):
        cx, cy = rect.centerx, rect.centery
        rad = max(4, min(rect.width, rect.height) // 2)
        pygame.draw.circle(screen, (8, 10, 16), (cx, cy), rad + 1)
        pygame.draw.circle(screen, color, (cx, cy), rad)
        pygame.draw.circle(screen, tuple(min(255, c + 55) for c in color),
                           (cx - rad // 3, cy - rad // 3), max(1, rad // 3))

    def pill(self, screen, rect, color, alpha=255):
        r = pygame.Rect(rect)
        pygame.draw.rect(screen, (*color[:3], alpha), r, border_radius=r.height // 2)

    def slider(self, screen, rect, value, color, dragging=False, locked=False,
               hover=False):
        base = C["faded"] if locked else color
        tr = pygame.Rect(rect)
        h = 7 if not dragging else 9
        tr.y += (rect.height - h) // 2
        tr.height = h
        if locked:
            self.gauge(screen, tr, value, (52, 57, 72))
            self.lock(screen, tr.centerx - 5, tr.centery - 6, (120, 126, 140))
            return
        self.gauge(screen, tr, value, base)
        hx = tr.x + int(tr.width * max(0.0, min(1.0, value)))
        hs = 15 if not dragging else 19
        if hover or dragging:
            self.knob(screen, pygame.Rect(hx - hs // 2, rect.centery - hs // 2, hs, hs), base)
        else:
            pygame.draw.circle(screen, (208, 218, 232), (hx, rect.centery), 4)
            pygame.draw.circle(screen, (18, 22, 32), (hx, rect.centery), 2)

    def accordion_header(self, screen, rect, label, color, open_, hovered,
                         count=0, avg=None):
        r = pygame.Rect(rect)
        # fond de section coloré selon l'état
        if open_:
            bgc = self._shade(color, -140) if hovered else self._shade(color, -160)
        else:
            bgc = (28, 32, 44) if hovered else (22, 26, 36)
        pygame.draw.rect(screen, bgc, r, border_radius=6)
        # accent gauche coloré (large)
        pygame.draw.rect(screen, color, (r.x + 2, r.y + 2, 4, r.height - 4), border_radius=2)
        # chevron
        cx, cy = r.x + 16, r.centery
        if open_:
            pts = [(cx - 4, cy - 2), (cx + 4, cy - 2), (cx, cy + 3)]
        else:
            pts = [(cx - 2, cy - 4), (cx + 3, cy), (cx - 2, cy + 4)]
        pygame.draw.polygon(screen, color if hovered else C["muted"], pts)
        # titre
        tw = self.draw_fit(screen, "h3", label.upper(),
                           C["ink"] if open_ else C["muted"],
                           r.x + 26, r.y + (r.height - self.fonts["h3"].get_height()) // 2 + 1,
                           r.width - 90)
        # moyenne quand replie
        x = r.x + 30 + tw
        if not open_ and avg is not None:
            gr = pygame.Rect(0, 0, 60, 5)
            gr.centery = r.centery
            gr.x = min(r.right - 68, x + 12)
            self.gauge(screen, gr, avg, color)
        # compteur
        pg = pygame.Rect(r.right - 30, r.centery - 8, 22, 16)
        pygame.draw.rect(screen, (14, 18, 28), pg, border_radius=8)
        self.draw_text(screen, "tiny", str(count), C["faded"], pg.x + 11, pg.centery,
                       cx=True, cy=True)

    def section_header(self, screen, rect, label, color, open_=True):
        self.accordion_header(screen, rect, label, color, open_, False)

    def arrow(self, screen, rect, direction, color=None):
        c = color or C["muted"]
        cx, cy = rect.centerx, rect.centery
        s = min(rect.width, rect.height) // 3
        if direction == "s":
            pts = [(cx - s, cy - s // 2), (cx + s, cy - s // 2), (cx, cy + s)]
        elif direction == "e":
            pts = [(cx - s // 2, cy - s), (cx + s, cy), (cx - s // 2, cy + s)]
        elif direction == "n":
            pts = [(cx - s, cy + s // 2), (cx + s, cy + s // 2), (cx, cy - s)]
        else:
            pts = [(cx + s // 2, cy - s), (cx - s, cy), (cx + s // 2, cy + s)]
        pygame.draw.polygon(screen, c, pts)

    def star(self, screen, rect, filled):
        c = C["gold"] if filled else C["faded"]
        cx, cy = rect.centerx, rect.centery
        r = min(rect.width, rect.height) // 2 - 1
        pts = []
        for i in range(5):
            import math
            a = math.radians(-90 + i * 72)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
            a2 = math.radians(-90 + i * 72 + 36)
            pts.append((cx + r * 0.4 * math.cos(a2), cy + r * 0.4 * math.sin(a2)))
        pygame.draw.polygon(screen, c, pts)
        if not filled:
            pygame.draw.polygon(screen, C["line"], pts, 1)

    def lock(self, screen, x, y, color=(240, 160, 150)):
        s = pygame.Surface((10, 12), pygame.SRCALPHA)
        pygame.draw.rect(s, (255, 255, 255), (0, 5, 10, 7), border_radius=2)
        pygame.draw.arc(s, (255, 255, 255), (2, 0, 6, 8), 0.2, 2.94, 2)
        s.fill((*color, 255), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(s, (x, y))

    def dot(self, screen, cx, cy, color, r=4, ring=None):
        pygame.draw.circle(screen, color, (cx, cy), r)
        if ring:
            pygame.draw.circle(screen, ring, (cx, cy), r, 1)

    def icon(self, screen, rect, icon_name, color="Grey"):
        c = self.BTN_PAL.get(color, C["muted"])
        cx, cy = rect.centerx, rect.centery
        s = min(rect.width, rect.height) // 3
        if "check" in icon_name:
            pygame.draw.lines(screen, c, False, [(cx - s, cy), (cx - s // 3, cy + s), (cx + s, cy - s)], 2)
        elif "cross" in icon_name:
            pygame.draw.line(screen, c, (cx - s, cy - s), (cx + s, cy + s), 2)
            pygame.draw.line(screen, c, (cx + s, cy - s), (cx - s, cy + s), 2)
        elif "circle" in icon_name:
            pygame.draw.circle(screen, c, (cx, cy), s)
        else:
            pygame.draw.rect(screen, c, rect.inflate(-6, -6), border_radius=3)

    def check(self, screen, rect, checked=False, color="Blue"):
        r = pygame.Rect(rect)
        pygame.draw.rect(screen, C["bg2"], r, border_radius=3)
        pygame.draw.rect(screen, C["line"], r, 1, border_radius=3)
        if checked:
            c = self.BTN_PAL.get(color, C["accent"])
            cx, cy = r.centerx, r.centery
            s = min(r.width, r.height) // 3
            pygame.draw.lines(screen, c, False,
                              [(cx - s, cy), (cx - s // 3, cy + s), (cx + s, cy - s)], 2)

    # ---------------------------------------------------------------- tooltips
    def tip(self, rect, lines):
        self._tips.append((rect, lines))

    def draw_tips(self, screen, mouse):
        if not self._tips:
            return
        for rect, lines in self._tips:
            if not rect.collidepoint(mouse):
                continue
            wdt = max(self.fonts["small"].size(s)[0] for s in lines) + 16
            hgt = 6 + 14 * len(lines)
            x = min(mouse[0] + 14, screen.get_width() - wdt - 4)
            y = min(mouse[1] + 16, screen.get_height() - hgt - 4)
            panel = pygame.Surface((wdt, hgt), pygame.SRCALPHA)
            pygame.draw.rect(panel, (10, 13, 22, 245), (0, 0, wdt, hgt), border_radius=7)
            pygame.draw.rect(panel, (*C["line"], 255), (0, 0, wdt, hgt), 1, border_radius=7)
            pygame.draw.line(panel, (255, 255, 255, 22), (6, 1), (wdt - 7, 1))
            screen.blit(panel, (x, y))
            for i, s in enumerate(lines):
                col = C["ink"] if i == 0 else C["muted"]
                self.draw_text(screen, "small", s, col, x + 8, y + 4 + i * 14)
        self._tips.clear()


_KIT = None


def get_kit():
    global _KIT
    if _KIT is None:
        _KIT = UiKit()
    return _KIT
