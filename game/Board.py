from . import Piece


class Board:
    def __init__(self, new: bool = True) -> None:
        if new:
            self.board: list[list[Square]] = []

            for i in range(1, 9):
                self.board.append([])
                for j in range(1, 9):
                    self.board.append([Square(position=(i, j))])

        else:
            self.board: list[list[Square]] = []


class Square:
    def __init__(self, position: tuple, piece: Piece.Piece = None) -> None:
        self.position = position
        self.piece = piece

    def __str__(self) -> str:
        return pos_to_str(self.position) + ": " + str(self.piece)


def pos_to_str(position: tuple) -> str:
    if position[0] < 1 or position[0] > 8 or position[1] < 1 or position[1] > 8:
        raise ValueError(
            "Invalid position value ("
            + str(position[0])
            + ", "
            + str(position[1])
            + ")."
        )
    return chr(position[0] + ord("a") - 1) + str(position[1])
