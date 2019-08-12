# Micah Johnson and Russell Schwartz
# August 2019

import pygame

from engine import Level
from levels import *
from entities import Entities

# UI-Related Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600                  # dimensions of screen in px
VIEWPORT_BUFFER_HOR, VIEWPORT_BUFFER_VERT = 50, 50      # level contents viewport edge buffers

viewport_rect = pygame.Rect(
    (VIEWPORT_BUFFER_HOR, VIEWPORT_BUFFER_VERT),
    (SCREEN_WIDTH - VIEWPORT_BUFFER_HOR * 2, SCREEN_HEIGHT - VIEWPORT_BUFFER_VERT * 2)
)

key_map = {
    pygame.K_UP: Level.UP,
    pygame.K_DOWN: Level.DOWN,
    pygame.K_LEFT: Level.LEFT,
    pygame.K_RIGHT: Level.RIGHT,
    pygame.K_z: Level.UNDO
}

entity_map = {
    Entities.MOMO: {
        "color": (255, 0, 0),       # TEMPORARY
        "src_image": None,
        "draw_precedence": 1
    },
    Entities.WALL: {
        "color": (0, 255, 255),     # TEMPORARY
        "src_image": None,
        "draw_precedence": 0
    },
    Entities.FLAG: {
        "color": (255, 255, 0),     # TEMPORARY
        "src_image": None,
        "draw_precedence": 0
    }
}


def process_keypress(level, key):
    level.process_input(key_map[key])


def draw_level(screen, level):
    board = level.board
    tile_size_px = min(viewport_rect.width // level.width, viewport_rect.height // level.height)
    print("tile_size_px:\t" + str(tile_size_px))

    for y in range(level.height):
        for x in range(level.width):
            tile_contents = board[y][x]
            tile_contents.sort(key=lambda e: entity_map[e]["draw_precedence"])
            for entity in tile_contents:
                img = pygame.Surface((tile_size_px, tile_size_px)) # entity_map[entity]["image"]
                img.fill(entity_map[entity]["color"])
                loc_px = (viewport_rect.left + x * tile_size_px, viewport_rect.top + y * tile_size_px)
                screen.blit(img, loc_px)

    pygame.display.update()


def play_level(level):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    draw_level(screen, level)

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
                    draw_level(screen, level)


if __name__ == "__main__":
    test_level = Level(test_level_start)
    play_level(test_level)
