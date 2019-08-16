# Micah Johnson and Russell Schwartz
# August 2019

import pygame

from engine import Level
from levels import *
from entities import *

# UI-Related Constants
STARTING_SCREEN_WIDTH, STARTING_SCREEN_HEIGHT = 800, 600  # starting dimensions of screen (px)
MIN_SCREEN_WIDTH = 160
MIN_SCREEN_HEIGHT = 120
VIEWPORT_MIN_BUFFER = 50  # minimum viewport edge buffer (px)

SCREEN_BACKGROUND_COLOR = (30, 30, 30)
VIEWPORT_BACKGROUND_COLOR = (100, 100, 100)

key_map = {
    pygame.K_UP: Level.UP,
    pygame.K_DOWN: Level.DOWN,
    pygame.K_LEFT: Level.LEFT,
    pygame.K_RIGHT: Level.RIGHT,
    pygame.K_SPACE: Level.WAIT,
    pygame.K_z: Level.UNDO
}

entity_map = {
    Objects.MOMO: {
        "color": (255, 0, 0),  # TEMPORARY
        "src_image": None,
        "draw_precedence": 2
    },
    Objects.WALL: {
        "color": (0, 255, 255),  # TEMPORARY
        "src_image": None,
        "draw_precedence": 0
    },
    Objects.FLAG: {
        "color": (255, 255, 0),  # TEMPORARY
        "src_image": None,
        "draw_precedence": 1
    },

    Nouns.MOMO: {
        "color": (127, 0, 0),  # TEMPORARY
        "src_image": None,
        "draw_precedence": 2
    },
    Nouns.WALL: {
        "color": (127, 127, 0),  # TEMPORARY
        "src_image": None,
        "draw_precedence": 2
    },
    Nouns.FLAG: {
        "color": (127, 127, 127),  # TEMPORARY
        "src_image": None,
        "draw_precedence": 2
    },
    Verbs.IS: {
        "color": (255, 255, 255),  # TEMPORARY
        "src_image": None,
        "draw_precedence": 2
    },
    Adjectives.YOU: {
        "color": (255, 0, 255),  # TEMPORARY
        "src_image": None,
        "draw_precedence": 2
    },
    Adjectives.STOP: {
        "color": (127, 0, 127),  # TEMPORARY
        "src_image": None,
        "draw_precedence": 2
    },
    Adjectives.WIN: {
        "color": (127, 0, 255),  # TEMPORARY
        "src_image": None,
        "draw_precedence": 2
    }
}


def process_keypress(level, key):
    if key in key_map.keys():
        level.process_input(key_map[key])


# Assumes given viewport surface has same exact aspect ratio as level.board (only draws squares)
def draw_level_onto_viewport(viewport, level):
    viewport.fill(VIEWPORT_BACKGROUND_COLOR)

    board = level.board
    tile_size_px = min(viewport.get_width() // level.width, viewport.get_height() // level.height)
    # print("tile_size_px:\t" + str(tile_size_px))

    for y in range(level.height):
        for x in range(level.width):
            tile_contents = board[y][x]
            tile_contents.sort(key=lambda e: entity_map[e]["draw_precedence"])
            for entity in tile_contents:
                img = pygame.Surface((tile_size_px, tile_size_px))  # entity_map[entity]["image"]
                img.fill(entity_map[entity]["color"])  # TEMPORARY
                loc_px = (tile_size_px * x, tile_size_px * y)
                viewport.blit(img, loc_px)


def update_screen(screen, level, viewport_rect):
    viewport = pygame.Surface((viewport_rect.width, viewport_rect.height))
    draw_level_onto_viewport(viewport, level)
    screen.blit(viewport, viewport_rect)
    pygame.display.update(viewport_rect)


# Size the viewport to both preserve level.board's aspect ratio and respect VIEWPORT_MIN_BUFFER
def get_viewport_rect(screen_width_px, screen_height_px, level_width_tiles, level_height_tiles):
    width_ratio = (screen_width_px - VIEWPORT_MIN_BUFFER * 2) // level_width_tiles
    height_ratio = (screen_height_px - VIEWPORT_MIN_BUFFER * 2) // level_height_tiles
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


def play_level(level):
    # initialize screen
    screen = get_initialized_screen(STARTING_SCREEN_WIDTH, STARTING_SCREEN_HEIGHT)
    pygame.display.update()

    # initialize viewport
    viewport_rect = get_viewport_rect(STARTING_SCREEN_WIDTH, STARTING_SCREEN_HEIGHT, level.width, level.height)
    update_screen(screen, level, viewport_rect)

    # main game loop
    clock = pygame.time.Clock()
    level_alive = True
    while level_alive:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                level_alive = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pass  # TODO: restart level
                else:
                    process_keypress(level, event.key)
                    update_screen(screen, level, viewport_rect)
            elif event.type == pygame.VIDEORESIZE:
                new_screen_width = max(event.w, MIN_SCREEN_WIDTH)
                new_screen_height = max(event.h, MIN_SCREEN_HEIGHT)
                screen = get_initialized_screen(new_screen_width, new_screen_height)
                pygame.display.update()
                viewport_rect = get_viewport_rect(new_screen_width, new_screen_height, level.width, level.height)
                update_screen(screen, level, viewport_rect)


if __name__ == "__main__":
    test_level = Level(test_level_start)
    play_level(test_level)
