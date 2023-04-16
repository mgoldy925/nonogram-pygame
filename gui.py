import pygame
from pygame.locals import *
import sys

def main():
    # Define constants
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
    DIMENSIONS = WIDTH, HEIGHT = 10, 10
    GRID_ORIGIN = (50, 50)
    BOX_DIM, NUM_LONG_DIM = 20, 50

    BOX_EMPTY = 0
    BOX_FILLED = 1
    BOX_MARKED = 2


    # Start game
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Nonogram")


    # Initialize board
    boxes = []
    
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False




    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()