"""Journal Panel — panneau journal Pygame avec snapshots."""
from __future__ import annotations
import pygame
from ui_pygame.base_panel import Panel
from game.ui_registry import LOG_CATS, LOG_TITLES


class JournalPanel(Panel):
    """Panneau journal filtrable, affiche les entrees de sim.journal."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jfilter = "tous"
        self._font_cache: dict = {}

    def draw(self, surface: pygame.Surface, rect: pygame.Rect,
             snapshot: dict, ui_state) -> None:
        """Dessine le panneau journal.

        snapshot doit contenir {"journal": [...]} ou la liste d'entrees.
        """
        entries = snapshot if isinstance(snapshot, list) else snapshot.get("journal", [])

        # Filtre
        if self.jfilter != "tous":
            entries = [e for e in entries if e.get("category") == self.jfilter]

        x0, y = rect.x, rect.y

        # Titre
        font_sub = self._font(15)
        title_surf = font_sub.render("JOURNAL", True, (31, 36, 48))
        surface.blit(title_surf, (x0 + 12, y))
        y += 26

        # Chips de categorie
        fx, fy = x0 + 8, y
        for cid in ["tous"] + list(LOG_CATS.keys()):
            col = (105, 114, 129) if cid == "tous" else LOG_CATS[cid]
            lbl = "tous" if cid == "tous" else LOG_TITLES.get(cid, cid)
            font_micro = self._font(11)
            cw = font_micro.size(lbl)[0] + 16
            if fx + cw > rect.right - 12:
                fx, fy = x0 + 12, fy + 23
            chip_rect = pygame.Rect(fx, fy, cw, 19)
            selected = self.jfilter == cid
            if selected:
                pygame.draw.rect(surface, col, chip_rect, border_radius=6)
                txt_col = (255, 255, 255)
            else:
                pygame.draw.rect(surface, (255, 255, 255), chip_rect, border_radius=6)
                pygame.draw.rect(surface, col, chip_rect, 1, border_radius=6)
                txt_col = col
            chip_text = font_micro.render(lbl, True, txt_col)
            surface.blit(chip_text, (fx + 8, fy + 3))
            fx += cw + 4

            # Stocker la zone du chip pour le clic
            if not hasattr(self, "_chips"):
                self._chips = []
            self._chips.append((chip_rect, cid))
        y = fy + 27

        # Liste des entrees
        region = pygame.Rect(x0 + 8, y, rect.width - 24, rect.height - (y - rect.y) - 8)
        pygame.draw.rect(surface, (255, 255, 255), region, border_radius=6)

        rh = 23
        shown = entries[-max(1, region.height // rh):]
        old_clip = surface.get_clip()
        surface.set_clip(region)

        for i, e in enumerate(shown):
            tick = e.get("tick", 0)
            text = e.get("text", "")
            cat = e.get("category", "monde")
            count = e.get("count", 1)
            ry = region.y + 6 + i * rh

            # Point de couleur
            color = LOG_CATS.get(cat, (105, 114, 129))
            pygame.draw.circle(surface, color, (region.x + 12, ry + 8), 4)

            # Timestamp
            import config as _cfg
            mm, ss = divmod(int(tick / getattr(_cfg, "SIM_HZ", 60)), 60)
            font_micro = self._font(11)
            ts_surf = font_micro.render(f"{mm:02}:{ss:02}", True, (156, 163, 176))
            surface.blit(ts_surf, (region.x + 27, ry + 2))

            # Texte
            font_small = self._font(12)
            display_text = text + (f"  x{count}" if count and count > 1 else "")
            # Tronquer si trop long
            max_w = region.width - 80
            while font_small.size(display_text)[0] > max_w and len(display_text) > 5:
                display_text = display_text[:-4] + "..."
            txt_surf = font_small.render(display_text, True, (31, 36, 48))
            surface.blit(txt_surf, (region.x + 68, ry + 1))

        if not shown:
            font_body = self._font(13)
            empty_surf = font_body.render("Rien a signaler pour ce filtre.", True, (156, 163, 176))
            surface.blit(empty_surf, (region.centerx - empty_surf.get_width() // 2,
                                      region.y + 36))

        surface.set_clip(old_clip)

    def handle_event(self, event: pygame.event.Event, rect: pygame.Rect,
                     ui_state) -> dict | None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not hasattr(self, "_chips"):
                return None
            for chip_rect, cid in self._chips:
                if chip_rect.collidepoint(event.pos):
                    self.jfilter = cid
                    if hasattr(ui_state, "journal_filter"):
                        ui_state.journal_filter = cid
                    return {"kind": "set_journal_filter", "filter": cid}
        return None
