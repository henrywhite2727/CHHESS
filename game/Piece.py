# Colour is a bool for now: 0 for white, 1 for black
# Position is a tuple for now: letter first, then numberFF


class Piece:
    def __init__(self, position: tuple, colour: bool, active: bool = True) -> None:
        if ord(position[0]) < ord("a") or ord(position[0]) > ord("h"):
            raise ValueError("Piece must have coordinates between a1 and h8.")
        self.position = position
        self.colour = colour
        self.active = active

    def __str__(self) -> str:
        return "implement me"

    def find_legal_moves(self) -> list:
        raise NotImplementedError("Please implement me")


class Pawn(Piece):
    def __init__(self, position: tuple, colour: bool, active: bool) -> None:
        super().__init__(position, colour, active)
        self.value = 1

    def find_legal_moves(self) -> list(tuple):
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


"""
        [('a',1),('b',1)]


henry = King(('d',1), 0, True, 10)
moves = henry.find_legal_moves()
"""
