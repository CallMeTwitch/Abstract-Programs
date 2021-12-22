# #########################
# Sudoku was created in 
# 1783 by Swiss mathematician 
# Leonhard Euler, originally 
# by the name of "Latin 
# Squares". This program 
# recursively tries every 
# combination of numbers 
# until it finds one that 
# works. The three puzzles 
# below all claim to be 
# the "World's Hardest 
# Sudoku". 1 solves in ~5 
# seconds. 2 & 3 take 
# much longer, but only 
# if show == True.
#
# Code written for Code 
# Golf (As short as 
# possiple), efficiency 
# and entertainment.
# #########################

# Imports
from termcolor import colored
import sys

# Check if number placement is valid
def isSafe(grid, row, col, num):
    if num in [grid[row][q] for q in range(9)] or num in [grid[q][col] for q in range(9)] or num in [grid[(row - row % 3) + q][(col - col % 3) + w] for q in range(3) for w in range(3)]:
        return False
    return True

# Print Sudoku to terminal
def print_grid(grid, row, col):
    for _ in range(19): sys.stdout.write("\x1b[1A\x1b[2K")
    output = '+---+---+---+---+---+---+---+---+---+\n'

    for x in range(len(grid)):
        output += ("|" + " {}   {}   {} |" * 3).format(*[str(colored(grid[x][y], 'green')) if x < row or (x == row and y < col) else str(colored(grid[x][y], 'red')) for y in range(len(grid[x]))]) + '\n'
        if x % 3 == 2:
            output += "|" + "---+"*8 + "---|\n"
        else:
            output += "|" + "   +"*8 + "   |\n"

    sys.stdout.write(output)

# Recursive Solve Function
def solveSuduko(grid, row = 0, col = 0, show = False):

    if show:
        print_grid(grid, row, col)        

    if col == 9:
        if row == 8:
            return True
        row += 1
        col = 0
 
    if grid[row][col]: 
        return solveSuduko(grid, row, col + 1, show)

    for num in range(1, 10):
        if isSafe(grid, row, col, num):
           
            grid[row][col] = num
 
            if solveSuduko(grid, row, col + 1, show):
                return True
 
        grid[row][col] = 0
    return False
 
# Sudoku Puzzles
grid1 = [
    [3, 0, 6, 5, 0, 8, 4, 0, 0],
    [5, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 7, 0, 0, 0, 0, 3, 1],
    [0, 0, 3, 0, 1, 0, 0, 8, 0],
    [9, 0, 0, 8, 6, 3, 0, 0, 5],
    [0, 5, 0, 0, 9, 0, 6, 0, 0],
    [1, 3, 0, 0, 0, 0, 2, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 7, 4],
    [0, 0, 5, 2, 0, 6, 3, 0, 0]
]
 
grid2 = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0]
]

grid3 = [
    [0, 0, 5, 3, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 0, 0, 0, 2, 0],
    [0, 7, 0, 0, 1, 0, 5, 0, 0],
    [4, 0, 0, 0, 0, 5, 3, 0, 0],
    [0, 1, 0, 0, 7, 0, 0, 0, 6],
    [0, 0, 3, 2, 0, 0, 0, 8, 0],
    [0, 6, 0, 5, 0, 0, 0, 0, 9],
    [0, 0, 4, 0, 0, 0, 0, 3, 0],
    [0, 0, 0, 0, 0, 9, 7, 0, 0]
]

# Solve
solveSuduko(grid3, show = True)
print_grid(grid3, 9, 9)