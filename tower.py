import pygame
import math
from settings import CELL_SIZE, TOWER_TYPES, DARK_GREY, WHITE, YELLOW
from map import cell_to_pixel

class Tower:
    def __init__(self, tower_type, col, row):
        self.type = tower_type
        self.col = col
        self.row = row
        self.cx, self.cy = cell_to_pixel(col, row)

        data = TOWER_TYPES[tower_type]
        self.name = data['name']
        self.base_color = data['color']
        self.cost = data['cost']
        self._angle = 0.0

    def draw(self, surface):
        cx, cy = self.cx, self.cy
        half = CELL_SIZE // 2 - 4

        base_rect = pygame.Rect(cx - half, cy - half, half * 2, half * 2)
        pygame.draw.rect(surface, DARK_GREY, base_rect, border_radius=4)
        pygame.draw.rect(surface, self.base_color, base_rect.inflate(-4, -4), border_radius=3)

        font = pygame.font.SysFont('consolas', 11, bold=True)
        txt = font.render(self.name[0], True, WHITE)
        surface.blit(txt, txt.get_rect(center=(cx, cy)))


class TowerGroup:
    def __init__(self):
        self.towers = []

    def add(self, tower):
        self.towers.append(tower)

    def draw(self, surface):
        for t in self.towers:
            t.draw(surface)
