"""Editeur de pixels integre : dessine un outil dans la fenetre pygame."""
from __future__ import annotations
import os
import pygame

GRID_SIZE = 16
CELL_PX = 18
PALETTE = [
    (60, 60, 66), (120, 90, 60), (150, 150, 156), (200, 170, 90),
    (90, 140, 90), (140, 90, 160), (200, 90, 90), (230, 230, 230),
]


class ToolEditor:
    def __init__(self):
        self.pixels = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.current_color = PALETTE[0]
        self.name = "mon_outil"
        self.rect = pygame.Rect(0, 0, GRID_SIZE * CELL_PX, GRID_SIZE * CELL_PX)
        self.palette_y = 0

    def clear(self):
        self.pixels = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def paint_at(self, mx, my, erase=False):
        if not self.rect.collidepoint(mx, my):
            return False
        col = (mx - self.rect.x) // CELL_PX
        row = (my - self.rect.y) // CELL_PX
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            self.pixels[row][col] = None if erase else self.current_color
            return True
        return False

    def palette_hit(self, mx, my):
        for i, c in enumerate(PALETTE):
            r = pygame.Rect(self.rect.x + i * 26, self.palette_y, 22, 22)
            if r.collidepoint(mx, my):
                return c
        return None

    def draw(self, screen, x, y):
        self.rect.topleft = (x, y)
        pygame.draw.rect(screen, (18, 20, 26), self.rect.inflate(4, 4))
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = pygame.Rect(x + col * CELL_PX, y + row * CELL_PX,
                                    CELL_PX - 1, CELL_PX - 1)
                pygame.draw.rect(screen, self.pixels[row][col] or (30, 32, 40), cell)
        self.palette_y = y + self.rect.height + 8
        for i, c in enumerate(PALETTE):
            r = pygame.Rect(x + i * 26, self.palette_y, 22, 22)
            pygame.draw.rect(screen, c, r, border_radius=4)
            if c == self.current_color:
                pygame.draw.rect(screen, (255, 255, 255), r, 2, border_radius=4)

    def render_surface(self):
        surf = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                c = self.pixels[row][col]
                if c is not None:
                    surf.set_at((col, row), (*c, 255))
        return pygame.transform.scale(surf, (GRID_SIZE * 4, GRID_SIZE * 4))

    def save_png(self, root_dir, tool_kind):
        os.makedirs(root_dir, exist_ok=True)
        surf = self.render_surface()
        safe = "".join(ch for ch in self.name if ch.isalnum() or ch in "_-") or "outil"
        path = os.path.join(root_dir, f"{safe}_{tool_kind}.png")
        pygame.image.save(surf, path)
        return path
