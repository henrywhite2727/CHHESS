import numpy as np

# Piece Section
# Colour is a bool for now: 0 for white, 1 for black
# Position is a tuple for now: letter first, then numberFF

class Piece:
    def __init__(self, position:tuple, colour:bool, active: bool=True):
        self.position = position
        self.colour = colour
        self.active = active
    def __str__(self):
        return "implement me"
    def __repr__(self):
        return "implement me"
    def find_legal_moves(self):
        print("please implement me")
        
class Pawn(Piece):
    def __init__(self, position :tuple, colour : bool, active: bool,value: int):
        super().__init__(position, colour, active)
        self.value = value

    def find_legal_moves(self):
        if self.colour == 0:
            if self.position[1] < 8:
                if self.position[0] == 'a':
                    return [('b',self.position[1]+1)]
                elif self.position[0] == 'b':
                    pass
                else:
                    legal_moves = [(self.position[0]-1, self.position[1]+1), (self.position[0]+1,self.position[1]+1)]
            else:
                pass
        else:
            if self.position[1] > 1:
                legal_moves = [(self.position[0]-1, self.position[1]+1), (self.position[0]+1,self.position[1]+1)]    
    def promote(self):
        "implement me"
        pass

class Knight(Piece):
    def __init__(self, position : tuple, colour : bool,active : bool,value: int):
        super().__init__(position, colour, active)
        self.value = value
        
    def find_legal_moves(self):
        return super().find_legal_moves()

'''
        [('a',1),('b',1)]


henry = King(('d',1), 0, True, 10)
moves = henry.find_legal_moves()
'''


# Board Section
rows, cols = (8, 8)
board = [[0]*cols]*rows
for i in range(8):
    for j in range(8):
        board[i,j]=

# History Section
prev_move=['piece used: class','previous location on board', 'current position on board']
