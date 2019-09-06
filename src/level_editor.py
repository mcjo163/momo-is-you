# Standalone GUI Applet for creating levels

from ui_helpers import *
from levels import level_starts, keystr_entity_map


# --- UI-Related Constants --- #
STARTING_SCREEN_WIDTH, STARTING_SCREEN_HEIGHT = 800, 600  # starting dimensions of screen (px)
MIN_SCREEN_WIDTH = 160
MIN_SCREEN_HEIGHT = 120
VIEWPORT_MIN_PADDING = 50  # minimum viewport edge padding (px)

SCREEN_BACKGROUND_COLOR = (25, 25, 32)
VIEWPORT_BACKGROUND_COLOR = (15, 15, 15)
GRID_COLOR = (0, 80, 90, 127)

TARGET_FPS = 60


# Draw the level onto a fresh viewport surface, render UI elements, blit it to the screen, and flip the display
def update_screen(screen, board, viewport_rect):
    viewport = pygame.Surface((viewport_rect.width, viewport_rect.height))
    draw_board_onto_viewport(viewport, board, VIEWPORT_BACKGROUND_COLOR, GRID_COLOR)
    screen.blit(viewport, viewport_rect)
    pygame.display.update(viewport_rect)


# Size the viewport to both preserve level.board's aspect ratio and respect VIEWPORT_MIN_PADDING
def get_viewport_rect(screen_width_px, screen_height_px, level_width_tiles, level_height_tiles):
    width_ratio = (screen_width_px - VIEWPORT_MIN_PADDING * 2) // level_width_tiles
    height_ratio = (screen_height_px - VIEWPORT_MIN_PADDING * 2) // level_height_tiles
    pixels_per_tile = min(width_ratio, height_ratio)

    viewport_width = level_width_tiles * pixels_per_tile
    viewport_height = level_height_tiles * pixels_per_tile

    return pygame.Rect(
        ((screen_width_px - viewport_width) // 2, (screen_height_px - viewport_height) // 2),  # centered in screen
        (viewport_width, viewport_height)
    )


def get_initialized_screen(screen_width_px, screen_height_px):
    new_screen = pygame.display.set_mode((screen_width_px, screen_height_px), pygame.RESIZABLE)
    new_screen.fill(SCREEN_BACKGROUND_COLOR)
    return new_screen


# Initializes display, listens for keypress's, and handles window re-size events
def run_editor(board=None):
    # initialize screen; VIDEORESIZE event is generated immediately
    screen = get_initialized_screen(STARTING_SCREEN_WIDTH, STARTING_SCREEN_HEIGHT)

    if board is None:
        board = [[[] for _ in range(21)] for _ in range(15)]

    board_width, board_height = len(board[0]), len(board)

    # main game loop
    clock = pygame.time.Clock()
    editor_alive = True
    while editor_alive:
        clock.tick(TARGET_FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                editor_alive = False
            elif event.type == pygame.VIDEORESIZE:
                new_screen_width = max(event.w, MIN_SCREEN_WIDTH)
                new_screen_height = max(event.h, MIN_SCREEN_HEIGHT)
                screen = get_initialized_screen(new_screen_width, new_screen_height)
                pygame.display.update()
                viewport_rect = get_viewport_rect(new_screen_width, new_screen_height, board_width, board_height)
                update_screen(screen, board, viewport_rect)


if __name__ == "__main__":
    run_editor(level_starts[0])