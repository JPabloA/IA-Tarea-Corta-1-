import numpy as np
from numpy.typing import NDArray
from PegSolitaire import PegSolitaire, PieceLocation, Piece, PieceInMap
import heapq

# https://en.wikipedia.org/wiki/A*_search_algorithm

class AStar_Node():
    def __init__(self, game_state: NDArray, parent_node, g_value: int, h_value: int) -> None:
        self.game_state = game_state.copy()
        self.parent_node = parent_node

        self.g_value = g_value
        self.h_value = h_value
        self.f_value = self.g_value + self.h_value

class AStar_Algorithm(PegSolitaire):

    def __calculateHeuristic(self, x: int, y: int):
        return abs( self.CENTER_Y - y ) + abs( self.CENTER_X - x )

    def __generateNode(self, current_piece_coord: tuple[int, int], next_position_coord: tuple[int, int], current_node: AStar_Node):
        coord_destiny_x = next_position_coord[1]
        coord_destiny_y = next_position_coord[0]

        piece_coord_x = current_piece_coord[0]
        piece_coord_y = current_piece_coord[1]

        target_piece = self.GetPieceInBetween(piece_coord_x, piece_coord_y, coord_destiny_x, coord_destiny_y)
        target_x = target_piece[1]
        target_y = target_piece[0]

        next_game_board = self.MakeMove(piece_coord_x, piece_coord_y, coord_destiny_x, coord_destiny_y, current_node.game_state.copy())
        if (next_game_board is not None):
            new_gValue = current_node.g_value + 1
            new_hValue = current_node.h_value

            new_hValue -= self.__calculateHeuristic(piece_coord_x, piece_coord_y)
            new_hValue -= self.__calculateHeuristic(target_x, target_y)
            new_hValue += self.__calculateHeuristic(coord_destiny_x, coord_destiny_y)

            new_node = AStar_Node(next_game_board.copy(), current_node, new_gValue, new_hValue)
            return new_node
        return None

    def __findPossibleNextMove(self, current_node: AStar_Node) -> list[ AStar_Node ]:

        result = []
        current_game_state = current_node.game_state

        y = 0
        x = 0

        for _ in range(self.GAME_SIZE * self.GAME_SIZE):

            if current_game_state[y, x] == 1:

                possible_moves = self.GetPiecePossibleNextPositions(x, y)

                node1 = self.__generateNode( (x, y), possible_moves[0], current_node )
                node2 = self.__generateNode( (x, y), possible_moves[1], current_node )
                node3 = self.__generateNode( (x, y), possible_moves[2], current_node )
                node4 = self.__generateNode( (x, y), possible_moves[3], current_node )

                if (node1 is not None):
                    result.append(node1)
                if (node2 is not None):
                    result.append(node2)
                if (node3 is not None):
                    result.append(node3)
                if (node4 is not None):
                    result.append(node4)

            x += 1
            if x >= self.GAME_SIZE:
                y += 1
                x = 0

        return result

    def rootNodeMD (self, matrix):
        m = len(matrix)
        n = len(matrix[1])
        centre = (m // 2, n // 2)
        total = 0

        for row in range(m):
            for column in range(n):
                if (matrix[row][column] != -1):
                    total += abs(row - centre[0]) + abs (column - centre[1])

        print("The MD is: ", total)
        return total

    def A_Star(self):

        # Set the initial and goal states
        initialState = self.GetGameMatrix()
        goalState = self.GetObjetiveMatrix()

        current: AStar_Node = None
        initial_h = self.rootNodeMD(initialState)
        initial_g = 0

        # Create open and close list variables
        openList: list[ AStar_Node ] = [
            AStar_Node(initialState, None, initial_g, initial_h),
        ]
        closeList: set = set()

        itern = 0
        while True:
            # 1. Get the selected node based on the f_value
            # current = min(openList, key=lambda node: node.f_value)
            current = openList.pop()
            itern += 1
            print("Iteraciones:", itern)

            # 2. Check if in the selected node, the MapState is equal to the goal
            if (np.array_equal(goalState, current.game_state)):
                # closeList.add( current )
                break

            # 3. Check if the game state already have been explored
            state_tuple = tuple(map(tuple, current.game_state))
            if state_tuple in closeList:
                # openList.remove(current)
                continue

            # 4. Explore next possible movement based on the current state
            nextNodes = self.__findPossibleNextMove( current )
            for node in nextNodes:
                node_tuple = tuple(map(tuple, node.game_state))
                if node_tuple not in closeList:
                    openList.append(node)

            # 5. Add current to the close list and remove it from the open
            closeList.add(state_tuple)
            # openList.remove(current)

        foundPath = []
        while current.parent_node != None:
            foundPath.append( current.game_state )
            current = current.parent_node
        foundPath.append( initialState )
        foundPath.reverse()

        print("Recorrido:")
        for state in foundPath:
            self.PrintGame( state )

