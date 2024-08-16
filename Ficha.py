# Definir una clase para representar una ficha en el tablero
class Ficha:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def colocar(self,tablero):
        tablero[self.fila, self.columna] = 1

    def quitar(self,tablero):
        tablero[self.fila, self.columna] = 0

    def mover(self, nueva_fila, nueva_columna):
        self.quitar()
        self.fila = nueva_fila
        self.columna = nueva_columna
        self.colocar()
