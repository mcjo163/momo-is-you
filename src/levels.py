# Level board starting states
# TODO: read these layouts from external files

import os

from entities import *

# Map from file key-strings to entities
# key-strings must be < 5 chars long and should be human-readable; asterisk indicates object
keystr_entity_map = {
    "": None,

    "MOM*": Objects.MOMO,
    "WAL*": Objects.WALL,
    "ROC*": Objects.ROCK,
    "FLA*": Objects.FLAG,
    "WAT*": Objects.WATER,

    "MOMO": Nouns.MOMO,
    "WALL": Nouns.WALL,
    "ROCK": Nouns.ROCK,
    "FLAG": Nouns.FLAG,
    "WATE": Nouns.WATER,

    "IS": Verbs.IS,
    "HAS": Verbs.HAS,

    "YOU": Adjectives.YOU,
    "WIN": Adjectives.WIN,
    "STOP": Adjectives.STOP,
    "PUSH": Adjectives.PUSH,
    "DEFE": Adjectives.DEFEAT,
    "SINK": Adjectives.SINK,
}


def read_level_start(filename):
    level_start = []
    with open(filename) as file:
        for line in file.readlines():
            row = []
            for tile in line.rstrip().split(";"):
                if len(tile) == 0:
                    row.append([])
                else:
                    keystrs = tile.split(",")
                    row.append([keystr_entity_map[keystr] for keystr in keystrs])
            level_start.append(row)

    return level_start


# --- Load All Levels --- #
levels_dirname = os.path.join(os.path.dirname(__file__), "levels")
filenames = ["level_1"]
level_starts = [read_level_start(os.path.join(levels_dirname, filename)) for filename in filenames]

# M = Objects.MOMO
# W = Objects.WALL
# R = Objects.ROCK
# F = Objects.FLAG
#
# IS = Verbs.IS
#
# test_level_1_start = [
#     [[Nouns.MOMO], [IS], [Adjectives.YOU], [], [], [W], [], [], [], [], []],
#     [[], [], [], [], [], [W], [], [], [], [], []],
#     [[], [], [], [], [], [W], [], [], [], [], []],
#     [[], [], [], [], [], [W], [], [], [], [], []],
#     [[], [], [M], [], [], [R], [], [], [F], [], []],
#     [[], [], [], [], [], [W], [], [], [], [], []],
#     [[Nouns.WALL], [Nouns.ROCK], [], [], [], [W], [], [], [], [], []],
#     [[IS], [IS], [], [], [], [W], [], [], [], [], []],
#     [[Adjectives.STOP], [Adjectives.PUSH], [], [], [], [W], [], [], [Nouns.FLAG], [IS], [Adjectives.WIN]]
# ]
#
# test_level_2_start = [
#     [[Nouns.MOMO], [IS], [Adjectives.YOU], [], [], [W], [], [], [], [], []],
#     [[], [], [], [], [], [W], [], [], [], [], []],
#     [[], [], [], [], [], [W], [], [], [], [], []],
#     [[], [], [], [], [], [W], [], [], [], [], []],
#     [[], [], [M], [], [], [W], [], [], [F], [], []],
#     [[], [], [], [], [], [W], [], [], [], [], []],
#     [[], [Nouns.WALL], [], [], [], [W], [], [], [], [], []],
#     [[], [IS], [], [], [], [W], [], [], [], [], []],
#     [[], [Adjectives.STOP], [], [], [], [W], [], [], [Nouns.FLAG], [IS], [Adjectives.WIN]]
# ]
#
# test_level_3_start = [[[] for x in range(20)] for y in range(15)]
# test_level_3_start[0][0:3] = [[Nouns.MOMO], [IS], [Adjectives.YOU]]
# test_level_3_start[1][0:3] = [[Nouns.WATER], [IS], [Adjectives.SINK]]
# test_level_3_start[-1][0:3] = [[Nouns.ROCK], [IS], [Adjectives.PUSH]]
# test_level_3_start[-2][0:3] = [[Nouns.FLAG], [IS], [Adjectives.WIN]]
# test_level_3_start[5][4] = [Objects.MOMO]
# test_level_3_start[8][4] = [Objects.ROCK]
# for row in test_level_3_start: row[12] = [Objects.WATER]
# test_level_3_start[7][18] = [Objects.FLAG]
#
# test_level_4_start = [
#     [[Nouns.MOMO], [IS], [Adjectives.YOU], [], [], [W], [], [], [], [], []],
#     [[], [], [], [], [], [W], [], [], [], [], []],
#     [[], [], [IS], [], [], [W], [], [], [], [], []],
#     [[], [], [], [], [], [W], [], [], [], [], []],
#     [[], [], [M], [], [], [W], [], [], [F], [], []],
#     [[], [], [], [Nouns.MOMO], [], [W], [], [], [], [], []],
#     [[Nouns.WALL], [], [], [], [], [W], [], [], [], [], []],
#     [[IS], [], [], [], [], [W], [], [], [], [], []],
#     [[Adjectives.STOP], [], [], [], [], [W], [], [], [Nouns.FLAG], [IS], [Adjectives.WIN]]
# ]
