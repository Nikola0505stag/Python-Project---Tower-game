import pygame
import math
from settings import CELL_SIZE, TOWER_TYPES, DARK_GREY, WHITE, YELLOW, SELL_REFUND
from map import cell_to_pixel
from projectile import Projectile

class Tower:
    def __init__(self, tower_type, col, row):
        self.type = tower_type
        self.col = col
        self.row = row
        self.cx, self.cy = cell_to_pixel(col, row)

        data = TOWER_TYPES[tower_type]
        self.name = data['name']
        self.base_color = data['color']
        self.levels = data['levels']
        self.base_cost = data['cost']
        self.gold_spent = data['cost']
        self.level = 0
        self.can_hit_ghost = data.get('can_hit_ghost', False)

        self._fire_timer = 0.0
        self._angle = 0.0
        self._apply_level()

    def _apply_level(self):
        level = self.levels[self.level]
        self.damage = level['damage']
        self.range_cells = level['range']
        self.range_px = level['range'] * CELL_SIZE
        self.fire_rate = level['fire_rate']
        self.projectile_speed = level['projectile_speed']
        self.upgrade_cost = level['upgrade_cost']

    def can_upgrade(self):
        return self.level < len(self.levels) - 1

    def upgrade(self):
        if self.can_upgrade():
            self.gold_spent += self.upgrade_cost
            self.level += 1
            self._apply_level()
    def sell_value(self):
        return int(self.gold_spent * SELL_REFUND)

    def update(self, dt, enemy_group, projectile_group):
        self._fire_timer -= dt
        target = enemy_group.get_first_in_range(self.cx, self.cy, self.range_px, ghost_ok=self.can_hit_ghost)

        if target:
            dx = target.x - self.cx
            dy = target.y - self.cy

            self._angle = math.atan2(dy, dx)

            if self._fire_timer <= 0:
                self._fire_timer = 1.0 / self.fire_rate
                projectile = Projectile(self.cx, self.cy, target, self.damage, self.projectile_speed, self.base_color)
                projectile_group.add(projectile)

    def draw(self, surface, selected=False):
        cx, cy = self.cx, self.cy
        half = CELL_SIZE // 2 - 4

        base_rect = pygame.Rect(cx - half, cy - half, half * 2, half * 2)
        pygame.draw.rect(surface, DARK_GREY, base_rect, border_radius=4)
        pygame.draw.rect(surface, self.base_color, base_rect.inflate(-4, -4), border_radius=3)

        for i in range(self.level + 1):
            pygame.draw.circle(surface, YELLOW, (cx - half + 4 + i * 8, cy + half - 6), 3)

        barrel_len = half + 2
        end_x = cx + math.cos(self._angle) * barrel_len
        end_y = cy + math.sin(self._angle) * barrel_len
        pygame.draw.line(surface, DARK_GREY, (cx, cy), (int(end_x), int(end_y)), 6)
        pygame.draw.line(surface, WHITE, (cx, cy), (int(end_x), int(end_y)), 4)

        if selected:
            pygame.draw.rect(surface, YELLOW, base_rect.inflate(4, 4), 2, border_radius=5)

        font = pygame.font.SysFont('consolas', 11, bold=True)
        txt = font.render(self.name[0], True, WHITE)
        surface.blit(txt, txt.get_rect(center=(cx, cy)))


class TowerGroup:
    def __init__(self):
        self.towers = []

    def add(self, tower):
        self.towers.append(tower)

    def remove(self, tower):
        self.towers = [t for t in self.towers if t is not tower]

    def update(self, dt, enemy_group, projectile_group):
        for tower in self.towers:
            tower.update(dt, enemy_group, projectile_group)

    def draw(self, surface, selected_tower=None):
        for t in self.towers:
            t.draw(surface, selected=(t is selected_tower))
