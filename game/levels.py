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

# TODO:
test_level_2_start = [[[] for x in range(17)] for y in range(15)]
test_level_2_start[10][0].append(M)
test_level_2_start[10][-1].append(M)
test_level_2_start[0][0].append(M)
test_level_2_start[-1][-1].append(M)
