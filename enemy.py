import pygame
import math
from settings import ENEMY_TYPES, DARK_GREY

class Enemy:
    def __init__(self, enemy_type, pixel_waypoints):
        data = ENEMY_TYPES[enemy_type]
        self.type = enemy_type
        self.color = data['color']
        self.size = data['size']
        self.speed = data['speed']
        self.max_hp = data['hp']
        self.hp = self.max_hp
        self.reward = data['reward']

        self.waypoints = pixel_waypoints
        self.waypoint_index = 1
        self.x = float(pixel_waypoints[0][0])
        self.y = float(pixel_waypoints[0][1])
        self.progress = 0.0

        self.alive = True
        self.reached_end = False

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False

    def update(self, dt):
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
        pygame.draw.circle(surface, self.color, (ix, iy), self.size)
        pygame.draw.circle(surface, DARK_GREY, (ix, iy), self.size, 2)

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
        for e in self.enemies:
            if not e.alive and not e.reached_end:
                gold_earned += e.reward
            elif e.alive:
                alive.append(e)
            
        self.enemies = alive
        return gold_earned

    def draw(self, surface):
        for e in self.enemies:
            e.draw(surface)

    def get_first_in_range(self, cx, cy, radius):
        best = None
        for e in self.enemies:
            if math.hypot(e.x - cx, e.y - cy) <= radius:
                if best is None or e.progress > best.progress:
                    best = e
        return best
