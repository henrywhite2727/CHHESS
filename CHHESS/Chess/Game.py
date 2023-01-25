# from . import Objects
import Objects


class Lawyer:
    pass


def legal_moves(piece: Objects.Piece, board: Objects.Board) -> list[Objects.Square]:
    moves = piece.possible_moves()
    for i in range(len(moves)):
        i_move = moves[i].index()
        colour_i = board.board[i_move[0]][i_move[1]].piece.colour
        if (board.colour and colour_i) or (not board.colour and not colour_i):
            moves.pop(i)
    return moves


def legal_moves_pawn(
    piece: Objects.Piece, board: Objects.Board
) -> list[Objects.Square]:
    pass


def legal_moves_knight(
    piece: Objects.Piece, board: Objects.Board
) -> list[Objects.Square]:
    pass


def legal_moves_bishop(
    piece: Objects.Piece, board: Objects.Board
) -> list[Objects.Square]:
    pass


def legal_moves_rook(
    piece: Objects.Piece, board: Objects.Board
) -> list[Objects.Square]:
    pass


def legal_moves_queen(
    piece: Objects.Piece, board: Objects.Board
) -> list[Objects.Square]:
    pass


def legal_moves_king(
    piece: Objects.Piece, board: Objects.Board
) -> list[Objects.Square]:
    pass


def play():
    pass


def turn():
    pass


def check_check(board: Objects.Board) -> bool:
    """Returns True if the board is in a checked state.

    Args:
        board (Objects.Board): The current board.

    Returns:
        bool: Whether or not the current player is in check.
    """
    # Check every one of opponent's legal moves for King
    for piece in board.active[0 if board.colour else 1]:
        for move in legal_moves(piece, board):
            if isinstance(move.piece, Objects.King) and (
                (move.piece.colour and board.colour)
                or (not move.piece.colour and not board.colour)
            ):
                return True
    return False


def check_mate(board: Objects.Board) -> bool:
    """Returns True if the board is in a checkmate state.

    Args:
        board (Objects.Board): The current board.

    Returns:
        bool: Whether or not the current player is in checkmate.
    """
    for piece in board.active[1 if board.colour else 0]:
        if (
            isinstance(piece, Objects.King)
            and (
                (piece.colour and board.colour)
                or (not piece.colour and not board.colour)
            )
            and len(legal_moves(piece.possible_moves(), board)) == 0
        ):
            return True
    return False


board = Objects.Board(notate=True)
piece = board.active[0][15]
print(board)
print(check_check(board))
print(check_mate(board))

# def move():
#     """
#     get user input
#     confirm it's legal
#     create Event in Sequence
#     move on Board
#     solver/other user's turn
#     loop

#     """


# def move(self, event: Event) -> None:
#     # TODO Implement string interpretation?
#     # TODO I want this to return itself [Hansen]
#     # Assume legal moves by the power of Piece
#     if event.capture:
#         if event.arrive.piece.colour:
#             self.captured[1].append(event.arrive.piece)
#         else:
#             self.captured[0].append(event.arrive.piece)
#     pos_d = event.depart.position.index()
#     pos_a = event.arrive.position.index()
#     self.board[pos_d[0]][pos_d[1]].piece = None
#     self.board[pos_a[0]][pos_a[1]].piece = event.depart.piece


# def get_legal_moves(self, possible_moves: list[tuple]):
#     """This function checks the possible moves and sorts through them and
#     removes illegal moves. The two criteria it looks for
#     are:
#     1. Trying to move a piece to a position not on the board
#     2. Trying to move a piece onto a square where your team already has a piece
#     Args:
#         possible_moves (list of tuples): list of all possible moves a piece can do
#     Returns:
#         legal_moves: list of tuples with subset of possible moves that are legal
#     """
#     legal_moves = []
#     for move in possible_moves:
#         # checking if move is within board
#         if (
#             self.position[0] < 8
#             and self.position[1] < 8
#             and self.position[0] > 0
#             and self.position[1] > 0
#         ):
#             # Checking if square is already occupied by a piece on your team
#             for p in pieces:
#                 if p.colour == self.colour and p.position != move:
#                     legal_moves.extend(move)
#     return legal_moves
