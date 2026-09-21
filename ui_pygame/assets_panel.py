"""Assets Panel — catalogue d'assets Pygame avec grille filtrable."""
from __future__ import annotations
import pygame
from ui_pygame.base_panel import Panel


class AssetsPanel(Panel):
    """Grille d'assets avec catégories, favoris, recherche."""

    CELL = 68

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search = ""
        self.category = "__all__"
        self.only_favs = False
        self.favs: list = []
        self._filtered_cache: list = []
        self._selected_idx = 0

    def set_catalog(self, am) -> None:
        """Met à jour le cache filtré à partir de l'AssetManager."""
        assets = []
        for i, a in enumerate(am.assets):
            cat = getattr(a, "category", "")
            if self.category != "__all__" and cat != self.category:
                continue
            if self.only_favs and i not in self.favs:
                continue
            if self.search:
                sl = self.search.lower()
                label = getattr(a, "label", getattr(a, "name", "")).lower()
                if sl not in label and sl not in cat.lower():
                    continue
            assets.append((i, a))
        self._filtered_cache = assets

    def draw(self, surface: pygame.Surface, rect: pygame.Rect,
             snapshot: dict, ui_state) -> None:
        """Dessine la grille d'assets."""
        x0, y = rect.x, rect.y

        # Titre
        font_sub = self._font(15)
        title_surf = font_sub.render("ASSETS", True, (31, 36, 48))
        surface.blit(title_surf, (x0 + 12, y))
        y += 26

        # Champ recherche
        sr = pygame.Rect(x0 + 8, y, rect.width - 24, 27)
        pygame.draw.rect(surface, (255, 255, 255), sr, border_radius=6)
        pygame.draw.rect(surface, (205, 210, 219), sr, 1, border_radius=6)
        font_body = self._font(13)
        search_txt = self.search or "Rechercher..."
        search_col = (31, 36, 48) if self.search else (156, 163, 176)
        search_surf = font_body.render(search_txt, True, search_col)
        surface.blit(search_surf, (sr.x + 10, sr.centery - search_surf.get_height() // 2))
        y = sr.bottom + 6

        # Region grille
        region = pygame.Rect(x0 + 8, y, rect.width - 24, rect.height - (y - rect.y) - 8)
        pygame.draw.rect(surface, (255, 255, 255), region, border_radius=6)

        cell = self.CELL
        cols = max(1, (region.width - 8) // (cell + 4))
        selected_id = getattr(ui_state, "selected_asset_id", None)

        old_clip = surface.get_clip()
        surface.set_clip(region)

        for idx, (aid, a) in enumerate(self._filtered_cache):
            col = idx % cols
            row = idx // cols
            cx = region.x + 4 + col * (cell + 4)
            cy = region.y + 4 + row * (cell + 4)
            if cy + cell > region.bottom:
                break

            r = pygame.Rect(cx, cy, cell, cell)
            # Selection
            if aid == selected_id:
                pygame.draw.rect(surface, (232, 240, 253), r, border_radius=6)
                pygame.draw.rect(surface, (59, 118, 214), r, 2, border_radius=6)
            elif r.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(surface, (241, 244, 249), r, border_radius=6)

            # Nom tronque
            font_micro = self._font(11)
            label = getattr(a, "label", getattr(a, "name", f"#{aid}"))
            if len(label) > 8:
                label = label[:7] + "."
            lbl_surf = font_micro.render(label, True, (105, 114, 129))
            surface.blit(lbl_surf, (cx + 2, cy + cell - 14))

            # Etoile favori
            if aid in self.favs:
                star = font_micro.render("*", True, (222, 160, 50))
                surface.blit(star, (cx + cell - 12, cy + 2))

        if not self._filtered_cache:
            font_body = self._font(13)
            empty = font_body.render("Aucun asset.", True, (156, 163, 176))
            surface.blit(empty, (region.centerx - empty.get_width() // 2,
                                 region.y + 36))

        surface.set_clip(old_clip)

    def handle_event(self, event: pygame.event.Event, rect: pygame.Rect,
                     ui_state) -> dict | None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Calculer la zone de la grille
            y_offset = rect.y + 26 + 33  # titre + search
            region = pygame.Rect(rect.x + 8, y_offset, rect.width - 24,
                                 rect.height - (y_offset - rect.y) - 8)
            if region.collidepoint(event.pos):
                col = (event.pos[0] - region.x - 4) // (self.CELL + 4)
                row = (event.pos[1] - region.y - 4) // (self.CELL + 4)
                cols = max(1, (region.width - 8) // (self.CELL + 4))
                idx = row * cols + col
                if 0 <= idx < len(self._filtered_cache):
                    aid, _ = self._filtered_cache[idx]
                    if hasattr(ui_state, "selected_asset_id"):
                        ui_state.selected_asset_id = aid
                    return {"kind": "select_asset", "aid": aid}
        return None
