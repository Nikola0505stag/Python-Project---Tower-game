import pygame
import settings as sett

def _font(size, bold=False):
    return pygame.font.SysFont('consolas', size, bold=bold)

def _draw_texgt(surface, text, x, y, font, color=sett.WHITE, center=False):
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
