import tkinter as tk
from tkinter import messagebox

# Define colors
WHITE = "#FFFFFF"
BLACK = "#000000"
GRAY = "#C8C8C8"
RED = "#FF0000"

# Board settings
WIDTH = 600
HEIGHT = 600
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE

# Define the Sudoku board
board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

# Sudoku solving functions
def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i
            if solve(bo):
                return True
            bo[row][col] = 0
    return False

def valid(bo, num, pos):
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False
    return True

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)
    return None

def is_solvable(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                for num in range(1, 10):
                    if valid(bo, num, (i, j)):
                        return True
    return False

def reset_board():
    global board
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

# Main game logic and UI
class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.board = board
        self.cells = {}

        self.create_grid()
        self.create_buttons()

    def create_grid(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = tk.Entry(self.root, width=5, font=("Arial", 18), justify="center")
                cell.grid(row=row, column=col, padx=5, pady=5)
                self.cells[(row, col)] = cell

                if self.board[row][col] != 0:
                    cell.insert(tk.END, str(self.board[row][col]))
                    cell.config(state="readonly")
    
    def create_buttons(self):
        solve_button = tk.Button(self.root, text="Solve", command=self.solve_sudoku, font=("Arial", 14))
        solve_button.grid(row=GRID_SIZE, column=0, columnspan=3, pady=10)

        reset_button = tk.Button(self.root, text="Reset", command=self.reset_sudoku, font=("Arial", 14))
        reset_button.grid(row=GRID_SIZE, column=3, columnspan=3, pady=10)

    def solve_sudoku(self):
        new_board = self.get_board_from_entries()
        if is_solvable(new_board):
            solve(new_board)
            self.update_grid(new_board)
        else:
            messagebox.showerror("Error", "This Sudoku puzzle is not solvable.")

    def reset_sudoku(self):
        reset_board()
        self.update_grid(board)

    def get_board_from_entries(self):
        new_board = []
        for row in range(GRID_SIZE):
            new_row = []
            for col in range(GRID_SIZE):
                value = self.cells[(row, col)].get()
                if value == "":  # Empty cell is represented as 0
                    new_row.append(0)
                else:
                    new_row.append(int(value))
            new_board.append(new_row)
        return new_board

    def update_grid(self, new_board):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if new_board[row][col] != 0:
                    self.cells[(row, col)].delete(0, tk.END)
                    self.cells[(row, col)].insert(tk.END, str(new_board[row][col]))

# Create the main window
root = tk.Tk()
app = SudokuApp(root)
root.mainloop()
