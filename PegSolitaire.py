import numpy as np
from numpy.typing import NDArray


class PegSolitaire:
    """
    Class representing the Peg Solitaire game.

    Attributes:
        GAME_SIZE (int): The size of the game board.
        CENTER_X (int): The x-coordinate of the center of the board.
        CENTER_Y (int): The y-coordinate of the center of the board.
        game_board (NDArray): The current state of the game board.
    """
    # Classic board 
    # GAME_SIZE = 7
    # CENTER_X = 3
    # CENTER_Y = 3
    
    #Square board
    # GAME_SIZE = 6
    # CENTER_X = 3
    # CENTER_Y = 2
    
    # German board
    GAME_SIZE = 9
    CENTER_X = 4
    CENTER_Y = 4

    def __init__(self):
        """
        Initializes the PegSolitaire game with a given board size.

        Parameters:
            game_size (int): The size of the game board.
        """
        self.__initializeObjectiveMatrix()

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
    
    def __initializeMatrixCornersG(self, matrix: NDArray):
        # Fill the matrix with -1 in the border
        matrix[0, 0] = -1
        matrix[0, 1] = -1
        matrix[0, 2] = -1
        matrix[0, -1] = -1
        matrix[0, -2] = -1
        matrix[0, -3] = -1
        
        matrix[-1, 0] = -1
        matrix[-1, 1] = -1
        matrix[-1, 2] = -1
        matrix[-1, -1] = -1
        matrix[-1, -2] = -1
        matrix[-1, -3] = -1
        
        matrix[1, 0] = -1
        matrix[1, 1] = -1
        matrix[1, 2] = -1
        matrix[1, -1] = -1
        matrix[1, -2] = -1
        matrix[1, -3] = -1
        
        matrix[-2, 0] = -1
        matrix[-2, 1] = -1
        matrix[-2, 2] = -1
        matrix[-2, -1] = -1
        matrix[-2, -2] = -1
        matrix[-2, -3] = -1
        
        matrix[2, 0] = -1
        matrix[2, 1] = -1
        matrix[2, 2] = -1
        matrix[2, -1] = -1
        matrix[2, -2] = -1
        matrix[2, -3] = -1
        
        matrix[-3, 0] = -1
        matrix[-3, 1] = -1
        matrix[-3, 2] = -1
        matrix[-3, -1] = -1
        matrix[-3, -2] = -1
        matrix[-3, -3] = -1

        return matrix

    def __initializeObjectiveMatrix(self):
        """
        Initializes the objective matrix for the game. 
        The objective matrix represents the goal state of the game.
        """
        # Create a 7x7 matrix to represent the goal state
        self.goalMatrix = np.zeros((self.GAME_SIZE, self.GAME_SIZE),dtype=object)
        #self.goalMatrix = self.__initializeMatrixCorners(self.goalMatrix)
        self.goalMatrix = self.__initializeMatrixCornersG(self.goalMatrix)

        # Fill the matrix with 1 in the center
        self.goalMatrix[self.CENTER_Y, self.CENTER_X] = 1

    def PrintGame(self, game_board: NDArray):
        """
        Prints the current state of the game board.
        Args:
            game_board (NDArray): The current state of the game board.
        """
        temp_matrix = np.zeros((self.GAME_SIZE, self.GAME_SIZE), dtype=object)

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
        """
        Gets the coordinates of the piece between two given coordinates.

        Parameters:
            x1 (int): The x-coordinate of the first position.
            y1 (int): The y-coordinate of the first position.
            x2 (int): The x-coordinate of the second position.
            y2 (int): The y-coordinate of the second position.

        Returns:
            tuple[int, int]: The coordinates of the piece in between.
        """
        target_x = x_from if x_from == x_to else (x_from + x_to) // 2
        target_y = y_from if y_from == y_to else (y_from + y_to) // 2

        return ( target_y, target_x )

    def MakeMove(self, x_from: int, y_from: int, x_to: int, y_to: int, game_board: NDArray):
        """
        Makes a move on the board by moving a piece from one position to another.

        Parameters:
            x1 (int): The x-coordinate of the starting position.
            y1 (int): The y-coordinate of the starting position.
            x2 (int): The x-coordinate of the destination position.
            y2 (int): The y-coordinate of the destination position.
            board (NDArray): The current state of the game board.

        Returns:
            NDArray: The new state of the game board after the move, or None if the move is invalid.
        """
        # Check if the to location is in bounds
        if (x_to < 0 or x_to >= self.GAME_SIZE or
            y_to < 0 or y_to >= self.GAME_SIZE or
            game_board[ y_to, x_to ] == -1
        ):
            return None

        # Check if the from location has no piece -> Cant move
        if game_board[y_from, x_from] != 1:
            return None

        # Check if the to location has a piece -> Cant move
        if game_board[y_to, x_to] != 0:
            return None

        # Check if the select locations are near each other (0: Pieces from same X/Y ; 2: Exact difference between X/Y for valid move)
        diff_x = abs(x_from - x_to)
        diff_y = abs(y_from - y_to)
        if (diff_x != 0 and diff_x != 2) or (diff_y != 0 and diff_y != 2):
            return None

        # 1. Get piece in between
        targetPiece = self.GetPieceInBetween(x_from, y_from, x_to, y_to)

        # 2. Check if the target location has no piece -> Cant move
        if game_board[ targetPiece[0], targetPiece[1] ] != 1:
            return None

        # 3. Remove the from location, target piece and set the to location
        game_board[ y_from, x_from ] = 0
        game_board[ targetPiece[0], targetPiece[1] ] = 0
        game_board[ y_to, x_to ] = 1

        return game_board

    def GetPiecePossibleNextPositions(self, x: int, y: int) -> list[tuple[int, int]] :
        """
        Gets the possible next positions for a piece at a given coordinate.
        Looks for the possible moves in the up, down, right and left directions with a distance of 2.

        Parameters:
            x (int): The x-coordinate of the piece.
            y (int): The y-coordinate of the piece.

        Returns:
            list[tuple[int, int]]: A list of possible next positions. 
            Index of array 0: Up, 1: Down, 2: Right, 3: Left
        """
        up_location    = (y - 2, x)
        down_location  = (y + 2, x)
        right_location = (y, x + 2)
        left_location  = (y, x - 2)

        return [ up_location, down_location, right_location, left_location ]

    def GetObjetiveMatrix(self):
        """
        Gets the objective matrix for

        Returns:
            NDArray: The objective matrix for the game.
        """
        return self.goalMatrix

    def GetGameMatrix(self):
        """
        Gets the current state of the game board.

        Returns:
            NDArray: The current state of the game board.
        """
        game_matrix = np.ones((self.GAME_SIZE, self.GAME_SIZE), dtype=object)
        #game_matrix = self.__initializeMatrixCorners( game_matrix )
        game_matrix = self.__initializeMatrixCornersG( game_matrix )
        
        # Fill the matrix with 0 in the center
        game_matrix[self.CENTER_Y, self.CENTER_X] = 0
        

        return game_matrix