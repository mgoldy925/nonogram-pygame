import pygame
from pygame.locals import *
import sys
from nonogram import Nonogram

def main():
    # Define constants
    SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600

    BOX_EMPTY = 0
    BOX_FILLED = 1
    BOX_MARKED = 2

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BACKGROUND = (110, 220, 250)

    BOARD_ORIGIN = BOARD_X, BOARD_Y = (50, 50)
    BOX_SIZE = 40
    INSTRUCTION_SIZE = 60

    # Start game
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Nonogram")
    BOARD_FONT = pygame.font.SysFont("arial", 24)
    BTN_FONT = pygame.font.SysFont("arial", 20)

    # Initialize buttons
    buttons = [
        (pygame.Rect(
            SCREEN_WIDTH/8, SCREEN_HEIGHT*7/8,
            SCREEN_WIDTH/6, SCREEN_HEIGHT/16), "New Game"),
        (pygame.Rect(
            SCREEN_WIDTH*3/8, SCREEN_HEIGHT*7/8,
            SCREEN_WIDTH/6, SCREEN_HEIGHT/16), "Check Board"),
        (pygame.Rect(
            SCREEN_WIDTH*5/8, SCREEN_HEIGHT*7/8,
            SCREEN_WIDTH/8, SCREEN_HEIGHT/16), "Show Answer")
    ]

    # Initialize board
    nonogram = Nonogram(10)

    box_coord = lambda n : (n > 0)*INSTRUCTION_SIZE + max(0, n-1)*BOX_SIZE
    box_width = lambda n : BOX_SIZE if n > 0 else INSTRUCTION_SIZE
    boxes = []
    for i in range(nonogram.size+1):
        row = []
        for j in range(nonogram.size+1):
            row.append(pygame.Rect(
                BOARD_X + box_coord(j), BOARD_Y + box_coord(i),
                box_width(j), box_width(i)
            ))
        boxes.append(row)


    # Game loop
    running = True
    while running:

        for event in pygame.event.get():
            # Check if user quit game
            if event.type == QUIT:
                running = False

            # Cheeck if user clicks on something
            elif event.type == MOUSEBUTTONUP:
                coords = pygame.mouse.get_pos()

                # Check if box is clicked
                for i, row in enumerate([r[1:] for r in boxes[1:]]):
                    for j, box in enumerate(row):
                        if box.collidepoint(coords):
                            i, j = i+1, j+1
                            # Marked if right click, otherwise invert
                            nonogram.board[i][j] = (BOX_MARKED if event.button == 3
                                                    else BOX_EMPTY if nonogram.board[i][j] == BOX_FILLED
                                                    else BOX_FILLED)
                            
                # Check if button is clicked
                for button, name in buttons:
                    if button.collidepoint(coords):
                        pass
                        # if name == "New Game":

                        # elif name == "Check Board":

                        # elif name == "Show "
    
        # Draw background
        screen.fill(BACKGROUND)

        # Draw board
        for row, val_row in zip(boxes, nonogram.board):
            for box, value in zip(row, val_row):
                # Empty boxes are white
                if value == BOX_EMPTY:
                    pygame.draw.rect(screen, WHITE, box)
                # Marked boxes have an X
                elif value == BOX_MARKED:
                    pygame.draw.rect(screen, WHITE, box)
                    screen.blit(BOARD_FONT.render("X", True, BLACK), box)
                # Filled boxes are black
                elif value == BOX_FILLED:
                    pygame.draw.rect(screen, BLACK, box)
                # Instructions
                else:
                    pygame.draw.rect(screen, WHITE, box)
                    sep = " " if box.width == INSTRUCTION_SIZE else "\n"
                    screen.blit(BOARD_FONT.render(sep.join(str(n) for n in value), True, BLACK), box)
                # Draw outline
                pygame.draw.rect(screen, BLACK, box, 2)

        # Draw buttons
        for button, name in buttons:
            pygame.draw.rect(screen, WHITE, button)
            pygame.draw.rect(screen, BLACK, button, 3)
            screen.blit(BTN_FONT.render(name, True, BLACK), button)

        pygame.display.flip()


    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()