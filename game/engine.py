# Game Engine

from entities import *


# --- Primary Engine Class; handles all game logic --- #
class Level:
    # input keys TODO replace with internal enum?
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    WAIT = "wait"
    UNDO = "undo"

    # valid rule patterns
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
        self.implicit_rules = [(Text, Verbs.IS, Adjectives.PUSH)]
        self.parse_rules_from_board()

    # Primary API method; handles all processing for a given input key
    def process_input(self, key):
        print("\nprocess_input(%s)" % key)
        if key in (Level.UP, Level.DOWN, Level.LEFT, Level.RIGHT):
            self.handle_motion(key)
        self.parse_rules_from_board()  # TODO: only call this when handle_motion actually has an effect
        self.apply_reactive_rules()

    def get_tile_at(self, x, y):
        return self.board[y][x]

    # Handles all level motion; assumes that self.rules_dict is constant
    def handle_motion(self, direction_key):
        print("\thandle_motion(%s)" % direction_key)

        yous = []
        for y in range(self.height):
            for x in range(self.width):
                for entity in self.get_tile_at(x, y):
                    if self.get_ruling(entity, Verbs.IS, Adjectives.YOU):
                        yous.append((entity, (x, y)))
        # print("\t\tyous:", yous)

        if len(yous) == 0:
            print("\t\tyou are nothing!!!")
            return

        displacement_vector = {
            Level.UP: (0, -1),
            Level.DOWN: (0, 1),
            Level.LEFT: (-1, 0),
            Level.RIGHT: (1, 0)
        }[direction_key]

        for you in yous:
            entity, starting_coords = you
            target_coords = (starting_coords[0] + displacement_vector[0], starting_coords[1] + displacement_vector[1])

            # check for out of bounds
            if not self.is_in_bounds(target_coords):
                continue

            # check for moving into STOP
            if any(self.get_ruling(e, Verbs.IS, Adjectives.STOP) for e in self.get_tile_at(*target_coords)):
                continue

            # check for moving into PUSH
            # TODO

            # move entity
            self.move_entity(entity, starting_coords, target_coords)

    def is_in_bounds(self, tile_coords):
        return 0 <= tile_coords[0] < self.width and 0 <= tile_coords[1] < self.height

    def move_entity(self, entity, starting_coords, ending_coords):
        self.get_tile_at(*starting_coords).remove(entity)
        self.get_tile_at(*ending_coords).append(entity)

    # Adds a given rule to self.rules_dict
    # (object, verb, complement)
    def add_rule(self, subject, predicate, complement):
        if subject not in self.rules_dict.keys():
            self.rules_dict[subject] = {}
        object_rules = self.rules_dict[subject]

        if predicate not in object_rules.keys():
            object_rules[predicate] = set()

        object_rules[predicate].add(complement)

    # Returns a ruling (T/F) for the given rule query based on the current state of self.rules_dict
    def get_ruling(self, subject, predicate, complement):
        if isinstance(subject, Text):  # ignore text subtype
            subject = Text

        if subject not in self.rules_dict.keys():
            return False
        object_rules = self.rules_dict[subject]

        if predicate not in object_rules:
            return False

        return complement in object_rules[predicate]

    # Call add_rule() on all 'implicit' rules
    def add_implicit_rules(self):
        for rule in self.implicit_rules:
            self.add_rule(*rule)

    # Scans the board for valid text patterns and calls add_rule() on all matches
    # TODO: research how Baba handles case of overlapping text
    def parse_rules_from_board(self):
        print("\tparse_rules_from_board()")

        self.rules_dict.clear()
        self.add_implicit_rules()

        # horizontal scan
        for x in range(self.width - 2):
            for y in range(self.height):
                tiles = [self.get_tile_at(x + offset, y) for offset in range(3)]
                filtered_tiles = [list(filter(lambda e: isinstance(e, Text), tile)) for tile in tiles]
                if all(len(tile) > 0 for tile in filtered_tiles):
                    texts = [tile[0] for tile in filtered_tiles]  # only examine first Text instance found
                    if any(matches_pattern(pattern, texts) for pattern in self.rule_patterns):
                        self.add_rule(get_object_from_noun(texts[0]), texts[1], texts[2])

        # vertical scan
        for x in range(self.width):
            for y in range(self.height - 2):
                tiles = [self.get_tile_at(x, y + offset) for offset in range(3)]
                filtered_tiles = [list(filter(lambda e: isinstance(e, Text), tile)) for tile in tiles]
                if all(len(tile) > 0 for tile in filtered_tiles):
                    texts = [tile[0] for tile in filtered_tiles]  # only examine first Text instance found
                    if any(matches_pattern(pattern, texts) for pattern in self.rule_patterns):
                        self.add_rule(get_object_from_noun(texts[0]), texts[1], texts[2])

        print("\t\trules_dict:", self.rules_dict)

    # Applies all 'reactive' rules (i.e. win, sink, move)
    def apply_reactive_rules(self):
        print("\tapply_reactive_rules()")
        for x in range(self.width):
            for y in range(self.height):
                tile = self.get_tile_at(x, y)
                for entity in tile[:]:  # iterate over copy of tile to avoid concurrent modification issues

                    # check for YOU intersections
                    if self.get_ruling(entity, Verbs.IS, Adjectives.YOU):
                        if any(self.get_ruling(e, Verbs.IS, Adjectives.WIN) for e in tile):  # YOU/WIN
                            print("\t\tcongrats! you beat the level!")
                        if any(self.get_ruling(e, Verbs.IS, Adjectives.DEFEAT) for e in tile):  # YOU/DEFEAT
                            tile.remove(entity)


# --- Helper Functions --- #

# Returns True iff the given entity list matches the given pattern
def matches_pattern(pattern, entities):
    return all(entity == target or (isinstance(target, type) and isinstance(entity, target)) for target, entity in
               zip(pattern, entities))


# Returns the object corresponding to the given noun
def get_object_from_noun(noun):
    return noun_object_map[noun]
