import numpy as np
from Piece import Piece

class PegSolitaire:

    # Create a dictionary to store the instances of Ficha
    pieces_dict: dict[tuple[int, int], Piece] = {}

    GAME_SIZE = 7

    def __init__(self):
        self.__initializeObjectiveMatrix()
        self.__initializeGameMatrix()

    def __initializeObjectiveMatrix(self):
        # Create a 7x7 matrix to represent the goal state
        self.goalMatrix = np.zeros((self.GAME_SIZE, self.GAME_SIZE),dtype=object)

        # Fill the matrix with -1 in the border
        self.goalMatrix[0, 0] = -1
        self.goalMatrix[0, 1] = -1
        self.goalMatrix[0, -1] = -1
        self.goalMatrix[0, -2] = -1

        self.goalMatrix[-1, 0] = -1
        self.goalMatrix[-1, 1] = -1
        self.goalMatrix[-1, -1] = -1
        self.goalMatrix[-1, -2] = -1

        self.goalMatrix[1, 0] = -1
        self.goalMatrix[1, 1] = -1
        self.goalMatrix[1, -1] = -1
        self.goalMatrix[1, -2] = -1

        self.goalMatrix[-2, 1] = -1
        self.goalMatrix[-2, 0] = -1
        self.goalMatrix[-2, -2] = -1
        self.goalMatrix[-2, -1] = -1

        # Fill the matrix with 1 in the center
        self.goalMatrix[3, 3] = 1

    def __initializeGameMatrix(self):
        # Create the instances of Ficha and store them in the dictionary
        for i in range(self.goalMatrix.shape[0]):
            for j in range(self.goalMatrix.shape[1]):
                if self.goalMatrix[i, j] == 0:
                    #Ficha is created with the position (i, j) in the matrix
                    self.pieces_dict[(i, j)] = Piece(i, j)

    def PrintGame(self):

        temp_matrix = np.zeros((self.GAME_SIZE, self.GAME_SIZE), dtype=object)

        # Fill the matrix with -1 in the border
        temp_matrix[0, 0] = -1
        temp_matrix[0, 1] = -1
        temp_matrix[0, -1] = -1
        temp_matrix[0, -2] = -1

        temp_matrix[-1, 0] = -1
        temp_matrix[-1, 1] = -1
        temp_matrix[-1, -1] = -1
        temp_matrix[-1, -2] = -1

        temp_matrix[1, 0] = -1
        temp_matrix[1, 1] = -1
        temp_matrix[1, -1] = -1
        temp_matrix[1, -2] = -1

        temp_matrix[-2, 1] = -1
        temp_matrix[-2, 0] = -1
        temp_matrix[-2, -2] = -1
        temp_matrix[-2, -1] = -1

        game_row_str = ""
        for i in range(temp_matrix.shape[0]):
            for j in range(temp_matrix.shape[1]):

                if temp_matrix[i, j] == -1:
                    game_row_str += "  "
                    continue

                if (i, j) in self.pieces_dict:
                    game_row_str += "1 "
                else:
                    game_row_str += "0 "
            game_row_str += "\n"

        print(game_row_str)

    def MakeMove(self, x_from: int, y_from: int, x_to: int, y_to: int):
        # Check if the from location has no piece -> Cant move
        if (y_from, x_from) not in self.pieces_dict:
            print("Invalid move: 1")
            return

        # Check if the to location has a piece -> Cant move
        if (y_to, x_to) in self.pieces_dict:
            print("Invalid move: 2")
            return

        # Check if the select locations are near each other (0: Pieces from same X/Y ; 2: Exact difference between X/Y for valid move)
        diff_x = abs(x_from - x_to)
        diff_y = abs(y_from - y_to)
        if (diff_x != 0 and diff_x != 2) or (diff_y != 0 and diff_y != 2):
            print("Invalid move: 3")
            return

        # 1. Get piece in between
        target_x = x_from if x_from == x_to else (x_from + x_to) // 2
        target_y = y_from if y_from == y_to else (y_from + y_to) // 2

        # 2. Check if the target location has no piece -> Cant move
        if (target_y, target_x) not in self.pieces_dict:
            print("Invalid move: 4")
            return

        # 3. Remove the from location, target piece and set the to location
        del self.pieces_dict[ (y_from, x_from) ]
        del self.pieces_dict[ (target_y, target_x) ]
        self.pieces_dict[ (y_to, x_to) ] = Piece(y_to, x_to)

    def GetObjetiveMatrix(self):
        return self.goalMatrix

    def GetGameDictionary(self):
        return self.pieces_dict
