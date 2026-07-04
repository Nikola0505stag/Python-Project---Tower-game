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
        self.rect = rect
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
