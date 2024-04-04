import random

class DominoBoard:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[0] * cols for _ in range(rows)]
        self.solutions = []

    def is_valid_position(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    # Esta weá está rara x la chucha
    def can_place_domino(self, row, col, direction):
        if direction == 'horizontal':
            return ((self.is_valid_position(row, col + 1) and self.board[row][col + 1] == 0) or \
                   (self.is_valid_position(row, col - 1) and self.board[row][col - 1] == 2))
        elif direction == 'vertical':
            return ((self.is_valid_position(row + 1, col) and self.board[row + 1][col] == 0) or \
                   (self.is_valid_position(row - 1, col) and self.board[row - 1][col] == 1))
        return False

    def place_domino(self, row, col, direction):
        if direction == 'horizontal':
            if col + 1 < self.cols:
                self.board[row][col] = 1
                self.board[row][col + 1] = 1
        elif direction == 'vertical':
            if row + 1 < self.rows:  
                self.board[row][col] = 2
                self.board[row + 1][col] = 2

    def is_solution(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == 0:
                    return False
        return True

    def find_solutions(self, row=0, col=0, found_solutions=set()):
        if self.is_solution():
            solution = tuple(tuple(row) for row in self.board)
            if solution not in found_solutions:
                found_solutions.add(solution)
                self.solutions.append([row[:] for row in self.board])
            return

        for r in range(row, self.rows):
            for c in range(col if r == row else 0, self.cols):
                if self.board[r][c] == 0:
                    if self.can_place_domino(r, c, 'horizontal'):
                        self.place_domino(r, c, 'horizontal')
                        if self.verify_after_placing(r, c):
                            self.find_solutions(r, c + 1, found_solutions)
                        self.remove_domino(r, c, 'horizontal')
                    if self.can_place_domino(r, c, 'vertical'):
                        self.place_domino(r, c, 'vertical')
                        if self.verify_after_placing(r, c):
                            self.find_solutions(r, c + 1, found_solutions)
                        self.remove_domino(r, c, 'vertical')  

    # Esta weá tmb ta rara pq no verifica na >:c
    def verify_after_placing(self, row, col):
        # Verificar si hay una pieza con orientación diferente en la misma fila
        for c in range(self.cols):
            if c != col and self.board[row][c] != 0 and self.board[row][c] != self.board[row][col]:
                return True  # Hay una pieza con orientación diferente en la misma fila, continuar con esta solución
        # Verificar si hay una pieza con orientación diferente en la misma columna
        for r in range(self.rows):
            if r != row and self.board[r][col] != 0 and self.board[r][col] != self.board[row][col]:
                return True  # Hay una pieza con orientación diferente en la misma columna, continuar con esta solución
        # Si no hay piezas con orientación diferente en la misma fila o columna, verificar si hay espacio para una nueva pieza con orientación diferente
        if any(self.board[row][c] == 0 for c in range(self.cols) if c != col) or \
        any(self.board[r][col] == 0 for r in range(self.rows) if r != row):
            return True  # Hay espacio para una nueva pieza con orientación diferente, continuar con esta solución
        return False  # No hay espacio para una nueva pieza con orientación diferente, descartar esta solución



    def remove_domino(self, row, col, direction):
        if direction == 'horizontal':
            if col + 1 < len(self.board[row]):
                self.board[row][col] = 0
                self.board[row][col + 1] = 0
        elif direction == 'vertical':
            if row + 1 < len(self.board):
                self.board[row][col] = 0
                self.board[row + 1][col] = 0

    def print_all_solutions(self):
        print(f"Total solutions: {len(self.solutions)}")
        for i, solution in enumerate(self.solutions):
            print(f"Solution {i + 1}:")
            for row in solution:
                print(row)
            print("\n")  # Print a newline for better readability between solutions


# Todavía no funciona la weá q rabia :c
rows = 4
cols = 3
domino_board = DominoBoard(rows, cols)
domino_board.find_solutions()
domino_board.print_all_solutions()

# O((n*m)^2) time complexity, where n is the number of rows and m is the number of columns in the board
