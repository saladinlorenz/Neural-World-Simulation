"""Base Panel — contrat commun pour tous les panneaux Pygame."""
from __future__ import annotations
import pygame


class Panel:
    """Classe de base pour les panneaux Pygame extraits du dashboard.

    Contrat :
        draw(surface, rect, snapshot, ui_state) -> None
        handle_event(event, rect, ui_state) -> command dict ou None
    """

    def __init__(self, x: int = 0, y: int = 0, w: int = 200, h: int = 400):
        self.rect = pygame.Rect(x, y, w, h)
        self._scroll_offset = 0
        self._buttons: list[pygame.Rect] = []

    def draw(self, surface: pygame.Surface, rect: pygame.Rect,
             snapshot: dict, ui_state) -> None:
        """Dessine le panneau dans la zone donnee."""
        raise NotImplementedError

    def handle_event(self, event: pygame.event.Event, rect: pygame.Rect,
                     ui_state) -> dict | None:
        """Traite un evenement. Retourne une commande dict ou None."""
        return None

    def _font(self, size: int = 13) -> pygame.font.Font:
        key = f"_{size}"
        if not hasattr(self, "_fonts"):
            self._fonts = {}
        if key not in self._fonts:
            self._fonts[key] = pygame.font.SysFont(
                "segoeui,inter,dejavusans,liberationsans,arial", size
            )
        return self._fonts[key]

    def _draw_text(self, surface, text, x, y, color=(31, 36, 48), size=13,
                   max_width=None):
        font = self._font(size)
        rendered = font.render(str(text), True, color)
        if max_width and rendered.get_width() > max_width:
            # Tronquer avec ...
            while rendered.get_width() > max_width - 20 and len(text) > 3:
                text = text[:-4] + "..."
                rendered = font.render(str(text), True, color)
        surface.blit(rendered, (x, y))
        return rendered.get_height()

    def _draw_rect(self, surface, color, rect, radius=0):
        if radius > 0:
            pygame.draw.rect(surface, color, rect, border_radius=radius)
        else:
            pygame.draw.rect(surface, color, rect)

    def _draw_bar(self, surface, x, y, w, h, value, color, bg=(237, 239, 244)):
        """Dessine une barre de progression."""
        self._draw_rect(surface, bg, pygame.Rect(x, y, w, h), radius=3)
        fill_w = max(0, min(w, int(w * max(0.0, min(1.0, value)))))
        if fill_w > 0:
            self._draw_rect(surface, color, pygame.Rect(x, y, fill_w, h), radius=3)
