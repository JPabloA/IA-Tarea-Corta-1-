# Represents a piece in the board using the coordinates of the matrix
class Peice:
    def __init__(self, row_index, column_index):
        self.row_index = row_index
        self.column_index = column_index

    def place_piece(self,game_board):
        game_board[self.row_index, self.column_index] = 1

    def remove(self,game_board):
        game_board[self.row_index, self.column_index] = 0

    def mover(self, nueva_fila, nueva_columna):
        self.remove()
        self.row_index = nueva_fila
        self.column_index = nueva_columna
        self.place_piece()