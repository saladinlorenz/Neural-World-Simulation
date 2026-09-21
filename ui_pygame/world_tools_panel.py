"""World Tools Panel — panneau d'outils de terrain Pygame."""
from __future__ import annotations
import pygame
from ui_pygame.base_panel import Panel


class WorldToolsPanel(Panel):
    """Panneau d'outils monde : poser, gommer, sol, eau, terre, mur, etc."""

    TOOLS = [
        ("place", "Poser"), ("erase", "Gommer"), ("floor", "Sol"),
        ("block", "Bloc"),
        ("water", "Eau"), ("land", "Terre"), ("wall", "Mur"),
        ("carve", "Sculpter"), ("restore", "Restaurer"),
        ("inspect", "Examiner"),
    ]

    HINTS = {
        "place": "clic = poser l'asset / glisser = peindre",
        "erase": "clic = effacer les objets",
        "floor": "clic = peindre le sol",
        "water": "glisser = transformer terre en eau",
        "land": "glisser = transformer eau en terre",
        "wall": "glisser = placer des rochers",
        "carve": "glisser = creuser les montagnes",
        "restore": "glisser = restaurer le terrain",
        "block": "clic = construire un bloc",
        "inspect": "clic = examiner",
    }

    def draw(self, surface: pygame.Surface, rect: pygame.Rect,
             snapshot: dict, ui_state) -> None:
        x0, y = rect.x, rect.y
        mode = getattr(ui_state, "active_mode", "inspect")

        # Titre
        font_sub = self._font(15)
        title_surf = font_sub.render("OUTILS", True, (31, 36, 48))
        surface.blit(title_surf, (x0 + 12, y))
        y += 26

        # Grille d'outils (2 colonnes)
        font_body = self._font(13)
        col_w = (rect.width - 28) // 2
        for i, (tool_id, label) in enumerate(self.TOOLS):
            col = i % 2
            row = i // 2
            tx = x0 + 12 + col * (col_w + 4)
            ty = y + row * 30
            tr = pygame.Rect(tx, ty, col_w, 26)

            selected = mode == tool_id
            if selected:
                pygame.draw.rect(surface, (232, 240, 253), tr, border_radius=6)
                pygame.draw.rect(surface, (59, 118, 214), tr, 1, border_radius=6)
            elif tr.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(surface, (241, 244, 249), tr, border_radius=6)

            tool_surf = font_body.render(label, True, (31, 36, 48) if selected else (105, 114, 129))
            surface.blit(tool_surf, (tx + 8, ty + 4))

        y += ((len(self.TOOLS) + 1) // 2) * 30 + 10

        # Hint
        hint = self.HINTS.get(mode, "")
        if hint:
            font_small = self._font(12)
            hint_surf = font_small.render(hint, True, (105, 114, 129))
            surface.blit(hint_surf, (x0 + 12, y))
            y += 20

        # Slider pinceau (pour modes brush)
        if mode in ("water", "land", "wall", "carve", "restore"):
            y += 6
            font_small = self._font(12)
            brush_label = font_small.render(f"Taille pinceau: {getattr(ui_state, 'brush_size', 3)}",
                                            True, (105, 114, 129))
            surface.blit(brush_label, (x0 + 12, y))
            y += 20
            slider_r = pygame.Rect(x0 + 12, y, rect.width - 24, 6)
            pygame.draw.rect(surface, (237, 239, 244), slider_r, border_radius=3)
            bs = getattr(ui_state, "brush_size", 3)
            fill = max(0, min(1.0, (bs - 1) / 14))
            fill_r = pygame.Rect(slider_r.x, slider_r.y, int(slider_r.width * fill), 6)
            pygame.draw.rect(surface, (59, 118, 214), fill_r, border_radius=3)

    def handle_event(self, event: pygame.event.Event, rect: pygame.Rect,
                     ui_state) -> dict | None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            y = rect.y + 26
            col_w = (rect.width - 28) // 2
            for i, (tool_id, label) in enumerate(self.TOOLS):
                col = i % 2
                row = i // 2
                tx = rect.x + 12 + col * (col_w + 4)
                ty = y + row * 30
                tr = pygame.Rect(tx, ty, col_w, 26)
                if tr.collidepoint(event.pos):
                    if hasattr(ui_state, "active_mode"):
                        ui_state.active_mode = tool_id
                    return {"kind": "set_mode", "mode": tool_id}
        return None
