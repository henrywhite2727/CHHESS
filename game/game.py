import numpy as np

# Piece Section
# Colour is a bool for now: 0 for white, 1 for black
# Position is a tuple for now: letter first, then number


class Piece:
    def __init__(self, position: tuple, colour: bool, active: bool = True):
        self.position = position
        self.colour = colour
        self.active = active

    def __str__(self):
        return "implement me"

    def __repr__(self):
        return "implement me"

    def find_legal_moves(self):
        print("please implement me")


class Pawn(Piece):
    def __init__(self, position: tuple, colour: bool, active: bool, value: int):
        super().__init__(position, colour, active)
        self.value = value

    def find_legal_moves(self):
        if self.colour == 0:
            if self.position[1] < 8:
                if self.position[0] == "a":
                    return [("b", self.position[1] + 1)]
                elif self.position[0] == "b":
                    h = 5  ##Use Hansen's code for this line
                else:
                    legal_moves = [
                        (self.position[0] - 1, self.position[1] + 1),
                        (self.position[0] + 1, self.position[1] + 1),
                    ]
            else:
                h = 6  ###use Hansen's code for this line
        else:
            if self.position[1] > 1:
                legal_moves = [
                    (self.position[0] - 1, self.position[1] + 1),
                    (self.position[0] + 1, self.position[1] + 1),
                ]

    def promote(self):
        h = 7  ##unsure what goes in this function
        "implement me"
        pass


class Knight(Piece):
    def __init__(self, position: tuple, colour: bool, active: bool, value: int):
        super().__init__(position, colour, active)
        self.value = value

    def find_legal_moves(self):
        possible_moves = [
            (self.position[0] + 2, self.position[1] + 1),
            (self.position[0] - 2, self.position[1] + 1),
            (self.position[0] + 2, self.position[1] - 1),
            (self.position[0] - 2, self.position[1] - 1),
            (self.position[0] + 1, self.position[1] + 2),
            (self.position[0] - 1, self.position[1] + 2),
            (self.position[0] + 1, self.position[1] - 2),
            (self.position[0] - 1, self.position[1] - 2),
        ]
        legal_moves = get_legal_moves(self, possible_moves)
        return legal_moves


class Rook(Piece):
    def __init__(self, position: tuple, colour: bool, active: bool, value: int):
        super().__init__(position, colour, active)
        self.value = value

    def find_legal_moves(self):
        possible_moves = [
            (self.position[0] + 1, self.position[1]),
            (self.position[0] + 2, self.position[1]),
            (self.position[0] + 3, self.position[1]),
            (self.position[0] + 4, self.position[1]),
            (self.position[0] + 5, self.position[1]),
            (self.position[0] + 6, self.position[1]),
            (self.position[0] + 7, self.position[1]),
            (self.position[0] - 1, self.position[1]),
            (self.position[0] - 2, self.position[1]),
            (self.position[0] - 3, self.position[1]),
            (self.position[0] - 4, self.position[1]),
            (self.position[0] - 5, self.position[1]),
            (self.position[0] - 6, self.position[1]),
            (self.position[0] - 7, self.position[1]),
            (self.position[0], self.position[1] + 1),
            (self.position[0], self.position[1] + 2),
            (self.position[0], self.position[1] + 3),
            (self.position[0], self.position[1] + 4),
            (self.position[0], self.position[1] + 5),
            (self.position[0], self.position[1] + 6),
            (self.position[0], self.position[1] + 7),
            (self.position[0], self.position[1] - 1),
            (self.position[0], self.position[1] - 2),
            (self.position[0], self.position[1] - 3),
            (self.position[0], self.position[1] - 4),
            (self.position[0], self.position[1] - 5),
            (self.position[0], self.position[1] - 6),
            (self.position[0], self.position[1] - 7),
        ]
        legal_moves = get_legal_moves(self, possible_moves)
        return legal_moves


"""
        [('a',1),('b',1)]


henry = King(('d',1), 0, True, 10)
moves = henry.find_legal_moves()
"""

pieces = [
    Pawn,
    Knight,
]  # This list will contain all the piece classes once they're finished


def get_legal_moves(self, possible_moves: list(tuple)):
    """This function checks the possible moves and sorts through them and removes illegal moves. The two criteria it looks for
    are:
    1. Trying to move a piece to a position not on the board
    2. Trying to move a piece onto a square where your team already has a piece
    3. Trying to "jump over" pieces (applies to everything except knights)

    Args:
        possible_moves (list of tuples): list of all possible moves a piece can do

    Returns:
        legal_moves: list of tuples with subset of possible moves that are legal
    """
    legal_moves = []

    for move in possible_moves:
        # checking if move is within board
        if (
            self.position[0] < 8
            and self.position[1] < 8
            and self.position[0] > 0
            and self.position[1] > 0
        ):
            # Checking if square is already occupied by a piece on your team
            for p in pieces:
                if p.colour == self.colour and p.position != move:
                    legal_moves.extend(move)

    return legal_moves


def RookPathCheck(self, possible_moves):
    for move in possible_moves:
        journey = (
            move - self.position
        )  # Journey is a vector that describes the path of the Rook in this possible move

        # Checking if rook path was horizontal (journey[0]=0) or vertical (journey[1]=0)
        if journey[0] == 0:
            for i in range(len(abs(journey[1]))):
                checksign = (
                    1  # this variable tells us whether rook moved forward or back
                )
                if journey[1] > 0:
                    continue_tat = "later"  # continue this later**


# Board Section
rows, cols = 8, 8
board = [[0] * cols] * rows
for i in range(8):
    for j in range(8):
        board[i, j] = 1000 * i + j  # Thus A1=1001 and C4=3004

# History Section
prev_move = [
    "piece used: class",
    "previous location on board",
    "current position on board",
]
