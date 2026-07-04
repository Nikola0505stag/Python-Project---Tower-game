import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from map import GameMap
from enemy import Enemy, EnemyGroup

def main():
    pygame.init()
    pygame.display.set_caption('Tower Defense')
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))##, pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    game_map = GameMap(0)
    enemy_group = EnemyGroup()

    enemy_group.add(Enemy('basic', game_map.pixel_waypoints))

    while True:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        enemy_group.update(dt)
        screen.fill((0,0,0))
        game_map.draw(screen)
        enemy_group.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
