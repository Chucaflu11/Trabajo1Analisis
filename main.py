import time

class DominoBoard:
    """
    Represents a domino board.

    Attributes:
    - rows (int): The number of rows in the board.
    - cols (int): The number of columns in the board.
    - board (list): A 2D list representing the board.
    - solutions (list): A list to store all the valid solutions found.

    Methods:
    - __init__(self, rows, cols): Initializes a new instance of the DominoBoard class.
    - is_valid_position(self, row, col): Checks if the given position is valid on the board.
    - can_place_domino(self, row, col, direction): Checks if a domino can be placed at the given position and direction.
    - place_domino(self, row, col, direction): Places a domino at the given position and direction.
    - is_solution(self): Checks if the current board configuration is a valid solution.
    - verify_after_placing(self, row, col, direction): Verifies if the current board configuration is valid after placing a domino.
    - find_solutions(self, row=0, col=0, found_solutions=set()): Finds all the valid solutions for the domino board.
    - remove_domino(self, row, col, direction): Removes a domino from the given position and direction.
    - print_all_solutions(self): Prints all the valid solutions found for the domino board.
    """

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
            # Check if there's a vertical tile in the same row
            if 2 in self.board[row]:
                return False
            # Check if there's vertical space in the row for a horizontal tile
            elif 0 in self.board[row]:
                return False
        elif direction == 'vertical':
            # Check if there's a horizontal tile in the same row
            if 1 in self.board[row]:
                return False
            # Check if there's horizontal space to place a vertical tile
            elif col + 1 < self.cols and self.board[row][col:col+2] == [0, 0]:
                return False
        return True

    def has_column_conflict(self, row, col, direction):
        if direction == 'vertical':
            # Check if there's a horizontal tile in the same column
            if any(self.board[r][col] == 1 for r in range(self.rows)):
                return False
            # Check if there's horizontal space in the column for a vertical tile
            elif any(self.board[r][col] == 0 for r in range(self.rows)):
                return False
        elif direction == 'horizontal':
            # Check if there's a vertical tile in the same column
            if any(self.board[r][col] == 2 for r in range(self.rows)):
                return False
            # Check if there's vertical space to place a horizontal tile
            elif row + 1 < self.rows and [self.board[r][col] for r in range(row, min(row + 2, self.rows))] == [0, 0]:
                return False
        return True
    
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

# 4x3 board working, 4x4 not: 2 solutions wrong
rows = 4
cols = 4
domino_board = DominoBoard(rows, cols)
start_time = time.time()
domino_board.find_solutions()
end_time = time.time()
domino_board.print_all_solutions()


print(f"The algorithm took {end_time - start_time} seconds to find all solutions for a {rows}x{cols} board.")
# O((n*m)^2) time complexity, where n is the number of rows and m is the number of columns in the board
