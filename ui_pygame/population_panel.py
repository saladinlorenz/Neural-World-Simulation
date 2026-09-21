"""Population Panel — panneau habitants Pygame avec snapshots."""
from __future__ import annotations
import pygame
from ui_pygame.base_panel import Panel


class PopulationPanel(Panel):
    """Panneau de la liste des habitants avec selection et suppression."""

    ROW_H = 38

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search = ""
        self.hdel_pending = None
        self._filtered_cache = []
        self._filter_hash = None

    def draw(self, surface: pygame.Surface, rect: pygame.Rect,
             snapshot: dict, ui_state) -> None:
        """Dessine le panneau habitants.

        snapshot doit contenir une liste d'agents OU {"population": [...]}.
        """
        if isinstance(snapshot, list):
            people = snapshot
        else:
            people = snapshot.get("population", [])

        # Filtrage par recherche
        if self.search:
            sl = self.search.lower()
            people = [a for a in people if sl in a.get("nom", "").lower()
                      or sl in a.get("clan", "").lower()
                      or sl in a.get("classe", "").lower()]

        selected_eid = getattr(ui_state, "selected_agent_eid", None)

        x0, y = rect.x, rect.y

        # Titre + compteur
        font_sub = self._font(15)
        title_surf = font_sub.render("HABITANTS", True, (31, 36, 48))
        surface.blit(title_surf, (x0 + 12, y))
        font_small = self._font(12)
        alive_count = len([a for a in people if a.get("vivant", True)])
        count_surf = font_small.render(f"{alive_count}", True, (105, 114, 129))
        surface.blit(count_surf, (rect.right - 20 - count_surf.get_width(), y + 2))
        y += 24

        # Champ de recherche
        sr = pygame.Rect(x0 + 8, y, rect.width - 24, 27)
        pygame.draw.rect(surface, (255, 255, 255), sr, border_radius=6)
        border_col = (59, 118, 214) if hasattr(ui_state, '_hab_focus') and ui_state._hab_focus else (205, 210, 219)
        pygame.draw.rect(surface, border_col, sr, 1, border_radius=6)
        font_body = self._font(13)
        display_search = self.search or "filtrer par nom, clan, classe..."
        search_col = (31, 36, 48) if self.search else (156, 163, 176)
        search_surf = font_body.render(display_search, True, search_col)
        surface.blit(search_surf, (sr.x + 10, sr.centery - search_surf.get_height() // 2))
        y = sr.bottom + 6

        # Region scrollable
        region = pygame.Rect(x0 + 8, y, rect.width - 24, rect.height - (y - rect.y) - 8)
        pygame.draw.rect(surface, (255, 255, 255), region, border_radius=6)

        rh = self.ROW_H
        off = self._scroll_offset
        old_clip = surface.get_clip()
        surface.set_clip(region)

        first = max(0, off // rh)
        mouse = pygame.mouse.get_pos()

        for i in range(first, min(len(people), first + region.height // rh + 2)):
            ag = people[i]
            eid = ag.get("eid")
            rr = pygame.Rect(region.x + 4, region.y + 4 + i * rh - off,
                             region.width - 8, rh - 2)

            # Surbrillance
            if eid == selected_eid:
                pygame.draw.rect(surface, (232, 240, 253), rr, border_radius=6)
            elif rr.collidepoint(mouse):
                pygame.draw.rect(surface, (241, 244, 249), rr, border_radius=6)

            # Nom + sexe
            font_body = self._font(13)
            name_text = f"{ag.get('nom', '?')} ({ag.get('sex', '?')})"
            name_surf = font_body.render(name_text, True, (31, 36, 48))
            surface.blit(name_surf, (rr.x + 28, rr.y + 5))

            # Infos
            font_micro = self._font(11)
            stage = ag.get("stage", "")
            age = ag.get("age_ans", 0)
            cls = ag.get("classe", "")
            info_text = f"{stage} . {age:.1f} ans . {cls}"
            info_surf = font_micro.render(info_text, True, (105, 114, 129))
            surface.blit(info_surf, (rr.x + 28, rr.y + 21))

            # Barres mini
            gx = rr.right - 130
            for j, (val, col) in enumerate([
                (ag.get("sante", 0), (67, 160, 92)),
                (ag.get("energie", 0), (222, 160, 50)),
                (1 - ag.get("faim", 0), (34, 158, 142)),
            ]):
                self._draw_bar(surface, gx + j * 34, rr.centery - 3, 30, 6, val, col)

            # Bouton supprimer
            dr = pygame.Rect(rr.right - 52, rr.centery - 10, 36, 20)
            if self.hdel_pending == eid:
                pygame.draw.rect(surface, (214, 84, 84), dr, border_radius=4)
                del_text = font_micro.render("OK?", True, (255, 255, 255))
                surface.blit(del_text, (dr.centerx - del_text.get_width() // 2,
                                        dr.centery - del_text.get_height() // 2))
            else:
                bg = (235, 100, 100) if dr.collidepoint(mouse) else (214, 84, 84)
                pygame.draw.rect(surface, bg, dr, border_radius=4)
                del_text = font_micro.render("X", True, (255, 255, 255))
                surface.blit(del_text, (dr.centerx - del_text.get_width() // 2,
                                        dr.centery - del_text.get_height() // 2))

        if not people:
            font_body = self._font(13)
            empty_surf = font_body.render("Aucun habitant ne correspond.", True, (156, 163, 176))
            surface.blit(empty_surf, (region.centerx - empty_surf.get_width() // 2,
                                      region.y + 36))

        surface.set_clip(old_clip)

    def handle_event(self, event: pygame.event.Event, rect: pygame.Rect,
                     ui_state) -> dict | None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Verifier clic sur un agent
            x0, y = rect.x, rect.y
            sr = pygame.Rect(x0 + 8, y + 24, rect.width - 24, 27)
            region = pygame.Rect(x0 + 8, sr.bottom + 6, rect.width - 24,
                                 rect.height - (sr.bottom + 6 - rect.y) - 8)

            if region.collidepoint(event.pos):
                idx = (event.pos[1] - region.y + self._scroll_offset) // self.ROW_H
                if 0 <= idx < len(self._filtered_cache):
                    ag = self._filtered_cache[idx]
                    eid = ag.get("eid")

                    # Verifier bouton supprimer
                    rr = pygame.Rect(region.x + 4, region.y + 4 + idx * self.ROW_H - self._scroll_offset,
                                     region.width - 8, self.ROW_H - 2)
                    dr = pygame.Rect(rr.right - 52, rr.centery - 10, 36, 20)
                    if dr.collidepoint(event.pos):
                        if self.hdel_pending == eid:
                            self.hdel_pending = None
                            return {"kind": "remove_agent", "eid": eid}
                        else:
                            self.hdel_pending = eid
                            return None
                    else:
                        self.hdel_pending = None
                        if hasattr(ui_state, "selected_agent_eid"):
                            ui_state.selected_agent_eid = eid
                        return {"kind": "select_agent", "eid": eid}

            # Verifier champ de recherche
            if sr.collidepoint(event.pos):
                if hasattr(ui_state, '_hab_focus'):
                    ui_state._hab_focus = True
                return None

        if event.type == pygame.KEYDOWN:
            if hasattr(ui_state, '_hab_focus') and ui_state._hab_focus:
                if event.key == pygame.K_BACKSPACE:
                    self.search = self.search[:-1]
                    return None
                elif event.key == pygame.K_RETURN:
                    if hasattr(ui_state, '_hab_focus'):
                        ui_state._hab_focus = False
                    return None
                elif event.unicode and event.unicode.isprintable():
                    self.search += event.unicode
                    return None

        return None
