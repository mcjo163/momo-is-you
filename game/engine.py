# Game engine

from game.entities import *


# Fully encapsulated Level object handles all game logic
class Level:
    # Input keys (static constants) TODO replace with internal enum
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    WAIT = "wait"
    UNDO = "undo"

    # Valid rule patterns
    rule_patterns = [[Nouns, Verbs.IS, Complements],
                     [Nouns, Verbs.HAS, Nouns]]

    def __init__(self, board):
        if len(board) == 0 or len(board[0]) == 0:
            raise ValueError("Invalid board shape; board cannot be empty.")

        if any(len(row) != len(board[0]) for row in board):
            raise ValueError("Invalid board shape; board must be rectangular.")

        if any(any(any(not isinstance(value, Entities) for value in tile) for tile in row) for row in board):
            raise ValueError("Invalid board contents; board can only contain Entities.")

        self.board = board
        self.height = len(board)
        self.width = len(board[0])

        self.rules_dict = {}
        self.parse_rules_from_board()

    def process_input(self, key):
        print("\nprocess_input(%s)" % key)
        if key in (Level.UP, Level.DOWN, Level.LEFT, Level.RIGHT):
            self.handle_motion(key)
        self.parse_rules_from_board()   # TODO: only call this when handle_motion actually has an effect
        self.apply_reactive_rules()

    def handle_motion(self, direction_key):
        print("\thandle_motion(%s)" % direction_key)

    def add_rule(self, subject, predicate, complement):
        if subject not in self.rules_dict.keys():
            self.rules_dict[subject] = {}
        object_rules = self.rules_dict[subject]

        if predicate not in object_rules.keys():
            object_rules[predicate] = set()

        object_rules[predicate].add(complement)

    def parse_rules_from_board(self):
        print("\tparse_rules_from_board()")

        self.rules_dict.clear()

        # horizontal scan
        for row in self.board:
            for x in range(self.width - 2):
                filtered_tiles = [list(filter(lambda e: isinstance(e, Text), tile)) for tile in row[x:x + 3]]
                if all(len(tile) > 0 for tile in filtered_tiles):
                    entities = [tile[0] for tile in filtered_tiles]     # only examine first Text instance found TODO: research how Baba handles case of overlapping text
                    if any(matches_pattern(pattern, entities) for pattern in self.rule_patterns):
                        # print("\thorizontal match found!")
                        self.add_rule(*entities)

        # vertical scan
        for x in range(self.width):
            for y in range(self.height - 2):
                tiles = [self.board[y + offset][x] for offset in range(3)]
                filtered_tiles = [list(filter(lambda e: isinstance(e, Text), tile)) for tile in tiles]
                if all(len(tile) > 0 for tile in filtered_tiles):
                    entities = [tile[0] for tile in filtered_tiles]     # only examine first Text instance found TODO: research how Baba handles case of overlapping text
                    if any(matches_pattern(pattern, entities) for pattern in self.rule_patterns):
                        # print("\tvertical match found!")
                        self.add_rule(*entities)

        print("\trules_dict:", self.rules_dict)

    def apply_reactive_rules(self):
        print("\tapply_reactive_rules()")


# Helper Functions
def matches_pattern(pattern, entities):
    return all(entity == target or (isinstance(target, type) and isinstance(entity, target)) for target, entity in zip(pattern, entities))
