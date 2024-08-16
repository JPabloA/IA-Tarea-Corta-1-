import numpy as np
from Peice import Peice

# Create a 7x7 matrix to represent the goal state
goalMatrix = np.zeros((7, 7),dtype=object)

# Create a dictionary to store the instances of Ficha
pieces_dict = {}

# Fill the matrix with -1 in the border
goalMatrix[0, 0] = -1
goalMatrix[0, 1] = -1
goalMatrix[0, -1] = -1
goalMatrix[0, -2] = -1

goalMatrix[-1, 0] = -1
goalMatrix[-1, 1] = -1
goalMatrix[-1, -1] = -1
goalMatrix[-1, -2] = -1

goalMatrix[1, 0] = -1
goalMatrix[1, 1] = -1
goalMatrix[1, -1] = -1
goalMatrix[1, -2] = -1

goalMatrix[-2, 1] = -1
goalMatrix[-2, 0] = -1
goalMatrix[-2, -2] = -1
goalMatrix[-2, -1] = -1

# Fill the matrix with 1 in the center
goalMatrix[3, 3] = 1

print("Goal matrix: \n",goalMatrix)

# Create the instances of Ficha and store them in the dictionary
for i in range(goalMatrix.shape[0]):
    for j in range(goalMatrix.shape[1]):
        if goalMatrix[i, j] == 0:
            #Ficha is created with the position (i, j) in the matrix
            pieces_dict[(i, j)] = Peice(i, j)

print('Peices in the board: \n',pieces_dict)
