"""Society Panel — panneau societe Pygame avec snapshots."""
from __future__ import annotations
import pygame
from ui_pygame.base_panel import Panel


class SocietyPanel(Panel):
    """Panneau de la societe avec statistiques groupees."""

    def draw(self, surface: pygame.Surface, rect: pygame.Rect,
             snapshot: dict, ui_state) -> None:
        """Dessine le panneau societe.

        snapshot doit contenir {"population", "stats", "sheep", "monsters", ...}
        """
        if isinstance(snapshot, dict):
            data = snapshot
        else:
            data = {}

        stats = data.get("stats", {})
        alive = data.get("population", 0)
        sheep = data.get("sheep", 0)
        monsters = data.get("monsters", 0)
        max_gen = data.get("max_generation", 0)
        bonded = data.get("bonded", 0)

        x0, y = rect.x, rect.y

        # Titre
        font_sub = self._font(15)
        title_surf = font_sub.render("SOCIETE", True, (31, 36, 48))
        surface.blit(title_surf, (x0 + 12, y))
        y += 26

        region = pygame.Rect(x0 + 8, y, rect.width - 24, rect.height - (y - rect.y) - 8)

        # Groupes de stats
        groups = [
            ("Demographie", (67, 160, 92), [
                ("Population", alive),
                ("Naissances", stats.get("births", 0)),
                ("Deces", stats.get("deaths", 0)),
                ("Generation max", max_gen),
                ("Couples", bonded),
            ]),
            ("Activite", (222, 164, 46), [
                ("Constructions", stats.get("builds", 0)),
                ("Villages", stats.get("villages", 0)),
                ("Recoltes", stats.get("harvests", 0)),
                ("Outils trouves", stats.get("tool_found", 0)),
            ]),
            ("Social", (146, 96, 186), [
                ("Dons", stats.get("gives", 0)),
                ("Vols", stats.get("takes", 0)),
                ("Paroles", stats.get("talks", 0)),
                ("Attaques", stats.get("attacks", 0)),
            ]),
            ("Monde", (62, 124, 214), [
                ("Feux", stats.get("fires", 0)),
                ("Moutons", sheep),
                ("Monstres", monsters),
            ]),
        ]

        old_clip = surface.get_clip()
        surface.set_clip(region)
        cy = region.y

        for title, color, rows in groups:
            h = 28 + ((len(rows) + 1) // 2) * 21 + 6
            card = pygame.Rect(region.x, cy, region.width, h)
            if card.bottom > region.bottom:
                break
            pygame.draw.rect(surface, (255, 255, 255), card, border_radius=6)
            # Accent bar
            pygame.draw.rect(surface, color, (card.x, card.y + 6, 3, 15), border_radius=2)

            # Titre groupe
            font_small = self._font(12)
            title_text = title.upper()
            # Mélanger couleur avec noir pour le texte du titre
            mixed = tuple(int(c * 0.7) for c in color)
            title_surf = font_small.render(title_text, True, mixed)
            surface.blit(title_surf, (card.x + 10, card.y + 6))

            # Rows (2 colonnes)
            colw = (card.width - 20) // 2
            font_small = self._font(12)
            font_body = self._font(13)
            for i, (lbl, val) in enumerate(rows):
                lx = card.x + 10 + (i % 2) * colw
                ly = card.y + 28 + (i // 2) * 21
                lbl_surf = font_small.render(str(lbl), True, (105, 114, 129))
                surface.blit(lbl_surf, (lx, ly))
                val_surf = font_body.render(str(val), True, (31, 36, 48))
                surface.blit(val_surf, (lx + colw - 10 - val_surf.get_width(), ly - 1))

            cy = card.bottom + 6

        surface.set_clip(old_clip)

    def handle_event(self, event: pygame.event.Event, rect: pygame.Rect,
                     ui_state) -> dict | None:
        return None
