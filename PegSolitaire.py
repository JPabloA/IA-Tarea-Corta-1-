import numpy as np
from numpy.typing import NDArray
from Piece import Piece

PieceLocation = tuple[int, int]
PieceObject = tuple[PieceLocation, Piece]
PieceInMap = dict[PieceLocation, Piece]

class PegSolitaire:

    GAME_SIZE = 7

    def __init__(self):
        self.__initializeObjectiveMatrix()
        # self.__initializeGameMatrix()

    def __initializeMatrixCorners(self, matrix: NDArray):
        # Fill the matrix with -1 in the border
        matrix[0, 0] = -1
        matrix[0, 1] = -1
        matrix[0, -1] = -1
        matrix[0, -2] = -1

        matrix[-1, 0] = -1
        matrix[-1, 1] = -1
        matrix[-1, -1] = -1
        matrix[-1, -2] = -1

        matrix[1, 0] = -1
        matrix[1, 1] = -1
        matrix[1, -1] = -1
        matrix[1, -2] = -1

        matrix[-2, 1] = -1
        matrix[-2, 0] = -1
        matrix[-2, -2] = -1
        matrix[-2, -1] = -1

        return matrix

    def __initializeObjectiveMatrix(self):
        # Create a 7x7 matrix to represent the goal state
        self.goalMatrix = np.zeros((self.GAME_SIZE, self.GAME_SIZE),dtype=object)
        self.goalMatrix = self.__initializeMatrixCorners(self.goalMatrix)

        # Fill the matrix with 1 in the center
        self.goalMatrix[3, 3] = 1

    def __initializeGameMatrix(self):
        # Create the instances of Ficha and store them in the dictionary
        for i in range(self.goalMatrix.shape[0]):
            for j in range(self.goalMatrix.shape[1]):
                if self.goalMatrix[i, j] == 0:
                    #Ficha is created with the position (i, j) in the matrix
                    self.pieces_dict[(i, j)] = Piece(i, j)

    def PrintGame(self, game_board: NDArray):
        temp_matrix = np.zeros((self.GAME_SIZE, self.GAME_SIZE), dtype=object)
        temp_matrix = self.__initializeMatrixCorners(temp_matrix)

        game_row_str = ""
        for i in range(game_board.shape[0]):
            for j in range(game_board.shape[1]):

                if game_board[i, j] == -1:
                    game_row_str += "  "
                if game_board[i, j] == 1:
                    game_row_str += " 1"
                if game_board[i, j] == 0:
                    game_row_str += " 0"
            game_row_str += "\n"

        print(game_row_str)

    def GetPieceInBetween(self, x_from: int, y_from: int, x_to: int, y_to: int):
        target_x = x_from if x_from == x_to else (x_from + x_to) // 2
        target_y = y_from if y_from == y_to else (y_from + y_to) // 2

        return ( target_y, target_x )

    def MakeMove(self, x_from: int, y_from: int, x_to: int, y_to: int, game_board: NDArray):
        # Check if the to location is in bounds
        if (x_to < 0 or x_to >= self.GAME_SIZE or
            y_to < 0 or y_to >= self.GAME_SIZE or
            game_board[ y_to, x_to ] == -1
        ):
            return None

        # Check if the from location has no piece -> Cant move
        if game_board[y_from, x_from] != 1:
            # print("Invalid move: 1")
            return None

        # Check if the to location has a piece -> Cant move
        if game_board[y_to, x_to] != 0:
            # print("Invalid move: 2")
            return None

        # Check if the select locations are near each other (0: Pieces from same X/Y ; 2: Exact difference between X/Y for valid move)
        diff_x = abs(x_from - x_to)
        diff_y = abs(y_from - y_to)
        if (diff_x != 0 and diff_x != 2) or (diff_y != 0 and diff_y != 2):
            # print("Invalid move: 3")
            return None

        # 1. Get piece in between
        targetPiece = self.GetPieceInBetween(x_from, y_from, x_to, y_to)

        # 2. Check if the target location has no piece -> Cant move
        if game_board[ targetPiece[0], targetPiece[1] ] != 1:
            # print("Invalid move: 4")
            return None

        # 3. Remove the from location, target piece and set the to location
        game_board[ y_from, x_from ] = 0
        game_board[ targetPiece[0], targetPiece[1] ] = 0
        game_board[ y_to, x_to ] = 1

        return game_board

    def GetPiecePossibleNextPositions(self, x: int, y: int) -> list[tuple[int, int]] :
        up_location    = (y - 2, x)
        down_location  = (y + 2, x)
        left_location  = (y, x - 2)
        right_location = (y, x + 2)

        return [ up_location, right_location, down_location, left_location ]

    def GetObjetiveMatrix(self):
        return self.goalMatrix

    def GetGameMatrix(self):
        game_matrix = np.ones((self.GAME_SIZE, self.GAME_SIZE), dtype=object)
        game_matrix = self.__initializeMatrixCorners( game_matrix )

        # Fill the matrix with 0 in the center
        game_matrix[3, 3] = 0

        return game_matrix

    # Return a NPArray based on the current piece dictionary
    def GenerateGameStateMatrix(self, pieces: PieceInMap):
        game_matrix = np.zeros((self.GAME_SIZE, self.GAME_SIZE),dtype=object)
        self.__initializeMatrixCorners(game_matrix)

        for location in pieces:
            game_matrix[location] = 1

        return game_matrix
