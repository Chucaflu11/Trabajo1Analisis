import time

class DominoBoard:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[0] * cols for _ in range(rows)]
        self.solutions = []
        self.found_solutions = set()

    def is_valid_position(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def can_place_domino(self, row, col, direction):
        if direction == 'horizontal':
            return self.is_valid_position(row, col + 1) and self.board[row][col] == 0 and self.board[row][col + 1] == 0
        elif direction == 'vertical':
            return self.is_valid_position(row + 1, col) and self.board[row][col] == 0 and self.board[row + 1][col] == 0
        return False

    def place_domino(self, row, col, direction):
        if direction == 'horizontal':
            self.board[row][col] = 1
            self.board[row][col + 1] = 1
        elif direction == 'vertical':
            self.board[row][col] = 2
            self.board[row + 1][col] = 2

    def is_solution(self):
        for row in self.board:
            if 0 in row:
                return False
        return True

    def has_row_conflict(self, row, col, direction):
        if direction == 'horizontal':
            if 2 in self.board[row]:
                return False
            elif 0 in self.board[row]:
                return False
        elif direction == 'vertical':
            if any(self.board[row][c] == 1 for c in range(self.cols)):
                return False
            else:
                for c in range(col, self.cols - 1):
                    if self.board[row][c] == self.board[row][c + 1] == 0:
                        return False
        return True

    def has_column_conflict(self, row, col, direction):
        if direction == 'vertical':
            if any(self.board[r][col] == 1 for r in range(self.rows)):
                return False
            elif any(self.board[r][col] == 0 for r in range(self.rows)):
                return False
        elif direction == 'horizontal':
            if any(self.board[r][col] == 2 for r in range(self.rows)):
                return False
            else:
                for r in range(row, self.rows - 1):
                    if self.board[r][col] == self.board[r + 1][col] == 0:
                        return False
        return True
    
    # Backtracking algorithm; As the board is filled from left to right, top to bottom, the algorithm will always not consider all possible solutions.
    def find_solutions(self, row=0, col=0):
        if self.is_solution():
            solution = tuple(tuple(row) for row in self.board)
            if solution not in self.found_solutions:
                self.found_solutions.add(solution)
                self.solutions.append([row[:] for row in self.board])
            return
    
        for r in range(row, self.rows):
            for c in range(col if r == row else 0, self.cols):
                if self.board[r][c] == 0:
                    if self.can_place_domino(r, c, 'horizontal'):
                        self.place_domino(r, c, 'horizontal')
                        if not self.has_row_conflict(r, c, 'horizontal') and not self.has_column_conflict(r, c, 'horizontal'):
                            self.find_solutions(r, c + 2 if c + 2 < self.cols else r + 1)
                        self.remove_domino(r, c, 'horizontal')
                    if self.can_place_domino(r, c, 'vertical'):
                        self.place_domino(r, c, 'vertical')
                        if not self.has_row_conflict(r, c, 'vertical') and not self.has_column_conflict(r, c, 'vertical'):
                            self.find_solutions(r, c + 1 if c + 1 < self.cols else r + 1)
                        self.remove_domino(r, c, 'vertical')

    def remove_domino(self, row, col, direction):
        if direction == 'horizontal':
            self.board[row][col] = 0
            self.board[row][col + 1] = 0
        elif direction == 'vertical':
            self.board[row][col] = 0
            self.board[row + 1][col] = 0

    def print_all_solutions(self):
        print(f"Total solutions: {len(self.solutions)}")
        for i, solution in enumerate(self.solutions):
            print(f"Solution {i + 1}:")
            for row in solution:
                print(row)
            print("\n")

# There would always be solutions not considered, because of the way the algorithm is implemented.
rows = 4
cols = 3
domino_board = DominoBoard(rows, cols)
start_time = time.time()
domino_board.find_solutions()
end_time = time.time()
domino_board.print_all_solutions()


print(f"The algorithm took {end_time - start_time} seconds to find all solutions for a {rows}x{cols} board.")
# O((n*m)^2) time complexity, where n is the number of rows and m is the number of columns in the board
