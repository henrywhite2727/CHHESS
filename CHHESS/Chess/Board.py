from . import Piece


class Square:
    def __init__(self, position: tuple, piece: Piece.Piece = None) -> None:
        self.position = position
        self.piece = piece

    def __str__(self) -> str:
        if self.piece is None:
            return "-"
        else:
            return str(self.piece)


class Sequence:
    def __init__(self, mode: str = "SAN") -> None:
        # TODO Initialize from input
        if mode != "SAN":
            if mode == "LAN":
                pass
            elif mode == "PGN":
                pass
            else:
                raise ValueError("Invalid game notation standard.")
        self.mode = mode
        self.sequence = []
        self.moves = 0

    def __str__(self):
        string = ""
        for i in range(len(self.sequence)):
            string += str(i) + ". " + str(self.sequence[i]) + " "


class Event:
    def __init__(
        self, depart: Square, arrive: Square, mode: str = "SAN", disam: int = 0
    ) -> None:
        # Assume legal moves by the power of Piece
        self.depart = depart
        self.arrive = arrive
        self.capture = False
        if self.arrive.piece is not None:
            self.capture = True
        self.disam = disam
        self.mode = mode

    def __str__(self):
        string = str(self.depart.piece)
        if self.disam == 1:
            string += pos_to_str(self.depart.position)[0]
        elif self.disam == 2:
            string += self.depart.position[1]
        elif self.disam == 3:
            string += pos_to_str(self.depart.position)
        if self.capture:
            string += "x"
        string += pos_to_str(self.arrive.position)
        return string


class Board:
    def __init__(self, sequence: Sequence = None) -> None:
        if sequence is None:
            # Initialize empty board
            self.board: list[list[Square]] = [
                [Square((j + 1, i)) for j in range(8)] for i in range(8)
            ]

            # Setup white pieces
            for j in range(8):
                self.board[1][j].piece = Piece.Pawn((j + 1, 2), False, True)
            for j in [0, 7]:
                self.board[0][j].piece = Piece.Rook((j + 1, 1), False, True)
            for j in [1, 6]:
                self.board[0][j].piece = Piece.Knight((j + 1, 1), False, True)
            for j in [2, 5]:
                self.board[0][j].piece = Piece.Bishop((j + 1, 1), False, True)
            self.board[0][3].piece = Piece.Queen((4, 1), False, True)
            self.board[0][4].piece = Piece.King((5, 1), False, True)

            # Setup black pieces
            for j in range(8):
                self.board[6][j].piece = Piece.Pawn((j + 1, 7), False, True)
            for j in [0, 7]:
                self.board[7][j].piece = Piece.Rook((j + 1, 8), False, True)
            for j in [1, 6]:
                self.board[7][j].piece = Piece.Knight((j + 1, 8), False, True)
            for j in [2, 5]:
                self.board[7][j].piece = Piece.Bishop((j + 1, 8), False, True)
            self.board[7][3].piece = Piece.Queen((4, 8), False, True)
            self.board[7][4].piece = Piece.King((5, 8), False, True)

            self.captured: list[list[Piece.Piece]] = [[], []]
        else:
            "Implement creating board from sequence"
            self.board: list[list[Square]] = []

    def __str__(self) -> str:
        string = ""
        for i in range(len(self.board) - 1, -1, -1):
            string += str(i + 1) + "  "
            for j in range(len(self.board[i])):
                string += str(self.board[i][j]) + " "
            string += "\n"
        string += "   a b c d e f g h"
        return string

    def move(self, event: Event) -> None:
        # TODO Implement string interpretation?
        # TODO I want this to return itself [Hansen]
        # Assume legal moves by the power of Piece
        if event.capture:
            if event.arrive.piece.colour:
                self.captured[1].append(event.arrive.piece)
            else:
                self.captured[0].append(event.arrive.piece)
        pos_d = pos_to_ind(event.depart.position)
        pos_a = pos_to_ind(event.arrive.position)
        self.board[pos_d[0]][pos_d[1]].piece = None
        self.board[pos_a[0]][pos_a[1]].piece = event.depart.piece


# These functions make it seem like we should write a Position class but it
# seems extra


def pos_to_ind(position: tuple[int]) -> tuple[int]:
    """Takes a position tuple and returns it in its indices on the Board.

    Args:
        position (tuple[int]): position in coordinate form

    Raises:
        ValueError: If position is out of bounds

    Returns:
        tuple[int]: position on Board object
    """
    if (
        len(position) > 2
        or position[0] < 1
        or position[0] > 8
        or position[1] < 1
        or position[1] > 8
    ):
        raise ValueError("Invalid position value " + str(position))
    return (position[1] - 1, position[0] - 1)


def ind_to_pos(index: tuple[int]) -> tuple[int]:
    """Takes a position as indexed on the Board and returns it in coordinate form.

    Args:
        index (tuple[int]): position on Board object

    Raises:
        ValueError: If position is out of bounds

    Returns:
        tuple[int]: position in coordinate form
    """
    if len(index) > 2 or index[0] < 1 or index[0] > 8 or index[1] < 1 or index[1] > 8:
        raise ValueError("Invalid position value " + str(index))
    return (index[1] + 1, index[0] + 1)


def pos_to_str(position: tuple[int]) -> str:
    """Takes a position tuple and returns it in string representation.

    Example:
    > square = Square((1,1))
    > print(Board.pos_to_str(square.position))
    >> a1

    Args:
        position (tuple[int]): Two coordinate int elements from 1 to 8

    Raises:
        ValueError: If position is out of bounds

    Returns:
        str: String representation of coordinate position
    """
    if (
        len(position) > 2
        or position[0] < 1
        or position[0] > 8
        or position[1] < 1
        or position[1] > 8
    ):
        raise ValueError("Invalid position value " + str(position))
    return chr(position[0] + ord("a") - 1) + str(position[1])


def str_to_pos(pos: str) -> tuple[int]:
    """Takes a position string and returns it in int representation.

    Example:
    > square = Square(Board.str_to_pos("b2"))
    > print(square.position)
    >> (2, 2)

    Args:
        pos (str): String representation of position

    Raises:
        ValueError: If position is invalid

    Returns:
        tuple[int]: Integer representation of position (see standards.txt)
    """
    x, y = int(ord(pos[0]) - ord("a")) + 1, int(pos[1])
    if len(pos) != 2 or x < 1 or x > 8 or y < 1 or y > 8:
        raise ValueError("Invalid position string " + pos + ".")
    return (x, y)
