# Level board starting states
# TODO: read these layouts from external files

from entities import *

M = Objects.MOMO
W = Objects.WALL
R = Objects.ROCK
F = Objects.FLAG

IS = Verbs.IS


test_level_start = [
    [[Nouns.MOMO], [IS], [Adjectives.YOU], [], [], [], [], [], [], [], []],
    [[], [], [], [], [], [], [], [], [], [], []],
    [[], [], [], [], [], [W], [], [], [], [], []],
    [[], [], [], [], [], [W], [], [], [], [], []],
    [[], [], [M], [], [], [W], [], [], [F], [], []],
    [[], [], [], [], [], [W], [], [], [], [], []],
    [[Nouns.WALL], [], [], [], [], [W], [], [], [], [], []],
    [[IS], [], [], [], [], [], [], [], [], [], []],
    [[Adjectives.STOP], [], [], [], [], [], [], [], [Nouns.FLAG], [IS], [Adjectives.WIN]]
]

# TODO:
test_level_2_start = [[[] for x in range(17)] for y in range(15)]
test_level_2_start[10][0].append(M)
test_level_2_start[10][-1].append(M)
test_level_2_start[0][0].append(M)
test_level_2_start[-1][-1].append(M)
