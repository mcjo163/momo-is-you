from enum import Enum, auto


# Abstract class encompassing all entities which can be in a level's board
class Entities:
    pass


class Objects(Entities, Enum):
    MOMO = auto()
    WALL = auto()
    ROCK = auto()
    FLAG = auto()


# Abstract class encompassing all text elements
class Text(Entities):
    pass


# Abstract class encompassing all text elements that can function as subject complements
class Complements(Text):
    pass


class Nouns(Complements, Enum):
    MOMO = auto()
    WALL = auto()
    ROCK = auto()
    FLAG = auto()


class Adjectives(Complements, Enum):
    YOU = auto()
    WIN = auto()
    STOP = auto()
    PUSH = auto()


class Verbs(Text, Enum):
    IS = auto()
    HAS = auto()
