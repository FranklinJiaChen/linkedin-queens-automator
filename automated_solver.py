import pyautogui
from PIL import Image
from datetime import datetime
from collections import defaultdict
from pysat.solvers import Glucose3
from itertools import combinations
from random import randint
import mss
import time

pyautogui.PAUSE = 0
solver = Glucose3()
randomtag = ''.join([chr(randint(97, 122)) for _ in range(5)])
print("attempt tag: ", randomtag) # for debugging with screenshot

def is_purpleish(colour):
    r, g, b = colour
    return r > 100 and g < 100 and b > 100  # Adjust this threshold as needed

# Start the puzzle
pyautogui.moveTo(1100, 1000)
# pyautogui.click()
pyautogui.moveTo(1100, 400) # avoid hovering over the puzzle

# Wait until the color at pixel (1100, 400) is not purpleish
while is_purpleish(pyautogui.screenshot().getpixel((1100, 400))):
    # Get and print the current pixel color
    color = pyautogui.screenshot().getpixel((1100, 400))
    print(color)
    print("waiting")

eye_start = time.time()

# Capture a screenshot of a specific region using mss
screenshot_area = (817, 429, 596, 596)
with mss.mss() as sct:
    screenshot = sct.grab({"left": screenshot_area[0], "top": screenshot_area[1],
                           "width": screenshot_area[2], "height": screenshot_area[3]})

image = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

colour_dict = defaultdict(int)

for x in range(0, image.width, randint(27, 30)):
    for y in range(0, image.height, randint(27, 30)):
        r, g, b = image.getpixel((x, y))
        colour_dict[(r, g, b)] += 1

# count number of unique colours with values > 10
unique_colours = sum(1 for value in colour_dict.values() if value > 10)-1

resized_image = image.resize((unique_colours, unique_colours), Image.NEAREST)

# create a dictionary of {colour: [(x, y), (x, y), ...]}
colour_dict = defaultdict(list)
for x in range(resized_image.width):
    for y in range(resized_image.height):
        r, g, b = resized_image.getpixel((x, y))
        colour_dict[(r, g, b)].append((x, y))

size = unique_colours

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

def index_to_coord(index: int) -> tuple[int, int]:
    """
    Convert a variable index to cell coordinates (i, j).

    Parameters:
    index: The variable index.

    Returns:
    A tuple of row and column indices (i, j).
    """
    return (index - 1) // size, (index - 1) % size

print("Eye time: ", time.time()-eye_start)
brain_start = time.time()

# Generate clauses for Queens constraints
# One queen per row
for i in range(size):
    # Each row must have at least one queen
    solver.add_clause([coord_to_index(i, j) for j in range(size)])

    # Each row must have at most one queen (no two queens in the same row)
    for j1, j2 in combinations(range(size), 2):
        solver.add_clause([-coord_to_index(i, j1), -coord_to_index(i, j2)])

# Step 2: One queen per column
for j in range(size):
    # Each column must have at least one queen
    solver.add_clause([coord_to_index(i, j) for i in range(size)])

    # Each column must have at most one queen (no two queens in the same column)
    for i1, i2 in combinations(range(size), 2):
        solver.add_clause([-coord_to_index(i1, j), -coord_to_index(i2, j)])

# Step 3: No two queens can touch adjacentally
# We just need to add diagonally adjacent constraints
for i in range(size - 1):
    for j in range(size):
        # Check for adjacent lower-right diagonal
        if j < size - 1:
            solver.add_clause([-coord_to_index(i, j), -coord_to_index(i + 1, j + 1)])

        # Check for adjacent lower-left diagonal
        if j > 0:
            solver.add_clause([-coord_to_index(i, j), -coord_to_index(i + 1, j - 1)])


colours = colour_dict.values()
colours = [[(j, i) for i, j in colour] for colour in colours]

# Step 4: One queen per colour
for colour in colours:
    # Each colour must have at most one queen (no two queens in the same colour)
    for (i1, j1), (i2, j2) in combinations(colour, 2):
        solver.add_clause([-coord_to_index(i1, j1), -coord_to_index(i2, j2)])

    # Each colour must have at least one queen
    solver.add_clause([coord_to_index(i, j) for i, j in colour])

solver.solve()
solution = solver.get_model()

show_solution = False
if show_solution:
    board = [['.' for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if solution[coord_to_index(i, j) - 1] > 0:
                board[i][j] = 'Q'
    for row in board:
        print("\t" + " ".join(row))
    print()

print("Brain time: ", time.time()-brain_start)

hand_start = time.time()

# solution = [var+1 for var in solution]
for var in solution:
    if var > 0:
        i, j = index_to_coord(var)
        # double click
        pyautogui.doubleClick((j+1)/(unique_colours+1)*screenshot_area[2] + screenshot_area[0],
                        (i+1)/(unique_colours+1)*screenshot_area[3] + screenshot_area[1])

print("Hand time:", time.time() - hand_start)

print("Total time: ", time.time()-eye_start)

# Save screenshot to a file
current_date = datetime.now().strftime('%Y-%m-%d')
image.save(f'./images/new-attempt/{current_date}_puzzle_{randomtag}.png')
