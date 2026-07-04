import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from map import GameMap

def main():
    pygame.init()
    pygame.display.set_caption('Tower Defense')
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))##, pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    game_map = GameMap(0)

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0,0,0))
        game_map.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
