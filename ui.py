import pygame
import settings as sett

def _font(size, bold=False):
    return pygame.font.SysFont('consolas', size, bold=bold)

def _draw_text(surface, text, x, y, font, color=sett.WHITE, center=False):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(x, y) if center else img.get_rect(topleft=(x, y)))
    surface.blit(img, rect)

class Button:
    def __init__(self, rect, label, color=(60, 60, 80), hover_color=(90, 90, 120), text_color=sett.WHITE, font_size=16, bold=False):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self._font = _font(font_size, bold)

    def draw(self, surface, mouse_pos=None, disabled=False):
        hovered = self.rect.collidepoint(mouse_pos) if mouse_pos else False
        col = (40, 40, 50) if disabled else (self.hover_color if hovered else self.color)
        pygame.draw.rect(surface, col, self.rect, border_radius=6)
        pygame.draw.rect(surface, sett.LIGHT_GRAY, self.rect, 1, border_radius=6)
        img = self._font.render(self.label, True, sett.GRAY if disabled else self.text_color)
        surface.blit(img, img.get_rect(center=self.rect.center))
    
    def is_clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and
                self.rect.collidepoint(event.pos))


class TowerButton:
    SIZE = 52
    
    def __init__(self, x, y, tower_type):
        self.rect = pygame.Rect(x, y, self.SIZE, self.SIZE)
        self.type = tower_type
        data = sett.TOWER_TYPES[tower_type]
        self.name = data['name']
        self.cost = data['cost']
        self.color =  data['color']
        self._f11 = _font(11)

    def draw(self, surface, mouse_pos, gold, selected_type):
        affordable = gold >= self.cost
        selected = selected_type == self.type
        hovered = self.rect.collidepoint(mouse_pos)

        bg = (70, 90, 110) if selected else (65, 75, 95) if hovered else (50, 50, 70)
        pygame.draw.rect(surface, bg, self.rect, border_radius=5)
        pygame.draw.circle(surface, self.color, self.rect.center, 14)

        col = sett.WHITE if affordable else sett.GRAY
        _draw_text(surface, self.name, self.rect.centerx, self.rect.top + 36, self._f11, col, center=True)
        _draw_text(surface, f'${self.cost}', self.rect.centerx, self.rect.top + 47, self._f11, sett.YELLOW if affordable else sett.PANEL_RED, center=True)

        border = sett.YELLOW if selected else (sett.LIGHT_GRAY if hovered else (70, 70, 90))
        pygame.draw.rect(surface, border, self.rect, 2, border_radius=5)

    def is_clicked(self, event, gold):
        return (event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and
                self.rect.collidepoint(event.pos) and
                gold >= self.cost)


class Panel:
    PANEL_X = sett.GAME_WIDTH

    def __init__(self):
        self._f16 = _font(16, bold=True)
        self._f14 = _font(14, bold=True)
        self._f13 = _font(13)
        self._f11 = _font(11)

        px = self.PANEL_X + 10
        btn_w = sett.PANEL_WIDTH - 20
        btns_y = 175

        self.tower_buttons = [
                TowerButton(self.PANEL_X + 10, btns_y, 'basic')
                ]

        self.btn_send_wave = Button(
                (px, btns_y + 70, btn_w, 32),
                'Send Wave!', color=(50, 110, 50), hover_color=(70, 150, 70), bold=True
                )

        self.btn_speed = Button(
                (px, btns_y + 112, btn_w, 30),
                '>> 2x'
                )

    def draw(self, surface, economy, wave_mgr, selected_type, speed_multiplier, mouse_pos):
        pygame.draw.rect(surface, sett.PANEL_BG, (self.PANEL_X, 0, sett.PANEL_WIDTH, sett.SCREEN_HEIGHT))
        pygame.draw.line(surface, sett.GRAY, (self.PANEL_X, 0), (self.PANEL_X, sett.SCREEN_HEIGHT), 2)

        px = self.PANEL_X + sett.PANEL_WIDTH // 2 
        y = 14

        _draw_text(surface, 'TOWER DEFENSE', px, y, self._f16, sett.YELLOW, center=True)
        y += 28

        _draw_text(surface, f'Gold   ${economy.gold}', px, y, self._f14, sett.YELLOW, center=True)
        _draw_text(surface, f'Lives   ${economy.lives}', px, y + 20, self._f14, sett.GREEN if economy.lives > 5 else sett.PANEL_RED, center=True)
        _draw_text(surface, f'Score   ${economy.score}', px, y + 40, self._f13, sett.LIGHT_GRAY, center=True)
        y += 65

        if wave_mgr.state == 'waiting':
            _draw_text(surface, f'Next wave in {wave_mgr.wait_seconds_left: .1f}s',
                       px, y, self._f11, sett.ORANGE, center=True)
        elif wave_mgr.state == 'spawning':
            _draw_text(surface, 'Spawning...', px, y, self._f11, sett.PANEL_RED, center=True)
        elif wave_mgr.state == 'in_wave':
            _draw_text(surface, 'Wave active', px, y, self._f11, (150, 220, 150), center=True)
        elif wave_mgr.state == 'finished':
            _draw_text(surface, 'All waves done!', px, y, self._f11, sett.YELLOW, center=True)

        for tower_button in self.tower_buttons:
            tower_button.draw(surface, mouse_pos, economy.gold, selected_type)

        can_send = wave_mgr.state == 'waiting'
        self.btn_send_wave.draw(surface, mouse_pos, disabled=not can_send)

        self.btn_speed.label = '>> 1x' if speed_multiplier > 1 else '>> 2x'
        self.btn_speed.draw(surface, mouse_pos)

    def handle_event(self, event, economy, wave_mgr):
        actions = {}

        for tower_button in self.tower_buttons:
            if tower_button.is_clicked(event, economy.gold):
                actions['select_type'] = tower_button.type

        if self.btn_send_wave.is_clicked(event) and wave_mgr.state == 'waiting':
            actions['send_wave'] = True

        if self.btn_speed.is_clicked(event):
            actions['toggle_speed'] = True

        return actions 


class MenuScreen:
    def __init__(self):
        self._f48 = _font(48, bold=True)
        self._f20 = _font(20)
        self._f14 = _font(14)
        cx =  sett.SCREEN_WIDTH // 2
        self.btn_play = Button((cx - 110, 300, 220, 50), 'Play',
                               color=(40, 100, 40), hover_color=(60, 140, 60),
                               font_size=22, bold=True)
        self.btn_quit = Button((cx - 110, 370, 220, 50), 'Quit',
                               color=(100, 40, 40), hover_color=(140, 55, 55),
                               font_size=22, bold=True)

    def draw(self, surface, mouse_pos):
        surface.fill((15, 15, 25))
        cx = sett.SCREEN_WIDTH // 2
        _draw_text(surface, 'TOWER DEFENSE', cx, 130, self._f48, sett.YELLOW, center=True)
        _draw_text(surface, 'Place towers. Survive all waves.',
                   cx, 220, self._f20, sett.LIGHT_GRAY, center=True)
        self.btn_play.draw(surface, mouse_pos)
        self.btn_quit.draw(surface, mouse_pos)

    def handle_event(self, event):
        if self.btn_play.is_clicked(event): 
            return 'play'
        if self.btn_quit.is_clicked(event):
            return 'quit'
        return None


class MapSelectScreen:
    def __init__(self, maps):
        self._f36 = _font(36, bold=True)
        self._f14 = _font(14)
        cx = sett.SCREEN_WIDTH // 2
        self.buttons = []

        for i, m in enumerate(maps):
            btn = Button((cx - 130, 260 + i * 80, 260, 54), m['name'], 
                         font_size=20, bold=True)
            self.buttons.append((btn, i))

    def draw(self, surface, mouse_pos):
        surface.fill((15, 15, 25))
        cx = sett.SCREEN_WIDTH // 2
        _draw_text(surface, 'SELECT MAP', cx, 130, self._f36, sett.YELLOW, center=True)
        _draw_text(surface, 'Choose a map to play on.',
                   cx, 185, self._f14, sett.LIGHT_GRAY, center=True)
        
        for btn, _ in self.buttons:
            btn.draw(surface, mouse_pos)

    def handle_event(self, event):
        for btn, idx in self.buttons:
            if btn.is_clicked(event):
                return idx
        return None


class GameOverScreen:
    def __init__(self):
        self._f48 = _font(48, bold=True)
        self._f22 = _font(22)
        cx = sett.SCREEN_WIDTH // 2
        self.btn_retry = Button((cx - 130, 370, 260, 50), 'Play Again',
                                color=(40, 100, 40), hover_color=(60, 140, 60),
                                font_size=20, bold=True)
        self.btn_menu = Button((cx - 130, 430, 260, 50), 'Main Manu',
                               color=(60, 60, 90), hover_color=(60, 80, 120),
                               font_size=20)

    def draw(self, surface, score, wave, mouse_pos, victory=False):
        overlay = pygame.Surface((sett.SCREEN_WIDTH, sett.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        surface.blit(overlay, (0, 0))
        cx = sett.SCREEN_WIDTH // 2
        title = 'YOU WON' if victory else 'GAME OVER'
        color = sett.YELLOW if victory else sett.PANEL_RED
        _draw_text(surface, title, cx, 220, self._f48, color, center=True)
        _draw_text(surface, f'Score: {score}   Wave: {wave}',
                   cx, 310, self._f22, sett.WHITE, center=True)
        self.btn_retry.draw(surface, mouse_pos)
        self.btn_menu.draw(surface, mouse_pos)

    def handle_event(self, event):
        if self.btn_retry.is_clicked(event):
            return 'retry'
        if self.btn_menu.is_clicked(event):
            return 'menu'
        return None
