import Piece
import Board


class Sequence:
    def __init__(self) -> None:
        pass


class Event:
    def __init__(
        self, depart: Board.Square, arrive: Board.Square, disam: int = 0
    ) -> None:
        # Assume legal moves as settled in Piece
        self.depart = depart
        self.arrive = arrive
        self.capture = False
        if self.arrive.piece is not None:
            self.capture = True
        self.disam = disam

    def __str__(self):
        string = str(self.depart.piece)
        if self.disam == 1:
            string += Board.pos_to_str(self.arrive.position)[0]

        if self.capture:
            string += "x"
        string += Board.pos_to_str(self.arrive.position)


b = "string"
print(b[0])
