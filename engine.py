# Game engine


# Fully encapsulated Level object handles all game logic
class Level:
    # Input keys (static constants)
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    WAIT = "wait"
    UNDO = "undo"

    def __init__(self, board):
        if len(board) == 0 or len(board[0]) == 0:
            raise ValueError("Invalid board shape; board cannot be empty.")

        if any(len(row) != len(board[0]) for row in board):
            raise ValueError("Invalid board shape; board must be rectangular.")

        self.board = board
        self.height = len(board)
        self.width = len(board[0])

    def process_input(self, key):
        pass

    def get_board(self):
        return self.board
