import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from settings import GAME_WIDTH, TOWER_TYPES
from map import GameMap, pixel_to_cell
from enemy import Enemy, EnemyGroup
from tower import Tower, TowerGroup
from projectile import ProjectileGroup
from economy import Economy
from wave_manager import WaveManager

def main():
    pygame.init()
    pygame.display.set_caption('Tower Defense')
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))##, pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    game_map = GameMap(0)
    enemy_group = EnemyGroup()
    tower_group = TowerGroup()
    projectile_group = ProjectileGroup()
    economy = Economy()
    wave_mgr = WaveManager(game_map.pixel_waypoints, enemy_group)

    game_over = False
    font = pygame.font.SysFont('consolas', 28, bold=True)

    while True:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if mx < GAME_WIDTH:
                    col, row = pixel_to_cell(mx, my)
                    if game_map.is_buildable(col, row):
                        cost = TOWER_TYPES['basic']['cost']
                        if economy.spend(cost):
                            t = Tower('basic', col, row)
                            game_map.place_tower(col, row, t)
                            tower_group.add(t)

        if not game_over:
            wave_mgr.update(dt)
            gold_earned, lives_lost = enemy_group.update(dt)
            economy.earn(gold_earned)
            economy.lose_life(lives_lost)
            tower_group.update(dt, enemy_group, projectile_group)
            projectile_group.update(dt)

            if economy.is_game_over():
                game_over = True

        
        screen.fill((0,0,0))
        game_map.draw(screen)
        tower_group.draw(screen)
        enemy_group.draw(screen)
        projectile_group.draw(screen)

        txt = font.render(
                f'Gold: {economy.gold}   Lives: {economy.lives}   Wave: {wave_mgr.wave_number}',
                True, (255, 215, 0)
                )
        screen.blit(txt, (10, 10))

        if game_over:
            msg = font.render('GAME OVER', True, (220, 40, 40))
            screen.blit(msg, (GAME_WIDTH // 2 - msg.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()


if __name__ == '__main__':
    main()
