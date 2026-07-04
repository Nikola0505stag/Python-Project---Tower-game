# screen
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
FPS = 60

# grid
GRID_COLS = 20
GRID_ROWS = 15
CELL_SIZE = 48
GAME_WIDTH = GRID_COLS * CELL_SIZE
GAME_HEIGHT = GRID_ROWS * CELL_SIZE

# money
STARTING_GOLD = 300

#lives
STARTING_LIVES = 20

#colors 
GRASS_COLOR = (55, 115, 35)
PATH_COLOR = (180, 150, 100)
GRID_LINE = (45, 100, 28)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
DARK_GREY = (40, 40, 40)
YELLOW = (255, 215, 0)
RED = (210, 55, 55)
STEEL_BLUE = (70, 130, 180)

# maps
MAPS = [
        {
            'name': 'S-Curve',
            'path': [(0, 7), (4, 7), (4, 3), (10, 3), (10, 11), (15, 11), (15, 5), (19, 5)]
            }
        ]

# enemies
ENEMY_TYPES = {
        "basic": {'name': 'Basic', 'hp': 100, 'speed': 80, 'color': RED, 'size': 14, 'hp': 100, 'reward': 50}
        }

# towers
TOWER_TYPES = {
        'basic': {
            'name': 'Basic',
            'cost': 100,
            'color': STEEL_BLUE,
            'damage': 20,
            'range': 3.0,
            'fire_rate': 1.0
            }

        }

