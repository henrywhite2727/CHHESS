import Piece


class Board:
    def __init__(self) -> None:
        self.board = []


class Square:
    def __init__(self, position: tuple, piece: Piece.Pawn) -> None:
        self.position = position
        self.piece = piece
