# Level board starting states
# TODO: read these layouts from external files

from entities import Entities

M = Entities.MOMO
W = Entities.WALL
R = Entities.ROCK
F = Entities.FLAG

test_level_start = [
    [[], [], [], [], [], [], [], [], [], [], []],
    [[], [], [], [], [], [W], [], [], [], [], []],
    [[], [], [], [], [], [W], [], [], [], [], []],
    [[], [], [M], [], [], [W], [], [], [F], [], []],
    [[], [], [], [], [], [W], [], [], [], [], []],
    [[], [], [], [], [], [W], [], [], [], [], []],
    [[], [], [], [], [], [], [], [], [], [], []],
    [[], [], [], [], [], [], [], [], [], [], []]
]
