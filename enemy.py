import pygame
import math
from settings import ENEMY_TYPES

class Enemy:
    def __init__(self, enemy_type, pixel_waypoints):
        data = ENEMY_TYPES[enemy_type]
        self.type = enemy_type
        self.color = data['color']
        self.size = data['size']
        self.speed = data['speed']

        self.waypoints = pixel_waypoints
        self.waypoint_index = 1
        self.x = float(pixel_waypoints[0][0])
        self.y = float(pixel_waypoints[0][1])

        self.alive = True
        self.reached_end = False

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

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)


class EnemyGroup:
    def __init__(self):
        self.enemies = []

    def add(self, enemy):
        self.enemies.append(enemy)

    def update(self, dt):
        for e in self.enemies:
            if e.alive:
                e.update(dt)
        self.enemies = [e for e in self.enemies if e.alive]

    def draw(self, surface):
        for e in self.enemies:
            e.draw(surface)
