import numpy as np
from numpy.typing import NDArray
from PegSolitaire import PegSolitaire, PieceLocation, Piece, PieceInMap
import random

class AStar_Node():
    def __init__(self, game_state: NDArray, parent, g_value: int, h_value: int) -> None:
        self.game_state = game_state.copy()
        self.parent = parent

        self.g_value = g_value
        self.h_value = h_value
        self.f_value = self.g_value + self.h_value

class AStar_Algorithm(PegSolitaire):

    def __calculateHeuristic(self, x: int, y: int):
        return abs(3-y)+abs(3-x)

    def __findPossibleNextMove(self, current: AStar_Node) -> list[ AStar_Node ]:

        result = []
        current_game_state = current.game_state

        for y in range(current_game_state.shape[0]):
            for x in range(current_game_state.shape[1]):
                if current_game_state[y, x] == 1:

                    possible_moves = self.GetPiecePossibleNextPositions(x, y)
                    for coord in possible_moves:

                        coord_destiny_x = coord[1]
                        coord_destiny_y = coord[0]

                        target_piece = self.GetPieceInBetween(x, y, coord_destiny_x, coord_destiny_y)
                        target_x = target_piece[1]
                        target_y = target_piece[0]

                        next_game_board = self.MakeMove(x, y, coord_destiny_x, coord_destiny_y, current_game_state.copy())
                        if (next_game_board is not None):
                            # print((x, y), "---\n")
                            # self.PrintGame( next_game_board )
                            # print("\n\n")

                            new_gValue = current.g_value + 1
                            new_hValue = current.h_value

                            new_hValue -= self.__calculateHeuristic(x, y)
                            new_hValue -= self.__calculateHeuristic(target_x, target_y)
                            new_hValue += self.__calculateHeuristic(coord_destiny_x, coord_destiny_y)

                            new_node = AStar_Node(next_game_board.copy(), current, new_gValue, new_hValue)
                            result.append( new_node )
        return result

    def ReconstructPath(self, current: AStar_Node):
        pass

    def A_Star(self):

        # Set the initial and goal states
        initialState = self.GetGameMatrix()
        goalState = self.GetObjetiveMatrix()

        initial_h = 88
        initial_g = 0

        # Create open and close list variables
        openList: list[ AStar_Node ] = [
            AStar_Node(initialState, None, initial_g, initial_h),
        ]
        closeList: list[ NDArray ] = []

        while True:
            # 1. Get the selected node based on the f_value
            current = min(openList, key=lambda node: node.f_value)
            # self.PrintGame( current.game_state )

            # 2. Check if in the selected node, the MapState is equal to the goal
            if (np.array_equal(goalState, current.game_state)):
                closeList.append( current )
                self.ReconstructPath( current )
                break

            # 3. Check if the game state already have been explored
            if any(np.array_equal(current.game_state, arr) for arr in closeList):
                openList.remove(current)
                continue

            # 4. Explore next possible movement based on the current state
            nextNodes = self.__findPossibleNextMove( current )
            for node in nextNodes:
                if not any(np.array_equal(node.game_state, arr) for arr in closeList):
                    openList.append(node)

            # 5. Add current to the close list and remove it from the open
            closeList.append(current.game_state)
            openList.remove(current)

        # print(openList[0].)
        print("Termino")




