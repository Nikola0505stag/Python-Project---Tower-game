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

# panel
PANEL_BG = (25, 25, 35)
PANEL_LIGHT = (40, 40, 55)
GRAY = (100, 100, 100)
LIGHT_GRAY = (180, 180, 180)
ORANGE = (255, 140, 0)
PANEL_RED = (200, 30, 30)
GREEN = (34, 139, 34)
PANEL_WIDTH = SCREEN_WIDTH - GAME_WIDTH

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

SELL_REFUND = 0.6
DARK_RED = (180, 60, 60)
CYAN = (40, 200, 200)
VIBRANT = (210, 135, 30)
# towers
TOWER_TYPES = {
        'basic': {
            'name': 'Basic',
            'cost': 100,
            'color': STEEL_BLUE,
            'desc': 'Balanced. Good for all situations.',
            'levels': [
                {'damage': 20, 'range': 3.0, 'fire_rate': 1.0, 'projectile_speed': 300, 'upgrade_cost': 150},
                {'damage': 38, 'range': 3.5, 'fire_rate': 1.3, 'projectile_speed': 330, 'upgrade_cost': 200},
                {'damage': 62, 'range': 4.0, 'fire_rate': 1.7, 'projectile_speed': 370, 'upgrade_cost': None}
                ]
            },
        'sniper': {
            'name': 'Sniper',
            'cost': 175,
            'color': DARK_RED,
            'desc': 'Long range, high damage, slow fire',
            'levels': [
                {'damage': 80, 'range': 6.0, 'fire_rate': 0.4, 'projectile_speed': 700, 'upgrade_cost': 225},
                {'damage': 145, 'range': 7.0, 'fire_rate': 0.4, 'projectile_speed': 800, 'upgrade_cost': 275},
                {'damage': 230, 'range': 8.5, 'fire_rate': 0.65, 'projectile_speed': 900, 'upgrade_cost': None}
                ]
            },
        'slow': {
            'name': 'Slow',
            'cost': 125,
            'color': CYAN,
            'desc': 'Slow enemies. Weak damage.',
            'levels': [
                {'damage': 8, 'range': 2.3, 'fire_rate': 1.0, 'projectile_speed': 220, 'upgrade_cost': 175},
                {'damage': 14, 'range': 3.0, 'fire_rate': 1.2, 'projectile_speed': 220, 'upgrade_cost': 225},
                {'damage': 22, 'range': 3.5, 'fire_rate': 1.5, 'projectile_speed': 220, 'upgrade_cost': None}
                ]
            },
        'splash': {
            'name': 'Splash',
            'cost': 200,
            'color': VIBRANT,
            'desc': 'Area damage. Great vs groups.',
            'levels': [
                {'damage': 30, 'range': 3.0, 'fire_rate': 0.6, 'projectile_speed': 210, 'upgrade_cost': 250},
                {'damage': 52, 'range': 3.5, 'fire_rate': 0.75, 'projectile_speed': 210, 'upgrade_cost': 300},
                {'damage': 80, 'range': 4.0, 'fire_rate': 0.9, 'projectile_speed': 230, 'upgrade_cost': None}
                ]
            }
        }
