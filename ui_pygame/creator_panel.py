"""Creator Panel — panneau création d'outils Pygame."""
from __future__ import annotations
import pygame
from ui_pygame.base_panel import Panel


class CreatorPanel(Panel):
    """Panneau de création d'outils personnalisés."""

    def draw(self, surface: pygame.Surface, rect: pygame.Rect,
             snapshot: dict, ui_state) -> None:
        x0, y = rect.x, rect.y

        # Titre
        font_sub = self._font(15)
        title_surf = font_sub.render("CREER UN OUTIL", True, (31, 36, 48))
        surface.blit(title_surf, (x0 + 12, y))
        font_small = self._font(12)
        subtitle = font_small.render("dessine, nomme, choisis un type, puis equipe l'etre selectionne",
                                     True, (105, 114, 129))
        surface.blit(subtitle, (x0 + 12, y + 18))
        y += 40

        # Zone de dessin (placeholder)
        draw_r = pygame.Rect(x0 + 12, y, rect.width - 24, 120)
        pygame.draw.rect(surface, (250, 251, 253), draw_r, border_radius=6)
        pygame.draw.rect(surface, (205, 210, 219), draw_r, 1, border_radius=6)
        font_body = self._font(13)
        placeholder = font_body.render("Zone de dessin (ToolEditor)", True, (156, 163, 176))
        surface.blit(placeholder, (draw_r.centerx - placeholder.get_width() // 2,
                                   draw_r.centery - placeholder.get_height() // 2))
        y = draw_r.bottom + 10

        # Champ nom
        name_r = pygame.Rect(x0 + 12, y, rect.width - 24, 28)
        pygame.draw.rect(surface, (255, 255, 255), name_r, border_radius=6)
        pygame.draw.rect(surface, (205, 210, 219), name_r, 1, border_radius=6)
        name_surf = font_body.render("Nom de l'outil...", True, (156, 163, 176))
        surface.blit(name_surf, (name_r.x + 8, name_r.centery - name_surf.get_height() // 2))
        y = name_r.bottom + 8

        # Types
        font_small = self._font(12)
        type_label = font_small.render("TYPE", True, (105, 114, 129))
        surface.blit(type_label, (x0 + 12, y))
        y += 18
        for i, kind in enumerate(("hache", "pioche", "marteau")):
            r = pygame.Rect(x0 + 12 + i * 74, y, 68, 22)
            pygame.draw.rect(surface, (255, 255, 255), r, border_radius=6)
            pygame.draw.rect(surface, (205, 210, 219), r, 1, border_radius=6)
            kind_surf = font_small.render(kind, True, (105, 114, 129))
            surface.blit(kind_surf, (r.centerx - kind_surf.get_width() // 2,
                                     r.centery - kind_surf.get_height() // 2))
        y += 30

        # Bouton creer
        btn_r = pygame.Rect(x0 + 12, y, rect.width - 24, 32)
        pygame.draw.rect(surface, (59, 118, 214), btn_r, border_radius=6)
        btn_text = font_body.render("Creer et equiper", True, (255, 255, 255))
        surface.blit(btn_text, (btn_r.centerx - btn_text.get_width() // 2,
                                btn_r.centery - btn_text.get_height() // 2))

    def handle_event(self, event: pygame.event.Event, rect: pygame.Rect,
                     ui_state) -> dict | None:
        return None
