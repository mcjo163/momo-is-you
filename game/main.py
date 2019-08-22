# Micah Johnson and Russell Schwartz
# August 2019

import pygame
from functools import lru_cache

from engine import Level
from levels import test_level_1_start, test_level_2_start, test_level_3_start, test_level_4_start
from entities import *
from assets import src_images

# --- UI-Related Constants --- #
STARTING_SCREEN_WIDTH, STARTING_SCREEN_HEIGHT = 800, 600  # starting dimensions of screen (px)
MIN_SCREEN_WIDTH = 160
MIN_SCREEN_HEIGHT = 120
VIEWPORT_MIN_PADDING = 50  # minimum viewport edge padding (px)

SCREEN_BACKGROUND_COLOR = (25, 25, 32)
VIEWPORT_BACKGROUND_COLOR = (15, 15, 15)

TARGET_FPS = 60
INPUT_REPEAT_BUFFER_MS = 120  # time between registered inputs when key is held

key_map = {
    pygame.K_UP: Level.UP,
    pygame.K_DOWN: Level.DOWN,
    pygame.K_LEFT: Level.LEFT,
    pygame.K_RIGHT: Level.RIGHT,
    pygame.K_SPACE: Level.WAIT,
    pygame.K_z: Level.UNDO,
    pygame.K_r: Level.RESTART
}

# Maps entities to the resources required for drawing
entity_map = {
    Objects.MOMO: {
        "color": None,
        "src_image_id": "momo_src",
        "draw_precedence": 2
    },
    Objects.WALL: {
        "color": None,
        "src_image_id": "wall_src",
        "draw_precedence": 0
    },
    Objects.ROCK: {
        "color": None,
        "src_image_id": "rock_src",
        "draw_precedence": 1
    },
    Objects.FLAG: {
        "color": None,
        "src_image_id": "flag_src",
        "draw_precedence": 1
    },
    Objects.WATER: {
        "color": (0, 0, 255),  # TEMPORARY
        "src_image_id": None,
        "draw_precedence": 1
    },

    Nouns.MOMO: {
        "color": None,
        "src_image_id": None,
        "text_str": "MOMO",
        "text_color": (127, 0, 0),
        "draw_precedence": 2
    },
    Nouns.WALL: {
        "color": None,
        "src_image_id": None,
        "text_str": "WALL",
        "text_color": (127, 127, 0),
        "draw_precedence": 2
    },
    Nouns.ROCK: {
        "color": None,
        "src_image_id": None,
        "text_str": "ROCK",
        "text_color": (180, 127, 127),
        "draw_precedence": 2
    },
    Nouns.FLAG: {
        "color": None,
        "src_image_id": None,
        "text_str": "FLAG",
        "text_color": (127, 127, 127),
        "draw_precedence": 2
    },
    Nouns.WATER: {
        "color": None,
        "src_image_id": None,
        "text_str": "WATER",
        "text_color": (0, 0, 127),
        "draw_precedence": 2
    },

    Verbs.IS: {
        "color": None,
        "src_image_id": None,
        "text_str": "IS",
        "text_color": (255, 255, 255),
        "draw_precedence": 2
    },

    Adjectives.YOU: {
        "color": None,
        "src_image_id": None,
        "text_str": "YOU",
        "text_color": (255, 0, 255),
        "draw_precedence": 2
    },
    Adjectives.WIN: {
        "color": None,
        "src_image_id": None,
        "text_str": "WIN",
        "text_color": (127, 0, 255),
        "draw_precedence": 2
    },
    Adjectives.STOP: {
        "color": None,
        "src_image_id": None,
        "text_str": "STOP",
        "text_color": (127, 0, 127),
        "draw_precedence": 2
    },
    Adjectives.PUSH: {
        "color": None,
        "src_image_id": None,
        "text_str": "PUSH",
        "text_color": (63, 63, 127),
        "draw_precedence": 2
    },
    Adjectives.DEFEAT: {
        "color": None,
        "src_image_id": None,
        "text_str": "DEFEAT",
        "text_color": (63, 0, 0),
        "draw_precedence": 2
    },
    Adjectives.SINK: {
        "color": None,
        "src_image_id": None,
        "text_str": "SINK",
        "text_color": (63, 53, 0),
        "draw_precedence": 2
    }
}


# Scales given surface to given size and returns results (expensive, results should be cached)
def get_scaled_image(surface, size):
    return pygame.transform.smoothscale(surface, (size, size))


# Binary search to find font size with correct height to fill tile with 2 chars vertically and 3 horizontally
@lru_cache(maxsize=20)  # for good measure
def get_font(name, tile_size_px):
    pygame.font.init()

    size_lower_bound = 8
    size_upper_bound = 200

    target_size_px = int(tile_size_px * 0.58)

    size = target_size_px  # initial guess
    while size_upper_bound - size_lower_bound > 1:
        font = pygame.font.SysFont(name, size, bold=True)
        text_size_px = max(font.size("M"))
        error = text_size_px - target_size_px
        # print(size, error, size_lower_bound, size_upper_bound)
        if error >= 0:
            size_upper_bound = size
        else:
            size_lower_bound = size
        size = (size_lower_bound + size_upper_bound) // 2

    return font


text_locations = {
    1: [(0.5, 0.5)],
    2: [(0.5, 0.25), (0.5, 0.75)],
    4: [(0.30, 0.27), (0.70, 0.27), (0.30, 0.73), (0.70, 0.73)]
}


# draws a square with rounded corners onto the given tile Surface
def draw_text_card_onto_tile(tile, color):
    tile_size_px = tile.get_width()
    corner_radius = tile_size_px // 6

    pygame.draw.rect(tile, color, pygame.Rect(0, corner_radius, tile_size_px, tile_size_px - corner_radius * 2))  # hor
    pygame.draw.rect(tile, color, pygame.Rect(corner_radius, 0, tile_size_px - corner_radius * 2, tile_size_px))  # vert

    pygame.draw.circle(tile, color, (corner_radius, corner_radius), corner_radius)
    pygame.draw.circle(tile, color, (tile_size_px - corner_radius, corner_radius), corner_radius)
    pygame.draw.circle(tile, color, (corner_radius, tile_size_px - corner_radius), corner_radius)
    pygame.draw.circle(tile, color, (tile_size_px - corner_radius, tile_size_px - corner_radius), corner_radius)


# Returns surface of size (tile_size_px, tile_size_px); cached for performance
@lru_cache(maxsize=len(entity_map) * 2)  # for good measure
def get_entity_image(entity, tile_size_px):
    if entity_map[entity]["src_image_id"] is not None:
        # get scaled texture
        src_image = src_images[entity_map[entity]["src_image_id"]]
        return get_scaled_image(src_image, tile_size_px)
    else:
        # render text
        img = pygame.Surface((tile_size_px, tile_size_px), pygame.SRCALPHA)
        if isinstance(entity, Text):
            font = get_font("comicsansms", tile_size_px)
            text_str = entity_map[entity]["text_str"]
            if len(text_str) < 4:
                text_substrings = [text_str]  # 1 line
            elif len(text_str) == 4:
                text_substrings = [char for char in text_str[:4]]  # 2x2 grid
            else:
                text_substrings = [text_str[:3], text_str[3:]]

            if isinstance(entity, Adjectives):
                draw_text_card_onto_tile(img, entity_map[entity]["text_color"])
                text_color = VIEWPORT_BACKGROUND_COLOR
            else:
                text_color = entity_map[entity]["text_color"]

            text_images = [font.render(substr, True, text_color) for substr in text_substrings]
            locations = text_locations[len(text_images)]
            for text_img, loc in zip(text_images, locations):
                dest = (
                    tile_size_px * loc[0] - text_img.get_width() // 2,
                    tile_size_px * loc[1] - text_img.get_height() // 2
                )
                img.blit(text_img, dest)
        else:
            img.fill(entity_map[entity]["color"])
        return img


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
                img = get_entity_image(entity, tile_size_px)
                loc_px = (tile_size_px * x, tile_size_px * y)
                viewport.blit(img, loc_px)


# Draw the level onto a fresh viewport surface, blit it to the screen, and flip the display
def update_screen(screen, level, viewport_rect):
    viewport = pygame.Surface((viewport_rect.width, viewport_rect.height))
    draw_level_onto_viewport(viewport, level)
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


# Initializes display, listens for keypress's, calls engine API methods, and handles window re-size events
def play_level(level):
    # initialize screen
    screen = get_initialized_screen(STARTING_SCREEN_WIDTH, STARTING_SCREEN_HEIGHT)
    pygame.display.update()

    # initialize viewport
    viewport_rect = get_viewport_rect(STARTING_SCREEN_WIDTH, STARTING_SCREEN_HEIGHT, level.width, level.height)
    update_screen(screen, level, viewport_rect)

    # initialize keypress vars
    currently_pressed = None
    last_input_timestamp = 0  # ms

    # main game loop
    clock = pygame.time.Clock()
    level_alive = True
    while level_alive:
        clock.tick(TARGET_FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                level_alive = False
            elif event.type == pygame.KEYDOWN:
                if event.key in key_map.keys():
                    currently_pressed = event.key
            elif event.type == pygame.KEYUP:
                if event.key == currently_pressed:
                    currently_pressed = None
            elif event.type == pygame.VIDEORESIZE:
                new_screen_width = max(event.w, MIN_SCREEN_WIDTH)
                new_screen_height = max(event.h, MIN_SCREEN_HEIGHT)
                screen = get_initialized_screen(new_screen_width, new_screen_height)
                pygame.display.update()
                viewport_rect = get_viewport_rect(new_screen_width, new_screen_height, level.width, level.height)
                update_screen(screen, level, viewport_rect)

        if currently_pressed is not None:
            current_timestamp = pygame.time.get_ticks()
            if current_timestamp - last_input_timestamp > INPUT_REPEAT_BUFFER_MS:
                last_input_timestamp = current_timestamp
                level.process_input(key_map[currently_pressed])
                update_screen(screen, level, viewport_rect)  # TODO: only call this when needed

        if level.has_won:
            print("\nCongrats! You beat the level!")
            pygame.time.wait(1000)
            level_alive = False


if __name__ == "__main__":
    test_level = Level(test_level_4_start)
    play_level(test_level)
