# Level board starting states
# TODO: read these layouts from external files

from entities import *

M = Objects.MOMO
W = Objects.WALL
R = Objects.ROCK
F = Objects.FLAG

IS = Verbs.IS


test_level_1_start = [
    [[Nouns.MOMO], [IS], [Adjectives.YOU], [], [], [W], [], [], [], [], []],
    [[], [], [], [], [], [W], [], [], [], [], []],
    [[], [], [], [], [], [W], [], [], [], [], []],
    [[], [], [], [], [], [W], [], [], [], [], []],
    [[], [], [M], [], [], [R], [], [], [F], [], []],
    [[], [], [], [], [], [W], [], [], [], [], []],
    [[Nouns.WALL], [Nouns.ROCK], [], [], [], [W], [], [], [], [], []],
    [[IS], [IS], [], [], [], [W], [], [], [], [], []],
    [[Adjectives.STOP], [Adjectives.PUSH], [], [], [], [W], [], [], [Nouns.FLAG], [IS], [Adjectives.WIN]]
]

test_level_2_start = [
    [[Nouns.MOMO], [IS], [Adjectives.YOU], [], [], [W], [], [], [], [], []],
    [[], [], [], [], [], [W], [], [], [], [], []],
    [[], [], [], [], [], [W], [], [], [], [], []],
    [[], [], [], [], [], [W], [], [], [], [], []],
    [[], [], [M], [], [], [W], [], [], [F], [], []],
    [[], [], [], [], [], [W], [], [], [], [], []],
    [[], [Nouns.WALL], [], [], [], [W], [], [], [], [], []],
    [[], [IS], [], [], [], [W], [], [], [], [], []],
    [[], [Adjectives.STOP], [], [], [], [W], [], [], [Nouns.FLAG], [IS], [Adjectives.WIN]]
]

test_level_3_start = [[[] for x in range(30)] for y in range(21)]
test_level_3_start[0][0:3] = [[Nouns.MOMO], [IS], [Adjectives.YOU]]
test_level_3_start[1][0:3] = [[Nouns.WATER], [IS], [Adjectives.SINK]]
test_level_3_start[-1][0:3] = [[Nouns.ROCK], [IS], [Adjectives.PUSH]]
test_level_3_start[-2][0:3] = [[Nouns.FLAG], [IS], [Adjectives.WIN]]
test_level_3_start[7][5] = [Objects.MOMO]
test_level_3_start[13][5] = [Objects.ROCK]
for row in test_level_3_start: row[12] = [Objects.WATER]
test_level_3_start[10][20] = [Objects.FLAG]
