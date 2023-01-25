from . import Objects
from . import Piece


def move():
    """
    get user input
    confirm it's legal
    create Event in Sequence
    move on Board
    solver/other user's turn
    loop

    """


def move(self, event: Event) -> None:
    # TODO Implement string interpretation?
    # TODO I want this to return itself [Hansen]
    # Assume legal moves by the power of Piece
    if event.capture:
        if event.arrive.piece.colour:
            self.captured[1].append(event.arrive.piece)
        else:
            self.captured[0].append(event.arrive.piece)
    pos_d = event.depart.position.index()
    pos_a = event.arrive.position.index()
    self.board[pos_d[0]][pos_d[1]].piece = None
    self.board[pos_a[0]][pos_a[1]].piece = event.depart.piece


def get_legal_moves(self, possible_moves: list[tuple]):
    """This function checks the possible moves and sorts through them and removes illegal moves. The two criteria it looks for
    are:
    1. Trying to move a piece to a position not on the board
    2. Trying to move a piece onto a square where your team already has a piece
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
