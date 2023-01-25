from typing import Union


class Position:
    """Representation of a coordinate on a chess board.

    Variables:
        file (int): Column-like position on chess board. The a-file corresponds
            to a value of 1, b-file to a value of 2, and so on.
        rank (int): Row-like position on chess board. The 1st rank corresponds
            to a value of 1, 2nd rank to a value of 2, and so on.
    """

    def __init__(
        self, position: Union[tuple[int], tuple[str, int], str], mode: int = 0
    ) -> None:
        """Initializes a Position object.

        Args:
            position (Union[tuple[int], tuple[str, int], str]): Coordinates.
            mode (int, optional): Mode of initiation. Defaults to 0.
                0 (tuple[int, int]): Board index, i.e. (1, 3)
                1 (tuple[int, int]): Position coordinates, i.e. (4, 2)
                2 (tuple[str, int]): Tupled algebraic notation, i.e. ("d", 2)
                3 (str): Algebraic notation, i.e. "d2"

        Raises:
            ValueError: Invalid initialization mode (see Args > mode for options).
            ValueError: Position out of bounds on board.
        """
        match mode:
            case 0:
                self.file = position[1] + 1
                self.rank = position[0] + 1
            case 1:
                self.file = position[0]
                self.rank = position[1]
            case 2:
                self.file = ord(position[0]) - ord("a")
                self.rank = position[1]
            case 3:
                self.file = ord(position[0]) - ord("a") + 1
                self.rank = ord(position[1]) - ord("1") + 1
            case _:
                raise ValueError("Invalid mode for position initialization.")
        if self.file < 1 or self.file > 8 or self.rank < 1 or self.rank > 8:
            raise ValueError(
                "Position ("
                + str(self.file)
                + ", "
                + str(self.rank)
                + ") out of bounds."
            )

    def __str__(self) -> str:
        """Returns representation of Position as a string in algebraic notation.

        Returns:
            str: Algebraic representation of Position.
        """
        return chr(self.file + ord("a") - 1) + str(self.rank)

    def index(self) -> tuple[int]:
        """Returns representation of Position as indices on the Board list.

        Returns:
            tuple[int]: Board index representation of Position.
        """
        return (self.rank - 1, self.file - 1)


class Piece:
    def __init__(self, position: Position, colour: bool, active: bool = True) -> None:
        self.position = position
        self.colour = colour
        self.active = active

    def __str__(self) -> str:
        return NotImplementedError(
            "This Piece's class __str__ has not been implemented"
        )

    def find_legal_moves(self) -> list:
        raise NotImplementedError(
            "This Piece's class find_legal_moves has not been implemented"
        )


class Pawn(Piece):
    value = 1

    def __init__(self, position: Position, colour: bool, active: bool = True) -> None:
        """Initializes Pawn object.

        Args:
            position (Position): Position of piece on board.
            colour (bool): Colour of piece.
            active (bool, optional): If the piece is on the board. Defaults to True.
        """
        super().__init__(position, colour, active)

    def __str__(self) -> str:
        """Returns representation of Pawn as a string.

        Returns:
            str: String representation of pawn.
        """
        return "P" if self.colour else "p"

    def possible_moves(self) -> list[Position]:
        """Returns all possible moves for this Pawn.

        Returns:
            list[Position]: Every advancing position possible for this pawn, this move.
        """
        moves = []

        # Beginning pawn can advance up to two ranks
        if (not self.colour and self.position.rank == 2) or (
            self.colour and self.position.rank == 7
        ):
            moves.append(
                Position(
                    (
                        self.position.file,
                        self.position.rank + (-2 if self.colour else 2),
                    ),
                    mode=1,
                )
            )

        files = range(
            max(1, self.position.file - 1), min(8, self.position.file + 1) + 1
        )
        for file in files:
            moves.append(
                Position(
                    (file, self.position.rank + (-1 if self.colour else 1)), mode=1
                )
            )
        return moves

    def promote(self):
        pass


class Knight(Piece):
    value = 3

    def __init__(self, position: Position, colour: bool, active: bool = True) -> None:
        """Initializes Knight object.

        Args:
            position (Position): Position of piece on board.
            colour (bool): Colour of piece.
            active (bool, optional): If the piece is on the board. Defaults to True.
        """
        super().__init__(position, colour, active)

    def __str__(self) -> str:
        """Returns representation of Knight as a string.

        Returns:
            str: String representation of knight.
        """
        return "N" if self.colour else "n"

    def possible_moves(self) -> list[Position]:
        """Returns all possible moves for this Knight.

        Returns:
            list[Position]: Every advancing position possible for this knight, this move.
        """
        moves = []

        wide = [
            [self.position.file - 2, self.position.file + 2],
            [self.position.rank - 1, self.position.rank + 1],
        ]
        tall = [
            [self.position.file - 1, self.position.file + 1],
            [self.position.rank - 2, self.position.rank + 2],
        ]

        for i in (0, 1):
            for j in (0, 1):
                if wide[i][j] < 1 or wide[i][j] > 8:
                    wide[i].pop(j)
                if tall[i][j] < 1 or tall[i][j] > 8:
                    tall[i].pop(j)

        for file in wide[0]:
            for rank in wide[1]:
                moves.append(Position((file, rank), mode=1))
        for file in tall[0]:
            for rank in tall[1]:
                moves.append(Position((file, rank), mode=1))

        return moves


knight = Knight(Position("d8", mode=3), False)
moves = knight.possible_moves()
for move in moves:
    print(move)


class Square:
    """Representation of a square on a chess board.

    Variables:
        position (Position): Position object representing position of Square on the board.
        piece (Piece): Piece object on the Square, if any. None if none.
    """

    def __init__(self, position: Position, piece: Piece = None) -> None:
        """Initializes a Square object.

        Args:
            position (Position): Position object representing position on the board.
            piece (Piece.Piece, optional): Piece occupying the Square. Defaults to None.
        """
        self.position = position
        self.piece = piece

    def __str__(self) -> str:
        """Returns representation of Square as a string. Prints one character
        representing occupying Piece, and '-' if empty.

        Returns:
            str: Algebraic representation of Square.
        """
        if self.piece is None:
            return "-"
        else:
            return str(self.piece)


class Event:
    def __init__(
        self, depart: Square, arrive: Square, mode: str = "SAN", disam: int = 0
    ) -> None:
        # TODO implement other notations
        # Assume legal moves by the power of Piece
        self.depart = depart
        self.arrive = arrive
        self.capture = False
        if self.arrive.piece is not None:
            self.capture = True
        if self.disam is not None and self.disam not in (0, 1, 2, 3):
            raise ValueError("Invalid disambiguation mode " + str(self.disam) + ".")
        self.disam = disam
        self.mode = mode

    def __str__(self):
        string = str(self.depart.piece)
        if self.disam == 1:
            string += str(self.depart.position)[0]
        elif self.disam == 2:
            string += str(self.depart.position.rank)
        elif self.disam == 3:
            string += str(self.depart.position)
        if self.capture:
            string += "x"
        string += str(self.arrive.position)
        return string


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

    def add_event(self, event: Event):
        self.sequence.append(event)


class Board:
    """Representation of a chess board.

    Variables:
        board (list[list[Square]]): 8x8 2D list of Square objects, representing the board.
        captured (list[list[Piece]]): 2x1 list of Piece objects, representing
            captured pieces. The 1st index refers to white pieces, the 2nd refers to black.
    """

    def __init__(self, sequence: Sequence = None) -> None:
        if sequence is None:
            # Initialize empty board
            self.board: list[list[Square]] = [
                [Square((j + 1, i)) for j in range(8)] for i in range(8)
            ]

            # Initialize white pieces
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

            # Initialize black pieces
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
