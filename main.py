import pygame
import sys

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
FPS = 60

def main():
    pygame.init()
    pygame.display.set_caption('Tower Defense')
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))##, pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            screen.fill((0,0,0))
            pygame.display.flip()


if __name__ == '__main__':
    main()
