import numpy as np
from numpy.typing import NDArray
import heapq
from PegSolitaire import PegSolitaire

# Algoritmo de referencia, tomado de:
# https://en.wikipedia.org/wiki/A*_search_algorithm

class AStar_Node():
    """
    Class representing a node in the A* algorithm.

    Attributes:
        game_state (NDArray): The game state at this node.
        parent_node (AStar_Node): The parent node of this node.
        g_value (int): The cost from the start node to this node.
        h_value (int): The estimated cost from this node to the goal node.
        f_value (int): The sum of g_value and h_value.
    """
    def __init__(self, game_state: NDArray, parent_node, g_value: int, h_value: int, previous_move: list[tuple] = None) -> None:
        self.game_state = game_state.copy()
        self.parent_node = parent_node
        self.previous_move = previous_move

        self.g_value = g_value
        self.h_value = h_value
        self.f_value = self.g_value + self.h_value

    def __lt__(self, other):
        return self.f_value < other.f_value

class AStar_Algorithm(PegSolitaire):
    """
    Class implementing the A* algorithm for the Peg Solitaire game.

    Methods:
        __calculateHeuristic(x: int, y: int) -> int:
            Calculates the heuristic value based on the Manhattan distance from a given coordinate to the center of the board.

        __generateNode(current_piece_coord: tuple[int, int], next_position_coord: tuple[int, int], current_node: AStar_Node) -> AStar_Node:
            Generates a new node based on moving a piece from a current coordinate to a destination coordinate.

        __findPossibleNextMove(current_node: AStar_Node) -> list[AStar_Node]:
            Finds all possible next moves from the current node.

        rootNodeMD(matrix: NDArray) -> int:
            Calculates the total Manhattan distance from all pieces to the center of the board.

        A_Star():
            Implements the A* algorithm to find the solution to the Peg Solitaire game.
    """

    def __calculateHeuristic(self, x: int, y: int):
        """
        Calculates the heuristic value based on the Manhattan distance from a given coordinate to the center of the board.

        Parameters:
            x (int): The x coordinate.
            y (int): The y coordinate.

        Returns:
            int: The heuristic value.
        """
        return abs( self.CENTER_Y - y ) + abs( self.CENTER_X - x )

    def __generateNode(self, current_piece_coord: tuple[int, int], next_position_coord: tuple[int, int], current_node: AStar_Node):
        """
        Generates a new node based on moving a piece from a current coordinate to a destination coordinate.

        Parameters:
            current_piece_coord (tuple[int, int]): Coordinates of the current piece.
            next_position_coord (tuple[int, int]): Coordinates of the destination position.
            current_node (AStar_Node): The current node.

        Returns:
            AStar_Node: The newly generated node.
        """
        # Set the coord of the piece destiny
        coord_destiny_x = next_position_coord[1]
        coord_destiny_y = next_position_coord[0]

        # Set the coord of the piece current position
        piece_coord_x = current_piece_coord[0]
        piece_coord_y = current_piece_coord[1]

        # Get the piece in between the current piece and the destiny
        target_piece = self.GetPieceInBetween(piece_coord_x, piece_coord_y, coord_destiny_x, coord_destiny_y)
        target_x = target_piece[1]
        target_y = target_piece[0]

        # Make the move of the piece and get the new game board state
        next_game_board = self.MakeMove(piece_coord_x, piece_coord_y, coord_destiny_x, coord_destiny_y, current_node.game_state.copy())
        if (next_game_board is not None):
            # Calculate the new g, h and f values for the new node
            new_gValue = current_node.g_value + 1
            new_hValue = current_node.h_value

            new_hValue -= self.__calculateHeuristic(piece_coord_x, piece_coord_y)
            new_hValue -= self.__calculateHeuristic(target_x, target_y)
            new_hValue += self.__calculateHeuristic(coord_destiny_x, coord_destiny_y)

            # Create and return the new node
            new_node = AStar_Node(next_game_board.copy(), current_node, new_gValue, new_hValue, [(piece_coord_x, piece_coord_y), (coord_destiny_x, coord_destiny_y)])
            return new_node

        # If the move is invalid := Return none (Did not create any node)
        return None

    def __findPossibleNextMove(self, current_node: AStar_Node) -> list[ AStar_Node ]:
        """
        Finds all possible next moves from the current node.

        Parameters:
            current_node (AStar_Node): The current node.

        Returns:
            list[AStar_Node]: A list of possible next nodes.
        """
        result = []
        x, y = 0, 0

        # Iterate through the game board
        for _ in range(self.GAME_SIZE * self.GAME_SIZE):

            # Check if there is a piece in the current location
            if current_node.game_state[y, x] == 1:
                possible_moves = self.GetPiecePossibleNextPositions(x, y)

                # Create 4 nodes based on the possible moves
                node1 = self.__generateNode( (x, y), possible_moves[0], current_node )
                node2 = self.__generateNode( (x, y), possible_moves[1], current_node )
                node3 = self.__generateNode( (x, y), possible_moves[2], current_node )
                node4 = self.__generateNode( (x, y), possible_moves[3], current_node )

                # Add the valid nodes to the result list
                if (node1 is not None):
                    result.append(node1)
                if (node2 is not None):
                    result.append(node2)
                if (node3 is not None):
                    result.append(node3)
                if (node4 is not None):
                    result.append(node4)

            # Move to the next location
            x += 1
            if x >= self.GAME_SIZE:
                y += 1
                x = 0

        return result

    def rootNodeMD (self, matrix):
        """
        Calculates the total Manhattan distance from all pieces to the center of the board.

        Parameters:
            matrix (NDArray): The game board matrix.

        Returns:
            int: The total Manhattan distance.
        """
        m = len(matrix)
        n = len(matrix[1])
        centre = (self.CENTER_X, self.CENTER_Y)
        total = 0

        for row in range(m):
            for column in range(n):
                if (matrix[row][column] != -1):
                    total += abs(row - centre[0]) + abs (column - centre[1])

        print("The MD is: ", total)
        return total

    def A_Star(self, showResult=True):
        """
        Implements the A* algorithm to find the solution to the Peg Solitaire game.
        """
        # Set the initial and goal states
        initialState = self.GetGameMatrix()
        goalState = self.GetObjetiveMatrix()

        current: AStar_Node = None
        initial_h = self.rootNodeMD(initialState)
        initial_g = 0

        # Create open and close list variables
        openList: list[ AStar_Node ] = []
        closeList: set = set()
        openList.append( AStar_Node(initialState, None, initial_g, initial_h) )

        # APPROACH Priority Queue: Create the initial node and add it to the open list
        # heapq.heappush(openList, (initial_h + initial_g, AStar_Node(initialState, None, initial_g, initial_h)))

        # Keep track of number of explored nodes
        exploredNodes = 0

        while True:
            # 1. Get the selected node based on the f_value
            current = min(openList, key=lambda node: node.f_value)
            # APPROACH Priority Queue: Get the selected node based on the f_value (Using a Priority Queue)
            # _, current = heapq.heappop(openList)

            # 2. Check if in the selected node, the MapState is equal to the goal
            if (np.array_equal(goalState, current.game_state)):
                break

            # 3. Check if the game state already have been explored
            state_tuple = tuple(map(tuple, current.game_state))
            if state_tuple in closeList:
                openList.remove(current)
                continue

            # Keep track of explored nodes
            exploredNodes += 1

            # 4. Explore next possible movement based on the current state
            nextNodes = self.__findPossibleNextMove( current )
            for node in nextNodes:
                node_tuple = tuple(map(tuple, node.game_state))
                if node_tuple not in closeList:
                    # heapq.heappush(openList, (node.f_value, node))
                    openList.append(node)

            # 5. Add current to the close list and remove it from the open
            closeList.add(state_tuple)
            openList.remove(current)

        # Keep the last node
        lastNode = current

        if (showResult):
          # Reconstruct the path from the initial state to the goal state
          foundPath: list[ AStar_Node ] = []
          while current != None:
              foundPath.append( current )
              current = current.parent_node
          foundPath.reverse()

          print("Recorrido:")
          for node in foundPath:
              self.PrintGame( node.game_state, node.previous_move )

          # Print the number of moves made until reach that state
          print("Total de movimientos realizados: ", lastNode.g_value)

          # Print the total of explored nodes
          print("Nodos explorados: ", exploredNodes)
