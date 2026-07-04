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
from ui import Panel

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
    panel = Panel()

    selected_type = 'basic'
    speed_multiplier = 1
    game_over = False
    font = pygame.font.SysFont('consolas', 28, bold=True)

    while True:
        dt = clock.tick(FPS) / 1000.0
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            actions = panel.handle_event(event, economy, wave_mgr)
            if 'select_type' in actions:
                selected_type = actions['select_type']
            if 'send_wave' in actions:
                wave_mgr.skip_wait()
            if 'toggle_speed' in actions:
                speed_multiplier = 1 if speed_multiplier > 1 else 2

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
            eff_dt = dt * speed_multiplier
            wave_mgr.update(eff_dt)
            gold_earned, lives_lost = enemy_group.update(eff_dt)
            economy.earn(gold_earned)
            economy.lose_life(lives_lost)
            tower_group.update(dt, enemy_group, projectile_group)
            projectile_group.update(eff_dt)

            if economy.is_game_over():
                game_over = True

        
        screen.fill((0,0,0))
        game_map.draw(screen)
        tower_group.draw(screen)
        enemy_group.draw(screen)
        projectile_group.draw(screen)
        panel.draw(screen, economy, wave_mgr, selected_type, speed_multiplier, mouse)

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
