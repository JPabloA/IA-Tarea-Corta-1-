import numpy as np
from numpy.typing import NDArray
from PegSolitaire import PegSolitaire, PieceLocation, Piece
import random

class AStar_Node():
    def __init__(self, piece: Piece, game_state: NDArray, g_value: int, h_value: int) -> None:
        self.piece = piece
        self.game_state = game_state

        self.g_value = 0
        self.h_value = 0
        self.f_value = self.g_value + self.h_value

class AStar_Algorithm(PegSolitaire):

    def __calculateHeuristic(self):
        return random.randrange(1, 10)

    def __findPossibleNextMove(self, current: AStar_Node) -> list[ AStar_Node ]:
        pass

    def ReconstructPath(self, current: AStar_Node):
        pass

    def A_Star(self):

        # Set the initial and goal states
        initialState = self.GenerateGameStateMatrix( self.pieces_dict )
        goalState = self.GetObjetiveMatrix()

        initial_h = self.calculateHeuristic()
        initial_g = 0

        # Create open and close list variables
        openList: list[ AStar_Node ] = [
            AStar_Node(None, initialState, initial_g, initial_h),
        ]
        closeList: list[ AStar_Node ] = []

        while True:
            # 1. Get the selected node based on the f_value
            current = min(openList, key=lambda node: node.f_value)

            # 2. Check if in the selected node, the MapState is equal to the goal
            if (np.array_equal(goalState, current.game_state)):
                closeList.append( current )
                self.ReconstructPath( current )
                break

            # 3. Explore next possible movement based on the current state
            nextNodes = self.__findPossibleNextMove( current )
            for node in nextNodes:
                if node not in closeList:
                    openList.append(node)

            # 4. Add current to the close list and remove it from the open
            closeList.append(current)
            openList.remove(current)



