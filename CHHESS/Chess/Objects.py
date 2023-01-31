# TODO write __repr__ for every class
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
                self.file: int = position[1] + 1
                self.rank: int = position[0] + 1
            case 1:
                self.file: int = position[0]
                self.rank: int = position[1]
            case 2:
                self.file: int = ord(position[0]) - ord("a")
                self.rank: int = position[1]
            case 3:
                self.file: int = ord(position[0]) - ord("a") + 1
                self.rank: int = ord(position[1]) - ord("1") + 1
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
        self.position: Position = position
        self.colour: bool = colour
        self.active: bool = active

    def __str__(self) -> str:
        return NotImplementedError(
            "This Piece's class __str__ has not been implemented"
        )

    def possible_moves(self) -> list[Position]:
        raise NotImplementedError(
            "This Piece's class possible_moves has not been implemented"
        )


class Pawn(Piece):
    value: int = 1

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
        moves: list[Position] = []

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


class Knight(Piece):
    value: int = 3

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
        moves: list[Position] = []

        wide = [
            [self.position.file - 2, self.position.file + 2],
            [self.position.rank - 1, self.position.rank + 1],
        ]
        tall = [
            [self.position.file - 1, self.position.file + 1],
            [self.position.rank - 2, self.position.rank + 2],
        ]

        for file in wide[0]:
            for rank in wide[1]:
                if file >= 1 and file <= 8 and rank >= 1 and rank <= 8:
                    moves.append(Position((file, rank), mode=1))
        for file in tall[0]:
            for rank in tall[1]:
                if file >= 1 and file <= 8 and rank >= 1 and rank <= 8:
                    moves.append(Position((file, rank), mode=1))
        return moves


class Bishop(Piece):
    value: int = 3

    def __init__(self, position: Position, colour: bool, active: bool = True) -> None:
        """Initializes Bishop object.

        Args:
            position (Position): Position of piece on board.
            colour (bool): Colour of piece.
            active (bool, optional): If the piece is on the board. Defaults to True.
        """
        super().__init__(position, colour, active)

    def __str__(self) -> str:
        """Returns representation of Bishop as a string.

        Returns:
            str: String representation of bishop.
        """
        return "B" if self.colour else "b"

    def possible_moves(self) -> list[Position]:
        """Returns all possible moves for this Bishop.

        Returns:
            list[Position]: Every advancing position possible for this bishop, this move.
        """
        moves: list[Position] = []

        for file in range(1 - self.position.file, 8 - self.position.file + 1):
            for rank in range(1 - self.position.rank, 8 - self.position.rank + 1):
                if abs(rank) == abs(file) and rank != 0:
                    moves.append(
                        Position(
                            (self.position.file + file, self.position.rank + rank),
                            mode=1,
                        )
                    )

        return moves


class Rook(Piece):
    value: int = 5

    def __init__(self, position: Position, colour: bool, active: bool = True) -> None:
        """Initializes Rook object.

        Args:
            position (Position): Position of piece on board.
            colour (bool): Colour of piece.
            active (bool, optional): If the piece is on the board. Defaults to True.
        """
        super().__init__(position, colour, active)

    def __str__(self) -> str:
        """Returns representation of Rook as a string.

        Returns:
            str: String representation of rook.
        """
        return "R" if self.colour else "r"

    def possible_moves(self) -> list[Position]:
        """Returns all possible moves for this Rook.

        Returns:
            list[Position]: Every advancing position possible for this rook, this move.
        """
        moves: list[Position] = []

        for n in range(1, 8 + 1):
            if n != self.position.file:
                moves.append(Position((n, self.position.rank), mode=1))
            if n != self.position.rank:
                moves.append(Position((self.position.file, n), mode=1))

        return moves


class Queen(Piece):
    value: int = 9

    def __init__(self, position: Position, colour: bool, active: bool = True) -> None:
        """Initializes Queen object.

        Args:
            position (Position): Position of piece on board.
            colour (bool): Colour of piece.
            active (bool, optional): If the piece is on the board. Defaults to True.
        """
        super().__init__(position, colour, active)

    def __str__(self) -> str:
        """Returns representation of Queen as a string.

        Returns:
            str: String representation of queen.
        """
        return "Q" if self.colour else "q"

    def possible_moves(self) -> list[Position]:
        """Returns all possible moves for this Queen.

        Returns:
            list[Position]: Every advancing position possible for this queen, this move.
        """
        moves: list[Position] = []

        for file in range(1 - self.position.file, 8 - self.position.file + 1):
            for rank in range(1 - self.position.rank, 8 - self.position.rank + 1):
                if abs(rank) == abs(file) and rank != 0:
                    moves.append(
                        Position(
                            (self.position.file + file, self.position.rank + rank),
                            mode=1,
                        )
                    )

        for n in range(1, 8 + 1):
            if n != self.position.file:
                moves.append(Position((n, self.position.rank), mode=1))
            if n != self.position.rank:
                moves.append(Position((self.position.file, n), mode=1))

        return moves


class King(Piece):
    value: int = 10

    def __init__(self, position: Position, colour: bool, active: bool = True) -> None:
        """Initializes King object.

        Args:
            position (Position): Position of piece on board.
            colour (bool): Colour of piece.
            active (bool, optional): If the piece is on the board. Defaults to True.
        """
        super().__init__(position, colour, active)

    def __str__(self) -> str:
        """Returns representation of King as a string.

        Returns:
            str: String representation of king.
        """
        return "K" if self.colour else "k"

    def possible_moves(self) -> list[Position]:
        """Returns all possible moves for this King.

        Returns:
            list[Position]: Every advancing position possible for this king, this move.
        """
        moves: list[Position] = []

        for file in range(
            max(1, self.position.file - 1), min(8, self.position.file + 1) + 1
        ):
            for rank in range(
                max(1, self.position.rank - 1), min(8, self.position.rank + 1) + 1
            ):
                if file != self.position.file or rank != self.position.rank:
                    moves.append(Position((file, rank), mode=1))

        return moves


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
        self.position: Position = position
        self.piece: Piece = piece

    def __str__(self) -> str:
        """Returns representation of Square as a string. Prints one character
        representing occupying Piece, and '-' if empty.

        Returns:
            str: Algebraic representation of Square.
        """
        if self.piece is None:
            # return "=" if (self.position.file + self.position.rank) % 2 == 0
            # else "-"
            return "-"
        else:
            return str(self.piece)


class Event:
    def __init__(
        self,
        depart: Square,
        arrive: Square,
        mode: Union[str, int] = 4,
        disam: int = 0,
    ) -> None:
        # TODO implement other notations
        # Assume legal moves by the power of Referee
        self.depart: Square = depart
        self.arrive: Square = arrive
        self.capture: bool = False
        if self.arrive.piece is not None:
            self.capture = True
        self.disam: int = disam
        if self.disam not in (0, 1, 2, 3):
            raise ValueError("Invalid disambiguation mode " + str(self.disam) + ".")
        self.mode: str = mode

    def __str__(self):
        if (
            isinstance(self.mode, str)
            and self.mode == "SAN"
            or isinstance(self.mode, int)
            and self.mode == 0
        ):
            string = str(self.depart.piece)
            match self.disam:
                case 1:
                    string += str(self.depart.position)[0]
                case 2:
                    string += str(self.depart.position.rank)
                case 3:
                    string += str(self.depart.position)
            if self.capture:
                string += "x"
            string += str(self.arrive.position)
            return string
        elif (
            isinstance(self.mode, str)
            and self.mode == "LAN"
            or isinstance(self.mode, int)
            and self.mode == 1
        ):
            raise NotImplementedError()
        elif (
            isinstance(self.mode, str)
            and self.mode == "ICFF"
            or isinstance(self.mode, int)
            and self.mode == 2
        ):
            raise NotImplementedError()
        elif (
            isinstance(self.mode, str)
            and self.mode == "PGN"
            or isinstance(self.mode, int)
            and self.mode == 3
        ):
            raise NotImplementedError()
        elif (
            isinstance(self.mode, str)
            and self.mode == "HHN"
            or isinstance(self.mode, int)
            and self.mode == 4
        ):
            return str(self.depart.position) + " " + str(self.arrive.position)


class Sequence:
    def __init__(self, mode: Union[str, int] = 3, sequence: list[str] = None) -> None:
        if sequence is not None:
            # TODO Initialize from input
            if (
                isinstance(mode, str)
                and mode == "SAN"
                or isinstance(mode, int)
                and mode == 0
            ):
                raise NotImplementedError()
            elif (
                isinstance(mode, str)
                and mode == "LAN"
                or isinstance(mode, int)
                and mode == 1
            ):
                raise NotImplementedError()
            elif (
                isinstance(mode, str)
                and mode == "ICFF"
                or isinstance(mode, int)
                and mode == 2
            ):
                raise NotImplementedError()
            elif (
                isinstance(mode, str)
                and mode == "PGN"
                or isinstance(mode, int)
                and mode == 3
            ):
                pass
            else:
                raise ValueError("Invalid game notation standard.")
            self.mode: str = mode
        else:
            self.sequence: list[str] = []
            self.moves: int = 0

            # PGN match data
            self.event: str = ""
            self.site: str = ""
            self.date: list[int] = []
            self.date_event: list[int] = []
            self.round: int = 0
            self.result: list[int] = []
            self.white: str = ""
            self.black: str = ""
            self.eco: str = ""
            self.elo_white: int = 0
            self.elo_black: int = 0
            self.count_ply: int = 0

    def __str__(self):
        string = ""
        for i in range(len(self.sequence)):
            string += str(i + 1) + ". " + str(self.sequence[i]) + " "
        return string

    def add_event(self, event: Event):
        self.sequence.append(str(event))


class Board:
    """Representation of a chess board.

    Variables:
        board (list[list[Square]]): 8x8 2D list of Square objects, representing
        the board.
        active (list[list[Piece]]): 2x1 list of Piece objects, representing
            active pieces. The 1st index refers to white pieces, the 2nd
            refers to black.
        captured (list[list[Piece]]): 2x1 list of Piece objects, representing
            captured pieces. The 1st index refers to white pieces, the 2nd
            refers to black.
        colour (bool): Colour corresponding to the player who moves next.
        notate (bool): Toggles algebraic notation display.
        sequence (Sequence): Sequence representing move history.
    """

    def __init__(self, sequence: Sequence = None, notate: bool = False) -> None:
        if sequence is None:
            # Initialize empty Sequence
            self.sequence: Sequence = Sequence()

            # Initialize empty list of active pieces
            self.active: list[list[Piece]] = [[], []]

            # Initialize empty list of captured pieces
            self.captured: list[list[Piece]] = [[], []]

            # White begins
            self.colour: bool = False

            # Default no notation
            self.notate: bool = notate

            # Initialize empty board
            self.board: list[list[Square]] = [
                [Square(Position((file, rank))) for rank in range(8)]
                for file in range(8)
            ]

            # Initialize pieces
            for colour in (False, True):
                for file in range(8):
                    rank = 6 if colour else 1
                    i_c = 1 if colour else 0
                    self.active[i_c].append(Pawn(Position((rank, file)), colour))
                    self.board[rank][file].piece = self.active[i_c][-1]
                rank = 7 if colour else 0
                for file in (0, 7):
                    self.active[i_c].append(Rook(Position((rank, file)), colour))
                    self.board[rank][file].piece = self.active[i_c][-1]
                for file in (1, 6):
                    self.active[i_c].append(Knight(Position((rank, file)), colour))
                    self.board[rank][file].piece = self.active[i_c][-1]
                for file in (2, 5):
                    self.active[i_c].append(Bishop(Position((rank, file)), colour))
                    self.board[rank][file].piece = self.active[i_c][-1]
                self.active[i_c].append(Queen(Position((rank, 3)), colour))
                self.board[rank][3].piece = self.active[i_c][-1]
                self.active[i_c].append(King(Position((rank, 4)), colour))
                self.board[rank][4].piece = self.active[i_c][-1]
        else:
            self.sequence: Sequence = sequence
            # TODO Implement creating board from sequence
            pass

    def __str__(self) -> str:
        string = ""
        if self.colour:
            if self.notate:
                string += "  h g f e d c b a\n"
            string += " _________________\n"
            for i in range(len(self.board)):
                string += "| "
                for j in range(len(self.board) - 1, -1, -1):
                    string += str(self.board[i][j]) + " "
                string += "| "
                if self.notate:
                    string += str(i + 1)
                string += "\n"
            string += " ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾"

        else:
            if self.notate:
                string += "  "
            string += " _________________\n"
            for i in range(len(self.board) - 1, -1, -1):
                if self.notate:
                    string += str(i + 1) + " "
                string += "| "
                for j in range(len(self.board[i])):
                    string += str(self.board[i][j]) + " "
                string += "|\n"
            if self.notate:
                string += "  "
            string += " ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾"
            if self.notate:
                string += "\n    a b c d e f g h"
        return string
