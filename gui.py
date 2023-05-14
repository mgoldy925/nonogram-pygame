import pygame
from pygame.locals import *
import sys
from nonogram import Nonogram


# Declare globals / Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600

BOX_EMPTY = 0
BOX_FILLED = 1
BOX_MARKED = 2

BLACK = (0, 0, 0)
GRAY = (160, 160, 160)
WHITE = (255, 255, 255)
BACKGROUND = (110, 220, 250)

BOARD_ORIGIN = BOARD_X, BOARD_Y = (30, 30)
BOX_SIZE = 40
INSTRUCTION_SIZE = 80
SPACE = 5
VERTICAL_TEXT_OFFSET = 6

BOARD_SIZE = 10


def init_board(nonogram):

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
        
    return nonogram, boxes

def main():

    nonogram = Nonogram(BOARD_SIZE)

    # Start game
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Nonogram")
    BOARD_FONT = pygame.font.SysFont("Monocraft", 14)
    X_FONT = pygame.font.SysFont("Monocraft", 24)
    X_SURF = X_FONT.render("X", True, BLACK)
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
    nonogram, boxes = init_board(nonogram)

    # Game loop
    running = True
    mouse_held_down = False
    fill_state = None
    is_left_mouse_btn = False
    
    while running:

        for event in pygame.event.get():
            # Check if user quit game
            if event.type == QUIT:
                running = False

            # Cheeck if user clicks on something
            elif event.type == MOUSEBUTTONDOWN:
                coords = pygame.mouse.get_pos()

                mouse_held_down, is_left_mouse_btn = True, event.button != 3

                # Check if button is clicked
                for button, name in buttons:
                    if button.collidepoint(coords):
                        if name == "New Game":
                            nonogram = Nonogram(BOARD_SIZE)

                        elif name == "Check Board":
                            if nonogram.check_board():
                                screen.fill(WHITE)
                            else:
                                screen.fill(WHITE)

                        elif name == "Show Answer":
                            screen.fill(WHITE)
                            nonogram, boxes = init_board(nonogram)

                            for row, val_row in zip(boxes, nonogram.answer):
                                for box, value in zip(row, val_row):
                                
                                    if value == BOX_EMPTY:
                                        pygame.draw.rect(screen, WHITE, box)
                                    elif value == BOX_FILLED:
                                        pygame.draw.rect(screen, BLACK, box)
                                    else:
                                        pygame.draw.rect(screen, WHITE, box)
                                        sep = " " if box.width == INSTRUCTION_SIZE else "\n"
                                        screen.blit(BOARD_FONT.render(sep.join(str(n) for n in value), True, BLACK), box)
                        
                                    pygame.draw.rect(screen, BLACK, box, 2)    

            elif event.type == MOUSEBUTTONUP:
                mouse_held_down, fill_state = False, None

        # Fill square if mouse is held down
        if mouse_held_down:
            fill_state = fill_box(nonogram, boxes, is_left_mouse_btn, fill_state)

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
                    screen.blit(X_SURF, center(X_SURF, box))
                # Filled boxes are black
                elif value == BOX_FILLED:
                    pygame.draw.rect(screen, BLACK, box)

                # Instructions
                else:
                    pygame.draw.rect(screen, WHITE, box)
                    is_vert = box.width != INSTRUCTION_SIZE
                    ins_surf = instruction_surf(value, is_vert, BOARD_FONT)
                    screen.blit(ins_surf, center(ins_surf, box))
                
                # Draw outline
                pygame.draw.rect(screen, GRAY, box, 2)

        # Draw buttons
        for button, name in buttons:
            pygame.draw.rect(screen, WHITE, button)
            pygame.draw.rect(screen, BLACK, button, 3)
            screen.blit(BTN_FONT.render(name, True, BLACK), button)

        pygame.display.flip()


    pygame.quit()
    sys.exit(0)


# Fill state represents initial box type clicked
# So, if user clicks and drags on filled box, only filled boxes are affected in drag
def fill_box(nonogram, boxes, left_mouse_clicked, fill_state):
    coords = pygame.mouse.get_pos()

    # Check if box is clicked
    for ii, row in enumerate([r[1:] for r in boxes[1:]]):
        for jj, box in enumerate(row):
            i, j = ii+1, jj+1
            cur_box = nonogram.board[i][j]
        
            # Only fill if clicking on box of same type as originally clicked
            if box.collidepoint(coords) and (fill_state == cur_box or fill_state is None):
                fill_state = cur_box
                
                if left_mouse_clicked:
                    nonogram.board[i][j] = BOX_EMPTY if cur_box == BOX_FILLED else BOX_FILLED
                else:
                    nonogram.board[i][j] = BOX_EMPTY if cur_box == BOX_MARKED else BOX_MARKED

                # # xnor = lambda box : (cur_box != box) == (fill_state != box)
                # cur_filled, state_filled = cur_box == BOX_FILLED, fill_state == BOX_FILLED
                # cur_marked, state_marked = cur_box == BOX_MARKED, fill_state == BOX_MARKED
            
                # if left_mouse_clicked and cur_filled == state_filled:
                #     nonogram.board[i][j] = BOX_EMPTY if cur_filled else BOX_FILLED
                # elif not left_mouse_clicked and cur_marked == state_marked:
                #     nonogram.board[i][j] = BOX_EMPTY if cur_marked else BOX_MARKED

                #     # Make filled boxes empty if started clicking a filled box
                #     if cur_box == BOX_FILLED and fill_state == BOX_FILLED:
                #         nonogram.board[i][j] = BOX_EMPTY
                #     # If didn't start clicking a filled box, fill non-filled boxes
                #     elif cur_box != BOX_FILLED and fill_state != BOX_FILLED:
                #         nonogram.board[i][j] = BOX_FILLED
                
                # elif cur_box != BOX_MARKED:
                #     # Make marked boxes empty if started clicking a marked box
                #     if cur_box == BOX_MARKED:
                #         nonogram.board[i][j] = BOX_EMPTY
                #     # If didn't start clicking a marked box, mark non-marked boxes
                #     else:
                #         nonogram.board[i][j] = BOX_MARKED
                
                break

    return fill_state


def center(surf, rect):
    # Need to return (centerx - surf_width//2, centery - surf_height // 2)
    # However, we need to ensure this doesn't go out of the bounds of the rect
    # So, we cap it by taking the max of the two

    new_dims = []
    for center, surf_dim, rect_pos in zip(rect.center, surf.get_size(), rect.topleft):
        new_dims.append(max(center - surf_dim // 2, rect_pos))
    return new_dims


def instruction_surf(instruction, is_vert, BOARD_FONT):
    surfs, rects = [], []

    # Create surf and rect for each number in instruction
    for n in instruction:
        surf = BOARD_FONT.render(str(n), True, BLACK)
        rect = surf.get_rect()
        # Add padding to the rect
        # Also, text already has some vertical padding (?), so get rid of it
        rect = rect.inflate(SPACE*(not is_vert), (SPACE - VERTICAL_TEXT_OFFSET)*(is_vert))

        surfs.append(surf)
        rects.append(rect)
    
    # Create parent surface for numbers in instruction
    # If vertical, need height to be sum of heights and vice versa
    # Note that we assume rects is nonempty bc empty instructions are not allowed
    if is_vert:
        w, h = max(rect.width for rect in rects), sum(rect.height for rect in rects)
    else:
        w, h = sum(rect.width for rect in rects), max(rect.height for rect in rects)
    parent_surf = pygame.Surface((w, h))
    parent_surf.fill(WHITE)
    
    # Blit each letter onto the parent surf
    x, y = 0, 0
    for surf, rect in zip(surfs, rects):
        parent_surf.blit(surf, (x, y))
        # Increment x if text is horizontal, increment y if text is vertical
        x += (rect.width)*(not is_vert)
        y += (rect.height)*(is_vert)

    return parent_surf


if __name__ == "__main__":
    main()