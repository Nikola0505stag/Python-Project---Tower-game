import pygame
import math

class Projectile:
    def __init__(self, x, y, target, damage, speed, color):
        self.x = float(x)
        self.y=  float(y)
        self.target = target
        self.damage = damage
        self.speed = speed
        self.color = color
        self.alive = True

    def update(self, dt):
        if not self.target.alive:
            self.alive = False
            return

        tx = self.target.x
        ty = self.target.y
        dx = tx - self.x
        dy = ty - self.y
        dist = math.hypot(dx, dy)
        move = self.speed * dt

        if dist <= move:
            self.target.take_damage(self.damage)
            self.alive = False
        else:
            self.x += dx / dist * move
            self.y += dy / dist * move

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 5)

class ProjectileGroup:
    def __init__(self):
        self.projectiles = []

    def add(self, projectile):
        self.projectiles.append(projectile)

    def update(self, dt):
        for projectile in self.projectiles:
            if projectile.alive:
                projectile.update(dt)
        self.projectiles = [projectile for projectile in self.projectiles if projectile.alive]

    def draw(self, surface):
        for projectile in self.projectiles:
            projectile.draw(surface)
