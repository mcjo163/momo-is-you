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
