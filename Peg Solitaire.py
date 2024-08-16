import numpy as np
from Ficha import Ficha

# Crear una matriz de float
matrizObjetivo = np.zeros((7, 7),dtype=object)

# Crear un diccionario para almacenar las instancias de Ficha
fichas = {}

# Llenar las esquinas con -1
matrizObjetivo[0, 0] = -1
matrizObjetivo[0, 1] = -1
matrizObjetivo[0, -1] = -1
matrizObjetivo[0, -2] = -1

matrizObjetivo[-1, 0] = -1
matrizObjetivo[-1, 1] = -1
matrizObjetivo[-1, -1] = -1
matrizObjetivo[-1, -2] = -1

matrizObjetivo[1, 0] = -1
matrizObjetivo[1, 1] = -1
matrizObjetivo[1, -1] = -1
matrizObjetivo[1, -2] = -1

matrizObjetivo[-2, 1] = -1
matrizObjetivo[-2, 0] = -1
matrizObjetivo[-2, -2] = -1
matrizObjetivo[-2, -1] = -1

# Colocar un 1 en el centro
matrizObjetivo[3, 3] = 1

print("Matriz objetivo: \n",matrizObjetivo)

# Asignar instancias de Ficha en un diccionario
for i in range(matrizObjetivo.shape[0]):
    for j in range(matrizObjetivo.shape[1]):
        if matrizObjetivo[i, j] == 0:
            fichas[(i, j)] = Ficha(i, j)

print('Fichas: \n',fichas)
