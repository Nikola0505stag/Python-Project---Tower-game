import pygame
import math
from settings import ENEMY_TYPES, DARK_GREY

class Enemy:
    def __init__(self, enemy_type, pixel_waypoints, hp_multiplier=1.0, speed_multiplier=1.0):
        data = ENEMY_TYPES[enemy_type]
        self.type = enemy_type
        self.color = data['color']
        self.size = data['size']
        self.base_speed = data['speed'] * speed_multiplier
        self.speed = self.base_speed
        self.max_hp = int(data['hp'] * hp_multiplier)
        self.hp = self.max_hp
        self.reward = data['reward']
        self.armor = data.get('armor', 0)
        self.regen_rate = data.get('regen', 0)
        self.splits = data.get('splits', False)
        self.is_ghost = data.get('ghost', False)

        self.waypoints = pixel_waypoints
        self.waypoint_index = 1
        self.x = float(pixel_waypoints[0][0])
        self.y = float(pixel_waypoints[0][1])
        self.progress = 0.0

        self.alive = True
        self.reached_end = False

    def take_damage(self, amount):
        actual = max(1, amount - self.armor)
        self.hp -= actual
        if self.hp <= 0:
            self.alive = False

    def update(self, dt):
        if self.regen_rate > 0 and self.hp < self.max_hp:
            self.hp = min(self.max_hp, self.hp + self.regen_rate *dt)

        if self.waypoint_index >= len(self.waypoints):
            self.reached_end = True
            self.alive = False
            return

        tx, ty = self.waypoints[self.waypoint_index]
        dx = tx - self.x
        dy = ty - self.y
        dist = math.hypot(dx, dy)
        move = self.speed * dt

        if dist <= move:
            self.x, self.y = tx, ty
            self.waypoint_index += 1
        else:
            self.x += dx / dist * move
            self.y += dy / dist * move

        self.progress += move

    def draw(self, surface):
        ix, iy = int(self.x), int(self.y)
        
        if self.is_ghost:
            s = pygame.Surface((self.size * 2 + 4, self.size * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, 140), (self.size + 2, self.size + 2), self.size)
            surface.blit(s, (ix - self.size -2, iy - self.size - 2))
        else:
            pygame.draw.circle(surface, self.color, (ix, iy), self.size)
            pygame.draw.circle(surface, DARK_GREY, (ix, iy), self.size, 2)

        if self.armor > 0:
            pygame.draw.circle(surface, (180, 180, 180), (ix, iy), self.size, 3)

        if self.regen_rate > 0 and self.hp < self.max_hp:
            pygame.draw.circle(surface, (60, 220, 80), (ix, iy), self.size + 2, 2)

        bar_w = self.size * 2
        bar_x = ix - self.size
        bar_y = iy - self.size - 8
        ratio = max(0, self.hp / self.max_hp)
        pygame.draw.rect(surface, (80, 0, 0), (bar_x, bar_y, bar_w, 5))
        pygame.draw.rect(surface, (50, 200, 50), (bar_x, bar_y, int(bar_w * ratio), 5))


class EnemyGroup:
    def __init__(self):
        self.enemies = []

    def add(self, enemy):
        self.enemies.append(enemy)

    def update(self, dt):
        for e in self.enemies:
            if e.alive:
                e.update(dt)

        gold_earned = 0
        alive = []
        lives_lost = 0
        killed = []
        spawns = []

        for e in self.enemies:
            if not e.alive:
                if e.reached_end:
                    lives_lost += 1
                else:
                    gold_earned += e.reward
                    killed.append(e)
                    if e.splits:
                        for _ in range(2):
                            mini = Enemy('mini', e.waypoints)
                            mini.x = e.x
                            mini.y = e.y
                            mini.waypoint_index = e.waypoint_index
                            mini.progress = e.progress
                            spawns.append(mini)
            else:
                alive.append(e)
            
        self.enemies = alive + spawns
        return gold_earned, lives_lost, killed

    def draw(self, surface):
        for e in self.enemies:
            e.draw(surface)

    def get_first_in_range(self, cx, cy, radius, ghost_ok=True):
        best = None
        for e in self.enemies:
            if e.is_ghost and not ghost_ok:
                continue
            if math.hypot(e.x - cx, e.y - cy) <= radius:
                if best is None or e.progress > best.progress:
                    best = e
        return best

    def is_empty(self):
        return len(self.enemies) == 0
