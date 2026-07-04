import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from settings import GAME_WIDTH, TOWER_TYPES
from map import GameMap, pixel_to_cell
from enemy import Enemy, EnemyGroup
from tower import Tower, TowerGroup
from economy import Economy

def main():
    pygame.init()
    pygame.display.set_caption('Tower Defense')
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))##, pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    game_map = GameMap(0)
    enemy_group = EnemyGroup()
    tower_group = TowerGroup()
    economy = Economy()

    enemy_group.add(Enemy('basic', game_map.pixel_waypoints))

    while True:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if mx < GAME_WIDTH:
                    col, row = pixel_to_cell(mx, my)
                    if game_map.is_buildable(col, row):
                        cost = TOWER_TYPES['basic']['cost']
                        if economy.spend(cost):
                            t = Tower('basic', col, row)
                            game_map.place_tower(col, row, t)
                            tower_group.add(t)


        enemy_group.update(dt)
        screen.fill((0,0,0))
        game_map.draw(screen)
        tower_group.draw(screen)
        enemy_group.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
