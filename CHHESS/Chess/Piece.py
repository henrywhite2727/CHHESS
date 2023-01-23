class Piece:
    def __init__(self, position: tuple, colour: bool, active: bool = True) -> None:
        if position[0] < 1 or position[0] > 8 or position[1] < 1 or position[1] > 8:
            raise ValueError("Piece must have coordinates between a1 and h8.")
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

    def __init__(self, position: tuple, colour: bool, active: bool = True) -> None:
        super().__init__(position, colour, active)

    def __str__(self):
        if self.colour:
            return "P"
        else:
            return "p"

    def find_legal_moves(self) -> list[tuple]:
        x, y = self.position[0], self.position[1]
        if self.colour == 0:
            if y < 8:
                if x == "a":
                    return [("b", y + 1)]
                elif x == "h":
                    return [("g", y + 1)]
                else:
                    return [(chr(ord(x) - 1), y + 1, chr(ord(x) + 1), y + 1)]
            else:
                raise ValueError("Pawn cannot be active on highest rank.")
        else:
            if y > 8:
                if x == "a":
                    return [("b", y - 1)]
                elif x == "h":
                    return [("g", y - 1)]
                else:
                    return [(chr(ord(x) - 1), y + 1, chr(ord(x) + 1), y + 1)]
            else:
                raise ValueError("Pawn cannot be active on highest rank.")

    def promote(self):
        "implement me"
        pass


class Knight(Piece):
    def __init__(self, position: tuple, colour: bool, active: bool, value: int):
        super().__init__(position, colour, active)
        self.value = value

    def find_legal_moves(self):
        return super().find_legal_moves()


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
