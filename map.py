import pygame
import settings as sett

def cell_to_pixel(col, row):
    return (col * sett.CELL_SIZE + sett.CELL_SIZE // 2, row * sett.CELL_SIZE + sett.CELL_SIZE // 2)

def pixel_to_cell(x, y):
    return (x // sett.CELL_SIZE, y // sett.CELL_SIZE)

def trace_segment(a, b):
    cells = []
    col0, row0 = a
    col1, row1 = b

    if col0 == col1:
        step = 1 if row1 > row0 else -1
        for r in range(row0, row1 + step, step):
            cells.append((col0, r))
    else:
        step = 1 if col1 > col0 else -1
        for c in range(col0, col1 + step, step):
            cells.append((c, row0))

    return cells

def build_path_cells(waypoints):
    ordered = []
    seen = set()
    for i in range(len(waypoints) - 1):
        for cell in trace_segment(waypoints[i], waypoints[i + 1]):
            if cell not in seen:
                seen.add(cell)
                ordered.append(cell)
    return ordered, seen

class GameMap:
    def __init__(self, map_index):
        data = self.waypoints = sett.MAPS[map_index]['path']
        self.path_cells, self.path_set = build_path_cells(data)
        self.pixel_waypoints = [cell_to_pixel(c, r) for c, r in data]
        self._bg = self._make_background()

    def _make_background(self):
        surf = pygame.Surface((sett.GAME_WIDTH, sett.GAME_HEIGHT))
        surf.fill(sett.GRASS_COLOR)

        for col, row in self.path_cells:
            r = pygame.Rect(col * sett.CELL_SIZE, row * sett.CELL_SIZE, sett.CELL_SIZE, sett.CELL_SIZE)
            pygame.draw.rect(surf, sett.PATH_COLOR, r)
            pygame.draw.rect(surf, (160, 130, 80), r, 1)

        for col in range(sett.GRID_COLS + 1):
            pygame.draw.line(surf, sett.GRID_LINE, (col * sett.CELL_SIZE, 0), (col * sett.CELL_SIZE, sett.GAME_HEIGHT), 1)
        for row in range(sett.GRID_ROWS + 1):
                pygame.draw.line(surf, sett.GRID_LINE, (0, row * sett.CELL_SIZE), (sett.GAME_WIDTH, row * sett.CELL_SIZE), 1)

        return surf

    def draw(self, surface):
        surface.blit(self._bg, (0, 0))
