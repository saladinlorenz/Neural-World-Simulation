"""Couche UI — API publique.

Seule interface que la boucle principale (main.py) utilise pour le rendu
et les entrées. Les classes internes (Renderer, Camera, ui_kit) restent
privées : elles peuvent être refactorisées librement tant que ce contrat tient.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import pygame

from game.assets_api import AssetData, get_asset
from game.brain_api import ACTION_NAMES_EXP as ACTION_NAMES

__all__ = ["init_ui", "handle_events", "draw_frame", "tooltip_for_asset"]


class UIContext:
    """État UI regroupé — Renderer + Camera."""
    def __init__(self, am):
        from game.renderer import Renderer
        from game.camera import Camera
        self.renderer = Renderer(am)
        self.camera = Camera()
        self.show_legend = False
        self.asset = 0


def init_ui(am) -> UIContext:
    return UIContext(am)


def handle_events(events: List[pygame.event.Event], ctx: UIContext, sim,
                  am) -> List[Tuple[str, Any]]:
    """Transforme les événements pygame en actions abstraites."""
    from game.camera import ZOOMS
    from game.config import LEFT_W, VIEW_W
    actions: List[Tuple[str, Any]] = []
    for ev in events:
        if ev.type == pygame.QUIT:
            actions.append(("quit", None))
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                actions.append(("quit", None))
            elif ev.key == pygame.K_SPACE:
                actions.append(("pause", None))
            elif ev.key in (pygame.K_PLUS, pygame.K_EQUALS):
                actions.append(("speed", +1))
            elif ev.key == pygame.K_MINUS:
                actions.append(("speed", -1))
            elif ev.key == pygame.K_g:
                ctx.renderer.show_grid = not ctx.renderer.show_grid
            elif ev.key == pygame.K_v:
                ctx.show_legend = not ctx.show_legend
        elif ev.type == pygame.MOUSEWHEEL:
            mx, my = pygame.mouse.get_pos()
            if LEFT_W <= mx < LEFT_W + VIEW_W:
                closest = min(range(len(ZOOMS)), key=lambda i: abs(ZOOMS[i] - ctx.camera.zoom))
                idx = max(0, min(len(ZOOMS) - 1, closest + (1 if ev.y > 0 else -1)))
                ctx.camera.set_zoom(ZOOMS[idx], anchor_screen=(mx - LEFT_W, my))
    return actions


def draw_frame(screen: pygame.Surface, ctx: UIContext, sim, cam,
               ui_state: Dict[str, Any]) -> None:
    """Dessine l'écran complet : carte du monde."""
    from game.config import SCREEN_H, VIEW_W, LEFT_W
    view = pygame.Surface((VIEW_W, SCREEN_H))
    ctx.renderer.draw(view, sim, cam, ui_state)
    screen.fill((12, 14, 20))
    screen.blit(view, (LEFT_W, 0))
    pygame.draw.line(screen, (10, 10, 14), (LEFT_W + VIEW_W - 1, 0),
                     (LEFT_W + VIEW_W - 1, SCREEN_H))


def tooltip_for_asset(surface: pygame.Surface, asset: AssetData,
                      pos: Tuple[int, int]) -> None:
    """Affiche un résumé structuré de l'asset."""
    from game.ui_kit import get_kit
    kit = get_kit()
    x, y = pos
    lines = [
        asset.label,
        f"role={asset.role} cat={asset.category}",
        f"placable={'oui' if asset.placable else 'non'} solid={asset.solid}",
        "afford: " + " ".join(asset.affordances[:5]),
    ]
    if asset.build_recipe:
        mats = ", ".join(f"{m['materiau']} x{m['quantity']}"
                         for m in asset.build_recipe["materials"])
        lines.append(f"recette: {mats}")
    for i, ln in enumerate(lines):
        kit.draw_fit(surface, "tiny", ln,
                     x + 10, y + 14 + i * 14,
                     kit.C["ink"], right=x + 250)
