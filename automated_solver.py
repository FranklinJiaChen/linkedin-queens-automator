"""
Automated solver for Linkedin's queens puzzle.
"""
from collections import defaultdict
from datetime import datetime
from itertools import combinations
from random import randint
import time

import mss
import pyautogui
from PIL import Image
from pysat.solvers import Glucose3

pyautogui.PAUSE = 0

SMALLEST_SIZE = 7 # smallest size of the puzzle (an educated guess)
LARGEST_SIZE = 12 # largest size of the puzzle (an educated guess)

# Change these coordinates to match the puzzle's location on your screen
START_BUTTON_COORDS = (1100, 1000) # coordinates of the start button
AWAY_FROM_PUZZLE_COORDS = (1100, 400) # coordinates away from the puzzle
PURPLE_POLLING_COORDS = (1100, 400) # coordinates to poll for purple colour

PUZZLE_X = 817
PUZZLE_Y = 429
PUZZLE_WIDTH = 596
PUZZLE_HEIGHT = 596

print_solution = False
load_puzzle = False # set to True if you want to load a puzzle from a file
image = Image.open('./images/old-puzzles/2025-01-01_puzzle.png')

def is_purpleish(colour):
    """
    Check if a colour is purpleish
    """
    return colour[0] > 100 and colour[2] > 100 and colour[1] < 100

def coord_to_index(i: int, j: int) -> int:
    """
    Convert a cell coordinate (i, j) to a unique variable index.

    Parameters:
    i: The row index. Zero-based.
    j: The column index. Zero-based.

    Returns:
    The variable index corresponding to the cell (i, j).
    the index is 1-based and row-major order.
    """
    return i * size + j + 1

def index_to_clicking_coords(index: int) -> tuple[int, int]:
    """
    Convert a variable index to clicking coordinates (x, y).

    Parameters:
    index: The variable index.

    Returns:
    The clicking coordinates of the cell corresponding to the variable index.
    """
    i = (index - 1) // size
    j = (index - 1) % size
    x = (j+1)/(size+1) * PUZZLE_WIDTH + PUZZLE_X
    y = (i+1)/(size+1) * PUZZLE_HEIGHT + PUZZLE_Y
    return x, y

def add_row_clauses(solver: Glucose3) -> Glucose3:
    """
    Add clauses to the solver to ensure that each row has exactly one queen.
    """
    for i in range(size):
        # Each row must have at least one queen
        solver.add_clause([coord_to_index(i, j) for j in range(size)])
        # Each row must have at most one queen
        for j1, j2 in combinations(range(size), 2):
            solver.add_clause([-coord_to_index(i, j1), -coord_to_index(i, j2)])
    return solver

def add_column_clauses(solver: Glucose3) -> Glucose3:
    """
    Add clauses to the solver to ensure that each column has exactly one queen.
    """
    for j in range(size):
        # Each column must have at least one queen
        solver.add_clause([coord_to_index(i, j) for i in range(size)])
        # Each column must have at most one queen
        for i1, i2 in combinations(range(size), 2):
            solver.add_clause([-coord_to_index(i1, j), -coord_to_index(i2, j)])

def add_adjacent_clauses(solver: Glucose3) -> Glucose3:
    """
    Add clauses to the solver to ensure that no two queens are adjacent.
    note: just checks for diagonal adjacency since
          we already row/column clauses check for orthogonal adjacency
    """
    for i in range(size - 1):
        for j in range(size):
            # Check for adjacent lower-right diagonal
            if j < size - 1:
                solver.add_clause([-coord_to_index(i, j),
                                -coord_to_index(i + 1, j + 1)])
            # Check for adjacent lower-left diagonal
            if j > 0:
                solver.add_clause([-coord_to_index(i, j),
                                -coord_to_index(i + 1, j - 1)])

# generate solvers for each size with universal clauses
size_to_solver = {}
for size in range(SMALLEST_SIZE, LARGEST_SIZE+1):
    solver = Glucose3()
    add_row_clauses(solver)
    add_column_clauses(solver)
    add_adjacent_clauses(solver)
    size_to_solver[size] = solver

# Start the puzzle
pyautogui.moveTo(START_BUTTON_COORDS)
pyautogui.click()
pyautogui.moveTo(AWAY_FROM_PUZZLE_COORDS) # avoid hovering over the puzzle
# Wait until the puzzle is loaded by polling the colour of a pixel
while is_purpleish(pyautogui.screenshot().getpixel(PURPLE_POLLING_COORDS)):
    pass

#region eye
eye_start = time.time()

with mss.mss() as sct:
    screenshot = sct.grab({"left": PUZZLE_X, "top": PUZZLE_Y,
                           "width": PUZZLE_WIDTH, "height": PUZZLE_HEIGHT})

if load_puzzle:
    _ = Image.frombytes("RGB", screenshot.size, screenshot.rgb) # simulate time
else:
    image = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

colour_dict = defaultdict(int)

for x in range(0, image.width, randint(7, 10)):
    for y in range(0, image.height, randint(7, 10)):
        r, g, b = image.getpixel((x, y))
        colour_dict[(r, g, b)] += 1

# remove the border colours of black with high occurences
# and many different grey colours with small occurences
unique_colours = sum(1 for value in colour_dict.values() if value > 10) - 1

resized_image = image.resize((unique_colours, unique_colours), Image.NEAREST)

# create a dictionary of {colour: [(i, j), (i, j), ...]}
colour_dict = defaultdict(list)
for x in range(resized_image.width):
    for y in range(resized_image.height):
        r, g, b = resized_image.getpixel((x, y))
        colour_dict[(r, g, b)].append((y, x))

size = unique_colours
print("Eye time: ", time.time()-eye_start)
#endregion

#region brain
brain_start = time.time()
solver = size_to_solver[size] # get the solver for the current size
# Step 4: One queen per colour
colours = colour_dict.values()
for colour in colours:
    # Each colour must have at least one queen
    solver.add_clause([coord_to_index(i, j) for i, j in colour])
    # Each colour must have at most one queen
    for (i1, j1), (i2, j2) in combinations(colour, 2):
        solver.add_clause([-coord_to_index(i1, j1), -coord_to_index(i2, j2)])

solver.solve()
solution = solver.get_model()

if print_solution:
    board = [['.' for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if solution[coord_to_index(i, j) - 1] > 0:
                board[i][j] = 'Q'
    for row in board:
        print("\t" + " ".join(row))
    print()

print("Brain time: ", time.time()-brain_start)
#endregion

#region hand
hand_start = time.time()

for var in solution:
    if var > 0:
        pyautogui.doubleClick(index_to_clicking_coords(var))

print("Hand time:", time.time() - hand_start)
# endregion

print("Total time: ", time.time()-eye_start)
# Save screenshot to a file
current_date = datetime.now().strftime('%Y-%m-%d')
image.save(f'./images/new-attempts/{current_date}_puzzle.png')
