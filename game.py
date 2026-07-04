import pygame
import sys
from settings import *
from map import GameMap, pixel_to_cell
from enemy import EnemyGroup
from tower import Tower, TowerGroup
from projectile import ProjectileGroup
from economy import Economy
from wave_manager import WaveManager
from ui import Panel, MenuScreen, MapSelectScreen, GameOverScreen, PauseScreen

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = 'menu'

        self.menu_screen = MenuScreen()
        self.map_selection_screen = MapSelectScreen(MAPS)
        self.gameover_screen = GameOverScreen()
        self.pause_screen = PauseScreen()

    def _init_session(self, map_index):
        self.map_index = map_index
        self.game_map = GameMap(map_index)
        self.enemy_group = EnemyGroup()
        self.projectile_group = ProjectileGroup()
        self.tower_group = TowerGroup()
        self.economy = Economy()
        self.wave_mgr = WaveManager(self.game_map.pixel_waypoints, self.enemy_group)
        self.panel = Panel()
        self.selected_type = 'basic'
        self.speed_multiplier = 1

    def handle_event(self, event):
        mouse = pygame.mouse.get_pos()

        if self.state == 'menu':
            action = self.menu_screen.handle_event(event)
            if action == 'play':
                self.state = 'map_select'
            elif action == 'quit':
                pygame.quit();
                sys.exit()

        elif self.state == 'map_select':
            idx = self.map_selection_screen.handle_event(event)
            if idx is not None:
                self._init_session(idx)
                self.state = 'playing'

        elif self.state == 'playing':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = 'paused'

            actions = self.panel.handle_event(event, self.economy, self.wave_mgr)
            if 'select_type' in actions:
                self.selected_type = actions['select_type']
            if 'send_wave' in actions:
                self.wave_mgr.skip_wait()
            if 'toggle_speed' in actions:
                self.speed_multiplier = 1 if self.speed_multiplier > 1 else 2

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if mx < GAME_WIDTH:
                    col, row = pixel_to_cell(mx, my)
                    if self.game_map.is_buildable(col, row):
                        cost = TOWER_TYPES[self.selected_type]['cost']
                        if self.economy.spend(cost):
                            tower = Tower(self.selected_type, col, row)
                            self.game_map.place_tower(col, row, tower)
                            self.tower_group.add(tower)

        elif self.state == 'paused':
            action = self.pause_screen.handle_event(event)
            if action == 'resume':
                self.state = 'playing'
            elif action == 'menu':
                self.state = 'menu'

        elif self.state in ('game_over', 'victory'):
            action = self.gameover_screen.handle_event(event)
            if action == 'retry':
                self._init_session(self.map_index)
                self.state = 'playing'
            elif action == 'menu':
                self.state = 'menu'

    def update(self, dt):
        if self.state != 'playing':
            return

        eff_dt = dt * self.speed_multiplier
        self.wave_mgr.update(eff_dt)
        gold_earned, lives_lost = self.enemy_group.update(eff_dt)
        self.economy.earn(gold_earned)
        self.economy.lose_life(lives_lost)
        self.tower_group.update(eff_dt, self.enemy_group, self.projectile_group)
        self.projectile_group.update(eff_dt)

        if self.economy.is_game_over():
            self.state = 'game_over'

        if self.wave_mgr.all_waves_done() and self.enemy_group.is_empty():
            self.state = 'victory'

    def draw(self):
        mouse = pygame.mouse.get_pos()
        self.screen.fill((10, 10, 10))

        if self.state == 'menu':
            self.menu_screen.draw(self.screen, mouse)
            return

        if self.state == 'map_select':
            self.map_selection_screen.draw(self.screen, mouse)
            return 

        if self.state in ('playing', 'paused', 'game_over', 'victory'):
            self.game_map.draw(self.screen)
            self.tower_group.draw(self.screen)
            self.enemy_group.draw(self.screen)
            self.projectile_group.draw(self.screen)
            self.panel.draw(self.screen, self.economy, self.wave_mgr, 
                            self.selected_type, self.speed_multiplier, mouse)

        if self.state == 'paused':
            self.pause_screen.draw(self.screen, mouse)

        if self.state in ('game_over', 'victory'):
            self.gameover_screen.draw(self.screen, self.economy.score,
                                      self.wave_mgr.wave_number, mouse,
                                      victory=(self.state == 'victory'))
